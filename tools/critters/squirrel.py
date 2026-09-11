from critter_parts import dot_eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled


def squirrel():
    fur_c, tail_c = "#8D6E63", "#6D4C41"
    tail = filled(ellipse(80, 140, (0, -70)), tail_c,
                  wiggle((80, 20), base_rot=30, amp=10, period=40), name="tail")
    return [
        tail,
        filled(ellipse(40, 50, (0, 40)), "#FFCC80", name="acorn"),
        smile(30, 10, y=25, color="#3E2723", w=3),
        dot_eye((-35, -10), 14), dot_eye((35, -10), 14),
        filled(ellipse(150, 140), fur_c, name="head"),
        filled(triangle(30, 40), fur_c, wiggle((-50, -60), base_rot=-20), name="ear"),
        filled(triangle(30, 40), fur_c, wiggle((50, -60), base_rot=20, phase=0.5), name="ear"),
    ]
