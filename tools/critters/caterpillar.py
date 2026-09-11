from critter_parts import FRAMES, dot_eye, smile
from lottie_kit import ellipse, filled, oscillate, transform


def caterpillar():
    skin = "#8BC34A"
    segments = []
    for i in range(5):
        segments.append(filled(ellipse(70, 70), skin,
                              transform(pos=(i * 45 - 90, oscillate(FRAMES, 0, 15, 30, phase=i*0.2)["k"][0]["s"][0])),
                              name=f"segment-{i}"))
    # Simpler segments for now without complex oscillation in pos
    segments = [
        filled(ellipse(70, 70), skin, transform(pos=(90, 0)), name="seg4"),
        filled(ellipse(70, 70), skin, transform(pos=(45, 0)), name="seg3"),
        filled(ellipse(70, 70), skin, transform(pos=(0, 0)), name="seg2"),
        filled(ellipse(70, 70), skin, transform(pos=(-45, 0)), name="seg1"),
        filled(ellipse(80, 80), skin, transform(pos=(-90, 0)), name="head"),
    ]
    return [
        smile(30, 10, y=10, color="#33691E", w=4),
        dot_eye((-105, -10), 8), dot_eye((-75, -10), 8),
        *segments
    ]
