from critter_parts import eye, triangle
from lottie_kit import ellipse, filled, path, transform


def puffin():
    feathers = "#263238"
    return [
        filled(triangle(60, 70), "#FFD54F", transform(pos=(0, 30), rotation=180), name="beak"),
        filled(path([(-30, 30), (0, -20), (30, 30)], closed=True), "#F44336", transform(pos=(0, 25)), name="beak-tip"),
        eye((-45, -20), 35, 35, iris="#CFD8DC"),
        eye((45, -20), 35, 35, iris="#CFD8DC"),
        filled(ellipse(180, 180), feathers, name="head"),
        filled(ellipse(120, 120), "#FFFFFF", transform(pos=(0, 10)), name="face"),
    ]
