from critter_parts import FRAMES, eye, triangle, wiggle
from lottie_kit import ellipse, filled, group, oscillate, outlined, path, rect, transform


def elephant():
    hide, inner, shadow_c, nostril_c = "#98a2ad", "#b6bfc8", "#767f89", "#454c53"

    # Wrinkle rings crossing the trunk, spaced down its length - the classic
    # cue that reads as "round tube" rather than "flat rectangle".
    def wrinkle(y, width):
        return outlined(path([(-width / 2, 0), (0, 4), (width / 2, 0)], closed=False),
                        shadow_c, 4, transform(pos=(0, y), opacity=45), name="wrinkle")

    trunk_top = group([
        wrinkle(-30, 40), wrinkle(-6, 42), wrinkle(18, 40),
        # A lit stripe on one side and a shaded stripe on the other, so the
        # shaft reads as a cylinder instead of a flat slab.
        filled(rect(16, 88, (-13, 0), radius=8), inner, transform(opacity=55), name="highlight"),
        filled(rect(14, 88, (15, 0), radius=7), shadow_c, transform(opacity=35), name="shade"),
        filled(rect(54, 96, (0, 0), radius=24), hide, name="trunk-top-base"),
    ], name="trunk-top")

    trunk_tip = group([
        filled(ellipse(7, 9, (2, 60)), nostril_c, name="nostril"),
        filled(ellipse(7, 9, (19, 60)), nostril_c, name="nostril"),
        filled(ellipse(13, 34, (3, 44)), inner, transform(opacity=50), name="tip-highlight"),
        filled(ellipse(11, 30, (19, 46)), shadow_c, transform(opacity=30), name="tip-shade"),
        filled(rect(42, 58, (10, 40), radius=20), hide, name="trunk-tip-base"),
    ], transform(rotation=22), name="trunk-tip")

    trunk = group(
        [trunk_tip, trunk_top],
        transform(pos=(0, 62), rotation=oscillate(FRAMES, 0, 7, 34)), name="trunk")

    ear = lambda x, ph: group(
        [filled(ellipse(96, 122, (x * 0.18, 6)), inner, name="inner"),
         filled(ellipse(126, 156), hide, name="outer")],
        wiggle((x, -8), base_rot=x * 0.09, amp=7, period=30, phase=ph), name="ear")
    return [
        trunk,
        filled(triangle(20, 40, tilt=-6), "#f4efe4",
               transform(pos=(-40, 92), rotation=8), name="tusk"),
        filled(triangle(20, 40, tilt=6), "#f4efe4",
               transform(pos=(40, 92), rotation=-8), name="tusk"),
        eye((-44, -24), 30, 32), eye((44, -24), 30, 32),
        filled(ellipse(180, 164), hide, name="head"),
        ear(-96, 0.0), ear(96, 0.5),
    ]
