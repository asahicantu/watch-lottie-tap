from feeling_parts import backdrop, bounce, head, mouth, spark, std_eyes

COLOR = "#6FCF97"


def hopeful():
    return [
        spark((0, -72), color="#FFE066", size=9),
        mouth([(-18, 20), (0, 28), (18, 20)], pos=(0, 34), width=5),
        *std_eyes(),
        head(),
        backdrop(COLOR),
    ], lambda layer: bounce(layer, amp=8, period=60)
