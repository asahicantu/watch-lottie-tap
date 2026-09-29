from feeling_parts import GOLD, backdrop, bounce, brows, eyes, head, smile, twinkle

COLOR = "#6FCF97"


def hopeful():
    return [
        twinkle((56, -86), GOLD, size=12, period=45),
        twinkle((78, -58), GOLD, size=7, period=45, delay=20),
        smile(w=24, depth=7, pos=(0, 48), width=4.5),
        *brows(y=-36, tilt=12, arch=4),
        # looking up at something, eyes shining
        *eyes(w=30, h=28, look=(3, -5), shine=True, glossy=True),
        head(),
        backdrop(COLOR),
    ], lambda layer: bounce(layer, amp=8, period=90)
