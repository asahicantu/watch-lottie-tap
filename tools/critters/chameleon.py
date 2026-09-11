from critter_parts import FRAMES, eye, smile
from lottie_kit import ellipse, filled, oscillate, outlined, path, transform


def chameleon():
    skin = "#4CAF50"
    return [
        outlined(path([(0, 0), (40, 20), (20, 60)], closed=False), skin, 8,
                 transform(pos=(70, 30), rotation=oscillate(FRAMES, 0, 30, 40)), name="tail"),
        smile(60, 20, y=20, color="#1B5E20", w=5),
        eye((-50, -20), 45, 45, iris="#8BC34A"),
        eye((40, -20), 45, 45, iris="#8BC34A"),
        filled(ellipse(190, 140), skin, name="body"),
    ]
