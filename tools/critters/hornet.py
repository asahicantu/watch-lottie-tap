from critter_parts import FRAMES, dot_eye, smile
from lottie_kit import ellipse, filled, oscillate, rect, transform


def hornet():
    body = "#FF6F00"
    return [
        smile(40, 15, y=-20, color="#212121", w=5),
        dot_eye((-35, -40), 18), dot_eye((35, -40), 18),
        filled(rect(120, 25, (0, 60), radius=10), "#212121", name="stripe"),
        filled(rect(160, 25, (0, 20), radius=10), "#212121", name="stripe"),
        filled(ellipse(190, 160), body, name="body"),
        filled(ellipse(60, 110), "#B0BEC5",
               transform(pos=(-70, -30), rotation=oscillate(FRAMES, -20, 30, 5), opacity=60), name="wing"),
        filled(ellipse(60, 110), "#B0BEC5",
               transform(pos=(70, -30), rotation=oscillate(FRAMES, 20, 30, 5, phase=0.5), opacity=60), name="wing"),
    ]
