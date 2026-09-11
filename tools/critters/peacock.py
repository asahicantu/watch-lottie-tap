import math

from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, group, transform


def peacock():
    body_c, fan_c = "#0288D1", "#4FC3F7"
    feathers = group([filled(ellipse(40, 80, (120 * math.cos(a), 40 + 60 * math.sin(a))), fan_c,
                             transform(rotation=math.degrees(a)+90))
                      for a in [math.pi * i / 6.0 for i in range(1, 6)]], name="fan")
    return [
        feathers,
        dot_eye((-25, -20), 12), dot_eye((25, -20), 12),
        filled(ellipse(100, 140), body_c, name="body"),
        filled(triangle(20, 25), "#FFD54F", transform(pos=(0, 0), rotation=180), name="beak"),
    ]
