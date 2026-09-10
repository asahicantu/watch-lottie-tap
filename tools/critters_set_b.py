"""Twenty more critters: the wild-and-farther-afield set.

Same construction as set A - a front-to-back list of shape groups that
`critter()` wraps in the shared idle motion.
"""

import math

from critter_parts import (
    FRAMES, dot_eye, eye, oscillate, smile, triangle, wiggle,
)
from lottie_kit import (
    animated, ellipse, filled, group, outlined, path, rect, transform,
)


# --------------------------------------------------------------------------- #
# extra features this set needs
# --------------------------------------------------------------------------- #

def tuft(x, y, spikes, color, w=22, h=46, spread=26, phase=0.0):
    """A little crest or forelock: a fan of triangles."""
    items = []
    for i in range(spikes):
        offset = (i - (spikes - 1) / 2.0) * spread
        items.append(filled(triangle(w, h - abs(offset) * 0.35, tilt=offset * 0.30),
                            color, transform(pos=(offset, 0)), name="spike"))
    return group(items, wiggle((x, y), amp=5, period=30, phase=phase), name="tuft")


def teeth(count, y, width, size=16, color="#ffffff"):
    items = []
    for i in range(count):
        x = (i - (count - 1) / 2.0) * (width / max(1, count - 1))
        items.append(filled(triangle(size, size * 1.1), color,
                            transform(pos=(x, y), rotation=180), name="tooth"))
    return group(items, name="teeth")


def nostrils(dx, y, w=20, h=14, color="#7a5c4a"):
    return group([filled(ellipse(w, h, (-dx, y)), color, name="nostril"),
                  filled(ellipse(w, h, (dx, y)), color, name="nostril")],
                 name="nostrils")


# --------------------------------------------------------------------------- #
# the critters
# --------------------------------------------------------------------------- #

def horse():
    coat, muzzle, mane = "#c17a3f", "#e6c199", "#5f3b1f"
    return [
        nostrils(24, 66, 22, 16, "#6b4423"),
        filled(ellipse(110, 90, (0, 56)), muzzle, name="muzzle"),
        eye((-46, -42), 32, 36), eye((46, -42), 32, 36),
        tuft(0, -96, 3, mane, w=26, h=52, spread=20),
        filled(ellipse(152, 200), coat, name="head"),
        filled(triangle(32, 56, tilt=-6), coat,
               wiggle((-46, -84), base_rot=-10, amp=7, period=28), name="ear"),
        filled(triangle(32, 56, tilt=6), coat,
               wiggle((46, -84), base_rot=10, amp=7, period=28, phase=0.5), name="ear"),
        filled(ellipse(44, 150, (0, 0)), mane,
               transform(pos=(-66, -18), rotation=-12), name="mane"),
        filled(ellipse(44, 150, (0, 0)), mane,
               transform(pos=(66, -18), rotation=12), name="mane"),
    ]


def elephant():
    hide, inner = "#98a2ad", "#b6bfc8"
    trunk = group(
        [filled(rect(42, 58, (10, 40), radius=20), hide,
                transform(rotation=22), name="trunk-tip"),
         filled(rect(54, 96, (0, 0), radius=24), hide, name="trunk-top")],
        transform(pos=(0, 62),
                  rotation=oscillate(FRAMES, 0, 7, 34)), name="trunk")
    ear = lambda x, ph: group(
        [filled(ellipse(96, 122, (x * 0.18, 6)), inner, name="inner"),
         filled(ellipse(126, 156), hide, name="outer")],
        wiggle((x, -8), base_rot=x * 0.09, amp=7, period=30, phase=ph), name="ear")
    return [
        trunk,
        filled(triangle(20, 40, tilt=-6), "#f4efe4",
               transform(pos=(-40, 92), rotation=8), name="tusk"),
        filled(triangle(20, 40, tilt=6), "#f4efe4",
               transform(pos=(40, 92), rotation=-8), name="tusk"),
        eye((-44, -24), 30, 32), eye((44, -24), 30, 32),
        filled(ellipse(180, 164), hide, name="head"),
        ear(-96, 0.0), ear(96, 0.5),
    ]


def monkey():
    fur, face = "#8a5a3b", "#dba97c"
    return [
        smile(56, 22, y=44, color="#7a4a2c", w=6),
        nostrils(11, 28, 13, 10, "#7a4a2c"),
        eye((-34, -8), 32, 36, iris="#3a2a20"), eye((34, -8), 32, 36, iris="#3a2a20"),
        filled(ellipse(136, 126, (0, 12)), face, name="face"),
        filled(ellipse(182, 170), fur, name="head"),
        tuft(0, -84, 3, fur, w=20, h=34, spread=18),
        group([filled(ellipse(40, 40), face, name="inner"),
               filled(ellipse(62, 62), fur, name="outer")],
              wiggle((-96, -4), amp=6, period=28), name="ear"),
        group([filled(ellipse(40, 40), face, name="inner"),
               filled(ellipse(62, 62), fur, name="outer")],
              wiggle((96, -4), amp=6, period=28, phase=0.5), name="ear"),
    ]


def penguin():
    coat, belly, beak = "#2c333b", "#f8f5ef", "#f0912a"
    return [
        filled(triangle(46, 50), beak,
               transform(pos=(0, 42), rotation=180,
                         scale=animated([(0, [100, 100]), (14, [104, 122]),
                                         (28, [100, 100]), (FRAMES, [100, 100])])),
               name="beak"),
        dot_eye((-36, -10), 17), dot_eye((36, -10), 17),
        filled(ellipse(136, 148, (0, 14)), belly, name="face"),
        filled(ellipse(190, 180), coat, name="head"),
    ]


def tiger():
    coat, cream, stripe = "#f0913c", "#fdf3e6", "#3a2a1e"
    bars = [
        filled(rect(14, 46, radius=7), stripe, transform(pos=(-54, -62), rotation=24),
               name="stripe"),
        filled(rect(14, 52, radius=7), stripe, transform(pos=(-20, -74)), name="stripe"),
        filled(rect(14, 52, radius=7), stripe, transform(pos=(20, -74)), name="stripe"),
        filled(rect(14, 46, radius=7), stripe, transform(pos=(54, -62), rotation=-24),
               name="stripe"),
        filled(rect(12, 38, radius=6), stripe, transform(pos=(-84, 6), rotation=76),
               name="stripe"),
        filled(rect(12, 38, radius=6), stripe, transform(pos=(84, 6), rotation=-76),
               name="stripe"),
    ]
    return [
        smile(54, 20, y=40, color="#6b4423", w=6),
        filled(triangle(30, 22, pos=(0, 16)), "#d9707f",
               transform(rotation=180), name="nose"),
        filled(ellipse(62, 48, (-28, 40)), cream, name="muzzle"),
        filled(ellipse(62, 48, (28, 40)), cream, name="muzzle"),
        eye((-44, -16), 34, 38, iris="#4a8c3f"), eye((44, -16), 34, 38, iris="#4a8c3f"),
    ] + bars + [
        filled(ellipse(198, 178), coat, name="head"),
        group([filled(ellipse(32, 32), "#f6c7a8", name="inner"),
               filled(ellipse(56, 56), coat, name="outer")],
              wiggle((-70, -72), amp=6, period=26), name="ear"),
        group([filled(ellipse(32, 32), "#f6c7a8", name="inner"),
               filled(ellipse(56, 56), coat, name="outer")],
              wiggle((70, -72), amp=6, period=26, phase=0.5), name="ear"),
    ]


def bear():
    fur, muzzle = "#8a6446", "#d8b48c"
    return [
        smile(46, 18, y=48, color="#4a3428", w=6),
        filled(ellipse(42, 32, (0, 26)), "#3a2a20", name="nose"),
        filled(ellipse(106, 84, (0, 42)), muzzle, name="muzzle"),
        dot_eye((-42, -18), 18), dot_eye((42, -18), 18),
        filled(ellipse(192, 178), fur, name="head"),
        group([filled(ellipse(34, 34), muzzle, name="inner"),
               filled(ellipse(58, 58), fur, name="outer")],
              wiggle((-72, -76), amp=5, period=30), name="ear"),
        group([filled(ellipse(34, 34), muzzle, name="inner"),
               filled(ellipse(58, 58), fur, name="outer")],
              wiggle((72, -76), amp=5, period=30, phase=0.5), name="ear"),
    ]


def rabbit():
    fur, inner, pink = "#ece7df", "#f3b9c4", "#e08fa0"
    ear = lambda x, ph: group(
        [filled(rect(24, 116, (0, -66), radius=12), inner, name="inner"),
         filled(rect(46, 152, (0, -76), radius=23), fur, name="outer")],
        wiggle((x, -54), base_rot=x * 0.16, amp=9, period=26, phase=ph), name="ear")
    whisker = lambda x, y: outlined(path([(0, 0), (x, 0)], closed=False), "#cfc7bc", 4,
                                    transform(pos=(x * 0.5, y)), name="whisker")
    return [
        whisker(66, 32), whisker(70, 44), whisker(-66, 32), whisker(-70, 44),
        filled(rect(28, 24, (0, 12), radius=6), "#ffffff",
               transform(pos=(0, 46)), name="teeth"),
        filled(triangle(24, 18, pos=(0, 8)), pink,
               transform(rotation=180), name="nose"),
        filled(ellipse(52, 42, (-38, 34)), "#f8f4ee", name="cheek"),
        filled(ellipse(52, 42, (38, 34)), "#f8f4ee", name="cheek"),
        eye((-46, -12), 32, 36, iris="#4a3b3b"), eye((46, -12), 32, 36, iris="#4a3b3b"),
        filled(ellipse(176, 162), fur, name="head"),
        ear(-38, 0.0), ear(38, 0.5),
    ]


def mouse():
    fur, pink = "#a9a29b", "#f2b6c0"
    ear = lambda x, ph: group(
        [filled(ellipse(58, 58), pink, name="inner"),
         filled(ellipse(88, 88), fur, name="outer")],
        wiggle((x, -54), amp=6, period=24, phase=ph), name="ear")
    whisker = lambda x, y: outlined(path([(0, 0), (x, 0)], closed=False), "#d8d2cb", 4,
                                    transform(pos=(x * 0.5, y)), name="whisker")
    return [
        whisker(62, 40), whisker(66, 52), whisker(-62, 40), whisker(-66, 52),
        filled(ellipse(24, 20, (0, 44)), pink, name="nose"),
        dot_eye((-32, 2), 16), dot_eye((32, 2), 16),
        filled(ellipse(160, 150), fur, name="head"),
        ear(-78, 0.0), ear(78, 0.5),
    ]


def fox():
    coat, cream, dark = "#e8792b", "#fdf6ec", "#3a2a24"
    ear = lambda x, ph: group(
        [filled(triangle(34, 40, tilt=x * 0.10), dark,
                transform(pos=(0, -40)), name="tip"),
         filled(triangle(72, 84, tilt=x * 0.12), coat, name="outer")],
        wiggle((x, -58), base_rot=x * 0.10, amp=6, period=26, phase=ph), name="ear")
    return [
        filled(triangle(28, 22, pos=(0, 12)), dark,
               transform(rotation=180), name="nose"),
        filled(ellipse(92, 74, (0, 40)), cream, name="muzzle"),
        eye((-42, -16), 32, 36, iris="#5a3a15"), eye((42, -16), 32, 36, iris="#5a3a15"),
        filled(ellipse(72, 52), cream, transform(pos=(-78, 28), rotation=-24),
               name="ruff"),
        filled(ellipse(72, 52), cream, transform(pos=(78, 28), rotation=24),
               name="ruff"),
        filled(ellipse(188, 168), coat, name="head"),
        ear(-58, 0.0), ear(58, 0.5),
    ]


def wolf():
    coat, light = "#7d858d", "#d8dde2"
    ear = lambda x, ph: group(
        [filled(triangle(30, 34, tilt=x * 0.10), "#5c646c",
                transform(pos=(0, -34)), name="tip"),
         filled(triangle(62, 76, tilt=x * 0.12), coat, name="outer")],
        wiggle((x, -62), base_rot=x * 0.12, amp=6, period=28, phase=ph), name="ear")
    return [
        # muzzle lifted and mouth open: mid-howl
        filled(ellipse(38, 30, (0, 22)), "#2b3138", name="nose"),
        filled(ellipse(44, 34, (0, 62)), "#3a2f33",
               transform(scale=animated([(0, [100, 60]), (18, [100, 120]),
                                         (40, [100, 96]), (FRAMES, [100, 60])])),
               name="mouth"),
        filled(ellipse(96, 92, (0, 44)), light, name="snout"),
        eye((-44, -20), 32, 34, iris="#e0a92e"), eye((44, -20), 32, 34, iris="#e0a92e"),
        filled(ellipse(184, 174), coat, name="head"),
        ear(-58, 0.0), ear(58, 0.5),
    ]


def rooster():
    body, red, beak = "#efe8dc", "#d94f3d", "#f5b02a"
    comb = group([filled(ellipse(40, 40, (-32, 6)), red, name="bump"),
                  filled(ellipse(46, 46, (0, -6)), red, name="bump"),
                  filled(ellipse(40, 40, (32, 6)), red, name="bump")],
                 wiggle((0, -92), amp=5, period=26), name="comb")
    return [
        filled(ellipse(24, 40, (-14, 20)), red, name="wattle"),
        filled(ellipse(24, 40, (14, 20)), red, name="wattle"),
        filled(triangle(52, 36), beak,
               transform(pos=(0, 30), rotation=180,
                         scale=animated([(0, [100, 100]), (12, [104, 126]),
                                         (26, [100, 100]), (FRAMES, [100, 100])])),
               name="beak"),
        dot_eye((-36, -18), 17), dot_eye((36, -18), 17),
        filled(ellipse(172, 166), body, name="head"),
        comb,
    ]


def goat():
    coat, horn, muzzle = "#f2ece1", "#cbbba4", "#e2d7c6"
    return [
        filled(triangle(50, 62), "#ded2c0",
               wiggle((0, 96), base_rot=180, amp=5, period=32), name="beard"),
        nostrils(20, 62, 16, 12, "#a08d76"),
        filled(ellipse(96, 78, (0, 56)), muzzle, name="muzzle"),
        eye((-44, -34), 40, 36, white="#fbf3dd"),
        eye((44, -34), 40, 36, white="#fbf3dd"),
        filled(ellipse(152, 184), coat, name="head"),
        filled(ellipse(78, 34), coat,
               wiggle((-84, -26), base_rot=-24, amp=7, period=28), name="ear"),
        filled(ellipse(78, 34), coat,
               wiggle((84, -26), base_rot=24, amp=7, period=28, phase=0.5), name="ear"),
        filled(triangle(26, 76, tilt=-22), horn,
               transform(pos=(-38, -80), rotation=-18), name="horn"),
        filled(triangle(26, 76, tilt=22), horn,
               transform(pos=(38, -80), rotation=18), name="horn"),
    ]


def donkey():
    coat, muzzle, mane = "#9b9086", "#d6cfc6", "#5d554e"
    ear = lambda x, ph: group(
        [filled(rect(24, 100, (0, -58), radius=12), "#b3a89d", name="inner"),
         filled(rect(46, 134, (0, -66), radius=23), coat, name="outer")],
        wiggle((x, -62), base_rot=x * 0.20, amp=8, period=27, phase=ph), name="ear")
    return [
        nostrils(24, 62, 20, 15, "#8a8078"),
        filled(ellipse(110, 88, (0, 56)), muzzle, name="muzzle"),
        eye((-44, -36), 32, 34), eye((44, -36), 32, 34),
        tuft(0, -90, 3, mane, w=22, h=42, spread=18),
        filled(ellipse(150, 186), coat, name="head"),
        ear(-42, 0.0), ear(42, 0.5),
    ]


def panda():
    white, black = "#f7f4ee", "#2b2b2b"
    patch = lambda x: group(
        [dot_eye((0, 0), 15),
         filled(ellipse(66, 78), black, transform(rotation=x * 0.16), name="patch")],
        transform(pos=(x, -10)), name="eye-patch")
    return [
        smile(48, 18, y=52, color="#4a4a4a", w=6),
        filled(ellipse(40, 32, (0, 30)), black, name="nose"),
        patch(-46), patch(46),
        filled(ellipse(196, 178), white, name="head"),
        filled(ellipse(58, 58), black,
               wiggle((-74, -74), amp=5, period=30), name="ear"),
        filled(ellipse(58, 58), black,
               wiggle((74, -74), amp=5, period=30, phase=0.5), name="ear"),
    ]


def koala():
    fur, fluff = "#9aa0a6", "#d3d8dc"
    ear = lambda x, ph: group(
        [filled(ellipse(70, 70), fluff, name="inner"),
         filled(ellipse(108, 108), fur, name="outer")],
        wiggle((x, -28), amp=5, period=30, phase=ph), name="ear")
    return [
        filled(ellipse(54, 68, (0, 30)), "#3c3f43", name="nose"),
        dot_eye((-42, -18), 17), dot_eye((42, -18), 17),
        filled(ellipse(178, 166), fur, name="head"),
        ear(-86, 0.0), ear(86, 0.5),
    ]


def giraffe():
    coat, spot, muzzle = "#f0c169", "#b57a2e", "#f7dcae"
    ossicone = lambda x: group(
        [filled(ellipse(26, 26, (0, -44)), "#8a5f22", name="knob"),
         filled(rect(14, 46, (0, -22), radius=7), coat, name="stalk")],
        wiggle((x, -84), base_rot=x * 0.12, amp=5, period=30,
               phase=0.0 if x < 0 else 0.5), name="ossicone")
    return [
        nostrils(22, 66, 18, 13, "#c69a5a"),
        filled(ellipse(100, 80, (0, 60)), muzzle, name="muzzle"),
        eye((-42, -44), 32, 36, iris="#4a3116"), eye((42, -44), 32, 36, iris="#4a3116"),
        filled(ellipse(34, 30, (-42, 8)), spot, name="spot"),
        filled(ellipse(30, 28, (40, -8)), spot, name="spot"),
        filled(ellipse(26, 24, (6, 24)), spot, name="spot"),
        filled(ellipse(132, 194), coat, name="head"),
        filled(ellipse(56, 30), coat,
               wiggle((-76, -66), base_rot=-28, amp=6, period=28), name="ear"),
        filled(ellipse(56, 30), coat,
               wiggle((76, -66), base_rot=28, amp=6, period=28, phase=0.5), name="ear"),
        ossicone(-30), ossicone(30),
    ]


def hippo():
    hide, muzzle = "#a98bb5", "#c9aed2"
    return [
        smile(84, 18, y=64, color="#8a6d96", w=6),
        nostrils(40, 20, 26, 18, "#7d6289"),
        filled(ellipse(172, 116, (0, 44)), muzzle, name="muzzle"),
        eye((-58, -50), 34, 36), eye((58, -50), 34, 36),
        filled(ellipse(216, 162), hide, name="head"),
        filled(ellipse(40, 30), hide,
               wiggle((-74, -70), amp=6, period=30), name="ear"),
        filled(ellipse(40, 30), hide,
               wiggle((74, -70), amp=6, period=30, phase=0.5), name="ear"),
    ]


def crocodile():
    skin, jaw_dark = "#5f9e56", "#4a8543"
    # Eyes ride on top of the skull, the way a croc watches from the water.
    dome = lambda x: group(
        [eye((0, 0), 32, 34, iris="#2f2a26"),
         filled(ellipse(58, 56), skin, name="dome")],
        transform(pos=(x, -74)), name="eyedome")
    snout = group(
        [teeth(6, -32, 122, 15),
         filled(rect(162, 88, radius=32), jaw_dark, name="jaw")],
        transform(pos=(0, 44),
                  rotation=animated([(0, 0), (12, 6), (24, 0), (36, 6), (48, 0),
                                     (FRAMES, 0)])),
        name="snout")
    return [
        nostrils(30, -6, 20, 14, "#33632e"),
        dome(-56), dome(56),
        snout,
        filled(ellipse(190, 130, (0, -14)), skin, name="skull"),
    ]


def snake():
    skin, dark, tongue = "#6fbf4a", "#3f8a2a", "#e2495b"
    flick = group(
        [filled(path([(-24, 34), (0, 8), (24, 34), (0, 22)]), tongue, name="fork"),
         outlined(path([(0, 0), (0, 18)], closed=False), tongue, 7, name="stem")],
        transform(pos=(0, -18),
                  scale=animated([(0, [100, 15]), (10, [100, 110]), (20, [100, 45]),
                                  (30, [100, 110]), (44, [100, 15]),
                                  (FRAMES, [100, 15])])),
        name="tongue")
    return [
        flick,
        eye((-34, -80), 32, 36, white="#f2d64f"),
        eye((34, -80), 32, 36, white="#f2d64f"),
        filled(ellipse(130, 106, (0, -70)), skin, name="head"),
        # two stroked ellipses read as a body coiled under the raised head
        outlined(ellipse(104, 54, (0, 54)), dark, 30, name="coil-inner"),
        outlined(ellipse(212, 122, (0, 46)), skin, 40, name="coil-outer"),
    ]


def parrot():
    feather, cheek, beak = "#3fb56a", "#f5c33b", "#f0a52a"
    return [
        filled(path([(-16, -8), (16, -8), (10, 16), (-10, 16)]), "#c96a13",
               transform(pos=(0, 50),
                         rotation=animated([(0, 0), (12, 14), (24, 0), (36, 14),
                                            (48, 0), (FRAMES, 0)])),
               name="lower-beak"),
        # hooked upper mandible: wide at the brow, curling to a point
        filled(path([(-28, -20), (28, -20), (20, 12), (4, 34), (-8, 16), (-22, 8)]),
               beak, transform(pos=(0, 28)), name="upper-beak"),
        filled(ellipse(34, 30, (-58, 4)), cheek, name="cheek"),
        filled(ellipse(34, 30, (58, 4)), cheek, name="cheek"),
        eye((-44, -26), 34, 36, iris="#2b2118"), eye((44, -26), 34, 36, iris="#2b2118"),
        filled(ellipse(178, 170), feather, name="head"),
        tuft(0, -86, 3, "#e8483c", w=26, h=54, spread=24),
    ]


SET_B = {
    "horse": horse, "elephant": elephant, "monkey": monkey, "penguin": penguin,
    "tiger": tiger, "bear": bear, "rabbit": rabbit, "mouse": mouse,
    "fox": fox, "wolf": wolf, "rooster": rooster, "goat": goat,
    "donkey": donkey, "panda": panda, "koala": koala, "giraffe": giraffe,
    "hippo": hippo, "crocodile": crocodile, "snake": snake, "parrot": parrot,
}
