from critter_parts import dot_eye
from lottie_kit import ellipse, filled, group, path, transform


def toucan():
    body_c, beak_c = "#212121", "#FFAB00"
    beak = group([filled(path([(0, 0), (120, 0), (100, 60), (0, 40)], True), beak_c, name="beak-main"),
                  filled(ellipse(30, 30, (20, 10)), "#D32F2F", name="spot")],
                 transform(pos=(0, 0)), name="beak")
    return [
        beak,
        dot_eye((-40, -20), 15, color="#FFFFFF"), dot_eye((40, -20), 15, color="#FFFFFF"),
        filled(ellipse(160, 160), body_c, name="head"),
    ]
