from feeling_parts import brow, droop, face, mouth, std_eyes, tear

FACE = "#6FA8DC"


def sad():
    return [
        tear((26, 18)),
        mouth([(-24, 20), (0, 4), (24, 20)]),
        brow((-17, -22), 20), brow((17, -22), -20),
        *std_eyes(),
        face(FACE),
    ], droop
