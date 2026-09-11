from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, rect


def moose():
    body, antlers = "#6D4C41", "#D7CCC8"
    def antler(x, phase):
        return group([filled(rect(80, 40, (x*0.5, -40), radius=20), antlers),
                      filled(rect(20, 60, (0, -20)), antlers)],
                     wiggle((x, -70), base_rot=x*0.2, amp=10, period=40, phase=phase), name="antler")

    return [
        filled(ellipse(120, 100, (0, 50)), "#4E342E", name="muzzle"),
        dot_eye((-40, -20), 16), dot_eye((40, -20), 16),
        filled(ellipse(190, 170), body, name="head"),
        antler(-80, 0), antler(80, 0.5),
    ]
