from critter_parts import FRAMES, dot_eye
from lottie_kit import ellipse, filled, oscillate, transform


def firefly():
    body, glow = "#37474F", "#FBC02D"
    return [
        filled(ellipse(100, 80), glow, transform(pos=(0, 70), opacity=oscillate(FRAMES, 70, 30, 20)), name="glow"),
        dot_eye((-30, -30), 15), dot_eye((30, -30), 15),
        filled(ellipse(140, 160), body, name="body"),
        filled(ellipse(50, 100), "#90A4AE", transform(pos=(-60, 0), rotation=-20), name="wing-l"),
        filled(ellipse(50, 100), "#90A4AE", transform(pos=(60, 0), rotation=20), name="wing-r"),
    ]
