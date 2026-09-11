from critter_parts import FRAMES, eye, smile, tuft, wiggle
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform


def dog():
    fur, fur_shade = "#E4A95F", "#C98A4B"
    ear_c, ear_rim, ear_in = "#B87A3D", "#96622F", "#D2934F"
    muzzle_c, nose_c, line_c = "#FCEFD8", "#3A2E28", "#6B4423"
    tongue_c, tongue_line, blush_c = "#F08A9A", "#D96C7E", "#F4A6A6"

    # Floppy ears sit *behind* the head, so they read as a clean silhouette
    # either side of the face instead of a slab painted over the cheeks.
    def flap(x_side, phase):
        return group([
            filled(ellipse(26, 60, (x_side * 8, 100)), ear_in, name="ear_inner"),
            filled(rect(60, 134, (0, 66), radius=30), ear_c, name="ear_outer"),
            filled(rect(70, 144, (0, 66), radius=35), ear_rim, name="ear_rim"),
        ], wiggle((x_side * 86, -40), base_rot=-x_side * 5, amp=5, period=24, phase=phase),
            name="ear")

    # The classic dog "W" mouth: two arcs meeting in a peak under the nose.
    mouth = [smile(32, 12, x=-15, y=46, color=line_c, w=5),
             smile(32, 12, x=15, y=46, color=line_c, w=5)]

    tongue = group([
        outlined(path([(0, 7), (0, 23)], closed=False), tongue_line, 3, name="crease"),
        filled(rect(38, 30, (0, 15), radius=15), tongue_c, name="tongue"),
    ], transform(pos=(0, 56),
                 scale=animated([(0, [100, 100]), (20, [100, 128]),
                                 (36, [100, 100]), (52, [100, 122]),
                                 (66, [100, 100]), (FRAMES, [100, 100])])),
        name="pant")

    nose = group([
        filled(ellipse(13, 7, (-9, -7)), "#FFFFFF", transform(opacity=55), name="nose_shine"),
        filled(ellipse(44, 32), nose_c, name="nose_bulb"),
    ], transform(pos=(0, 28)), name="nose")

    # Whisker freckles, tucked between the nose and the edge of the muzzle
    freckles = [filled(ellipse(8, 8, (x, y)), fur_shade, transform(opacity=65), name="freckle")
                for x, y in [(-34, 22), (-46, 30), (-34, 38),
                             (34, 22), (46, 30), (34, 38)]]

    blush = [filled(ellipse(28, 18, (-75, 26)), blush_c, transform(opacity=60), name="blush"),
             filled(ellipse(28, 18, (75, 26)), blush_c, transform(opacity=60), name="blush")]

    return [
        eye((-45, -30), 36, 40, iris="#3A2A20", blink_at=48),
        eye((45, -30), 36, 40, iris="#3A2A20", blink_at=56),
        # A patch around one eye, behind it, for that scruffy-puppy look
        filled(ellipse(86, 76, (-45, -30)), ear_c, name="eye_patch"),
    ] + blush + freckles + mouth + [
        tongue,
        nose,
        filled(ellipse(126, 72, (0, 46)), muzzle_c, name="muzzle"),
        filled(ellipse(204, 180, (0, -6)), fur, name="head"),
        filled(ellipse(214, 190, (0, -3)), fur_shade, transform(opacity=55), name="head_rim"),
        tuft(0, -86, 3, fur, w=24, h=38, spread=20),
        flap(-1, 0.0), flap(1, 0.5),
    ]
