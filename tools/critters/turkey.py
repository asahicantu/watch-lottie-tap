import math

from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, group, transform


def turkey():
    body_c, red_c = "#BF360C", "#D32F2F"
    fan = group([filled(ellipse(50, 120, (120*math.cos(math.radians(a)), 120*math.sin(math.radians(a)))), "#795548", transform(rotation=a+90))
                 for a in range(-120, 121, 30)], name="fan")
    return [
        fan,
        filled(ellipse(20, 40, (15, 20)), red_c, name="wattle"),
        filled(triangle(30, 25), "#FFD54F", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-35, -15), 15), dot_eye((35, -15), 15),
        filled(ellipse(160, 150), body_c, name="head"),
    ]
