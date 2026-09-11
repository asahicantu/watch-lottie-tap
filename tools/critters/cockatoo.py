from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, transform


def cockatoo():
    feathers = "#ECEFF1"
    crest = "#FFF176"
    return [
        filled(triangle(40, 60), crest, wiggle((0, -90), base_rot=0, amp=15), name="crest"),
        filled(triangle(30, 40), "#455A64", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(160, 180), feathers, name="head"),
    ]
