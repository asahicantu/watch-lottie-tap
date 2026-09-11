from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, path, rect


def lobster():
    body_c = "#E64A19"
    def claw(x, ph):
        return group([filled(path([(0, 0), (20, -30), (40, 0), (20, 10)], True), body_c, name="pincer"),
                      filled(rect(12, 50, (0, 30), radius=6), body_c, name="arm")],
                     wiggle((x, -30), base_rot=x*0.3, amp=20, period=25, phase=ph), name="claw")
    return [
        claw(-110, 0.0), claw(110, 0.5),
        dot_eye((-30, -60), 12), dot_eye((30, -60), 12),
        filled(ellipse(140, 180), body_c, name="body"),
        filled(rect(100, 20, (0, 60), radius=10), body_c, name="segment"),
    ]
