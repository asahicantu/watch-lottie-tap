from critter_parts import eye, smile, wiggle
from lottie_kit import ellipse, filled, group, rect, transform


def llama():
    wool, muzzle_c, pink = "#E0E0E0", "#F5F5F5", "#F8BBD0"

    # Banana ears
    def ear(x, ph):
        return group(
            [filled(rect(20, 70, (0, -35), radius=10), pink, name="inner"),
             filled(rect(34, 100, (0, -45), radius=17), wool, name="outer")],
            wiggle((x, -74), base_rot=x * 0.25, amp=8, period=32, phase=ph), name="ear")

    # Fluffy wool on top of the head
    puffs = [
        filled(ellipse(50, 50, (-40, -80)), wool, name="puff"),
        filled(ellipse(54, 54, (0, -90)), wool, name="puff"),
        filled(ellipse(50, 50, (40, -80)), wool, name="puff"),
    ]

    return [
        smile(44, 16, y=52, color="#9E9E9E", w=5),
        group([filled(ellipse(14, 10, (-16, 0)), "#BDBDBD", name="nostril"),
               filled(ellipse(14, 10, (16, 0)), "#BDBDBD", name="nostril")],
              transform(pos=(0, 42)), name="nostrils"),
        filled(ellipse(90, 74, (0, 48)), muzzle_c, name="muzzle"),
        eye((-40, -22), 34, 38, iris="#424242"),
        eye((40, -22), 34, 38, iris="#424242"),
        filled(ellipse(164, 184), wool, name="head"),
    ] + puffs + [ear(-62, 0.0), ear(62, 0.5)]
