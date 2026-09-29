from feeling_parts import backdrop, closed_eye, head, mouth, pulse

COLOR = "#F2C14E"


def grateful():
    return [
        mouth([(-20, 12), (0, 24), (20, 12)], pos=(0, 34), width=5),
        closed_eye((-23, -6)), closed_eye((23, -6)),
        head(),
        backdrop(COLOR),
    ], lambda layer: pulse(layer, base=100, amp=6, period=90)
