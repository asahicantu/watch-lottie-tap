"""Generates the bundled Lottie animations for Tap a Critter.

Run:  python tools/gen_critters.py
Out:  app/src/main/assets/animations/<critter>.json

Every animation is 300x300, 30 fps, 3 seconds, built from plain shape layers so
it renders identically on a watch as it does in lottie-web.

  lottie_kit.py      Bodymovin JSON primitives
  critter_parts.py   shared features: idle bob, blinking eyes, wiggling ears
  critters_set_a.py  the first ten
  critters_set_b.py  the other twenty
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from critter_parts import critter  # noqa: E402
from critters_set_a import SET_A  # noqa: E402
from critters_set_b import SET_B  # noqa: E402
from lottie_kit import write  # noqa: E402

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "app", "src", "main", "assets", "animations",
)

CRITTERS = dict(SET_A)
CRITTERS.update(SET_B)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0
    for name in sorted(CRITTERS):
        out = os.path.join(OUT_DIR, name + ".json")
        write(critter(name, CRITTERS[name]()), out)
        size = os.path.getsize(out)
        total += size
        print("wrote %-16s %6d bytes" % (os.path.basename(out), size))
    print("-" * 34)
    print("%-16s %6d animations, %.1f kB" % ("total", len(CRITTERS), total / 1024.0))


if __name__ == "__main__":
    main()
