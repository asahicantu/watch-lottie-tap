from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, rect, transform


def kookaburra():
    feathers = "#795548"
    return [
        filled(triangle(40, 80), "#D7CCC8", transform(pos=(0, 30), rotation=180), name="beak"),
        dot_eye((-40, -20), 18), dot_eye((40, -20), 18),
        filled(ellipse(170, 160), feathers, name="head"),
        filled(rect(60, 20, (0, -90), radius=5), "#5D4037", name="tuft"),
    ]
