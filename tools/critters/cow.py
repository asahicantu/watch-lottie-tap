from critter_parts import eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def cow():
    coat, dark, pink = "#F7F3EC", "#3F3833", "#F2AAB4"
    inner_ear, horn_c, line = "#F8BBD0", "#E8DCC2", "#6A4D45"

    def ear(side, phase):
        return group([
            filled(ellipse(38, 22, (0, 3)), inner_ear, name="inner-ear"),
            filled(ellipse(66, 43), "#F2D9A8", name="ear"),
        ], wiggle((side * 102, -18), base_rot=side * 16, amp=6, period=30,
                   phase=phase), name="ear")

    def horn(side, phase):
        return group([
            filled(triangle(15, 27, tilt=side * 3), "#FFF8E1", name="horn-highlight"),
            filled(triangle(27, 39, tilt=side * 6), horn_c, name="horn"),
        ], wiggle((side * 57, -82), base_rot=side * 12, amp=4, period=34,
                   phase=phase), name="horn")

    def foot(x, phase):
        return group([
            filled(ellipse(37, 17, (0, 24)), dark, name="hoof"),
            filled(ellipse(38, 56), coat, name="leg"),
        ], wiggle((x, 140), amp=2, period=25, phase=phase), name="foot")

    tail = group([
        filled(ellipse(22, 28, (15, 48)), dark, name="tail-tuft"),
        outlined(path([(0, 0), (8, 32), (15, 48)], closed=False), line, 6,
                 name="tail-stalk"),
    ], wiggle((95, 74), base_rot=18, amp=8, period=28), name="tail")

    return [
        smile(44, 12, y=59, color=line, w=4),
        filled(ellipse(20, 14, (26, 46)), "#C4707C", name="right-nostril"),
        filled(ellipse(20, 14, (-26, 46)), "#C4707C", name="left-nostril"),
        filled(ellipse(122, 84, (0, 44)), pink, name="muzzle"),
        eye((-46, -28), 34, 38),
        eye((46, -28), 34, 38),
        filled(ellipse(56, 46, (58, 42)), dark, name="right-face-spot"),
        filled(ellipse(64, 54, (-56, -50)), dark, name="left-face-spot"),
        filled(ellipse(192, 172), coat, name="head"),
        filled(ellipse(72, 38, (-52, 106)), dark, name="left-body-spot"),
        filled(ellipse(58, 34, (54, 85)), dark, name="right-body-spot"),
        filled(ellipse(110, 50, (0, 108)), "#FFFFFF", name="chest"),
        filled(ellipse(188, 132, (0, 96)), coat, name="round-body"),
        filled(ellipse(204, 144, (0, 103)), "#D7D2C9", name="body-shadow"),
        foot(-62, 0.00), foot(-22, 0.25),
        foot(22, 0.50), foot(62, 0.75),
        ear(-1, 0.0), ear(1, 0.5),
        horn(-1, 0.0), horn(1, 0.5), tail,
    ]
