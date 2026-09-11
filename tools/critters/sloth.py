from critter_parts import dot_eye
from lottie_kit import ellipse, filled, transform


def sloth():
    fur_c, face_c = "#795548", "#D7CCC8"
    patch = lambda x: filled(ellipse(64, 82, (x, 0)), "#5D4037", transform(rotation=x*0.2), name="patch")
    return [
        dot_eye((-45, 0), 12), dot_eye((45, 0), 12),
        patch(-45), patch(45),
        filled(ellipse(140, 120), face_c, name="face"),
        filled(ellipse(180, 160), fur_c, name="head"),
    ]
