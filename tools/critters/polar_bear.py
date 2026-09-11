from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled


def polar_bear():
    fur_c = "#FFFFFF"
    return [
        smile(46, 18, y=48, color="#B0BEC5", w=5),
        filled(ellipse(42, 32, (0, 26)), "#263238", name="nose"),
        dot_eye((-45, -20), 18), dot_eye((45, -20), 18),
        filled(ellipse(190, 180), fur_c, name="head"),
        filled(ellipse(50, 50), fur_c, wiggle((-70, -75)), name="ear"),
        filled(ellipse(50, 50), fur_c, wiggle((70, -75), phase=0.5), name="ear"),
    ]
