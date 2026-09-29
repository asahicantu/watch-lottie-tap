from feeling_parts import closed_eye, droop, face, mouth

FACE = "#A79E8C"


def tired():
    return [
        mouth([(-16, 20), (0, 24), (16, 20)], width=5),
        closed_eye((-17, -6), w=18), closed_eye((17, -6), w=18),
        face(FACE),
    ], droop
