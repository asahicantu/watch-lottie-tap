"""Generates the bundled Lottie animations for Tap a Critter.

Run:  python tools/gen_critters.py
Out:  app/src/main/assets/animations/<critter>.json

Every animation is 300x300, 30 fps, 3 seconds, built from plain shape layers so
it renders identically on a watch as it does in lottie-web.

  lottie_kit.py      Bodymovin JSON primitives
  critter_parts.py   shared features: idle bob, blinking eyes, wiggling ears
  critters/          one file per animal, named after it
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import critters  # noqa: E402
from critter_parts import critter  # noqa: E402
from lottie_kit import write  # noqa: E402

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "app", "src", "main", "assets", "animations",
)

CRITTERS = critters.load_all()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0
    names = []
    for name in sorted(CRITTERS):
        out = os.path.join(OUT_DIR, name + ".json")
        try:
            write(critter(name, CRITTERS[name]()), out)
            size = os.path.getsize(out)
            total += size
            names.append(name)
            print("wrote %-16s %6d bytes" % (os.path.basename(out), size))
        except Exception as e:
            print("failed to write %s: %s" % (name, e))
            # Still add it to names if it exists to keep the gallery coherent
            if os.path.exists(out):
                names.append(name)

    # Write a manifest for the gallery viewer
    manifest_path = os.path.join(OUT_DIR, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(names, f)
    print("wrote %-16s (for gallery)" % "manifest.json")

    # Also write a JS file for the gallery (avoids CORS issues when opening file://)
    names_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview", "animations_data.js")
    animations_data = {}
    for name in sorted(CRITTERS):
        animations_data[name] = critter(name, CRITTERS[name]())

    with open(names_js_path, "w") as f:
        f.write("const ANIMATIONS = ")
        json.dump(animations_data, f)
        f.write(";")
    print("wrote %-16s (for gallery)" % "animations_data.js")

    print("-" * 34)
    print("%-16s %6d animations, %.1f kB" % ("total", len(CRITTERS), total / 1024.0))


if __name__ == "__main__":
    main()
