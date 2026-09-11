from critter_parts import eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def cockatoo():
    feathers, shade, crest = "#ECEFF1", "#B0BEC5", "#FFF176"
    beak, deep, cheek = "#607D8B", "#37474F", "#FFCCBC"

    def wing(side, phase):
        return group([
            outlined(path([(0, -40), (side * 12, 4), (0, 48)], closed=False),
                     "#90A4AE", 3, name="wing-seam"),
            filled(ellipse(58, 112), shade, name="wing"),
        ], wiggle((side * 78, 47), base_rot=side * 12, amp=10, period=26,
                   phase=phase), name="wing")

    def foot(x, phase):
        return group([
            filled(ellipse(34, 15, (0, 18)), deep, name="toes"),
            filled(ellipse(20, 35), "#90A4AE", name="leg"),
        ], wiggle((x, 139), amp=2, period=24, phase=phase), name="foot")

    crest_feathers = group([
        filled(path([(-12, 0), (2, -62), (16, 0)], closed=True), crest,
               name="centre-crest"),
        filled(path([(-25, 2), (-34, -48), (-2, -3)], closed=True), crest,
               name="left-crest"),
        filled(path([(3, -3), (34, -48), (25, 2)], closed=True), crest,
               name="right-crest"),
        filled(path([(-39, 7), (-60, -28), (-18, 1)], closed=True), "#FDD835",
               name="far-left-crest"),
        filled(path([(18, 1), (60, -28), (39, 7)], closed=True), "#FDD835",
               name="far-right-crest"),
    ], wiggle((0, -91), amp=7, period=24), name="crest")

    upper_beak = group([
        filled(path([(-22, -15), (23, -15), (20, 10), (5, 34),
                     (-11, 17), (-23, 6)], closed=True), "#90A4AE", name="highlight"),
        filled(path([(-28, -20), (28, -20), (24, 13), (4, 39),
                     (-12, 18), (-26, 8)], closed=True), beak, name="upper-beak"),
    ], transform(pos=(0, 16)), name="beak")

    return [
        upper_beak,
        outlined(path([(-18, 49), (0, 57), (18, 49)], closed=False), deep, 4,
                 name="lower-beak-seam"),
        eye((-42, -24), 34, 38, iris="#263238"),
        eye((42, -24), 34, 38, iris="#263238"),
        filled(ellipse(37, 27, (-57, 4)), cheek, name="left-cheek"),
        filled(ellipse(37, 27, (57, 4)), cheek, name="right-cheek"),
        filled(ellipse(170, 158, (0, -15)), feathers, name="head"),
        filled(ellipse(106, 57, (0, 103)), "#FFFFFF", name="chest"),
        filled(ellipse(180, 142, (0, 87)), feathers, name="round-body"),
        filled(ellipse(196, 154, (0, 94)), shade, name="body-shadow"),
        foot(-33, 0.0), foot(33, 0.5),
        wing(-1, 0.0), wing(1, 0.5),
        crest_feathers,
    ]
