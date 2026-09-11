from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path, rect, transform


def beaver():
    fur, dark, tail_c, deep = "#5D4037", "#3E2723", "#2B1B17", "#1A1412"

    # Flat paddle tail. It sits behind the head and only shows below the chin -
    # in front of the face it just hid everything.
    paddle = filled(ellipse(78, 116), tail_c,
                    wiggle((36, 88), base_rot=-22, amp=10, period=40),
                    name="tail")

    # The buck teeth a beaver is known for: two big incisors hanging out of a
    # dark mouth, below the nose.
    mouth = filled(rect(66, 26, (0, 46), radius=10), deep, name="mouth")
    incisors = group(
        [filled(rect(22, 32, (-12, 0), radius=5), "#FFFFFF", name="tooth"),
         filled(rect(22, 32, (12, 0), radius=5), "#FFFFFF", name="tooth")],
        transform(pos=(0, 58)), name="teeth")

    # Whiskers, pale enough to read against the fur they lie on
    whisker = lambda x, y, rot: outlined(path([(0, 0), (x, 0)], closed=False), "#D7CCC8", 3,
                                       transform(pos=(x * 0.4 + (44 if x > 0 else -44), y), rotation=rot), name="whisker")
    whiskers = [
        whisker(50, 24, -10), whisker(54, 36, 0), whisker(50, 48, 10),
        whisker(-50, 24, 10), whisker(-54, 36, 0), whisker(-50, 48, -10)
    ]

    return whiskers + [
        incisors,
        mouth,
        filled(ellipse(36, 26, (0, 14)), deep, name="nose"),
        filled(ellipse(118, 92, (0, 36)), "#4E3629", name="muzzle"), # Darker snout area
        dot_eye((-44, -14), 16), dot_eye((44, -14), 16),
        filled(ellipse(186, 172), fur, name="head"),
        # A broad, soft body gives the beaver a friendly, plush silhouette.
        filled(ellipse(44, 35, (-62, 96)), "#8D6350", name="left-paw"),
        filled(ellipse(44, 35, (62, 96)), "#8D6350", name="right-paw"),
        filled(ellipse(108, 96, (0, 106)), "#B08972", name="round-belly"),
        filled(ellipse(176, 156, (0, 86)), fur, name="round-body"),
        filled(ellipse(194, 170, (0, 92)), dark, name="body-shadow"),
        group([filled(ellipse(44, 44), fur, name="outer"),
               filled(ellipse(28, 28), dark, name="inner")],
              wiggle((-76, -64), amp=5, period=32), name="ear"),
        group([filled(ellipse(44, 44), fur, name="outer"),
               filled(ellipse(28, 28), dark, name="inner")],
              wiggle((76, -64), amp=5, period=32, phase=0.5), name="ear"),
        paddle,
    ]
