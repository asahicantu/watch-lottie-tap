import math

from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, outlined, path, transform


def jellyfish():
    body_c = "#CE93D8"
    tentacles = [outlined(path([(x, 40), (x, 100 + 20 * math.sin(x))], False), body_c, 5,
                          wiggle((0, 0), amp=10, period=30, phase=x*0.1)) for x in range(-60, 61, 30)]
    return tentacles + [
        filled(ellipse(160, 100), body_c, transform(opacity=70), name="dome"),
        dot_eye((-30, 0), 10, color="#4A148C"), dot_eye((30, 0), 10, color="#4A148C"),
    ]
