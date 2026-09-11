from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect


def badger():
    fur, dark, stripe = "#455A64", "#263238", "#ECEFF1"
    inner_ear, muzzle, line = "#90A4AE", "#CFD8DC", "#1B252B"

    def ear(side, phase):
        return group([
            filled(ellipse(28, 28, (0, 4)), inner_ear, name="inner-ear"),
            filled(ellipse(54, 58), fur, name="ear"),
        ], wiggle((side * 70, -67), base_rot=side * 15, amp=8, period=26,
                   phase=phase), name="ear")

    return [
        # The face is listed first to keep its markings above the fur.
        smile(38, 11, y=35, color=line, w=4),
        filled(ellipse(25, 17, (0, 23)), line, name="nose"),
        filled(ellipse(56, 30, (0, 29)), muzzle, name="muzzle"),
        outlined(path([(0, 30), (0, 35)], closed=False), line, 4,
                 name="nose-bridge"),
        dot_eye((-39, -8), 13), dot_eye((39, -8), 13),
        filled(ellipse(68, 59, (-42, -5)), dark, name="left-mask"),
        filled(ellipse(68, 59, (42, -5)), dark, name="right-mask"),
        filled(ellipse(55, 21, (0, -58)), "#FFFFFF", name="forehead-highlight"),
        filled(rect(43, 137, (0, -6), radius=20), stripe, name="forehead-stripe"),
        filled(ellipse(180, 160), fur, name="head"),
        filled(ellipse(68, 37, (0, 91)), stripe, name="chest"),
        filled(ellipse(132, 82, (0, 80)), fur, name="body"),
        filled(ellipse(148, 94, (0, 85)), dark, name="body-shadow"),
        ear(-1, 0.0), ear(1, 0.5),
    ]
