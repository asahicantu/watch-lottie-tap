from critter_parts import FRAMES, dot_eye, triangle, wiggle
from lottie_kit import animated, ellipse, filled, group, transform


def rooster():
    body, red, beak = "#efe8dc", "#d94f3d", "#f5b02a"
    comb = group([filled(ellipse(40, 40, (-32, 6)), red, name="bump"),
                  filled(ellipse(46, 46, (0, -6)), red, name="bump"),
                  filled(ellipse(40, 40, (32, 6)), red, name="bump")],
                 wiggle((0, -92), amp=5, period=26), name="comb")
    return [
        filled(ellipse(24, 40, (-14, 20)), red, name="wattle"),
        filled(ellipse(24, 40, (14, 20)), red, name="wattle"),
        filled(triangle(52, 36), beak,
               transform(pos=(0, 30), rotation=180,
                         scale=animated([(0, [100, 100]), (12, [104, 126]),
                                         (26, [100, 100]), (FRAMES, [100, 100])])),
               name="beak"),
        dot_eye((-36, -18), 17), dot_eye((36, -18), 17),
        filled(ellipse(172, 166), body, name="head"),
        comb,
    ]
