from feeling_parts import brow, ellipse, face, filled, spin_wobble, transform

FACE = "#4FC3F7"


def curious():
    return [
        filled(ellipse(16, 18), "#2b2b2b", tr=transform(pos=(4, 16)), name="mouth-o"),
        brow((-17, -24), 10), brow((17, -28), -22),
        filled(ellipse(15, 17), "#2b2b2b", tr=transform(pos=(-17, -8)), name="eye"),
        filled(ellipse(16, 19), "#2b2b2b", tr=transform(pos=(17, -8)), name="eye"),
        face(FACE),
    ], lambda layer: spin_wobble(layer, amp=8, period=65)
