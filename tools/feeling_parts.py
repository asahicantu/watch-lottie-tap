"""Reusable pieces every feeling face is built from: a consistent toddler
head (skin, cheeks, a cowlick tuft), a human eye style of its own, mouth and
brow paths, a few emotion props (tears, sweat, sparks, blush, hearts), the
per-feeling motion signatures, and the wrapper that turns a list of shape
groups into a finished Lottie animation.

Mirrors critter_parts.py's shape (a `<name>()` function per file, wrapped by
one `feeling()` call), but every feeling shares the same child character -
only the expression changes. The per-feeling accent color moves to a
background disc behind the head rather than tinting the face itself, so the
colour still reads as a mood cue at a glance while the head stays one
consistent kid throughout the catalog.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lottie_bounds import fit_transform  # noqa: E402
from lottie_kit import (  # noqa: E402
    CENTER, animated, animation, ellipse, filled, group, oscillate, outlined,
    path, shape_layer, transform,
)

FRAMES = 90

# --------------------------------------------------------------------------- #
# the shared child character
# --------------------------------------------------------------------------- #

SKIN = "#F0C29A"
BLUSH_TINT = "#F0908B"  # rosy cheek tint, drawn as a soft translucent-looking disc
HAIR = "#6B4226"
BROW_COLOR = "#4A2E18"
LINE_COLOR = "#3B2A22"   # mouth/lash ink - warm dark brown, not flat black
BACKDROP_R = 128
HEAD_R = 92
CHEEK_DX = 58
CHEEK_DY = 34
CHEEK_R = 22


def backdrop(color):
    """The per-feeling accent colour, now a disc behind the head rather than
    the face itself - keeps the at-a-glance colour cue without recoloring
    the child's skin."""
    return filled(ellipse(BACKDROP_R * 2, BACKDROP_R * 2), color, name="backdrop")


def head():
    """The shared round toddler head: rosy cheeks and a single cowlick curl.
    Every feeling includes this unchanged - only the expression drawn on top
    of it differs."""
    cheek_l = filled(ellipse(CHEEK_R * 2, CHEEK_R * 2), BLUSH_TINT,
                     tr=transform(pos=(-CHEEK_DX, CHEEK_DY), opacity=55), name="cheek")
    cheek_r = filled(ellipse(CHEEK_R * 2, CHEEK_R * 2), BLUSH_TINT,
                     tr=transform(pos=(CHEEK_DX, CHEEK_DY), opacity=55), name="cheek")
    skull = filled(ellipse(HEAD_R * 2, HEAD_R * 2), SKIN, name="skull")
    # a single comma-shaped curl, like a cowlick that loops up and over
    curl = filled(
        path([(-4, 8), (-10, -18), (4, -32), (16, -20), (10, -2)], closed=True,
             tangents=[
                 ((0, 6), (-6, -2)),
                 ((3, 8), (5, -10)),
                 ((-6, -6), (7, -4)),
                 ((3, 7), (-2, 7)),
                 ((4, 6), (0, 0)),
             ]),
        HAIR, tr=transform(pos=(2, -80)), name="tuft")
    return group([curl, cheek_l, cheek_r, skull], name="head")


# --------------------------------------------------------------------------- #
# eyes - a human style of its own: almond white, small dark iris, a thin lash
# line on the upper lid rather than the critter cast's big round cartoon eye
# --------------------------------------------------------------------------- #

def human_eye(pos, w=30, h=24, iris="#4A2E18", blink_at=52, lash=True):
    """One eye: a wide white oval, a large dark iris with a highlight, and
    (unless `lash=False`, for a startled/rounder look) a bold lash arc along
    the upper lid. Simpler geometry than the critter cast's perfectly round
    cartoon eye - wider than tall, with the lash doing the expressive work.
    Blinks once per loop like the critter eyes do."""
    white = filled(ellipse(w, h), "#ffffff", name="white")
    iris_r = h * 0.56
    iris_shape = filled(ellipse(iris_r, iris_r), iris, tr=transform(pos=(0, 2)),
                        name="iris")
    highlight = filled(ellipse(iris_r * 0.4, iris_r * 0.4), "#ffffff",
                       tr=transform(pos=(-iris_r * 0.3, -iris_r * 0.3)),
                       name="highlight")
    parts = [highlight, iris_shape, white]
    if lash:
        lash_arc = outlined(
            path([(-w / 2 * 0.95, -h * 0.1), (0, -h * 0.72), (w / 2 * 0.95, -h * 0.1)],
                 closed=False,
                 tangents=[((0, 0), (w * 0.2, -h * 0.25)),
                           ((-w * 0.2, -h * 0.25), (w * 0.2, -h * 0.25)),
                           ((-w * 0.2, -h * 0.25), (0, 0))]),
            LINE_COLOR, 4, name="lash")
        parts.insert(0, lash_arc)
    scale = blink_scale(blink_at) if blink_at is not None else None
    tr = transform(pos=pos, scale=scale) if scale else transform(pos=pos)
    return group(parts, tr, name="eye")


def blink_scale(at=52, shut=10):
    return animated([
        (0, [100, 100]), (at, [100, 100]), (at + 3, [100, shut]),
        (at + 6, [100, 100]), (FRAMES, [100, 100]),
    ])


def closed_eye(pos, w=22, color=LINE_COLOR):
    verts = [(-w / 2, 0), (0, 2), (w / 2, 0)]
    tangents = [((0, 0), (w * 0.2, 3)), ((-w * 0.2, 3), (w * 0.2, 3)), ((-w * 0.2, 3), (0, 0))]
    p = path(verts, closed=False, tangents=tangents)
    return outlined(p, color, 4, tr=transform(pos=pos), name="closed-eye")


def std_eyes(spacing=46, y=-6, **kw):
    """The common two-eyes-side-by-side layout most feelings use."""
    return [human_eye((-spacing / 2, y), **kw), human_eye((spacing / 2, y), **kw)]


# --------------------------------------------------------------------------- #
# mouth, brows, emotion props
# --------------------------------------------------------------------------- #

def mouth(verts, color=LINE_COLOR, width=6, pos=(0, 0), closed=False, tangents=None):
    p = path(verts, closed=closed, tangents=tangents)
    return outlined(p, color, width, tr=transform(pos=pos), name="mouth")


def filled_mouth(verts, color=LINE_COLOR, pos=(0, 0), tangents=None):
    p = path(verts, closed=True, tangents=tangents)
    return filled(p, color, tr=transform(pos=pos), name="mouth")


def open_mouth(w, h, pos, color=LINE_COLOR, tongue=True):
    """A rounded open-mouth O, with a small tongue hint for a fuller
    expression (surprise, a yawn, a wail)."""
    parts = [filled(ellipse(w, h), color, name="mouth-o")]
    if tongue:
        parts.append(filled(ellipse(w * 0.55, h * 0.4), "#C96B6B",
                            tr=transform(pos=(0, h * 0.22)), name="tongue"))
    return group(parts, tr=transform(pos=pos), name="mouth")


def brow(pos, angle, w=26, color=BROW_COLOR):
    half = w / 2
    dx = half * math.cos(math.radians(angle))
    dy = half * math.sin(math.radians(angle))
    verts = [(-dx, -dy), (dx, dy)]
    p = path(verts, closed=False, tangents=[((0, 0), (0, 0))] * 2)
    return outlined(p, color, 6, tr=transform(pos=pos), name="brow")


def tear(pos, color="#5FB0E8"):
    verts = [(0, -10), (7, 6), (0, 14), (-7, 6)]
    p = path(verts, closed=True)
    return filled(p, color, tr=transform(pos=pos), name="tear")


def sweat(pos, color="#8FD3F4"):
    verts = [(0, -9), (6, 5), (0, 11), (-6, 5)]
    p = path(verts, closed=True)
    return filled(p, color, tr=transform(pos=pos), name="sweat")


def spark(pos, color="#FFE066", size=10):
    verts = [(0, -size), (size * 0.28, -size * 0.28), (size, 0),
             (size * 0.28, size * 0.28), (0, size), (-size * 0.28, size * 0.28),
             (-size, 0), (-size * 0.28, -size * 0.28)]
    p = path(verts, closed=True)
    return filled(p, color, tr=transform(pos=pos), name="spark")


def heart(pos, color, size=20, rotation=0, name="heart"):
    """A single heart silhouette: two lobes over a pointed base."""
    s = size / 20.0
    verts = [(0, 8 * s), (-10 * s, -2 * s), (0, -6 * s), (10 * s, -2 * s)]
    tangents = [
        ((-6 * s, 6 * s), (0, 0)),
        ((0, -8 * s), (-8 * s, -8 * s)),
        ((8 * s, -8 * s), (0, -8 * s)),
        ((0, 0), (6 * s, 6 * s)),
    ]
    return filled(path(verts, closed=True, tangents=tangents), color,
                 tr=transform(pos=pos, rotation=rotation), name=name)


def blush(pos, color="#F0908B", name="blush"):
    return filled(ellipse(20, 13), color, tr=transform(pos=pos), name=name)


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
    return animation(name, [layer], FRAMES)
