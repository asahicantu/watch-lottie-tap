"""Copies auditioned critter sounds into the app and wires them up.

    python tools/wire_sounds.py                # wire every critter with a sound
    python tools/wire_sounds.py --only cat dog  # a subset
    python tools/wire_sounds.py --dry-run       # show what would change, write nothing

Picks up `sounds/<id>.<ext>` — the single file you have already chosen by ear
as the winner (when `fetch_sounds.py` ran with `--candidates N > 1`, the
candidates land in `sounds/<id>/` for audition; save the one you pick as
`sounds/<id>.<ext>` before running this). Copies it into
`app/src/main/res/raw/<id>.<ext>` and adds `soundRes = R.raw.<id>` to that
critter's entry in CritterCatalog.kt.

A `sounds/<id>/` directory of un-auditioned candidates is left alone — this
script only ever touches a critter once a single winning file exists for it.
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUNDS_DIR = os.path.join(ROOT, "sounds")
RAW_DIR = os.path.join(ROOT, "app", "src", "main", "res", "raw")
CATALOG = os.path.join(ROOT, "app", "src", "main", "java", "com", "example",
                        "crittertap", "data", "CritterCatalog.kt")

# Same formats fetch_sounds.py can produce (see extension_for() there).
AUDIO_EXTENSIONS = (".ogg", ".mp3", ".wav", ".flac", ".oga", ".m4a")

CRITTER_LINE = re.compile(
    r'critter\(\s*"(?P<id>[a-z0-9_]+)"\s*,\s*(?P<accent>0x[0-9A-Fa-f]+)\s*'
    r'(?P<rest>(?:,[^)]*)?)\)'
)


def catalog_ids(text):
    return [m.group("id") for m in CRITTER_LINE.finditer(text)]


def find_source(critter_id):
    """The single auditioned file at sounds/<id>.<ext>, or None."""
    for ext in AUDIO_EXTENSIONS:
        path = os.path.join(SOUNDS_DIR, critter_id + ext)
        if os.path.isfile(path):
            return path
    return None


def existing_raw(critter_id):
    if not os.path.isdir(RAW_DIR):
        return []
    return [os.path.join(RAW_DIR, name) for name in os.listdir(RAW_DIR)
            if os.path.splitext(name)[0] == critter_id]


def copy_into_raw(critter_id, source, dry_run):
    """
    Android raw resources are named by stripping the extension, so a stale
    `cat.mp3` left behind by an earlier pick would collide with a fresh
    `cat.ogg` at build time. Whatever else is filed under this id goes first.
    """
    ext = os.path.splitext(source)[1].lower()
    dest = os.path.join(RAW_DIR, critter_id + ext)
    stale = [path for path in existing_raw(critter_id) if path != dest]
    if dry_run:
        for path in stale:
            print("  would remove %s" % os.path.relpath(path, ROOT))
        print("  would copy %s -> %s" % (os.path.relpath(source, ROOT),
                                          os.path.relpath(dest, ROOT)))
        return dest
    os.makedirs(RAW_DIR, exist_ok=True)
    for path in stale:
        os.remove(path)
    with open(source, "rb") as handle:
        data = handle.read()
    with open(dest, "wb") as handle:
        handle.write(data)
    return dest


def wire_factory(text):
    """Extends the `critter(id, accent)` helper to take an optional soundRes."""
    old = (
        "    private fun critter(id: String, accent: Long) =\n"
        '        Critter(id = id, assetPath = "animations/$id.json", accent = Color(accent))'
    )
    new = (
        "    private fun critter(id: String, accent: Long, @RawRes soundRes: Int? = null) =\n"
        '        Critter(id = id, assetPath = "animations/$id.json", accent = Color(accent),\n'
        "                soundRes = soundRes)"
    )
    if old not in text:
        return text, False
    text = text.replace(old, new, 1)
    if "import androidx.annotation.RawRes" not in text:
        text = text.replace(
            "import androidx.compose.ui.graphics.Color",
            "import androidx.annotation.RawRes\nimport androidx.compose.ui.graphics.Color",
            1,
        )
    return text, True


def wire_catalog(text, wired_ids):
    """Adds `soundRes = R.raw.<id>` to each listed critter's entry."""
    if "import com.example.crittertap.R" not in text:
        text = text.replace(
            "import androidx.compose.ui.graphics.Color",
            "import androidx.compose.ui.graphics.Color\nimport com.example.crittertap.R",
            1,
        )

    def replace(match):
        critter_id = match.group("id")
        if critter_id not in wired_ids or "soundRes" in match.group("rest"):
            return match.group(0)          # not ours, or already wired
        return 'critter("%s", %s%s, soundRes = R.raw.%s)' % (
            critter_id, match.group("accent"), match.group("rest"), critter_id)

    return CRITTER_LINE.sub(replace, text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*", help="limit to these critter ids")
    parser.add_argument("--dry-run", action="store_true",
                        help="show what would change, write nothing")
    args = parser.parse_args()

    with open(CATALOG, "r", encoding="utf-8") as handle:
        original = handle.read()
    ids = catalog_ids(original)
    wanted = args.only or ids

    wired, un_auditioned, no_sound = [], [], []
    for critter_id in wanted:
        if critter_id not in ids:
            print("%-11s not in CritterCatalog.kt, skipping" % critter_id)
            continue
        source = find_source(critter_id)
        if source is None:
            if os.path.isdir(os.path.join(SOUNDS_DIR, critter_id)):
                un_auditioned.append(critter_id)
            else:
                no_sound.append(critter_id)
            continue
        dest = copy_into_raw(critter_id, source, args.dry_run)
        print("%-11s %s -> %s" % (critter_id, os.path.relpath(source, ROOT),
                                    os.path.relpath(dest, ROOT)))
        wired.append(critter_id)

    if wired:
        text, changed_factory = wire_factory(original)
        text = wire_catalog(text, set(wired))
        if text != original:
            if args.dry_run:
                print("\nwould update %s" % os.path.relpath(CATALOG, ROOT))
            else:
                with open(CATALOG, "w", encoding="utf-8") as handle:
                    handle.write(text)
                print("\nupdated %s" % os.path.relpath(CATALOG, ROOT))
        else:
            print("\n%s already wired for: %s" % (os.path.relpath(CATALOG, ROOT),
                                                    ", ".join(wired)))

    if un_auditioned:
        print("\nun-auditioned candidates only, nothing wired for: %s"
              % ", ".join(sorted(un_auditioned)))
        print("Pick the best clip from sounds/<id>/, save it as sounds/<id>.<ext>, "
              "and re-run.")
    if no_sound:
        print("\nno sound file at all for:", ", ".join(sorted(no_sound)))


if __name__ == "__main__":
    sys.exit(main())
