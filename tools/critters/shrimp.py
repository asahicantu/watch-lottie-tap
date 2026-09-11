from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, outlined, path, transform


def shrimp():
    body = "#FFAB91"
    return [
        dot_eye((-40, -20), 12), dot_eye((40, -20), 12),
        filled(ellipse(180, 120), body, name="body"),
        outlined(path([(0, 0), (-60, -40)], closed=False), body, 4, wiggle((-20, -40), amp=20, period=15), name="antenna"),
        outlined(path([(0, 0), (60, -40)], closed=False), body, 4, wiggle((20, -40), amp=20, period=15, phase=0.5), name="antenna"),
        filled(triangle(40, 60), body, transform(pos=(90, 0), rotation=90), name="tail"),
    ]
