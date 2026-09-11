import math

from critter_parts import FRAMES, eye, smile
from lottie_kit import (
    animated, ellipse, filled, group, oscillate, path, rect, transform,
)


def squid():
    """A squid, not a triangle on sticks. The old one drew five stiff bars
    that swung through each other into a W, over a flat pink wedge.

    What makes a squid a squid rather than the octopus two files over: a
    pointed torpedo mantle, the pair of fins fluttering at the tip of it, and
    ten limbs instead of eight - eight short arms, and two long feeding
    tentacles that hang past them with a paddle-shaped club on the end.

    The motion is built on the jet cycle rather than on one sine wave shared
    out among the parts: mantle, fins, arms, chromatophores and the surge of
    the whole animal all read off PROFILE below, so the squid gathers itself
    and darts instead of wobbling in place.
    """
    skin, deep, pale = "#EE5A76", "#8E1B3F", "#F6A7B6"
    fin_c, cup_c = "#F4869B", "#FDE2E8"

    # ------------------------------------------------------------- the jet --
    # One stroke, twice over the 90-frame loop. Negative levels are the slow
    # refill - the mantle fattens and the arms spread; level 1 is the squeeze
    # four frames later, which stretches the mantle and streamlines the arms
    # behind it.
    JET = 45.0
    PROFILE = ((0.0, 0.0), (20.0, -0.35), (30.0, -0.40), (34.0, 1.0),
               (40.0, 0.30))

    def level_at(t):
        u = t % JET
        pts = list(PROFILE) + [(JET, 0.0)]
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            if t0 <= u <= t1:
                return v0 + (v1 - v0) * ((u - t0) / (t1 - t0))
        return 0.0

    def jet_keys(fn, lag=0.0):
        """The profile mapped through `fn`, repeated across the loop. `lag`
        holds a part a few frames behind whatever drives it."""
        frames = {0.0, float(FRAMES)}
        for cycle in (0, 1):
            for t, _ in PROFILE:
                f = t + cycle * JET + lag
                if 0.0 < f < FRAMES:
                    frames.add(f)
        return animated([(f, fn(level_at(f - lag))) for f in sorted(frames)],
                        ease=(0.2, 0.8))

    def limb(attach, heading, lens, rads, curl, phase, amp, cups=0, club=None,
             sweep=0.55, lag=0.0):
        """A tapered chain of rounded capsules, each joint parented to the end
        of the one before it. The outer joints ride a sine, each swinging
        wider and later than its parent so the bend travels out to the tip;
        the root instead follows the jet, swinging the whole limb in toward
        the body axis as the mantle squeezes."""
        node = None
        for s in reversed(range(len(lens))):
            length, r = lens[s], rads[s]
            items = []
            if s == len(lens) - 1 and club is not None:
                cw, ch = club
                items += [filled(ellipse(cw * 0.34, cw * 0.34,
                                         (length + cw * (f - 0.5) * 0.6,
                                          -curl * ch * 0.2)), cup_c, name="cup")
                          for f in (0.3, 0.7)]
                items.append(filled(ellipse(cw, ch, (length, 0)), fin_c,
                                    name="club"))
            if s < cups:
                items += [filled(ellipse(r * 0.48, r * 0.48,
                                         (length * f, -curl * r * 0.42)),
                                 cup_c, name="cup")
                          for f in (0.3, 0.72)]
            items.append(filled(rect(length + 2 * r, 2 * r, (length * 0.5, 0),
                                     radius=r), skin, name="limb"))
            if node is not None:
                items.append(node)
            if s == 0:
                rot = jet_keys(
                    lambda level, h=heading: 90 + (h - 90) * (1 - sweep * level)
                    + curl * 1.5, lag=lag)
            else:
                rot = oscillate(FRAMES, curl * (1.5 + 3.0 * s),
                                amp * (1 + 0.7 * s), 30, phase + s * 0.16,
                                steps=3)
            node = group(items,
                         transform(pos=attach if s == 0 else (lens[s - 1], 0),
                                   rotation=rot),
                         name="joint")
        return node

    # eight arms in a fan, the outer ones shorter so the bunch tapers
    arms = []
    for i in range(8):
        f = i / 7.0
        spread = (f - 0.5) * 2.0                      # -1 left .. +1 right
        heading = 90 - spread * 46
        attach = (spread * 46, 58 - abs(spread) * 8)
        scale = 1.0 - 0.20 * abs(spread)
        arms.append(limb(attach, heading,
                         [46 * scale, 38 * scale, 30 * scale],
                         [11.5, 8.5, 5.5],
                         -1.0 if spread >= 0 else 1.0,
                         phase=0.10 * i, amp=3.2, cups=2,
                         # the outer arms have furthest to travel and start
                         # last, so the fan closes from the outside in
                         sweep=0.55 + 0.35 * abs(spread),
                         lag=2.0 * abs(spread)))

    # the two feeding tentacles: longer, thinner, slower to react, and clubbed
    tentacles = [limb((x, 52), 90 - x * 0.30, [58, 52, 46],
                      [8.5, 7.0, 5.5], -1.0 if x > 0 else 1.0,
                      phase=0.35 if x > 0 else 0.85, amp=2.0, club=(38, 24),
                      sweep=0.85, lag=6.0)
                 for x in (-24, 24)]

    def fin(s, phase):
        """A fin at the tip of the mantle. It ripples on its own while the
        squid coasts, then folds back against the body on the squeeze - the
        ripple flattening out is most of what sells the dart."""
        tip = 92 * s
        keys = []
        for i in range(31):
            t = FRAMES * i / 30.0
            surge = max(level_at(t), 0.0)
            ripple = 7.0 * math.sin(2 * math.pi * (t / 30.0 + phase))
            keys.append((t, ripple * (1 - 0.8 * surge) - 24.0 * surge * s))
        return group([filled(path([(0, -44), (tip, 6), (0, 40)], True,
                                  tangents=[((-tip * 0.1, -18), (tip * 0.42, -14)),
                                            ((-tip * 0.3, -16), (-tip * 0.3, 16)),
                                            ((tip * 0.42, 18), (0, 0))]),
                             fin_c, name="blade")],
                     transform(pos=(24 * s, -58), rotation=animated(keys)),
                     name="fin")

    # a pointed mantle: apex on top, shoulders below the fins, rounded off
    # where the head begins
    mantle = filled(path([(0, -128), (66, -22), (0, 32), (-66, -22)], True,
                         tangents=[((-13, 30), (13, 30)),
                                   ((6, -54), (-2, 30)),
                                   ((38, 4), (-38, 4)),
                                   ((2, 30), (-6, -54))]),
                    skin, name="mantle")
    # chromatophores: the speckling a squid flushes across its mantle. They
    # fade while it coasts and flare on the stroke, the way the real animal
    # flushes when it startles.
    speckles = group([filled(ellipse(r, r, (sx, sy)), deep, name="speckle")
                      for sx, sy, r in ((-20, -80, 8), (18, -66, 7),
                                        (-28, -44, 8), (26, -34, 7),
                                        (0, -56, 6), (-4, -18, 7))],
                     transform(opacity=jet_keys(
                         lambda level: 42 + 58 * max(level, 0.0))),
                     name="speckles")

    # the mantle narrows and stretches as it empties, taking the fins and the
    # speckling with it
    body = group([speckles, mantle, fin(-1, 0.0), fin(1, 0.5)],
                 transform(scale=jet_keys(
                     lambda level: [100 - 14 * level, 100 + 13 * level])),
                 name="body")

    face = [
        smile(42, 11, y=46, color=deep, w=5),
        eye((-48, 14), 34, 38, iris="#5E1030"),
        eye((48, 14), 34, 38, iris="#5E1030"),
        filled(ellipse(132, 84, (0, 22)), pale, name="head"),
    ]

    # and the whole animal gathers, then darts, apex first
    return [group(arms + tentacles + face + [body],
                  transform(pos=jet_keys(
                      lambda level: [0, 5 * max(-level, 0.0)
                                     - 17 * max(level, 0.0)], lag=2.0)),
                  name="swim")]
