from critter_parts import dot_eye
from lottie_kit import ellipse, filled, path, transform


def pelican():
    body_c, pouch_c = "#CFD8DC", "#FFD54F"
    return [
        filled(ellipse(100, 60, (40, 30)), pouch_c, name="pouch"),
        filled(path([(0, 0), (100, 0), (80, 20), (0, 20)], True), "#FFB300", transform(pos=(0, 10)), name="beak"),
        dot_eye((-30, -20), 12), dot_eye((30, -20), 12),
        filled(ellipse(150, 140), body_c, name="head"),
    ]
