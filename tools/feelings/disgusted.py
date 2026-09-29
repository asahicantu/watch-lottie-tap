from feeling_parts import brow, eye, face, mouth, sway

FACE = "#8BC34A"


def disgusted():
    return [
        mouth([(-20, 18), (-6, 26), (6, 10), (20, 20)]),
        brow((-17, -20), 14), brow((17, -20), -6),
        eye((-17, -8), w=14, h=10), eye((17, -8), w=14, h=16),
        face(FACE),
    ], lambda layer: sway(layer, amp=4, period=50)
