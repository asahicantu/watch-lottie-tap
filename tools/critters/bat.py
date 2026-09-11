from critter_parts import dot_eye, smile, triangle, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, transform


def bat():
    fur, membrane, bone = "#37474F", "#2E3B43", "#7A8F99"
    ear_in, muzzle_c, deep = "#4A2F38", "#455A64", "#1C252A"

    # A bat wing is an arm: one bone out to the wrist, then four fingers with
    # the membrane scalloped between their tips. The old wing was a flat
    # ellipse squashed on the y axis, which read as a lump rather than a flap.
    wrist = (52, -40)
    tips = [(104, -52), (112, 6), (96, 50), (70, 80)]
    outline = [(0, -10), wrist, (104, -52), (84, -12), (112, 6), (82, 24),
               (96, 50), (66, 48), (70, 80), (16, 52), (0, 18)]

    def wing(mirror, phase):
        struts = [outlined(path([(4, -8), wrist], closed=False), bone, 5,
                           name="arm"),
                  outlined(path([wrist, (64, -62)], closed=False), bone, 4,
                           name="thumb")]
        struts += [outlined(path([wrist, t], closed=False), bone, 3,
                            name="finger") for t in tips]
        # the whole wing swings from the shoulder; the left one is the same
        # drawing mirrored, so both flap in step the way a bat's do
        return group(
            struts + [outlined(path(outline), bone, 3, name="edge"),
                      filled(path(outline), membrane, name="membrane")],
            wiggle((46 * mirror, -6), base_rot=-8 * mirror, amp=20 * mirror,
                   period=18, phase=phase, scale=(100 * mirror, 100)),
            name="wing")

    def ear(x, phase):
        return group(
            [filled(triangle(30, 52, pos=(0, -6)), ear_in, name="inner"),
             filled(triangle(54, 80), fur, name="outer")],
            wiggle((x, -44), base_rot=x * 0.32, amp=5, period=34, phase=phase),
            name="ear")

    fangs = group(
        [filled(triangle(11, 16, pos=(-12, 0)), "#F7F7F2", name="fang"),
         filled(triangle(11, 16, pos=(12, 0)), "#F7F7F2", name="fang")],
        transform(pos=(0, 44), rotation=180), name="fangs")

    return [
        fangs,
        smile(46, 10, y=34, color=deep, w=5),
        filled(triangle(20, 15), deep,
               transform(pos=(0, 22), rotation=180), name="nose"),
        filled(ellipse(78, 58, (0, 32)), muzzle_c, name="muzzle"),
        dot_eye((-32, -18), 10, color="#FFFFFF"),
        dot_eye((32, -18), 10, color="#FFFFFF"),
        filled(ellipse(150, 128), fur, name="head"),
        ear(-44, 0.0), ear(44, 0.5),
        wing(-1, 0.0), wing(1, 0.0),
    ]
