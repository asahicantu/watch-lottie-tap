import math

from critter_parts import dot_eye, smile, triangle
from lottie_kit import ellipse, filled, group, transform


def hedgehog():
    skin_c, spike_c = "#D7CCC8", "#6D4C41"
    spikes = group([filled(triangle(30, 40), spike_c, transform(pos=(100 * math.cos(a), 100 * math.sin(a)), rotation=math.degrees(a)+90))
                    for a in [math.pi * i / 6.0 for i in range(13)]], name="spikes")
    return [
        spikes,
        smile(40, 10, y=30, color="#3E2723", w=3),
        dot_eye((-30, -10), 12), dot_eye((30, -10), 12),
        filled(ellipse(160, 140), skin_c, name="body"),
        filled(ellipse(20, 20, (0, 10)), "#3E2723", name="nose"),
    ]
