"""Fetches freely-licensed critter sounds from Wikimedia Commons.

    python tools/fetch_sounds.py                 # search + download into sounds/
    python tools/fetch_sounds.py --report        # search only, download nothing
    python tools/fetch_sounds.py --only cat dog  # a subset

Commons is used because it is the only large animal-audio source reachable from
a script with no credentials: it has an open API, no key, no account, and it
publishes a machine-readable licence per file. Freesound and Pixabay both need
API keys, xeno-canto retired its keyless v2 API, and the BBC archive is licensed
for non-commercial use only.

Coverage is uneven — Commons is an encyclopedia's media store, not a sound
effects library — so expect gaps and expect to run this more than once with
different search terms.

Nothing here can judge whether a clip *sounds* like the animal it claims to be,
or whether it is pleasant. Everything lands in `sounds/` for a human to
audition. Only files that decode, are a sane length, and carry a licence
permitting redistribution are kept.
"""

import argparse
import json
import os
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

API = "https://commons.wikimedia.org/w/api.php"
UA = "CritterTapSoundFetcher/1.0 (Wear OS hobby app; https://commons.wikimedia.org)"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "sounds")
CREDITS = os.path.join(ROOT, "SOUND_CREDITS.md")

MIN_SECONDS, MAX_SECONDS = 0.25, 6.0
MIN_BYTES, MAX_BYTES = 3_000, 4_000_000

# Commons rate-limits hard; anything under a second earns a 429.
REQUEST_GAP = 1.4

AUDIO_MIMES = ("audio/", "application/ogg")

# Where a critter's audio might live. Commons files a recording under whichever
# category the uploader chose, so both the scientific name and the common-noun
# phrasing have to be tried — the cat meows live in "Audio files of cats
# meowing", while the cow lives under "Audio files of Bos taurus".
CATEGORIES = {
    "cat": ["cats meowing", "Felis catus", "Felis silvestris catus"],
    "dog": ["dogs barking", "Canis lupus familiaris", "Canis familiaris"],
    "cow": ["Bos taurus", "cattle"],
    "duck": ["Anas platyrhynchos", "Anatidae", "ducks"],
    "frog": ["Anura", "Rana temporaria", "Pelophylax", "frogs"],
    "lion": ["Panthera leo", "lions"],
    "bee": ["Apis mellifera", "Bombus", "bees"],
    "sheep": ["Ovis aries", "Ovis", "sheep"],
    "owl": ["Strix aluco", "Bubo bubo", "Strigidae", "owls"],
    "pig": ["Sus scrofa domesticus", "Sus scrofa", "pigs"],
    "horse": ["Equus ferus caballus", "Equus caballus", "horses"],
    "elephant": ["Loxodonta africana", "Elephas maximus", "Elephantidae"],
    "monkey": ["Macaca", "Cercopithecidae", "Cebidae", "monkeys"],
    "penguin": ["Spheniscidae", "Aptenodytes forsteri", "Spheniscus"],
    "tiger": ["Panthera tigris", "tigers"],
    "bear": ["Ursus arctos", "Ursidae", "bears"],
    "rabbit": ["Oryctolagus cuniculus", "Leporidae", "rabbits"],
    "mouse": ["Mus musculus", "Apodemus", "mice"],
    "fox": ["Vulpes vulpes", "foxes"],
    "wolf": ["Canis lupus", "wolves"],
    "rooster": ["Gallus gallus domesticus", "Gallus gallus", "roosters"],
    "goat": ["Capra aegagrus hircus", "Capra hircus", "goats"],
    "donkey": ["Equus africanus asinus", "Equus asinus", "donkeys"],
    "panda": ["Ailuropoda melanoleuca"],
    "koala": ["Phascolarctos cinereus"],
    "giraffe": ["Giraffa camelopardalis", "Giraffa"],
    "hippo": ["Hippopotamus amphibius"],
    "crocodile": ["Crocodylus niloticus", "Crocodylia", "Alligator mississippiensis"],
    "snake": ["Crotalus", "Serpentes", "Naja"],
    "parrot": ["Psittacidae", "Psittaciformes", "Ara", "Melopsittacus undulatus"],
}

# Free-text fallback when the categories come up empty.
QUERIES = {
    "cat": ["cat meow"], "dog": ["dog barking"], "cow": ["cow moo"],
    "duck": ["duck quack"], "frog": ["frog croak"], "lion": ["lion roar"],
    "bee": ["bee buzzing"], "sheep": ["sheep bleat"], "owl": ["owl hoot"],
    "pig": ["pig grunt"], "horse": ["horse whinny"], "elephant": ["elephant trumpet"],
    "monkey": ["monkey call"], "penguin": ["penguin call"], "tiger": ["tiger growl"],
    "bear": ["bear growl"], "rabbit": ["rabbit squeal"], "mouse": ["mouse squeak"],
    "fox": ["fox call"], "wolf": ["wolf howl"], "rooster": ["cock crowing"],
    "goat": ["goat bleat"], "donkey": ["donkey braying"], "panda": ["panda call"],
    "koala": ["koala bellow"], "giraffe": ["giraffe sound"], "hippo": ["hippopotamus call"],
    "crocodile": ["crocodile hiss"], "snake": ["snake hiss"], "parrot": ["parrot call"],
}


# --------------------------------------------------------------------------- #
# polite HTTP
# --------------------------------------------------------------------------- #

_last_request = [0.0]


def get(url, tries=4):
    """One request, never faster than REQUEST_GAP, backing off on a 429."""
    for attempt in range(tries):
        wait = REQUEST_GAP - (time.time() - _last_request[0])
        if wait > 0:
            time.sleep(wait)
        _last_request[0] = time.time()
        try:
            request = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code in (429, 503) and attempt < tries - 1:
                backoff = 4 * (attempt + 1)
                print("  (rate limited, waiting %ds)" % backoff, end="", flush=True)
                time.sleep(backoff)
                continue
            raise
    raise RuntimeError("gave up after %d attempts" % tries)


def api(**params):
    params.setdefault("format", "json")
    params.setdefault("action", "query")
    return json.loads(get(API + "?" + urllib.parse.urlencode(params)))


# --------------------------------------------------------------------------- #
# licences
# --------------------------------------------------------------------------- #

def licence_is_free(short_name, code):
    """True for licences that allow redistribution inside an app."""
    text = ("%s %s" % (short_name, code)).lower()
    words = re.split(r"[^a-z0-9]+", text)
    if "nc" in words or "nd" in words:                 # NonCommercial / NoDerivatives
        return False
    if "fair" in words or "non-free" in text:
        return False
    return (
        "cc0" in text
        or "public domain" in text
        or text.strip().startswith("pd")
        or "cc-by" in text
        or "cc by" in text
    )


SPEECH_MARKERS = re.compile(
    r"pronunciation|pronounce|lingua libre|spoken (word|version)|"
    r"audio recording of the word|wiktionary",
    re.IGNORECASE,
)


def is_someone_saying_the_word(hit):
    """
    Commons is full of Wiktionary pronunciation clips, and they are filed in the
    animal's own category — `Qc-lapin.ogg` sits in "Audio files of Oryctolagus
    cuniculus" but is a man saying "lapin". Without this the app would announce
    "Rabbit" and then play a human voice saying it again in French.
    """
    haystack = " ".join((hit.get("categories", ""), hit.get("description", ""),
                         hit.get("title", "")))
    return bool(SPEECH_MARKERS.search(haystack))


# The noise each critter makes, used to rank candidates. A file whose title or
# description mentions the animal or its call is far more likely to be the right
# recording than one that merely sits in the same taxonomic category - domestic
# dogs are Canis lupus, so the wolf category is full of barking.
ACTIONS = {
    "cat": ["meow", "purr"], "dog": ["bark", "woof"], "cow": ["moo", "low"],
    "duck": ["quack"], "frog": ["croak", "ribbit"], "lion": ["roar"],
    "bee": ["buzz", "hum"], "sheep": ["bleat", "baa"], "owl": ["hoot", "call"],
    "pig": ["grunt", "oink", "squeal"], "horse": ["neigh", "whinny", "wiehern"],
    "elephant": ["trumpet"], "monkey": ["call", "hoot"], "penguin": ["call", "bray"],
    "tiger": ["roar", "growl"], "bear": ["growl", "roar"], "rabbit": ["squeal"],
    "mouse": ["squeak"], "fox": ["bark", "scream", "call"], "wolf": ["howl"],
    "rooster": ["crow", "cock"], "goat": ["bleat"], "donkey": ["bray"],
    "panda": ["bleat", "call"], "koala": ["bellow", "call"], "giraffe": ["snort", "hum"],
    "hippo": ["grunt", "snort"], "crocodile": ["hiss", "bellow"],
    "snake": ["hiss", "rattle"], "parrot": ["squawk", "call"],
}


def relevance(critter, hit):
    """How strongly the file's own words tie it to this critter. Higher is better."""
    haystack = (" ".join((hit.get("title", ""), hit.get("description", "")))).lower()
    terms = {critter, critter + "s"}
    for name in CATEGORIES.get(critter, []):
        terms.update(word.lower() for word in name.split() if len(word) > 3)
    score = sum(2 for term in terms if term in haystack)
    score += sum(1 for action in ACTIONS.get(critter, []) if action in haystack)
    return score


# --------------------------------------------------------------------------- #
# duration, without ffmpeg
# --------------------------------------------------------------------------- #

def ogg_duration(data):
    """Seconds, from the granule position on the final Ogg page."""
    first = data.find(b"OggS")
    if first < 0:
        return None
    head = data[first:first + 8192]
    if b"\x01vorbis" in head:
        at = head.index(b"\x01vorbis") + 7
        rate = struct.unpack_from("<I", head, at + 5)[0]   # version(4) channels(1)
    elif b"OpusHead" in head:
        rate = 48000                                       # Opus granules are 48 kHz
    else:
        return None
    last = data.rfind(b"OggS")
    if rate <= 0 or last < 0 or last + 14 > len(data):
        return None
    granule = struct.unpack_from("<q", data, last + 6)[0]
    return granule / float(rate) if granule > 0 else None


def wav_duration(data):
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        return None
    pos, rate, bits, channels = 12, None, None, None
    while pos + 8 <= len(data):
        chunk = data[pos:pos + 4]
        size = struct.unpack_from("<I", data, pos + 4)[0]
        body = pos + 8
        if chunk == b"fmt ":
            channels = struct.unpack_from("<H", data, body + 2)[0]
            rate = struct.unpack_from("<I", data, body + 4)[0]
            bits = struct.unpack_from("<H", data, body + 14)[0]
        elif chunk == b"data" and rate and channels and bits:
            frames = size / float(channels * max(1, bits // 8))
            return frames / rate
        pos = body + size + (size & 1)
    return None


_MP3_RATES = {
    3: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0],   # MPEG1
    2: [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0],       # MPEG2
}
_MP3_SAMPLE_RATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000],
                     0: [11025, 12000, 8000]}


def mp3_duration(data):
    """
    Commons stores most of its wildlife recordings as MP3 — every xeno-canto
    bird upload is one — so skipping the format threw away the best material.
    """
    at = 0
    if data[:3] == b"ID3":                       # step over the metadata tag
        size = 0
        for byte in data[6:10]:
            size = (size << 7) | (byte & 0x7F)   # syncsafe integer
        at = 10 + size

    while at + 4 <= len(data) - 4:
        if data[at] == 0xFF and (data[at + 1] & 0xE0) == 0xE0:
            header = data[at:at + 4]
            version = (header[1] >> 3) & 0x03    # 3 = MPEG1, 2 = MPEG2, 0 = MPEG2.5
            layer = (header[1] >> 1) & 0x03      # 1 = Layer III
            bitrate_index = (header[2] >> 4) & 0x0F
            rate_index = (header[2] >> 2) & 0x03
            if layer == 1 and version in _MP3_RATES and rate_index < 3 \
                    and 0 < bitrate_index < 15:
                bitrate = _MP3_RATES[version][bitrate_index] * 1000
                sample_rate = _MP3_SAMPLE_RATES[version][rate_index]
                per_frame = 1152 if version == 3 else 576
                # A Xing/Info header carries an exact frame count for VBR files.
                window = data[at:at + 1024]
                for tag in (b"Xing", b"Info"):
                    found = window.find(tag)
                    if found >= 0 and found + 12 <= len(window):
                        flags = struct.unpack_from(">I", window, found + 4)[0]
                        if flags & 1:
                            frames = struct.unpack_from(">I", window, found + 8)[0]
                            if frames:
                                return frames * per_frame / float(sample_rate)
                if bitrate:
                    return (len(data) - at) * 8 / float(bitrate)   # assume CBR
            at += 1
        else:
            at += 1
    return None


def looks_like_mp3(data):
    if data[:3] == b"ID3":
        return True
    return len(data) > 1 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0


def duration_of(data):
    if data[:4] == b"OggS":
        return ogg_duration(data)
    if data[:4] == b"RIFF":
        return wav_duration(data)
    if looks_like_mp3(data):
        return mp3_duration(data)
    return None                                  # webm/flac: playable, not parsed


def extension_for(data):
    """Android sniffs the content, but a sane extension keeps the folder readable."""
    if data[:4] == b"RIFF":
        return ".wav"
    if looks_like_mp3(data):
        return ".mp3"
    return ".ogg"


# --------------------------------------------------------------------------- #
# finding candidates
# --------------------------------------------------------------------------- #

def describe(page):
    info = (page.get("imageinfo") or [{}])[0]
    meta = info.get("extmetadata", {}) or {}

    def field(key):
        return (meta.get(key, {}) or {}).get("value", "") or ""

    def clean(html):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(html))).strip()

    return {
        "title": page.get("title", ""),
        "url": info.get("url", ""),
        "mime": info.get("mime", ""),
        "size": info.get("size", 0),
        "licence": clean(field("LicenseShortName")),
        "code": field("License"),
        "author": clean(field("Artist"))[:90],
        "page": info.get("descriptionurl", ""),
        "categories": field("Categories"),
        "description": clean(field("ImageDescription"))[:200],
    }


def files_in_category(name):
    payload = api(generator="categorymembers",
                  gcmtitle="Category:Audio files of " + name,
                  gcmtype="file", gcmlimit="60",
                  prop="imageinfo", iiprop="url|mime|size|extmetadata")
    return [describe(p) for p in payload.get("query", {}).get("pages", {}).values()]


def files_by_search(term):
    payload = api(generator="search", gsrsearch=term, gsrnamespace="6",
                  gsrlimit="20", prop="imageinfo",
                  iiprop="url|mime|size|extmetadata")
    return [describe(p) for p in payload.get("query", {}).get("pages", {}).values()]


def candidates_for(critter, verbose=False):
    seen, keep, rejected = set(), [], []

    def consider(hits, source):
        for hit in hits:
            if hit["title"] in seen or not hit["mime"].startswith(AUDIO_MIMES):
                continue
            seen.add(hit["title"])
            if not (MIN_BYTES <= hit["size"] <= MAX_BYTES):
                rejected.append((hit, "size %d B" % hit["size"]))
                continue
            if not licence_is_free(hit["licence"], hit["code"]):
                rejected.append((hit, "licence %r" % (hit["licence"] or hit["code"] or "?")))
                continue
            if is_someone_saying_the_word(hit):
                rejected.append((hit, "a person pronouncing the word"))
                continue
            hit["source"] = source
            keep.append(hit)

    for name in CATEGORIES.get(critter, []):
        try:
            consider(files_in_category(name), "category:" + name)
        except Exception as error:                              # noqa: BLE001
            print("  ! category %r failed: %s" % (name, error), end="")
        if len(keep) >= 4:
            break

    if not keep:
        for term in QUERIES.get(critter, []):
            try:
                consider(files_by_search(term), "search:" + term)
            except Exception as error:                          # noqa: BLE001
                print("  ! search %r failed: %s" % (term, error), end="")

    # Most obviously on-topic first, then Ogg (always decodable here), then small.
    for hit in keep:
        hit["relevance"] = relevance(critter, hit)
    keep.sort(key=lambda h: (-h["relevance"], 0 if "ogg" in h["mime"] else 1, h["size"]))
    if verbose:
        for hit, why in rejected[:6]:
            print("\n    skipped %-44s %s" % (hit["title"][5:48], why), end="")
    return keep


# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true",
                        help="search and print, download nothing")
    parser.add_argument("--only", nargs="*", help="limit to these critter ids")
    parser.add_argument("--verbose", action="store_true",
                        help="explain why candidates were skipped")
    args = parser.parse_args()

    wanted = args.only or list(CATEGORIES)
    os.makedirs(OUT_DIR, exist_ok=True)
    taken, missing = [], []

    for critter in wanted:
        print("%-11s" % critter, end=" ", flush=True)
        picked = None
        for hit in candidates_for(critter, args.verbose)[:12]:
            if args.report:
                picked = dict(hit, seconds=None)
                break
            try:
                data = get(hit["url"])
            except Exception as error:                          # noqa: BLE001
                print("\n    ! download failed: %s" % error, end="")
                continue
            seconds = duration_of(data)
            if seconds is None or not (MIN_SECONDS <= seconds <= MAX_SECONDS):
                if args.verbose:
                    print("\n    skipped %-44s duration %s" % (
                        hit["title"][5:48],
                        "unreadable" if seconds is None else "%.1fs" % seconds), end="")
                continue
            extension = extension_for(data)
            path = os.path.join(OUT_DIR, critter + extension)
            with open(path, "wb") as handle:
                handle.write(data)
            picked = dict(hit, seconds=seconds, path=path)
            break

        if picked:
            print("%-38s %-12s %6s  rel=%-2s %s" % (
                picked["title"][5:43],
                picked["licence"][:12] or "?",
                ("%.1fs" % picked["seconds"]) if picked.get("seconds") else "",
                picked.get("relevance", "?"),
                (picked.get("description") or "")[:44]))
            taken.append((critter, picked))
        else:
            print("-- nothing usable")
            missing.append(critter)

    if not args.report and taken:
        write_credits(taken)

    print("\n%d of %d critters have a sound in %s" % (len(taken), len(wanted), OUT_DIR))
    if missing:
        print("no luck for:", ", ".join(missing))
        print("These need a hand-picked file, or a source that needs an API key.")


def write_credits(entries):
    lines = [
        "# Sound credits",
        "",
        "Each clip came from Wikimedia Commons under a licence permitting",
        "redistribution. Licences requiring attribution are satisfied by this",
        "file — keep it with the app and reproduce it in the store listing or an",
        "about screen.",
        "",
        "Check each one by ear before shipping it: the fetcher can confirm a",
        "licence and a duration, but not that a clip is the right animal.",
        "",
        "| Critter | File | Licence | Author | What Commons says it is |",
        "| --- | --- | --- | --- | --- |",
    ]
    for critter, hit in sorted(entries):
        title = hit["title"][5:].replace("|", "\\|")
        author = (hit["author"] or "unknown").replace("|", "\\|")
        note = (hit.get("description") or "").replace("|", "/")[:90]
        lines.append("| %s | [%s](%s) | %s | %s | %s |" % (
            critter, title, hit.get("page", ""), hit["licence"] or "?", author, note))
    with open(CREDITS, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("\nwrote", CREDITS)


if __name__ == "__main__":
    sys.exit(main())
