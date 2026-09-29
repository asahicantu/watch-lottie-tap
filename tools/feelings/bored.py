from feeling_parts import backdrop, head, human_eye, mouth, sway

COLOR = "#9DA5B4"


def bored():
    return [
        mouth([(-18, 30), (18, 30)], pos=(0, 34), width=5, closed=False),
        human_eye((-23, -6), w=28, h=12, lash=False),
        human_eye((23, -6), w=28, h=12, lash=False),
        head(),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=3, period=140)
