from feeling_parts import bounce, face, filled_mouth, spark, std_eyes

FACE = "#FF6F61"


def excited():
    return [
        spark((-52, -50), color="#FFE066"),
        spark((52, -46), color="#FFE066", size=8),
        filled_mouth([(-24, 8), (0, 30), (24, 8), (0, 16)]),
        *std_eyes(w=18, h=20),
        face(FACE),
    ], lambda layer: bounce(layer, amp=18, period=26)
