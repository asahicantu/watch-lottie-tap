from feeling_parts import backdrop, blushes, brows, eyes, head, jitter, sweat, wavy_mouth

COLOR = "#F4989C"


def embarrassed():
    return [
        sweat((70, -42)),
        *blushes(w=38, h=22, opacity=85),
        wavy_mouth(w=22, amp=2, waves=2, pos=(0, 50), bend=-2),
        *brows(y=-32, tilt=12, arch=3),
        # won't meet your gaze: eyes turned down and away
        *eyes(w=28, h=24, lid=0.18, tilt=2, look=(-6, 4)),
        head(),
        backdrop(COLOR),
    ], lambda layer: jitter(layer, amp=3, period=15)
