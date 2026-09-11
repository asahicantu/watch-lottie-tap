from critter_parts import FRAMES, dot_eye, smile, triangle, wiggle
from lottie_kit import (
    ellipse, filled, group, oscillate, outlined, path, rect, transform,
)


def bee():
    def wing(x, phase):
        return group([
            outlined(path([(0, -9), (0, -80)], closed=False), "#B0D5E5", 3,
                     name="wing-vein"),
            outlined(path([(0, -45), (19, -65)], closed=False), "#B0D5E5", 2,
                     name="upper-vein"),
            outlined(path([(0, -43), (-17, -24)], closed=False), "#B0D5E5", 2,
                     name="lower-vein"),
            filled(ellipse(58, 96, (0, -48)), "#eaf4ff", name="wing"),
        ],
                     transform(pos=(x, -46), opacity=78,
                               rotation=oscillate(FRAMES, x * 0.62, 26, 6, phase)),
                     name="wing-pivot")

    def antenna(x, phase):
        return group([filled(ellipse(16, 16, (x * 0.5, -46)), "#3a3226", name="tip"),
                      outlined(path([(0, 0), (x * 0.5, -46)], closed=False),
                               "#3a3226", 6, name="stalk")],
                     wiggle((x, -62), amp=6, period=22, phase=phase), name="antenna")

    def leg(side, y, phase):
        return outlined(
            path([(0, 0), (side * 18, 13), (side * 31, 27)], closed=False,
                 tangents=[((0, 0), (side * 8, 6)),
                           ((side * -7, -5), (side * 8, 7)),
                           ((side * -7, -7), (0, 0))]),
            "#3a3226", 5,
            wiggle((side * 70, y), base_rot=side * 4, amp=6, period=20,
                   phase=phase),
            name="leg")

    return [
        # the face sits above the stripes so neither hides the other
        smile(40, 14, y=-18, color="#3a3226", w=5),
        dot_eye((-34, -46), 15), dot_eye((34, -46), 15),
        filled(ellipse(26, 14, (-57, -20)), "#FFAB91", name="left-cheek"),
        filled(ellipse(26, 14, (57, -20)), "#FFAB91", name="right-cheek"),
        filled(ellipse(48, 22, (0, -7)), "#FFE57F", name="honey-glow"),
        filled(rect(112, 24, (0, 58), radius=12), "#3a3226", name="stripe"),
        filled(rect(150, 24, (0, 22), radius=12), "#3a3226", name="stripe"),
        filled(ellipse(184, 158, (0, 12)), "#ffd21f", name="body"),
        leg(-1, 10, 0.00), leg(1, 10, 0.50),
        leg(-1, 44, 0.20), leg(1, 44, 0.70),
        leg(-1, 75, 0.40), leg(1, 75, 0.90),
        filled(triangle(26, 30), "#3a3226", transform(pos=(0, 116)), name="stinger"),
        antenna(-40, 0.0), antenna(40, 0.5),
        wing(-58, 0.0), wing(58, 0.5),
    ]
