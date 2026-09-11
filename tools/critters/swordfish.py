from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, outlined, path, transform


def swordfish():
    body = "#546E7A"
    return [
        outlined(path([(0, 0), (0, 120)], closed=False), "#90A4AE", 6, transform(pos=(0, 40)), name="sword"),
        dot_eye((-35, -20), 20), dot_eye((35, -20), 20),
        filled(ellipse(130, 180), body, name="body"),
        filled(triangle(40, 60), "#455A64", transform(pos=(0, -80)), name="fin"),
    ]
