"""Twenty-five more critters: set D."""

import math

from critter_parts import (
    dot_eye, eye, pin_eye, smile, triangle, wiggle,
)
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def seal():
    body_c, belly_c = "#78909C", "#CFD8DC"
    whisker = lambda x, y, rot: outlined(path([(0, 0), (x, 0)], False), "#B0BEC5", 2, transform(pos=(30, y), rotation=rot))
    return [
        whisker(30, 30, 10), whisker(30, 40, 0), whisker(-30, 30, -10), whisker(-30, 40, 0),
        filled(ellipse(20, 15, (0, 20)), "#263238", name="nose"),
        dot_eye((-40, -10), 14), dot_eye((40, -10), 14),
        filled(ellipse(190, 150), body_c, name="body"),
        filled(ellipse(60, 30, (-90, 50)), body_c, transform(rotation=20), name="flipper"),
        filled(ellipse(60, 30, (90, 50)), body_c, transform(rotation=-20), name="flipper"),
    ]


def sloth():
    fur_c, face_c = "#795548", "#D7CCC8"
    patch = lambda x: filled(ellipse(64, 82, (x, 0)), "#5D4037", transform(rotation=x*0.2), name="patch")
    return [
        dot_eye((-45, 0), 12), dot_eye((45, 0), 12),
        patch(-45), patch(45),
        filled(ellipse(140, 120), face_c, name="face"),
        filled(ellipse(180, 160), fur_c, name="head"),
    ]


def spider():
    body_c = "#000000"
    legs = []
    for i in range(4):
        y = i * 20 - 30
        legs.append(outlined(path([(-60, y), (-100, y - 20)], False), body_c, 6, name="leg"))
        legs.append(outlined(path([(60, y), (100, y - 20)], False), body_c, 6, name="leg"))
    eyes = group([pin_eye((x, y), 13, color="#FFFFFF")
                  for x, y in [(-34, -34), (0, -40), (34, -34),
                               (-16, -14), (16, -14)]], name="eyes")
    return legs + [
        eyes,
        filled(ellipse(140, 140), body_c, name="body"),
    ]


def toucan():
    body_c, beak_c = "#212121", "#FFAB00"
    beak = group([filled(path([(0, 0), (120, 0), (100, 60), (0, 40)], True), beak_c, name="beak-main"),
                  filled(ellipse(30, 30, (20, 10)), "#D32F2F", name="spot")],
                 transform(pos=(0, 0)), name="beak")
    return [
        beak,
        dot_eye((-40, -20), 15, color="#FFFFFF"), dot_eye((40, -20), 15, color="#FFFFFF"),
        filled(ellipse(160, 160), body_c, name="head"),
    ]


def walrus():
    body_c, tusk_c = "#5D4037", "#F5F5F5"
    tusks = group([filled(triangle(20, 60), tusk_c, transform(pos=(x, 40), rotation=180)) for x in [-30, 30]], name="tusks")
    return [
        tusks,
        smile(80, 15, y=30, color="#3E2723", w=4),
        dot_eye((-50, -20), 16), dot_eye((50, -20), 16),
        filled(ellipse(210, 170), body_c, name="body"),
    ]


def bat():
    fur, membrane, bone = "#37474F", "#2E3B43", "#7A8F99"
    ear_in, muzzle_c, deep = "#4A2F38", "#455A64", "#1C252A"

    # A bat wing is an arm: one bone out to the wrist, then four fingers with
    # the membrane scalloped between their tips. The old wing was a flat
    # ellipse squashed on the y axis, which read as a lump rather than a flap.
    wrist = (52, -40)
    tips = [(104, -52), (112, 6), (96, 50), (70, 80)]
    outline = [(0, -10), wrist, (104, -52), (84, -12), (112, 6), (82, 24),
               (96, 50), (66, 48), (70, 80), (16, 52), (0, 18)]

    def wing(mirror, phase):
        struts = [outlined(path([(4, -8), wrist], closed=False), bone, 5,
                           name="arm"),
                  outlined(path([wrist, (64, -62)], closed=False), bone, 4,
                           name="thumb")]
        struts += [outlined(path([wrist, t], closed=False), bone, 3,
                            name="finger") for t in tips]
        # the whole wing swings from the shoulder; the left one is the same
        # drawing mirrored, so both flap in step the way a bat's do
        return group(
            struts + [outlined(path(outline), bone, 3, name="edge"),
                      filled(path(outline), membrane, name="membrane")],
            wiggle((46 * mirror, -6), base_rot=-8 * mirror, amp=20 * mirror,
                   period=18, phase=phase, scale=(100 * mirror, 100)),
            name="wing")

    def ear(x, phase):
        return group(
            [filled(triangle(30, 52, pos=(0, -6)), ear_in, name="inner"),
             filled(triangle(54, 80), fur, name="outer")],
            wiggle((x, -44), base_rot=x * 0.32, amp=5, period=34, phase=phase),
            name="ear")

    fangs = group(
        [filled(triangle(11, 16, pos=(-12, 0)), "#F7F7F2", name="fang"),
         filled(triangle(11, 16, pos=(12, 0)), "#F7F7F2", name="fang")],
        transform(pos=(0, 44), rotation=180), name="fangs")

    return [
        fangs,
        smile(46, 10, y=34, color=deep, w=5),
        filled(triangle(20, 15), deep,
               transform(pos=(0, 22), rotation=180), name="nose"),
        filled(ellipse(78, 58, (0, 32)), muzzle_c, name="muzzle"),
        dot_eye((-32, -18), 10, color="#FFFFFF"),
        dot_eye((32, -18), 10, color="#FFFFFF"),
        filled(ellipse(150, 128), fur, name="head"),
        ear(-44, 0.0), ear(44, 0.5),
        wing(-1, 0.0), wing(1, 0.0),
    ]


def beaver():
    fur, dark, tail_c, deep = "#5D4037", "#3E2723", "#2B1B17", "#1A1412"

    # Flat paddle tail. It sits behind the head and only shows below the chin -
    # in front of the face it just hid everything.
    paddle = filled(ellipse(78, 116), tail_c,
                    wiggle((36, 88), base_rot=-22, amp=10, period=40),
                    name="tail")

    # The buck teeth a beaver is known for: two big incisors hanging out of a
    # dark mouth, below the nose.
    mouth = filled(rect(66, 26, (0, 46), radius=10), deep, name="mouth")
    incisors = group(
        [filled(rect(22, 32, (-12, 0), radius=5), "#FFFFFF", name="tooth"),
         filled(rect(22, 32, (12, 0), radius=5), "#FFFFFF", name="tooth")],
        transform(pos=(0, 58)), name="teeth")

    # Whiskers, pale enough to read against the fur they lie on
    whisker = lambda x, y, rot: outlined(path([(0, 0), (x, 0)], closed=False), "#D7CCC8", 3,
                                       transform(pos=(x * 0.4 + (44 if x > 0 else -44), y), rotation=rot), name="whisker")
    whiskers = [
        whisker(50, 24, -10), whisker(54, 36, 0), whisker(50, 48, 10),
        whisker(-50, 24, 10), whisker(-54, 36, 0), whisker(-50, 48, -10)
    ]

    return whiskers + [
        incisors,
        mouth,
        filled(ellipse(36, 26, (0, 14)), deep, name="nose"),
        filled(ellipse(118, 92, (0, 36)), "#4E3629", name="muzzle"), # Darker snout area
        dot_eye((-44, -14), 16), dot_eye((44, -14), 16),
        filled(ellipse(186, 172), fur, name="head"),
        group([filled(ellipse(44, 44), fur, name="outer"),
               filled(ellipse(28, 28), dark, name="inner")],
              wiggle((-76, -64), amp=5, period=32), name="ear"),
        group([filled(ellipse(44, 44), fur, name="outer"),
               filled(ellipse(28, 28), dark, name="inner")],
              wiggle((76, -64), amp=5, period=32, phase=0.5), name="ear"),
        paddle,
    ]


def cheetah():
    fur, spot, cream = "#FBC02D", "#212121", "#FFF9C4"
    # Malar stripes (teardrop marks) from eyes to mouth corners
    teardrops = [
        outlined(path([(-24, -10), (-26, 12), (-24, 38)], closed=False), spot, 5, name="teardrop"),
        outlined(path([(24, -10), (26, 12), (24, 38)], closed=False), spot, 5, name="teardrop")
    ]
    # Small solid black spots distributed across the head
    spots_pos = [
        (-60, 20), (60, 20), (0, -60), (-35, -55), (35, -55),
        (-75, -20), (75, -20), (-45, 45), (45, 45), (0, 75),
        (-30, 0), (30, 0), (0, -25)
    ]
    spots = [filled(ellipse(10, 10, pos), spot, name="spot") for pos in spots_pos]

    ear = lambda x, ph: group(
        [filled(ellipse(28, 28), spot, name="inner"),
         filled(ellipse(50, 50), fur, name="outer")],
        wiggle((x, -70), base_rot=x * 0.1, amp=6, period=28, phase=ph), name="ear")

    return [
        smile(52, 18, y=38, color="#7F6D00", w=5),
        filled(triangle(26, 18, pos=(0, 15)), "#D81B60", transform(rotation=180), name="nose"),
        filled(ellipse(96, 78, (0, 42)), cream, name="muzzle"),
        eye((-42, -18), 34, 36, iris=spot),
        eye((42, -18), 34, 36, iris=spot),
    ] + teardrops + spots + [
        filled(ellipse(194, 178), fur, name="head"),
        ear(-72, 0.0), ear(72, 0.5)
    ]


def dinosaur():
    skin_c = "#2E7D32"
    arms = [filled(rect(20, 10, (x, 40), radius=5), skin_c) for x in [-40, 40]]
    return arms + [
        smile(60, 20, y=20, color="#1B5E20", w=5),
        dot_eye((-40, -30), 15), dot_eye((40, -30), 15),
        filled(ellipse(180, 140, (0, 0)), skin_c, name="head"),
        filled(ellipse(120, 180, (0, 80)), skin_c, name="body"),
    ]


def gorilla():
    fur_c, skin_c = "#212121", "#424242"
    return [
        filled(ellipse(120, 80, (0, 40)), skin_c, name="chest"),
        eye((-40, -30), 34, 38, iris="#000000"), eye((40, -30), 34, 38, iris="#000000"),
        filled(ellipse(200, 180), fur_c, name="head"),
    ]


def jellyfish():
    body_c = "#CE93D8"
    tentacles = [outlined(path([(x, 40), (x, 100 + 20 * math.sin(x))], False), body_c, 5,
                          wiggle((0, 0), amp=10, period=30, phase=x*0.1)) for x in range(-60, 61, 30)]
    return tentacles + [
        filled(ellipse(160, 100), body_c, transform(opacity=70), name="dome"),
        dot_eye((-30, 0), 10, color="#4A148C"), dot_eye((30, 0), 10, color="#4A148C"),
    ]


def lemur():
    fur_c, tail_c = "#9E9E9E", "#424242"
    tail = group([filled(rect(30, 20, (0, i*20)), (tail_c if i % 2 == 0 else "#FFFFFF")) for i in range(6)],
                 wiggle((100, 40), base_rot=30, amp=10, period=40), name="tail")
    return [
        tail,
        eye((-45, -10), 40, 44, iris="#FFD54F", white="#212121"), eye((45, -10), 40, 44, iris="#FFD54F", white="#212121"),
        filled(ellipse(170, 160), fur_c, name="head"),
    ]


def leopard():
    fur, pale, spot = "#E9A13B", "#F7E4C8", "#3E2723"
    rose_c, deep = "#C97A20", "#2A1B14"

    def rosette(x, y, r):
        """A leopard's spot is a broken ring of flecks round a darker centre,
        not the single outlined circle this used to draw."""
        flecks = [filled(ellipse(r * 0.5, r * 0.5,
                                 (r * math.cos(a), r * math.sin(a))), spot,
                         name="fleck")
                  for a in (0.5, 1.6, 2.7, 3.8, 4.9, 6.0)]
        return group(flecks + [filled(ellipse(r * 1.5, r * 1.5), rose_c,
                                      name="centre")],
                     transform(pos=(x, y)), name="rosette")

    def ear(x, phase):
        return group([filled(ellipse(34, 30, (0, 4)), pale, name="inner"),
                      filled(ellipse(52, 48), fur, name="outer"),
                      filled(ellipse(62, 58), spot, name="back")],
                     wiggle((x, -68), base_rot=x * 0.16, amp=5, period=32,
                            phase=phase), name="ear")

    def whisker(x, y, tilt):
        return outlined(path([(0, 0), (x, tilt)], closed=False), "#FBEFDC", 4,
                        transform(pos=(x * 0.58, y)), name="whisker")

    # the rosettes keep clear of the eyes, muzzle and ears
    rosettes = [rosette(x, y, r) for x, y, r in
                ((-50, -60, 15), (50, -60, 14), (-66, -12, 15), (66, -10, 14),
                 (0, -62, 13), (-62, 34, 14), (62, 32, 13))]
    # small solid flecks where the whiskers grow
    flecks = [filled(ellipse(9, 9, (x, y)), deep, name="fleck")
              for x, y in ((-58, 20), (-46, 34), (58, 20), (46, 34))]

    return [
        whisker(62, 4, -12), whisker(68, 16, 2), whisker(62, 28, 14),
        whisker(-62, 4, -12), whisker(-68, 16, 2), whisker(-62, 28, 14),
    ] + flecks + [
        smile(48, 15, y=48, color=deep, w=5),
        filled(triangle(26, 19, pos=(0, 9)), "#C4626F",
               transform(pos=(0, 24), rotation=180), name="nose"),
        filled(ellipse(58, 44, (-24, 44)), pale, name="muzzle"),
        filled(ellipse(58, 44, (24, 44)), pale, name="muzzle"),
        eye((-46, -18), 34, 38, iris="#D9A227"),
        eye((46, -18), 34, 38, iris="#D9A227"),
    ] + rosettes + [
        filled(ellipse(182, 172), fur, name="head"),
        ear(-76, 0.0), ear(76, 0.5),
    ]
def otter():
    fur_c = "#795548"
    return [
        smile(40, 10, y=30, color="#3E2723", w=3),
        filled(ellipse(20, 15, (0, 20)), "#212121", name="nose"),
        dot_eye((-40, -10), 14), dot_eye((40, -10), 14),
        filled(ellipse(170, 150), fur_c, name="head"),
        filled(ellipse(50, 30, (-80, 50)), fur_c, transform(rotation=30), name="flipper"),
        filled(ellipse(50, 30, (80, 50)), fur_c, transform(rotation=-30), name="flipper"),
    ]


def pelican():
    body_c, pouch_c = "#CFD8DC", "#FFD54F"
    return [
        filled(ellipse(100, 60, (40, 30)), pouch_c, name="pouch"),
        filled(path([(0, 0), (100, 0), (80, 20), (0, 20)], True), "#FFB300", transform(pos=(0, 10)), name="beak"),
        dot_eye((-30, -20), 12), dot_eye((30, -20), 12),
        filled(ellipse(150, 140), body_c, name="head"),
    ]


def platypus():
    fur_c, bill_c = "#4E342E", "#212121"
    return [
        filled(ellipse(80, 40, (40, 20)), bill_c, name="bill"),
        dot_eye((-30, -10), 12, color="#FFFFFF"), dot_eye((30, -10), 12, color="#FFFFFF"),
        filled(ellipse(160, 130), fur_c, name="head"),
        filled(ellipse(60, 30, (-80, 40)), bill_c, transform(rotation=20), name="foot"),
        filled(ellipse(60, 30, (80, 40)), bill_c, transform(rotation=-20), name="foot"),
    ]


def polar_bear():
    fur_c = "#FFFFFF"
    return [
        smile(46, 18, y=48, color="#B0BEC5", w=5),
        filled(ellipse(42, 32, (0, 26)), "#263238", name="nose"),
        dot_eye((-45, -20), 18), dot_eye((45, -20), 18),
        filled(ellipse(190, 180), fur_c, name="head"),
        filled(ellipse(50, 50), fur_c, wiggle((-70, -75)), name="ear"),
        filled(ellipse(50, 50), fur_c, wiggle((70, -75), phase=0.5), name="ear"),
    ]


def porcupine():
    body_c, spike_c = "#455A64", "#90A4AE"
    spikes = group([outlined(path([(0, 0), (x, y)], False), spike_c, 3) for x, y in [(-80, -80), (-40, -100), (0, -110), (40, -100), (80, -80)]],
                   wiggle((0, 0), amp=5, period=30), name="spikes")
    return [
        spikes,
        dot_eye((-35, -10), 12, color="#FFFFFF"), dot_eye((35, -10), 12, color="#FFFFFF"),
        filled(ellipse(170, 150), body_c, name="body"),
        filled(ellipse(20, 20, (0, 10)), "#212121", name="nose"),
    ]


def raccoon():
    fur_c, mask_c = "#616161", "#212121"
    mask = group([filled(ellipse(76, 58, (x, -10)), mask_c, transform(rotation=x*0.2)) for x in [-45, 45]], name="mask")
    return [
        dot_eye((-45, -10), 12, color="#FFFFFF"), dot_eye((45, -10), 12, color="#FFFFFF"),
        mask,
        filled(ellipse(180, 160), fur_c, name="head"),
        filled(triangle(40, 50), fur_c, wiggle((-60, -70), base_rot=-20), name="ear"),
        filled(triangle(40, 50), fur_c, wiggle((60, -70), base_rot=20, phase=0.5), name="ear"),
    ]


def red_panda():
    fur_c, face_c = "#D84315", "#FFFFFF"
    return [
        filled(ellipse(50, 40, (-60, 20)), face_c, name="patch"),
        filled(ellipse(50, 40, (60, 20)), face_c, name="patch"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(180, 160), fur_c, name="head"),
        filled(triangle(40, 50), fur_c, wiggle((-65, -70), base_rot=-20), name="ear"),
        filled(triangle(40, 50), fur_c, wiggle((65, -70), base_rot=20, phase=0.5), name="ear"),
    ]


def snail():
    shell_c, skin_c = "#8D6E63", "#F5F5F5"
    shell = group([outlined(ellipse(i*20, i*20), "#5D4037", 4) for i in range(1, 5)], name="spiral")
    return [
        shell,
        filled(ellipse(120, 120), shell_c, name="shell"),
        outlined(path([(-20, -40), (-40, -80)], False), skin_c, 4, name="stalk"),
        outlined(path([(20, -40), (40, -80)], False), skin_c, 4, name="stalk"),
        dot_eye((-40, -80), 8), dot_eye((40, -80), 8),
        filled(ellipse(160, 40, (0, 40)), skin_c, name="body"),
    ]


def squid():
    body_c = "#EC407A"
    tentacles = [filled(rect(15, 80, radius=7), body_c,
                        wiggle((x, 60), base_rot=0, amp=15, period=30, phase=x*0.1)) for x in range(-50, 51, 25)]
    return tentacles + [
        eye((-40, 10), 34, 38, iris="#880E4F"), eye((40, 10), 34, 38, iris="#880E4F"),
        filled(path([(-80, 20), (0, -100), (80, 20)], True), body_c, name="head"),
    ]


def starfish():
    body_c = "#FF7043"
    points = [filled(triangle(40, 100), body_c, transform(rotation=72*i, pos=(80*math.sin(math.radians(72*i)), -80*math.cos(math.radians(72*i))))) for i in range(5)]
    return points + [
        dot_eye((-20, -10), 10, color="#FFFFFF"), dot_eye((20, -10), 10, color="#FFFFFF"),
        filled(ellipse(80, 80), body_c, name="body"),
    ]


def swan():
    body_c, beak_c = "#FAFAFA", "#FF9800"
    return [
        filled(triangle(30, 40), beak_c, transform(pos=(0, -50), rotation=180), name="beak"),
        dot_eye((-20, -75), 10), dot_eye((20, -75), 10),
        filled(ellipse(90, 80, (0, -75)), body_c, name="head"),
        outlined(path([(0, -40), (0, 60)], False), body_c, 30, name="neck"),
        filled(ellipse(180, 120, (0, 80)), body_c, name="body"),
    ]


def turkey():
    body_c, red_c = "#BF360C", "#D32F2F"
    fan = group([filled(ellipse(50, 120, (120*math.cos(math.radians(a)), 120*math.sin(math.radians(a)))), "#795548", transform(rotation=a+90))
                 for a in range(-120, 121, 30)], name="fan")
    return [
        fan,
        filled(ellipse(20, 40, (15, 20)), red_c, name="wattle"),
        filled(triangle(30, 25), "#FFD54F", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-35, -15), 15), dot_eye((35, -15), 15),
        filled(ellipse(160, 150), body_c, name="head"),
    ]


SET_D = {
    "seal": seal, "sloth": sloth, "spider": spider, "toucan": toucan,
    "walrus": walrus, "bat": bat, "beaver": beaver, "cheetah": cheetah,
    "dinosaur": dinosaur, "gorilla": gorilla, "jellyfish": jellyfish,
    "lemur": lemur, "leopard": leopard, "otter": otter, "pelican": pelican,
    "platypus": platypus, "polar_bear": polar_bear, "porcupine": porcupine,
    "raccoon": raccoon, "red_panda": red_panda, "snail": snail, "squid": squid,
    "starfish": starfish, "swan": swan, "turkey": turkey,
}
