from feeling_parts import blush, face, jitter, mouth, std_eyes

FACE = "#F4989C"


def embarrassed():
    return [
        blush((-40, 6), name="blush-l"),
        blush((40, 6), name="blush-r"),
        mouth([(-16, 16), (0, 22), (16, 16)], width=5),
        *std_eyes(w=12, h=14),
        face(FACE),
    ], lambda layer: jitter(layer, amp=3, period=14)
