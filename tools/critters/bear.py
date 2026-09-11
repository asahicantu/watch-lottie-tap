from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, group


def bear():
    fur, muzzle = "#8a6446", "#d8b48c"
    return [
        smile(46, 18, y=48, color="#4a3428", w=6),
        filled(ellipse(42, 32, (0, 26)), "#3a2a20", name="nose"),
        filled(ellipse(106, 84, (0, 42)), muzzle, name="muzzle"),
        dot_eye((-42, -18), 18), dot_eye((42, -18), 18),
        filled(ellipse(192, 178), fur, name="head"),
        group([filled(ellipse(34, 34), muzzle, name="inner"),
               filled(ellipse(58, 58), fur, name="outer")],
              wiggle((-72, -76), amp=5, period=30), name="ear"),
        group([filled(ellipse(34, 34), muzzle, name="inner"),
               filled(ellipse(58, 58), fur, name="outer")],
              wiggle((72, -76), amp=5, period=30, phase=0.5), name="ear"),
    ]
