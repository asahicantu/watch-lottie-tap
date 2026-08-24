"""Measures how much of the canvas a built animation actually covers.

Hand-placed shapes drift: an ear drawn 150 units above the origin sits outside a
300x300 canvas once its group is offset, and the viewer clips it. Rather than
nudging coordinates by hand, `critter()` measures the finished geometry and
applies one corrective transform, so every critter ends up the same size and
centred on the canvas.

The bounds are deliberately conservative — bezier control points rather than the
curve itself, un-rotated boxes for ellipses — so the fit never clips.
"""

import math

# Affine transform as (a, b, c, d, e, f):  x' = a*x + c*y + e,  y' = b*x + d*y + f
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def m_apply(m, point):
    a, b, c, d, e, f = m
    x, y = point
    return (a * x + c * y + e, b * x + d * y + f)


def m_mul(outer, inner):
    """The transform that applies `inner` first, then `outer`."""
    a1, b1, c1, d1, e1, f1 = outer
    a2, b2, c2, d2, e2, f2 = inner
    return (
        a1 * a2 + c1 * b2, b1 * a2 + d1 * b2,
        a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
        a1 * e2 + c1 * f2 + e1, b1 * e2 + d1 * f2 + f1,
    )


def m_translate(x, y):
    return (1.0, 0.0, 0.0, 1.0, x, y)


def m_scale(sx, sy):
    return (sx, 0.0, 0.0, sy, 0.0, 0.0)


def m_rotate(degrees):
    """Lottie rotates clockwise on screen, in a y-down coordinate system."""
    r = math.radians(degrees)
    return (math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0.0, 0.0)


# --------------------------------------------------------------------------- #
# property sampling
# --------------------------------------------------------------------------- #

def value_at(prop, frame):
    """Linear sample of a static or keyframed property. Returns a list."""
    if prop.get("a", 0) == 0:
        k = prop["k"]
        if isinstance(k, dict):
            return k
        return list(k) if isinstance(k, list) else [k]
    keys = prop["k"]
    if frame <= keys[0]["t"]:
        return list(keys[0]["s"])
    for first, second in zip(keys, keys[1:]):
        if first["t"] <= frame <= second["t"]:
            span = second["t"] - first["t"]
            u = 0.0 if span == 0 else (frame - first["t"]) / span
            return [a + (b - a) * u for a, b in zip(first["s"], second["s"])]
    return list(keys[-1]["s"])


def transform_at(tr, frame):
    px, py = value_at(tr["p"], frame)[:2]
    ax, ay = value_at(tr["a"], frame)[:2]
    sx, sy = value_at(tr["s"], frame)[:2]
    rot = value_at(tr["r"], frame)[0]
    return m_mul(
        m_mul(m_translate(px, py), m_rotate(rot)),
        m_mul(m_scale(sx / 100.0, sy / 100.0), m_translate(-ax, -ay)),
    )


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #

def _shape_points(item, frame):
    kind = item["ty"]
    if kind in ("el", "rc"):
        w, h = value_at(item["s"], frame)[:2]
        cx, cy = value_at(item["p"], frame)[:2]
        return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
                (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    if kind == "sh":
        bez = value_at(item["ks"], frame)
        points = []
        for index, vertex in enumerate(bez["v"]):
            vx, vy = vertex
            points.append((vx, vy))
            ix, iy = bez["i"][index]
            ox, oy = bez["o"][index]
            points.append((vx + ix, vy + iy))
            points.append((vx + ox, vy + oy))
        return points
    return []


def _collect(items, frame, matrix, out):
    tr = next((i for i in items if i["ty"] == "tr"), None)
    here = m_mul(matrix, transform_at(tr, frame)) if tr else matrix

    pad = 0.0
    for item in items:
        if item["ty"] == "st":
            pad = max(pad, value_at(item["w"], frame)[0] / 2.0)

    for item in items:
        if item["ty"] == "gr":
            _collect(item["it"], frame, here, out)
        else:
            for point in _shape_points(item, frame):
                for dx, dy in ((-pad, -pad), (pad, -pad), (pad, pad), (-pad, pad)):
                    out.append(m_apply(here, (point[0] + dx, point[1] + dy)))


def bounds(shapes, frames, step=2):
    """(min_x, min_y, max_x, max_y) over the whole animation, in layer space."""
    points = []
    frame = 0
    while frame <= frames:
        for shape in shapes:
            _collect(shape["it"] if shape["ty"] == "gr" else [shape],
                     frame, IDENTITY, points)
        frame += step
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return (min(xs), min(ys), max(xs), max(ys))


def fit_transform(shapes, frames, target, max_scale=1.35):
    """
    Scale and offset that put `shapes` centred inside a `target`-wide square.

    Returns (scale, offset_x, offset_y) in layer space, where the layer origin
    is the centre of the canvas.
    """
    min_x, min_y, max_x, max_y = bounds(shapes, frames)
    width = max(max_x - min_x, 1e-6)
    height = max(max_y - min_y, 1e-6)
    scale = min(target / max(width, height), max_scale)
    centre_x = (min_x + max_x) / 2.0
    centre_y = (min_y + max_y) / 2.0
    return scale, -scale * centre_x, -scale * centre_y
