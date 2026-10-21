"""Builds the static profile graphics in both GitHub themes: python3 scripts/build_assets.py

Writes assets/<name>-dark.svg and assets/<name>-light.svg for the title screen, the link
prompts, the queue rows, the section labels and the greetings scroller. The live signal
graph is drawn separately by scripts/signal.py.
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
W = 830  # GitHub's profile README column

# The hidden part's second layer. Only the shifted note lives in this repo.
NOTE = "ENW{u1qq3a_c4eg_hay0px3q}"


def write(name: str, theme: dict, markup: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}-{theme['name']}.svg").write_text(markup, encoding="utf-8")


# ---------------------------------------------------------------- dust
def dust_layer(rng: random.Random, count: int, size: float, top: float, bottom: float) -> str:
    """Square dust motes gathered into two slow sine bands. Every term repeats over W, so a
    copy placed one width over makes the drift seamless."""
    tau = 2 * math.pi
    bands = [  # centre, amplitude, phase, base spread, spread swing, spread phase
        (170, 64, .6, 9, 16, 1.0),
        (300, 46, 2.5, 13, 20, 4.0),
    ]
    out = []
    while len(out) < count:
        x = rng.uniform(0, W)
        if rng.random() < .12:
            y = rng.uniform(top, bottom)
        else:
            cy, amp, ph, s0, s1, sp = rng.choice(bands)
            y = cy + amp * math.sin(tau * x / W + ph) + rng.gauss(0, s0 + s1 * (.5 + .5 * math.sin(tau * 2 * x / W + sp)))
        if top <= y <= bottom:
            out.append(f"M{n(x)} {n(y)}h{n(size)}v{n(size)}h{n(-size)}z")
    return "".join(out)


def dust(theme: dict, top: float, bottom: float, seed: int = 204570) -> tuple[str, str]:
    """Three planes of dust. The rear plane drifts fastest and each step forward halves the
    rate; the type in front of them never moves."""
    rng = random.Random(seed)
    planes = [  # class, count, size, colour, opacity, seconds per width
        ("far", 760, 1.2, theme["d3"], .8 if theme is bm.DARK else .5, 70),
        ("mid", 340, 1.8, theme["d3"], 1 if theme is bm.DARK else .7, 140),
        ("near", 110, 2.4, theme["d2"], .65 if theme is bm.DARK else .5, 280),
    ]
    css, g = [], []
    for cls, cnt, size, col, op, secs in planes:
        d = dust_layer(rng, cnt, size, top, bottom)
        g.append(f'<g class="{cls}" fill="{col}" opacity="{op}"><path id="{cls}" d="{d}"/><use href="#{cls}" xlink:href="#{cls}" x="{W}"/></g>')
        css.append(f".{cls}{{animation:drift {secs}s linear infinite}}")
    css.append(f"@keyframes drift{{to{{transform:translateX(-{W}px)}}}}")
    return "".join(css), "".join(g)


# ---------------------------------------------------------------- title screen
def hero(theme: dict) -> str:
    t = theme
    dark = t is bm.DARK
    H = 412
    css, motes = dust(t, 70, H - 4)
    o = [motes]

    # masthead, top left
    o.append(bm.text("RAJ PATEL", 0, 8, 3, t["ink"], track=1.4))
    mx = bm.width("RAJ PATEL", 3, 1.4) + 8
    o.append(f'<rect x="{n(mx)}" y="{8 + 4 * 3}" width="9" height="9" fill="{t["signal"]}"/>')
    o.append(bm.text("R204570 · AHMEDABAD, IN", 0, 42, 2, t["d2"], track=2))

    # status, top right
    o.append(bm.text("STATUS", W, 8, 2, t["d2"], track=2, anchor="end"))
    bars = "".join(f'<rect x="{W - 28 + i * 7}" y="{40 - (i + 2) * 3}" width="5" height="{(i + 2) * 3}"/>' for i in range(4))
    o.append(f'<g fill="{t["signal"]}">{bars}</g>')
    o.append(bm.text("open to ai roles + freelance", W - 38, 26, 2, t["ink"], anchor="end"))
    o.append(bm.text("NOW", W, 60, 2, t["d2"], track=2, anchor="end"))
    o.append(bm.text("shipping docsforge", W, 78, 2, t["ink"], anchor="end"))

    # the headline: lit cells with a little phosphor flicker
    c = 10
    ops = (1, .9, .8) if dark else (1, .93, .86)
    for line, y in (("i build ai", 104), ("that ships", 214)):
        for d, op in zip(bm.grain_paths(line, 0, y, c), ops):
            o.append(f'<path d="{d}" fill="{t["ink"]}" fill-opacity="{op}"/>')
    px = bm.width("that ships", c) + c
    o.append(f'<rect class="caret" x="{n(px)}" y="{214 + 4 * c}" width="{3 * c}" height="{3 * c}" fill="{t["signal"]}"/>')

    o.append(bm.text("agents, vision models and the apps", 0, 334, 3, t["d1"]))
    o.append(bm.text("around them, from idea to deployed.", 0, 370, 3, t["d1"]))

    css += ".caret{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    return bm.svg(
        W, H, "".join(o),
        "Raj Patel, R204570: I build AI that ships",
        "Raj Patel, AI engineer in Ahmedabad. I build AI that ships: agents, vision models and the apps around them, "
        "from idea to deployed. Status: open to AI roles and freelance work. Now shipping DocsForge.",
        css,
        comment=f"hidden part :: {NOTE}" if dark else "",
    )


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
    c = 2
    s = "> " + label
    w = bm.width(s, c) + 2
    body = bm.text(">", 0, 4, c, theme["signal"]) + bm.text(label, bm.width("> ", c) + c, 4, c, theme["signal"] if primary else theme["ink"])
    return bm.svg(w, 4 + 9 * c + 2, body, label)


# ---------------------------------------------------------------- queue rows
ROWS = [  # key, depth, name, status, status in signal colour
    ("docsforge", 0, "docsforge", "in production", True),
    ("neuroassist", 1, "neuroassist", "capstone", False),
    ("hospital", 2, "hospital ms", "100★ · live", False),
    ("pcb", 3, "pcb inspection", "intel · live", False),
]
DEPTH_INK = ("ink", "d1", "d1", "d2")
DEPTH_TRACK = (2, 1.5, 1, 1)
DEPTH_DRIFT = (0, 5.4, 2.7, 1.35)  # seconds per 8px of leader; halves at each step back


def row(theme: dict, depth: int, name: str, status: str, hot: bool) -> str:
    t = theme
    c, y = 4, 3
    base = y + bm.CAP * c  # baseline
    o = [bm.text(">", 0, y, c, t["signal"])]
    o.append(bm.text(f"{depth:02d}", 32, y, 2, t["d2"]))
    nx = 72
    o.append(bm.text(name, nx, y, c, t[DEPTH_INK[depth]], track=DEPTH_TRACK[depth]))
    o.append(bm.text(status, W, base - bm.CAP * 3, 3, t["signal"] if hot else t["d1"], anchor="end"))

    x0 = nx + bm.width(name, c, DEPTH_TRACK[depth]) + 16
    x1 = W - bm.width(status, 3) - 16
    dots = "".join(f"M{n(x)} {base - 2}h2v2h-2z" for x in range(int(x0) - 8, int(x1) + 8, 8))
    secs = DEPTH_DRIFT[depth]
    css = ""
    cls = ""
    if secs:
        css = f".lead{{animation:lead {secs}s linear infinite}}@keyframes lead{{to{{transform:translateX(-8px)}}}}"
        cls = ' class="lead"'
    o.append(f'<defs><clipPath id="lc"><rect x="{n(x0)}" y="0" width="{n(max(x1 - x0, 0))}" height="40"/></clipPath></defs>'
             f'<g clip-path="url(#lc)"><path{cls} d="{dots}" fill="{t["d3"]}"/></g>')
    return bm.svg(W, 40, "".join(o), f"{depth:02d} {name}: {status}", style=css)


# ---------------------------------------------------------------- section labels
LABELS = [
    ("queue", "QUEUE", "SHIPPED WORK, RANKED BY DEPTH"),
    ("signal", "SIGNAL", "LIVE FROM MY CONTRIBUTION CALENDAR"),
    ("layers", "LAYERS", "WHAT IT IS BUILT WITH"),
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


def scroller(theme: dict) -> str:
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
        for key, lab, primary in LINKS:
            write(f"link-{key}", t, prompt(t, lab, primary))
        for key, depth, name, status, hot in ROWS:
            write(f"row-{key}", t, row(t, depth, name, status, hot))
        for key, head, tail in LABELS:
            write(f"label-{key}", t, label(t, head, tail))
        write("scroller", t, scroller(t))
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:28} {p.stat().st_size:>7}")


if __name__ == "__main__":
    main()
