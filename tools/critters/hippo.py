from critter_parts import eye, nostrils, smile, wiggle
from lottie_kit import ellipse, filled


def hippo():
    hide, muzzle = "#a98bb5", "#c9aed2"
    return [
        smile(84, 18, y=64, color="#8a6d96", w=6),
        nostrils(40, 20, 26, 18, "#7d6289"),
        filled(ellipse(172, 116, (0, 44)), muzzle, name="muzzle"),
        eye((-58, -50), 34, 36), eye((58, -50), 34, 36),
        filled(ellipse(216, 162), hide, name="head"),
        filled(ellipse(40, 30), hide,
               wiggle((-74, -70), amp=6, period=30), name="ear"),
        filled(ellipse(40, 30), hide,
               wiggle((74, -70), amp=6, period=30, phase=0.5), name="ear"),
    ]
