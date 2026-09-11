from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def caterpillar():
    skin, shadow, glow, line = "#8BC34A", "#689F38", "#C5E1A5", "#33691E"

    def segment(x, size, phase, name):
        return group([
            filled(ellipse(size * 0.34, size * 0.20, (-size * 0.16, -size * 0.20)),
                   glow, name="highlight"),
            filled(ellipse(size * 0.20, size * 0.20, (size * 0.20, -size * 0.04)),
                   shadow, name="spot"),
            filled(ellipse(size, size), skin, name="segment"),
            filled(ellipse(size + 8, size + 8, (0, 6)), shadow, name="shadow"),
        ], wiggle((x, 0), base_rot=(x / 90) * 4, amp=4, period=26,
                   phase=phase), name=name)

    def foot(x, phase):
        return group([
            filled(ellipse(28, 16, (0, 15)), line, name="foot"),
            filled(ellipse(22, 30), shadow, name="leg"),
        ], wiggle((x, 42), amp=3, period=22, phase=phase), name="foot")

    def antenna(side, phase):
        return group([
            filled(ellipse(14, 14, (side * 18, -34)), "#F1F8E9", name="tip"),
            outlined(path([(0, 0), (side * 8, -19), (side * 18, -34)], closed=False),
                     line, 4, name="stalk"),
        ], wiggle((-90 + side * 17, -51), amp=6, period=24, phase=phase),
           name="antenna")

    head = group([
        filled(ellipse(32, 17, (-12, -20)), glow, name="head-highlight"),
        filled(ellipse(84, 84), skin, name="head"),
        filled(ellipse(92, 92, (0, 6)), shadow, name="head-shadow"),
    ], wiggle((-90, 0), amp=2, period=30), name="head")

    return [
        # The head and face stay above the softly wobbling body segments.
        smile(32, 10, x=-90, y=20, color=line, w=4),
        dot_eye((-106, -12), 10), dot_eye((-75, -12), 10),
        filled(ellipse(20, 12, (-111, 10)), "#AED581", name="left-cheek"),
        filled(ellipse(20, 12, (-70, 10)), "#AED581", name="right-cheek"),
        head,
        segment(-43, 70, 0.00, "segment-one"),
        segment(4, 72, 0.25, "segment-two"),
        segment(51, 70, 0.50, "segment-three"),
        segment(94, 65, 0.75, "segment-four"),
        foot(-43, 0.00), foot(1, 0.25), foot(45, 0.50), foot(87, 0.75),
        antenna(-1, 0.0), antenna(1, 0.5),
    ]
