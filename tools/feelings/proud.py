from feeling_parts import brow, face, filled_mouth, std_eyes, sway

FACE = "#D4A017"


def proud():
    return [
        filled_mouth([(-24, 10), (0, 26), (24, 10), (0, 16)]),
        brow((-17, -22), -10), brow((17, -22), 10),
        *std_eyes(),
        face(FACE),
    ], lambda layer: sway(layer, amp=6, period=80)
