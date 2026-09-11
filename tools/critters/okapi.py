from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, rect


def okapi():
    fur = "#3E2723"
    return [
        filled(rect(100, 15, (0, 70), radius=5), "#FFFFFF", name="leg-stripe"),
        filled(rect(120, 15, (0, 90), radius=5), "#FFFFFF", name="leg-stripe"),
        dot_eye((-40, -20), 18), dot_eye((40, -20), 18),
        filled(ellipse(160, 190), fur, name="head"),
        filled(ellipse(60, 90), "#5D4037", wiggle((-80, -70), base_rot=-20), name="ear"),
        filled(ellipse(60, 90), "#5D4037", wiggle((80, -70), base_rot=20, phase=0.5), name="ear"),
    ]
