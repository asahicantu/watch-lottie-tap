from critter_parts import eye, nostrils, triangle, tuft, wiggle
from lottie_kit import ellipse, filled, transform


def horse():
    coat, muzzle, mane = "#c17a3f", "#e6c199", "#5f3b1f"
    return [
        nostrils(24, 66, 22, 16, "#6b4423"),
        filled(ellipse(110, 90, (0, 56)), muzzle, name="muzzle"),
        eye((-46, -42), 32, 36), eye((46, -42), 32, 36),
        tuft(0, -96, 3, mane, w=26, h=52, spread=20),
        filled(ellipse(152, 200), coat, name="head"),
        filled(triangle(32, 56, tilt=-6), coat,
               wiggle((-46, -84), base_rot=-10, amp=7, period=28), name="ear"),
        filled(triangle(32, 56, tilt=6), coat,
               wiggle((46, -84), base_rot=10, amp=7, period=28, phase=0.5), name="ear"),
        filled(ellipse(44, 150, (0, 0)), mane,
               transform(pos=(-66, -18), rotation=-12), name="mane"),
        filled(ellipse(44, 150, (0, 0)), mane,
               transform(pos=(66, -18), rotation=12), name="mane"),
    ]
