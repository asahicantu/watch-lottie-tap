"""Twenty-five more critters: set C."""

import math

from critter_parts import (
    FRAMES, dot_eye, eye, oscillate, smile, triangle, wiggle,
)
from lottie_kit import (
    animated, ellipse, filled, group, outlined, path, rect, transform,
)


def whale():
    body_c, belly_c = "#1E88E5", "#BBDEFB"
    def fin(x, ph):
        return filled(ellipse(60, 30), body_c,
                      wiggle((x, 40), base_rot=x * 0.2, amp=10, period=40, phase=ph),
                      name="fin")
    spout = group([filled(ellipse(10, 20, (0, -20)), "#E3F2FD", name="drop") for i in range(3)],
                  transform(pos=(0, -80), scale=animated([(0, [0, 0]), (20, [100, 100]), (40, [0, 0]), (FRAMES, [0, 0])])),
                  name="spout")
    return [
        spout,
        dot_eye((-50, -10), 15), dot_eye((50, -10), 15),
        filled(ellipse(160, 60, (0, 60)), belly_c, name="belly"),
        filled(ellipse(220, 160), body_c, name="body"),
        fin(-100, 0.0), fin(100, 0.5),
    ]


def shark():
    body_c, belly_c = "#78909C", "#CFD8DC"
    dorsal = filled(triangle(60, 80, tilt=20), body_c, transform(pos=(0, -90)), name="dorsal")
    teeth = group([filled(triangle(15, 20), "#FFFFFF", transform(pos=(i*20 - 40, 40), rotation=180)) for i in range(5)], name="teeth")
    return [
        teeth,
        smile(100, 20, y=30, color="#455A64", w=4),
        dot_eye((-50, -20), 14), dot_eye((50, -20), 14),
        filled(ellipse(160, 50, (0, 50)), belly_c, name="belly"),
        filled(ellipse(210, 140), body_c, name="body"),
        dorsal,
    ]


def dolphin():
    body_c, belly_c = "#4FC3F7", "#E1F5FE"
    return [
        smile(60, 15, y=30, color="#0288D1", w=4),
        dot_eye((-40, -20), 12), dot_eye((40, -20), 12),
        filled(ellipse(140, 40, (0, 45)), belly_c, name="belly"),
        filled(ellipse(190, 120), body_c, name="body"),
        filled(ellipse(60, 30, (0, 0)), body_c, transform(pos=(0, 60), rotation=10), name="tail"),
    ]


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
def turtle():
    shell_c, skin_c = "#43A047", "#8BC34A"
    pattern = group([filled(ellipse(40, 40, (x, y)), "#2E7D32") for x, y in [(-40, -30), (40, -30), (0, 20)]], name="pattern")
    return [
        pattern,
        filled(ellipse(180, 140), shell_c, name="shell"),
        dot_eye((-40, -60), 12), dot_eye((40, -60), 12),
        filled(ellipse(100, 80, (0, -70)), skin_c, name="head"),
        filled(ellipse(50, 30, (-80, 40)), skin_c, transform(rotation=-30), name="flipper"),
        filled(ellipse(50, 30, (80, 40)), skin_c, transform(rotation=30), name="flipper"),
    ]


def crab():
    body_c = "#E53935"
    def claw(x, ph):
        return group([filled(ellipse(50, 40, (0, -20)), body_c, name="pincer"),
                      filled(rect(15, 40, (0, 20), radius=7), body_c, name="arm")],
                     wiggle((x, -40), base_rot=x*0.2, amp=20, period=25, phase=ph), name="claw")
    return [
        claw(-100, 0.0), claw(100, 0.5),
        dot_eye((-30, -70), 10), dot_eye((30, -70), 10),
        outlined(path([(-30, -40), (-30, -70)], False), body_c, 4, name="stalk"),
        outlined(path([(30, -40), (30, -70)], False), body_c, 4, name="stalk"),
        filled(ellipse(180, 120), body_c, name="body"),
    ]


def butterfly():
    edge, field, core = "#AD1457", "#F06292", "#F8BBD0"
    body_c, seg_c = "#4A2C3A", "#7B4A5C"

    # Forewing above, hindwing below. Each is drawn three times - full size in
    # the border colour, then smaller copies inset toward the body - which
    # leaves an even band of colour round the outer edge.
    fore = [(0, -18), (42, -122), (100, -130), (128, -72), (112, -14), (36, 6)]
    hind = [(0, -6), (84, 8), (110, 54), (78, 110), (28, 102), (8, 46)]

    def wing_path(verts, k=0.28):
        """Rounds the corners off a wing outline, so it reads as a wing rather
        than a hexagon: each tangent follows the line between its neighbours."""
        tans = []
        for i, _ in enumerate(verts):
            px, py = verts[i - 1]
            nx, ny = verts[(i + 1) % len(verts)]
            ox, oy = (nx - px) * k, (ny - py) * k
            tans.append(((-ox, -oy), (ox, oy)))
        return path(verts, closed=True, tangents=tans)

    def ocellus(x, y, r):
        return group([filled(ellipse(r * 0.40, r * 0.40), "#FFF3F7", name="pupil"),
                      filled(ellipse(r, r), body_c, name="ring")],
                     transform(pos=(x, y)), name="ocellus")

    def panel(verts, spots, name):
        return group(
            spots + [group([filled(wing_path(verts), core, name="core")],
                           transform(scale=(62, 62)), name="core-inset"),
                     group([filled(wing_path(verts), field, name="field")],
                           transform(scale=(86, 86)), name="field-inset"),
                     filled(wing_path(verts), edge, name="edge")],
            name=name)

    def flap(mirror):
        # a head-on flap is a horizontal squeeze; four beats across the loop
        keys = []
        for i in range(4):
            keys.append((i * 22, [100 * mirror, 100]))
            keys.append((i * 22 + 11, [68 * mirror, 100]))
        keys.append((FRAMES, [100 * mirror, 100]))
        return animated(keys)

    def wing(mirror):
        return group([panel(fore, [ocellus(84, -80, 18), ocellus(60, -36, 10)],
                            "forewing"),
                      panel(hind, [ocellus(62, 56, 14)], "hindwing")],
                     transform(pos=(0, -12), scale=flap(mirror)), name="wing")

    def antenna(mirror):
        return group([filled(ellipse(16, 16, (34 * mirror, -46)), body_c,
                             name="club"),
                      outlined(path([(0, 0), (10 * mirror, -26),
                                     (34 * mirror, -46)], closed=False),
                               body_c, 5, name="stalk")],
                     wiggle((14 * mirror, -98), amp=4, period=26,
                            phase=0.25 * mirror), name="antenna")

    return [
        antenna(-1), antenna(1),
        dot_eye((-26, -74), 9), dot_eye((26, -74), 9),
        filled(ellipse(102, 82, (0, -72)), body_c, name="head"),
        outlined(path([(-14, 24), (14, 24)], closed=False), seg_c, 4, name="seam"),
        outlined(path([(-12, 44), (12, 44)], closed=False), seg_c, 4, name="seam"),
        outlined(path([(-9, 64), (9, 64)], closed=False), seg_c, 4, name="seam"),
        filled(ellipse(36, 94, (0, 42)), body_c, name="abdomen"),
        filled(ellipse(56, 66, (0, -16)), body_c, name="thorax"),
        wing(-1), wing(1),
    ]
def squirrel():
    fur_c, tail_c = "#8D6E63", "#6D4C41"
    tail = filled(ellipse(80, 140, (0, -70)), tail_c,
                  wiggle((80, 20), base_rot=30, amp=10, period=40), name="tail")
    return [
        tail,
        filled(ellipse(40, 50, (0, 40)), "#FFCC80", name="acorn"),
        smile(30, 10, y=25, color="#3E2723", w=3),
        dot_eye((-35, -10), 14), dot_eye((35, -10), 14),
        filled(ellipse(150, 140), fur_c, name="head"),
        filled(triangle(30, 40), fur_c, wiggle((-50, -60), base_rot=-20), name="ear"),
        filled(triangle(30, 40), fur_c, wiggle((50, -60), base_rot=20, phase=0.5), name="ear"),
    ]


def zebra():
    base_c, stripe_c = "#FFFFFF", "#424242"
    stripes = group([filled(rect(40 if i == 1 else 100, 15, (0, i*30 - 60),
                                 radius=5), stripe_c) for i in range(5)],
                    name="stripes")
    return [
        eye((-45, -30), 32, 36), eye((45, -30), 32, 36),
        stripes,
        filled(ellipse(160, 190), base_c, name="head"),
        filled(triangle(35, 60), base_c, wiggle((-55, -85), base_rot=-15), name="ear"),
        filled(triangle(35, 60), base_c, wiggle((55, -85), base_rot=15, phase=0.5), name="ear"),
    ]


def kangaroo():
    fur_c = "#FB8C00"
    return [
        smile(40, 15, y=35, color="#BF360C", w=4),
        dot_eye((-40, -15), 15), dot_eye((40, -15), 15),
        filled(ellipse(120, 50, (0, 60)), "#FFCC80", name="pouch"),
        filled(ellipse(170, 180), fur_c, name="head"),
        filled(rect(30, 90, (0, -45), radius=15), fur_c, wiggle((-50, -80), base_rot=-20), name="ear"),
        filled(rect(30, 90, (0, -45), radius=15), fur_c, wiggle((50, -80), base_rot=20, phase=0.5), name="ear"),
    ]


def camel():
    fur_c = "#C2B280"
    humps = group([filled(ellipse(70, 60, (x, -70)), fur_c) for x in [-40, 40]], name="humps")
    return [
        humps,
        smile(50, 15, y=40, color="#8D6E63", w=4),
        eye((-45, -10), 34, 38, iris="#5D4037"), eye((45, -10), 34, 38, iris="#5D4037"),
        filled(ellipse(160, 150), fur_c, name="head"),
    ]


def deer():
    fur_c = "#8B4513"
    antler = lambda x, ph: group([filled(rect(10, 60, (0, -30), radius=5), "#D7CCC8"),
                                 filled(rect(30, 8, (0, -50), radius=4), "#D7CCC8")],
                                wiggle((x, -90), base_rot=x*0.2, amp=5, period=40, phase=ph), name="antler")
    spots = [filled(ellipse(15, 10, (x, y)), "#FFFFFF") for x, y in [(-30, 40), (30, 40), (0, 60)]]
    return [
        antler(-40, 0.0), antler(40, 0.5),
    ] + spots + [
        dot_eye((-40, -20), 16), dot_eye((40, -20), 16),
        filled(ellipse(170, 160), fur_c, name="head"),
        filled(triangle(30, 50), fur_c, wiggle((-60, -70), base_rot=-30), name="ear"),
        filled(triangle(30, 50), fur_c, wiggle((60, -70), base_rot=30, phase=0.5), name="ear"),
    ]


def eagle():
    head_c, feather_c, beak_c = "#FFFFFF", "#795548", "#FFD54F"
    dark, brow_c = "#5D4037", "#D6CCC2"

    def wing(mirror, phase):
        # the outer edge steps down in three primary feathers
        shape = [(0, -20), (54, -8), (88, 24), (94, 56), (72, 50), (76, 88),
                 (50, 66), (46, 98), (22, 60), (0, 28)]
        verts = [(x * mirror, y) for x, y in shape]
        return group([outlined(path(verts), dark, 4, name="edge"),
                      filled(path(verts), feather_c, name="pinion")],
                     wiggle((86 * mirror, 26), base_rot=6 * mirror, amp=7,
                            period=30, phase=phase), name="wing")

    # the white head ends in a ruff of round feathers over the brown chest
    ruff = [filled(ellipse(40, 36, (x, 64)), "#F4F0EA", name="ruff")
            for x in (-56, -28, 0, 28, 56)]

    return [
        smile(50, 5, y=18, color="#A9791C", w=4),
        filled(ellipse(9, 7, (-16, -2)), dark, name="nostril"),
        filled(ellipse(9, 7, (16, -2)), dark, name="nostril"),
        # one shape for the whole beak: wide at the brow, hooking to a point
        filled(path([(-38, -20), (38, -20), (28, 24), (17, 58), (11, 78),
                     (-11, 78), (-17, 58), (-28, 24)]),
               beak_c, transform(pos=(0, 4)), name="beak"),
        filled(ellipse(30, 26, (0, 80)), "#EFA51C", name="hook"),
        filled(rect(48, 12, radius=6), brow_c,
               transform(pos=(-45, -44), rotation=-16), name="brow"),
        filled(rect(48, 12, radius=6), brow_c,
               transform(pos=(45, -44), rotation=16), name="brow"),
        eye((-42, -18), 34, 38, iris="#F9A825"),
        eye((42, -18), 34, 38, iris="#F9A825"),
        filled(ellipse(168, 152), head_c, name="head"),
    ] + ruff + [
        filled(ellipse(196, 118, (0, 96)), feather_c, name="body"),
        wing(-1, 0.0), wing(1, 0.5),
    ]
def flamingo():
    pink_c, beak_c = "#FF80AB", "#212121"
    return [
        filled(path([(0, 0), (20, 0), (10, 50), (-5, 30)], True), beak_c, transform(pos=(0, -60), rotation=10), name="beak"),
        dot_eye((-20, -80), 10), dot_eye((20, -80), 10),
        filled(ellipse(80, 70, (0, -80)), pink_c, name="head"),
        outlined(path([(0, -50), (0, 50)], False), pink_c, 20, name="neck"),
        filled(ellipse(150, 100, (0, 60)), pink_c, name="body"),
    ]


def hamster():
    fur_c, cheek_c = "#FFD180", "#FFAB91"
    return [
        filled(ellipse(50, 40, (-60, 30)), cheek_c, name="cheek"),
        filled(ellipse(50, 40, (60, 30)), cheek_c, name="cheek"),
        smile(30, 10, y=30, color="#5D4037", w=3),
        dot_eye((-40, -10), 16), dot_eye((40, -10), 16),
        filled(ellipse(180, 160), fur_c, name="head"),
        filled(ellipse(40, 40), fur_c, wiggle((-70, -70)), name="ear"),
        filled(ellipse(40, 40), fur_c, wiggle((70, -70), phase=0.5), name="ear"),
    ]


def hedgehog():
    skin_c, spike_c = "#D7CCC8", "#6D4C41"
    spikes = group([filled(triangle(30, 40), spike_c, transform(pos=(100 * math.cos(a), 100 * math.sin(a)), rotation=math.degrees(a)+90))
                    for a in [math.pi * i / 6.0 for i in range(13)]], name="spikes")
    return [
        spikes,
        smile(40, 10, y=30, color="#3E2723", w=3),
        dot_eye((-30, -10), 12), dot_eye((30, -10), 12),
        filled(ellipse(160, 140), skin_c, name="body"),
        filled(ellipse(20, 20, (0, 10)), "#3E2723", name="nose"),
    ]


def ladybug():
    red_c, black_c = "#D32F2F", "#212121"
    spots = group([filled(ellipse(25, 25, (x, y)), black_c) for x, y in [(-40, -20), (40, -20), (0, 40)]], name="spots")
    return [
        dot_eye((-32, -112), 8, color="#FFFFFF"),
        dot_eye((32, -112), 8, color="#FFFFFF"),
        spots,
        filled(ellipse(190, 170), red_c, name="body"),
        filled(ellipse(140, 110, (0, -92)), black_c, name="head"),
    ]


def llama():
    wool, muzzle_c, pink = "#E0E0E0", "#F5F5F5", "#F8BBD0"

    # Banana ears
    def ear(x, ph):
        return group(
            [filled(rect(20, 70, (0, -35), radius=10), pink, name="inner"),
             filled(rect(34, 100, (0, -45), radius=17), wool, name="outer")],
            wiggle((x, -74), base_rot=x * 0.25, amp=8, period=32, phase=ph), name="ear")

    # Fluffy wool on top of the head
    puffs = [
        filled(ellipse(50, 50, (-40, -80)), wool, name="puff"),
        filled(ellipse(54, 54, (0, -90)), wool, name="puff"),
        filled(ellipse(50, 50, (40, -80)), wool, name="puff"),
    ]

    return [
        smile(44, 16, y=52, color="#9E9E9E", w=5),
        group([filled(ellipse(14, 10, (-16, 0)), "#BDBDBD", name="nostril"),
               filled(ellipse(14, 10, (16, 0)), "#BDBDBD", name="nostril")],
              transform(pos=(0, 42)), name="nostrils"),
        filled(ellipse(90, 74, (0, 48)), muzzle_c, name="muzzle"),
        eye((-40, -22), 34, 38, iris="#424242"),
        eye((40, -22), 34, 38, iris="#424242"),
        filled(ellipse(164, 184), wool, name="head"),
    ] + puffs + [ear(-62, 0.0), ear(62, 0.5)]


def lobster():
    body_c = "#E64A19"
    def claw(x, ph):
        return group([filled(path([(0, 0), (20, -30), (40, 0), (20, 10)], True), body_c, name="pincer"),
                      filled(rect(12, 50, (0, 30), radius=6), body_c, name="arm")],
                     wiggle((x, -30), base_rot=x*0.3, amp=20, period=25, phase=ph), name="claw")
    return [
        claw(-110, 0.0), claw(110, 0.5),
        dot_eye((-30, -60), 12), dot_eye((30, -60), 12),
        filled(ellipse(140, 180), body_c, name="body"),
        filled(rect(100, 20, (0, 60), radius=10), body_c, name="segment"),
    ]


def mole():
    fur_c, nose_c = "#3E2723", "#F8BBD0"
    return [
        filled(ellipse(30, 20, (0, 25)), nose_c, name="nose"),
        dot_eye((-35, -10), 8), dot_eye((35, -10), 8),
        filled(ellipse(170, 150), fur_c, name="head"),
        filled(ellipse(60, 40, (-80, 40)), "#D7CCC8", transform(rotation=20), name="claw"),
        filled(ellipse(60, 40, (80, 40)), "#D7CCC8", transform(rotation=-20), name="claw"),
    ]


def ostrich():
    skin_c, feather_c = "#E0E0E0", "#BDBDBD"
    return [
        filled(triangle(40, 30), "#FFD54F", transform(pos=(0, -50), rotation=180), name="beak"),
        eye((-25, -75), 36, 40), eye((25, -75), 36, 40),
        filled(ellipse(80, 90, (0, -75)), skin_c, name="head"),
        outlined(path([(0, -30), (0, 50)], False), skin_c, 25, name="neck"),
        filled(ellipse(180, 120, (0, 70)), feather_c, name="body"),
    ]


def peacock():
    body_c, fan_c = "#0288D1", "#4FC3F7"
    feathers = group([filled(ellipse(40, 80, (120 * math.cos(a), 40 + 60 * math.sin(a))), fan_c,
                             transform(rotation=math.degrees(a)+90))
                      for a in [math.pi * i / 6.0 for i in range(1, 6)]], name="fan")
    return [
        feathers,
        dot_eye((-25, -20), 12), dot_eye((25, -20), 12),
        filled(ellipse(100, 140), body_c, name="body"),
        filled(triangle(20, 25), "#FFD54F", transform(pos=(0, 0), rotation=180), name="beak"),
    ]


def rhino():
    hide_c = "#9E9E9E"
    return [
        filled(triangle(30, 50), "#CFD8DC", transform(pos=(0, 20), rotation=0), name="horn"),
        dot_eye((-50, -20), 15), dot_eye((50, -20), 15),
        filled(ellipse(200, 160), hide_c, name="head"),
        filled(triangle(30, 40), hide_c, wiggle((-70, -70), base_rot=-20), name="ear"),
        filled(triangle(30, 40), hide_c, wiggle((70, -70), base_rot=20, phase=0.5), name="ear"),
    ]


def scorpion():
    body_c = "#212121"
    tail = group([filled(ellipse(30, 30, (0, -i*25)), body_c) for i in range(4)],
                 wiggle((0, -80), base_rot=0, amp=15, period=35), name="tail")
    return [
        tail,
        filled(triangle(20, 30), "#D32F2F", transform(pos=(0, -160)), name="stinger"),
        dot_eye((-30, -20), 8, color="#FFFFFF"), dot_eye((30, -20), 8, color="#FFFFFF"),
        filled(ellipse(160, 120), body_c, name="body"),
        filled(ellipse(50, 40, (-90, 0)), body_c, name="pincer"),
        filled(ellipse(50, 40, (90, 0)), body_c, name="pincer"),
    ]


def seahorse():
    body_c = "#FFD54F"
    return [
        filled(ellipse(40, 20, (30, -20)), body_c, name="snout"),
        dot_eye((-10, -40), 12), dot_eye((40, -40), 12),
        filled(ellipse(100, 160), body_c, name="body"),
        filled(path([(0, 80), (20, 120), (-20, 120)], True), body_c, name="tail"),
        filled(ellipse(40, 60, (-50, 20)), "#FFF176", name="fin"),
    ]


SET_C = {
    "whale": whale, "shark": shark, "dolphin": dolphin, "octopus": octopus,
    "turtle": turtle, "crab": crab, "butterfly": butterfly, "squirrel": squirrel,
    "zebra": zebra, "kangaroo": kangaroo, "camel": camel, "deer": deer,
    "eagle": eagle, "flamingo": flamingo, "hamster": hamster, "hedgehog": hedgehog,
    "ladybug": ladybug, "llama": llama, "lobster": lobster, "mole": mole,
    "ostrich": ostrich, "peacock": peacock, "rhino": rhino, "scorpion": scorpion,
    "seahorse": seahorse,
}
