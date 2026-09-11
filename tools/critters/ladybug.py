from critter_parts import dot_eye
from lottie_kit import ellipse, filled, group


def ladybug():
    red_c, black_c = "#D32F2F", "#212121"
    spots = group([filled(ellipse(25, 25, (x, y)), black_c) for x, y in [(-40, -20), (40, -20), (0, 40)]], name="spots")
    return [
        dot_eye((-32, -112), 8, color="#FFFFFF"),
        dot_eye((32, -112), 8, color="#FFFFFF"),
        spots,
        filled(ellipse(190, 170), red_c, name="body"),
        filled(ellipse(140, 110, (0, -92)), black_c, name="head"),
    ]
