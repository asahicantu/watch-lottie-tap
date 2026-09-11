from critter_parts import FRAMES, dot_eye, wiggle
from lottie_kit import (
    animated, ellipse, filled, group, outlined, path, transform,
)


def butterfly():
    edge, field, core = "#AD1457", "#F06292", "#F8BBD0"
    body_c, seg_c = "#4A2C3A", "#7B4A5C"

    # Forewing above, hindwing below. Each is drawn three times - full size in
    # the border colour, then smaller copies inset toward the body - which
    # leaves an even band of colour round the outer edge.
    fore = [(0, -18), (42, -122), (100, -130), (128, -72), (112, -14), (36, 6)]
    hind = [(0, -6), (84, 8), (110, 54), (78, 110), (28, 102), (8, 46)]

    def wing_path(verts, k=0.28):
        """Rounds the corners off a wing outline, so it reads as a wing rather
        than a hexagon: each tangent follows the line between its neighbours."""
        tans = []
        for i, _ in enumerate(verts):
            px, py = verts[i - 1]
            nx, ny = verts[(i + 1) % len(verts)]
            ox, oy = (nx - px) * k, (ny - py) * k
            tans.append(((-ox, -oy), (ox, oy)))
        return path(verts, closed=True, tangents=tans)

    def ocellus(x, y, r):
        return group([filled(ellipse(r * 0.40, r * 0.40), "#FFF3F7", name="pupil"),
                      filled(ellipse(r, r), body_c, name="ring")],
                     transform(pos=(x, y)), name="ocellus")

    def panel(verts, spots, name):
        return group(
            spots + [group([filled(wing_path(verts), core, name="core")],
                           transform(scale=(62, 62)), name="core-inset"),
                     group([filled(wing_path(verts), field, name="field")],
                           transform(scale=(86, 86)), name="field-inset"),
                     filled(wing_path(verts), edge, name="edge")],
            name=name)

    def flap(mirror):
        # a head-on flap is a horizontal squeeze; four beats across the loop
        keys = []
        for i in range(4):
            keys.append((i * 22, [100 * mirror, 100]))
            keys.append((i * 22 + 11, [68 * mirror, 100]))
        keys.append((FRAMES, [100 * mirror, 100]))
        return animated(keys)

    def wing(mirror):
        return group([panel(fore, [ocellus(84, -80, 18), ocellus(60, -36, 10)],
                            "forewing"),
                      panel(hind, [ocellus(62, 56, 14)], "hindwing")],
                     transform(pos=(0, -12), scale=flap(mirror)), name="wing")

    def antenna(mirror):
        return group([filled(ellipse(16, 16, (34 * mirror, -46)), body_c,
                             name="club"),
                      outlined(path([(0, 0), (10 * mirror, -26),
                                     (34 * mirror, -46)], closed=False),
                               body_c, 5, name="stalk")],
                     wiggle((14 * mirror, -98), amp=4, period=26,
                            phase=0.25 * mirror), name="antenna")

    return [
        antenna(-1), antenna(1),
        dot_eye((-26, -74), 9), dot_eye((26, -74), 9),
        filled(ellipse(102, 82, (0, -72)), body_c, name="head"),
        outlined(path([(-14, 24), (14, 24)], closed=False), seg_c, 4, name="seam"),
        outlined(path([(-12, 44), (12, 44)], closed=False), seg_c, 4, name="seam"),
        outlined(path([(-9, 64), (9, 64)], closed=False), seg_c, 4, name="seam"),
        filled(ellipse(36, 94, (0, 42)), body_c, name="abdomen"),
        filled(ellipse(56, 66, (0, -16)), body_c, name="thorax"),
        wing(-1), wing(1),
    ]
