from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, rect, transform


def badger():
    fur, stripe = "#455A64", "#ECEFF1"
    return [
        filled(ellipse(22, 16), "#2b2724", transform(pos=(0, 42)), name="nose"),
        dot_eye((-40, 0), 12), dot_eye((40, 0), 12),
        filled(rect(34, 92, (40, 0), radius=16), "#2b2724", name="eye-stripe"),
        filled(rect(34, 92, (-40, 0), radius=16), "#2b2724", name="eye-stripe"),
        filled(rect(40, 140, (0, 0), radius=20), stripe, name="stripe"),
        filled(ellipse(180, 160), fur, name="head"),
        filled(ellipse(50, 50), fur, wiggle((-70, -60), base_rot=-20), name="ear"),
        filled(ellipse(50, 50), fur, wiggle((70, -60), base_rot=20, phase=0.5), name="ear"),
    ]
