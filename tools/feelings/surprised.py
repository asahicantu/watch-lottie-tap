from feeling_parts import backdrop, bounce, brows, eyes, head, open_mouth, shock_lines

COLOR = "#F5A623"


def surprised():
    return [
        shock_lines((-94, -58), -1),
        shock_lines((94, -58), 1),
        open_mouth(24, 30, (0, 54), kind="oval", teeth=False),
        # brows shoot up with each hop
        *brows(y=-42, tilt=2, arch=7, pos_path=[
            (0, (0, 0)), (0.2, (0, -5)), (0.5, (0, 0)), (0.7, (0, -5)), (1, (0, 0)),
        ]),
        *eyes(w=34, h=34, iris_scale=0.7),
        head(),
        backdrop(COLOR),
    ], lambda layer: bounce(layer, amp=10, period=45)
