from feeling_parts import backdrop, brows, eyes, head, jitter, open_mouth, sweat

COLOR = "#C9ADA7"


def nervous():
    return [
        sweat((66, -44)),
        sweat((-72, -30), size=6, delay=45),
        # a clenched, wobbly grimace
        open_mouth(34, 12, (0, 52), kind="rect", all_teeth=True, bend=-1, rotation=4),
        *brows(y=-32, tilt=16, arch=3),
        # small pupils flicking side to side
        *eyes(w=28, h=26, iris_scale=0.7, look_path=[
            (0, (-5, 0)), (0.2, (-5, 0)), (0.25, (5, 0)), (0.45, (5, 0)),
            (0.5, (-5, 0)), (0.7, (-5, 0)), (0.75, (5, 0)), (0.95, (5, 0)), (1, (-5, 0)),
        ]),
        head(),
        backdrop(COLOR),
    ], lambda layer: jitter(layer, amp=3, period=10)
