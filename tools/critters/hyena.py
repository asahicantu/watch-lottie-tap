from critter_parts import eye, smile, wiggle
from lottie_kit import ellipse, filled


def hyena():
    body, spot = "#A1887F", "#5D4037"
    return [
        smile(50, 20, y=40, color="#3E2723"),
        filled(ellipse(40, 30, (0, 20)), "#212121", name="nose"),
        eye((-40, -15), 34, 38, iris="#FFD54F"),
        eye((40, -15), 34, 38, iris="#FFD54F"),
        filled(ellipse(180, 160), body, name="head"),
        filled(ellipse(40, 40, (-50, 40)), spot, name="spot"),
        filled(ellipse(30, 30, (60, -40)), spot, name="spot"),
        filled(ellipse(80, 100), body, wiggle((-70, -70), base_rot=-30, amp=10, period=25), name="ear"),
        filled(ellipse(80, 100), body, wiggle((70, -70), base_rot=30, amp=10, period=25, phase=0.5), name="ear"),
    ]
