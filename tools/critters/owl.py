from critter_parts import eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, transform


def owl():
    body, disc = "#8b5e3c", "#f0dcc2"

    def disc_eye(x):
        return group([eye((0, 0), 40, 44, iris="#2b2118"),
                      filled(ellipse(96, 96), disc, name="disc")],
                     transform(pos=(x, -22)), name="eye-disc")

    return [
        # Between and just below the eye discs, which meet at x=0 - not down on
        # the belly, where it was.
        filled(triangle(38, 42), "#f0902a",
               transform(pos=(0, -24), rotation=180), name="beak"),
        disc_eye(-48), disc_eye(48),
        filled(ellipse(120, 96, (0, 56)), "#c9a273", name="belly"),
        filled(ellipse(200, 196), body, name="body"),
        filled(ellipse(60, 116, (0, 46)), "#6f4728",
               wiggle((-78, 10), base_rot=12, amp=10, period=28), name="wing"),
        filled(ellipse(60, 116, (0, 46)), "#6f4728",
               wiggle((78, 10), base_rot=-12, amp=10, period=28, phase=0.5), name="wing"),
        filled(triangle(46, 46, tilt=-8), body,
               wiggle((-58, -84), base_rot=-10, amp=5, period=34), name="tuft"),
        filled(triangle(46, 46, tilt=8), body,
               wiggle((58, -84), base_rot=10, amp=5, period=34, phase=0.5), name="tuft"),
    ]
