from feeling_parts import brow, eye, face, mouth, sway

FACE = "#7CB342"


def jealous():
    return [
        mouth([(-18, 20), (0, 14), (18, 20)], width=6),
        brow((-17, -18), -16), brow((17, -18), 4),
        eye((-17, -8), w=14, h=10), eye((17, -8), w=14, h=10),
        face(FACE),
    ], lambda layer: sway(layer, amp=5, period=55)
