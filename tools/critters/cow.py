from critter_parts import eye, triangle, wiggle
from lottie_kit import ellipse, filled, transform


def cow():
    return [
        filled(ellipse(20, 14, (26, 46)), "#c4707c", name="nostril"),
        filled(ellipse(20, 14, (-26, 46)), "#c4707c", name="nostril"),
        filled(ellipse(122, 84, (0, 44)), "#f2aab4", name="muzzle"),
        eye((-46, -28), 34, 38),
        eye((46, -28), 34, 38),
        filled(ellipse(56, 46, (58, 42)), "#3f3833", name="spot"),
        filled(ellipse(64, 54, (-56, -50)), "#3f3833", name="spot"),
        filled(ellipse(192, 172), "#f7f3ec", name="head"),
        filled(ellipse(64, 40), "#f2d9a8",
               wiggle((-104, -18), base_rot=-16, amp=5, period=32), name="ear"),
        filled(ellipse(64, 40), "#f2d9a8",
               wiggle((104, -18), base_rot=16, amp=5, period=32, phase=0.5),
               name="ear"),
        filled(triangle(24, 34, tilt=-6), "#e8dcc2",
               transform(pos=(-56, -78), rotation=-14), name="horn"),
        filled(triangle(24, 34, tilt=6), "#e8dcc2",
               transform(pos=(56, -78), rotation=14), name="horn"),
    ]
