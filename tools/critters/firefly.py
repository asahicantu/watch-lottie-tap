from critter_parts import FRAMES, dot_eye, smile, wiggle
from lottie_kit import animated, ellipse, filled, group, oscillate, outlined, path, transform


def firefly():
    body, shade, cheek_c = "#37474F", "#20292D", "#546069"
    wing_c, wing_vein = "#DCEEF5", "#9DBAC7"
    glow_c, glow_soft, line_c = "#FBC02D", "#FFF3B0", "#151C1F"

    def antenna(side, phase):
        return group([
            filled(ellipse(14, 14, (side * 22, -38)), line_c, name="tip"),
            outlined(path([(0, 0), (side * 10, -22), (side * 22, -38)],
                          closed=False), line_c, 5, name="stalk"),
        ], wiggle((side * 26, -108), base_rot=side * 8, amp=8, period=24,
                   phase=phase), name="antenna")

    def leg(side, y, phase):
        return outlined(
            path([(0, 0), (side * 24, 10), (side * 42, 30)], closed=False,
                 tangents=[((0, 0), (side * 10, 4)),
                           ((side * -8, -4), (side * 8, 8)),
                           ((side * -8, -8), (0, 0))]),
            line_c, 6,
            wiggle((side * 58, y), base_rot=side * 4, amp=6, period=20,
                   phase=phase), name="leg")

    def wing(side, phase):
        return group([
            outlined(path([(0, -8), (0, -72)], closed=False), wing_vein, 3, name="vein"),
            outlined(path([(0, -40), (side * 15, -58)], closed=False), wing_vein, 2, name="vein2"),
            filled(ellipse(50, 88, (0, -44)), wing_c, transform(opacity=76), name="wing"),
        ], transform(pos=(side * 62, -8),
                     rotation=oscillate(FRAMES, side * 10, 18, 7, phase)),
            name="wing-pivot")

    segments = [
        outlined(path([(-w / 2, 0), (0, 5), (w / 2, 0)], closed=False), shade, 4,
                 transform(pos=(0, y), opacity=40), name="segment")
        for y, w in [(40, 84), (68, 92), (96, 82)]
    ]

    glow = group([
        filled(ellipse(112, 94), glow_soft,
               transform(opacity=oscillate(FRAMES, 22, 14, 22),
                         scale=animated([(0, [100, 100]), (10, [118, 118]),
                                        (20, [100, 100]), (FRAMES, [100, 100])])),
               name="halo"),
        filled(ellipse(84, 68), glow_c,
               transform(opacity=oscillate(FRAMES, 72, 26, 22)), name="core"),
    ], transform(pos=(0, 144)), name="glow")

    return [
        smile(30, 9, y=-38, color=shade, w=4),
        dot_eye((-32, -72), 14), dot_eye((32, -72), 14),
        filled(ellipse(20, 12, (-40, -50)), cheek_c, transform(opacity=55), name="cheek"),
        filled(ellipse(20, 12, (40, -50)), cheek_c, transform(opacity=55), name="cheek"),
        antenna(-1, 0.0), antenna(1, 0.5),
        filled(ellipse(120, 98, (0, -70)), body, name="head"),
        glow,
        segments[0], segments[1], segments[2],
        filled(ellipse(94, 76, (0, -8)), body, name="thorax"),
        filled(ellipse(122, 142, (0, 82)), body, name="abdomen"),
        leg(-1, 10, 0.00), leg(1, 10, 0.50),
        leg(-1, 42, 0.25), leg(1, 42, 0.75),
        leg(-1, 74, 0.10), leg(1, 74, 0.60),
        wing(-1, 0.0), wing(1, 0.5),
        filled(ellipse(102, 84, (0, -6)), shade, transform(opacity=45), name="thorax-shadow"),
        filled(ellipse(130, 150, (0, 84)), shade, transform(opacity=45), name="abdomen-shadow"),
    ]
