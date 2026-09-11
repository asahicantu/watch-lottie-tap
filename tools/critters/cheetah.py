from critter_parts import eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def cheetah():
    fur, spot, cream = "#FBC02D", "#212121", "#FFF9C4"
    # Malar stripes (teardrop marks) from eyes to mouth corners
    teardrops = [
        outlined(path([(-24, -10), (-26, 12), (-24, 38)], closed=False), spot, 5, name="teardrop"),
        outlined(path([(24, -10), (26, 12), (24, 38)], closed=False), spot, 5, name="teardrop")
    ]
    # Small solid black spots distributed across the head
    spots_pos = [
        (-60, 20), (60, 20), (0, -60), (-35, -55), (35, -55),
        (-75, -20), (75, -20), (-45, 45), (45, 45), (0, 75),
        (-30, 0), (30, 0), (0, -25)
    ]
    spots = [filled(ellipse(10, 10, pos), spot, name="spot") for pos in spots_pos]

    ear = lambda x, ph: group(
        [filled(ellipse(28, 28), spot, name="inner"),
         filled(ellipse(50, 50), fur, name="outer")],
        wiggle((x, -70), base_rot=x * 0.1, amp=6, period=28, phase=ph), name="ear")

    return [
        smile(52, 18, y=38, color="#7F6D00", w=5),
        filled(triangle(26, 18, pos=(0, 15)), "#D81B60", transform(rotation=180), name="nose"),
        filled(ellipse(96, 78, (0, 42)), cream, name="muzzle"),
        eye((-42, -18), 34, 36, iris=spot),
        eye((42, -18), 34, 36, iris=spot),
    ] + teardrops + spots + [
        filled(ellipse(194, 178), fur, name="head"),
        ear(-72, 0.0), ear(72, 0.5)
    ]
