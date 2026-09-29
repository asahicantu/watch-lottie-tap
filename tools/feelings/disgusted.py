from feeling_parts import (
    backdrop, brows, eyes, head, nose_wrinkle, stink_lines, sway,
    tongue_out,
)

COLOR = "#8BC34A"


def disgusted():
    return [
        stink_lines((-70, 30), period=45),
        stink_lines((-84, 16), period=45, delay=22),
        tongue_out((0, 50), rotation=-5),
        nose_wrinkle(),
        *brows(y=-26, tilt=-10, arch=2, right={"tilt": -2, "y": -30}),
        # scrunched: lids down, cheeks up
        *eyes(w=28, h=22, lid=0.25, lower=0.3, look=(3, 0)),
        head(cheeks=20),
        backdrop(COLOR),
    ], lambda layer: sway(layer, amp=4, period=45)
