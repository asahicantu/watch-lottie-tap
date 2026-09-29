from feeling_parts import backdrop, brow, head, human_eye, mouth, shake

COLOR = "#E15554"


def angry():
    return [
        mouth([(-20, 30), (0, 18), (20, 30)], pos=(0, 34), width=7),
        brow((-23, -22), 22),
        brow((23, -22), -22),
        human_eye((-23, -6), h=18),
        human_eye((23, -6), h=18),
        head(),
        backdrop(COLOR),
    ], shake
