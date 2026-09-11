from critter_parts import eye, smile
from lottie_kit import ellipse, filled, group, transform


def frog():
    skin, belly = "#6cc24a", "#a7dd7f"

    def eye_dome(x):
        return group([eye((0, 0), 40, 42, iris="#2f2a26"),
                      filled(ellipse(92, 88), skin, name="dome")],
                     transform(pos=(x, -62)), name="eyedome")

    return [
        filled(ellipse(14, 10, (-22, -6)), "#3d7a2a", name="nostril"),
        filled(ellipse(14, 10, (22, -6)), "#3d7a2a", name="nostril"),
        smile(126, 44, y=18, color="#2f6b20", w=9),
        filled(ellipse(120, 60, (0, 52)), belly, name="chin"),
        filled(ellipse(206, 156), skin, name="head"),
        eye_dome(-58), eye_dome(58),
    ]
