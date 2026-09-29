from feeling_parts import backdrop, droop, head, human_eye, mouth

COLOR = "#5C7A99"


def lonely():
    return [
        mouth([(-18, 28), (0, 22), (18, 28)], pos=(0, 34), width=5),
        human_eye((-23, -6), w=24, h=18, lash=False),
        human_eye((23, -6), w=24, h=18, lash=False),
        head(),
        backdrop(COLOR),
    ], droop
