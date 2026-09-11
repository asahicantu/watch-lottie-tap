from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, rect


def kangaroo():
    fur_c = "#FB8C00"
    return [
        smile(40, 15, y=35, color="#BF360C", w=4),
        dot_eye((-40, -15), 15), dot_eye((40, -15), 15),
        filled(ellipse(120, 50, (0, 60)), "#FFCC80", name="pouch"),
        filled(ellipse(170, 180), fur_c, name="head"),
        filled(rect(30, 90, (0, -45), radius=15), fur_c, wiggle((-50, -80), base_rot=-20), name="ear"),
        filled(rect(30, 90, (0, -45), radius=15), fur_c, wiggle((50, -80), base_rot=20, phase=0.5), name="ear"),
    ]
