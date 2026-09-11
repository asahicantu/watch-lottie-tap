from critter_parts import eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, rect, transform


def tiger():
    coat, cream, stripe = "#f0913c", "#fdf3e6", "#3a2a1e"
    bars = [
        filled(rect(14, 46, radius=7), stripe, transform(pos=(-54, -62), rotation=24),
               name="stripe"),
        filled(rect(14, 52, radius=7), stripe, transform(pos=(-20, -74)), name="stripe"),
        filled(rect(14, 52, radius=7), stripe, transform(pos=(20, -74)), name="stripe"),
        filled(rect(14, 46, radius=7), stripe, transform(pos=(54, -62), rotation=-24),
               name="stripe"),
        filled(rect(12, 38, radius=6), stripe, transform(pos=(-84, 6), rotation=76),
               name="stripe"),
        filled(rect(12, 38, radius=6), stripe, transform(pos=(84, 6), rotation=-76),
               name="stripe"),
    ]
    return [
        smile(54, 20, y=40, color="#6b4423", w=6),
        filled(triangle(30, 22, pos=(0, 16)), "#d9707f",
               transform(rotation=180), name="nose"),
        filled(ellipse(62, 48, (-28, 40)), cream, name="muzzle"),
        filled(ellipse(62, 48, (28, 40)), cream, name="muzzle"),
        eye((-44, -16), 34, 38, iris="#4a8c3f"), eye((44, -16), 34, 38, iris="#4a8c3f"),
    ] + bars + [
        filled(ellipse(198, 178), coat, name="head"),
        group([filled(ellipse(32, 32), "#f6c7a8", name="inner"),
               filled(ellipse(56, 56), coat, name="outer")],
              wiggle((-70, -72), amp=6, period=26), name="ear"),
        group([filled(ellipse(32, 32), "#f6c7a8", name="inner"),
               filled(ellipse(56, 56), coat, name="outer")],
              wiggle((70, -72), amp=6, period=26, phase=0.5), name="ear"),
    ]
