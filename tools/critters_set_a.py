"""The first ten critters: the farmyard-and-garden set."""

import math

from critter_parts import (
    FRAMES, critter, dot_eye, eye, oscillate, smile, triangle, wiggle,
)
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform


def cat():
    fur, inner = "#f0a04b", "#f6c7a8"

    def ear(x, phase):
        return group(
            [filled(triangle(52, 46, tilt=x * 0.18), inner,
                    transform(scale=(62, 62)), name="inner"),
             filled(triangle(74, 72, tilt=x * 0.14), fur, name="outer")],
            wiggle((x, -58), base_rot=x * 0.09, amp=6, period=26, phase=phase),
            name="ear")

    def whisker(x, y, tilt):
        return outlined(path([(0, 0), (x, tilt)], closed=False), "#f7e6d4", 5,
                        transform(pos=(x * 0.42, y)), name="whisker")

    return [
        whisker(74, 8, -12), whisker(80, 22, 2), whisker(74, 36, 16),
        whisker(-74, 8, -12), whisker(-80, 22, 2), whisker(-74, 36, 16),
        smile(46, 16, y=34, color="#8a4a3c", w=6),
        filled(triangle(26, 20, pos=(0, 10)), "#e2657a",
               transform(rotation=180), name="nose"),
        eye((-44, -10), 36, 42, iris="#4b9b52"),
        eye((44, -10), 36, 42, iris="#4b9b52"),
        filled(ellipse(196, 176), fur, name="head"),
        ear(-62, 0.0), ear(62, 0.5),
    ]


def dog():
    fur, ear_c = "#c98a4b", "#8e5a2b"

    def flap(x, phase):
        return filled(rect(58, 128, (0, 62), radius=28), ear_c,
                      wiggle((x, -34), base_rot=x * 0.12, amp=11, period=24,
                             phase=phase),
                      name="ear")

    return [
        filled(rect(44, 34, (0, 16), radius=16), "#e5717f",
               transform(pos=(0, 60),
                         scale=animated([(0, [100, 100]), (20, [100, 128]),
                                         (36, [100, 100]), (52, [100, 122]),
                                         (66, [100, 100]), (FRAMES, [100, 100])])),
               name="tongue"),
        filled(ellipse(46, 34, (0, 14)), "#2b2320", name="nose"),
        filled(ellipse(120, 86, (0, 34)), "#f3e2c8", name="snout"),
        eye((-44, -30), 34, 38, iris="#3a2a20"),
        eye((44, -30), 34, 38, iris="#3a2a20"),
        filled(ellipse(190, 174), fur, name="head"),
        flap(-84, 0.0), flap(84, 0.5),
    ]


def cow():
    return [
        filled(ellipse(20, 14, (26, 46)), "#c4707c", name="nostril"),
        filled(ellipse(20, 14, (-26, 46)), "#c4707c", name="nostril"),
        filled(ellipse(122, 84, (0, 44)), "#f2aab4", name="muzzle"),
        eye((-46, -28), 34, 38),
        eye((46, -28), 34, 38),
        filled(ellipse(56, 46, (58, 42)), "#3f3833", name="spot"),
        filled(ellipse(64, 54, (-56, -50)), "#3f3833", name="spot"),
        filled(ellipse(192, 172), "#f7f3ec", name="head"),
        filled(ellipse(64, 40), "#f2d9a8",
               wiggle((-104, -18), base_rot=-16, amp=5, period=32), name="ear"),
        filled(ellipse(64, 40), "#f2d9a8",
               wiggle((104, -18), base_rot=16, amp=5, period=32, phase=0.5),
               name="ear"),
        filled(triangle(24, 34, tilt=-6), "#e8dcc2",
               transform(pos=(-56, -78), rotation=-14), name="horn"),
        filled(triangle(24, 34, tilt=6), "#e8dcc2",
               transform(pos=(56, -78), rotation=14), name="horn"),
    ]


def duck():
    return [
        # the lower bill hinges open and shut, so the duck reads as quacking
        filled(ellipse(98, 40, (0, 14)), "#d9741c",
               transform(pos=(0, 30), rotation=animated(
                   [(0, 0), (10, 13), (20, 0), (30, 13), (40, 0), (FRAMES, 0)])),
               name="lower-bill"),
        filled(ellipse(116, 48, (0, -6)), "#f6a02c",
               transform(pos=(0, 30)), name="upper-bill"),
        dot_eye((-44, -22), 20),
        dot_eye((44, -22), 20),
        filled(ellipse(178, 166), "#ffd93b", name="head"),
        filled(path([(0, 0), (-18, -44), (10, -30), (0, -66), (26, -26), (16, -8)]),
               "#ffe882", wiggle((-6, -78), amp=7, period=28), name="tuft"),
    ]


def frog():
    skin, belly = "#6cc24a", "#a7dd7f"

    def eye_dome(x):
        return group([eye((0, 0), 40, 42, iris="#2f2a26"),
                      filled(ellipse(72, 70), skin, name="dome")],
                     transform(pos=(x, -70)), name="eyedome")

    return [
        filled(ellipse(14, 10, (-22, -6)), "#3d7a2a", name="nostril"),
        filled(ellipse(14, 10, (22, -6)), "#3d7a2a", name="nostril"),
        smile(126, 44, y=18, color="#2f6b20", w=9),
        filled(ellipse(120, 60, (0, 52)), belly, name="chin"),
        filled(ellipse(206, 156), skin, name="head"),
        eye_dome(-58), eye_dome(58),
    ]


def lion():
    mane, fur = "#c9741f", "#f4c07a"
    tufts = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        tufts.append(filled(ellipse(76, 76, (110 * math.cos(a), 110 * math.sin(a))),
                            "#a75a13", name="tuft"))
    mane_group = group(tufts + [filled(ellipse(238, 232), mane, name="mane-core")],
                       transform(rotation=oscillate(FRAMES, 0, 6, 60)), name="mane")
    return [
        smile(52, 20, y=34, color="#7a4a20", w=6),
        filled(triangle(30, 22, pos=(0, 11)), "#7a4a20",
               transform(rotation=180), name="nose"),
        filled(ellipse(58, 46, (-26, 34)), "#fce4c0", name="muzzle"),
        filled(ellipse(58, 46, (26, 34)), "#fce4c0", name="muzzle"),
        eye((-40, -20), 32, 36, iris="#5a3a15"),
        eye((40, -20), 32, 36, iris="#5a3a15"),
        filled(ellipse(172, 158), fur, name="face"),
        mane_group,
    ]


def bee():
    def wing(x, phase):
        return group([filled(ellipse(58, 96, (0, -48)), "#eaf4ff", name="wing")],
                     transform(pos=(x, -46), opacity=78,
                               rotation=oscillate(FRAMES, x * 0.62, 26, 6, phase)),
                     name="wing-pivot")

    def antenna(x, phase):
        return group([filled(ellipse(16, 16, (x * 0.5, -46)), "#3a3226", name="tip"),
                      outlined(path([(0, 0), (x * 0.5, -46)], closed=False),
                               "#3a3226", 6, name="stalk")],
                     wiggle((x, -62), amp=6, period=22, phase=phase), name="antenna")

    return [
        # the face sits above the stripes so neither hides the other
        smile(40, 14, y=-18, color="#3a3226", w=5),
        dot_eye((-34, -46), 15), dot_eye((34, -46), 15),
        filled(rect(112, 24, (0, 58), radius=12), "#3a3226", name="stripe"),
        filled(rect(150, 24, (0, 22), radius=12), "#3a3226", name="stripe"),
        filled(ellipse(184, 158, (0, 12)), "#ffd21f", name="body"),
        filled(triangle(26, 30), "#3a3226", transform(pos=(0, 116)), name="stinger"),
        antenna(-40, 0.0), antenna(40, 0.5),
        wing(-58, 0.0), wing(58, 0.5),
    ]


def sheep():
    puffs = []
    for i in range(9):
        a = 2 * math.pi * i / 9
        puffs.append(filled(ellipse(96, 96, (96 * math.cos(a), 96 * math.sin(a))),
                            "#fdfbf6", name="puff"))
    fluff = group(puffs + [filled(ellipse(190, 178), "#f2eee6", name="fluff-core")],
                  transform(rotation=oscillate(FRAMES, 0, 5, 64)), name="fluff")
    return [
        filled(ellipse(12, 9, (-14, 44)), "#5c4b41", name="nostril"),
        filled(ellipse(12, 9, (14, 44)), "#5c4b41", name="nostril"),
        dot_eye((-30, 4), 16), dot_eye((30, 4), 16),
        filled(ellipse(112, 130, (0, 22)), "#e3d3c0", name="face"),
        filled(ellipse(64, 38), "#cbb7a2",
               wiggle((-72, 4), base_rot=-18, amp=7, period=26), name="ear"),
        filled(ellipse(64, 38), "#cbb7a2",
               wiggle((72, 4), base_rot=18, amp=7, period=26, phase=0.5), name="ear"),
        fluff,
    ]


def owl():
    body, disc = "#8b5e3c", "#f0dcc2"

    def disc_eye(x):
        return group([eye((0, 0), 40, 44, iris="#2b2118"),
                      filled(ellipse(96, 96), disc, name="disc")],
                     transform(pos=(x, -22)), name="eye-disc")

    return [
        filled(triangle(34, 40), "#f0902a",
               transform(pos=(0, 62), rotation=180), name="beak"),
        disc_eye(-48), disc_eye(48),
        filled(ellipse(120, 118, (0, 62)), "#c9a273", name="belly"),
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


def pig():
    skin, deep = "#f6a5b8", "#e07f96"
    snout = group(
        [filled(ellipse(18, 24, (-20, 0)), "#a9526a", name="nostril"),
         filled(ellipse(18, 24, (20, 0)), "#a9526a", name="nostril"),
         filled(ellipse(104, 76), deep, name="snout")],
        transform(pos=(0, 34),
                  scale=animated([(0, [100, 100]), (24, [110, 92]), (40, [100, 100]),
                                  (56, [108, 94]), (70, [100, 100]),
                                  (FRAMES, [100, 100])])),
        name="snout-group")
    return [
        snout,
        dot_eye((-46, -26), 18), dot_eye((46, -26), 18),
        filled(ellipse(196, 168), skin, name="head"),
        filled(triangle(64, 62, tilt=-10), deep,
               wiggle((-64, -62), base_rot=-12, amp=8, period=26), name="ear"),
        filled(triangle(64, 62, tilt=10), deep,
               wiggle((64, -62), base_rot=12, amp=8, period=26, phase=0.5), name="ear"),
    ]


SET_A = {
    "cat": cat, "dog": dog, "cow": cow, "duck": duck, "frog": frog,
    "lion": lion, "bee": bee, "sheep": sheep, "owl": owl, "pig": pig,
}
