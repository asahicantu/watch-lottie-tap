from feeling_parts import backdrop, brows, closed_eyes, head, pulse, smile, twinkle

COLOR = "#7FD1B9"


def calm():
    return [
        twinkle((-72, -64), color="#FFFFFF", size=7, period=90),
        twinkle((70, -70), color="#FFFFFF", size=6, period=90, delay=45),
        smile(w=26, depth=7, pos=(0, 48), width=4.5),
        *brows(y=-32, tilt=3, arch=3, thick=6),
        *closed_eyes(kind="calm", w=26),
        head(),
        backdrop(COLOR),
    ], lambda layer: pulse(layer, base=100, amp=3, period=90)
