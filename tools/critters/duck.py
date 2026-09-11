import math

from critter_parts import FRAMES, eye, wiggle
from lottie_kit import animated, ellipse, filled, group, outlined, path, transform


def _smooth_tangents(points, closed=True, k=0.24):
    """Catmull-Rom-style handles so a hand-placed polygon reads as a curved
    feather instead of a jagged zig-zag."""
    n = len(points)
    tangents = []
    for i in range(n):
        if closed:
            px, py = points[(i - 1) % n]
            nx, ny = points[(i + 1) % n]
        else:
            px, py = points[i - 1] if i > 0 else points[i]
            nx, ny = points[i + 1] if i < n - 1 else points[i]
        tx, ty = (nx - px) * k, (ny - py) * k
        tangents.append(((-tx, -ty), (tx, ty)))
    return tangents


def _petal(base, tip, right_amt, left_amt, t=0.45, bulge=0.42):
    """A pointed leaf/petal: sharp corners at `base` and `tip`, with the two
    edges between them bowed outward - a real feather silhouette, not a
    rounded blob."""
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
    return pts, tangents


def duck():
    head_c, head_shade, cheek_c = "#FFD93B", "#F2B705", "#FFF3B0"
    bill_c, bill_dark, bill_line = "#F6A02C", "#D9741C", "#8C4A0F"
    tuft_c, tuft_shade = "#FFE882", "#F2C230"

    def feather(base, tip, right_amt, left_amt, color, **kw):
        pts, tans = _petal(base, tip, right_amt, left_amt, **kw)
        return filled(path(pts, closed=True, tangents=tans), color, name="feather")

    # A curled quiff of two pointed feathers, shaded dark-behind-light for
    # volume, swaying together as one piece so it reads as a real curl
    # instead of a rounded, artificial-looking blob.
    peak = group([
        feather((4, 6), (-9, -50), 15, 7, tuft_shade),
        feather((-3, 6), (5, -60), 9, 16, tuft_c),
    ], wiggle((-2, -78), amp=6, period=28), name="peak")

    brows = [
        outlined(path([(-14, 4), (0, -6), (14, 4)], closed=False), bill_line, 4,
                 transform(pos=(-46, -42), opacity=55), name="brow"),
        outlined(path([(-14, 4), (0, -6), (14, 4)], closed=False), bill_line, 4,
                 transform(pos=(46, -42), opacity=55), name="brow"),
    ]

    cheeks = [
        filled(ellipse(38, 28, (-64, 14)), cheek_c, transform(opacity=70), name="cheek"),
        filled(ellipse(38, 28, (64, 14)), cheek_c, transform(opacity=70), name="cheek"),
    ]

    # Short curved feather strokes for texture, tucked along the crown
    feather_lines = [
        outlined(path([(-10, -4), (0, 0), (10, -4)], closed=False), head_shade, 3,
                 transform(pos=(x, y), opacity=45), name="feather_line")
        for x, y in [(-46, -56), (-26, -66), (0, -70), (26, -66), (46, -56)]
    ]

    nostrils = group([
        filled(ellipse(7, 5, (-16, -6)), bill_line, name="nostril"),
        filled(ellipse(7, 5, (16, -6)), bill_line, name="nostril"),
    ], transform(pos=(0, 30)), name="nostrils")

    bill_shine = filled(ellipse(30, 12, (-14, -12)), "#FFFFFF",
                        transform(pos=(0, 30), opacity=40), name="bill_shine")

    bill_seam = outlined(path([(-40, 0), (0, 8), (40, 0)], closed=False), bill_dark, 3,
                         transform(pos=(0, 45), opacity=60), name="bill_seam")

    chin_shadow = filled(ellipse(90, 18, (0, 62)), "#000000",
                         transform(opacity=12), name="chin_shadow")

    return [
        eye((-46, -20), 34, 38, iris="#3a2a20", blink_at=48),
        eye((46, -20), 34, 38, iris="#3a2a20", blink_at=48),
    ] + brows + [
        # the lower bill hinges open and shut, so the duck reads as quacking
        filled(ellipse(98, 40, (0, 14)), bill_dark,
               transform(pos=(0, 30), rotation=animated(
                   [(0, 0), (10, 13), (20, 0), (30, 13), (40, 0), (FRAMES, 0)])),
               name="lower-bill"),
        bill_seam,
        nostrils,
        bill_shine,
        filled(ellipse(116, 48, (0, -6)), bill_c, transform(pos=(0, 30)), name="upper-bill"),
    ] + cheeks + feather_lines + [
        chin_shadow,
        peak,
        filled(ellipse(156, 84, (0, -30)), head_shade, transform(opacity=50), name="head_shade"),
        filled(ellipse(180, 168, (0, 4)), head_c, name="head"),
    ]
