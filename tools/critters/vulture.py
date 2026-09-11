from critter_parts import dot_eye
from lottie_kit import ellipse, filled, path, transform


def vulture():
    body, head = "#4E342E", "#F06292"
    return [
        filled(path([(0, 0), (0, 40), (-30, 20)], closed=True), "#757575",
               transform(pos=(0, 10)), name="beak"),
        dot_eye((-20, -10), 10), dot_eye((20, -10), 10),
        filled(ellipse(100, 100), head, name="head"),
        filled(ellipse(160, 60, (0, 60)), "#BDBDBD", name="ruff"),
    ]
