"""A snake coiled on the floor with its head raised out of the middle: a real
spiral rather than two concentric rings, a wedge-shaped skull with brow scales
and saddle markings banding the body."""

import math

from critter_parts import EYE_RIM, FRAMES, RIM_COLOR, blink_scale, eye_size
from lottie_kit import (animated, ellipse, filled, group, oscillate, outlined,
                        path, transform)

SKIN = "#6fbf4a"
DARK = "#3f8a2a"
DEEP = "#2f6a20"
IRIS = "#f2d64f"
TONGUE = "#e2495b"

HEAD_Y = -114.0
HEAD_SCALE = 1.16
COIL = (0.0, 52.0, 1.35, 106.0, 38.0)   # centre x/y, turns, outer r, inner r


# --------------------------------------------------------------------------- #
# the coil
# --------------------------------------------------------------------------- #

def _at(f):
    """A point `f` of the way along the body, tail end first."""
    cx, cy, turns, r0, r1 = COIL
    a1 = -math.pi / 2.0                 # the head end comes out at the top
    a = a1 - 2 * math.pi * turns * (1.0 - f)
    r = r0 + (r1 - r0) * f
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def _heading(f):
    """Which way the body is running there, in degrees."""
    step = 4e-3
    (ax, ay), (bx, by) = _at(max(0.0, f - step)), _at(min(1.0, f + step))
    return math.degrees(math.atan2(by - ay, bx - ax))


def _girth(f):
    """The body is thin at the tail and thick where it leaves the coil."""
    return 18.0 + 26.0 * f


def _body():
    """Three strokes of rising width stand in for a taper the kit can't draw.
    The thick inner winding is listed first, so it sits over the tail."""
    pts = [_at(i / 48.0) for i in range(49)]
    return group(
        [outlined(path(pts[30:], closed=False), SKIN, _girth(0.75), name="near"),
         outlined(path(pts[14:32], closed=False), SKIN, _girth(0.45), name="mid"),
         outlined(path(pts[:16], closed=False), SKIN, _girth(0.14), name="tail")],
        name="coil")


def _saddles():
    """Diamond bands laid along the body, each turned to follow the curve."""
    out = []
    for f in (0.10, 0.26, 0.43, 0.60, 0.78, 0.94):
        x, y = _at(f)
        across = _girth(f) * 0.34
        out.append(filled(
            path([(0, -across), (17, 0), (0, across), (-17, 0)], closed=True),
            DARK, transform(pos=(x, y), rotation=_heading(f)), name="saddle"))
    return group(out, name="saddles")


def _tail_tip():
    """The last hand's-width of tail, flicking clear of the coil."""
    x, y = _at(0.0)
    d = _heading(0.0) + 180.0                # pointing away from the body
    return outlined(
        path([(0, 0), (30, -6), (54, -26)], closed=False,
             tangents=[((0, 0), (10, 0)), ((-10, 2), (10, -2)),
                       ((-10, 6), (0, 0))]),
        SKIN, 11, transform(pos=(x, y), rotation=d), name="tail-tip")


# --------------------------------------------------------------------------- #
# the head
# --------------------------------------------------------------------------- #

def _skull():
    """A shield: wide across the jaw hinges, narrowing to a blunt snout."""
    return path([(-66, -10), (0, -56), (66, -10), (0, 54)], closed=True,
                tangents=[((-6, 22), (-4, -24)), ((-38, -6), (38, -6)),
                          ((4, -24), (6, 22)), ((26, -14), (-26, -14))])


def _eye(x):
    """The house eye, but with a viper's slit where the round pupil goes."""
    w, h = eye_size(30, 34)
    return group(
        [filled(ellipse(11, 11, (-11, -14)), "#ffffff", name="glint"),
         filled(ellipse(5, 5, (10, 12)), "#ffffff", name="spark"),
         filled(ellipse(w * 0.26, h * 0.72), "#241f1a", name="slit"),
         filled(ellipse(w, h), IRIS, name="white"),
         filled(ellipse(w + EYE_RIM, h + EYE_RIM), RIM_COLOR, name="rim")],
        transform(pos=(x, -18), scale=blink_scale()), name="eye")


def _brow(x):
    """The heavy supraocular scale that gives a snake its stare."""
    side = 1 if x > 0 else -1
    return filled(ellipse(52, 17), DEEP,
                  transform(pos=(x, -46), rotation=-side * 12), name="brow")


def _tongue():
    """Forked, stroked rather than filled so the prongs keep their round tips,
    and flicked out twice a loop."""
    prong = lambda side: outlined(
        path([(0, 0), (side * 17, 20)], closed=False,
             tangents=[((0, 0), (side * 3, 9)), ((-side * 7, -4), (0, 0))]),
        TONGUE, 6, transform(pos=(0, 26)), name="prong")
    return group(
        [prong(-1), prong(1),
         outlined(path([(0, 0), (0, 28)], closed=False), TONGUE, 8,
                  name="stem")],
        transform(pos=(0, HEAD_Y + 52 * HEAD_SCALE),
                  scale=animated([(0, [100, 6]), (10, [100, 110]),
                                  (20, [100, 45]), (30, [100, 110]),
                                  (44, [100, 6]), (FRAMES, [100, 6])])),
        name="tongue")


def _head():
    return group(
        [filled(ellipse(9, 8, (-13, 26)), DEEP, name="nostril"),
         filled(ellipse(9, 8, (13, 26)), DEEP, name="nostril"),
         outlined(path([(-37, 12), (0, 33), (37, 12)], closed=False,
                       tangents=[((0, 0), (13, 13)), ((-15, 3), (15, 3)),
                                 ((-13, 13), (0, 0))]),
                  DEEP, 7, name="mouth"),
         _eye(-38), _eye(38),
         _brow(-38), _brow(38),
         filled(_skull(), SKIN, name="skull"),
         # a dark crown patch, tucked behind the skull so only its edge shows
         filled(ellipse(84, 46, (0, -44)), DARK, name="crown")],
        transform(pos=(0, HEAD_Y), scale=(HEAD_SCALE * 100, HEAD_SCALE * 100),
                  rotation=oscillate(FRAMES, 0, 4, 60)),
        name="head")


# --------------------------------------------------------------------------- #

def snake():
    return [
        _tongue(),
        _head(),
        # the neck, bridging the raised head down into the middle of the coil
        outlined(path([(0, HEAD_Y + 30), (0, 14)], closed=False), SKIN, 52,
                 name="neck"),
        _saddles(),
        _body(),
        _tail_tip(),
    ]
