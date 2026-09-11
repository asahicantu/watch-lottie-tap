from critter_parts import pin_eye
from lottie_kit import ellipse, filled, group, outlined, path


def spider():
    body_c = "#000000"
    legs = []
    for i in range(4):
        y = i * 20 - 30
        legs.append(outlined(path([(-60, y), (-100, y - 20)], False), body_c, 6, name="leg"))
        legs.append(outlined(path([(60, y), (100, y - 20)], False), body_c, 6, name="leg"))
    eyes = group([pin_eye((x, y), 13, color="#FFFFFF")
                  for x, y in [(-34, -34), (0, -40), (34, -34),
                               (-16, -14), (16, -14)]], name="eyes")
    return legs + [
        eyes,
        filled(ellipse(140, 140), body_c, name="body"),
    ]
