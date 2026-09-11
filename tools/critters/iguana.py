from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, group, transform


def iguana():
    body = "#8BC34A"
    return [
        dot_eye((-50, -10), 15), dot_eye((50, -10), 15),
        filled(ellipse(220, 140), body, name="head"),
        filled(ellipse(30, 30, (0, 60)), "#689F38", name="dewlap"),
        group([filled(triangle(15, 20), "#689F38") for i in range(5)],
              transform(pos=(0, -70)), name="spikes"),
    ]
