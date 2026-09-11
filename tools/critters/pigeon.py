from critter_parts import FRAMES, eye, triangle, wiggle
from lottie_kit import animated, ellipse, filled, group, path, rect, transform


def pigeon():
    """A rock dove. The old one was a grey disc with a dark triangle for a
    beak and a purple lozenge under the chin that read as a scarf rather than
    as the neck it was meant to be.

    The three things that make a pigeon: the iridescent collar (green over
    mauve, which is where that purple belongs), the white cere sitting on top
    of a stubby beak, and the head-jab it does instead of walking smoothly.
    """
    head_c, body_c = "#9AA7B0", "#8896A1"
    wing_c, bar_c = "#7A8894", "#5B6873"
    breast_c, sheen_g, sheen_p = "#9C8189", "#4E9E80", "#7E57C2"
    beak_c, cere_c = "#A2948B", "#EFEAE4"

    def wing(s, phase):
        """A folded wing with the two dark bars a rock dove carries, lifted
        just enough to look loose rather than pinned on."""
        bars = [filled(rect(46, 10, (0, y), radius=5), bar_c, name="bar")
                for y in (2, 24)]
        blade = path([(0, -62), (26 * s, -20), (10 * s, 64), (-22 * s, 6)],
                     True,
                     tangents=[((-14 * s, -6), (14 * s, 6)),
                               ((0, -22), (-4 * s, 26)),
                               ((10 * s, 22), (-10 * s, -22)),
                               ((-2 * s, 26), (2 * s, -26))])
        return group(bars + [filled(blade, wing_c, name="blade")],
                     wiggle((76 * s, 82), base_rot=s * -10, amp=5, period=32,
                            phase=phase), name="wing")

    # the collar: green over mauve, both fading out at the edges, so the neck
    # shifts colour the way the real bird's does
    collar = [filled(ellipse(156, 44, (0, 30)), sheen_p,
                     transform(opacity=45), name="sheen-mauve"),
              filled(ellipse(142, 42, (0, 16)), sheen_g,
                     transform(opacity=50), name="sheen-green")]

    # everything that belongs to the head rides in one group, so the jab
    # carries the beak and the eyes with it
    jab = animated([(0, [0, 0]), (8, [0, 9]), (14, [0, -5]), (20, [0, 0]),
                    (44, [0, 0]), (52, [0, 9]), (58, [0, -5]), (64, [0, 0]),
                    (FRAMES, [0, 0])])
    head = group([
        # the cere - the white nub at the base of the bill - sits over the
        # beak, and is most of what tells a pigeon from any other grey bird
        filled(ellipse(38, 18, (0, -18)), cere_c, name="cere"),
        filled(triangle(26, 38), beak_c,
               transform(pos=(0, 10), rotation=180), name="beak"),
        eye((-42, -34), 28, 30, iris="#E4561D"),
        eye((42, -34), 28, 30, iris="#E4561D"),
        filled(ellipse(152, 140, (0, -44)), head_c, name="head"),
    ], transform(pos=jab), name="head-group")

    # the breast sits over the sheen, not under it, so the chin and the
    # breast pinch it down to a crescent at the neck
    return [head,
            filled(ellipse(146, 104, (0, 92)), breast_c, name="breast"),
            ] + collar + [
        wing(-1, 0.0), wing(1, 0.5),
        filled(ellipse(192, 156, (0, 78)), body_c, name="body"),
    ]
