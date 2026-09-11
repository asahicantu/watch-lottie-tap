from critter_parts import eye, triangle
from lottie_kit import ellipse, filled, transform


def dragon():
    body, belly = "#4CAF50", "#C8E6C9"
    return [
        filled(triangle(40, 50), "#FFD54F", transform(pos=(0, 40), rotation=180), name="snout"),
        eye((-45, -20), 40, 45, iris="#E65100"),
        eye((45, -20), 40, 45, iris="#E65100"),
        filled(ellipse(200, 180), body, name="head"),
        filled(triangle(30, 40), "#388E3C", transform(pos=(-60, -80), rotation=-20), name="spike"),
        filled(triangle(30, 40), "#388E3C", transform(pos=(0, -95)), name="spike"),
        filled(triangle(30, 40), "#388E3C", transform(pos=(60, -80), rotation=20), name="spike"),
    ]
