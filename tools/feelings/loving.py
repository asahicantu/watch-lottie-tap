from feeling_parts import (
    backdrop, blushes, brows, eyes, float_heart, head, open_mouth, pulse,
)

COLOR = "#F06292"
HEART_COLOR = "#FF4D6D"


def loving():
    return [
        float_heart((-64, -50), HEART_COLOR, size=16, period=90),
        float_heart((66, -46), HEART_COLOR, size=13, period=90, delay=30),
        float_heart((0, -96), HEART_COLOR, size=11, period=90, delay=60),
        open_mouth(30, 16, (0, 44), kind="grin"),
        *blushes(opacity=80),
        *brows(y=-36, tilt=6, arch=5),
        *eyes(w=32, h=28, heart_iris=True, blink_at=None),
        head(),
        backdrop(COLOR),
    ], lambda layer: pulse(layer, base=100, amp=6, period=45)
