from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled


def red_panda():
    fur_c, face_c = "#D84315", "#FFFFFF"
    return [
        filled(ellipse(50, 40, (-60, 20)), face_c, name="patch"),
        filled(ellipse(50, 40, (60, 20)), face_c, name="patch"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(180, 160), fur_c, name="head"),
        filled(triangle(40, 50), fur_c, wiggle((-65, -70), base_rot=-20), name="ear"),
        filled(triangle(40, 50), fur_c, wiggle((65, -70), base_rot=20, phase=0.5), name="ear"),
    ]
