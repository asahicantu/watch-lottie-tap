from critter_parts import FRAMES, dot_eye, wiggle
from lottie_kit import animated, ellipse, filled, path, transform


def duck():
    return [
        # the lower bill hinges open and shut, so the duck reads as quacking
        filled(ellipse(98, 40, (0, 14)), "#d9741c",
               transform(pos=(0, 30), rotation=animated(
                   [(0, 0), (10, 13), (20, 0), (30, 13), (40, 0), (FRAMES, 0)])),
               name="lower-bill"),
        filled(ellipse(116, 48, (0, -6)), "#f6a02c",
               transform(pos=(0, 30)), name="upper-bill"),
        dot_eye((-44, -22), 20),
        dot_eye((44, -22), 20),
        filled(ellipse(178, 166), "#ffd93b", name="head"),
        filled(path([(0, 0), (-18, -44), (10, -30), (0, -66), (26, -26), (16, -8)]),
               "#ffe882", wiggle((-6, -78), amp=7, period=28), name="tuft"),
    ]
