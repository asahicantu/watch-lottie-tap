from feeling_parts import backdrop, closed_eye, droop, head, mouth

COLOR = "#A79E8C"


def tired():
    return [
        mouth([(-16, 30), (0, 34), (16, 30)], pos=(0, 34), width=5),
        closed_eye((-23, -4), w=24), closed_eye((23, -4), w=24),
        head(),
        backdrop(COLOR),
    ], droop
