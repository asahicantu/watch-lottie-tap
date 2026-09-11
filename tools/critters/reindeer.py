from critter_parts import eye, wiggle
from lottie_kit import ellipse, filled, group, path


def reindeer():
    body, antlers = "#A1887F", "#5D4037"
    def antler(x, phase):
        return group([filled(path([(0,0), (0,-60), (x*0.3, -80), (x*0.1, -50)], closed=False), antlers)],
                     wiggle((x, -70), base_rot=x*0.1, amp=12, period=35, phase=phase), name="antler")

    return [
        filled(ellipse(30, 25, (0, 30)), "#E53935", name="nose"),
        eye((-40, -20), 34, 38, iris="#3E2723"),
        eye((40, -20), 34, 38, iris="#3E2723"),
        filled(ellipse(180, 160), body, name="head"),
        antler(-60, 0), antler(60, 0.5),
    ]
