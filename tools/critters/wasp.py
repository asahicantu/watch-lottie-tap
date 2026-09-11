from critter_parts import dot_eye
from lottie_kit import ellipse, filled, rect, transform


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
