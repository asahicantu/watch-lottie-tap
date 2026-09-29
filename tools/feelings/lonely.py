from feeling_parts import backdrop, brows, droop, ellipsis, eyes, head, smile

COLOR = "#5C7A99"


def lonely():
    return [
        ellipsis((70, -80)),
        smile(w=22, depth=-5, pos=(0, 50), width=4.5, dimples=False),
        *brows(y=-30, tilt=12, arch=3),
        # glossy eyes looking down and aside
        *eyes(w=28, h=24, lid=0.28, tilt=3, look=(-4, 5), glossy=True),
        head(cheeks=30),
        backdrop(COLOR),
    ], droop
