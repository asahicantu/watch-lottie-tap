from critter_parts import dot_eye
from lottie_kit import ellipse, filled, path, transform


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
