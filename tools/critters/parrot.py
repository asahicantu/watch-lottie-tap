from critter_parts import FRAMES, eye, tuft
from lottie_kit import animated, ellipse, filled, path, transform


def parrot():
    feather, cheek, beak = "#3fb56a", "#f5c33b", "#f0a52a"
    return [
        filled(path([(-16, -8), (16, -8), (10, 16), (-10, 16)]), "#c96a13",
               transform(pos=(0, 50),
                         rotation=animated([(0, 0), (12, 14), (24, 0), (36, 14),
                                            (48, 0), (FRAMES, 0)])),
               name="lower-beak"),
        # hooked upper mandible: wide at the brow, curling to a point
        filled(path([(-28, -20), (28, -20), (20, 12), (4, 34), (-8, 16), (-22, 8)]),
               beak, transform(pos=(0, 28)), name="upper-beak"),
        filled(ellipse(34, 30, (-58, 4)), cheek, name="cheek"),
        filled(ellipse(34, 30, (58, 4)), cheek, name="cheek"),
        eye((-44, -26), 34, 36, iris="#2b2118"), eye((44, -26), 34, 36, iris="#2b2118"),
        filled(ellipse(178, 170), feather, name="head"),
        tuft(0, -86, 3, "#e8483c", w=26, h=54, spread=24),
    ]
