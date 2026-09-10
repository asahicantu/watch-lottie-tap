"""The fifth ten critters: more exotic and wild animals."""

import math

from critter_parts import (
    FRAMES, critter, dot_eye, eye, oscillate, smile, triangle, wiggle,
)
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform


def ant():
    body = "#B22222"
    def leg(x, y, rotation):
        return outlined(path([(0, 0), (x, y)], closed=False), body, 6,
                        wiggle((0, 0), base_rot=rotation, amp=10, period=20), name="leg")

    return [
        dot_eye((-30, -10), 12), dot_eye((30, -10), 12),
        filled(ellipse(100, 80), body, name="head"),
        leg(-60, 40, -30), leg(60, 40, 30),
        leg(-60, 0, -10), leg(60, 0, 10),
        group([filled(ellipse(20, 40, (0, -20)), body)],
              wiggle((-20, -40), base_rot=-20, amp=15, period=25), name="antenna"),
        group([filled(ellipse(20, 40, (0, -20)), body)],
              wiggle((20, -40), base_rot=20, amp=15, period=25, phase=0.5), name="antenna"),
    ]


def buffalo():
    body, horns = "#5D4037", "#D7CCC8"
    return [
        filled(ellipse(130, 90, (0, 40)), "#3E2723", name="muzzle"),
        dot_eye((-45, -10), 15), dot_eye((45, -10), 15),
        filled(ellipse(200, 180), body, name="head"),
        filled(path([(0, 0), (-40, -20), (-60, -60), (0, -40)], closed=True), horns,
               transform(pos=(-70, -60)), name="horn"),
        filled(path([(0, 0), (40, -20), (60, -60), (0, -40)], closed=True), horns,
               transform(pos=(70, -60)), name="horn"),
    ]


def hen():
    body, comb = "#FFB74D", "#E53935"
    return [
        filled(triangle(30, 40), "#FDD835", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-35, -20), 12), dot_eye((35, -20), 12),
        filled(ellipse(160, 160), body, name="head"),
        filled(ellipse(40, 60, (0, -80)), comb, wiggle((0, 0), amp=5, period=30), name="comb"),
        filled(ellipse(30, 50, (-30, -70)), comb, wiggle((0, 0), amp=5, period=30, phase=0.3), name="comb"),
        filled(ellipse(30, 50, (30, -70)), comb, wiggle((0, 0), amp=5, period=30, phase=0.6), name="comb"),
    ]


def dragon():
    body, belly = "#4CAF50", "#C8E6C9"
    return [
        filled(triangle(40, 50), "#FFD54F", transform(pos=(0, 40), rotation=180), name="snout"),
        eye((-45, -20), 40, 45, iris="#E65100"),
        eye((45, -20), 40, 45, iris="#E65100"),
        filled(ellipse(200, 180), body, name="head"),
        filled(triangle(30, 40), "#388E3C", transform(pos=(-60, -80), rotation=-20), name="spike"),
        filled(triangle(30, 40), "#388E3C", transform(pos=(0, -95)), name="spike"),
        filled(triangle(30, 40), "#388E3C", transform(pos=(60, -80), rotation=20), name="spike"),
    ]


def goldfish():
    body = "#FF9800"
    def fin(pos, rot, phase):
        return filled(ellipse(60, 40), "#FB8C00",
                      wiggle(pos, base_rot=rot, amp=20, period=20, phase=phase), name="fin")

    return [
        eye((-50, -10), 45, 45, iris="#000000"),
        eye((50, -10), 45, 45, iris="#000000"),
        filled(ellipse(180, 160), body, name="body"),
        fin((-80, 40), 30, 0), fin((80, 40), -30, 0.5),
        filled(ellipse(100, 120, (0, 80)), body, wiggle((0, 0), amp=10, period=30), name="tail"),
    ]


def hyena():
    body, spot = "#A1887F", "#5D4037"
    return [
        smile(50, 20, y=40, color="#3E2723"),
        filled(ellipse(40, 30, (0, 20)), "#212121", name="nose"),
        eye((-40, -15), 34, 38, iris="#FFD54F"),
        eye((40, -15), 34, 38, iris="#FFD54F"),
        filled(ellipse(180, 160), body, name="head"),
        filled(ellipse(40, 40, (-50, 40)), spot, name="spot"),
        filled(ellipse(30, 30, (60, -40)), spot, name="spot"),
        filled(ellipse(80, 100), body, wiggle((-70, -70), base_rot=-30, amp=10, period=25), name="ear"),
        filled(ellipse(80, 100), body, wiggle((70, -70), base_rot=30, amp=10, period=25, phase=0.5), name="ear"),
    ]


def iguana():
    body = "#8BC34A"
    return [
        dot_eye((-50, -10), 15), dot_eye((50, -10), 15),
        filled(ellipse(220, 140), body, name="head"),
        filled(ellipse(30, 30, (0, 60)), "#689F38", name="dewlap"),
        group([filled(triangle(15, 20), "#689F38") for i in range(5)],
              transform(pos=(0, -70)), name="spikes"),
    ]


def kiwi():
    body = "#795548"
    return [
        outlined(path([(0, 0), (0, 80)], closed=False), "#D7CCC8", 6,
                 transform(pos=(0, 20), rotation=-10), name="beak"),
        dot_eye((-20, -10), 10), dot_eye((20, -10), 10),
        filled(ellipse(140, 160), body, name="body"),
    ]


def moose():
    body, antlers = "#6D4C41", "#D7CCC8"
    def antler(x, phase):
        return group([filled(rect(80, 40, (x*0.5, -40), radius=20), antlers),
                      filled(rect(20, 60, (0, -20)), antlers)],
                     wiggle((x, -70), base_rot=x*0.2, amp=10, period=40, phase=phase), name="antler")

    return [
        filled(ellipse(120, 100, (0, 50)), "#4E342E", name="muzzle"),
        dot_eye((-40, -20), 16), dot_eye((40, -20), 16),
        filled(ellipse(190, 170), body, name="head"),
        antler(-80, 0), antler(80, 0.5),
    ]


def narwhal():
    body = "#90A4AE"
    return [
        filled(triangle(20, 100), "#ECEFF1", transform(pos=(0, -70)), name="tusk"),
        dot_eye((-50, 10), 12), dot_eye((50, 10), 12),
        filled(ellipse(200, 150), body, name="body"),
    ]


def orca():
    body, white = "#212121", "#FFFFFF"
    return [
        filled(ellipse(60, 30, (-60, -20)), white, name="patch"),
        filled(ellipse(60, 30, (60, -20)), white, name="patch"),
        dot_eye((-50, 10), 15), dot_eye((50, 10), 15),
        filled(ellipse(220, 160), body, name="body"),
        filled(triangle(40, 80), body, wiggle((0, -80), amp=5, period=40), name="fin"),
    ]


def pigeon():
    body, neck = "#9E9E9E", "#7E57C2"
    return [
        filled(triangle(20, 25), "#424242", transform(pos=(0, 20), rotation=180), name="beak"),
        eye((-35, -15), 30, 30, iris="#FF5722"),
        eye((35, -15), 30, 30, iris="#FF5722"),
        filled(ellipse(150, 150), body, name="head"),
        filled(ellipse(100, 40, (0, 60)), neck, transform(opacity=50), name="neck-sheen"),
    ]


def reindeer():
    body, antlers = "#A1887F", "#5D4037"
    def antler(x, phase):
        return group([filled(path([(0,0), (0,-60), (x*0.3, -80), (x*0.1, -50)], closed=False), antlers)],
                     wiggle((x, -70), base_rot=x*0.1, amp=12, period=35, phase=phase), name="antler")

    return [
        filled(ellipse(30, 25, (0, 30)), "#E53935", name="nose"),
        eye((-40, -20), 34, 38, iris="#3E2723"),
        eye((40, -20), 34, 38, iris="#3E2723"),
        filled(ellipse(180, 160), body, name="head"),
        antler(-60, 0), antler(60, 0.5),
    ]


def seagull():
    body, beak = "#ECEFF1", "#FBC02D"
    return [
        filled(path([(0, 0), (40, 10), (0, 20)], closed=True), beak,
               transform(pos=(0, 10)), name="beak"),
        dot_eye((-30, -20), 10), dot_eye((30, -20), 10),
        filled(ellipse(160, 160), body, name="head"),
        filled(ellipse(60, 30, (-70, 40)), "#9E9E9E", wiggle((0, 0), amp=10, period=30), name="wing"),
        filled(ellipse(60, 30, (70, 40)), "#9E9E9E", wiggle((0, 0), amp=10, period=30, phase=0.5), name="wing"),
    ]


def shrimp():
    body = "#FFAB91"
    return [
        dot_eye((-40, -20), 12), dot_eye((40, -20), 12),
        filled(ellipse(180, 120), body, name="body"),
        outlined(path([(0, 0), (-60, -40)], closed=False), body, 4, wiggle((-20, -40), amp=20, period=15), name="antenna"),
        outlined(path([(0, 0), (60, -40)], closed=False), body, 4, wiggle((20, -40), amp=20, period=15, phase=0.5), name="antenna"),
        filled(triangle(40, 60), body, transform(pos=(90, 0), rotation=90), name="tail"),
    ]


def skunk():
    body, stripe = "#000000", "#FFFFFF"
    return [
        filled(ellipse(20, 15, (0, 30)), "#424242", name="nose"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(180, 160), body, name="head"),
        filled(rect(40, 160, (0, -40), radius=20), stripe, name="stripe"),
    ]


def stingray():
    body = "#B0BEC5"
    return [
        dot_eye((-60, -20), 15), dot_eye((60, -20), 15),
        filled(ellipse(260, 180), body, name="body"),
        outlined(path([(0, 0), (0, 120)], closed=False), body, 8, wiggle((0, 80), amp=15, period=25), name="tail"),
    ]


def vulture():
    body, head = "#4E342E", "#F06292"
    return [
        filled(path([(0, 0), (0, 40), (-30, 20)], closed=True), "#757575",
               transform(pos=(0, 10)), name="beak"),
        dot_eye((-20, -10), 10), dot_eye((20, -10), 10),
        filled(ellipse(100, 100), head, name="head"),
        filled(ellipse(160, 60, (0, 60)), "#BDBDBD", name="ruff"),
    ]


def wasp():
    body, stripe = "#FBC02D", "#000000"
    return [
        dot_eye((-40, -20), 18), dot_eye((40, -20), 18),
        filled(ellipse(180, 140), body, name="body"),
        filled(rect(140, 20, (0, 20), radius=10), stripe, name="stripe"),
        filled(rect(100, 20, (0, 50), radius=10), stripe, name="stripe"),
        filled(ellipse(80, 40, (-60, -60)), "#E1F5FE", transform(opacity=60), name="wing"),
        filled(ellipse(80, 40, (60, -60)), "#E1F5FE", transform(opacity=60), name="wing"),
    ]


def yak():
    body, horns = "#3E2723", "#BDBDBD"
    return [
        filled(ellipse(100, 80, (0, 40)), "#212121", name="muzzle"),
        dot_eye((-45, -10), 15), dot_eye((45, -10), 15),
        filled(ellipse(200, 180), body, name="head"),
        outlined(path([(0,0), (-60, -20), (-80, -80)], closed=False), horns, 12, transform(pos=(-70, -40)), name="horn"),
        outlined(path([(0,0), (60, -20), (80, -80)], closed=False), horns, 12, transform(pos=(70, -40)), name="horn"),
        filled(rect(180, 60, (0, 80), radius=30), body, name="fringe"),
    ]


SET_E = {
    "ant": ant, "buffalo": buffalo, "hen": hen, "dragon": dragon, "goldfish": goldfish,
    "hyena": hyena, "iguana": iguana, "kiwi": kiwi, "moose": moose, "narwhal": narwhal,
    "orca": orca, "pigeon": pigeon, "reindeer": reindeer, "seagull": seagull, "shrimp": shrimp,
    "skunk": skunk, "stingray": stingray, "vulture": vulture, "wasp": wasp, "yak": yak,
}
