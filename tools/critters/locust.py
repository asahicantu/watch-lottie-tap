from critter_parts import dot_eye
from lottie_kit import ellipse, filled, outlined, path, transform


def locust():
    skin = "#9E9D24"
    return [
        outlined(path([(-20, -70), (-40, -110)], closed=False), skin, 5, name="antenna"),
        outlined(path([(20, -70), (40, -110)], closed=False), skin, 5, name="antenna"),
        dot_eye((-40, -30), 15), dot_eye((40, -30), 15),
        filled(ellipse(130, 200), skin, name="body"),
        filled(ellipse(40, 150), "#C0CA33", transform(pos=(-60, 20), rotation=-10), name="wing"),
        filled(ellipse(40, 150), "#C0CA33", transform(pos=(60, 20), rotation=10), name="wing"),
    ]
