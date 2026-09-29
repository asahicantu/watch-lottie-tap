"""Reusable pieces every feeling face is built from: the flat circular face,
simple dot/line eyes, mouth and brow paths, a few emotion props (tears, sweat,
sparks, hearts), the per-feeling motion signatures, and the wrapper that turns
a list of shape groups into a finished Lottie animation.

Mirrors critter_parts.py's shape (a `<name>()` function per file, wrapped by
one `feeling()` call) but keeps its own, simpler visual language: feelings are
a flat colored circle with a minimal expressive face, not the cartoon-critter
look built from `eye()`/`triangle()`/etc. Deliberately not sharing code with
critter_parts.py beyond the underlying lottie_kit/lottie_bounds primitives -
the two catalogs are stylistically distinct on purpose.
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
FACE_R = 95  # face radius-ish (ellipse w/h)


# --------------------------------------------------------------------------- #
# face + features
# --------------------------------------------------------------------------- #

def face(color):
    return filled(ellipse(FACE_R * 2, FACE_R * 2), color, name="face")


def eye(pos, w=14, h=18, color="#2b2b2b"):
    return filled(ellipse(w, h, pos=(0, 0)), color, tr=transform(pos=pos), name="eye")


def closed_eye(pos, w=16, color="#2b2b2b"):
    verts = [(-w / 2, 0), (w / 2, 0)]
    tangents = [((0, 0), (0, 0)), ((0, 0), (0, 0))]
    p = path(verts, closed=False, tangents=tangents)
    return outlined(p, color, 4, tr=transform(pos=pos), name="closed-eye")


def mouth(verts, color="#2b2b2b", width=6, pos=(0, 0), closed=False):
    p = path(verts, closed=closed)
    return outlined(p, color, width, tr=transform(pos=pos), name="mouth")


def filled_mouth(verts, color="#2b2b2b", pos=(0, 0)):
    p = path(verts, closed=True)
    return filled(p, color, tr=transform(pos=pos), name="mouth")


def brow(pos, angle, w=22, color="#2b2b2b"):
    half = w / 2
    dx = half * math.cos(math.radians(angle))
    dy = half * math.sin(math.radians(angle))
    verts = [(-dx, -dy), (dx, dy)]
    p = path(verts, closed=False, tangents=[((0, 0), (0, 0))] * 2)
    return outlined(p, color, 5, tr=transform(pos=pos), name="brow")


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


def heart_half(pos, rotation, color, name="heart-half"):
    return filled(ellipse(14, 12), color, tr=transform(pos=pos, rotation=rotation),
                  name=name)


def blush(pos, color="#E8636A", name="blush"):
    return filled(ellipse(16, 12), color, tr=transform(pos=pos), name=name)


def std_eyes(spacing=34, y=-8, **kw):
    """The common two-eyes-side-by-side layout most feelings use."""
    return [eye((-spacing / 2, y), **kw), eye((spacing / 2, y), **kw)]


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
