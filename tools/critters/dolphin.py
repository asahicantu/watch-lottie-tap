from critter_parts import dot_eye, smile
from lottie_kit import ellipse, filled, transform


def dolphin():
    body_c, belly_c = "#4FC3F7", "#E1F5FE"
    return [
        smile(60, 15, y=30, color="#0288D1", w=4),
        dot_eye((-40, -20), 12), dot_eye((40, -20), 12),
        filled(ellipse(140, 40, (0, 45)), belly_c, name="belly"),
        filled(ellipse(190, 120), body_c, name="body"),
        filled(ellipse(60, 30, (0, 0)), body_c, transform(pos=(0, 60), rotation=10), name="tail"),
    ]
