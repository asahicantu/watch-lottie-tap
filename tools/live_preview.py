"""Live preview: edit an animal or a feeling, save, watch it change in the browser.

    python tools/live_preview.py            # opens on the last thing you edited
    python tools/live_preview.py gorilla    # start on one in particular
    python tools/live_preview.py happy      # names are looked up in both catalogs
    python tools/live_preview.py --port 9000

It serves one page on http://localhost:8765/ that rebuilds whatever you are
looking at straight from `tools/critters/<name>.py` or `tools/feelings/<name>.py`
every time the file changes on disk - no restart, no regenerating everything,
no writing anything into the repo. Saving a file with a syntax error puts the
traceback on the page and keeps the last good frame up, so a broken edit costs
you nothing.

Editing a different animal or feeling switches the page to it, which means the
preview follows you around as you work. Names are unique across both
catalogs, so which one you meant is never ambiguous. `critter_parts.py`,
`feeling_parts.py` and `lottie_kit.py` are all watched too, so a change to a
shared feature rebuilds whatever is on screen.

The page also has an inspector: a tree of every named layer/group in the
animation (an eye, a pupil, a tuft - whatever the parts module named its
groups) with per-part visibility toggles and an "isolate" button, plus a
properties panel to edit transform/fill/stroke/shape values live. Edits only
touch the in-browser copy of the JSON; they are not written back to the .py
source and are replaced whenever the file rebuilds. Use "export json" to save
a snapshot, or "reset edits" to discard them.

Nothing here is needed to build the app: `gen_critters.py`/`gen_feelings.py`
remain the things that write the assets. This is only for the edit loop. The
page itself lives in `tools/preview/live_preview.html` + `live_preview.js`,
also hot-reloaded from disk on every request.
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
REPO_ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import critters  # noqa: E402
import feelings  # noqa: E402

POLL_SECONDS = 0.25


class Package(object):
    """One `<name>.py`-per-item catalog: where its files live, how to rebuild
    one, and which shared files should also trigger a rebuild when touched."""

    def __init__(self, module, dir_, shared_files, build):
        self.module = module
        self.dir = dir_
        self.shared_files = shared_files
        self.build = build          # (name) -> animation dict, may raise

    def names(self):
        return self.module.names()

    def path_of(self, name):
        return self.module.path_of(name)


def _build_critter(name):
    critters.reset()
    critter_parts = importlib.import_module("critter_parts")
    return critter_parts.critter(name, critters.load(name)())


def _build_feeling(name):
    feelings.reset()
    feeling_parts = importlib.import_module("feeling_parts")
    parts, motion = feelings.load(name)()
    return feeling_parts.feeling(name, parts, motion)


PACKAGES = [
    Package(critters, os.path.join(TOOLS, "critters"),
            ("critter_parts.py", "lottie_kit.py", "lottie_bounds.py"),
            _build_critter),
    Package(feelings, os.path.join(TOOLS, "feelings"),
            ("feeling_parts.py", "lottie_kit.py", "lottie_bounds.py"),
            _build_feeling),
]


def all_names():
    """Every animal and feeling name, sorted, from both catalogs combined."""
    out = []
    for pkg in PACKAGES:
        out.extend(pkg.names())
    return sorted(out)


def package_of(name):
    """Which [Package] `name` belongs to, or None if it is in neither."""
    for pkg in PACKAGES:
        if name in pkg.names():
            return pkg
    return None


# --------------------------------------------------------------------------- #
# building
# --------------------------------------------------------------------------- #

class Build(object):
    """The most recent attempt at building one animal."""

    def __init__(self):
        self.lock = threading.Lock()
        self.name = None
        self.path = None          # source .py path, relative to the repo root
        self.version = 0          # bumped on every rebuild, good or bad
        self.animation = None     # last animation that built cleanly
        self.error = None         # traceback string, or None
        self.built_at = 0.0
        self.ms = 0.0

    def rebuild(self, name):
        """Re-read `name` from disk and build it. Never raises."""
        started = time.time()
        animation, error, path = None, None, None
        try:
            pkg = package_of(name)
            if pkg is None:
                raise ValueError("no such animal or feeling: %r" % name)
            path = os.path.relpath(pkg.path_of(name), REPO_ROOT).replace(os.sep, "/")
            animation = pkg.build(name)   # each build() resets its own cache
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
                self.path = path
        return error is None

    def state(self):
        with self.lock:
            return {
                "name": self.name,
                "path": self.path,
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
    """{path: mtime} for every source file the preview cares about, across
    every [Package]."""
    out = {}
    for pkg in PACKAGES:
        for f in os.listdir(pkg.dir):
            if f.endswith(".py"):
                p = os.path.join(pkg.dir, f)
                try:
                    out[p] = os.path.getmtime(p)
                except OSError:
                    pass
        for f in pkg.shared_files:
            p = os.path.join(TOOLS, f)
            if os.path.exists(p):
                out[p] = os.path.getmtime(p)
    return out


def watch(selected):
    """Rebuild whenever a watched file changes.

    `selected` is a one-item list so the HTTP handler can change which item
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
        # if an item file was the thing that changed, follow the edit
        for p in touched:
            stem = os.path.splitext(os.path.basename(p))[0]
            owner = next((pkg for pkg in PACKAGES
                          if os.path.dirname(p) == pkg.dir), None)
            if owner is not None and stem != "__init__":
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
            return self._send(200, json.dumps(all_names()),
                              "application/json")

        if path == "/api/state":
            return self._send(200, json.dumps(BUILD.state()),
                              "application/json")

        if path == "/api/select":
            name = args.get("name", "")
            if package_of(name) is not None:
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
    parser.add_argument("item", nargs="?", default=None,
                        help="which animal or feeling to open on (default: "
                             "the one edited most recently)")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    available = all_names()
    name = args.item
    if name is None:
        newest_paths = [(pkg, n) for pkg in PACKAGES for n in pkg.names()]
        pkg, name = max(newest_paths,
                        key=lambda pn: os.path.getmtime(pn[0].path_of(pn[1])))
    if name not in available:
        parser.error("no such animal or feeling: %s\n(try one of: %s ...)"
                     % (name, ", ".join(available[:6])))

    selected = [name]
    Handler.selected = selected
    BUILD.rebuild(name)

    threading.Thread(target=watch, args=(selected,), daemon=True).start()

    url = "http://localhost:%d/" % args.port
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("live preview on %s  (watching tools/critters/*.py and tools/feelings/*.py)" % url)
    print("editing any animal or feeling file switches the page to it; ctrl-c to stop")
    if not args.no_browser:
        threading.Timer(0.4, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
