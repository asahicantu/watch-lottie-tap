from feeling_parts import backdrop, brow, head, human_eye, open_mouth, spin_wobble

COLOR = "#4FC3F7"


def curious():
    return [
        open_mouth(16, 18, (4, 34), tongue=False),
        brow((-23, -30), 12),
        brow((23, -34), -22),
        human_eye((-23, -8), w=26, h=22),
        human_eye((23, -8), w=28, h=24),
        head(),
        backdrop(COLOR),
    ], lambda layer: spin_wobble(layer, amp=8, period=65)
