"""Reusable pieces every critter is built from: the idle motion, eyes that
blink, ears that wiggle, and the wrapper that turns a list of shape groups into
a finished Lottie animation."""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lottie_bounds import fit_transform  # noqa: E402
from lottie_kit import (  # noqa: E402
    animated, animation, ellipse, filled, group, oscillate, outlined, path,
    shape_layer, static, transform,
)

FRAMES = 90

# Every critter is scaled to sit inside a square this wide, centred on the
# canvas. It leaves a small margin inside the 300x300 canvas so a stroke or a
# rotating ear never touches the edge, and it means an elephant and a mouse
# arrive on screen the same size instead of one filling it and one floating in
# the middle of it.
FIT_BOX = 272.0


def bob_transform(amp=9.0, period=48.0, rot=3.5, pop=True):
    """The whole-critter idle: a soft float plus a pop-in on the first frames."""
    keys = []
    steps = 16
    for i in range(steps + 1):
        t = FRAMES * i / steps
        keys.append((t, [0.0, amp * math.sin(2 * math.pi * t / period)]))
    scale = (
        animated([(0, [58, 58]), (7, [112, 112]), (13, [96, 96]),
                  (19, [100, 100]), (FRAMES, [100, 100])])
        if pop else static([100, 100])
    )
    return transform(pos=animated(keys),
                     rotation=oscillate(FRAMES, 0, rot, period * 2),
                     scale=scale)


def wiggle(pos, base_rot=0.0, amp=8.0, period=30.0, phase=0.0, scale=(100, 100)):
    return transform(pos=pos, scale=scale,
                     rotation=oscillate(FRAMES, base_rot, amp, period, phase))


def blink_scale(at=52, shut=9):
    return animated([
        (0, [100, 100]), (at, [100, 100]), (at + 3, [100, shut]),
        (at + 6, [100, 100]), (FRAMES, [100, 100]),
    ])


def eye(pos, w=34, h=38, iris="#2f2a26", white="#ffffff", blink_at=52,
        pupil_offset=(0, 2), highlight=True):
    parts = []
    if highlight:
        parts.append(filled(ellipse(w * 0.30, h * 0.30,
                                    (pupil_offset[0] - w * 0.16,
                                     pupil_offset[1] - h * 0.20)),
                            "#ffffff", name="glint"))
    parts.append(filled(ellipse(w * 0.58, h * 0.62, pupil_offset), iris, name="iris"))
    parts.append(filled(ellipse(w, h), white, name="white"))
    return group(parts, transform(pos=pos, scale=blink_scale(blink_at)), name="eye")


def dot_eye(pos, r=19, color="#2b2724", blink_at=52):
    return group([filled(ellipse(r * 0.32, r * 0.32, (-r * 0.22, -r * 0.26)),
                         "#ffffff", name="glint"),
                  filled(ellipse(r, r), color, name="dot")],
                 transform(pos=pos, scale=blink_scale(blink_at)), name="eye")


def triangle(base_w, height, tilt=0.0, pos=(0, 0)):
    """Isosceles triangle whose base sits on the group origin, apex pointing up."""
    hw = base_w / 2.0
    verts = [(-hw, 0), (hw, 0), (tilt, -height)]
    return path([(v[0] + pos[0], v[1] + pos[1]) for v in verts], closed=True)


def smile(width=70, drop=26, y=0, color="#5a3b2e", w=8):
    hw = width / 2.0
    return outlined(
        path([(-hw, y), (0, y + drop), (hw, y)], closed=False,
             tangents=[((0, 0), (hw * 0.35, drop * 0.9)),
                       ((-hw * 0.45, 0), (hw * 0.45, 0)),
                       ((-hw * 0.35, drop * 0.9), (0, 0))]),
        color, w, name="smile")


def critter(name, parts, extra_layers=None):
    """Wraps `parts` in the idle motion, then scales the result to [FIT_BOX]."""
    root = group(parts, bob_transform(), name=name)
    scale, offset_x, offset_y = fit_transform([root], FRAMES, FIT_BOX)
    fitted = group(
        [root],
        transform(pos=(offset_x, offset_y), scale=(scale * 100, scale * 100)),
        name="fit")
    layers = [shape_layer(name, [fitted], FRAMES, index=1)]
    if extra_layers:
        layers = list(extra_layers) + layers
    return animation(name, layers, FRAMES)
