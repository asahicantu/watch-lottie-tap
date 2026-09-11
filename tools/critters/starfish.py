import math

from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, transform


def starfish():
    body_c = "#FF7043"
    points = [filled(triangle(40, 100), body_c, transform(rotation=72*i, pos=(80*math.sin(math.radians(72*i)), -80*math.cos(math.radians(72*i))))) for i in range(5)]
    return points + [
        dot_eye((-20, -10), 10, color="#FFFFFF"), dot_eye((20, -10), 10, color="#FFFFFF"),
        filled(ellipse(80, 80), body_c, name="body"),
    ]
