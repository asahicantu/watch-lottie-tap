import math
from critter_parts import eye, smile, wiggle, FRAMES
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform


def crab():
    body_c, dark_c, highlight_c = "#E53935", "#B71C1C", "#FF8A80"

    def leg(x_side, y_pos, phase):
        x_base = 80 * x_side
        return outlined(
            path([(0, 0), (20 * x_side, -10), (40 * x_side, 20)], closed=False),
            body_c, 8,
            wiggle((x_base, y_pos), base_rot=0, amp=15, period=20, phase=phase),
            name="leg"
        )

    def claw(x_side, phase):
        # Larger, more rounded "cartoon" pincers
        x_base = 110 * x_side

        # Pincer parts
        lower = filled(ellipse(65, 45, (35 * x_side, 12)), body_c, name="lower")
        upper = filled(ellipse(65, 45, (35 * x_side, -12)), dark_c,
                       transform(rotation=animated([(0, 0), (12, -30 * x_side), (25, 0), (FRAMES, 0)])),
                       name="upper")

        palm = filled(ellipse(55, 60), body_c, name="palm")
        arm = filled(rect(22, 50, (0, 35), radius=12), body_c, name="arm")

        return group(
            [upper, lower, palm, arm],
            wiggle((x_base, -10), base_rot=x_side * 30, amp=20, period=25, phase=phase),
            name="claw_group"
        )

    def eye_stalk(x, phase):
        # Use dark_c for the stalk so it stands out against the bright body_c
        stalk = outlined(path([(0, 0), (0, -55)], closed=False), dark_c, 10, name="stalk")
        # Larger, more prominent eye
        e = eye((0, -55), w=44, h=44, iris="#000000", white="#ffffff", blink_at=45 + int(phase * 10))
        return group([e, stalk], wiggle((x, -25), amp=8, period=40, phase=phase), name="eye_stalk")

    highlights = [
        filled(ellipse(50, 25, (-40, -35)), highlight_c, transform(opacity=50), name="shine"),
        filled(ellipse(30, 15, (55, -20)), highlight_c, transform(opacity=40), name="shine"),
    ]

    # Render order: index 0 is FRONT.
    # Front-to-back: Eyes > Claws > Highlights > Smile > Body > Legs
    return [
        eye_stalk(-40, 0.0),
        eye_stalk(40, 0.4),
        claw(-1, 0.0),
        claw(1, 0.5),
        highlights[0],
        highlights[1],
        smile(65, 22, y=15, color=dark_c, w=8),
        filled(ellipse(190, 135), body_c, name="body"),
        leg(-1, 15, 0.1), leg(-1, 35, 0.3), leg(-1, 55, 0.5),
        leg(1, 15, 0.2), leg(1, 35, 0.4), leg(1, 55, 0.6),
    ]
