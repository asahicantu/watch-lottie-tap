from critter_parts import eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def camel():
    fur, shade, muzzle = "#C2B280", "#8D7A58", "#E4D5A6"
    line, inner_ear, glow = "#5F513A", "#D6C48C", "#F0E1AE"

    def ear(side, phase):
        return group([
            filled(ellipse(23, 38, (0, -4)), inner_ear, name="inner-ear"),
            filled(ellipse(42, 62), fur, name="ear"),
        ], wiggle((side * 77, -51), base_rot=side * 12, amp=6, period=28,
                   phase=phase), name="ear")

    def hump(x, phase):
        return group([
            filled(ellipse(46, 22, (0, -10)), glow, name="hump-highlight"),
            filled(ellipse(86, 88), fur, name="hump"),
            filled(ellipse(97, 98, (0, 7)), shade, name="hump-shadow"),
        ], wiggle((x, 40), amp=3, period=30, phase=phase), name="hump")

    def foot(x, phase):
        return group([
            filled(ellipse(35, 18, (0, 29)), line, name="hoof"),
            filled(ellipse(36, 62), fur, name="leg"),
        ], wiggle((x, 139), amp=2, period=25, phase=phase), name="foot")

    forelock = group([
        filled(ellipse(26, 34, (-22, 0)), shade, name="left-lock"),
        filled(ellipse(30, 40, (0, -5)), shade, name="middle-lock"),
        filled(ellipse(26, 34, (22, 0)), shade, name="right-lock"),
    ], wiggle((0, -83), amp=3, period=30), name="forelock")

    return [
        # Foreground details stay above the long, rounded face.
        smile(44, 12, y=51, color=line, w=4),
        filled(ellipse(17, 12, (-27, 36)), line, name="left-nostril"),
        filled(ellipse(17, 12, (27, 36)), line, name="right-nostril"),
        filled(ellipse(25, 17, (0, 23)), line, name="nose"),
        eye((-42, -16), 34, 40, iris="#5D4037"),
        eye((42, -16), 34, 40, iris="#5D4037"),
        outlined(path([(-66, -39), (-44, -47), (-23, -39)], closed=False), line, 4,
                 name="left-brow"),
        outlined(path([(23, -39), (44, -47), (66, -39)], closed=False), line, 4,
                 name="right-brow"),
        forelock,
        filled(ellipse(122, 82, (0, 42)), muzzle, name="muzzle"),
        filled(ellipse(168, 166, (0, -13)), fur, name="head"),
        filled(ellipse(93, 43, (0, 102)), glow, name="chest"),
        filled(ellipse(188, 132, (0, 94)), fur, name="round-body"),
        filled(ellipse(204, 144, (0, 101)), shade, name="body-shadow"),
        foot(-62, 0.00), foot(-22, 0.25),
        foot(22, 0.50), foot(62, 0.75),
        ear(-1, 0.0), ear(1, 0.5),
        hump(-48, 0.0), hump(48, 0.5),
    ]
