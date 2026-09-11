from critter_parts import FRAMES, eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, oscillate, rect, transform


def elephant():
    hide, inner = "#98a2ad", "#b6bfc8"
    trunk = group(
        [filled(rect(42, 58, (10, 40), radius=20), hide,
                transform(rotation=22), name="trunk-tip"),
         filled(rect(54, 96, (0, 0), radius=24), hide, name="trunk-top")],
        transform(pos=(0, 62),
                  rotation=oscillate(FRAMES, 0, 7, 34)), name="trunk")
    ear = lambda x, ph: group(
        [filled(ellipse(96, 122, (x * 0.18, 6)), inner, name="inner"),
         filled(ellipse(126, 156), hide, name="outer")],
        wiggle((x, -8), base_rot=x * 0.09, amp=7, period=30, phase=ph), name="ear")
    return [
        trunk,
        filled(triangle(20, 40, tilt=-6), "#f4efe4",
               transform(pos=(-40, 92), rotation=8), name="tusk"),
        filled(triangle(20, 40, tilt=6), "#f4efe4",
               transform(pos=(40, 92), rotation=-8), name="tusk"),
        eye((-44, -24), 30, 32), eye((44, -24), 30, 32),
        filled(ellipse(180, 164), hide, name="head"),
        ear(-96, 0.0), ear(96, 0.5),
    ]
