from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, group, transform


def panda():
    white, black = "#f7f4ee", "#2b2b2b"
    patch = lambda x: group(
        [dot_eye((0, 0), 15),
         filled(ellipse(66, 78), black, transform(rotation=x * 0.16), name="patch")],
        transform(pos=(x, -10)), name="eye-patch")
    return [
        smile(48, 18, y=52, color="#4a4a4a", w=6),
        filled(ellipse(40, 32, (0, 30)), black, name="nose"),
        patch(-46), patch(46),
        filled(ellipse(196, 178), white, name="head"),
        filled(ellipse(58, 58), black,
               wiggle((-74, -74), amp=5, period=30), name="ear"),
        filled(ellipse(58, 58), black,
               wiggle((74, -74), amp=5, period=30, phase=0.5), name="ear"),
    ]
