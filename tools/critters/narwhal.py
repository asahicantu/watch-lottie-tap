from critter_parts import dot_eye, triangle
from lottie_kit import ellipse, filled, transform


def narwhal():
    body = "#90A4AE"
    return [
        filled(triangle(20, 100), "#ECEFF1", transform(pos=(0, -70)), name="tusk"),
        dot_eye((-50, 10), 12), dot_eye((50, 10), 12),
        filled(ellipse(200, 150), body, name="body"),
    ]
