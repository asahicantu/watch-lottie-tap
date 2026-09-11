from critter_parts import eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def _smooth_tangents(points, closed=True, k=0.22):
    """Catmull-Rom-style tangent handles so a hand-placed polygon reads as a
    smooth, rounded curve instead of straight segments meeting at corners."""
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


def dolphin():
    body_c, cape_c, belly_c = "#4FC3F7", "#0288D1", "#E1F5FE"
    line_c, shine_c = "#01579B", "#FFFFFF"

    # A smoothly-curved fin with its own rounded outline stroke drawn on top,
    # so it always reads as a distinct piece instead of a flat-colored blob.
    def _fin(points, tr, name, k=0.22):
        tans = _smooth_tangents(points, closed=True, k=k)
        return group([
            outlined(path(points, closed=True, tangents=tans), line_c, 3, name=f"{name}_edge"),
            filled(path(points, closed=True, tangents=tans), body_c, name=name),
        ], tr, name=f"{name}_group")

    dorsal = _fin(
        [(-14, 22), (-16, -14), (0, -46), (18, -22), (12, 14)],
        transform(pos=(6, -76)), "dorsal")

    def flipper(x_side, phase):
        pts = [(0, -10), (22, 0), (28, 20), (10, 32), (-8, 16)]
        pts = [(x_side * px, py) for px, py in pts]
        return _fin(pts, wiggle((x_side * 92, 26), base_rot=x_side * 8, amp=10,
                                period=32, phase=phase), "flipper")

    fluke_pts = [(-48, -6), (-16, 26), (0, 10), (16, 26), (48, -6),
                 (22, -22), (0, -10), (-22, -22)]
    fluke_tans = _smooth_tangents(fluke_pts, closed=True, k=0.16)
    fluke = group([
        outlined(path(fluke_pts, closed=True, tangents=fluke_tans), line_c, 3, name="fluke_edge"),
        filled(path(fluke_pts, closed=True, tangents=fluke_tans), body_c, name="fluke"),
        outlined(path([(0, -8), (0, 14)], closed=False), line_c, 3, name="fluke_notch"),
    ], transform(pos=(0, 118)), name="fluke_group")
    peduncle = filled(rect(34, 46, (0, 96), radius=17), body_c, name="peduncle")

    # A crease separating the rounded melon/face from the tapered rostrum -
    # smoothed into a single gentle curve rather than a sharp V.
    crease_pts = [(-34, 8), (0, -6), (34, 8)]
    crease = outlined(path(crease_pts, closed=False,
                          tangents=_smooth_tangents(crease_pts, closed=False, k=0.4)),
                      line_c, 5, transform(pos=(0, 30)), name="crease")

    rostrum = group([
        filled(rect(48, 34, (0, 90), radius=17), body_c, name="rostrum_tip"),
        filled(rect(76, 56, (0, 62), radius=28), body_c, name="rostrum_base"),
    ], name="rostrum")

    blowhole_pts = [(-9, 2), (0, -3), (9, 2)]
    blowhole = outlined(path(blowhole_pts, closed=False,
                            tangents=_smooth_tangents(blowhole_pts, closed=False, k=0.4)),
                        line_c, 4, transform(pos=(0, -58)), name="blowhole")

    melon_shine = filled(ellipse(46, 28, (-34, -44)), shine_c, transform(opacity=30), name="melon_shine")
    cape = filled(ellipse(174, 56, (0, -34)), cape_c, transform(opacity=80), name="cape")
    belly = filled(ellipse(118, 48, (0, 70)), belly_c, name="belly")

    return [
        eye((-42, -16), 28, 30, iris="#01313f", blink_at=48),
        eye((42, -16), 28, 30, iris="#01313f", blink_at=58),
        smile(34, 9, y=92, color=line_c, w=4),
        crease,
        rostrum,
        blowhole,
        melon_shine,
        belly,
        cape,
        filled(ellipse(196, 156, (0, 10)), body_c, name="body"),
        flipper(-1, 0.0), flipper(1, 0.5),
        peduncle,
        fluke,
        dorsal,
    ]
