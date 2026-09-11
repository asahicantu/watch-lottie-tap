from critter_parts import eye, nostrils, wiggle
from lottie_kit import ellipse, filled, group, rect


def giraffe():
    coat, spot, muzzle = "#f0c169", "#b57a2e", "#f7dcae"
    ossicone = lambda x: group(
        [filled(ellipse(26, 26, (0, -44)), "#8a5f22", name="knob"),
         filled(rect(14, 46, (0, -22), radius=7), coat, name="stalk")],
        wiggle((x, -84), base_rot=x * 0.12, amp=5, period=30,
               phase=0.0 if x < 0 else 0.5), name="ossicone")
    return [
        nostrils(22, 66, 18, 13, "#c69a5a"),
        filled(ellipse(100, 80, (0, 60)), muzzle, name="muzzle"),
        eye((-42, -44), 32, 36, iris="#4a3116"), eye((42, -44), 32, 36, iris="#4a3116"),
        filled(ellipse(34, 30, (-42, 8)), spot, name="spot"),
        filled(ellipse(30, 28, (40, -8)), spot, name="spot"),
        filled(ellipse(26, 24, (6, 24)), spot, name="spot"),
        filled(ellipse(132, 194), coat, name="head"),
        filled(ellipse(56, 30), coat,
               wiggle((-76, -66), base_rot=-28, amp=6, period=28), name="ear"),
        filled(ellipse(56, 30), coat,
               wiggle((76, -66), base_rot=28, amp=6, period=28, phase=0.5), name="ear"),
        ossicone(-30), ossicone(30),
    ]
