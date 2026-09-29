from feeling_parts import backdrop, brow, head, human_eye, mouth, sway

COLOR = "#7CB342"


def jealous():
    return [
        mouth([(-18, 30), (0, 22), (18, 30)], pos=(0, 34), width=6),
        brow((-23, -22), 16),
        brow((23, -22), -4),
        human_eye((-23, -8), w=24, h=16),
        human_eye((23, -8), w=24, h=16),
        head(),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=5, period=55)
