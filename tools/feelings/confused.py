from feeling_parts import (
    backdrop, brow, eyes, head, question_mark, spin_wobble, wavy_mouth,
)

COLOR = "#B39DDB"


def confused():
    return [
        question_mark((74, -78)),
        wavy_mouth(w=26, amp=3, waves=1.5, pos=(2, 50), rotation=-6),
        brow((-30, -38), -1, tilt=10, arch=6),
        brow((30, -26), 1, tilt=-8, arch=2),
        *eyes(left={"w": 32, "h": 30}, right={"w": 28, "h": 22, "lid": 0.25},
              look_path=[(0, (-4, -4)), (0.45, (-4, -4)), (0.55, (4, -4)),
                         (0.95, (4, -4)), (1, (-4, -4))]),
        head(),
        backdrop(COLOR),
    ], lambda layer: spin_wobble(layer, amp=10, period=90)
