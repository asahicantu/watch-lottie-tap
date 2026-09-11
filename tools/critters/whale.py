from critter_parts import FRAMES, dot_eye, wiggle
from lottie_kit import animated, ellipse, filled, group, transform


def whale():
    body_c, belly_c = "#1E88E5", "#BBDEFB"
    def fin(x, ph):
        return filled(ellipse(60, 30), body_c,
                      wiggle((x, 40), base_rot=x * 0.2, amp=10, period=40, phase=ph),
                      name="fin")
    spout = group([filled(ellipse(10, 20, (0, -20)), "#E3F2FD", name="drop") for i in range(3)],
                  transform(pos=(0, -80), scale=animated([(0, [0, 0]), (20, [100, 100]), (40, [0, 0]), (FRAMES, [0, 0])])),
                  name="spout")
    return [
        spout,
        dot_eye((-50, -10), 15), dot_eye((50, -10), 15),
        filled(ellipse(160, 60, (0, 60)), belly_c, name="belly"),
        filled(ellipse(220, 160), body_c, name="body"),
        fin(-100, 0.0), fin(100, 0.5),
    ]
