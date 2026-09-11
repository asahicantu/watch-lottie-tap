from critter_parts import dot_eye
from lottie_kit import ellipse, filled, outlined, path, transform


def moth():
    body = "#9E9E9E"
    return [
        outlined(path([(-10, -50), (-40, -80)], closed=False), "#616161", 4, name="antenna"),
        outlined(path([(10, -50), (40, -80)], closed=False), "#616161", 4, name="antenna"),
        dot_eye((-30, -20), 18), dot_eye((30, -20), 18),
        filled(ellipse(120, 150), body, name="body"),
        filled(ellipse(90, 140), "#BDBDBD", transform(pos=(-70, 0), rotation=-30), name="wing"),
        filled(ellipse(90, 140), "#BDBDBD", transform(pos=(70, 0), rotation=30), name="wing"),
    ]
