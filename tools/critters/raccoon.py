from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, transform


def raccoon():
    fur_c, mask_c = "#616161", "#212121"
    mask = group([filled(ellipse(76, 58, (x, -10)), mask_c, transform(rotation=x*0.2)) for x in [-45, 45]], name="mask")
    return [
        dot_eye((-45, -10), 12, color="#FFFFFF"), dot_eye((45, -10), 12, color="#FFFFFF"),
        mask,
        filled(ellipse(180, 160), fur_c, name="head"),
        filled(triangle(40, 50), fur_c, wiggle((-60, -70), base_rot=-20), name="ear"),
        filled(triangle(40, 50), fur_c, wiggle((60, -70), base_rot=20, phase=0.5), name="ear"),
    ]
