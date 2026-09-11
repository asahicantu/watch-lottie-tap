from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled


def hamster():
    fur_c, cheek_c = "#FFD180", "#FFAB91"
    return [
        filled(ellipse(50, 40, (-60, 30)), cheek_c, name="cheek"),
        filled(ellipse(50, 40, (60, 30)), cheek_c, name="cheek"),
        smile(30, 10, y=30, color="#5D4037", w=3),
        dot_eye((-40, -10), 16), dot_eye((40, -10), 16),
        filled(ellipse(180, 160), fur_c, name="head"),
        filled(ellipse(40, 40), fur_c, wiggle((-70, -70)), name="ear"),
        filled(ellipse(40, 40), fur_c, wiggle((70, -70), phase=0.5), name="ear"),
    ]
