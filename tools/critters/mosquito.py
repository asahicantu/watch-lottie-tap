from critter_parts import FRAMES, dot_eye
from lottie_kit import ellipse, filled, oscillate, outlined, path, transform


def mosquito():
    body = "#607D8B"
    return [
        outlined(path([(0, 0), (0, 70)], closed=False), "#263238", 3, transform(pos=(0, 30)), name="proboscis"),
        dot_eye((-25, -20), 15), dot_eye((25, -20), 15),
        filled(ellipse(100, 120), body, name="body"),
        filled(ellipse(30, 120), "#B0BEC5",
               transform(pos=(-50, -20), rotation=oscillate(FRAMES, -30, 20, 5), opacity=50), name="wing"),
        filled(ellipse(30, 120), "#B0BEC5",
               transform(pos=(50, -20), rotation=oscillate(FRAMES, 30, 20, 5, phase=0.5), opacity=50), name="wing"),
    ]
