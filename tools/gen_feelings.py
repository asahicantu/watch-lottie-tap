"""Generates the bundled Lottie animations for the Feelings category.

Run:  python tools/gen_feelings.py
Out:  app/src/main/assets/animations/feelings/<feeling>.json

Every animation is 300x300, 30 fps, 3 seconds, matching the critter
animations' format. Mirrors gen_critters.py exactly, one directory over.

  lottie_kit.py       Bodymovin JSON primitives
  feeling_parts.py     shared features: face, eyes, mouths, motion signatures
  feelings/           one file per feeling, named after it
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import feelings  # noqa: E402
from feeling_parts import feeling  # noqa: E402
from lottie_kit import write  # noqa: E402

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "app", "src", "main", "assets", "animations", "feelings",
)

FEELINGS = feelings.load_all()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0
    animations_data = {}
    for name in sorted(FEELINGS):
        out = os.path.join(OUT_DIR, name + ".json")
        try:
            parts, motion = FEELINGS[name]()
            animation = feeling(name, parts, motion)
            write(animation, out)
            animations_data[name] = animation
            size = os.path.getsize(out)
            total += size
            print("wrote %-16s %6d bytes" % (os.path.basename(out), size))
        except Exception as e:
            print("failed to write %s: %s" % (name, e))

    # Also write a JS file for the gallery (avoids CORS issues when opening file://)
    names_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "preview", "feelings_data.js")
    with open(names_js_path, "w") as f:
        f.write("const FEELINGS_DATA = ")
        json.dump(animations_data, f)
        f.write(";")
    print("wrote %-16s (for gallery)" % "feelings_data.js")

    print("-" * 34)
    print("%-16s %6d animations, %.1f kB" % ("total", len(FEELINGS), total / 1024.0))


if __name__ == "__main__":
    main()
