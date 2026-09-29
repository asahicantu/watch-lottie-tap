from feeling_parts import backdrop, brow, head, human_eye, mouth, spin_wobble

COLOR = "#B39DDB"


def confused():
    return [
        mouth([(-16, 30), (0, 24), (16, 32)], pos=(0, 34), width=5),
        brow((-23, -28), 20),
        brow((23, -32), -4),
        human_eye((-23, -8), w=26, h=20),
        human_eye((23, -8), w=26, h=20),
        head(),
        backdrop(COLOR),
    ], lambda layer: spin_wobble(layer, amp=10, period=75)
