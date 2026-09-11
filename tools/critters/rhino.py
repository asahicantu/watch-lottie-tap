from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, transform


def rhino():
    hide_c = "#9E9E9E"
    return [
        filled(triangle(30, 50), "#CFD8DC", transform(pos=(0, 20), rotation=0), name="horn"),
        dot_eye((-50, -20), 15), dot_eye((50, -20), 15),
        filled(ellipse(200, 160), hide_c, name="head"),
        filled(triangle(30, 40), hide_c, wiggle((-70, -70), base_rot=-20), name="ear"),
        filled(triangle(30, 40), hide_c, wiggle((70, -70), base_rot=20, phase=0.5), name="ear"),
    ]
