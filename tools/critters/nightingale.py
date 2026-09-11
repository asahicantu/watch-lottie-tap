from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, transform


def nightingale():
    feathers = "#8D6E63"
    return [
        filled(triangle(30, 40), "#FDD835", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(160, 160), feathers, name="head"),
        filled(ellipse(100, 60), "#A1887F", transform(pos=(0, 60)), name="chest"),
    ]
