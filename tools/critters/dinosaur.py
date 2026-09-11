from critter_parts import eye, nostrils, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def dinosaur():
    skin_c, dark_c = "#4CAF50", "#1B5E20"
    belly_c, plate_c = "#DCEDC8", "#2E7D32"

    # Tiny T-rex arms with three clawed fingers
    def arm(x_side, phase):
        claws = group([filled(triangle(7, 10), dark_c, transform(pos=(cx, 18)), name="claw")
                        for cx in (-7, 0, 7)], name="claws")
        upper = filled(rect(18, 36, (0, 0), radius=9), skin_c, name="upper-arm")
        return group([claws, upper], wiggle((x_side * 76, 45), base_rot=x_side * 10,
                                            amp=8, period=30, phase=phase), name="arm")

    # Thick legs with three-toed clawed feet
    def foot(x_side, phase):
        toes = group([filled(triangle(11, 15), dark_c, transform(pos=(tx, 12)), name="claw")
                       for tx in (-13, 0, 13)], name="toes")
        leg = filled(ellipse(38, 62, (0, -8)), skin_c, name="leg")
        return group([toes, leg], wiggle((x_side * 46, 150), amp=4, period=26, phase=phase),
                     name="foot")

    # A row of triangular back plates, largest over the shoulders, tapering
    # down the spine toward the tail for a classic dino silhouette.
    def plate(y, scale=1.0):
        return filled(triangle(20 * scale, 28 * scale), plate_c, transform(pos=(0, y)), name="plate")

    plates = [plate(-138, 0.9), plate(-118, 1.05), plate(-96, 1.0),
              plate(-10, 0.9), plate(30, 0.8), plate(66, 0.65)]

    # A single thick, round-tipped tail trailing out to the side and drooping
    # gently down - one coherent shape swaying as a whole, not a stack of
    # independently-wiggling segments (which read as curly and vertical).
    tail_side = 1
    tail_segs = [
        filled(ellipse(74, 58, (tail_side * 18, 6)), skin_c, name="tail_base"),
        filled(ellipse(58, 46, (tail_side * 60, 16)), skin_c, name="tail_mid"),
        filled(ellipse(40, 34, (tail_side * 96, 24)), skin_c, name="tail_taper"),
        filled(ellipse(26, 26, (tail_side * 122, 30)), skin_c, name="tail_tip"),
    ]
    tail_parts = [group(tail_segs, wiggle((tail_side * 66, 96), base_rot=tail_side * 12,
                                          amp=7, period=34), name="tail")]

    brows = [
        outlined(path([(-22, 4), (0, -10), (22, 4)], closed=False), dark_c, 7,
                 transform(pos=(-44, -100)), name="brow"),
        outlined(path([(-22, 4), (0, -10), (22, 4)], closed=False), dark_c, 7,
                 transform(pos=(44, -100)), name="brow"),
    ]

    # A toothy grin: a smile line with a couple of little fangs poking up
    fangs = [
        filled(triangle(9, 13), "#ffffff", transform(pos=(-16, -10), rotation=180), name="fang"),
        filled(triangle(9, 13), "#ffffff", transform(pos=(16, -10), rotation=180), name="fang"),
    ]
    mouth = group([smile(46, 13, y=8, color=dark_c, w=5)] + fangs,
                  transform(pos=(0, -12)), name="mouth")

    chin_patch = filled(ellipse(78, 52, (0, 8)), belly_c, name="chin_patch")
    chest = filled(ellipse(96, 108, (0, 82)), belly_c, name="chest")

    return (
        [eye((-44, -84), 32, 34, iris="#1B0E0A", white="#ffffff", blink_at=48),
         eye((44, -84), 32, 34, iris="#1B0E0A", white="#ffffff", blink_at=58)]
        + brows
        + [mouth,
           nostrils(16, -58, 14, 10, dark_c),
           plates[0], plates[1], plates[2],
           arm(-1, 0.0), arm(1, 0.5),
           chin_patch,
           filled(ellipse(196, 158, (0, -68)), skin_c, name="head"),
           plates[3], plates[4], plates[5],
           chest,
           filled(ellipse(176, 172, (0, 62)), skin_c, name="body"),
           filled(ellipse(190, 184, (0, 70)), dark_c, transform(opacity=45), name="body-shadow"),
           foot(-1, 0.0), foot(1, 0.5)]
        + tail_parts
    )
