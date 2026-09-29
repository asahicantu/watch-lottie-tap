from feeling_parts import eye, face, jitter, mouth, sweat

FACE = "#C9ADA7"


def nervous():
    return [
        sweat((32, -30), color="#8FD3F4"),
        mouth([(-16, 18), (-4, 14), (4, 20), (16, 16)], width=5),
        eye((-17, -8), w=12, h=14), eye((17, -8), w=12, h=14),
        face(FACE),
    ], lambda layer: jitter(layer, amp=4, period=10)
