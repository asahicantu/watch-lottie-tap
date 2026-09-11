import math

from critter_parts import FRAMES, eye, smile, wiggle
from lottie_kit import (
    animated, ellipse, filled, group, outlined, path, rect, transform,
)


def pig():
    """A storybook piglet. The old one was a flat disc with two hard
    triangles for ears and nothing between the eyes and the snout - no mouth,
    no shaping, and a snout that was a plain oval with two dots punched in.

    Everything here is built round the two things that say `pig` from across a
    watch face: the disc snout, which keeps its sniff, and big floppy ears.
    """
    skin, deep, rim = "#f6a5b8", "#e07f96", "#c9647e"
    inner_c, nostril_c = "#ea8ea6", "#93465d"
    blush_c, mouth_c = "#ef7f9c", "#8f3f57"

    def ear(s, phase):
        """A rounded floppy triangle rather than a hard one, hinged at the
        crown so the whole ear swings and the tip trails behind it."""
        def blade(w, h):
            return path([(-36 * w * s, 8 * h), (6 * w * s, -76 * h),
                         (38 * w * s, 4 * h)], True,
                        tangents=[((-16 * s, 4), (2 * s, -34 * h)),
                                  ((-14 * s, 26), (12 * s, 26)),
                                  ((0, -34 * h), (-18 * s, 6))])
        return group([filled(blade(0.58, 0.56), inner_c,
                             transform(pos=(3 * s, -8)), name="inner"),
                      filled(blade(1.18, 0.94), deep, name="outer")],
                     wiggle((66 * s, -56), base_rot=s * 24, amp=8, period=30,
                            phase=phase), name="ear")

    # the snout keeps its sniff - a squash and stretch on the disc - and gains
    # a rim and a highlight so it sits proud of the face instead of in it
    snout = group(
        [filled(ellipse(19, 26, (-23, 2)), nostril_c,
                transform(rotation=-8), name="nostril"),
         filled(ellipse(19, 26, (23, 2)), nostril_c,
                transform(rotation=8), name="nostril"),
         filled(ellipse(64, 20, (0, -22)), "#f5b3c3", transform(opacity=70),
                name="shine"),
         filled(ellipse(112, 84), deep, name="snout"),
         filled(ellipse(124, 96), rim, name="snout-rim")],
        transform(pos=(0, 30),
                  scale=animated([(0, [100, 100]), (24, [110, 92]), (40, [100, 100]),
                                  (56, [108, 94]), (70, [100, 100]),
                                  (FRAMES, [100, 100])])),
        name="snout-group")

    def brow(s):
        return filled(rect(34, 9, radius=5), rim,
                      transform(pos=(48 * s, -72), rotation=s * -12),
                      name="brow")

    def blush(s):
        return filled(ellipse(50, 30), blush_c,
                      transform(pos=(82 * s, 26), opacity=55), name="blush")

    # the little corkscrew of bristle every cartoon pig has on its crown:
    # a stem, then a spiral of one and a half turns winding tighter
    curl_pts = [(0.0, 0.0)]
    for i in range(1, 16):
        t = i / 15.0
        a = math.pi / 2 + t * 1.5 * 2 * math.pi
        r = 17.0 - 11.0 * t
        curl_pts.append((r * math.cos(a), -24 + r * math.sin(a)))
    curl = outlined(path(curl_pts, False), deep, 7,
                    wiggle((0, -88), amp=6, period=30), name="curl")

    return [
        snout,
        smile(58, 14, y=76, color=mouth_c, w=6),
        brow(-1), brow(1),
        eye((-48, -26), 34, 38, iris="#6b4a3a"),
        eye((48, -26), 34, 38, iris="#6b4a3a"),
        blush(-1), blush(1),
        filled(ellipse(210, 184), skin, name="head"),
        ear(-1, 0.0), ear(1, 0.5),
        curl,
    ]
