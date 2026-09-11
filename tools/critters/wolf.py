from critter_parts import FRAMES, eye, triangle, wiggle
from lottie_kit import animated, ellipse, filled, group, transform


def wolf():
    coat, light = "#7d858d", "#d8dde2"
    ear = lambda x, ph: group(
        [filled(triangle(30, 34, tilt=x * 0.10), "#5c646c",
                transform(pos=(0, -34)), name="tip"),
         filled(triangle(62, 76, tilt=x * 0.12), coat, name="outer")],
        wiggle((x, -62), base_rot=x * 0.12, amp=6, period=28, phase=ph), name="ear")
    return [
        # muzzle lifted and mouth open: mid-howl
        filled(ellipse(38, 30, (0, 22)), "#2b3138", name="nose"),
        filled(ellipse(44, 34, (0, 62)), "#3a2f33",
               transform(scale=animated([(0, [100, 60]), (18, [100, 120]),
                                         (40, [100, 96]), (FRAMES, [100, 60])])),
               name="mouth"),
        filled(ellipse(96, 92, (0, 44)), light, name="snout"),
        eye((-44, -20), 32, 34, iris="#e0a92e"), eye((44, -20), 32, 34, iris="#e0a92e"),
        filled(ellipse(184, 174), coat, name="head"),
        ear(-58, 0.0), ear(58, 0.5),
    ]
