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


# --------------------------------------------------------------------------- #
# eyes
#
# Children read a face eye-first, so every critter shares one big cartoon eye:
# a dark rim, a bright white, an oversized round pupil, a glint high and a
# spark low. Whatever size a critter asks for is blended toward EYE_BASE, so a
# bee and a buffalo come out looking like siblings rather than two unrelated
# drawings. Tune the three constants to restyle all 120 critters at once.
# --------------------------------------------------------------------------- #

EYE_BASE = (46.0, 50.0)   # the shared eye every critter is pulled toward
EYE_MIX = 0.6             # 0 keeps the asked-for size, 1 gives everyone EYE_BASE
EYE_GROW = 1.12           # a final nudge so the whole cast reads bigger
EYE_RIM = 8.0             # outline width, so a white eye survives a pale critter
RIM_COLOR = "#3b322c"
IRIS_COLOR = "#2b2724"
PUPIL_SPAN = 0.66         # pupil diameter as a fraction of the smaller axis


def eye_size(w, h):
    """Blend an asked-for eye size toward the shared cartoon default."""
    bw, bh = EYE_BASE
    return ((w + (bw - w) * EYE_MIX) * EYE_GROW,
            (h + (bh - h) * EYE_MIX) * EYE_GROW)


def blink_scale(at=52, shut=9):
    return animated([
        (0, [100, 100]), (at, [100, 100]), (at + 3, [100, shut]),
        (at + 6, [100, 100]), (FRAMES, [100, 100]),
    ])


def _lum(color):
    h = color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b


def _pale(color):
    """True for a colour light enough to work as the white of an eye."""
    return _lum(color) > 0.62


def eye(pos, w=34, h=38, iris=IRIS_COLOR, white="#ffffff", blink_at=52,
        pupil_offset=(0, 2), highlight=True, rim=RIM_COLOR):
    """The house eye. `w`/`h` are a request, not a promise - see eye_size."""
    w, h = eye_size(w, h)
    d = min(w, h) * PUPIL_SPAN
    px, py = pupil_offset
    parts = []
    if highlight:
        parts.append(filled(ellipse(d * 0.36, d * 0.36,
                                    (px - d * 0.22, py - d * 0.28)),
                            "#ffffff", name="glint"))
        parts.append(filled(ellipse(d * 0.17, d * 0.17,
                                    (px + d * 0.25, py + d * 0.24)),
                            "#ffffff", name="spark"))
    if _lum(iris) > 0.25:
        # a coloured iris needs a pupil of its own, or it reads as a flat disc
        parts.append(filled(ellipse(d * 0.58, d * 0.58, (px, py)), IRIS_COLOR,
                            name="pupil"))
    parts.append(filled(ellipse(d, d, (px, py)), iris, name="iris"))
    parts.append(filled(ellipse(w, h), white, name="white"))
    if rim:
        parts.append(filled(ellipse(w + EYE_RIM, h + EYE_RIM), rim, name="rim"))
    return group(parts, transform(pos=pos, scale=blink_scale(blink_at)),
                 name="eye")


def dot_eye(pos, r=19, color=IRIS_COLOR, blink_at=52):
    """The old plain dot, now drawn as the house eye so the cast matches.

    A pale `color` was chosen to read against a dark critter, so it becomes the
    white of the eye rather than the pupil.
    """
    w = h = r * 2.1
    if _pale(color):
        return eye(pos, w, h, white=color, blink_at=blink_at)
    return eye(pos, w, h, iris=color, blink_at=blink_at)


def pin_eye(pos, r=16, color=IRIS_COLOR, blink_at=52):
    """A plain glinting dot, for the few critters that want a cluster of little
    eyes - a spider - instead of the house pair."""
    return group([filled(ellipse(r * 0.32, r * 0.32, (-r * 0.22, -r * 0.26)),
                         "#ffffff", name="glint"),
                  filled(ellipse(r, r), color, name="dot")],
                 transform(pos=pos, scale=blink_scale(blink_at)), name="pin-eye")


def triangle(base_w, height, tilt=0.0, pos=(0, 0)):
    """Isosceles triangle whose base sits on the group origin, apex pointing up."""
    hw = base_w / 2.0
    verts = [(-hw, 0), (hw, 0), (tilt, -height)]
    return path([(v[0] + pos[0], v[1] + pos[1]) for v in verts], closed=True)


def smile(width=70, drop=26,x=0, y=0, color="#5a3b2e", w=8):
    hw = width / 2.0
    return outlined(
        path([(x - hw, y), (x, y + drop), (x + hw, y)], closed=False,
             tangents=[((0, 0), (hw * 0.35, drop * 0.9)),
                       ((-hw * 0.45, 0), (hw * 0.45, 0)),
                       ((-hw * 0.35, drop * 0.9), (0, 0))]),
        color, w, name="smile")


# --------------------------------------------------------------------------- #
# features several critters share
# --------------------------------------------------------------------------- #

def tuft(x, y, spikes, color, w=22, h=46, spread=26, phase=0.0):
    """A little crest or forelock: a fan of triangles."""
    items = []
    for i in range(spikes):
        offset = (i - (spikes - 1) / 2.0) * spread
        items.append(filled(triangle(w, h - abs(offset) * 0.35, tilt=offset * 0.30),
                            color, transform(pos=(offset, 0)), name="spike"))
    return group(items, wiggle((x, y), amp=5, period=30, phase=phase), name="tuft")


def teeth(count, y, width, size=16, color="#ffffff"):
    items = []
    for i in range(count):
        x = (i - (count - 1) / 2.0) * (width / max(1, count - 1))
        items.append(filled(triangle(size, size * 1.1), color,
                            transform(pos=(x, y), rotation=180), name="tooth"))
    return group(items, name="teeth")


def nostrils(dx, y, w=20, h=14, color="#7a5c4a"):
    return group([filled(ellipse(w, h, (-dx, y)), color, name="nostril"),
                  filled(ellipse(w, h, (dx, y)), color, name="nostril")],
                 name="nostrils")


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
