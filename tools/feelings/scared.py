from feeling_parts import backdrop, brow, head, human_eye, jitter, open_mouth, sweat

COLOR = "#8E7CC3"


def scared():
    return [
        sweat((40, -30)),
        open_mouth(20, 24, (0, 36), tongue=False),
        brow((-23, -32), -14),
        brow((23, -32), 14),
        human_eye((-23, -8), w=32, h=28),
        human_eye((23, -8), w=32, h=28),
        head(),
        backdrop(COLOR),
    ], jitter
