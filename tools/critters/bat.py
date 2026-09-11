from critter_parts import dot_eye, smile, triangle, wiggle
from lottie_kit import animated, ellipse, filled, group, outlined, path, transform


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
        # Pull the fingers back toward the wrist on each downstroke.  Scaling
        # from the wrist, rather than the centre, makes the membrane curl.
        curl_keys = []
        for frame in range(0, 90, 18):
            curl_keys.extend([
                (frame, [100, 100]),
                (frame + 5, [76, 91]),
                (frame + 10, [64, 84]),
                (frame + 15, [86, 96]),
            ])
        curl_keys.append((90, [100, 100]))
        struts = [outlined(path([(4, -8), wrist], closed=False), bone, 5,
                           name="arm"),
                  outlined(path([wrist, (64, -62)], closed=False), bone, 4,
                           name="thumb")]
        struts += [outlined(path([wrist, t], closed=False), bone, 3,
                            name="finger") for t in tips]
        curled_shape = group(
            struts + [outlined(path(outline), bone, 3, name="edge"),
                      filled(path(outline), membrane, name="membrane")],
            transform(anchor=wrist, scale=animated(curl_keys)), name="curled-web")
        # The whole wing swings from the shoulder; the left one is the same
        # drawing mirrored, so both flap together while the web folds inward.
        return group(
            [curled_shape],
            wiggle((46 * mirror, -6), base_rot=-12 * mirror, amp=30 * mirror,
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

    belly = group([
        outlined(path([(-19, 53), (0, 59), (19, 53)], closed=False), bone, 3,
                 name="upper-rib"),
        outlined(path([(-22, 70), (0, 76), (22, 70)], closed=False), bone, 3,
                 name="middle-rib"),
        outlined(path([(-17, 87), (0, 92), (17, 87)], closed=False), bone, 3,
                 name="lower-rib"),
        filled(ellipse(82, 92, (0, 72)), deep, name="belly-shadow"),
    ], name="segmented-belly")

    return [
        fangs,
        smile(46, 10, y=34, color=deep, w=5),
        filled(triangle(20, 15), deep,
               transform(pos=(0, 22), rotation=180), name="nose"),
        filled(ellipse(78, 58, (0, 32)), muzzle_c, name="muzzle"),
        outlined(path([(-49, -34), (-32, -40), (-16, -34)], closed=False), deep, 5,
                 name="left-brow"),
        outlined(path([(16, -34), (32, -40), (49, -34)], closed=False), deep, 5,
                 name="right-brow"),
        dot_eye((-32, -18), 10, color="#FFFFFF"),
        dot_eye((32, -18), 10, color="#FFFFFF"),
        filled(ellipse(150, 128), fur, name="head"),
        belly,
        filled(ellipse(92, 104, (0, 76)), fur, name="body"),
        ear(-44, 0.0), ear(44, 0.5),
        wing(-1, 0.0), wing(1, 0.0),
    ]
