from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, rect


def deer():
    fur_c = "#8B4513"
    antler = lambda x, ph: group([filled(rect(10, 60, (0, -30), radius=5), "#D7CCC8"),
                                 filled(rect(30, 8, (0, -50), radius=4), "#D7CCC8")],
                                wiggle((x, -90), base_rot=x*0.2, amp=5, period=40, phase=ph), name="antler")
    spots = [filled(ellipse(15, 10, (x, y)), "#FFFFFF") for x, y in [(-30, 40), (30, 40), (0, 60)]]
    return [
        antler(-40, 0.0), antler(40, 0.5),
    ] + spots + [
        dot_eye((-40, -20), 16), dot_eye((40, -20), 16),
        filled(ellipse(170, 160), fur_c, name="head"),
        filled(triangle(30, 50), fur_c, wiggle((-60, -70), base_rot=-30), name="ear"),
        filled(triangle(30, 50), fur_c, wiggle((60, -70), base_rot=30, phase=0.5), name="ear"),
    ]
