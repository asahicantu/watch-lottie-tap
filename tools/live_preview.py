"""Live preview: edit an animal, save, watch it change in the browser.

    python tools/live_preview.py            # opens on the last animal you edited
    python tools/live_preview.py gorilla    # start on one in particular
    python tools/live_preview.py --port 9000

It serves one page on http://localhost:8765/ that rebuilds the animal you are
looking at straight from `tools/critters/<name>.py` every time the file
changes on disk - no restart, no regenerating all 120, no writing anything
into the repo. Saving a file with a syntax error puts the traceback on the
page and keeps the last good frame up, so a broken edit costs you nothing.

Editing a different animal switches the page to it, which means the preview
follows you around as you work. `critter_parts.py` and `lottie_kit.py` are
watched too, so a change to a shared feature rebuilds whatever is on screen.

The page also has an inspector: a tree of every named layer/group in the
animation (an eye, a pupil, a tuft - whatever `critter_parts.py` named its
groups) with per-part visibility toggles and an "isolate" button, plus a
properties panel to edit transform/fill/stroke/shape values live. Edits only
touch the in-browser copy of the JSON; they are not written back to the .py
source and are replaced whenever the file rebuilds. Use "export json" to save
a snapshot, or "reset edits" to discard them.

Nothing here is needed to build the app: `gen_critters.py` remains the thing
that writes the assets. This is only for the edit loop. The page itself lives
in `tools/preview/live_preview.html` + `live_preview.js`, also hot-reloaded
from disk on every request.
"""

import argparse
import importlib
import json
import os
import sys
import threading
import time
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

import critters  # noqa: E402

CRITTER_DIR = os.path.join(TOOLS, "critters")
SHARED_FILES = ("critter_parts.py", "lottie_kit.py", "lottie_bounds.py")
POLL_SECONDS = 0.25


# --------------------------------------------------------------------------- #
# building
# --------------------------------------------------------------------------- #

class Build(object):
    """The most recent attempt at building one animal."""

    def __init__(self):
        self.lock = threading.Lock()
        self.name = None
        self.version = 0          # bumped on every rebuild, good or bad
        self.animation = None     # last animation that built cleanly
        self.error = None         # traceback string, or None
        self.built_at = 0.0
        self.ms = 0.0

    def rebuild(self, name):
        """Re-read `name` from disk and build it. Never raises."""
        started = time.time()
        animation, error = None, None
        try:
            # forget the cached modules, so the file on disk is what runs
            critters.reset()
            critter_parts = importlib.import_module("critter_parts")
            animation = critter_parts.critter(name, critters.load(name)())
        except Exception:
            error = traceback.format_exc()
        with self.lock:
            self.name = name
            self.version += 1
            self.error = error
            self.built_at = time.time()
            self.ms = (time.time() - started) * 1000.0
            if animation is not None:
                self.animation = animation
        return error is None

    def state(self):
        with self.lock:
            return {
                "name": self.name,
                "version": self.version,
                "error": self.error,
                "ms": round(self.ms, 1),
                "hasAnimation": self.animation is not None,
            }

    def payload(self):
        with self.lock:
            return self.animation


BUILD = Build()


# --------------------------------------------------------------------------- #
# watching
# --------------------------------------------------------------------------- #

def snapshot():
    """{path: mtime} for every source file the preview cares about."""
    out = {}
    for f in os.listdir(CRITTER_DIR):
        if f.endswith(".py"):
            p = os.path.join(CRITTER_DIR, f)
            try:
                out[p] = os.path.getmtime(p)
            except OSError:
                pass
    for f in SHARED_FILES:
        p = os.path.join(TOOLS, f)
        if os.path.exists(p):
            out[p] = os.path.getmtime(p)
    return out


def watch(selected):
    """Rebuild whenever a watched file changes.

    `selected` is a one-item list so the HTTP handler can change which animal
    is on screen without this thread having to be restarted.
    """
    seen = snapshot()
    while True:
        time.sleep(POLL_SECONDS)
        now = snapshot()
        touched = [p for p, m in now.items() if seen.get(p) != m]
        seen = now
        if not touched:
            continue
        # if an animal file was the thing that changed, follow the edit
        for p in touched:
            stem = os.path.splitext(os.path.basename(p))[0]
            if os.path.dirname(p) == CRITTER_DIR and stem != "__init__":
                selected[0] = stem
                break
        ok = BUILD.rebuild(selected[0])
        print("%s  %-16s %6.1f ms  %s"
              % (time.strftime("%H:%M:%S"), selected[0], BUILD.ms,
                 "ok" if ok else "FAILED - see the page"), flush=True)


# --------------------------------------------------------------------------- #
# serving
# --------------------------------------------------------------------------- #

PAGE_PATH = os.path.join(TOOLS, "preview", "live_preview.html")
PAGE_JS_PATH = os.path.join(TOOLS, "preview", "live_preview.js")


class Handler(BaseHTTPRequestHandler):
    selected = None                     # the one-item list shared with watch()

    def _send(self, code, body, mime):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path, _, query = self.path.partition("?")
        args = dict(p.split("=", 1) for p in query.split("&") if "=" in p)

        if path == "/":
            with open(PAGE_PATH, "rb") as fh:
                return self._send(200, fh.read(), "text/html; charset=utf-8")

        if path == "/live_preview.js":
            with open(PAGE_JS_PATH, "rb") as fh:
                return self._send(200, fh.read(), "application/javascript")

        if path == "/lottie.min.js":
            lib = os.path.join(TOOLS, "preview", "lottie.min.js")
            with open(lib, "rb") as fh:
                return self._send(200, fh.read(), "application/javascript")

        if path == "/api/names":
            return self._send(200, json.dumps(critters.names()),
                              "application/json")

        if path == "/api/state":
            return self._send(200, json.dumps(BUILD.state()),
                              "application/json")

        if path == "/api/select":
            name = args.get("name", "")
            if name in critters.names():
                Handler.selected[0] = name
                BUILD.rebuild(name)
            return self._send(200, json.dumps(BUILD.state()),
                              "application/json")

        if path == "/api/animation":
            data = BUILD.payload()
            if data is None:
                return self._send(503, json.dumps({"error": "nothing built"}),
                                  "application/json")
            return self._send(200, json.dumps(data, separators=(",", ":")),
                              "application/json")

        self._send(404, "not found", "text/plain")

    def log_message(self, *_args):
        pass                            # the watcher already prints what matters


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("critter", nargs="?", default=None,
                        help="which animal to open on (default: the one edited "
                             "most recently)")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    available = critters.names()
    name = args.critter
    if name is None:
        newest = max(available, key=lambda n: os.path.getmtime(critters.path_of(n)))
        name = newest
    if name not in available:
        parser.error("no such animal: %s\n(try one of: %s ...)"
                     % (name, ", ".join(available[:6])))

    selected = [name]
    Handler.selected = selected
    BUILD.rebuild(name)

    threading.Thread(target=watch, args=(selected,), daemon=True).start()

    url = "http://localhost:%d/" % args.port
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("live preview on %s  (watching tools/critters/*.py)" % url)
    print("editing any animal file switches the page to it; ctrl-c to stop")
    if not args.no_browser:
        threading.Timer(0.4, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
