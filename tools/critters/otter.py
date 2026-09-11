from critter_parts import dot_eye, smile
from lottie_kit import ellipse, filled, transform


def otter():
    fur_c = "#795548"
    return [
        smile(40, 10, y=30, color="#3E2723", w=3),
        filled(ellipse(20, 15, (0, 20)), "#212121", name="nose"),
        dot_eye((-40, -10), 14), dot_eye((40, -10), 14),
        filled(ellipse(170, 150), fur_c, name="head"),
        filled(ellipse(50, 30, (-80, 50)), fur_c, transform(rotation=30), name="flipper"),
        filled(ellipse(50, 30, (80, 50)), fur_c, transform(rotation=-30), name="flipper"),
    ]
