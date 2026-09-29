from feeling_parts import (
    anger_mark, backdrop, brow_furrow, brows, eyes, face_tint, head, open_mouth,
    shake, steam,
)

COLOR = "#E15554"


def angry():
    return [
        anger_mark((60, -64)),
        steam((-98, -64), -1, period=30),
        steam((98, -64), 1, period=30, delay=15),
        open_mouth(40, 16, (0, 52), kind="rect", all_teeth=True, bend=6),
        brow_furrow(),
        *brows(y=-24, tilt=-24, thick=8.5, arch=2),
        *eyes(w=30, h=24, lid=0.22, tilt=-7, iris_scale=0.85),
        head(cheeks=65, tint=face_tint("#E0303A", opacity=18, pos=(0, 30), size=(150, 70),
                                      pulse_period=30)),
        backdrop(COLOR),
    ], shake
