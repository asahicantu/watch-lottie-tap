from feeling_parts import backdrop, brow, droop, head, human_eye, mouth, tear

COLOR = "#6FA8DC"


def sad():
    return [
        tear((32, 14)),
        mouth([(-20, 30), (0, 16), (20, 30)], pos=(0, 34), width=5),
        brow((-23, -26), -20),
        brow((23, -26), 20),
        human_eye((-23, -6), lash=False),
        human_eye((23, -6), lash=False),
        head(),
        backdrop(COLOR),
    ], droop
