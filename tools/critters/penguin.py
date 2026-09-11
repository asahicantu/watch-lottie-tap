from critter_parts import FRAMES, dot_eye, triangle
from lottie_kit import animated, ellipse, filled, transform


def penguin():
    coat, belly, beak = "#2c333b", "#f8f5ef", "#f0912a"
    return [
        filled(triangle(46, 50), beak,
               transform(pos=(0, 42), rotation=180,
                         scale=animated([(0, [100, 100]), (14, [104, 122]),
                                         (28, [100, 100]), (FRAMES, [100, 100])])),
               name="beak"),
        dot_eye((-36, -10), 17), dot_eye((36, -10), 17),
        filled(ellipse(136, 148, (0, 14)), belly, name="face"),
        filled(ellipse(190, 180), coat, name="head"),
    ]
