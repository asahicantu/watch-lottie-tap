from feeling_parts import backdrop, blush, head, human_eye, jitter, mouth

COLOR = "#F4989C"


def embarrassed():
    return [
        blush((-58, 34), name="blush-l"),
        blush((58, 34), name="blush-r"),
        mouth([(-14, 30), (0, 34), (14, 30)], pos=(0, 34), width=5),
        human_eye((-23, -6), w=26, h=18, lash=False),
        human_eye((23, -6), w=26, h=18, lash=False),
        head(),
        backdrop(COLOR),
    ], lambda layer: jitter(layer, amp=3, period=14)
