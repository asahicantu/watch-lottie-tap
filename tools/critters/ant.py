from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def ant():
    body = "#B22222"
    def leg(x, y, rotation):
        return outlined(path([(0, 0), (x, y)], closed=False), body, 6,
                        wiggle((0, 0), base_rot=rotation, amp=10, period=20), name="leg")

    return [
        dot_eye((-30, -10), 12), dot_eye((30, -10), 12),
        filled(ellipse(100, 80), body, name="head"),
        leg(-60, 40, -30), leg(60, 40, 30),
        leg(-60, 0, -10), leg(60, 0, 10),
        group([filled(ellipse(20, 40, (0, -20)), body)],
              wiggle((-20, -40), base_rot=-20, amp=15, period=25), name="antenna"),
        group([filled(ellipse(20, 40, (0, -20)), body)],
              wiggle((20, -40), base_rot=20, amp=15, period=25, phase=0.5), name="antenna"),
    ]
