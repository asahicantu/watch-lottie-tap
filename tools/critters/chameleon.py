"""A whole chameleon rather than a green face: body laid out sideways along a
branch, tail coiled at the back, and the head turned to look straight out at
whoever tapped it."""

import math

from critter_parts import FRAMES, eye, nostrils, smile, triangle, wiggle
from lottie_kit import (ellipse, filled, group, oscillate, outlined, path,
                        rect, transform)

SKIN = "#5fbf5c"
SHADE = "#3f9a48"
BAND = "#a5db63"
BELLY = "#d9ef9f"
DARK = "#2c6f36"

BODY = (-24, 6, 200, 140)       # centre x, centre y, width, height
HEAD = (76, -28, 126, 120)


def _on_body(dx, frac):
    """A vertical span `frac` of the body's height, `dx` from its centre.

    Stripes and spots are painted straight onto the body with no clipping, so
    every one of them has to be measured against the ellipse it sits on.
    """
    _, cy, w, h = BODY
    t = max(0.0, 1.0 - (dx / (w / 2.0)) ** 2) ** 0.5
    return h * t * frac


# --------------------------------------------------------------------------- #
# tail
# --------------------------------------------------------------------------- #

def _coil(turns=1.55, r0=52, r1=8, steps=30):
    """Points of a spiral wound in toward its own centre."""
    pts = []
    for i in range(steps + 1):
        f = i / float(steps)
        a = 2 * math.pi * turns * f
        r = r0 + (r1 - r0) * f
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def _tail():
    """Three strokes of falling width stand in for the taper the kit can't
    draw; the tip is drawn first so the inside of the curl sits on top."""
    pts = _coil()
    return group(
        [outlined(path(pts[20:], closed=False), SHADE, 9, name="tip"),
         outlined(path(pts[10:22], closed=False), SKIN, 18, name="mid"),
         outlined(path(pts[:12], closed=False), SKIN, 30, name="base")],
        transform(pos=(-152, 30), rotation=oscillate(FRAMES, 0, 7, 54)),
        name="tail")


# --------------------------------------------------------------------------- #
# legs
# --------------------------------------------------------------------------- #

def _leg(x, y, color, lean, phase, shin=54):
    """One leg ending in the split, pincer-like foot a chameleon grips with."""
    foot = group(
        [filled(rect(40, 18, radius=9), DARK,
                transform(pos=(13, 3), rotation=26), name="toe"),
         filled(rect(40, 18, radius=9), DARK,
                transform(pos=(-13, 3), rotation=-26), name="toe")],
        transform(pos=(0, shin + 20)), name="foot")
    return group(
        [foot,
         filled(rect(30, shin + 14, (0, shin * 0.55), radius=15), color,
                name="shin"),
         filled(ellipse(64, 70), color, name="thigh")],
        wiggle((x, y), base_rot=lean, amp=4, period=36, phase=phase),
        name="leg")


# --------------------------------------------------------------------------- #
# head
# --------------------------------------------------------------------------- #

def _turret(x, period, phase):
    """A cone-shaped eye turret. The pupil is set off-centre, so spinning the
    eyeball inside its cone reads as the eye roaming on its own - the one thing
    everybody knows a chameleon for."""
    return group(
        [group([eye((0, 0), 34, 34, iris="#f0a62c", pupil_offset=(8, 0))],
               transform(rotation=oscillate(FRAMES, 0, 72, period, phase)),
               name="swivel"),
         filled(ellipse(74, 74), SHADE, name="cone"),
         filled(ellipse(88, 86), SKIN, name="turret")],
        transform(pos=(x, -32)), name="turret-eye")


def _casque():
    """The helmet a chameleon wears on the back of its skull. Symmetric,
    because this one is facing us - only the fan above the head shows."""
    return filled(
        path([(12, -44), (76, -118), (140, -44)], closed=True,
             tangents=[((0, 0), (16, -30)), ((-34, 10), (34, 10)),
                       ((-16, -30), (0, 0))]),
        SHADE, name="casque")


def _crest():
    """Saw-tooth ridge running the length of the back, tucking in behind the
    head at the front and under the tail at the back."""
    spikes = []
    for i in range(9):
        f = i / 8.0
        dx = -92 + 152 * f
        spikes.append(filled(
            triangle(18, 30 - 14 * abs(f * 2 - 1), tilt=6), SHADE,
            transform(pos=(BODY[0] + dx, BODY[1] - _on_body(dx, 0.5) + 7)),
            name="spike"))
    return group(spikes, name="crest")


# --------------------------------------------------------------------------- #

def chameleon():
    def band(dx, wide):
        return filled(ellipse(wide, _on_body(dx, 0.88), (BODY[0] + dx, 10)),
                      BAND, name="band")

    return [
        _turret(34, 41, 0.0),
        _turret(118, 37, 0.35),
        # low on the snout, where the eye turrets do not cover them
        group([nostrils(13, 0, 11, 8, DARK)], transform(pos=(76, 4)),
              name="nose"),
        group([smile(98, 15, color=DARK, w=7)], transform(pos=(76, 12)),
              name="mouth"),
        filled(ellipse(102, 48, (76, 12)), BAND, name="chin"),
        filled(ellipse(HEAD[2], HEAD[3], HEAD[:2]), SKIN, name="head"),
        _casque(),
        # near-side legs, in front of the body; the far pair is behind it
        _leg(36, 46, SKIN, -6, 0.0),
        _leg(-76, 44, SKIN, 7, 0.45),
        filled(ellipse(26, 20, (-72, -22)), SHADE, name="spot"),
        filled(ellipse(20, 16, (-6, -32)), SHADE, name="spot"),
        band(-62, 26), band(-20, 30), band(22, 26),
        filled(ellipse(156, 56, (-26, 42)), BELLY, name="belly"),
        filled(ellipse(BODY[2], BODY[3], BODY[:2]), SKIN, name="body"),
        _crest(),
        _leg(12, 40, SHADE, -10, 0.2, shin=46),
        _leg(-98, 38, SHADE, 11, 0.65, shin=46),
        _tail(),
    ]
