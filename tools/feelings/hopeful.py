from feeling_parts import bounce, face, mouth, spark, std_eyes

FACE = "#6FCF97"


def hopeful():
    return [
        spark((0, -66), color="#FFE066", size=9),
        mouth([(-18, 12), (0, 20), (18, 12)], width=5),
        *std_eyes(),
        face(FACE),
    ], lambda layer: bounce(layer, amp=8, period=60)
