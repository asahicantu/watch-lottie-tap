from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def crayfish():
    shell = "#BF360C"
    def claw(x, phase):
        return group([filled(ellipse(50, 80), shell, name="claw-inner")],
                     wiggle((x, -40), base_rot=x*0.5, amp=20, period=25, phase=phase), name="claw")
    return [
        claw(-80, 0), claw(80, 0.5),
        outlined(path([(-30, -80), (0, -120), (30, -80)], closed=False), shell, 4, name="antenna"),
        dot_eye((-30, -20), 12), dot_eye((30, -20), 12),
        filled(ellipse(120, 180), shell, name="body"),
    ]
