from feeling_parts import closed_eye, face, filled_mouth, heart_half, pulse

FACE = "#F06292"


def loving():
    return [
        heart_half((-16, -30), 45, FACE, name="heart-a"),
        heart_half((16, -30), -45, FACE, name="heart-b"),
        filled_mouth([(-20, 8), (0, 24), (20, 8), (0, 14)]),
        closed_eye((-17, -8)), closed_eye((17, -8)),
        face(FACE),
    ], lambda layer: pulse(layer, base=100, amp=10, period=50)
