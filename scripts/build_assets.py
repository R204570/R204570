"""Builds the static profile graphics: python3 scripts/build_assets.py

Every graphic is written per theme (-dark / -light). The ones that would shrink on a phone
also get a -narrow drawing at 360px, set 1:1, so no text cell drops below 2px; the README's
<picture> elements pick it under 600px. The live signal graph is drawn by scripts/signal.py.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bitmap as bm  # noqa: E402
from bitmap import n  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"
WIDE, NARROW = 830, 360  # GitHub's profile README column; a phone

# The hidden part's second layer. Only the shifted note lives in this repo.
NOTE = "ENW{u1qq3a_c4eg_hay0px3q}"


def write(name: str, theme: dict, markup: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}-{theme['name']}.svg").write_text(markup, encoding="utf-8")


# ---------------------------------------------------------------- dust
def dust_layer(rng: random.Random, W: float, count: int, size: float, bands: list, top: float, bottom: float) -> str:
    """Square motes gathered into swept sine ribbons. Every term repeats over W, so a copy
    placed one width over makes the drift seamless."""
    tau = 2 * math.pi
    out = []
    while len(out) < count:
        x = rng.uniform(0, W)
        if rng.random() < .08:
            y = rng.uniform(top, bottom)
        else:
            cy, amp, ph, s0, s1, sp = rng.choice(bands)
            y = cy + amp * math.sin(tau * x / W + ph) + rng.gauss(0, s0 + s1 * (.5 + .5 * math.sin(tau * 2 * x / W + sp)))
        if top <= y <= bottom:
            out.append(f"M{n(x)} {n(y)}h{n(size)}v{n(size)}h{n(-size)}z")
    return "".join(out)


def dust(theme: dict, W: float, bands: list, top: float, bottom: float, planes: tuple = ("far", "mid", "near")) -> tuple[str, str]:
    """Up to three planes of dust. The rear plane drifts fastest and each step forward halves
    the rate; the type in front of them never moves."""
    rng = random.Random(204570)
    dark = theme is bm.DARK
    spec = {  # count per 830px, size, colour, opacity, seconds per width
        "far": (1600, 1.2, theme["d3"], .9 if dark else .8, 70),
        "mid": (360, 1.8, theme["d3"] if dark else theme["d2"], 1 if dark else .9, 140),
        "near": (110, 2.4, theme["d2"], .7 if dark else .6, 280),
    }
    css, g = [], []
    for cls in planes:
        cnt, size, col, op, secs = spec[cls]
        d = dust_layer(rng, W, round(cnt * W / WIDE), size, bands, top, bottom)
        g.append(f'<g class="{cls}" fill="{col}" opacity="{op}"><path id="{cls}" d="{d}"/><use href="#{cls}" xlink:href="#{cls}" x="{W}"/></g>')
        css.append(f".{cls}{{animation:drift {round(secs * W / WIDE)}s linear infinite}}")
    css.append(f"@keyframes drift{{to{{transform:translateX(-{W}px)}}}}")
    return "".join(css), "".join(g)


def headline(theme: dict, lines: list[tuple[str, float, float]], c: float) -> str:
    """Lit cells with a faint phosphor flicker; in the dark they also bleed a little light."""
    dark = theme is bm.DARK
    ops = (1, .97, .94) if dark else (1, .97, .95)
    o = []
    if dark:
        glow = "".join(bm.path(s, x, y, c) for s, x, y in lines)
        o.append(f'<defs><filter id="bleed" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="{n(c * .45)}"/></filter></defs>'
                 f'<path d="{glow}" fill="{theme["ink"]}" opacity=".38" filter="url(#bleed)"/>')
    for s, x, y in lines:
        for d, op in zip(bm.grain_paths(s, x, y, c), ops):
            o.append(f'<path d="{d}" fill="{theme["ink"]}" fill-opacity="{op}"/>')
    return "".join(o)


def caret(theme: dict, s: str, x: float, y: float, c: float) -> str:
    return f'<rect class="caret" x="{n(x + bm.width(s, c) + c)}" y="{n(y + 4 * c)}" width="{n(3 * c)}" height="{n(3 * c)}" fill="{theme["signal"]}"/>'


CARET_CSS = ".caret{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
HERO_TITLE = "Raj Patel, R204570: I build AI that ships"
HERO_DESC = ("Raj Patel, AI engineer in Ahmedabad. I build AI that ships: agents, vision models and the apps around them, "
             "from idea to deployed. Status: open to AI roles and freelance work. Now shipping DocsForge.")


def bars(theme: dict, x: float, base: float) -> str:
    return f'<g fill="{theme["signal"]}">' + "".join(
        f'<rect x="{n(x + i * 7)}" y="{n(base - (i + 2) * 3)}" width="5" height="{(i + 2) * 3}"/>' for i in range(4)) + "</g>"


# ---------------------------------------------------------------- title screen
def hero(theme: dict) -> str:
    t, W, H = theme, WIDE, 412
    bands = [(150, 60, .6, 5, 10, 1.0), (220, 80, 3.6, 6, 12, 2.0), (310, 44, 2.5, 7, 12, 4.0)]
    css, motes = dust(t, W, bands, 70, H - 4)
    o = [motes]
    o.append(bm.text("RAJ PATEL", 0, 8, 3, t["ink"], track=1.4))
    o.append(f'<rect x="{n(bm.width("RAJ PATEL", 3, 1.4) + 8)}" y="20" width="9" height="9" fill="{t["signal"]}"/>')
    o.append(bm.text("R204570 · AHMEDABAD, IN", 0, 42, 2, t["d2"], track=2))
    o.append(bm.text("STATUS", W, 8, 2, t["d2"], track=2, anchor="end"))
    o.append(bars(t, W - 28, 40))
    o.append(bm.text("open to ai roles + freelance", W - 38, 26, 2, t["ink"], anchor="end"))
    o.append(bm.text("NOW", W, 60, 2, t["d2"], track=2, anchor="end"))
    o.append(bm.text("shipping docsforge", W, 78, 2, t["ink"], anchor="end"))
    o.append(headline(t, [("i build ai", 0, 104), ("that ships", 0, 214)], 10))
    o.append(caret(t, "that ships", 0, 214, 10))
    o.append(bm.text("agents, vision models and the apps", 0, 334, 3, t["d1"]))
    o.append(bm.text("around them, from idea to deployed.", 0, 370, 3, t["d1"]))
    return bm.svg(W, H, "".join(o), HERO_TITLE, HERO_DESC, css + CARET_CSS,
                  comment=f"hidden part :: {NOTE}" if t is bm.DARK else "")


def hero_narrow(theme: dict) -> str:
    t, W, H = theme, NARROW, 300
    bands = [(150, 40, .6, 4, 8, 1.0), (220, 34, 3.6, 5, 9, 2.0)]
    css, motes = dust(t, W, bands, 104, H - 4, planes=("far",))
    o = [motes]
    o.append(bm.text("RAJ PATEL", 0, 6, 3, t["ink"], track=1.4))
    o.append(f'<rect x="{n(bm.width("RAJ PATEL", 3, 1.4) + 8)}" y="18" width="9" height="9" fill="{t["signal"]}"/>')
    o.append(bm.text("R204570 · AHMEDABAD, IN", 0, 38, 2, t["d2"], track=2))
    o.append(bars(t, W - 26, 27))
    o.append(bm.text("open to ai roles + freelance", 0, 62, 2, t["ink"]))
    o.append(bm.text("now shipping docsforge", 0, 84, 2, t["d2"]))
    o.append(headline(t, [("i build ai", 0, 120), ("that ships", 0, 176)], 5))
    o.append(caret(t, "that ships", 0, 176, 5))
    for i, line in enumerate(("agents, vision models and", "the apps around them, from", "idea to deployed.")):
        o.append(bm.text(line, 0, 238 + i * 22, 2, t["d1"]))
    return bm.svg(W, H, "".join(o), HERO_TITLE, HERO_DESC, css + CARET_CSS)


# ---------------------------------------------------------------- link prompts
LINKS = [  # file key, label, primary
    ("resume", "résumé", True),
    ("email", "email", False),
    ("linkedin", "linkedin", False),
    ("portfolio", "portfolio", False),
    ("kaggle", "kaggle", False),
    ("medium", "medium", False),
]


def prompt(theme: dict, label: str, primary: bool) -> str:
    """Native size everywhere: 14px caps on a phone and on a desktop. Only the primary
    action spends the amber."""
    c = 2
    w = bm.width("> " + label, c) + 2
    body = (bm.text(">", 0, 4, c, theme["signal"] if primary else theme["d2"])
            + bm.text(label, bm.width("> ", c) + c, 4, c, theme["signal"] if primary else theme["ink"]))
    return bm.svg(w, 4 + 9 * c + 2, body, label)


# ---------------------------------------------------------------- queue rows
ROWS = [  # key, depth, name, status, title
    ("docsforge", 0, "docsforge", "in production", "DocsForge, in production"),
    ("neuroassist", 1, "neuroassist", "capstone", "NeuroAssist, capstone"),
    ("hospital", 2, "hospital ms", "100★ · live", "Hospital Management System, 100 stars, live"),
    ("pcb", 3, "pcb inspection", "intel · live", "PCB Inspection, Intel, live"),
]
TRACK = (2.5, 1.75, 1, .5)         # the frontmost row is set widest
LEAD_DRIFT = (0, 5.4, 2.7, 1.35)   # seconds per 8px of leader; halves at each step back


def row(theme: dict, depth: int, name: str, status: str, title: str) -> str:
    t = theme
    c, y = 4, 3
    base = y + bm.CAP * c
    ink = t[bm.STEPS[depth]]
    o = [bm.text(">", 0, y, c, t["signal"] if depth == 0 else ink)]
    nx = 36
    o.append(bm.text(name, nx, y, c, ink, track=TRACK[depth]))
    o.append(bm.text(status, WIDE, base - bm.CAP * 3, 3, t["signal"] if depth == 0 else ink, anchor="end"))
    x0 = nx + bm.width(name, c, TRACK[depth]) + 16
    x1 = WIDE - bm.width(status, 3) - 16
    dots = "".join(f"M{x} {base - 2}h2v2h-2z" for x in range(int(x0) - 8, int(x1) + 8, 8))
    secs = LEAD_DRIFT[depth]
    css = f".lead{{animation:lead {secs}s linear infinite}}@keyframes lead{{to{{transform:translateX(-8px)}}}}" if secs else ""
    cls = ' class="lead"' if secs else ""
    o.append(f'<defs><clipPath id="lc"><rect x="{n(x0)}" y="0" width="{n(max(x1 - x0, 0))}" height="40"/></clipPath></defs>'
             f'<g clip-path="url(#lc)"><path{cls} d="{dots}" fill="{t["d3"]}"/></g>')
    return bm.svg(WIDE, 40, "".join(o), title, style=css)


def row_narrow(theme: dict, depth: int, name: str, status: str, title: str) -> str:
    """Phone: the status drops under the name and the leader goes; depth keeps its brightness."""
    t = theme
    ink = t[bm.STEPS[depth]]
    o = [bm.text(">", 0, 3, 3, t["signal"] if depth == 0 else ink),
         bm.text(name, 26, 3, 3, ink, track=TRACK[depth]),
         bm.text(status, 26, 36, 2, t["signal"] if depth == 0 else ink)]
    return bm.svg(NARROW, 56, "".join(o), title)


# ---------------------------------------------------------------- section labels
LABELS = [  # short enough to stay at native size on a phone
    ("queue", "QUEUE", "SHIPPED WORK"),
    ("signal", "SIGNAL", "LIVE ACTIVITY"),
    ("layers", "LAYERS", "THE STACK"),
]


def label(theme: dict, head: str, tail: str) -> str:
    c, tr = 2, 2
    hw = bm.width(head + "  ", c, tr) + tr * c
    body = bm.text(head, 0, 2, c, theme["ink"], track=tr) + bm.text("· " + tail, hw, 2, c, theme["d2"], track=tr)
    return bm.svg(hw + bm.width("· " + tail, c, tr) + 2, 20, body, f"{head.title()}: {tail.lower()}")


# ---------------------------------------------------------------- greetings scroller
SCROLL = ("greetz to everyone who reads the source   ·   there is a hidden part on this screen   ·   "
          "it starts where browsers don't render   ·   one layer is 64 characters wide, the other is older than computers   ·   "
          "found the flag? mail it with the subject FLAG   ·   thanks for scrolling this far   ·   ")


def scroller(theme: dict, W: float) -> str:
    c = 2
    tw = bm.width(SCROLL, c) + 6 * c  # one full loop, gap included
    secs = round(tw / 42)
    body = (f'<g class="s" fill="{theme["d2"]}"><path id="sc" d="{bm.path(SCROLL, 0, 4, c)}"/>'
            f'<use href="#sc" xlink:href="#sc" x="{n(tw)}"/></g>')
    css = f".s{{animation:scroll {secs}s linear infinite}}@keyframes scroll{{to{{transform:translateX(-{n(tw)}px)}}}}"
    return bm.svg(W, 4 + 9 * c + 2, body, "Greetings scroller",
                  "Greetz to everyone who reads the source. There is a hidden part on this screen.", css)


# ---------------------------------------------------------------- main
def main() -> None:
    for t in bm.THEMES:
        write("hero", t, hero(t))
        write("hero-narrow", t, hero_narrow(t))
        for key, lab, primary in LINKS:
            write(f"link-{key}", t, prompt(t, lab, primary))
        for key, depth, name, status, title in ROWS:
            write(f"row-{key}", t, row(t, depth, name, status, title))
            write(f"row-{key}-narrow", t, row_narrow(t, depth, name, status, title))
        for key, head, tail in LABELS:
            write(f"label-{key}", t, label(t, head, tail))
        write("scroller", t, scroller(t, WIDE))
        write("scroller-narrow", t, scroller(t, NARROW))
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:34} {p.stat().st_size:>7}")


if __name__ == "__main__":
    main()
