from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, path, transform


def seagull():
    body, beak = "#ECEFF1", "#FBC02D"
    return [
        filled(path([(0, 0), (40, 10), (0, 20)], closed=True), beak,
               transform(pos=(0, 10)), name="beak"),
        dot_eye((-30, -20), 10), dot_eye((30, -20), 10),
        filled(ellipse(160, 160), body, name="head"),
        filled(ellipse(60, 30, (-70, 40)), "#9E9E9E", wiggle((0, 0), amp=10, period=30), name="wing"),
        filled(ellipse(60, 30, (70, 40)), "#9E9E9E", wiggle((0, 0), amp=10, period=30, phase=0.5), name="wing"),
    ]
