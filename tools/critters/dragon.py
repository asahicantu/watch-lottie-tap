from critter_parts import FRAMES, eye, nostrils, smile, triangle, wiggle
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform


def _smooth_tangents(points, closed=True, k=0.22):
    """Catmull-Rom-style handles so a hand-placed polygon reads as a curved
    horn/spike instead of a flat-sided triangle."""
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


def dragon():
    body, dark, belly = "#4CAF50", "#2E7D32", "#C8E6C9"
    horn_c, mouth_c, smoke_c = "#FFECB3", "#7A1F1F", "#ECEFF1"

    def _curved(points, color, tr=None, name="shape", k=0.24):
        return filled(path(points, closed=True, tangents=_smooth_tangents(points, k=k)),
                      color, tr, name=name)

    # Curved horns sweeping back from the sides of the head
    def horn(x_side):
        pts = [(-9 * x_side, 4), (-11 * x_side, -26), (-1 * x_side, -54),
               (8 * x_side, -46), (10 * x_side, -18), (6 * x_side, 6)]
        return _curved(pts, horn_c, transform(pos=(x_side * 72, -66), rotation=x_side * 12), "horn")

    # A smooth bony ridge of spikes down the crown, tucked behind the head so
    # only the curved tips show proud of the silhouette
    def spike(x, y, scale=1.0):
        pts = [(-10, 6), (-8, -14), (0, -30), (8, -14), (10, 6)]
        return _curved(pts, dark, transform(pos=(x, y), scale=(100 * scale, 100 * scale)), "spike")

    brows = [
        outlined(path([(-22, 6), (0, -10), (22, 6)], closed=False), dark, 7,
                 transform(pos=(-46, -58)), name="brow"),
        outlined(path([(-22, 6), (0, -10), (22, 6)], closed=False), dark, 7,
                 transform(pos=(46, -58)), name="brow"),
    ]

    # Small triangular jaw scutes flanking the snout for reptilian texture
    jaw_scutes = [
        filled(triangle(12, 14), dark, transform(pos=(x, 54), rotation=180), name="jaw_scute")
        for x in (-56, -40, 40, 56)
    ]

    # Gentle rising smoke puffs above each nostril
    def smoke(x_side, phase):
        keys = [(0, [0, 0]), (18, [90, 130]), (36, [40, 60]), (FRAMES, [0, 0])]
        return group(
            [filled(ellipse(16, 16), smoke_c, name="puff")],
            transform(pos=(x_side * 14, 4), scale=animated(keys)),
            name="smoke")

    fangs = [
        filled(triangle(9, 14), "#FFFFFF", transform(pos=(-14, 6), rotation=180), name="fang"),
        filled(triangle(9, 14), "#FFFFFF", transform(pos=(14, 6), rotation=180), name="fang"),
    ]
    mouth = group([smile(48, 14, y=0, color="#1B4A1E", w=5)] + fangs,
                  transform(pos=(0, 46)), name="mouth")

    snout = group([
        filled(rect(64, 40, (0, 44), radius=20), body, name="snout_tip"),
        filled(rect(96, 58, (0, 12), radius=30), body, name="snout_base"),
    ], name="snout")

    lip_crease = outlined(path([(-40, 6), (0, -6), (40, 6)], closed=False,
                               tangents=_smooth_tangents([(-40, 6), (0, -6), (40, 6)],
                                                          closed=False, k=0.4)),
                          dark, 5, transform(pos=(0, -2)), name="lip_crease")

    chin_patch = filled(ellipse(58, 34, (0, 60)), belly, name="chin_patch")

    return [
        eye((-46, -22), 42, 46, iris="#E65100"),
        eye((46, -22), 42, 46, iris="#E65100"),
    ] + brows + [
        mouth,
        nostrils(14, 24, 12, 9, dark),
        smoke(-1, 0.0), smoke(1, 0.4),
        lip_crease,
        chin_patch,
        snout,
    ] + jaw_scutes + [
        horn(-1), horn(1),
        spike(-42, -84, 0.85), spike(0, -96, 1.0), spike(42, -84, 0.85),
        filled(ellipse(206, 186, (0, -6)), body, name="head"),
    ]
