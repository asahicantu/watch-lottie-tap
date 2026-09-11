import math

from critter_parts import FRAMES, eye, smile
from lottie_kit import ellipse, filled, group, oscillate, rect, transform


def octopus():
    mantle, arm_c, cup_c, deep = "#BA68C8", "#A83FB6", "#E3BCF0", "#5B1470"

    # Each arm is a chain of six rounded capsules, every one parented to the
    # end of the one before it. A single stiff arm swinging from the shoulder
    # looked like a wiper blade; because each joint here oscillates a little
    # wider and a little later than its parent, the bend travels out to the
    # tip and the arm undulates instead of pivoting.
    LENS = (38, 34, 30, 26, 22)
    RADS = (17.0, 13.5, 10.0, 7.0, 4.0)
    # no two neighbouring arms the same length, mirrored left to right
    STRETCH = (1.00, 0.94, 1.06, 0.97)

    def arm(i):
        phi = math.pi * (0.10 + 0.80 * i / 7.0)
        attach = (84 * math.cos(phi), 70 * math.sin(phi))
        side = 1.0 if phi < math.pi / 2 else -1.0
        # most arms hook in under the body; the outermost pair hooks out
        curl = -side if i in (0, 7) else side
        stretch = STRETCH[min(i, 7 - i)]
        # the arm fans outward, pulled back toward straight down - the
        # outward-hooking pair starts steeper so its curl lifts the tip
        # instead of throwing the whole arm out sideways
        pull = 0.78 if curl != side else 0.38
        heading = math.degrees(phi + (math.pi / 2 - phi) * pull)

        node = None
        for s in reversed(range(len(LENS))):     # built from the tip inward
            length, r = LENS[s] * stretch, RADS[s]
            items = []
            if s < 3:
                items += [filled(ellipse(r * 0.5, r * 0.5,
                                         (length * f, curl * r * 0.44)),
                                 cup_c, name="cup")
                          for f in (0.28, 0.70)]
            # a capsule: as long as the segment, rounded off at both ends
            items.append(filled(rect(length + 2 * r, 2 * r, (length * 0.5, 0),
                                     radius=r), arm_c, name="limb"))
            if node is not None:
                items.append(node)
            base = (heading if s == 0 else 0.0) + curl * (2.5 + 4.0 * s)
            node = group(
                items,
                transform(pos=attach if s == 0 else (LENS[s - 1] * stretch, 0),
                          rotation=oscillate(FRAMES, base, 2.5 + 2.2 * s, 40,
                                             i * 0.13 + s * 0.15, steps=3)),
                name="joint")
        return node

    return [
        smile(44, 11, y=44, color=deep, w=5),
        eye((-44, -26), 34, 38, iris="#4A148C"),
        eye((44, -26), 34, 38, iris="#4A148C"),
        filled(ellipse(124, 96, (0, 28)), "#CE93D8", name="front"),
        filled(ellipse(172, 180, (0, -14)), mantle, name="mantle"),
    ] + [arm(i) for i in range(8)]
