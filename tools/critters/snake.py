from critter_parts import FRAMES, eye
from lottie_kit import (
    animated, ellipse, filled, group, outlined, path, transform,
)


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
