import math

from critter_parts import eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def _petal_shape(base, tip, right_amt, left_amt, t=0.45, bulge=0.42):
    """A pointed leaf/petal: sharp corners at `base` and `tip`, with the two
    edges between them bowed outward - reads as a real curved shape rather
    than a flat-sided polygon."""
    bx, by = base
    tx, ty = tip
    mx, my = bx + (tx - bx) * t, by + (ty - by) * t
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy)
    px, py = -dy / length, dx / length
    pts = [base, (mx + px * right_amt, my + py * right_amt),
           tip, (mx - px * left_amt, my - py * left_amt)]
    tangents = []
    for i in range(4):
        if i in (0, 2):
            tangents.append(((0, 0), (0, 0)))
        else:
            ppx, ppy = pts[(i - 1) % 4]
            npx, npy = pts[(i + 1) % 4]
            tx2, ty2 = (npx - ppx) * bulge, (npy - ppy) * bulge
            tangents.append(((-tx2, -ty2), (tx2, ty2)))
    return path(pts, closed=True, tangents=tangents)


def flamingo():
    pink, pink_light, pink_dark = "#FF80AB", "#FFC1D9", "#E85C93"
    beak_base, beak_tip, leg_c, leg_dark = "#FFB8CE", "#212121", "#F2A6C4", "#C4718F"

    # The neck bows out in a single smooth "?"-shaped curve instead of a
    # straight rod - the one feature that makes a flamingo read as a flamingo.
    neck = outlined(
        path([(0, 55), (14, -42)], closed=False,
             tangents=[((0, 0), (46, -20)), ((30, 40), (0, 0))]),
        pink, 28, name="neck")

    # A bent, two-tone beak: pale pink at the base, dipping to a black tip.
    beak = group([
        filled(_petal_shape((26, 15), (48, 30), 6, 4), beak_tip, name="beak-tip"),
        filled(_petal_shape((0, 0), (30, 20), 10, 6), beak_base, name="beak-base"),
    ], transform(pos=(30, -58), rotation=6), name="beak")

    # Folded-wing flight feathers peeking past the body, a signature detail
    tail_feathers = group([
        filled(_petal_shape((0, 0), (16, 34), 8, 5), beak_tip, name="feather"),
        filled(_petal_shape((14, 4), (30, 30), 7, 4), beak_tip, name="feather"),
    ], transform(pos=(38, 90), rotation=18, opacity=90), name="tail-feathers")

    def leg(x, foot_y, phase, tucked=False):
        knee = (x * 0.3, foot_y * 0.55)
        foot = (x * (0.5 if not tucked else -0.2), foot_y)
        bend = 18 if not tucked else 30
        tans = [((0, 0), (0, bend)), ((0, -bend), (0, bend)), ((0, -bend), (0, 0))]
        shaft = outlined(path([(0, 0), knee, foot], closed=False, tangents=tans),
                         leg_c, 9, name="shaft")
        shaft_line = outlined(path([(0, 0), knee, foot], closed=False, tangents=tans),
                              leg_dark, 2, name="shaft-line")
        toes = group([
            outlined(path([(0, 0), (tx, 14)], closed=False), leg_dark, 5, name="toe")
            for tx in (-10, 0, 10)
        ], transform(pos=foot), name="toes")
        return group([toes, shaft_line, shaft],
                     wiggle((x, 130), amp=2 if tucked else 0, period=50, phase=phase),
                     name="leg")

    return [
        eye((0, -70), 26, 28, iris="#1B0E0A", blink_at=48),
        eye((28, -70), 26, 28, iris="#1B0E0A", blink_at=58),
        beak,
        neck,
        filled(ellipse(80, 72, (14, -70)), pink, name="head"),
        filled(ellipse(150, 68, (0, 70)), pink_dark, transform(opacity=45), name="wing-shade"),
        filled(ellipse(90, 56, (-14, 100)), pink_light, transform(opacity=60), name="belly"),
        tail_feathers,
        filled(ellipse(158, 108, (0, 80)), pink, name="body"),
        leg(-16, 100, 0.0, tucked=False),
        leg(18, 54, 0.3, tucked=True),
    ]
