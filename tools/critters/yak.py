from critter_parts import dot_eye
from lottie_kit import ellipse, filled, outlined, path, rect, transform


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
