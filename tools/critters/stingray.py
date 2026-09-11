from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, outlined, path


def stingray():
    body = "#B0BEC5"
    return [
        dot_eye((-60, -20), 15), dot_eye((60, -20), 15),
        filled(ellipse(260, 180), body, name="body"),
        outlined(path([(0, 0), (0, 120)], closed=False), body, 8, wiggle((0, 80), amp=15, period=25), name="tail"),
    ]
