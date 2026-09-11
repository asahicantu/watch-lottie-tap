from critter_parts import dot_eye
from lottie_kit import ellipse, filled, transform


def mole():
    fur_c, nose_c = "#3E2723", "#F8BBD0"
    return [
        filled(ellipse(30, 20, (0, 25)), nose_c, name="nose"),
        dot_eye((-35, -10), 8), dot_eye((35, -10), 8),
        filled(ellipse(170, 150), fur_c, name="head"),
        filled(ellipse(60, 40, (-80, 40)), "#D7CCC8", transform(rotation=20), name="claw"),
        filled(ellipse(60, 40, (80, 40)), "#D7CCC8", transform(rotation=-20), name="claw"),
    ]
