from critter_parts import eye, pin_eye, smile, triangle, tuft, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def spider():
    # The app draws on pure black, so a black spider vanished. It is now a
    # deep purple, and every piece of it - body, head and each leg - carries a
    # pale lavender contour so the whole silhouette reads against the dark.
    body_c, shade_c, light_c = "#4B3B6B", "#35284F", "#7A64A8"
    rim_c = "#C7B3FF"
    spot_c = "#A48BE0"
    ink = "#140F1F"

    # ---- legs: four per side, knee high, foot planted ----------------------
    # (hip, knee, foot) for the right side, relative to the body; the left
    # side is the mirror image. Each leg is drawn twice - a wide pale stroke
    # underneath and the purple on top - which gives it its contour.
    right_legs = [
        ((46, -6), (40, -52), (82, -22)),
        ((54, 12), (54, -34), (96, 14)),
        ((54, 30), (56, -12), (92, 48)),
        ((44, 46), (42, 8), (70, 78)),
    ]
    legs = []
    for i, (hip, knee, foot) in enumerate(right_legs):
        for side in (1, -1):
            hx, hy = hip[0] * side, hip[1]
            pts = [(0, 0), (knee[0] * side, knee[1]), (foot[0] * side, foot[1])]
            fx, fy = pts[2]
            legs.append(group([
                filled(ellipse(9, 9, (fx, fy)), shade_c, name="foot"),
                outlined(path(pts, closed=False), body_c, 8, name="leg_fill"),
                filled(ellipse(17, 17, (fx, fy)), rim_c, name="foot_rim"),
                outlined(path(pts, closed=False), rim_c, 15, name="leg_rim"),
            ], wiggle((hx, hy), amp=5, period=24, phase=i * 0.22 + (0.5 if side < 0 else 0)),
                name="leg"))

    # ---- face ---------------------------------------------------------------
    small_eyes = group([
        pin_eye((x, y), 12, color=ink, blink_at=60)
        for x, y in [(-40, -10), (-15, -18), (15, -18), (40, -10)]
    ], name="small-eyes")

    fangs = group([
        filled(triangle(11, 14, pos=(x, 0)), "#FFF4E0",
               transform(pos=(0, 76), rotation=180), name="fang")
        for x in (-9, 9)
    ], name="fangs")

    cheeks = [
        filled(ellipse(20, 11, (x, 54)), "#FF8FB8", transform(opacity=45), name="cheek")
        for x in (-44, 44)
    ]

    # ---- abdomen markings ---------------------------------------------------
    spots = [
        filled(ellipse(w, h, (x, y)), spot_c, name="spot")
        for x, y, w, h in [(0, -92, 30, 20), (-42, -72, 20, 14), (42, -72, 20, 14),
                           (-22, -104, 12, 9), (22, -104, 12, 9)]
    ]

    return [
        eye((-24, 20), 30, 34, blink_at=48),
        eye((24, 20), 30, 34, blink_at=48),
        small_eyes,
        smile(width=34, drop=12, y=60, color=ink, w=5),
        fangs,
    ] + cheeks + [
        filled(ellipse(56, 26, (-24, -2)), light_c, transform(rotation=-14, opacity=55),
               name="head_shine"),
        filled(ellipse(140, 116, (0, 34)), body_c, name="head"),
        filled(ellipse(152, 128, (0, 36)), shade_c, name="head_shade"),
        filled(ellipse(160, 136, (0, 36)), rim_c, name="head_rim"),
        filled(ellipse(44, 20, (-44, -92)), "#FFFFFF",
               transform(rotation=-28, opacity=22), name="abdomen_shine"),
    ] + spots + [
        filled(ellipse(170, 142, (0, -48)), body_c, name="abdomen"),
        filled(ellipse(182, 154, (0, -46)), shade_c, name="abdomen_shade"),
        filled(ellipse(190, 162, (0, -46)), rim_c, name="abdomen_rim"),
        tuft(0, -122, 3, rim_c, w=12, h=22, spread=14),
    ] + legs
