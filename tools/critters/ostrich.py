from critter_parts import eye, triangle
from lottie_kit import ellipse, filled, outlined, path, transform


def ostrich():
    skin_c, feather_c = "#E0E0E0", "#BDBDBD"
    return [
        filled(triangle(40, 30), "#FFD54F", transform(pos=(0, -50), rotation=180), name="beak"),
        eye((-25, -75), 36, 40), eye((25, -75), 36, 40),
        filled(ellipse(80, 90, (0, -75)), skin_c, name="head"),
        outlined(path([(0, -30), (0, 50)], False), skin_c, 25, name="neck"),
        filled(ellipse(180, 120, (0, 70)), feather_c, name="body"),
    ]
