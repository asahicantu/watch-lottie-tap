import math

from critter_parts import FRAMES, eye, smile, triangle
from lottie_kit import ellipse, filled, group, oscillate, transform


def lion():
    mane, fur = "#c9741f", "#f4c07a"
    tufts = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        tufts.append(filled(ellipse(76, 76, (110 * math.cos(a), 110 * math.sin(a))),
                            "#a75a13", name="tuft"))
    mane_group = group(tufts + [filled(ellipse(238, 232), mane, name="mane-core")],
                       transform(rotation=oscillate(FRAMES, 0, 6, 60)), name="mane")
    return [
        smile(52, 20, y=34, color="#7a4a20", w=6),
        filled(triangle(30, 22, pos=(0, 11)), "#7a4a20",
               transform(rotation=180), name="nose"),
        filled(ellipse(58, 46, (-26, 34)), "#fce4c0", name="muzzle"),
        filled(ellipse(58, 46, (26, 34)), "#fce4c0", name="muzzle"),
        eye((-40, -20), 32, 36, iris="#5a3a15"),
        eye((40, -20), 32, 36, iris="#5a3a15"),
        filled(ellipse(172, 158), fur, name="face"),
        mane_group,
    ]
