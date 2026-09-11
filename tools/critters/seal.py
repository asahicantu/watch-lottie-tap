from critter_parts import dot_eye
from lottie_kit import ellipse, filled, outlined, path, transform


def seal():
    body_c, belly_c = "#78909C", "#CFD8DC"
    whisker = lambda x, y, rot: outlined(path([(0, 0), (x, 0)], False), "#B0BEC5", 2, transform(pos=(30, y), rotation=rot))
    return [
        whisker(30, 30, 10), whisker(30, 40, 0), whisker(-30, 30, -10), whisker(-30, 40, 0),
        filled(ellipse(20, 15, (0, 20)), "#263238", name="nose"),
        dot_eye((-40, -10), 14), dot_eye((40, -10), 14),
        filled(ellipse(190, 150), body_c, name="body"),
        filled(ellipse(60, 30, (-90, 50)), body_c, transform(rotation=20), name="flipper"),
        filled(ellipse(60, 30, (90, 50)), body_c, transform(rotation=-20), name="flipper"),
    ]
