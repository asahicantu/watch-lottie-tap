from critter_parts import dot_eye, smile, teeth, triangle
from lottie_kit import ellipse, filled, group, transform


def shark():
    body_c, belly_c = "#78909C", "#CFD8DC"
    dorsal = filled(triangle(60, 80, tilt=20), body_c, transform(pos=(0, -90)), name="dorsal")
    teeth = group([filled(triangle(15, 20), "#FFFFFF", transform(pos=(i*20 - 40, 40), rotation=180)) for i in range(5)], name="teeth")
    return [
        teeth,
        smile(100, 20, y=30, color="#455A64", w=4),
        dot_eye((-50, -20), 14), dot_eye((50, -20), 14),
        filled(ellipse(160, 50, (0, 50)), belly_c, name="belly"),
        filled(ellipse(210, 140), body_c, name="body"),
        dorsal,
    ]
