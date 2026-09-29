from feeling_parts import brow, ellipse, face, filled, jitter, std_eyes, sweat, transform

FACE = "#8E7CC3"


def scared():
    return [
        sweat((34, -28)),
        filled(ellipse(20, 26), "#2b2b2b", tr=transform(pos=(0, 18)), name="mouth-o"),
        brow((-17, -24), 26), brow((17, -24), -26),
        *std_eyes(w=18, h=22),
        face(FACE),
    ], jitter
