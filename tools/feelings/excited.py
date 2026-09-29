from feeling_parts import backdrop, bounce, filled_mouth, head, spark, std_eyes

COLOR = "#FF6F61"


def excited():
    return [
        spark((-62, -56), color="#FFE066"),
        spark((62, -50), color="#FFE066", size=8),
        filled_mouth([(-24, 4), (0, 30), (24, 4), (0, 12)], pos=(0, 38)),
        *std_eyes(w=34, h=26),
        head(),
        backdrop(COLOR),
    ], lambda layer: bounce(layer, amp=18, period=26)
