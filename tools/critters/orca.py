from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled


def orca():
    body, white = "#212121", "#FFFFFF"
    return [
        filled(ellipse(60, 30, (-60, -20)), white, name="patch"),
        filled(ellipse(60, 30, (60, -20)), white, name="patch"),
        dot_eye((-50, 10), 15), dot_eye((50, 10), 15),
        filled(ellipse(220, 160), body, name="body"),
        filled(triangle(40, 80), body, wiggle((0, -80), amp=5, period=40), name="fin"),
    ]
