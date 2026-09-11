from critter_parts import dot_eye, wiggle
from lottie_kit import ellipse, filled, group, outlined, path


def porcupine():
    body_c, spike_c = "#455A64", "#90A4AE"
    spikes = group([outlined(path([(0, 0), (x, y)], False), spike_c, 3) for x, y in [(-80, -80), (-40, -100), (0, -110), (40, -100), (80, -80)]],
                   wiggle((0, 0), amp=5, period=30), name="spikes")
    return [
        spikes,
        dot_eye((-35, -10), 12, color="#FFFFFF"), dot_eye((35, -10), 12, color="#FFFFFF"),
        filled(ellipse(170, 150), body_c, name="body"),
        filled(ellipse(20, 20, (0, 10)), "#212121", name="nose"),
    ]
