from feeling_parts import backdrop, head, human_eye, jitter, mouth, sweat

COLOR = "#C9ADA7"


def nervous():
    return [
        sweat((38, -32), color="#8FD3F4"),
        mouth([(-16, 30), (-4, 26), (4, 32), (16, 28)], pos=(0, 34), width=5),
        human_eye((-23, -6), w=24, h=18),
        human_eye((23, -6), w=24, h=18),
        head(),
        backdrop(COLOR),
    ], lambda layer: jitter(layer, amp=4, period=10)
