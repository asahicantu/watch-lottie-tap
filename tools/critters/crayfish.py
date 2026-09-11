import math
from critter_parts import eye, triangle, wiggle, FRAMES
from lottie_kit import animated, ellipse, filled, group, outlined, path, rect, transform


def crayfish():
    shell_c, dark_c, highlight_c = "#BF360C", "#872605", "#D84315"

    def antenna(x_side, phase):
        # Long, sweeping, wiggling antenna
        return outlined(
            path([(0, 0), (50 * x_side, -80), (100 * x_side, -130)], closed=False),
            shell_c, 5,
            wiggle((20 * x_side, -60), base_rot=x_side * 10, amp=20, period=40, phase=phase),
            name="antenna"
        )

    def leg(x_side, y_pos, phase):
        # Small bent walking legs attached to the side
        return outlined(
            path([(0, 0), (25 * x_side, 10), (35 * x_side, 30)], closed=False),
            shell_c, 6,
            wiggle((60 * x_side, y_pos), base_rot=0, amp=12, period=25, phase=phase),
            name="leg"
        )

    def claw(x_side, phase):
        # Elongated lobster-style pincers that snap
        x_base = 100 * x_side

        # Pincer jaws
        lower = filled(ellipse(45, 80, (20 * x_side, -20)), shell_c, name="lower")
        upper = filled(ellipse(40, 70, (20 * x_side, -20)), dark_c,
                       transform(rotation=animated([(0, 0), (15, -25 * x_side), (30, 0), (FRAMES, 0)])),
                       name="upper")

        arm = filled(rect(20, 55, (0, 25), radius=10), shell_c, name="arm")
        joint = filled(ellipse(45, 45), shell_c, name="joint")

        return group(
            [upper, lower, joint, arm],
            wiggle((x_base, -20), base_rot=x_side * 20, amp=22, period=30, phase=phase),
            name="claw_group"
        )

    # Segmented tail segments tapering away
    tail_segments = []
    for i in range(4):
        y_off = 70 + i * 22
        w = 120 - i * 15
        h = 45
        tail_segments.append(
            filled(ellipse(w, h), shell_c,
                   wiggle((0, y_off), amp=5, period=35, phase=i * 0.15),
                   name=f"tail_seg_{i}")
        )

    # Tail fan (uropods and telson)
    tail_fan = group([
        filled(triangle(45, 55, pos=(-35, 0), tilt=-12), dark_c, name="side_fan"),
        filled(triangle(45, 65, pos=(0, 0)), shell_c, name="center_fan"),
        filled(triangle(45, 55, pos=(35, 0), tilt=12), dark_c, name="side_fan")
    ], transform(pos=(0, 160), rotation=180), name="tail_fan")

    # Body parts ordered from top (front) to bottom (back)
    return [
        antenna(-1, 0.0), antenna(1, 0.4),
        eye((-38, -48), 30, 30, iris="#000000", white="#ffffff", blink_at=48),
        eye((38, -48), 30, 30, iris="#000000", white="#ffffff", blink_at=55),
        claw(-1, 0.0), claw(1, 0.5),
        filled(ellipse(140, 170, (0, -15)), shell_c, name="cephalothorax"),
        leg(-1, 5, 0.1), leg(-1, 25, 0.3), leg(-1, 45, 0.5),
        leg(1, 5, 0.2), leg(1, 25, 0.4), leg(1, 45, 0.6),
    ] + tail_segments + [tail_fan]
