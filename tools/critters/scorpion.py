from critter_parts import dot_eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, transform


def scorpion():
    body_c = "#212121"
    tail = group([filled(ellipse(30, 30, (0, -i*25)), body_c) for i in range(4)],
                 wiggle((0, -80), base_rot=0, amp=15, period=35), name="tail")
    return [
        tail,
        filled(triangle(20, 30), "#D32F2F", transform(pos=(0, -160)), name="stinger"),
        dot_eye((-30, -20), 8, color="#FFFFFF"), dot_eye((30, -20), 8, color="#FFFFFF"),
        filled(ellipse(160, 120), body_c, name="body"),
        filled(ellipse(50, 40, (-90, 0)), body_c, name="pincer"),
        filled(ellipse(50, 40, (90, 0)), body_c, name="pincer"),
    ]
