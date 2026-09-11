from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect


def crab():
    body_c = "#E53935"
    def claw(x, ph):
        return group([filled(ellipse(50, 40, (0, -20)), body_c, name="pincer"),
                      filled(rect(15, 40, (0, 20), radius=7), body_c, name="arm")],
                     wiggle((x, -40), base_rot=x*0.2, amp=20, period=25, phase=ph), name="claw")
    return [
        claw(-100, 0.0), claw(100, 0.5),
        dot_eye((-30, -70), 10), dot_eye((30, -70), 10),
        outlined(path([(-30, -40), (-30, -70)], False), body_c, 4, name="stalk"),
        outlined(path([(30, -40), (30, -70)], False), body_c, 4, name="stalk"),
        filled(ellipse(180, 120), body_c, name="body"),
    ]
