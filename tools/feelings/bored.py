from feeling_parts import eye, face, mouth, sway

FACE = "#9DA5B4"


def bored():
    return [
        mouth([(-18, 18), (18, 18)], width=5, closed=False),
        eye((-17, -8), w=16, h=6), eye((17, -8), w=16, h=6),
        face(FACE),
    ], lambda layer: sway(layer, amp=3, period=140)
