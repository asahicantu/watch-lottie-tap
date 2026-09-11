from critter_parts import dot_eye
from lottie_kit import ellipse, filled, group, transform


def turtle():
    shell_c, skin_c = "#43A047", "#8BC34A"
    pattern = group([filled(ellipse(40, 40, (x, y)), "#2E7D32") for x, y in [(-40, -30), (40, -30), (0, 20)]], name="pattern")
    return [
        pattern,
        filled(ellipse(180, 140), shell_c, name="shell"),
        dot_eye((-40, -60), 12), dot_eye((40, -60), 12),
        filled(ellipse(100, 80, (0, -70)), skin_c, name="head"),
        filled(ellipse(50, 30, (-80, 40)), skin_c, transform(rotation=-30), name="flipper"),
        filled(ellipse(50, 30, (80, 40)), skin_c, transform(rotation=30), name="flipper"),
    ]
