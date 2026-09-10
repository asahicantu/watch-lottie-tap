"""Set F: 20 more animals for CritterTap."""

import math
from critter_parts import (
    FRAMES, critter, dot_eye, eye, oscillate, smile, triangle, wiggle,
)
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform

def badger():
    fur, stripe = "#455A64", "#ECEFF1"
    return [
        filled(ellipse(22, 16), "#2b2724", transform(pos=(0, 42)), name="nose"),
        dot_eye((-40, 0), 12), dot_eye((40, 0), 12),
        filled(rect(34, 92, (40, 0), radius=16), "#2b2724", name="eye-stripe"),
        filled(rect(34, 92, (-40, 0), radius=16), "#2b2724", name="eye-stripe"),
        filled(rect(40, 140, (0, 0), radius=20), stripe, name="stripe"),
        filled(ellipse(180, 160), fur, name="head"),
        filled(ellipse(50, 50), fur, wiggle((-70, -60), base_rot=-20), name="ear"),
        filled(ellipse(50, 50), fur, wiggle((70, -60), base_rot=20, phase=0.5), name="ear"),
    ]

def caterpillar():
    skin = "#8BC34A"
    segments = []
    for i in range(5):
        segments.append(filled(ellipse(70, 70), skin,
                              transform(pos=(i * 45 - 90, oscillate(FRAMES, 0, 15, 30, phase=i*0.2)["k"][0]["s"][0])),
                              name=f"segment-{i}"))
    # Simpler segments for now without complex oscillation in pos
    segments = [
        filled(ellipse(70, 70), skin, transform(pos=(90, 0)), name="seg4"),
        filled(ellipse(70, 70), skin, transform(pos=(45, 0)), name="seg3"),
        filled(ellipse(70, 70), skin, transform(pos=(0, 0)), name="seg2"),
        filled(ellipse(70, 70), skin, transform(pos=(-45, 0)), name="seg1"),
        filled(ellipse(80, 80), skin, transform(pos=(-90, 0)), name="head"),
    ]
    return [
        smile(30, 10, y=10, color="#33691E", w=4),
        dot_eye((-105, -10), 8), dot_eye((-75, -10), 8),
        *segments
    ]

def chameleon():
    skin = "#4CAF50"
    return [
        outlined(path([(0, 0), (40, 20), (20, 60)], closed=False), skin, 8,
                 transform(pos=(70, 30), rotation=oscillate(FRAMES, 0, 30, 40)), name="tail"),
        smile(60, 20, y=20, color="#1B5E20", w=5),
        eye((-50, -20), 45, 45, iris="#8BC34A"),
        eye((40, -20), 45, 45, iris="#8BC34A"),
        filled(ellipse(190, 140), skin, name="body"),
    ]

def cockatoo():
    feathers = "#ECEFF1"
    crest = "#FFF176"
    return [
        filled(triangle(40, 60), crest, wiggle((0, -90), base_rot=0, amp=15), name="crest"),
        filled(triangle(30, 40), "#455A64", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(160, 180), feathers, name="head"),
    ]

def crayfish():
    shell = "#BF360C"
    def claw(x, phase):
        return group([filled(ellipse(50, 80), shell, name="claw-inner")],
                     wiggle((x, -40), base_rot=x*0.5, amp=20, period=25, phase=phase), name="claw")
    return [
        claw(-80, 0), claw(80, 0.5),
        outlined(path([(-30, -80), (0, -120), (30, -80)], closed=False), shell, 4, name="antenna"),
        dot_eye((-30, -20), 12), dot_eye((30, -20), 12),
        filled(ellipse(120, 180), shell, name="body"),
    ]

def firefly():
    body, glow = "#37474F", "#FBC02D"
    return [
        filled(ellipse(100, 80), glow, transform(pos=(0, 70), opacity=oscillate(FRAMES, 70, 30, 20)), name="glow"),
        dot_eye((-30, -30), 15), dot_eye((30, -30), 15),
        filled(ellipse(140, 160), body, name="body"),
        filled(ellipse(50, 100), "#90A4AE", transform(pos=(-60, 0), rotation=-20), name="wing-l"),
        filled(ellipse(50, 100), "#90A4AE", transform(pos=(60, 0), rotation=20), name="wing-r"),
    ]

def guinea_pig():
    fur = "#A1887F"
    return [
        filled(ellipse(15, 10), "#5D4037", transform(pos=(0, 25)), name="nose"),
        dot_eye((-50, -10), 18), dot_eye((50, -10), 18),
        filled(ellipse(200, 150), fur, name="body"),
        filled(ellipse(50, 35, (0, 0)), "#D7CCC8", transform(pos=(-90, -40), rotation=-30), name="ear"),
        filled(ellipse(50, 35, (0, 0)), "#D7CCC8", transform(pos=(90, -40), rotation=30), name="ear"),
    ]

def hummingbird():
    body = "#00BCD4"
    def wing(x, phase):
        return filled(ellipse(30, 100), "#4DD0E1",
                      transform(pos=(x, 0), rotation=oscillate(FRAMES, x*0.5, 45, 4, phase)), name="wing")
    return [
        wing(-60, 0), wing(60, 0.5),
        outlined(path([(0, 0), (0, 80)], closed=False), "#263238", 4, transform(pos=(0, 20)), name="beak"),
        dot_eye((-30, -20), 12), dot_eye((30, -20), 12),
        filled(ellipse(120, 140), body, name="body"),
    ]

def kookaburra():
    feathers = "#795548"
    return [
        filled(triangle(40, 80), "#D7CCC8", transform(pos=(0, 30), rotation=180), name="beak"),
        dot_eye((-40, -20), 18), dot_eye((40, -20), 18),
        filled(ellipse(170, 160), feathers, name="head"),
        filled(rect(60, 20, (0, -90), radius=5), "#5D4037", name="tuft"),
    ]

def locust():
    skin = "#9E9D24"
    return [
        outlined(path([(-20, -70), (-40, -110)], closed=False), skin, 5, name="antenna"),
        outlined(path([(20, -70), (40, -110)], closed=False), skin, 5, name="antenna"),
        dot_eye((-40, -30), 15), dot_eye((40, -30), 15),
        filled(ellipse(130, 200), skin, name="body"),
        filled(ellipse(40, 150), "#C0CA33", transform(pos=(-60, 20), rotation=-10), name="wing"),
        filled(ellipse(40, 150), "#C0CA33", transform(pos=(60, 20), rotation=10), name="wing"),
    ]

def meerkat():
    fur = "#D7CCC8"
    return [
        filled(ellipse(20, 15), "#3E2723", transform(pos=(0, 20)), name="nose"),
        filled(ellipse(40, 40), "#A1887F", transform(pos=(-45, -15)), name="eye-patch"),
        filled(ellipse(40, 40), "#A1887F", transform(pos=(45, -15)), name="eye-patch"),
        dot_eye((-45, -15), 12), dot_eye((45, -15), 12),
        filled(ellipse(140, 180), fur, name="head"),
        filled(ellipse(30, 30), "#3E2723", transform(pos=(-75, -60)), name="ear"),
        filled(ellipse(30, 30), "#3E2723", transform(pos=(75, -60)), name="ear"),
    ]

def mosquito():
    body = "#607D8B"
    return [
        outlined(path([(0, 0), (0, 70)], closed=False), "#263238", 3, transform(pos=(0, 30)), name="proboscis"),
        dot_eye((-25, -20), 15), dot_eye((25, -20), 15),
        filled(ellipse(100, 120), body, name="body"),
        filled(ellipse(30, 120), "#B0BEC5",
               transform(pos=(-50, -20), rotation=oscillate(FRAMES, -30, 20, 5), opacity=50), name="wing"),
        filled(ellipse(30, 120), "#B0BEC5",
               transform(pos=(50, -20), rotation=oscillate(FRAMES, 30, 20, 5, phase=0.5), opacity=50), name="wing"),
    ]

def moth():
    body = "#9E9E9E"
    return [
        outlined(path([(-10, -50), (-40, -80)], closed=False), "#616161", 4, name="antenna"),
        outlined(path([(10, -50), (40, -80)], closed=False), "#616161", 4, name="antenna"),
        dot_eye((-30, -20), 18), dot_eye((30, -20), 18),
        filled(ellipse(120, 150), body, name="body"),
        filled(ellipse(90, 140), "#BDBDBD", transform(pos=(-70, 0), rotation=-30), name="wing"),
        filled(ellipse(90, 140), "#BDBDBD", transform(pos=(70, 0), rotation=30), name="wing"),
    ]

def nightingale():
    feathers = "#8D6E63"
    return [
        filled(triangle(30, 40), "#FDD835", transform(pos=(0, 20), rotation=180), name="beak"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(160, 160), feathers, name="head"),
        filled(ellipse(100, 60), "#A1887F", transform(pos=(0, 60)), name="chest"),
    ]

def puffin():
    feathers = "#263238"
    return [
        filled(triangle(60, 70), "#FFD54F", transform(pos=(0, 30), rotation=180), name="beak"),
        filled(path([(-30, 30), (0, -20), (30, 30)], closed=True), "#F44336", transform(pos=(0, 25)), name="beak-tip"),
        eye((-45, -20), 35, 35, iris="#CFD8DC"),
        eye((45, -20), 35, 35, iris="#CFD8DC"),
        filled(ellipse(180, 180), feathers, name="head"),
        filled(ellipse(120, 120), "#FFFFFF", transform(pos=(0, 10)), name="face"),
    ]

def salamander():
    skin = "#FF9800"
    return [
        filled(ellipse(20, 20), "#F57C00", transform(pos=(-40, 40)), name="spot"),
        filled(ellipse(25, 25), "#F57C00", transform(pos=(50, -30)), name="spot"),
        smile(70, 25, y=30, color="#E65100", w=6),
        dot_eye((-50, -20), 20), dot_eye((50, -20), 20),
        filled(ellipse(200, 130), skin, name="body"),
    ]

def swordfish():
    body = "#546E7A"
    return [
        outlined(path([(0, 0), (0, 120)], closed=False), "#90A4AE", 6, transform(pos=(0, 40)), name="sword"),
        dot_eye((-35, -20), 20), dot_eye((35, -20), 20),
        filled(ellipse(130, 180), body, name="body"),
        filled(triangle(40, 60), "#455A64", transform(pos=(0, -80)), name="fin"),
    ]

def woodpecker():
    feathers = "#D32F2F"
    return [
        outlined(path([(0, 0), (0, 90)], closed=False), "#455A64", 8,
                 transform(pos=(0, 20), rotation=oscillate(FRAMES, 0, 10, 10)), name="beak"),
        dot_eye((-40, -10), 15), dot_eye((40, -10), 15),
        filled(ellipse(160, 170), "#263238", name="head"),
        filled(rect(40, 80, (0, -70), radius=10), feathers, name="crest"),
    ]

def hornet():
    body = "#FF6F00"
    return [
        smile(40, 15, y=-20, color="#212121", w=5),
        dot_eye((-35, -40), 18), dot_eye((35, -40), 18),
        filled(rect(120, 25, (0, 60), radius=10), "#212121", name="stripe"),
        filled(rect(160, 25, (0, 20), radius=10), "#212121", name="stripe"),
        filled(ellipse(190, 160), body, name="body"),
        filled(ellipse(60, 110), "#B0BEC5",
               transform(pos=(-70, -30), rotation=oscillate(FRAMES, -20, 30, 5), opacity=60), name="wing"),
        filled(ellipse(60, 110), "#B0BEC5",
               transform(pos=(70, -30), rotation=oscillate(FRAMES, 20, 30, 5, phase=0.5), opacity=60), name="wing"),
    ]

def okapi():
    fur = "#3E2723"
    return [
        filled(rect(100, 15, (0, 70), radius=5), "#FFFFFF", name="leg-stripe"),
        filled(rect(120, 15, (0, 90), radius=5), "#FFFFFF", name="leg-stripe"),
        dot_eye((-40, -20), 18), dot_eye((40, -20), 18),
        filled(ellipse(160, 190), fur, name="head"),
        filled(ellipse(60, 90), "#5D4037", wiggle((-80, -70), base_rot=-20), name="ear"),
        filled(ellipse(60, 90), "#5D4037", wiggle((80, -70), base_rot=20, phase=0.5), name="ear"),
    ]

SET_F = {
    "badger": badger, "caterpillar": caterpillar, "chameleon": chameleon,
    "cockatoo": cockatoo, "crayfish": crayfish, "firefly": firefly,
    "guinea_pig": guinea_pig, "hummingbird": hummingbird, "kookaburra": kookaburra,
    "locust": locust, "meerkat": meerkat, "mosquito": mosquito, "moth": moth,
    "nightingale": nightingale, "puffin": puffin, "salamander": salamander,
    "swordfish": swordfish, "woodpecker": woodpecker, "hornet": hornet, "okapi": okapi,
}
