"""Fetches freely-licensed critter sounds from Wikimedia Commons.

    python tools/fetch_sounds.py                    # one clip per critter
    python tools/fetch_sounds.py --candidates 5     # five each, to audition
    python tools/fetch_sounds.py --report           # search only, download nothing
    python tools/fetch_sounds.py --only rooster     # a subset

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

MIN_SECONDS, MAX_SECONDS = 0.25, 12.0
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
    "pig": ["Sus scrofa domesticus", "Sus scrofa", "Suidae", "pigs"],
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
    "rooster": ["Gallus gallus domesticus", "Gallus gallus", "Gallus", "chickens", "roosters"],
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
    "cat":          ["cat meow"],
    "dog":          ["dog barking"],
    "cow":          ["cow moo"],
    "duck":         ["duck quack"],
    "frog":         ["frog croak"],
    "lion":         ["lion roar"],
    "bee":          ["bee buzzing"],
    "sheep":        ["sheep bleat"],
    "owl":          ["owl hoot"],
    "pig":          ["pig grunt"],
    "horse":        ["horse whinny"],
    "elephant":     ["elephant trumpet"],
    "monkey":       ["monkey call"],
    "penguin":      ["penguin call"],
    "tiger":        ["tiger growl"],
    "bear":         ["bear growl"],
    "rabbit":        ["rabbit squeal"],
    "mouse":        ["mouse squeak"],
    "fox":          ["fox call"],
    "wolf":         ["wolf howl"],
    "rooster":      ["rooster crowing"],
    "goat":         ["goat bleat"],
    "donkey":       ["donkey braying"],
    "panda":        ["panda call"],
    "koala":        ["koala bellow"],
    "giraffe":      ["giraffe sound"],
    "hippo":        ["hippopotamus call"],
    "crocodile":    ["crocodile hiss"],
    "snake":        ["snake hiss"],
    "parrot":       ["parrot call"],

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


HUMAN_AUDIO = re.compile(
    # Wiktionary and Lingua Libre pronunciation clips
    r"pronun\w*|pronou\w*|lingua libre|spoken (word|version)|wiktionary|"
    r"audio recording of the word|"
    # vocabulary projects: "Igbo words", "Tyap word for hare or rabbit"
    r"\bwords\b|\bword for\b|"
    # Commons' own categories for human-made noise
    r"sounds created by (people|babies)|whistling|"
    # "Vezo people", "Malagasy language" — language and culture recordings
    r"\b\w+ people\b|\b\w+ language\b",
    re.IGNORECASE,
)

# The naming convention those language projects use: "Goat in Antefasy",
# "Tiger in Vezo" — the animal's name spoken in some language.
WORD_IN_LANGUAGE = re.compile(r"^[\w' -]{1,24} in [A-Z][a-z]+$")


def is_a_person_not_an_animal(hit):
    """
    Commons files human recordings in the animals' own categories, and they come
    in more flavours than plain pronunciation clips:

      Qc-lapin.ogg        a man saying "lapin", in Audio files of Oryctolagus
      Lion-agu.oga        the Igbo word for lion, in "Igbo words"
      Wolf whistle.ogg    a person whistling, in "Sounds created by people"
      Babys rattle.ogg    a toy, in "Sounds created by babies"

    Any of these would have the app announce the animal and then play a human.
    """
    haystack = " ".join((hit.get("categories", ""), hit.get("description", ""),
                         hit.get("title", "")))
    if HUMAN_AUDIO.search(haystack):
        return True
    stem = os.path.splitext(hit.get("title", "")[5:])[0]
    return bool(WORD_IN_LANGUAGE.match(stem))


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


def identity_terms(critter):
    """
    Words that name this animal: the id, its plural, and its scientific names.

    Action words are stripped out even when they appear in a category name.
    "dogs barking" would otherwise contribute *barking* as proof of identity,
    which is exactly how a black-tailed prairie dog won the slot for "dog".
    """
    noises = ACTIONS.get(critter, [])
    terms = {critter, critter + "s"}
    for name in CATEGORIES.get(critter, []):
        for word in name.split():
            word = word.lower()
            if len(word) > 2 and not any(noise in word for noise in noises):
                terms.add(word)
    return terms


# Names that contain a critter's name but are not that critter. A prairie dog
# barks and is filed as a "dog"; Scotch rabbit is cheese on toast.
CONFUSABLE = {
    "dog": ["prairie dog", "dogfish", "dog rose", "dogwood"],
    "cat": ["catfish", "cattle", "catbird", "caterpillar"],
    "rabbit": ["scotch rabbit", "welsh rarebit", "rabbit stew", "jackrabbit"],
    "bear": ["bearing", "bear market", "teddy"],
    "mouse": ["computer mouse", "mouse click", "titmouse"],
    "horse": ["horseshoe", "seahorse", "horsepower"],
    "bee": ["beetle", "beech", "beer"],
    "snake": ["snakeskin"],
    "wolf": ["wolf whistle", "wolfram"],
    "tiger": ["tiger moth", "tiger beetle"],
    "monkey": ["monkey wrench", "monkey puzzle"],
    "cow": ["cattle egret", "cowbird", "cowrie"],
    "pig": ["guinea pig"],
}


def names_something_else(critter, haystack):
    return any(phrase in haystack for phrase in CONFUSABLE.get(critter, []))


def filed_under_another_animal(critter, hit):
    """
    True when Commons has classified the file as some *other* animal.

    This is the reliable version of the confusable-phrase list. The prairie dog
    that kept winning the "dog" slot is described as a "prarie dog" — the
    uploader's typo, which no phrase list would ever have caught — but it is
    filed under `Audio files of Sciuridae`, the squirrel family. A curator has
    already answered the question; reading their answer beats guessing from
    prose.
    """
    taxa = [part[len("audio files of "):].strip().lower()
            for part in hit.get("categories", "").split("|")
            if part.strip().lower().startswith("audio files of ")]
    # "Audio files of 2006" is a date, not a species.
    taxa = [taxon for taxon in taxa if taxon and not taxon.isdigit()]
    if not taxa:
        return False                     # unclassified: fall back to the prose
    terms = identity_terms(critter)
    return not any(re.search(r"\b%s\b" % re.escape(term), taxon)
                   for taxon in taxa for term in terms)


def relevance(critter, hit):
    """
    Returns (identity, action) — how strongly the file names the animal, and how
    strongly it names the noise.

    They are kept apart because matching only the *action* is what let a
    black-tailed prairie dog win the slot for "dog": the file says "barking"
    but never "dog". A candidate that cannot name the animal is not a candidate.

    Matching is whole-word, so "cat" no longer matches *cattle* and "bee" no
    longer matches *beetle*.
    """
    haystack = (" ".join((hit.get("title", ""), hit.get("description", "")))).lower()
    # Commons titles glue words with hyphens and underscores. Flattening them
    # means "prairie-dog" reads as the compound it is, rather than as a word
    # boundary that hands the match to "dog".
    haystack = re.sub(r"[-_/]+", " ", haystack)
    if names_something_else(critter, haystack):
        return 0, 0
    identity = sum(2 for term in identity_terms(critter)
                   if re.search(r"\b%s\b" % re.escape(term), haystack))
    action = sum(1 for noise in ACTIONS.get(critter, []) if noise in haystack)
    return identity, action


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


def flac_duration(data):
    """From STREAMINFO, which FLAC always puts first."""
    if data[:4] != b"fLaC" or len(data) < 42:
        return None
    body = data[8:8 + 34]                        # magic(4) + block header(4)
    packed = int.from_bytes(body[10:18], "big")  # 20b rate, 3b channels, 5b depth, 36b samples
    rate = packed >> 44
    samples = packed & ((1 << 36) - 1)
    return samples / float(rate) if rate and samples else None


def looks_like_mp3(data):
    if data[:3] == b"ID3":
        return True
    return len(data) > 1 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0


def duration_of(data):
    if data[:4] == b"OggS":
        return ogg_duration(data)
    if data[:4] == b"RIFF":
        return wav_duration(data)
    if data[:4] == b"fLaC":
        return flac_duration(data)
    if looks_like_mp3(data):
        return mp3_duration(data)
    return None                                  # webm: playable, not parsed here


def extension_for(data):
    """Android sniffs the content, but a sane extension keeps the folder readable."""
    if data[:4] == b"RIFF":
        return ".wav"
    if data[:4] == b"fLaC":
        return ".flac"
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


FILE_FIELDS = "url|mime|size|extmetadata"

# How many candidates are enough before we stop spending requests.
CANDIDATE_BUDGET = 30


def files_in_category(title):
    """`title` is a full 'Category:...' page title."""
    payload = api(generator="categorymembers", gcmtitle=title,
                  gcmtype="file", gcmlimit="60",
                  prop="imageinfo", iiprop=FILE_FIELDS)
    return [describe(p) for p in payload.get("query", {}).get("pages", {}).values()]


def files_by_search(term):
    """
    `filetype:audio` is the whole trick.

    Commons ranks images and PDFs above audio for the same words, so a plain
    search for "cock crowing" comes back with twenty results and *none* of them
    a sound — the rooster's six perfectly good recordings never even reached the
    candidate list. Constraining the search to audio makes every result usable
    and lets the limit be raised at the same time.
    """
    payload = api(generator="search", gsrsearch=term + " filetype:audio",
                  gsrnamespace="6", gsrlimit="40",
                  prop="imageinfo", iiprop=FILE_FIELDS)
    return [describe(p) for p in payload.get("query", {}).get("pages", {}).values()]


def search_terms(critter):
    """
    Build queries from what we already know about the critter rather than
    relying on one hand-written phrase: the name on its own, the name paired
    with each noise it makes, any hand-written extras, and the scientific names.
    """
    terms = [critter]
    terms += ["%s %s" % (critter, action) for action in ACTIONS.get(critter, [])]
    terms += QUERIES.get(critter, [])
    terms += [name for name in CATEGORIES.get(critter, []) if name[:1].isupper()]
    ordered, seen = [], set()
    for term in terms:
        key = term.lower()
        if key not in seen:
            seen.add(key)
            ordered.append(term)
    return ordered


def discover_categories(critter):
    """
    Ask Commons which "Audio files of ..." categories exist for this critter.

    Hand-maintaining that list guesses wrong: the rooster's recordings sit in
    `Category:Audio files of chickens`, which no amount of staring at a species
    name would have produced.
    """
    found, seen = [], set()
    probes = [critter, critter + "s"]
    probes += [name for name in CATEGORIES.get(critter, []) if name[:1].isupper()][:2]
    for probe in probes[:3]:
        try:
            payload = api(list="search", srsearch="Audio files of " + probe,
                          srnamespace="14", srlimit="10")
        except Exception as error:                              # noqa: BLE001
            print("  ! category lookup %r failed: %s" % (probe, error), end="")
            continue
        for hit in payload.get("query", {}).get("search", []):
            title = hit.get("title", "")
            if title.startswith("Category:Audio files of") and title not in seen:
                seen.add(title)
                found.append(title)
    return found


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
            if is_a_person_not_an_animal(hit):
                rejected.append((hit, "a person, not an animal"))
                continue
            if filed_under_another_animal(critter, hit):
                rejected.append((hit, "Commons files it as a different animal"))
                continue
            identity, action = relevance(critter, hit)
            if identity == 0:
                rejected.append((hit, "never names the animal"))
                continue
            # Commons filing something under "Audio files of <taxon>" is a
            # curator's judgement that it really is that animal — worth more
            # than any word-matching this script can do. "Scotch rabbit" (a
            # dish, filed under Welsh rarebit) sinks below any real rabbit.
            hit["curated"] = "audio files of" in hit.get("categories", "").lower()
            hit["identity"], hit["action"] = identity, action
            hit["relevance"] = identity + action + (3 if hit["curated"] else 0)
            hit["source"] = source
            keep.append(hit)

    # Search first: with the audio filter it is now the highest-yield route.
    for term in search_terms(critter)[:5]:
        try:
            consider(files_by_search(term), "search:" + term)
        except Exception as error:                              # noqa: BLE001
            print("  ! search %r failed: %s" % (term, error), end="")
        if len(keep) >= CANDIDATE_BUDGET:
            break

    # Then categories, which catch recordings whose titles are in another
    # language — "Kykyryký.ogg" is a rooster, but no English query finds it.
    if len(keep) < CANDIDATE_BUDGET:
        titles = ["Category:Audio files of " + name for name in CATEGORIES.get(critter, [])]
        titles += [t for t in discover_categories(critter) if t not in titles]
        for title in titles[:6]:
            try:
                consider(files_in_category(title), "category:" + title[24:])
            except Exception as error:                          # noqa: BLE001
                print("  ! category %r failed: %s" % (title, error), end="")
            if len(keep) >= CANDIDATE_BUDGET:
                break

    # Most obviously on-topic first, then Ogg (always decodable here), then small.
    keep.sort(key=lambda h: (not h["curated"], -h["identity"], -h["action"],
                             0 if "ogg" in h["mime"] else 1, h["size"]))
    if verbose:
        print("\n    %d candidates from %d files seen" % (len(keep), len(seen)), end="")
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
    parser.add_argument("--candidates", type=int, default=1, metavar="N",
                        help="download up to N clips per critter, into "
                             "sounds/<critter>/, so you can pick by ear")
    parser.add_argument("--max-seconds", type=float, default=MAX_SECONDS, metavar="S",
                        help="longest clip to accept (default %.0f); raise it when "
                             "auditioning and trim the winner afterwards"
                             % MAX_SECONDS)
    args = parser.parse_args()
    longest = args.max_seconds

    wanted = args.only or list(CATEGORIES)
    os.makedirs(OUT_DIR, exist_ok=True)
    taken, missing = [], []

    for critter in wanted:
        print("%-11s" % critter, end=" ", flush=True)
        picked, tried = [], 0
        for hit in candidates_for(critter, args.verbose):
            if len(picked) >= args.candidates or tried >= 5 + args.candidates * 3:
                break
            if args.report:
                picked.append(dict(hit, seconds=None))
                continue
            tried += 1
            try:
                data = get(hit["url"])
            except Exception as error:                          # noqa: BLE001
                print("\n    ! download failed: %s" % error, end="")
                continue
            seconds = duration_of(data)
            if seconds is None or not (MIN_SECONDS <= seconds <= longest):
                if args.verbose:
                    print("\n    skipped %-44s duration %s" % (
                        hit["title"][5:48],
                        "unreadable" if seconds is None else "%.1fs" % seconds), end="")
                continue
            path = save_path(critter, hit, data, len(picked), args.candidates)
            with open(path, "wb") as handle:
                handle.write(data)
            picked.append(dict(hit, seconds=seconds, path=path))

        if picked:
            for index, hit in enumerate(picked):
                prefix = "%-11s" % "" if index else ""
                print("%s%-38s %-12s %6s  rel=%-2s %s" % (
                    prefix,
                    hit["title"][5:43],
                    hit["licence"][:12] or "?",
                    ("%.1fs" % hit["seconds"]) if hit.get("seconds") else "",
                    hit.get("relevance", "?"),
                    (hit.get("description") or "")[:44]))
            taken.append((critter, picked))
        else:
            print("-- nothing usable")
            missing.append(critter)

    if not args.report and taken:
        write_credits(taken)

    print("\n%d of %d critters have a sound in %s"
          % (len(taken), len(wanted), OUT_DIR))
    if args.candidates > 1:
        print("Up to %d per critter — audition them and keep the best." % args.candidates)
    if missing:
        print("no luck for:", ", ".join(missing))
        print("These need a hand-picked file, or a source that needs an API key.")


def save_path(critter, hit, data, index, wanted):
    """One file per critter stays flat; several go in a folder, ranked by name."""
    extension = extension_for(data)
    if wanted <= 1:
        return os.path.join(OUT_DIR, critter + extension)
    folder = os.path.join(OUT_DIR, critter)
    os.makedirs(folder, exist_ok=True)
    name = os.path.splitext(hit["title"][5:])[0]          # drop Commons' own extension
    stem = re.sub(r"[^A-Za-z0-9]+", "-", name)[:48].strip("-").lower()
    return os.path.join(folder, "%d-%s%s" % (index + 1, stem, extension))


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
    for critter, hits in sorted(entries):
        for hit in hits:
            title = hit["title"][5:].replace("|", "/")
            author = (hit["author"] or "unknown").replace("|", "/")
            note = (hit.get("description") or "").replace("|", "/")[:90]
            lines.append("| %s | [%s](%s) | %s | %s | %s |" % (
                critter, title, hit.get("page", ""), hit["licence"] or "?",
                author, note))
    with open(CREDITS, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print("\nwrote", CREDITS)


if __name__ == "__main__":
    sys.exit(main())
