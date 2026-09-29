from feeling_parts import backdrop, closed_eye, filled_mouth, head, heart, pulse

COLOR = "#F06292"
HEART_COLOR = "#FF4D6D"


def loving():
    return [
        heart((-42, -58), HEART_COLOR, size=22, rotation=-10, name="heart-a"),
        heart((42, -58), HEART_COLOR, size=22, rotation=10, name="heart-b"),
        filled_mouth([(-20, 6), (0, 24), (20, 6), (0, 12)], pos=(0, 36)),
        closed_eye((-23, -6)), closed_eye((23, -6)),
        head(),
        backdrop(COLOR),
    ], lambda layer: pulse(layer, base=100, amp=10, period=50)
