from critter_parts import dot_eye
from lottie_kit import ellipse, filled, transform


def platypus():
    fur_c, bill_c = "#4E342E", "#212121"
    return [
        filled(ellipse(80, 40, (40, 20)), bill_c, name="bill"),
        dot_eye((-30, -10), 12, color="#FFFFFF"), dot_eye((30, -10), 12, color="#FFFFFF"),
        filled(ellipse(160, 130), fur_c, name="head"),
        filled(ellipse(60, 30, (-80, 40)), bill_c, transform(rotation=20), name="foot"),
        filled(ellipse(60, 30, (80, 40)), bill_c, transform(rotation=-20), name="foot"),
    ]
