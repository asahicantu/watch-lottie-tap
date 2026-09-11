from critter_parts import dot_eye
from lottie_kit import ellipse, filled, path


def seahorse():
    body_c = "#FFD54F"
    return [
        filled(ellipse(40, 20, (30, -20)), body_c, name="snout"),
        dot_eye((-10, -40), 12), dot_eye((40, -40), 12),
        filled(ellipse(100, 160), body_c, name="body"),
        filled(path([(0, 80), (20, 120), (-20, 120)], True), body_c, name="tail"),
        filled(ellipse(40, 60, (-50, 20)), "#FFF176", name="fin"),
    ]
