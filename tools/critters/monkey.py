from critter_parts import eye, nostrils, smile, tuft, wiggle
from lottie_kit import ellipse, filled, group


def monkey():
    fur, face = "#8a5a3b", "#dba97c"
    return [
        smile(56, 22, y=44, color="#7a4a2c", w=6),
        nostrils(11, 28, 13, 10, "#7a4a2c"),
        eye((-34, -8), 32, 36, iris="#3a2a20"), eye((34, -8), 32, 36, iris="#3a2a20"),
        filled(ellipse(136, 126, (0, 12)), face, name="face"),
        filled(ellipse(182, 170), fur, name="head"),
        tuft(0, -84, 3, fur, w=20, h=34, spread=18),
        group([filled(ellipse(40, 40), face, name="inner"),
               filled(ellipse(62, 62), fur, name="outer")],
              wiggle((-96, -4), amp=6, period=28), name="ear"),
        group([filled(ellipse(40, 40), face, name="inner"),
               filled(ellipse(62, 62), fur, name="outer")],
              wiggle((96, -4), amp=6, period=28, phase=0.5), name="ear"),
    ]
