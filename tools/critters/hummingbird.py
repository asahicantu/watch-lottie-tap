from critter_parts import FRAMES, dot_eye
from lottie_kit import ellipse, filled, oscillate, outlined, path, transform


def hummingbird():
    body = "#00BCD4"
    def wing(x, phase):
        return filled(ellipse(30, 100), "#4DD0E1",
                      transform(pos=(x, 0), rotation=oscillate(FRAMES, x*0.5, 45, 4, phase)), name="wing")
    return [
        wing(-60, 0), wing(60, 0.5),
        outlined(path([(0, 0), (0, 80)], closed=False), "#263238", 4, transform(pos=(0, 20)), name="beak"),
        dot_eye((-30, -20), 12), dot_eye((30, -20), 12),
        filled(ellipse(120, 140), body, name="body"),
    ]
