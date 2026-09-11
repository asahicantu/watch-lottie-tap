from critter_parts import dot_eye, smile, triangle
from lottie_kit import ellipse, filled, group, transform


def walrus():
    body_c, tusk_c = "#5D4037", "#F5F5F5"
    tusks = group([filled(triangle(20, 60), tusk_c, transform(pos=(x, 40), rotation=180)) for x in [-30, 30]], name="tusks")
    return [
        tusks,
        smile(80, 15, y=30, color="#3E2723", w=4),
        dot_eye((-50, -20), 16), dot_eye((50, -20), 16),
        filled(ellipse(210, 170), body_c, name="body"),
    ]
