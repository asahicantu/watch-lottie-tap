from feeling_parts import backdrop, bounce, brows, eyes, head, open_mouth, twinkle

COLOR = "#FFC93C"


def happy():
    return [
        twinkle((-70, -70), size=9, period=45),
        twinkle((72, -62), size=7, period=45, delay=22),
        open_mouth(42, 26, (0, 42), kind="grin"),
        *brows(y=-34, tilt=5, arch=6),
        # cheeks push the lower lids up - the squint of a real smile
        *eyes(w=30, h=26, lower=0.3, look=(0, -1)),
        head(cheeks=60),
        backdrop(COLOR),
    ], bounce
