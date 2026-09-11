from critter_parts import dot_eye, smile
from lottie_kit import ellipse, filled, transform


def salamander():
    skin = "#FF9800"
    return [
        filled(ellipse(20, 20), "#F57C00", transform(pos=(-40, 40)), name="spot"),
        filled(ellipse(25, 25), "#F57C00", transform(pos=(50, -30)), name="spot"),
        smile(70, 25, y=30, color="#E65100", w=6),
        dot_eye((-50, -20), 20), dot_eye((50, -20), 20),
        filled(ellipse(200, 130), skin, name="body"),
    ]
