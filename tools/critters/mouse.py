from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def mouse():
    fur, pink = "#a9a29b", "#f2b6c0"
    ear = lambda x, ph: group(
        [filled(ellipse(58, 58), pink, name="inner"),
         filled(ellipse(88, 88), fur, name="outer")],
        wiggle((x, -54), amp=6, period=24, phase=ph), name="ear")
    whisker = lambda x, y: outlined(path([(0, 0), (x, 0)], closed=False), "#d8d2cb", 4,
                                    transform(pos=(x * 0.5, y)), name="whisker")
    return [
        whisker(62, 40), whisker(66, 52), whisker(-62, 40), whisker(-66, 52),
        filled(ellipse(24, 20, (0, 44)), pink, name="nose"),
        dot_eye((-32, 2), 16), dot_eye((32, 2), 16),
        filled(ellipse(160, 150), fur, name="head"),
        ear(-78, 0.0), ear(78, 0.5),
    ]
