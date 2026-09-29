from feeling_parts import backdrop, brows, droop, eyes, head, smile, tear, tear_track

COLOR = "#6FA8DC"


def sad():
    return [
        tear((-40, 8), period=45),
        tear((40, 8), period=45, delay=22),
        tear_track(-1), tear_track(1),
        smile(w=30, depth=-9, pos=(0, 50), dimples=False, name="frown"),
        *brows(y=-32, tilt=18, arch=3),
        # wet, glossy eyes under lids that droop toward the outer corners
        *eyes(w=30, h=26, lid=0.15, tilt=4, look=(0, 3), glossy=True, iris_scale=1.08),
        head(),
        backdrop(COLOR),
    ], droop
