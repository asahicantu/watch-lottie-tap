from critter_parts import eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def cat():
    fur, inner = "#f0a04b", "#f6c7a8"

    def ear(x, phase):
        return group(
            [filled(triangle(52, 46, tilt=x * 0.18), inner,
                    transform(scale=(62, 62)), name="inner"),
             filled(triangle(74, 72, tilt=x * 0.14), fur, name="outer")],
            wiggle((x, -58), base_rot=x * 0.09, amp=6, period=26, phase=phase),
            name="ear")

    def whisker(x, y, tilt):
        return outlined(path([(0, 0), (x, tilt)], closed=False), "#f7e6d4", 5,
                        transform(pos=(x * 0.42, y)), name="whisker")

    return [
        whisker(74, 8, -12), whisker(80, 22, 2), whisker(74, 36, 16),
        whisker(-74, 8, -12), whisker(-80, 22, 2), whisker(-74, 36, 16),
        smile(46, 16, y=34, color="#8a4a3c", w=6),
        filled(triangle(26, 20, pos=(0, 10)), "#e2657a",
               transform(rotation=180), name="nose"),
        eye((-44, -10), 36, 42, iris="#4b9b52"),
        eye((44, -10), 36, 42, iris="#4b9b52"),
        filled(ellipse(196, 176), fur, name="head"),
        ear(-62, 0.0), ear(62, 0.5),
    ]
