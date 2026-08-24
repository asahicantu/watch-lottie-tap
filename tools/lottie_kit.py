"""Minimal Lottie (Bodymovin) JSON builder.

Just enough of the schema to hand-author shape-layer animations:
groups, ellipses, rects, bezier paths, fills, strokes and animated transforms.
Everything is emitted at 30 fps on a 300x300 canvas with the origin at the
centre of the canvas, so shape coordinates read like "20 to the right of the
nose" instead of absolute pixels.
"""

import json
import math

FPS = 30
SIZE = 300
CENTER = SIZE / 2.0


# --------------------------------------------------------------------------- #
# colours + properties
# --------------------------------------------------------------------------- #

def rgb(hexstr):
    """'#ff8800' -> [1.0, 0.533, 0.0, 1.0]"""
    h = hexstr.lstrip("#")
    return [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)] + [1.0]


def static(value):
    return {"a": 0, "k": value}


def animated(keys, ease=(0.35, 0.65)):
    """keys: [(frame, value), ...]. Values may be scalars or lists."""
    out = []
    ox, ix = ease
    for i, (t, v) in enumerate(keys):
        k = {"t": float(t), "s": v if isinstance(v, list) else [v]}
        if i < len(keys) - 1:
            k["i"] = {"x": [ix], "y": [1.0]}
            k["o"] = {"x": [ox], "y": [0.0]}
        out.append(k)
    return {"a": 1, "k": out}


def oscillate(frames, base, amp, period, phase=0.0, steps=8):
    """A looping sine wave sampled into keyframes, for a scalar property."""
    keys = []
    n = max(2, int(round(frames / period * steps)))
    for i in range(n + 1):
        t = frames * i / n
        keys.append((t, base + amp * math.sin(2 * math.pi * (t / period + phase))))
    return animated(keys)


# --------------------------------------------------------------------------- #
# shape primitives
# --------------------------------------------------------------------------- #

def ellipse(w, h, pos=(0, 0)):
    return {"d": 1, "ty": "el", "s": static([w, h]), "p": static(list(pos)), "nm": "ellipse"}


def rect(w, h, pos=(0, 0), radius=0):
    return {"d": 1, "ty": "rc", "s": static([w, h]), "p": static(list(pos)),
            "r": static(radius), "nm": "rect"}


def path(verts, closed=True, tangents=None):
    """verts: [(x, y), ...]; tangents: optional [((ix,iy),(ox,oy)), ...]."""
    if tangents is None:
        tangents = [((0, 0), (0, 0))] * len(verts)
    return {
        "d": 1, "ty": "sh", "nm": "path",
        "ks": static({
            "i": [list(t[0]) for t in tangents],
            "o": [list(t[1]) for t in tangents],
            "v": [list(v) for v in verts],
            "c": closed,
        }),
    }


def fill(color, opacity=100):
    return {"ty": "fl", "c": static(rgb(color) if isinstance(color, str) else color),
            "o": static(opacity), "r": 1, "bm": 0, "nm": "fill"}


def stroke(color, width, cap=2, join=2):
    return {"ty": "st", "c": static(rgb(color) if isinstance(color, str) else color),
            "o": static(100), "w": static(width), "lc": cap, "lj": join,
            "ml": 4, "bm": 0, "nm": "stroke"}


def transform(pos=(0, 0), anchor=(0, 0), scale=(100, 100), rotation=0, opacity=100):
    def p(v, dims):
        return v if isinstance(v, dict) else static(list(v) if dims > 1 else v)
    return {
        "ty": "tr",
        "p": p(pos, 2), "a": p(anchor, 2), "s": p(scale, 2),
        "r": p(rotation, 1), "o": p(opacity, 1),
        "sk": static(0), "sa": static(0), "nm": "transform",
    }


def group(items, tr=None, name="group"):
    """items are drawn front-to-back in list order (first item is on top)."""
    contents = list(items) + [tr or transform()]
    return {"ty": "gr", "nm": name, "np": len(contents), "bm": 0, "hd": False,
            "it": contents}


def filled(shape, color, tr=None, name="shape"):
    return group([shape, fill(color)], tr, name)


def outlined(shape, color, width, tr=None, name="line"):
    return group([shape, stroke(color, width)], tr, name)


# --------------------------------------------------------------------------- #
# layer + document
# --------------------------------------------------------------------------- #

def shape_layer(name, shapes, frames, index=1, pos=(CENTER, CENTER), parent=None):
    layer = {
        "ddd": 0, "ind": index, "ty": 4, "nm": name, "sr": 1,
        "ks": {
            "o": static(100), "r": static(0),
            "p": static([pos[0], pos[1], 0]),
            "a": static([0, 0, 0]),
            "s": static([100, 100, 100]),
        },
        "ao": 0, "shapes": shapes,
        "ip": 0, "op": float(frames), "st": 0, "bm": 0,
    }
    if parent is not None:
        layer["parent"] = parent
    return layer


def animation(name, layers, frames):
    return {
        "v": "5.7.4", "fr": FPS, "ip": 0, "op": float(frames),
        "w": SIZE, "h": SIZE, "nm": name, "ddd": 0,
        "assets": [], "layers": layers,
        "markers": [],
    }


def write(anim, out_path):
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(anim, fh, separators=(",", ":"))
    return out_path
