import math
from critter_parts import eye, nostrils, teeth, triangle, wiggle, FRAMES
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform

def crocodile():
    skin_c, dark_c, belly_c, mouth_c = "#5F9E56", "#33632E", "#C8ECA0", "#8E2424"
    shine_c = "#EFFFE0"

    # A long wiggling tail behind the body, with a couple of trailing scutes
    # so the bony ridge on the head reads as a continuation of the spine.
    tail_parts = []
    for i in range(3):
        y_off = 78 + i * 26
        w = 112 - i * 28
        h = 42
        tail_parts.append(
            filled(ellipse(w, h, (0, 0)), skin_c,
                   wiggle((0, y_off), amp=8, period=40, phase=i * 0.2),
                   name=f"tail_seg_{i}")
        )
    tail_scutes = [
        filled(triangle(16, 18), dark_c, wiggle((-14, 82), amp=8, period=40, phase=0.0)),
        filled(triangle(16, 18), dark_c, wiggle((14, 104), amp=8, period=40, phase=0.2)),
    ]

    # Bony crown spikes, sitting proud of the head's silhouette
    def scute(x, y, scale=1.0):
        return filled(path([(0, 0), (-11, 18), (11, 18)], closed=True), dark_c,
                      transform(pos=(x, y), scale=(100 * scale, 100 * scale), rotation=180),
                      name="scute")

    # Thick, angled brow ridges for that grinning "cartoon" attitude
    brows = [
        outlined(path([(-26, 6), (0, -14), (26, 6)], closed=False), dark_c, 10,
                 wiggle((-58, -104), base_rot=-6, amp=4, period=40), name="brow"),
        outlined(path([(-26, 6), (0, -14), (26, 6)], closed=False), dark_c, 10,
                 wiggle((58, -104), base_rot=6, amp=4, period=40, phase=0.5), name="brow"),
    ]

    # Scales/Bumps on the head for texture
    bumps = [
        filled(ellipse(16, 11, (-38, -48)), dark_c, transform(opacity=35), name="bump"),
        filled(ellipse(14, 9, (42, -42)), dark_c, transform(opacity=28), name="bump"),
        filled(ellipse(18, 13, (0, -68)), dark_c, transform(opacity=32), name="bump"),
        filled(ellipse(12, 8, (-18, -20)), dark_c, transform(opacity=22), name="bump"),
        filled(ellipse(12, 8, (24, -14)), dark_c, transform(opacity=22), name="bump"),
    ]

    # A darker cranium cap gives the head a two-tone, cartoon-reptile finish
    head_top = filled(ellipse(196, 118, (0, -58)), dark_c, transform(opacity=55), name="head_top")

    # A soft gloss highlight so the head reads as smooth and glossy, not flat
    head_shine = filled(ellipse(58, 34, (-52, -92)), shine_c, transform(opacity=35), name="head_shine")

    # Eyes ride on top of the wiggling domes
    def eye_dome(x, phase):
        e = eye((0, 0), w=42, h=42, iris="#000000", white="#ffffff", blink_at=50 + int(phase * 10))
        dome = filled(ellipse(76, 72), skin_c, name="dome")
        rim = filled(ellipse(82, 78), dark_c, transform(opacity=25), name="dome_rim")
        return group([e, dome, rim], wiggle((x, -88), amp=3, period=45, phase=phase), name="eyedome")

    # Pronounced, rounded snout tip with nostrils and a glossy highlight -
    # sits at the *front* (far) end of the snout, not tucked under the eyes.
    nose_tip = group([
        filled(ellipse(16, 9, (-10, -8)), shine_c, transform(opacity=45), name="nose_shine"),
        nostrils(11, -4, 15, 11, dark_c),
        filled(ellipse(58, 38), skin_c, name="nose_bulb"),
    ], transform(pos=(0, 80)), name="nose_tip")

    # Snout: a rounded base tapering into the nose bulb, with a snapping jaw.
    # The nose sits on top; the teeth are pushed to the back, behind the jaw.
    snout_top = group([
        nose_tip,
        # Tapered upper-jaw shape: wide where it meets the head, narrowing
        # toward the nose so the whole snout reads as one continuous shape.
        filled(rect(88, 46, (0, 58), radius=22), skin_c, name="upper_jaw_tip"),
        filled(rect(126, 68, (0, 16), radius=32), skin_c, name="upper_jaw_base"),
        # Large jagged teeth on the upper jaw, tucked behind the jaw shape
        teeth(6, 46, 104, size=15),
    ], transform(pos=(0, 26),
                 rotation=animated([(0, 0), (15, -14), (30, 0), (45, -12), (60, 0), (FRAMES, 0)])),
    name="snout_top")

    # Wiggling pink tongue inside the mouth
    tongue = filled(ellipse(42, 60), "#D81B60",
                    wiggle((0, 16), amp=10, period=25), name="tongue")

    lower_jaw = group([
        # A pale chin nub under the mouth, mirroring the nose for symmetry
        filled(ellipse(42, 22, (0, 46)), belly_c, name="chin"),
        # Mouth on top: tongue and the red mouth interior sit in front of the
        # teeth, which are pushed to the back, behind the jaw shape.
        tongue,
        filled(ellipse(128, 40, (0, 14)), mouth_c, name="mouth_inner"),
        # Teeth on the lower jaw pointing up, tucked behind the mouth
        group([filled(path([(0, 0), (-11, -18), (11, -18)], closed=True), "#ffffff",
                      transform(pos=(x, 0)), name="tooth") for x in [-52, -26, 26, 52]],
              transform(pos=(0, 22))),
        filled(rect(140, 48, (0, 22), radius=24), dark_c, name="bottom_jaw"),
    ], transform(pos=(0, 40),
                 rotation=animated([(0, 0), (15, 20), (30, 0), (45, 15), (60, 0), (FRAMES, 0)])),
    name="snout_bottom")

    return (
        [eye_dome(-58, 0.0), eye_dome(58, 0.3),
         snout_top,
         lower_jaw]
        + brows
        + [scute(-42, -104, 0.85), scute(0, -116, 1.0), scute(42, -104, 0.85)]
        + bumps
        + [head_top, head_shine,
           filled(ellipse(206, 168, (0, -12)), skin_c, name="main_head")]
        + tail_parts + tail_scutes
    )
