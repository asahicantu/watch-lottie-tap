"""A cat face built the way a cat is actually shaped: a skull wider than it is
tall, cheek ruffs bulging past it, and a short muzzle of two whisker pads under
a heart-shaped nose."""

from critter_parts import eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform

FUR = "#f0a04b"
TABBY = "#d9823a"
INNER = "#f6c7a8"
MUZZLE = "#fbe3cd"
NOSE = "#e2657a"
NOSE_RIM = "#c1546a"
MOUTH = "#8a4a3c"
WHISKER = "#f7e6d4"


def _ear(x, phase):
    """A leaf-shaped ear: a soft outer curve to a blunt tip, a pink inner, and
    the wisps of fur that stick out of the near edge."""
    side = 1 if x > 0 else -1

    def leaf(w, h, tilt):
        hw = w / 2.0
        return path([(-hw, 0), (tilt, -h), (hw, 0)], closed=True,
                    tangents=[((0, 0), (hw * 0.10, -h * 0.42)),
                              ((-hw * 0.26, h * 0.30), (hw * 0.26, h * 0.30)),
                              ((-hw * 0.10, -h * 0.42), (0, 0))])

    tufts = group(
        [filled(triangle(9, 20 - 4 * i), WHISKER,
                transform(pos=(-side * (10 + i * 11), -6), rotation=-side * 26),
                name="tuft")
         for i in range(3)],
        name="tufts")
    return group(
        [tufts,
         filled(leaf(44, 48, x * 0.16), INNER, transform(pos=(0, -6)),
                name="inner"),
         filled(leaf(78, 80, x * 0.14), FUR, name="outer")],
        wiggle((x, -56), base_rot=x * 0.10, amp=6, period=26, phase=phase),
        name="ear")


def _nose():
    """The leather: a rounded triangle, pointing down, on a darker rim."""
    def leather(w, h):
        hw = w / 2.0
        return path([(-hw, -h / 2), (hw, -h / 2), (0, h / 2)], closed=True,
                    tangents=[((-1, h * 0.34), (w * 0.22, -h * 0.17)),
                              ((-w * 0.22, -h * 0.17), (1, h * 0.34)),
                              ((w * 0.22, -h * 0.24), (-w * 0.22, -h * 0.24))])

    return group([filled(leather(33, 25), NOSE, name="leather"),
                  filled(leather(41, 32), NOSE_RIM, name="rim")],
                 transform(pos=(0, 28)), name="nose")


def _mouth():
    """Philtrum down from the nose, then the two arcs of the cat's `w`."""
    def lip(side):
        return outlined(
            path([(0, 0), (side * 27, 6)], closed=False,
                 tangents=[((0, 0), (side * 5, 13)),
                           ((-side * 11, 3), (0, 0))]),
            MOUTH, 6, name="lip")

    return group([lip(-1), lip(1),
                  outlined(path([(0, -15), (0, 0)], closed=False), MOUTH, 5,
                           name="philtrum")],
                 transform(pos=(0, 52)), name="mouth")


def _whisker(x, y, drop):
    """A whisker that starts at the edge of a pad and bows on the way out."""
    return outlined(
        path([(0, 0), (x, drop)], closed=False,
             tangents=[((0, 0), (x * 0.3, drop * 0.1)),
                       ((-x * 0.3, -drop * 0.55), (0, 0))]),
        WHISKER, 5, transform(pos=(x * 0.58, y)), name="whisker")


def _stripe(x, y, w, h, rot):
    return filled(triangle(w, h), TABBY, transform(pos=(x, y), rotation=rot),
                  name="stripe")


def cat():
    pad = lambda x: filled(ellipse(64, 48, (x, 48)), MUZZLE, name="pad")
    dots = group(
        [filled(ellipse(7, 7, (x, y)), TABBY, name="dot")
         for x, y in ((-38, 40), (-24, 34), (-44, 52),
                      (38, 40), (24, 34), (44, 52))],
        name="whisker-dots")

    return [
        _whisker(78, 12, -14), _whisker(86, 28, 2), _whisker(78, 44, 18),
        _whisker(-78, 12, -14), _whisker(-86, 28, 2), _whisker(-78, 44, 18),
        _mouth(),
        dots,
        _nose(),
        pad(-24), pad(24),
        eye((-46, -14), 36, 42, iris="#4b9b52"),
        eye((46, -14), 36, 42, iris="#4b9b52"),
        # the tabby M, and a pair of bars on each cheek
        _stripe(0, -42, 17, 38, 0),
        _stripe(-27, -40, 15, 32, 13), _stripe(27, -40, 15, 32, -13),
        _stripe(-50, -32, 13, 26, 24), _stripe(50, -32, 13, 26, -24),
        _stripe(-64, 0, 10, 36, -96), _stripe(64, 0, 10, 36, 96),
        _stripe(-68, 22, 9, 32, -84), _stripe(68, 22, 9, 32, 84),
        filled(ellipse(198, 170), FUR, name="head"),
        # ruffs, behind the skull, so the cheeks bulge past it
        filled(ellipse(86, 94, (-80, 22)), FUR, name="ruff"),
        filled(ellipse(86, 94, (80, 22)), FUR, name="ruff"),
        _ear(-66, 0.0), _ear(66, 0.5),
    ]
