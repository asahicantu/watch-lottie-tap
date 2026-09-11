from critter_parts import eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, rect


def zebra():
    base_c, stripe_c = "#FFFFFF", "#424242"
    stripes = group([filled(rect(40 if i == 1 else 100, 15, (0, i*30 - 60),
                                 radius=5), stripe_c) for i in range(5)],
                    name="stripes")
    return [
        eye((-45, -30), 32, 36), eye((45, -30), 32, 36),
        stripes,
        filled(ellipse(160, 190), base_c, name="head"),
        filled(triangle(35, 60), base_c, wiggle((-55, -85), base_rot=-15), name="ear"),
        filled(triangle(35, 60), base_c, wiggle((55, -85), base_rot=15, phase=0.5), name="ear"),
    ]
