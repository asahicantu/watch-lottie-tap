from critter_parts import FRAMES, eye, smile, wiggle
from lottie_kit import (
    ellipse, filled, group, oscillate, outlined, path, transform,
)


def sheep():
    """A woolly head-on sheep: an irregular fleece framing a long tapered face,
    with the drooping ears and horizontal slit pupils sheep actually have."""
    wool, wool_hi, wool_lo = "#f7f3ea", "#fdfaf2", "#ddd3c1"
    face, face_lo, shade = "#ddcbb0", "#c6b094", "#cdc2ad"
    ear_in, nose, slit = "#b0887c", "#5d4f46", "#241e1a"

    # Puffs of differing size on a wobbly ring, so the fleece reads as a clump
    # of wool rather than a cog of even circles. The ring stops short at the
    # bottom, which lets the muzzle poke out below the wool.
    ring = [(2, -120, 116), (-56, -106, 106), (-106, -66, 118), (-124, -6, 102),
            (-112, 48, 94), (-70, 88, 86), (66, 92, 90), (114, 52, 98),
            (124, -8, 106), (100, -64, 112), (56, -110, 102)]
    puffs = [filled(ellipse(d, d * 0.92, (x, y)), wool, name="puff")
             for x, y, d in ring]
    # brighter caps up on the crown, where the light would land
    puffs = [filled(ellipse(d, d * 0.8, (x, y)), wool_hi, name="puff-lit")
             for x, y, d in ((-62, -116, 54), (-4, -130, 50), (-112, -78, 44))] + puffs
    fleece = group(
        puffs + [filled(ellipse(230, 208, (0, -14)), wool_lo, name="fleece-core")],
        transform(rotation=oscillate(FRAMES, 0, 3, 76)), name="fleece")

    def ear(x, phase):
        return group(
            [filled(ellipse(46, 20, (x * 0.52, 26)), ear_in, name="inner"),
             filled(ellipse(106, 54, (x * 0.44, 24)), face_lo, name="outer")],
            wiggle((x, -16), base_rot=x * 0.26, amp=6, period=30, phase=phase),
            name="ear")

    return [
        smile(42, 6, y=92, color="#7d6857", w=5),
        outlined(path([(0, 80), (0, 92)], closed=False), "#7d6857", 5,
                 name="philtrum"),
        filled(ellipse(17, 10), slit,
               transform(pos=(-19, 64), rotation=-26), name="nostril"),
        filled(ellipse(17, 10), slit,
               transform(pos=(19, 64), rotation=26), name="nostril"),
        filled(ellipse(62, 38, (0, 62)), nose, name="nose-pad"),
        eye((-46, -14), 40, 42), eye((46, -14), 40, 42),
        # the woolly forelock breaks over the brow, as it does on a real sheep
        group([filled(ellipse(62, 44, (-42, -4)), wool, name="curl"),
               filled(ellipse(62, 44, (42, -4)), wool, name="curl"),
               filled(ellipse(72, 48, (0, 6)), wool, name="curl")],
              transform(pos=(0, -66)), name="forelock"),
        filled(ellipse(104, 126, (0, 44)), face, name="muzzle"),
        filled(ellipse(150, 128, (0, -14)), face, name="skull"),
        # a darker wool ring behind the face reads as the fleece shadowing it
        filled(ellipse(168, 146, (0, 2)), shade, name="face-shadow"),
        ear(-76, 0.0), ear(76, 0.5),
        fleece,
    ]
