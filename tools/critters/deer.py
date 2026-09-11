from critter_parts import eye, nostrils, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def deer():
    fur_c, fur_dark = "#B07A4E", "#8A5A34"
    muzzle_c = "#F3E3C8"
    nose_c = "#3E2723"
    antler_c, antler_dark = "#EFE6D2", "#D2C6A6"

    # A branching cartoon antler: a main beam plus two forking tines, each
    # capped with a small point so it reads as bone rather than a bare stick.
    def _point(pos, rotation=0):
        return filled(triangle(11, 16), antler_c, transform(pos=pos, rotation=rotation), name="tip")

    def _tine(base_y, length, angle, x_side):
        return group([
            _point((0, -length)),
            filled(rect(9, length, (0, -length / 2), radius=4), antler_dark, name="tine_shade"),
            filled(rect(7, length, (0, -length / 2), radius=4), antler_c, name="tine"),
        ], transform(pos=(0, base_y), rotation=angle * x_side), name="tine_group")

    def antler(x_side, phase):
        beam = filled(rect(14, 82, (0, -41), radius=7), antler_dark, name="beam_shade")
        beam_top = filled(rect(11, 82, (0, -41), radius=6), antler_c, name="beam")
        beam_tip = _point((0, -82))
        return group([
            _tine(-30, 40, 42, x_side),
            _tine(-58, 34, 62, x_side),
            beam_tip, beam_top, beam,
        ], wiggle((x_side * 40, -78), base_rot=x_side * 6, amp=4, period=42, phase=phase),
            name="antler")

    def ear(x_side, phase):
        outer = filled(triangle(36, 66, tilt=x_side * 6), fur_c, name="ear_outer")
        inner = filled(triangle(20, 46, tilt=x_side * 6), fur_dark, transform(pos=(0, -6)), name="ear_inner")
        return group([inner, outer], wiggle((x_side * 82, -58), base_rot=x_side * 22, amp=6, period=36, phase=phase),
                     name="ear")

    def lash(x_side, phase):
        return outlined(path([(-9, 0), (0, -8), (9, -2)], closed=False), fur_dark, 4,
                         wiggle((x_side * 46, -46), amp=2, period=45, phase=phase), name="lash")

    nose = group([
        filled(ellipse(10, 6, (-7, -6)), "#FFFFFF", transform(opacity=55), name="nose_shine"),
        nostrils(9, -3, 9, 7, "#1B0E0A"),
        filled(ellipse(36, 26), nose_c, name="nose_bulb"),
    ], transform(pos=(0, 95)), name="nose")

    spots = [filled(ellipse(13, 9, (x, y)), "#FFFFFF", transform(opacity=85), name="spot")
             for x, y in [(-56, 22), (56, 22), (0, 48)]]

    return (
        [eye((-44, -26), 30, 34, iris="#2b2724", white="#ffffff", blink_at=48),
         eye((44, -26), 30, 34, iris="#2b2724", white="#ffffff", blink_at=58),
         lash(-1, 0.0), lash(1, 0.4),
         smile(30, 9, y=113, color=nose_c, w=5),
         nose,
         ear(-1, 0.0), ear(1, 0.5),
         antler(-1, 0.0), antler(1, 0.5)]
        + spots
        + [filled(ellipse(72, 56, (0, 76)), muzzle_c, name="muzzle_patch"),
           filled(rect(102, 92, (0, 56), radius=46), fur_c, name="muzzle_base"),
           filled(ellipse(186, 162, (0, -18)), fur_c, name="head")]
    )
