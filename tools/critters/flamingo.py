from critter_parts import dot_eye
from lottie_kit import ellipse, filled, outlined, path, transform


def flamingo():
    pink_c, beak_c = "#FF80AB", "#212121"
    return [
        filled(path([(0, 0), (20, 0), (10, 50), (-5, 30)], True), beak_c, transform(pos=(0, -60), rotation=10), name="beak"),
        dot_eye((-20, -80), 10), dot_eye((20, -80), 10),
        filled(ellipse(80, 70, (0, -80)), pink_c, name="head"),
        outlined(path([(0, -50), (0, 50)], False), pink_c, 20, name="neck"),
        filled(ellipse(150, 100, (0, 60)), pink_c, name="body"),
    ]
