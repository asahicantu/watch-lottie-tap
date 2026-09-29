from feeling_parts import backdrop, brow, eyes, head, open_mouth, spin_wobble, twinkle

COLOR = "#4FC3F7"


def curious():
    return [
        twinkle((74, -70), size=9, period=45),
        open_mouth(13, 15, (6, 52), kind="oval", teeth=False, tongue=False),
        brow((-30, -30), -1, tilt=2, arch=3),
        brow((30, -40), 1, tilt=-6, arch=7),
        # glancing one way, then the other
        *eyes(right={"w": 34, "h": 30}, w=30, h=26, iris_scale=0.95, look_path=[
            (0, (-6, -1)), (0.3, (-6, -1)), (0.4, (6, -1)), (0.7, (6, -1)),
            (0.8, (-6, -1)), (1, (-6, -1)),
        ]),
        head(),
        backdrop(COLOR),
    ], lambda layer: spin_wobble(layer, amp=8, period=90)
