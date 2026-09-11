from critter_parts import dot_eye
from lottie_kit import ellipse, filled, outlined, path, transform


def kiwi():
    body = "#795548"
    return [
        outlined(path([(0, 0), (0, 80)], closed=False), "#D7CCC8", 6,
                 transform(pos=(0, 20), rotation=-10), name="beak"),
        dot_eye((-20, -10), 10), dot_eye((20, -10), 10),
        filled(ellipse(140, 160), body, name="body"),
    ]
