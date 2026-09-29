from feeling_parts import closed_eye, face, mouth, pulse

FACE = "#7FD1B9"


def calm():
    return [
        mouth([(-18, 12), (0, 18), (18, 12)], width=5),
        closed_eye((-17, -8)), closed_eye((17, -8)),
        face(FACE),
    ], lambda layer: pulse(layer, base=100, amp=4, period=110)
