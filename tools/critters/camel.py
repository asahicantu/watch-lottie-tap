from critter_parts import eye, smile
from lottie_kit import ellipse, filled, group


def camel():
    fur_c = "#C2B280"
    humps = group([filled(ellipse(70, 60, (x, -70)), fur_c) for x in [-40, 40]], name="humps")
    return [
        humps,
        smile(50, 15, y=40, color="#8D6E63", w=4),
        eye((-45, -10), 34, 38, iris="#5D4037"), eye((45, -10), 34, 38, iris="#5D4037"),
        filled(ellipse(160, 150), fur_c, name="head"),
    ]
