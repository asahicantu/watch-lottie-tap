from feeling_parts import backdrop, brows, droop, eyes, head, open_mouth, uniform, zzz

COLOR = "#A79E8C"


def tired():
    return [
        zzz((62, -70), size=14, period=90),
        zzz((78, -92), size=10, period=90, delay=45),
        # a slow yawn that opens and closes
        open_mouth(20, 26, (0, 54), kind="oval", teeth=False,
                   scale=uniform([(0, 45), (0.4, 105), (0.65, 100), (1, 45)])),
        *brows(y=-28, tilt=6, arch=2),
        *eyes(w=30, h=24, lid=0.58, tilt=2, look=(0, 3), bags=True, lash=False),
        head(cheeks=30),
        backdrop(COLOR),
    ], droop
