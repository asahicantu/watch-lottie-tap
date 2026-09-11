from critter_parts import dot_eye
from lottie_kit import ellipse, filled, transform


def meerkat():
    fur = "#D7CCC8"
    return [
        filled(ellipse(20, 15), "#3E2723", transform(pos=(0, 20)), name="nose"),
        filled(ellipse(40, 40), "#A1887F", transform(pos=(-45, -15)), name="eye-patch"),
        filled(ellipse(40, 40), "#A1887F", transform(pos=(45, -15)), name="eye-patch"),
        dot_eye((-45, -15), 12), dot_eye((45, -15), 12),
        filled(ellipse(140, 180), fur, name="head"),
        filled(ellipse(30, 30), "#3E2723", transform(pos=(-75, -60)), name="ear"),
        filled(ellipse(30, 30), "#3E2723", transform(pos=(75, -60)), name="ear"),
    ]
