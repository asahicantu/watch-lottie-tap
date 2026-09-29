import math

from critter_parts import FRAMES, eye, wiggle
from lottie_kit import animated, ellipse, filled, group, outlined, path, transform


def _smooth_tangents(points, closed=True, k=0.24):
    """Catmull-Rom-style handles so a hand-placed polygon reads as a curved
    feather instead of a jagged zig-zag."""
    n = len(points)
    tangents = []
    for i in range(n):
        if closed:
            px, py = points[(i - 1) % n]
            nx, ny = points[(i + 1) % n]
        else:
            px, py = points[i - 1] if i > 0 else points[i]
            nx, ny = points[i + 1] if i < n - 1 else points[i]
        tx, ty = (nx - px) * k, (ny - py) * k
        tangents.append(((-tx, -ty), (tx, ty)))
    return tangents


def _smooth(points, k=0.2):
    return path(points, closed=True, tangents=_smooth_tangents(points, k=k))


def _mirror(half):
    """Right-hand outline (top to bottom) -> the full closed, symmetric shape."""
    return half + [(-x, y) for x, y in reversed(half) if x != 0]


def _petal(base, tip, right_amt, left_amt, t=0.45, bulge=0.42):
    """A pointed leaf/petal: sharp corners at `base` and `tip`, with the two
    edges between them bowed outward - a real feather silhouette, not a
    rounded blob."""
    bx, by = base
    tx, ty = tip
    mx, my = bx + (tx - bx) * t, by + (ty - by) * t
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy)
    px, py = -dy / length, dx / length
    pts = [base, (mx + px * right_amt, my + py * right_amt),
           tip, (mx - px * left_amt, my - py * left_amt)]
    tangents = []
    for i in range(4):
        if i in (0, 2):
            tangents.append(((0, 0), (0, 0)))
        else:
            ppx, ppy = pts[(i - 1) % 4]
            npx, npy = pts[(i + 1) % 4]
            tx2, ty2 = (npx - ppx) * bulge, (npy - ppy) * bulge
            tangents.append(((-tx2, -ty2), (tx2, ty2)))
    return pts, tangents


def _blade(c1, c2, tip, width, steps=10):
    """A curved, tapering feather grown from the origin along a cubic spine
    (origin -> c1 -> c2 -> tip). Fat near the root, needle-sharp at the tip,
    so a tuft of them curls like real down instead of standing up as spikes."""
    def at(t):
        u = 1 - t
        x = 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * tip[0]
        y = 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * tip[1]
        return x, y

    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        x, y = at(t)
        ax, ay = at(max(0.0, t - 0.01))
        bx, by = at(min(1.0, t + 0.01))
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / n, dx / n
        w = width * 0.5 * (1 - t) ** 0.85 * (0.55 + 0.45 * math.sin(math.pi * min(1.0, t * 1.6)))
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + [at(1.0)] + list(reversed(right[:-1]))
    tans = _smooth_tangents(pts, k=0.16)
    tans[steps + 1] = ((0, 0), (0, 0))   # keep the tip pointed
    return path(pts, closed=True, tangents=tans)


def duck():
    head_c, head_shade, head_light, cheek_c = "#FFD93B", "#EDB21C", "#FFF08A", "#FFF3B0"
    bill_c, bill_dark, bill_line = "#F7A233", "#D9701A", "#8C4A0F"
    mouth_c, tongue_c = "#6E2616", "#E8705E"
    tuft_c, tuft_mid, tuft_shade = "#FFE67A", "#FFD23F", "#E8A915"

    def feather(base, tip, right_amt, left_amt, color, **kw):
        pts, tans = _petal(base, tip, right_amt, left_amt, **kw)
        return filled(path(pts, closed=True, tangents=tans), color, name="feather")

    def blade(root, c1, c2, tip, width, color, amp, phase, highlight=None):
        parts = []
        if highlight:
            parts.append(filled(_blade(c1, c2, tip, width * 0.35), highlight,
                                transform(pos=(-width * 0.12, 0), opacity=70),
                                name="blade_shine"))
        parts.append(filled(_blade(c1, c2, tip, width), color, name="blade"))
        # each blade sways on its own root, a beat behind the tuft, so the
        # tips trail the motion like soft down instead of moving as a slab
        return group(parts, wiggle(root, amp=amp, period=30, phase=phase),
                     name="blade")

    # ---- the peak: a swept-forward duckling cowlick -------------------------
    # Five curved down feathers rooted in one spot on the crown. The tall one
    # hooks over into a curl, shorter ones fan out behind it, darker at the
    # back for depth. The whole tuft rocks from its root, and each feather
    # follows through on its own, slightly late.
    peak = group([
        blade((6, 2), (14, -24), (42, -34), (48, -16), 15, tuft_mid, 7, 0.30),
        blade((0, 0), (-16, -72), (62, -100), (48, -54), 30, tuft_c, 5, 0.12,
              highlight="#FFFBD9"),
        blade((-3, 2), (-28, -42), (-18, -82), (10, -84), 22, tuft_mid, 6, 0.20),
        blade((-6, 4), (-34, -22), (-54, -48), (-48, -70), 18, tuft_shade, 8, 0.26),
        blade((3, 2), (34, -36), (16, -64), (36, -74), 17, tuft_shade, 7, 0.36),
], wiggle((-2, -80), amp=5, period=30), name="peak")

    brows = [
        outlined(path([(-12, 3), (0, -4), (12, 3)], closed=False), bill_line, 4,
                 transform(pos=(x, -64), rotation=r, opacity=60), name="brow")
        for x, r in [(-48, -8), (48, 8)]
    ]

    # ---- bill ---------------------------------------------------------------
    # Seen head-on a duck bill is a broad, flat spatula: pinched where it
    # grows out of the face, flared and rounded at the tip, with the mouth
    # line smiling up at the corners.
    upper_shape = _mirror([
        (0, -31), (30, -28), (52, -18), (66, -2), (66, 10),
        (58, 18), (32, 24), (0, 27),
    ])
    upper_bill = group([
        filled(ellipse(40, 10, (-14, -18)), "#FFFFFF",
               transform(opacity=45), name="bill_shine"),
        filled(ellipse(8, 5, (-13, -12)), bill_line, transform(rotation=-18),
               name="nostril"),
        filled(ellipse(8, 5, (13, -12)), bill_line, transform(rotation=18),
               name="nostril"),
        # the hard "nail" at the tip of every real duck's bill
        filled(ellipse(24, 8, (0, 20)), bill_dark, transform(opacity=55),
               name="bill_nail"),
        filled(_smooth(upper_shape), bill_c,
               transform(pos=(0, -3), scale=(95, 90)), name="bill_top"),
        filled(_smooth(upper_shape), bill_dark, name="bill_under"),
    ], transform(pos=(0, 30)), name="upper-bill")

    # the jaw drops from its hinge and the dark mouth opens behind it, so the
    # duck reads as quacking rather than tilting a disc about
    quack = [(0, 0), (10, 1), (20, 0), (30, 1), (40, 0), (FRAMES, 0)]
    lower_bill = filled(
        _smooth(_mirror([(0, 16), (44, 12), (50, 20), (36, 32), (0, 38)])),
        bill_dark,
        transform(pos=animated([(t, [0, 30 + 12 * o]) for t, o in quack])),
        name="lower-bill")
    mouth = group([
        filled(ellipse(40, 14, (0, 10)), tongue_c, name="tongue"),
        filled(ellipse(88, 30, (0, 6)), mouth_c, name="mouth_inside"),
    ], transform(pos=(0, 44), anchor=(0, 0),
                 scale=animated([(t, [100, 15 + 85 * o]) for t, o in quack])),
        name="mouth")

    # ---- head ---------------------------------------------------------------
    head_shape = _mirror([
        (0, -84), (48, -74), (80, -44), (92, -4), (88, 36),
        (66, 70), (32, 88), (0, 92),
    ])

    cheeks = [
        filled(ellipse(40, 28, (x, 16)), cheek_c, transform(opacity=70), name="cheek")
        for x in (-64, 64)
    ] + [
        filled(ellipse(22, 12, (x, 22)), "#FF9F80", transform(opacity=30), name="blush")
        for x in (-66, 66)
    ]

    # fuzzy down poking out past the cheek line, so the head outline reads as
    # fluffy duckling instead of a perfect ball
    fluff = [
        feather((s * 84, y), (s * (84 + dx), y + dy), 5, 5, head_c)
        for s in (-1, 1)
        for y, dx, dy in [(4, 14, 2), (22, 12, 10)]
    ]

    feather_lines = [
        outlined(path([(-10, -4), (0, 0), (10, -4)], closed=False), head_shade, 3,
                 transform(pos=(x, y), opacity=40), name="feather_line")
        for x, y in [(-50, -54), (-28, -66), (28, -66), (50, -54)]
    ]

    chin_shadow = filled(ellipse(96, 18, (0, 64)), "#000000",
                         transform(opacity=12), name="chin_shadow")

    return [
        eye((-46, -20), 34, 38, iris="#3a2a20", blink_at=48),
        eye((46, -20), 34, 38, iris="#3a2a20", blink_at=48),
    ] + brows + [
        upper_bill,
        mouth,
        lower_bill,
    ] + cheeks + feather_lines + [
        chin_shadow,
        filled(ellipse(70, 34, (-22, -52)), head_light,
               transform(rotation=-18, opacity=55), name="head_shine"),
        filled(_smooth(head_shape), head_c,
               transform(pos=(-1, -3), scale=(96, 95)), name="head"),
        filled(_smooth(head_shape), head_shade, name="head_shade"),
        peak,
    ] + fluff
