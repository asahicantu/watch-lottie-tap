from critter_parts import eye, wiggle
from lottie_kit import ellipse, filled, group, rect


def lemur():
    fur_c, tail_c = "#9E9E9E", "#424242"
    tail = group([filled(rect(30, 20, (0, i*20)), (tail_c if i % 2 == 0 else "#FFFFFF")) for i in range(6)],
                 wiggle((100, 40), base_rot=30, amp=10, period=40), name="tail")
    return [
        tail,
        eye((-45, -10), 40, 44, iris="#FFD54F", white="#212121"), eye((45, -10), 40, 44, iris="#FFD54F", white="#212121"),
        filled(ellipse(170, 160), fur_c, name="head"),
    ]
