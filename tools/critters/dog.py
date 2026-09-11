from critter_parts import FRAMES, eye, wiggle
from lottie_kit import animated, ellipse, filled, rect, transform


def dog():
    fur, ear_c = "#c98a4b", "#8e5a2b"

    def flap(x, phase):
        return filled(rect(58, 128, (0, 62), radius=28), ear_c,
                      wiggle((x, -34), base_rot=x * 0.12, amp=11, period=24,
                             phase=phase),
                      name="ear")

    return [
        filled(rect(44, 34, (0, 16), radius=16), "#e5717f",
               transform(pos=(0, 60),
                         scale=animated([(0, [100, 100]), (20, [100, 128]),
                                         (36, [100, 100]), (52, [100, 122]),
                                         (66, [100, 100]), (FRAMES, [100, 100])])),
               name="tongue"),
        filled(ellipse(46, 34, (0, 14)), "#2b2320", name="nose"),
        filled(ellipse(120, 86, (0, 34)), "#f3e2c8", name="snout"),
        eye((-44, -30), 34, 38, iris="#3a2a20"),
        eye((44, -30), 34, 38, iris="#3a2a20"),
        filled(ellipse(190, 174), fur, name="head"),
        flap(-84, 0.0), flap(84, 0.5),
    ]
