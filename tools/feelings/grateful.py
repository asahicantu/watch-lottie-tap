from feeling_parts import closed_eye, face, mouth, pulse

FACE = "#F2C14E"


def grateful():
    return [
        mouth([(-20, 10), (0, 20), (20, 10)], width=5),
        closed_eye((-17, -8)), closed_eye((17, -8)),
        face(FACE),
    ], lambda layer: pulse(layer, base=100, amp=6, period=90)
