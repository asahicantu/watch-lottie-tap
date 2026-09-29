from feeling_parts import brow, eye, face, mouth, shake

FACE = "#E15554"


def angry():
    return [
        mouth([(-22, 24), (0, 14), (22, 24)], width=7),
        brow((-17, -18), -18), brow((17, -18), 18),
        eye((-17, -8), h=12), eye((17, -8), h=12),
        face(FACE),
    ], shake
