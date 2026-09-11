from critter_parts import dot_eye
from lottie_kit import ellipse, filled, transform


def guinea_pig():
    fur = "#A1887F"
    return [
        filled(ellipse(15, 10), "#5D4037", transform(pos=(0, 25)), name="nose"),
        dot_eye((-50, -10), 18), dot_eye((50, -10), 18),
        filled(ellipse(200, 150), fur, name="body"),
        filled(ellipse(50, 35, (0, 0)), "#D7CCC8", transform(pos=(-90, -40), rotation=-30), name="ear"),
        filled(ellipse(50, 35, (0, 0)), "#D7CCC8", transform(pos=(90, -40), rotation=30), name="ear"),
    ]
