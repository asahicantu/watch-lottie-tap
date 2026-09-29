from feeling_parts import bounce, face, filled_mouth, std_eyes

FACE = "#FFC93C"


def happy():
    return [
        filled_mouth([(-28, 6), (0, 34), (28, 6), (0, 14)]),
        *std_eyes(),
        face(FACE),
    ], bounce
