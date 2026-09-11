from critter_parts import eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def rabbit():
    fur, inner, pink = "#ece7df", "#f3b9c4", "#e08fa0"
    ear = lambda x, ph: group(
        [filled(rect(24, 116, (0, -66), radius=12), inner, name="inner"),
         filled(rect(46, 152, (0, -76), radius=23), fur, name="outer")],
        wiggle((x, -54), base_rot=x * 0.16, amp=9, period=26, phase=ph), name="ear")
    whisker = lambda x, y: outlined(path([(0, 0), (x, 0)], closed=False), "#cfc7bc", 4,
                                    transform(pos=(x * 0.5, y)), name="whisker")
    return [
        whisker(66, 32), whisker(70, 44), whisker(-66, 32), whisker(-70, 44),
        filled(rect(28, 24, (0, 12), radius=6), "#ffffff",
               transform(pos=(0, 46)), name="teeth"),
        filled(triangle(24, 18, pos=(0, 8)), pink,
               transform(rotation=180), name="nose"),
        filled(ellipse(52, 42, (-38, 34)), "#f8f4ee", name="cheek"),
        filled(ellipse(52, 42, (38, 34)), "#f8f4ee", name="cheek"),
        eye((-46, -12), 32, 36, iris="#4a3b3b"), eye((46, -12), 32, 36, iris="#4a3b3b"),
        filled(ellipse(176, 162), fur, name="head"),
        ear(-38, 0.0), ear(38, 0.5),
    ]
