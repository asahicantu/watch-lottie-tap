from critter_parts import FRAMES, dot_eye
from lottie_kit import (
    ellipse, filled, oscillate, outlined, path, rect, transform,
)


def woodpecker():
    feathers = "#D32F2F"
    return [
        outlined(path([(0, 0), (0, 90)], closed=False), "#455A64", 8,
                 transform(pos=(0, 20), rotation=oscillate(FRAMES, 0, 10, 10)), name="beak"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(160, 170), "#263238", name="head"),
        filled(rect(40, 80, (0, -70), radius=10), feathers, name="crest"),
    ]
