from critter_parts import dot_eye, smile, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def ant():
    body, shade, highlight = "#B22222", "#7F1D1D", "#E85D45"
    line = "#4A1717"

    def leg(side, y, phase):
        """A two-jointed leg that swings independently from the thorax."""
        return outlined(
            path([(0, 0), (side * 28, 10), (side * 51, 38)], closed=False,
                 tangents=[((0, 0), (side * 12, 4)),
                           ((side * -10, -4), (side * 12, 12)),
                           ((side * -10, -12), (0, 0))]),
            line, 7,
            wiggle((side * 44, y), base_rot=side * 5, amp=8, period=22,
                   phase=phase),
            name="leg")

    def antenna(side, phase):
        return group([
            filled(ellipse(18, 18, (side * 25, -43)), highlight, name="tip"),
            outlined(path([(0, 0), (side * 12, -26), (side * 25, -43)],
                          closed=False), line, 6, name="stalk"),
        ], wiggle((side * 33, -74), base_rot=side * 8, amp=9, period=24,
                   phase=phase), name="antenna")

    return [
        # Facial features come first so they remain above the head segment.
        smile(40, 12, y=-10, color=line, w=5),
        dot_eye((-34, -31), 14), dot_eye((34, -31), 14),
        filled(ellipse(22, 12, (-31, -5)), highlight, name="left-cheek"),
        filled(ellipse(22, 12, (31, -5)), highlight, name="right-cheek"),
        filled(ellipse(112, 98, (0, -32)), body, name="head"),
        filled(ellipse(69, 64, (0, 34)), body, name="thorax"),
        filled(ellipse(48, 24, (0, 70)), highlight, name="abdomen-shine"),
        filled(ellipse(90, 73, (0, 85)), body, name="abdomen"),
        leg(-1, 7, 0.00), leg(1, 7, 0.50),
        leg(-1, 34, 0.20), leg(1, 34, 0.70),
        leg(-1, 61, 0.40), leg(1, 61, 0.90),
        antenna(-1, 0.00), antenna(1, 0.50),
        # Slightly larger, darker silhouettes make the segments read as layered.
        filled(ellipse(78, 72, (0, 39)), shade, name="thorax-shadow"),
        filled(ellipse(99, 82, (0, 91)), shade, name="abdomen-shadow"),
    ]
