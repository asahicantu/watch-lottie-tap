from critter_parts import eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def cheetah():
    fur, spot, cream = "#FBC02D", "#212121", "#FFF9C4"
    shade, line = "#C69200", "#4A3A12"
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

    def whisker(side, y, tilt):
        return outlined(path([(0, 0), (side * 48, tilt)], closed=False), cream, 3,
                        transform(pos=(side * 51, y)), name="whisker")

    def paw(side, phase):
        return group([
            filled(ellipse(35, 17, (0, 19)), line, name="paw-pad"),
            filled(ellipse(43, 43), fur, name="paw"),
        ], wiggle((side * 58, 133), amp=3, period=24, phase=phase), name="paw")

    tail = filled(ellipse(36, 96), fur,
                  wiggle((103, 90), base_rot=37, amp=9, period=28), name="tail")

    nose = group([
        filled(ellipse(10, 5, (-7, -4)), "#F7B6C3", name="nose-highlight"),
        filled(ellipse(8, 6, (-8, 2)), "#682438", name="left-nostril"),
        filled(ellipse(8, 6, (8, 2)), "#682438", name="right-nostril"),
        filled(path([(-18, -7), (18, -7), (0, 14)], closed=True), "#C94C69",
               name="nose"),
        filled(path([(-22, -10), (22, -10), (0, 18)], closed=True), "#6E293B",
               name="nose-outline"),
    ], transform(pos=(0, 18)), name="cheetah-nose")

    return [
        whisker(-1, 5, -11), whisker(-1, 18, 0), whisker(-1, 31, 11),
        whisker(1, 5, -11), whisker(1, 18, 0), whisker(1, 31, 11),
        smile(52, 18, y=38, color="#7F6D00", w=5),
        nose,
        filled(ellipse(96, 78, (0, 42)), cream, name="muzzle"),
        eye((-42, -18), 34, 36, iris=spot),
        eye((42, -18), 34, 36, iris=spot),
    ] + teardrops + spots + [
        filled(ellipse(194, 178), fur, name="head"),
        filled(ellipse(100, 52, (0, 107)), cream, name="chest"),
        filled(ellipse(186, 126, (0, 94)), fur, name="round-body"),
        filled(ellipse(202, 138, (0, 101)), shade, name="body-shadow"),
        paw(-1, 0.0), paw(1, 0.5),
        ear(-72, 0.0), ear(72, 0.5), tail,
    ]
