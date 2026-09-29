"""Reusable pieces every feeling face is built from: a consistent toddler
head (layered hair with a swept fringe and a cowlick, ears, a button nose,
shaded skin, rosy freckled cheeks), a detailed human eye (lids, lashes,
crease, a ringed iris with pupil and catch-lights), tapered eyebrows, a
family of mouths (smiles, grins with teeth and tongue, gritted teeth, wobbles,
pouts), animated emotion props (falling tears, sliding sweat, twinkles,
floating hearts, Zzz, steam, question marks...), the per-feeling motion
signatures, and the wrapper that turns a list of shape groups into a finished
Lottie animation.

Mirrors critter_parts.py's shape (a `<name>()` function per file, wrapped by
one `feeling()` call), but every feeling shares the same child character -
only the expression changes. The per-feeling accent color moves to a
background disc behind the head rather than tinting the face itself, so the
colour still reads as a mood cue at a glance while the head stays one
consistent kid throughout the catalog.

Coordinates are relative to the canvas centre (y grows downward), and lists
of parts are drawn first-on-top, as everywhere in lottie_kit. Wherever a
feature has a left and a right copy, `side` is -1 for the child's
screen-left and +1 for screen-right; "inner" always means toward the nose.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lottie_kit import (  # noqa: E402
    CENTER, animated, animation, ellipse, filled, group, oscillate, outlined,
    path, shape_layer, transform,
)

FRAMES = 90

# --------------------------------------------------------------------------- #
# palette + layout of the shared child character
# --------------------------------------------------------------------------- #

SKIN = "#F3C6A0"
SKIN_SHADE = "#E2A67E"   # rim shadow, ear hollow, the fringe's cast shadow
SKIN_DEEP = "#C9855F"    # fine lines: nostrils, creases, ear curl, freckles
SKIN_LIGHT = "#FCDDC4"   # nose highlight
LID = "#EAB38D"          # eyelid skin, a touch darker than the face
BLUSH_TINT = "#F28C8C"
HAIR = "#6B4226"
HAIR_DARK = "#4A2C17"
HAIR_LIGHT = "#A0714A"
BROW_COLOR = "#4A2E18"
LINE_COLOR = "#3B2A22"   # mouth/lash ink - warm dark brown, not flat black
IRIS = "#7A4E2D"
IRIS_RIM = "#3F2615"
PUPIL = "#1B110B"
EYE_WHITE = "#FFFFFF"
EYE_SHADOW = "#D9E0EC"   # the lid's shadow across the top of the eye white
MOUTH_DARK = "#5E2426"
TONGUE = "#E8797B"
TONGUE_DARK = "#C4545A"
TEETH = "#FFFFFF"
TEAR = "#6EC1F0"
SWEAT = "#9BD8F6"
GOLD = "#FFE066"

BACKDROP_R = 128
HEAD_R = 92
EYE_DX = 30
EYE_Y = -4
BROW_Y = -30
MOUTH_Y = 48
CHEEK_DX = 56
CHEEK_DY = 30


# --------------------------------------------------------------------------- #
# geometry + animation helpers
# --------------------------------------------------------------------------- #

def curve(points, closed=False, tension=1.0):
    """A smooth (Catmull-Rom) bezier through `points`. A point given as
    (x, y, 0) is a sharp corner instead - lock tips, mouth corners."""
    pts = [(p[0], p[1]) for p in points]
    sharp = [len(p) > 2 and p[2] == 0 for p in points]
    n = len(pts)
    tangents = []
    for i in range(n):
        if sharp[i]:
            tangents.append(((0, 0), (0, 0)))
            continue
        if closed:
            prev, nxt = pts[i - 1], pts[(i + 1) % n]
        else:
            prev, nxt = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx = (nxt[0] - prev[0]) * tension / 6.0
        dy = (nxt[1] - prev[1]) * tension / 6.0
        tangents.append(((-dx, -dy), (dx, dy)))
    return path(pts, closed=closed, tangents=tangents)


def arc(rx, ry, a0, a1, n=6, cx=0.0, cy=0.0):
    """Points along an ellipse, angles in degrees measured clockwise on
    screen from 3 o'clock (so 270 is straight up)."""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def line(points, color=LINE_COLOR, width=4, pos=(0, 0), opacity=100, name="line"):
    """A smooth open stroke through `points`."""
    return outlined(curve(points), color, width,
                    tr=transform(pos=pos, opacity=opacity), name=name)


def _lerp(a, b, k):
    if isinstance(a, (list, tuple)):
        return [x + (y - x) * k for x, y in zip(a, b)]
    return a + (b - a) * k


def cycle(stages, period=FRAMES, delay=0.0):
    """A looping keyframed property. `stages` is [(fraction, value), ...]
    over one period, starting at fraction 0 and ending at 1; the pattern
    repeats every `period` frames (which should divide FRAMES for a seamless
    loop), shifted later by `delay` frames."""
    def at(t):
        f = ((t - delay) % period) / float(period)
        for (f0, v0), (f1, v1) in zip(stages, stages[1:]):
            if f0 <= f <= f1:
                return _lerp(v0, v1, 0 if f1 == f0 else (f - f0) / (f1 - f0))
        return stages[-1][1]

    times = {0.0, float(FRAMES)}
    start = delay - period * math.ceil(delay / float(period))
    while start < FRAMES:
        for f, _ in stages[:-1]:
            t = round(start + f * period, 3)
            if 0 < t < FRAMES:
                times.add(t)
        start += period
    return animated([(t, list(at(t)) if isinstance(stages[0][1], (list, tuple))
                      else at(t)) for t in sorted(times)])


def _offset(pos, stages, period=FRAMES, delay=0.0):
    """Animate a position as `pos` plus a cycling (dx, dy) offset."""
    return cycle([(f, [pos[0] + d[0], pos[1] + d[1]]) for f, d in stages],
                 period, delay)


def uniform(stages, period=FRAMES, delay=0.0):
    """Animate a uniform scale from [(fraction, percent), ...]."""
    return cycle([(f, [s, s]) for f, s in stages], period, delay)


# --------------------------------------------------------------------------- #
# the head
# --------------------------------------------------------------------------- #

# the fringe's lower edge, right to left: rounded notches between sharp lock
# tips, each tip sitting right of its lock's centre so the bangs sweep over
FRINGE = [
    (92, -4, 0), (86, -24), (74, -36, 0), (58, -50), (46, -42, 0), (28, -56),
    (16, -47, 0), (-4, -58), (-16, -48, 0), (-34, -56), (-46, -42, 0),
    (-62, -48), (-74, -34, 0), (-86, -22),
]
LOCK_TIPS = [p for p in FRINGE[1:] if len(p) > 2]


def backdrop(color):
    """The per-feeling accent colour, a disc behind the head rather than the
    face itself - keeps the at-a-glance colour cue without recoloring the
    child's skin."""
    return filled(ellipse(BACKDROP_R * 2, BACKDROP_R * 2), color, name="backdrop")


def _hair_cap_path():
    crown = arc(100, 98, 190, 350, n=8, cy=-8)
    return curve([(-92, -4, 0)] + crown + FRINGE, closed=True)


def _hair():
    cap = filled(_hair_cap_path(), HAIR, name="hair")
    # the same silhouette in skin shadow, dropped a little, is the shade the
    # fringe casts on the forehead
    cast = filled(_hair_cap_path(), SKIN_SHADE,
                  tr=transform(pos=(2, 6), opacity=80), name="hair-shadow")
    strands = []
    for i, (x, y, _) in enumerate(LOCK_TIPS):
        top = (x * 0.3 + 8, -98)
        strands.append(line([top, (x * 0.75 + 6, (top[1] + y) / 2 - 4), (x * 0.95, y - 7)],
                            HAIR_DARK, 2.2, opacity=75, name="strand"))
    shine = [
        line(arc(80, 76, 212, 246, n=4, cy=-8), HAIR_LIGHT, 5, opacity=70, name="shine"),
        line(arc(86, 82, 252, 262, n=2, cy=-8), HAIR_LIGHT, 4, opacity=60, name="shine"),
    ]
    # a single comma-shaped curl, like a cowlick that loops up and over
    curl = group([
        outlined(curve([(0, 2), (-3, -14), (6, -26), (13, -18)]), HAIR_DARK, 2.2,
                 name="curl-line"),
        filled(path([(-4, 8), (-10, -18), (4, -32), (16, -20), (10, -2)], closed=True,
                    tangents=[((0, 6), (-6, -2)), ((3, 8), (5, -10)),
                              ((-6, -6), (7, -4)), ((3, 7), (-2, 7)),
                              ((4, 6), (0, 0))]),
               HAIR, name="curl"),
    ], transform(pos=(2, -90)), name="tuft")
    return group([curl] + shine + strands + [cap, cast], name="hair")


def _ear(side):
    cx, cy = side * 96, 6
    return group([
        line([(cx + side * 1, cy - 12), (cx + side * 9, cy - 6),
              (cx + side * 9, cy + 6), (cx + side * 2, cy + 13)],
             SKIN_DEEP, 2.4, name="ear-curl"),
        filled(ellipse(12, 20), SKIN_SHADE, tr=transform(pos=(cx + side * 2, cy + 1)),
               name="ear-hollow"),
        filled(ellipse(26, 36), SKIN, tr=transform(pos=(cx, cy)), name="ear"),
        filled(ellipse(26, 36), SKIN_SHADE, tr=transform(pos=(cx + side * 2, cy + 3)),
               name="ear-shade"),
    ], name="ear-l" if side < 0 else "ear-r")


def _nose():
    return group([
        line([(-7, 22), (-3, 25), (3, 25), (7, 22)], SKIN_DEEP, 2.5, name="nostrils"),
        filled(ellipse(7, 5), SKIN_LIGHT, tr=transform(pos=(-3, 15)), name="nose-shine"),
        line([(-3, 2), (-6, 10), (-7, 16)], SKIN_SHADE, 2, name="nose-bridge"),
        filled(ellipse(20, 13), SKIN_SHADE, tr=transform(pos=(1, 19), opacity=85),
               name="nose-tip"),
    ], name="nose")


def _cheek(side, opacity=45):
    x, y = side * CHEEK_DX, CHEEK_DY
    freckles = [filled(ellipse(3.6, 3.6), SKIN_DEEP,
                       tr=transform(pos=(x + side * dx, y + dy), opacity=60), name="freckle")
                for dx, dy in ((-9, -6), (-1, -10), (7, -5), (-3, -1))]
    return group(freckles + [
        filled(ellipse(34, 22), BLUSH_TINT, tr=transform(pos=(x, y), opacity=opacity),
               name="cheek"),
    ], name="cheek-l" if side < 0 else "cheek-r")


def head(cheeks=45, tint=None):
    """The shared round toddler head. Every feeling includes this unchanged -
    only the expression drawn on top of it differs. `cheeks` is the blush
    opacity, for the few feelings that want the face a little rosier;
    `tint` is a face_tint() slipped in under the hair, so a mood wash colours
    the skin without staining the fringe."""
    face = filled(ellipse(178, 178), SKIN, tr=transform(pos=(-3, -3)), name="face")
    rim = filled(ellipse(HEAD_R * 2, HEAD_R * 2), SKIN_SHADE, name="face-rim")
    chin = line([(-9, 81), (0, 83), (9, 81)], SKIN_SHADE, 2.5, name="chin")
    return group([_hair()] + ([tint] if tint else []) + [
        _nose(), chin, _cheek(-1, cheeks), _cheek(1, cheeks),
        face, rim, _ear(-1), _ear(1),
    ], name="head")


# --------------------------------------------------------------------------- #
# eyes
# --------------------------------------------------------------------------- #

def blink_scale(at=52, shut=10):
    return animated([
        (0, [100, 100]), (at, [100, 100]), (at + 3, [100, shut]),
        (at + 6, [100, 100]), (FRAMES, [100, 100]),
    ])


def _half_width(rx, ry, y):
    """Where a horizontal line at height `y` crosses the eye's outline."""
    return rx * math.sqrt(max(0.0, 1 - (y / ry) ** 2))


def _iris(ir, color, pupil_scale, shine, glossy, heart_iris):
    if heart_iris:
        return [
            filled(ellipse(ir * 0.28, ir * 0.22), "#ffffff",
                   tr=transform(pos=(-ir * 0.24, -ir * 0.18)), name="highlight"),
            heart((0, 0), "#FF4D6D", size=ir * 1.3, name="heart-iris"),
        ]
    hx, hy = -ir * 0.22, -ir * 0.24
    items = []
    if shine:
        items.append(spark((hx, hy), "#ffffff", size=ir * 0.3, name="highlight"))
    else:
        big = ir * (0.42 if glossy else 0.34)
        items.append(filled(ellipse(big, big), "#ffffff", tr=transform(pos=(hx, hy)),
                            name="highlight"))
    items.append(filled(ellipse(ir * 0.14, ir * 0.14), "#ffffff",
                        tr=transform(pos=(ir * 0.2, ir * 0.2)), name="glint"))
    if glossy:
        items.append(filled(ellipse(ir * 0.56, ir * 0.18), "#ffffff",
                            tr=transform(pos=(0, ir * 0.3), opacity=55), name="sheen"))
    p = ir * 0.46 * pupil_scale
    items += [
        filled(ellipse(p, p), PUPIL, name="pupil"),
        filled(ellipse(ir * 0.82, ir * 0.82), color, name="iris"),
        filled(ellipse(ir, ir), IRIS_RIM, name="iris-rim"),
    ]
    return items


def human_eye(pos, side, w=32, h=28, look=(0, 0), look_path=None, lid=0.0,
              tilt=0.0, lower=0.0, lash=True, iris_scale=1.0, pupil_scale=1.0,
              iris=IRIS, shine=False, glossy=False, heart_iris=False, bags=False,
              blink_at=52):
    """One detailed eye, made of (front to back):

    - lash line + a couple of lash flicks at the outer corner
    - an upper lid in eyelid skin, lowered by `lid` (0 open .. ~0.6 heavy)
      and slanted by `tilt` px (positive drops the outer corner - sad;
      negative drops the inner corner - angry)
    - a lower lid pushed up by `lower` (the cheek-raise of a real smile or a
      squint), or else a faint lower lash line
    - a ringed iris with a pupil and two catch-lights; `shine` swaps the main
      catch-light for a star, `glossy` makes it wet-looking, `heart_iris`
      replaces the iris with a pulsing heart
    - the white, shaded along the top where the lid overhangs it
    - an eyelid crease above, and optional tired `bags` below

    `look` offsets the iris (px); `look_path` is [(fraction, (dx, dy)), ...]
    to animate it instead. Blinks once per loop unless blink_at is None."""
    rx, ry = w / 2.0, h / 2.0
    outer = side                       # +1: outer corner is on the right
    ir = min(h * 0.74, w * 0.62) * iris_scale
    limit = max(0.0, rx - ir / 2 - 1)

    def clamp(d):
        return [max(-limit, min(limit, d[0])), d[1] + 1]

    if look_path:
        iris_pos = cycle([(f, clamp(d)) for f, d in look_path])
    else:
        iris_pos = clamp(look)
    iris_scale_anim = None
    if heart_iris:
        iris_scale_anim = uniform([(0, 100), (0.25, 118), (0.5, 100), (0.75, 118), (1, 100)])
    iris_group = group(_iris(ir, iris, pupil_scale, shine, glossy, heart_iris),
                       transform(pos=iris_pos, scale=iris_scale_anim or (100, 100)),
                       name="iris")

    front = []
    if lid > 0 or tilt:
        base = -ry + lid * h
        y_out = max(-ry, min(ry * 0.6, base + tilt))
        y_in = max(-ry, min(ry * 0.6, base - tilt))
        x_out, x_in = outer * (rx + 2), -outer * (rx + 2)
        mid = (y_in + y_out) / 2 + 1.5
        top = arc(rx + 2, ry + 3, 190, 350, n=6)
        if outer > 0:
            top.reverse()               # run the arc from the outer corner
        lid_shape = curve(top + [(x_in, y_in, 0), (0, mid), (x_out, y_out, 0)],
                          closed=True)
        edge = [(outer * (_half_width(rx, ry, y_out) - 0.5), y_out), (0, mid),
                (-outer * (_half_width(rx, ry, y_in) - 0.5), y_in)]
        if lash:
            front.append(line([edge[0], (edge[0][0] + outer * 6, edge[0][1] - 3)],
                              LINE_COLOR, 2.6, name="lash-flick"))
        front += [
            line(edge, LINE_COLOR, 3.5, name="lash-line"),
            filled(lid_shape, LID, name="lid"),
        ]
    else:
        top = arc(rx + 0.5, ry + 0.5, 195, 345, n=6)
        corner = top[0] if outer < 0 else top[-1]
        second = arc(rx + 0.5, ry + 0.5, 215, 325, n=1)[0 if outer < 0 else 1]
        if lash:
            front += [
                line([corner, (corner[0] + outer * 7, corner[1] - 2)], LINE_COLOR, 2.6,
                     name="lash-flick"),
                line([second, (second[0] + outer * 5, second[1] - 6)], LINE_COLOR, 2.4,
                     name="lash-flick"),
            ]
        front.append(line(top, LINE_COLOR, 3.5 if lash else 2.5, name="lash-line"))

    if lower > 0:
        y_mid = ry - lower * h
        y_end = min(ry * 0.35, y_mid + lower * h * 0.6)
        bottom = arc(rx + 2, ry + 3, 10, 170, n=6)
        front += [
            line([(-_half_width(rx, ry, y_end), y_end), (0, y_mid),
                  (_half_width(rx, ry, y_end), y_end)], SKIN_DEEP, 2, name="lower-lid-line"),
            filled(curve(bottom + [(-rx - 2, y_end, 0), (0, y_mid), (rx + 2, y_end, 0)],
                         closed=True), SKIN, name="lower-lid"),
        ]
    else:
        front.append(line(arc(rx, ry, 30, 150, n=4), SKIN_DEEP, 1.6, opacity=55,
                          name="lower-lash"))

    back = [
        filled(ellipse(w - 1, h - 3), EYE_WHITE, tr=transform(pos=(0, 1.5)), name="white"),
        filled(ellipse(w, h), EYE_SHADOW, name="white-shade"),
        line(arc(rx * 0.85, ry + 5, 215, 325, n=4), SKIN_DEEP, 1.8, opacity=45, name="crease"),
    ]
    if bags:
        back += [
            line(arc(rx * 0.8, ry + 4, 35, 145, n=4), SKIN_DEEP, 2, opacity=70, name="bag"),
            line(arc(rx * 0.55, ry + 8, 50, 130, n=3), SKIN_DEEP, 1.6, opacity=45, name="bag"),
            filled(ellipse(w * 0.9, 10), "#B98A92", tr=transform(pos=(0, ry + 2), opacity=35),
                   name="bag-shadow"),
        ]
    scale = blink_scale(blink_at) if blink_at is not None else (100, 100)
    return group(front + [iris_group] + back, transform(pos=pos, scale=scale),
                 name="eye-l" if side < 0 else "eye-r")


def eyes(left=None, right=None, dx=EYE_DX, y=EYE_Y, **kw):
    """Both eyes, sharing `kw`; `left`/`right` dicts override one side."""
    return [human_eye((-dx, y), -1, **dict(kw, **(left or {}))),
            human_eye((dx, y), 1, **dict(kw, **(right or {})))]


def closed_eye(pos, side, w=28, kind="happy", lash=True, color=LINE_COLOR):
    """A shut eye. `happy` is the upturned arc of a big smile, `calm` the
    downturned sleepy arc with lashes, `squeeze` a tight > < scrunch."""
    rx = w / 2.0
    parts = []
    if kind == "happy":
        parts.append(line([(-rx, 5), (-rx * 0.5, -3), (0, -6), (rx * 0.5, -3), (rx, 5)],
                          color, 4.5, name="lid-arc"))
        if lash:
            parts.append(line([(side * rx, 5), (side * (rx + 5), 1)], color, 2.6,
                              name="lash-flick"))
    elif kind == "calm":
        parts.append(line([(-rx, -2), (-rx * 0.5, 3.5), (0, 5), (rx * 0.5, 3.5), (rx, -2)],
                          color, 4, name="lid-arc"))
        if lash:
            for u in (0.25, 0.6, 0.92):
                x = side * rx * u
                y = 5 - 7 * u * u
                parts.append(line([(x, y + 1), (x + side * 2, y + 6)], color, 2.2,
                                  name="lash"))
        parts.append(line(arc(rx * 0.85, 9, 215, 325, n=4, cy=-2), SKIN_DEEP, 1.8,
                          opacity=45, name="crease"))
    else:  # squeeze
        tip = -side * rx * 0.55
        parts.append(line([(side * rx, -7), (tip, 0, 0), (side * rx, 7)], color, 4.5,
                          name="lid-squeeze"))
    return group(parts, transform(pos=pos), name="closed-eye-l" if side < 0 else "closed-eye-r")


def closed_eyes(dx=EYE_DX, y=EYE_Y, **kw):
    return [closed_eye((-dx, y), -1, **kw), closed_eye((dx, y), 1, **kw)]


# --------------------------------------------------------------------------- #
# brows
# --------------------------------------------------------------------------- #

def brow(pos, side, tilt=0.0, w=30, thick=7, arch=4, color=BROW_COLOR, pos_path=None):
    """A tapered eyebrow: thick at the inner end, fining to a point at the
    tail, bowed up by `arch`. `tilt` in degrees raises the inner end
    (worried/sad) when positive and drags it down (angry) when negative.
    `pos_path` is [(fraction, (dx, dy)), ...] to animate it."""
    n = 6
    top, bottom = [], []
    for i in range(n + 1):
        u = -1 + 2.0 * i / n
        c = -arch * (1 - u * u)
        t = thick * (1 - 0.8 * ((u + 1) / 2) ** 1.4)
        top.append((u * w / 2, c - t / 2))
        bottom.append((u * w / 2, c + t / 2))
    tail = top[-1][0] + 2, (top[-1][1] + bottom[-1][1]) / 2
    pts = top[:-1] + [(tail[0], tail[1], 0)] + list(reversed(bottom[:-1]))

    a = math.radians(tilt)
    turned = []
    for p in pts:
        x, y = p[0], p[1]
        x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        # built with the inner end on the left - right for the left brow
        turned.append((x if side > 0 else -x, y) + tuple(p[2:]))
    where = _offset(pos, pos_path) if pos_path else pos
    return filled(curve(turned, closed=True), color, tr=transform(pos=where),
                  name="brow-l" if side < 0 else "brow-r")


def brows(y=BROW_Y, dx=EYE_DX, left=None, right=None, **kw):
    """Both brows, sharing `kw`; `left`/`right` dicts override one side
    (including its height, as `y`)."""
    def one(side, override):
        opts = dict(kw, **(override or {}))
        return brow((side * dx, opts.pop("y", y)), side, **opts)
    return [one(-1, left), one(1, right)]


# --------------------------------------------------------------------------- #
# mouths
# --------------------------------------------------------------------------- #

def smile(w=34, depth=10, pos=(0, MOUTH_Y), width=5, dimples=True, skew=0.0,
          color=LINE_COLOR, name="mouth"):
    """A closed-mouth curve; negative `depth` makes it a frown. `skew`
    lifts the right corner (negative lifts the left) for a smirk."""
    pts = [(u * w / 2, depth * (1 - u * u) - skew * u) for u in (-1, -0.5, 0, 0.5, 1)]
    parts = [line(pts, color, width, name="lips")]
    if dimples:
        for sx in (-1, 1):
            ex, ey = pts[0] if sx < 0 else pts[-1]
            parts.append(line([(ex - sx * 1, ey - 5), (ex + sx * 3, ey - 1),
                               (ex + sx * 1, ey + 4)], color, 2.6, name="dimple"))
    return group(parts, transform(pos=pos), name=name)


def wavy_mouth(w=28, amp=3, waves=2.0, pos=(0, MOUTH_Y), width=4.5, bend=0.0,
               rotation=0, color=LINE_COLOR):
    """A wobbly line - nerves, embarrassment, confusion."""
    n = int(waves * 4) + 1
    pts = []
    for i in range(n + 1):
        u = -1 + 2.0 * i / n
        pts.append((u * w / 2, amp * math.sin(u * math.pi * waves) + bend * u * u))
    return group([line(pts, color, width, name="lips")],
                 transform(pos=pos, rotation=rotation), name="mouth")


_MOUTH_KINDS = {
    # (top edge, bottom edge), each as a function of u in [-1, 1] and height
    "grin": (lambda u, h: 0.1 * h * (1 - u * u),
             lambda u, h: h * (1 - u * u) ** 0.7),
    "oval": (lambda u, h: -h / 2 * math.sqrt(max(0.0, 1 - u * u)),
             lambda u, h: h / 2 * math.sqrt(max(0.0, 1 - u * u))),
    "wail": (lambda u, h: -h * (1 - u * u) ** 0.7,
             lambda u, h: -0.1 * h * (1 - u * u)),
    "rect": (lambda u, h: -h / 2 * (1 - abs(u) ** 4) ** 0.25,
             lambda u, h: h / 2 * (1 - abs(u) ** 4) ** 0.25),
}


def _band(fn, other, h, t, u_max, below=True, samples=9):
    """A strip of thickness `t` hugging one edge of the mouth, kept to the
    stretch where the mouth is tall enough to hold it."""
    ut = 0.0
    for i in range(1, 101):
        u = u_max * i / 100.0
        if abs(other(u, h) - fn(u, h)) < t + 1.5:
            break
        ut = u
    if ut < 0.15:
        return None
    us = [-ut + 2 * ut * i / (samples - 1) for i in range(samples)]
    s = 1 if below else -1
    edge = [(u, fn(u, h)) for u in us]
    inner = [(u, fn(u, h) + s * t) for u in reversed(us)]
    return edge, inner


def open_mouth(w, h, pos=(0, MOUTH_Y), kind="grin", teeth=True, lower_teeth=False,
               tongue=True, bend=0.0, rotation=0, scale=(100, 100), all_teeth=False):
    """An open mouth: dark interior, lip outline, and optional upper/lower
    teeth and a grooved tongue, all built to follow the mouth's own edges so
    nothing spills outside it. `kind` picks the shape - `grin` (a D, hangs
    down from `pos`), `oval` (centred on `pos`), `wail` (an upside-down D,
    rises from `pos`) or `rect` (a rounded box, for gritted teeth with
    `all_teeth`). `bend` > 0 turns the corners down, < 0 up."""
    top_fn, bot_fn = _MOUTH_KINDS[kind]

    def top(u, hh=h):
        return top_fn(u, hh) + bend * u * u

    def bot(u, hh=h):
        return bot_fn(u, hh) + bend * u * u

    n = 12
    us = [-math.cos(math.pi * i / n) for i in range(n + 1)]
    sharp_ends = kind in ("grin", "wail")
    upper = [(u * w / 2, top(u)) for u in us]
    lower = [(u * w / 2, bot(u)) for u in reversed(us)]
    if sharp_ends:
        upper[0] += (0,)
        upper[-1] += (0,)
    outline = upper + lower[1:-1]

    items = [outlined(curve(outline, closed=True), LINE_COLOR, 3, name="lip-line")]
    if all_teeth:
        mid = [(u * w / 2, (top(u) + bot(u)) / 2) for u in us[1:-1]]
        items.append(line(mid, "#9C8A80", 1.8, name="bite"))
        for u in (-0.6, -0.3, 0, 0.3, 0.6):
            items.append(line([(u * w / 2, top(u) + 1), (u * w / 2, bot(u) - 1)],
                              "#9C8A80", 1.6, name="tooth-gap"))
        items.append(filled(curve(outline, closed=True), TEETH, name="teeth"))
        return group(items, transform(pos=pos, rotation=rotation, scale=scale), name="mouth")

    gap = bot(0) - top(0)
    if teeth:
        band = _band(top, bot, h, gap * 0.24, 0.9)
        if band:
            edge, inner = band
            pts = [(u * w / 2, y) for u, y in edge] + [(u * w / 2, y) for u, y in inner]
            pts[0] += (0,)
            pts[len(edge) - 1] += (0,)
            pts[len(edge)] += (0,)
            pts[-1] += (0,)
            items.append(filled(curve(pts, closed=True), TEETH, name="teeth-top"))
    if lower_teeth:
        band = _band(bot, top, h, gap * 0.18, 0.8, below=False)
        if band:
            edge, inner = band
            pts = [(u * w / 2, y) for u, y in edge] + [(u * w / 2, y) for u, y in inner]
            pts[0] += (0,)
            pts[len(edge) - 1] += (0,)
            pts[len(edge)] += (0,)
            pts[-1] += (0,)
            items.append(filled(curve(pts, closed=True), TEETH, name="teeth-bottom"))
    if tongue:
        tu, th = 0.6, gap * 0.42
        tus = [-tu + 2 * tu * i / 10 for i in range(11)]
        # two lobes: the rounded top dips a little at the centre groove
        crest = [(u * w / 2, bot(u) - th * math.sqrt(max(0.0, 1 - (u / tu) ** 2))
                  + th * 0.22 * math.exp(-(u / 0.12) ** 2)) for u in tus]
        base = [(u * w / 2, bot(u) - 0.5) for u in reversed(tus[1:-1])]
        crest[0] += (0,)
        crest[-1] += (0,)
        items += [
            line([(0, bot(0) - th * 0.72), (0, bot(0) - th * 0.25)], TONGUE_DARK, 2,
                 name="tongue-groove"),
            filled(curve(crest + base, closed=True), TONGUE, name="tongue"),
        ]
    items.append(filled(curve(outline, closed=True), MOUTH_DARK, name="mouth-inside"))
    return group(items, transform(pos=pos, rotation=rotation, scale=scale), name="mouth")


def pout(pos=(0, MOUTH_Y), w=22, rotation=0):
    """A pushed-out lower lip under a small frown."""
    return group([
        line([(-w / 2, 3), (0, -3), (w / 2, 3)], LINE_COLOR, 4.5, name="lips"),
        line([(-w * 0.3, 7), (0, 10), (w * 0.3, 7)], SKIN_DEEP, 2.4, name="lower-lip"),
        filled(ellipse(w * 0.7, 8), "#E59A8E", tr=transform(pos=(0, 5), opacity=80),
               name="lip"),
    ], transform(pos=pos, rotation=rotation), name="mouth")


def tongue_out(pos=(0, MOUTH_Y), w=30, rotation=0):
    """A crooked grimace with the tongue sticking out - "blech"."""
    tongue = group([
        line([(0, 3), (0, 11)], TONGUE_DARK, 2, name="tongue-groove"),
        outlined(curve([(-8, -1, 0), (-9, 9), (0, 17), (9, 9), (8, -1, 0)], closed=True),
                 LINE_COLOR, 2.5, name="tongue-line"),
        filled(curve([(-8, -1, 0), (-9, 9), (0, 17), (9, 9), (8, -1, 0)], closed=True),
               TONGUE, name="tongue"),
    ], transform(pos=(4, 2), rotation=_uniform_rot()), name="tongue")
    lips = line([(-w / 2, -2), (-w / 4, 3), (0, 0), (w / 4, 2), (w / 2, -4)],
                LINE_COLOR, 4.5, name="lips")
    return group([lips, tongue], transform(pos=pos, rotation=rotation), name="mouth")


def _uniform_rot():
    return cycle([(0, -6), (0.5, 6), (1, -6)], period=45)


# --------------------------------------------------------------------------- #
# emotion props
# --------------------------------------------------------------------------- #

def spark(pos, color=GOLD, size=10, rotation=0, name="spark"):
    """A four-point star with pinched, curved sides."""
    s, k = size, size * 0.18
    verts = [(0, -s), (k, -k), (s, 0), (k, k), (0, s), (-k, k), (-s, 0), (-k, -k)]
    return filled(path(verts, closed=True), color,
                  tr=transform(pos=pos, rotation=rotation), name=name)


def twinkle(pos, color=GOLD, size=10, period=45, delay=0):
    """A star that pops in, spins a little and shrinks away, on a loop."""
    return group([spark((0, 0), color, size)], transform(
        pos=pos,
        scale=uniform([(0, 20), (0.35, 110), (0.6, 90), (1, 20)], period, delay),
        rotation=cycle([(0, 0), (1, 90)], period, delay),
    ), name="twinkle")


def heart(pos, color, size=20, rotation=0, name="heart"):
    """A heart silhouette with a small shine: two lobes over a point."""
    s = size / 20.0
    verts = [(0, 8 * s), (-10 * s, -2 * s), (0, -6 * s), (10 * s, -2 * s)]
    tangents = [
        ((-6 * s, 6 * s), (0, 0)),
        ((0, -8 * s), (-8 * s, -8 * s)),
        ((8 * s, -8 * s), (0, -8 * s)),
        ((0, 0), (6 * s, 6 * s)),
    ]
    return group([
        filled(ellipse(4 * s, 3 * s), "#ffffff", tr=transform(pos=(-5 * s, -4 * s), opacity=75),
               name="heart-shine"),
        filled(path(verts, closed=True, tangents=tangents), color, name="heart-body"),
    ], transform(pos=pos, rotation=rotation), name=name)


def float_heart(pos, color="#FF4D6D", size=16, rise=46, drift=10, period=90, delay=0):
    """A heart that swells in, floats upward with a sway, and fades."""
    return group([heart((0, 0), color, size)], transform(
        pos=_offset(pos, [(0, (0, 0)), (0.33, (drift, -rise * 0.33)),
                          (0.66, (-drift * 0.3, -rise * 0.66)), (1, (drift, -rise))],
                    period, delay),
        scale=uniform([(0, 40), (0.25, 100), (1, 100)], period, delay),
        opacity=cycle([(0, 0), (0.15, 100), (0.7, 100), (0.95, 0), (1, 0)], period, delay),
    ), name="float-heart")


def _drop(size, color, outline=None):
    s = size
    body = curve([(0, -1.2 * s, 0), (0.7 * s, 0.25 * s), (0, 1.0 * s), (-0.7 * s, 0.25 * s)],
                 closed=True)
    items = [filled(ellipse(0.28 * s, 0.45 * s), "#ffffff",
                    tr=transform(pos=(-0.25 * s, 0.2 * s), opacity=85), name="drop-shine")]
    if outline:
        items.append(outlined(body, outline, 1.8, name="drop-line"))
    items.append(filled(body, color, name="drop"))
    return items


def tear(pos, fall=38, size=7, period=45, delay=0, color=TEAR):
    """A tear that wells at the eye's corner, runs down the cheek and fades."""
    return group(_drop(size, color), transform(
        pos=_offset(pos, [(0, (0, 0)), (0.18, (0, 0)), (0.8, (0, fall)), (1, (0, fall))],
                    period, delay),
        scale=uniform([(0, 30), (0.18, 100), (1, 100)], period, delay),
        opacity=cycle([(0, 0), (0.1, 100), (0.72, 100), (0.9, 0), (1, 0)], period, delay),
    ), name="tear")


def tear_track(side, color=TEAR):
    """The wet streak a tear leaves down the cheek."""
    x = side * (EYE_DX + 8)
    return line([(x, 10), (x + side * 3, 26), (x + side * 2, 44)], color, 4, opacity=45,
                name="tear-track")


def sweat(pos, size=8, slide=12, period=90, delay=0):
    """A classic anime sweat drop that beads, slides a little, and fades."""
    return group(_drop(size, SWEAT, outline="#4BA3D9"), transform(
        pos=_offset(pos, [(0, (0, 0)), (0.2, (0, 0)), (0.85, (0, slide)), (1, (0, slide))],
                    period, delay),
        scale=uniform([(0, 40), (0.2, 100), (1, 100)], period, delay),
        opacity=cycle([(0, 0), (0.12, 100), (0.75, 100), (0.95, 0), (1, 0)], period, delay),
    ), name="sweat")


def zzz(pos, size=12, rise=34, period=90, delay=0, color="#3B4A6B"):
    """A floating sleepy Z."""
    s = size / 2.0
    z = [(-s, -s, 0), (s, -s, 0), (-s, s, 0), (s, s, 0)]
    return group([outlined(path([p[:2] for p in z], closed=False), color, size * 0.28,
                           name="z")], transform(
        pos=_offset(pos, [(0, (0, 0)), (1, (rise * 0.5, -rise))], period, delay),
        scale=uniform([(0, 40), (0.4, 100), (1, 120)], period, delay),
        rotation=cycle([(0, -10), (0.5, 8), (1, -10)], period, delay),
        opacity=cycle([(0, 0), (0.15, 100), (0.7, 100), (1, 0)], period, delay),
    ), name="zzz")


def steam(pos, side, period=30, delay=0):
    """A puff of hot-headed steam that billows up and away."""
    puff = [
        filled(ellipse(12, 12), "#ffffff", tr=transform(pos=(side * 4, -12)), name="puff"),
        filled(ellipse(16, 16), "#ffffff", tr=transform(pos=(side * 9, -2)), name="puff"),
        filled(ellipse(18, 18), "#ffffff", tr=transform(pos=(0, 0)), name="puff"),
    ]
    return group(puff, transform(
        pos=_offset(pos, [(0, (0, 0)), (1, (side * 10, -18))], period, delay),
        scale=uniform([(0, 40), (0.5, 105), (1, 120)], period, delay),
        opacity=cycle([(0, 0), (0.2, 90), (0.6, 80), (1, 0)], period, delay),
    ), name="steam")


def anger_mark(pos, size=13, color="#D8342C", period=30):
    """The cartoon throbbing vein: four curved corners around a gap."""
    s = size
    arms = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        arms.append(line([(sx * s * 0.25, sy * s), (sx * s * 0.32, sy * s * 0.32),
                          (sx * s, sy * s * 0.25)], color, 3.6, name="vein"))
    return group(arms, transform(
        pos=pos, scale=uniform([(0, 85), (0.2, 118), (0.4, 92), (1, 85)], period),
    ), name="anger-mark")


def question_mark(pos, size=24, color="#FFFFFF", outline=LINE_COLOR, period=45):
    """A bobbing, tilting question mark."""
    s = size
    hook = [(-0.42 * s, -0.5 * s), (-0.2 * s, -0.9 * s), (0.25 * s, -0.88 * s),
            (0.42 * s, -0.55 * s), (0.2 * s, -0.22 * s), (0, -0.05 * s), (0, 0.22 * s)]
    items = [
        filled(ellipse(0.24 * s, 0.24 * s), color, tr=transform(pos=(0, 0.55 * s)), name="dot"),
        filled(ellipse(0.24 * s + 5, 0.24 * s + 5), outline, tr=transform(pos=(0, 0.55 * s)),
               name="dot-edge"),
        outlined(curve(hook), color, 0.16 * s, name="hook"),
        outlined(curve(hook), outline, 0.16 * s + 5, name="hook-edge"),
    ]
    return group(items, transform(
        pos=_offset(pos, [(0, (0, 0)), (0.5, (0, -6)), (1, (0, 0))], period),
        rotation=cycle([(0, -12), (0.5, 12), (1, -12)], period * 2),
    ), name="question")


def shock_lines(pos, side, color=LINE_COLOR, period=30):
    """Three short strokes bursting out beside the head - "!"."""
    items = []
    for a in (-60, -25, 10):
        rad = math.radians(a if side > 0 else 180 - a)
        c, s = math.cos(rad), math.sin(rad)
        items.append(line([(c * 6, s * 6), (c * 18, s * 18)], color, 4, name="shock"))
    return group(items, transform(
        pos=pos, scale=uniform([(0, 70), (0.25, 115), (0.5, 90), (1, 70)], period),
    ), name="shock-lines")


def gloom_lines(color="#5B4B9A", opacity=55, xs=(-36, -18, 0, 18, 36), y=-74, length=26):
    """Vertical strokes hanging over the forehead - dread, or envy in green."""
    items = []
    for i, x in enumerate(xs):
        ln = length * (0.75 if i % 2 else 1.0)
        items.append(line([(x, y), (x, y + ln)], color, 3, opacity=opacity, name="gloom"))
    return group(items, name="gloom")


def stink_lines(pos, color="#6E9F2E", period=45, delay=0):
    """A wavy whiff that rises and fades."""
    wave = [(0, 0), (4, -6), (0, -12), (-4, -18), (0, -24)]
    return group([line(wave, color, 3, name="whiff")], transform(
        pos=_offset(pos, [(0, (0, 6)), (1, (0, -10))], period, delay),
        opacity=cycle([(0, 0), (0.3, 90), (0.7, 70), (1, 0)], period, delay),
    ), name="stink")


def ellipsis(pos, color="#ffffff", period=90):
    """Three dots that appear one after another - "...", waiting on someone."""
    dots = []
    for i in range(3):
        d = i * period * 0.18
        dots.append(filled(ellipse(8, 8), color, tr=transform(
            pos=(i * 13 - 13, 0),
            opacity=cycle([(0, 0), (0.1, 100), (0.6, 100), (0.8, 0), (1, 0)], period, d),
        ), name="dot"))
    return group(dots, transform(pos=pos), name="ellipsis")


def sigh_puff(pos, side, period=90, delay=30):
    """A little breath of air huffed out of the corner of the mouth."""
    puff = [
        filled(ellipse(10, 10), "#ffffff", tr=transform(pos=(side * 8, -3)), name="puff"),
        filled(ellipse(13, 13), "#ffffff", name="puff"),
    ]
    return group(puff, transform(
        pos=_offset(pos, [(0, (0, 0)), (1, (side * 22, 4))], period, delay),
        scale=uniform([(0, 30), (0.3, 100), (1, 130)], period, delay),
        opacity=cycle([(0, 0), (0.15, 85), (0.6, 60), (0.9, 0), (1, 0)], period, delay),
    ), name="sigh")


def blush(pos, w=34, h=20, opacity=75, color=BLUSH_TINT, hatch=True, name="blush"):
    """A strong flush over a cheek, optionally with cartoon hatch strokes."""
    items = []
    if hatch:
        for dx in (-8, 0, 8):
            items.append(line([(dx - 2, 4), (dx + 3, -4)], "#D9606A", 2.2, name="hatch"))
    items.append(filled(ellipse(w, h), color, tr=transform(opacity=opacity), name="flush"))
    return group(items, transform(pos=pos), name=name)


def blushes(**kw):
    return [blush((-CHEEK_DX, CHEEK_DY), name="blush-l", **kw),
            blush((CHEEK_DX, CHEEK_DY), name="blush-r", **kw)]


def face_tint(color, opacity=25, pos=(0, -10), size=(150, 80), pulse_period=None):
    """A translucent wash over part of the face - an angry flush, a queasy
    green, a scared pallor. Pass it to head(tint=...) so it sits under the
    hair, and keep it inside the skull."""
    op = opacity
    if pulse_period:
        op = cycle([(0, opacity * 0.6), (0.5, opacity), (1, opacity * 0.6)], pulse_period)
    return filled(ellipse(*size), color, tr=transform(pos=pos, opacity=op), name="tint")


def nose_wrinkle():
    """Scrunch lines either side of the bridge of the nose."""
    items = []
    for sx in (-1, 1):
        for dy in (0, 6):
            items.append(line([(sx * 6, 4 + dy), (sx * 11, 6 + dy), (sx * 14, 10 + dy)],
                              SKIN_DEEP, 2.2, name="wrinkle"))
    return group(items, name="nose-wrinkle")


def brow_furrow():
    """The pinched creases between angry brows."""
    return group([
        line([(-4, -36), (-2, -30), (-3, -24)], SKIN_DEEP, 2.4, name="furrow"),
        line([(4, -36), (2, -30), (3, -24)], SKIN_DEEP, 2.4, name="furrow"),
    ], name="furrow")


# --------------------------------------------------------------------------- #
# motion signatures
#
# Each takes the finished layer's `ks` block and mutates its p/r/s keyframes in
# place. Distinct per feeling so the deck reads at a glance even before the
# face is legible - "the bouncy one" vs. "the droopy one" - the same way a
# critter's silhouette reads before its face does.
# --------------------------------------------------------------------------- #

def bounce(layer, amp=14, period=45):
    cx, cy = CENTER, CENTER
    keys = []
    n = 16
    for i in range(n + 1):
        t = FRAMES * i / n
        y = cy - abs(amp * math.sin(2 * math.pi * t / period))
        keys.append((t, [cx, y, 0]))
    layer["ks"]["p"] = animated(keys)


def shake(layer, amp=8, period=18):
    cx, cy = CENTER, CENTER
    keys = []
    n = 24
    for i in range(n + 1):
        t = FRAMES * i / n
        x = cx + amp * math.sin(2 * math.pi * t / period)
        keys.append((t, [x, cy, 0]))
    layer["ks"]["p"] = animated(keys)


def sway(layer, amp=10, period=90):
    layer["ks"]["r"] = oscillate(FRAMES, 0, amp, period)


def pulse(layer, base=100, amp=8, period=60):
    scaled = oscillate(FRAMES, base, amp, period, steps=12)
    scaled["k"] = [{**k, "s": [k["s"][0], k["s"][0]]} for k in scaled["k"]]
    layer["ks"]["s"] = scaled


def droop(layer):
    cx, cy = CENTER, CENTER
    layer["ks"]["p"] = animated([
        (0, [cx, cy, 0]), (45, [cx, cy + 10, 0]), (90, [cx, cy, 0]),
    ])
    layer["ks"]["r"] = animated([(0, -3), (45, 3), (90, -3)])


def jitter(layer, amp=5, period=8):
    cx, cy = CENTER, CENTER
    keys = []
    n = 40
    for i in range(n + 1):
        t = FRAMES * i / n
        x = cx + amp * math.sin(2 * math.pi * t / period)
        y = cy + amp * 0.6 * math.cos(2 * math.pi * t / (period * 1.3))
        keys.append((t, [x, y, 0]))
    layer["ks"]["p"] = animated(keys)


def spin_wobble(layer, amp=6, period=70):
    layer["ks"]["r"] = oscillate(FRAMES, 0, amp, period)
    bounce(layer, amp=6, period=period)


# --------------------------------------------------------------------------- #
# wrapper
# --------------------------------------------------------------------------- #

def feeling(name, parts, motion=bounce):
    """Wraps `parts` as a face layer with `motion` applied, matching the
    dimensions/frame-rate/canvas of critter_parts.critter() so both catalogs
    render identically on a watch."""
    layer = shape_layer(name, list(parts), FRAMES)
    motion(layer)
    return _rounded(animation(name, [layer], FRAMES))


def _rounded(value, places=2):
    """Trims float noise from the finished JSON - the curves above produce
    long decimals that would otherwise several-fold the file size for no
    visible difference."""
    if isinstance(value, float):
        r = round(value, places)
        return int(r) if r == int(r) else r
    if isinstance(value, list):
        return [_rounded(v, places) for v in value]
    if isinstance(value, dict):
        return {k: _rounded(v, places) for k, v in value.items()}
    return value
