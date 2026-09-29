from feeling_parts import (
    backdrop, brows, eyes, gloom_lines, head, jitter, open_mouth, sweat,
)

COLOR = "#8E7CC3"


def scared():
    return [
        sweat((70, -40)),
        gloom_lines(),
        open_mouth(32, 22, (0, 62), kind="wail", tongue=False),
        *brows(y=-38, tilt=20, arch=4),
        # huge whites, pin-prick pupils
        *eyes(w=34, h=32, iris_scale=0.55, pupil_scale=0.8, lash=False),
        head(cheeks=15),
        backdrop(COLOR),
    ], jitter
