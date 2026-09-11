from critter_parts import dot_eye
from lottie_kit import ellipse, filled, rect


def skunk():
    body, stripe = "#000000", "#FFFFFF"
    return [
        filled(ellipse(20, 15, (0, 30)), "#424242", name="nose"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(180, 160), body, name="head"),
        filled(rect(40, 160, (0, -40), radius=20), stripe, name="stripe"),
    ]
