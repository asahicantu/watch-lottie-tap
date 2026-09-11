"""Every critter, one file per animal.

`critters/gorilla.py` defines `gorilla()`, and that is the whole convention -
the file name, the function name and the name of the generated
`gorilla.json` are the same string. To add an animal, drop a new file in
this directory; nothing has to be registered anywhere.

    import critters
    critters.names()          -> ['ant', 'badger', ...]
    critters.load('gorilla')  -> the gorilla function
    critters.load_all()       -> {'ant': <fn>, ...}

`reset()` forgets every cached module so the next `load()` re-reads from
disk. That is what lets `live_preview.py` pick up an edit without a restart.
"""

import importlib
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(DIR)

# the animal modules do `from critter_parts import ...`, which only resolves
# if tools/ is importable - so put it on the path here rather than asking
# every caller to remember
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

# reloaded alongside the animals, because an animal binds the names it
# imports at import time and would otherwise keep the stale ones
SHARED = ("critter_parts", "lottie_kit", "lottie_bounds")


def names():
    """Every animal in this directory, sorted."""
    return sorted(f[:-3] for f in os.listdir(DIR)
                  if f.endswith(".py") and not f.startswith("_"))


def path_of(name):
    """Where the source for `name` lives - handy in error messages."""
    return os.path.join(DIR, name + ".py")


def load(name):
    """The builder function for one animal."""
    module = importlib.import_module(__name__ + "." + name)
    try:
        return getattr(module, name)
    except AttributeError:
        raise AttributeError(
            "%s must define a function called %r to match its file name"
            % (path_of(name), name))


def load_all():
    """Every animal, as {name: function}."""
    return {name: load(name) for name in names()}


def reset():
    """Drop the cached animal and shared modules, so the next load() is fresh."""
    stale = [m for m in sys.modules
             if m.startswith(__name__ + ".") or m in SHARED]
    for m in stale:
        del sys.modules[m]
