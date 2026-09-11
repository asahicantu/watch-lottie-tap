from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, outlined, path, transform


def swan():
    body_c, beak_c = "#FAFAFA", "#FF9800"
    return [
        filled(triangle(30, 40), beak_c, transform(pos=(0, -50), rotation=180), name="beak"),
        dot_eye((-20, -75), 10), dot_eye((20, -75), 10),
        filled(ellipse(90, 80, (0, -75)), body_c, name="head"),
        outlined(path([(0, -40), (0, 60)], False), body_c, 30, name="neck"),
        filled(ellipse(180, 120, (0, 80)), body_c, name="body"),
    ]
