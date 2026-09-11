from critter_parts import FRAMES, eye, smile, wiggle
from lottie_kit import ellipse, filled, group, oscillate, rect, transform


def gorilla():
    """A silverback portrait: peaked crest, heavy brow, broad flat muzzle, and
    two fists taking turns on the chest. The old one was a black disc with
    eyes - at watch size nothing but the eyes survived, because every feature
    was the same near-black. The fur is lifted to a warm charcoal so the face,
    muzzle and brow can each sit a step apart from it and still read.
    """
    fur, crest_c, shade = "#3D3733", "#2B2624", "#332E2B"
    face_c, muzzle_c = "#584D47", "#6B5C53"
    deep, silver = "#1E1A18", "#5C544E"

    def ear(x, phase):
        return group([filled(ellipse(18, 24), muzzle_c, name="inner"),
                      filled(ellipse(36, 44), fur, name="outer")],
                     wiggle((x, -16), base_rot=x * 0.05, amp=4, period=45,
                            phase=phase), name="ear")

    def arm(x, phase):
        """A forearm hinged at the shoulder. Both swing on the same short
        period half a cycle apart, so the fists take turns thumping the chest
        the way a gorilla actually drums."""
        knuckles = [filled(ellipse(11, 11, (k, 74)), silver, name="knuckle")
                    for k in (-15, 0, 15)]
        return group(
            knuckles + [
                filled(ellipse(56, 50, (0, 86)), crest_c, name="fist"),
                filled(rect(40, 96, (0, 48), radius=20), fur, name="forearm"),
            ],
            transform(pos=(x, 40),
                      rotation=oscillate(FRAMES, x * 0.30, 10, 30, phase)),
            name="arm")

    def nostril(x):
        return filled(ellipse(15, 22), deep,
                      transform(pos=(x, 36), rotation=x * 0.85), name="nostril")

    return [
        nostril(-17), nostril(17),
        smile(66, 15, y=74, color=deep, w=6),
        # the nose pad is one wide flat block, not a snout - it is what tells
        # a gorilla apart from every other dark round face in the set
        filled(rect(80, 48, (0, 32), radius=20), shade, name="nose"),
        filled(ellipse(152, 96, (0, 50)), muzzle_c, name="muzzle"),
        eye((-46, -18), 32, 34, iris="#7A4B22"),
        eye((46, -18), 32, 34, iris="#7A4B22"),
        # the brow is fur-coloured on purpose: it merges into the head and
        # notches the top of the pale face instead of drawing a dark band
        # across it, and that notch is what reads as the scowl
        filled(rect(176, 48, (0, -60), radius=24), fur, name="brow"),
        filled(ellipse(164, 142, (0, 12)), face_c, name="face"),
        # the sagittal crest, drawn on the head rather than behind it, so the
        # skull peaks instead of wearing a hat
        filled(ellipse(64, 96, (0, -76)), shade, name="crest-ridge"),
        filled(ellipse(206, 182, (0, -8)), fur, name="head"),
        ear(-100, 0.0), ear(100, 0.5),
        filled(ellipse(148, 88, (0, -80)), fur, name="crest"),
        arm(-98, 0.0), arm(98, 0.5),
        filled(ellipse(98, 62, (0, 126)), silver, name="chest-patch"),
        filled(ellipse(192, 130, (0, 120)), fur, name="chest"),
    ]
