from feeling_parts import backdrop, brows, eyes, head, smile, sway, twinkle

COLOR = "#D4A017"


def proud():
    return [
        twinkle((-58, -92), "#FFFFFF", size=10, period=45),
        twinkle((82, -30), "#FFFFFF", size=7, period=45, delay=22),
        # a lopsided, pleased-with-myself smirk
        smile(w=34, depth=8, pos=(2, 46), skew=-5),
        *brows(y=-36, tilt=-4, arch=6),
        # smug half-closed lids, chin up
        *eyes(w=30, h=24, lid=0.42, look=(0, -2)),
        head(),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=6, period=90)
