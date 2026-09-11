from critter_parts import eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, transform


def fox():
    coat, cream, dark = "#e8792b", "#fdf6ec", "#3a2a24"
    ear = lambda x, ph: group(
        [filled(triangle(34, 40, tilt=x * 0.10), dark,
                transform(pos=(0, -40)), name="tip"),
         filled(triangle(72, 84, tilt=x * 0.12), coat, name="outer")],
        wiggle((x, -58), base_rot=x * 0.10, amp=6, period=26, phase=ph), name="ear")
    return [
        filled(triangle(28, 22, pos=(0, 12)), dark,
               transform(rotation=180), name="nose"),
        filled(ellipse(92, 74, (0, 40)), cream, name="muzzle"),
        eye((-42, -16), 32, 36, iris="#5a3a15"), eye((42, -16), 32, 36, iris="#5a3a15"),
        filled(ellipse(72, 52), cream, transform(pos=(-78, 28), rotation=-24),
               name="ruff"),
        filled(ellipse(72, 52), cream, transform(pos=(78, 28), rotation=24),
               name="ruff"),
        filled(ellipse(188, 168), coat, name="head"),
        ear(-58, 0.0), ear(58, 0.5),
    ]
