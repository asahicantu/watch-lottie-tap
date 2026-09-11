from critter_parts import FRAMES, eye, nostrils, teeth
from lottie_kit import animated, ellipse, filled, group, rect, transform


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
