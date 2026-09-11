from critter_parts import dot_eye
from lottie_kit import ellipse, filled, group, outlined, path


def snail():
    shell_c, skin_c = "#8D6E63", "#F5F5F5"
    shell = group([outlined(ellipse(i*20, i*20), "#5D4037", 4) for i in range(1, 5)], name="spiral")
    return [
        shell,
        filled(ellipse(120, 120), shell_c, name="shell"),
        outlined(path([(-20, -40), (-40, -80)], False), skin_c, 4, name="stalk"),
        outlined(path([(20, -40), (40, -80)], False), skin_c, 4, name="stalk"),
        dot_eye((-40, -80), 8), dot_eye((40, -80), 8),
        filled(ellipse(160, 40, (0, 40)), skin_c, name="body"),
    ]
