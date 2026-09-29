from feeling_parts import backdrop, brows, eyes, head, sigh_puff, smile, sway

COLOR = "#9DA5B4"


def bored():
    return [
        sigh_puff((22, 50), 1),
        smile(w=24, depth=-1, pos=(6, 50), dimples=False, skew=3),
        *brows(y=-26, tilt=-3, arch=1),
        # heavy lids, eyes rolling slowly up and across
        *eyes(w=30, h=24, lid=0.5, lash=False, look_path=[
            (0, (-5, -2)), (0.4, (-5, -2)), (0.55, (5, -3)), (0.9, (5, -3)), (1, (-5, -2)),
        ]),
        head(cheeks=30),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=3, period=90)
