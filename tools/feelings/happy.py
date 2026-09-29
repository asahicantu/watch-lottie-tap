from feeling_parts import backdrop, bounce, filled_mouth, head, std_eyes

COLOR = "#FFC93C"


def happy():
    return [
        filled_mouth([(-22, 4), (0, 26), (22, 4), (0, 10)], pos=(0, 38)),
        *std_eyes(),
        head(),
        backdrop(COLOR),
    ], bounce
