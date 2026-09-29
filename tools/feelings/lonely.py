from feeling_parts import droop, eye, face, mouth

FACE = "#5C7A99"


def lonely():
    return [
        mouth([(-18, 18), (0, 12), (18, 18)], width=5),
        eye((-17, -8), w=12, h=16), eye((17, -8), w=12, h=16),
        face(FACE),
    ], droop
