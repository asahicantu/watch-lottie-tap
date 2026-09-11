from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, transform


def hen():
    body, comb = "#FFB74D", "#E53935"
    return [
        filled(triangle(30, 40), "#FDD835", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-35, -20), 12), dot_eye((35, -20), 12),
        filled(ellipse(160, 160), body, name="head"),
        filled(ellipse(40, 60, (0, -80)), comb, wiggle((0, 0), amp=5, period=30), name="comb"),
        filled(ellipse(30, 50, (-30, -70)), comb, wiggle((0, 0), amp=5, period=30, phase=0.3), name="comb"),
        filled(ellipse(30, 50, (30, -70)), comb, wiggle((0, 0), amp=5, period=30, phase=0.6), name="comb"),
    ]
