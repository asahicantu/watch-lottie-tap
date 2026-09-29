from feeling_parts import backdrop, bounce, brow, head, human_eye, open_mouth

COLOR = "#F5A623"


def surprised():
    return [
        open_mouth(22, 28, (0, 36)),
        brow((-23, -32), 10),
        brow((23, -32), -10),
        human_eye((-23, -10), w=30, h=30),
        human_eye((23, -10), w=30, h=30),
        head(),
        backdrop(COLOR),
    ], lambda layer: bounce(layer, amp=10, period=20)
