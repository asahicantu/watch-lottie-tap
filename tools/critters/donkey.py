from critter_parts import eye, nostrils, tuft, wiggle
from lottie_kit import ellipse, filled, group, rect


def donkey():
    coat, muzzle, mane = "#9b9086", "#d6cfc6", "#5d554e"
    ear = lambda x, ph: group(
        [filled(rect(24, 100, (0, -58), radius=12), "#b3a89d", name="inner"),
         filled(rect(46, 134, (0, -66), radius=23), coat, name="outer")],
        wiggle((x, -62), base_rot=x * 0.20, amp=8, period=27, phase=ph), name="ear")
    return [
        nostrils(24, 62, 20, 15, "#8a8078"),
        filled(ellipse(110, 88, (0, 56)), muzzle, name="muzzle"),
        eye((-44, -36), 32, 34), eye((44, -36), 32, 34),
        tuft(0, -90, 3, mane, w=22, h=42, spread=18),
        filled(ellipse(150, 186), coat, name="head"),
        ear(-42, 0.0), ear(42, 0.5),
    ]
