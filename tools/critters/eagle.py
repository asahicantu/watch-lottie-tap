from critter_parts import eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def eagle():
    head_c, feather_c, beak_c = "#FFFFFF", "#795548", "#FFD54F"
    dark, brow_c = "#5D4037", "#D6CCC2"

    def wing(mirror, phase):
        # the outer edge steps down in three primary feathers
        shape = [(0, -20), (54, -8), (88, 24), (94, 56), (72, 50), (76, 88),
                 (50, 66), (46, 98), (22, 60), (0, 28)]
        verts = [(x * mirror, y) for x, y in shape]
        return group([outlined(path(verts), dark, 4, name="edge"),
                      filled(path(verts), feather_c, name="pinion")],
                     wiggle((86 * mirror, 26), base_rot=6 * mirror, amp=7,
                            period=30, phase=phase), name="wing")

    # the white head ends in a ruff of round feathers over the brown chest
    ruff = [filled(ellipse(40, 36, (x, 64)), "#F4F0EA", name="ruff")
            for x in (-56, -28, 0, 28, 56)]

    return [
        smile(50, 5, y=18, color="#A9791C", w=4),
        filled(ellipse(9, 7, (-16, -2)), dark, name="nostril"),
        filled(ellipse(9, 7, (16, -2)), dark, name="nostril"),
        # one shape for the whole beak: wide at the brow, hooking to a point
        filled(path([(-38, -20), (38, -20), (28, 24), (17, 58), (11, 78),
                     (-11, 78), (-17, 58), (-28, 24)]),
               beak_c, transform(pos=(0, 4)), name="beak"),
        filled(ellipse(30, 26, (0, 80)), "#EFA51C", name="hook"),
        filled(rect(48, 12, radius=6), brow_c,
               transform(pos=(-45, -44), rotation=-16), name="brow"),
        filled(rect(48, 12, radius=6), brow_c,
               transform(pos=(45, -44), rotation=16), name="brow"),
        eye((-42, -18), 34, 38, iris="#F9A825"),
        eye((42, -18), 34, 38, iris="#F9A825"),
        filled(ellipse(168, 152), head_c, name="head"),
    ] + ruff + [
        filled(ellipse(196, 118, (0, 96)), feather_c, name="body"),
        wing(-1, 0.0), wing(1, 0.5),
    ]
