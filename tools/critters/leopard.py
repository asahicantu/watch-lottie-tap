import math

from critter_parts import eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def leopard():
    fur, pale, spot = "#E9A13B", "#F7E4C8", "#3E2723"
    rose_c, deep = "#C97A20", "#2A1B14"

    def rosette(x, y, r):
        """A leopard's spot is a broken ring of flecks round a darker centre,
        not the single outlined circle this used to draw."""
        flecks = [filled(ellipse(r * 0.5, r * 0.5,
                                 (r * math.cos(a), r * math.sin(a))), spot,
                         name="fleck")
                  for a in (0.5, 1.6, 2.7, 3.8, 4.9, 6.0)]
        return group(flecks + [filled(ellipse(r * 1.5, r * 1.5), rose_c,
                                      name="centre")],
                     transform(pos=(x, y)), name="rosette")

    def ear(x, phase):
        return group([filled(ellipse(34, 30, (0, 4)), pale, name="inner"),
                      filled(ellipse(52, 48), fur, name="outer"),
                      filled(ellipse(62, 58), spot, name="back")],
                     wiggle((x, -68), base_rot=x * 0.16, amp=5, period=32,
                            phase=phase), name="ear")

    def whisker(x, y, tilt):
        return outlined(path([(0, 0), (x, tilt)], closed=False), "#FBEFDC", 4,
                        transform(pos=(x * 0.58, y)), name="whisker")

    # the rosettes keep clear of the eyes, muzzle and ears
    rosettes = [rosette(x, y, r) for x, y, r in
                ((-50, -60, 15), (50, -60, 14), (-66, -12, 15), (66, -10, 14),
                 (0, -62, 13), (-62, 34, 14), (62, 32, 13))]
    # small solid flecks where the whiskers grow
    flecks = [filled(ellipse(9, 9, (x, y)), deep, name="fleck")
              for x, y in ((-58, 20), (-46, 34), (58, 20), (46, 34))]

    return [
        whisker(62, 4, -12), whisker(68, 16, 2), whisker(62, 28, 14),
        whisker(-62, 4, -12), whisker(-68, 16, 2), whisker(-62, 28, 14),
    ] + flecks + [
        smile(48, 15, y=48, color=deep, w=5),
        filled(triangle(26, 19, pos=(0, 9)), "#C4626F",
               transform(pos=(0, 24), rotation=180), name="nose"),
        filled(ellipse(58, 44, (-24, 44)), pale, name="muzzle"),
        filled(ellipse(58, 44, (24, 44)), pale, name="muzzle"),
        eye((-46, -18), 34, 38, iris="#D9A227"),
        eye((46, -18), 34, 38, iris="#D9A227"),
    ] + rosettes + [
        filled(ellipse(182, 172), fur, name="head"),
        ear(-76, 0.0), ear(76, 0.5),
    ]
