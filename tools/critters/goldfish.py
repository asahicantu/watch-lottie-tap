from critter_parts import eye, wiggle
from lottie_kit import ellipse, filled


def goldfish():
    body = "#FF9800"
    def fin(pos, rot, phase):
        return filled(ellipse(60, 40), "#FB8C00",
                      wiggle(pos, base_rot=rot, amp=20, period=20, phase=phase), name="fin")

    return [
        eye((-50, -10), 45, 45, iris="#000000"),
        eye((50, -10), 45, 45, iris="#000000"),
        filled(ellipse(180, 160), body, name="body"),
        fin((-80, 40), 30, 0), fin((80, 40), -30, 0.5),
        filled(ellipse(100, 120, (0, 80)), body, wiggle((0, 0), amp=10, period=30), name="tail"),
    ]
