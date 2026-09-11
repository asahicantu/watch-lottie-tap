from critter_parts import eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def goldfish():
    body, shadow, gold = "#FF9800", "#EF6C00", "#FFB300"
    line, cheek = "#9A3E00", "#FFCC80"

    def fin(pos, rot, phase, size=(62, 42), name="fin"):
        return filled(ellipse(*size), gold,
                      wiggle(pos, base_rot=rot, amp=16, period=24, phase=phase),
                      name=name)

    tail = group([
        filled(path([(-8, 0), (-62, 70), (-18, 92), (16, 45)], True), gold,
               name="tail-left"),
        filled(path([(8, 0), (62, 70), (18, 92), (-16, 45)], True), gold,
               name="tail-right"),
        filled(ellipse(28, 35, (0, 36)), shadow, name="tail-base"),
    ], wiggle((0, 82), amp=13, period=22, phase=0.15), name="flowing-tail")

    return [
        # Face markings are placed first so they sit on top of the body.
        filled(ellipse(28, 16, (0, 33)), cheek, name="muzzle"),
        outlined(path([(-13, 31), (0, 40), (13, 31)], closed=False,
                      tangents=[((0, 0), (7, 8)), ((-7, 0), (7, 0)),
                                ((-7, 8), (0, 0))]), line, 5, name="smile"),
        outlined(path([(-69, 7), (-59, 22), (-52, 31)], closed=False,
                      tangents=[((0, 0), (7, 7)), ((-7, 0), (4, 4)),
                                ((-4, 4), (0, 0))]), line, 4, name="left-gill"),
        outlined(path([(69, 7), (59, 22), (52, 31)], closed=False,
                      tangents=[((0, 0), (-7, 7)), ((7, 0), (-4, 4)),
                                ((4, 4), (0, 0))]), line, 4, name="right-gill"),
        eye((-47, -20), 42, 48, iris="#263238", pupil_offset=(2, 3)),
        eye((47, -20), 42, 48, iris="#263238", pupil_offset=(-2, 3)),
        filled(ellipse(25, 14, (-32, 22)), cheek, name="left-cheek"),
        filled(ellipse(25, 14, (32, 22)), cheek, name="right-cheek"),
        filled(ellipse(24, 16, (-28, 55)), shadow, name="scale-left"),
        filled(ellipse(24, 16, (0, 61)), shadow, name="scale-middle"),
        filled(ellipse(24, 16, (28, 55)), shadow, name="scale-right"),
        fin((-77, 36), 32, 0.0, name="left-pectoral-fin"),
        fin((77, 36), -32, 0.5, name="right-pectoral-fin"),
        fin((0, -79), 0, 0.25, size=(55, 30), name="dorsal-fin"),
        filled(ellipse(174, 156), body, name="body"),
        filled(ellipse(125, 72, (0, 36)), "#FFA726", name="belly-glow"),
        tail,
    ]
