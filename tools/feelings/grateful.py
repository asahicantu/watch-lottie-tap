from feeling_parts import (
    backdrop, blushes, brows, closed_eyes, float_heart, head, pulse, smile,
)

COLOR = "#F2C14E"


def grateful():
    return [
        float_heart((66, -52), size=14, period=90),
        smile(w=30, depth=10, pos=(0, 46)),
        *blushes(hatch=False, opacity=50),
        *brows(y=-34, tilt=10, arch=4),
        *closed_eyes(kind="happy", w=26),
        head(),
        backdrop(COLOR),
    ], lambda layer: pulse(layer, base=100, amp=5, period=90)
