from feeling_parts import bounce, brow, ellipse, face, filled, std_eyes, transform

FACE = "#F5A623"


def surprised():
    return [
        filled(ellipse(22, 28), "#2b2b2b", tr=transform(pos=(0, 18)), name="mouth-o"),
        brow((-17, -26), 8), brow((17, -26), -8),
        *std_eyes(w=20, h=24, y=-10),
        face(FACE),
    ], lambda layer: bounce(layer, amp=10, period=20)
