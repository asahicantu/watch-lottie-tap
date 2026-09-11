from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def buffalo():
    fur, dark, horns = "#5D4037", "#3E2723", "#D7CCC8"
    muzzle, line, inner_ear = "#795548", "#241714", "#A1887F"

    def horn(side):
        outer = [(0, 16), (side * 20, -1), (side * 58, -19),
                 (side * 82, -58), (side * 48, -43), (side * 22, -19)]
        inner = [(side * 8, 10), (side * 25, -5), (side * 54, -22),
                 (side * 64, -42), (side * 43, -31), (side * 21, -12)]
        return group([
            filled(path(inner), "#F4E7D4", name="horn-highlight"),
            filled(path(outer), horns, name="horn"),
        ], wiggle((side * 63, -57), base_rot=side * 5, amp=4, period=34,
                   phase=0.25 if side > 0 else 0.0), name="horn")

    def ear(side, phase):
        return group([
            filled(ellipse(35, 24, (0, 4)), inner_ear, name="inner-ear"),
            filled(ellipse(60, 42), fur, name="ear"),
        ], wiggle((side * 92, -27), base_rot=side * 10, amp=6, period=26,
                   phase=phase), name="ear")

    mane = group([
        filled(ellipse(28, 39, (-27, 0)), dark, name="left-lock"),
        filled(ellipse(34, 46, (0, -4)), dark, name="middle-lock"),
        filled(ellipse(28, 39, (27, 0)), dark, name="right-lock"),
    ], wiggle((0, -77), amp=4, period=28), name="forelock")

    def foot(x, phase):
        return group([
            filled(ellipse(38, 19, (0, 25)), line, name="hoof"),
            filled(ellipse(40, 54), fur, name="leg"),
        ], wiggle((x, 136), amp=2.5, period=24, phase=phase), name="foot")

    return [
        # Facial details come first so they sit above the rounded head.
        smile(42, 11, y=53, color=line, w=4),
        filled(ellipse(19, 13, (-30, 39)), line, name="left-nostril"),
        filled(ellipse(19, 13, (30, 39)), line, name="right-nostril"),
        filled(ellipse(28, 19, (0, 25)), line, name="nose"),
        dot_eye((-46, -12), 16), dot_eye((46, -12), 16),
        outlined(path([(-69, -34), (-48, -43), (-25, -34)], closed=False), line, 5,
                 name="left-brow"),
        outlined(path([(25, -34), (48, -43), (69, -34)], closed=False), line, 5,
                 name="right-brow"),
        mane,
        filled(ellipse(132, 88, (0, 43)), muzzle, name="muzzle"),
        filled(ellipse(206, 180), fur, name="head"),
        filled(ellipse(110, 48, (0, 104)), "#8D6E63", name="chest"),
        filled(ellipse(180, 118, (0, 96)), dark, name="body-shadow"),
        foot(-62, 0.00), foot(-23, 0.25),
        foot(23, 0.50), foot(62, 0.75),
        ear(-1, 0.0), ear(1, 0.5),
        horn(-1), horn(1),
    ]
