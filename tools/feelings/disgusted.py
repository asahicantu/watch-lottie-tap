from feeling_parts import backdrop, brow, head, human_eye, mouth, sway

COLOR = "#8BC34A"


def disgusted():
    return [
        mouth([(-18, 26), (-4, 34), (6, 20), (18, 28)], pos=(0, 30), width=6),
        brow((-23, -22), 14),
        brow((23, -22), -4),
        human_eye((-23, -8), w=26, h=16),
        human_eye((23, -8), w=26, h=20),
        head(),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=4, period=50)
