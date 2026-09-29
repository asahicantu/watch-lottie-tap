from feeling_parts import brow, eye, face, mouth, spin_wobble

FACE = "#B39DDB"


def confused():
    return [
        mouth([(-16, 16), (0, 10), (16, 18)], width=5),
        brow((-17, -22), 18), brow((17, -26), -2),
        eye((-17, -8), w=14, h=16), eye((17, -8), w=14, h=16),
        face(FACE),
    ], lambda layer: spin_wobble(layer, amp=10, period=75)
