from critter_parts import eye, nostrils, triangle, wiggle
from lottie_kit import ellipse, filled, transform


def goat():
    coat, horn, muzzle = "#f2ece1", "#cbbba4", "#e2d7c6"
    return [
        filled(triangle(50, 62), "#ded2c0",
               wiggle((0, 96), base_rot=180, amp=5, period=32), name="beard"),
        nostrils(20, 62, 16, 12, "#a08d76"),
        filled(ellipse(96, 78, (0, 56)), muzzle, name="muzzle"),
        eye((-44, -34), 40, 36, white="#fbf3dd"),
        eye((44, -34), 40, 36, white="#fbf3dd"),
        filled(ellipse(152, 184), coat, name="head"),
        filled(ellipse(78, 34), coat,
               wiggle((-84, -26), base_rot=-24, amp=7, period=28), name="ear"),
        filled(ellipse(78, 34), coat,
               wiggle((84, -26), base_rot=24, amp=7, period=28, phase=0.5), name="ear"),
        filled(triangle(26, 76, tilt=-22), horn,
               transform(pos=(-38, -80), rotation=-18), name="horn"),
        filled(triangle(26, 76, tilt=22), horn,
               transform(pos=(38, -80), rotation=18), name="horn"),
    ]
