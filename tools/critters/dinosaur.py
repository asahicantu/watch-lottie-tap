from critter_parts import dot_eye, smile
from lottie_kit import ellipse, filled, rect


def dinosaur():
    skin_c = "#2E7D32"
    arms = [filled(rect(20, 10, (x, 40), radius=5), skin_c) for x in [-40, 40]]
    return arms + [
        smile(60, 20, y=20, color="#1B5E20", w=5),
        dot_eye((-40, -30), 15), dot_eye((40, -30), 15),
        filled(ellipse(180, 140, (0, 0)), skin_c, name="head"),
        filled(ellipse(120, 180, (0, 80)), skin_c, name="body"),
    ]
