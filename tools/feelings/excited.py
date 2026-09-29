from feeling_parts import (
    GOLD, backdrop, blushes, bounce, brows, eyes, head, open_mouth, twinkle,
)

COLOR = "#FF6F61"


def excited():
    return [
        twinkle((-72, -62), GOLD, size=11, period=30),
        twinkle((72, -56), GOLD, size=9, period=30, delay=15),
        twinkle((-84, 8), "#FFFFFF", size=7, period=45, delay=10),
        twinkle((86, 14), "#FFFFFF", size=7, period=45, delay=32),
        open_mouth(46, 30, (0, 40), kind="grin"),
        *blushes(hatch=False, opacity=55),
        *brows(y=-38, tilt=4, arch=7),
        # sparkly star catch-lights in wide eyes
        *eyes(w=34, h=30, shine=True, iris_scale=1.05, look=(0, -1)),
        head(),
        backdrop(COLOR),
    ], lambda layer: bounce(layer, amp=18, period=30)
