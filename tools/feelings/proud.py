from feeling_parts import backdrop, brow, filled_mouth, head, human_eye, sway

COLOR = "#D4A017"


def proud():
    return [
        filled_mouth([(-24, 6), (0, 26), (24, 6), (0, 14)], pos=(0, 36)),
        brow((-23, -26), -8),
        brow((23, -26), 8),
        human_eye((-23, -8), h=20),
        human_eye((23, -8), h=20),
        head(),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=6, period=80)
