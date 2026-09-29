from feeling_parts import backdrop, closed_eye, head, mouth, pulse

COLOR = "#7FD1B9"


def calm():
    return [
        mouth([(-18, 14), (0, 20), (18, 14)], pos=(0, 34), width=5),
        closed_eye((-23, -6)), closed_eye((23, -6)),
        head(),
        backdrop(COLOR),
    ], lambda layer: pulse(layer, base=100, amp=4, period=110)
