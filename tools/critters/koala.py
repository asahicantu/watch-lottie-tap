from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group


def koala():
    fur, fluff = "#9aa0a6", "#d3d8dc"
    ear = lambda x, ph: group(
        [filled(ellipse(70, 70), fluff, name="inner"),
         filled(ellipse(108, 108), fur, name="outer")],
        wiggle((x, -28), amp=5, period=30, phase=ph), name="ear")
    return [
        filled(ellipse(54, 68, (0, 30)), "#3c3f43", name="nose"),
        dot_eye((-42, -18), 17), dot_eye((42, -18), 17),
        filled(ellipse(178, 166), fur, name="head"),
        ear(-86, 0.0), ear(86, 0.5),
    ]
