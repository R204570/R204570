"""Builds the static profile panels: python3 scripts/build_assets.py

Needs fontTools and brotli (pip install fonttools brotli). It fetches Geist and Geist Mono from
google/fonts once (cached in scripts/fonts/src, not committed), writes the basic-latin subsets and
metrics the live panels use, then draws the buttons, project cards and section labels. The hero
and the activity panel carry live data, so scripts/activity.py draws those with the standard library.

Each card also gets a -narrow drawing at 360px; the README's <picture> elements pick it under 600px.
"""
from __future__ import annotations

import io
import json
import sys
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import console as C  # noqa: E402
from console import (BLUE, BLUE_HI, BLUE_LO, LABEL_LIGHT, LIFT, MONO, MUTED, PANEL, SANS, SEAM, SOFT, TEXT, WHITE,  # noqa: E402
                     Canvas, measure, n, wrap)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
WIDE, NARROW = 830, 360

SOURCES = {
    SANS: "https://raw.githubusercontent.com/google/fonts/main/ofl/geist/Geist%5Bwght%5D.ttf",
    MONO: "https://raw.githubusercontent.com/google/fonts/main/ofl/geistmono/GeistMono%5Bwght%5D.ttf",
}
BASIC = "".join(chr(c) for c in range(32, 127)) + "·×→↗•★–—…’é®"


# ---------------------------------------------------------------- fonts
_instances: dict[tuple[str, int], bytes] = {}


def instance(family: str, weight: int) -> bytes:
    if (family, weight) not in _instances:
        src = C.FONTS / "src" / f"{family.replace(' ', '')}.ttf"
        if not src.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(SOURCES[family], timeout=60) as r:
                src.write_bytes(r.read())
        f = instancer.instantiateVariableFont(TTFont(src), {"wght": weight})
        b = io.BytesIO()
        f.save(b)
        _instances[(family, weight)] = b.getvalue()
    return _instances[(family, weight)]


def woff2(family: str, weight: int, text: str) -> bytes:
    f = TTFont(io.BytesIO(instance(family, weight)))
    o = subset.Options()
    o.flavor = "woff2"
    o.layout_features = ["kern", "liga", "calt", "tnum"]
    s = subset.Subsetter(o)
    s.populate(text=text)
    s.subset(f)
    b = io.BytesIO()
    f.flavor = "woff2"
    f.save(b)
    return b.getvalue()


def build_fonts() -> None:
    """Committed subsets and advance widths, so the Action can set type without fontTools."""
    table = {}
    for (fam, wt), fname in C.FACES.items():
        (C.FONTS / fname).write_bytes(woff2(fam, wt, BASIC))
        f = TTFont(io.BytesIO(instance(fam, wt)))
        cmap, hmtx = f.getBestCmap(), f["hmtx"]
        table[f"{fam}:{wt}"] = {"upm": f["head"].unitsPerEm,
                                "adv": {ch: hmtx[cmap[ord(ch)]][0] for ch in BASIC if ord(ch) in cmap}}
    (C.FONTS / "metrics.json").write_text(json.dumps(table, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    C._metrics = None


def finish(cv: Canvas, name: str, title: str, desc: str = "") -> None:
    exact = {k: woff2(*k, "".join(sorted(v))) for k, v in cv.chars.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(cv.svg(title, desc, exact), encoding="utf-8")


# ---------------------------------------------------------------- link buttons
BUTTONS = [  # key, label, icon, primary
    ("resume", "Résumé", "file", True),
    ("email", "Email", "mail", False),
    ("linkedin", "LinkedIn", "linkedin", False),
    ("portfolio", "Portfolio", "globe", False),
    ("kaggle", "Kaggle", "chart", False),
    ("medium", "Medium", "book", False),
]


def button(key: str, label: str, icon: str, primary: bool) -> None:
    w = 14 + 16 + 8 + measure(label, SANS, 500, 14) + 16
    cv = Canvas(w, 36)
    if primary:  # the one solid blue on the page, with the same grain as the lettering
        cv.rect(0.5, 0.5, w - 1, 35, BLUE, r=8, extra=cv.speckle())
        cv.icon(icon, 14, 10, 16, WHITE)
        cv.text(38, 23, label, 14, WHITE, SANS, 500)
    else:
        cv.rect(0.5, 0.5, w - 1, 35, PANEL, SEAM, r=8)
        cv.icon(icon, 14, 10, 16, MUTED)
        cv.text(38, 23, label, 14, TEXT, SANS, 500)
    finish(cv, f"btn-{key}", label)


# ---------------------------------------------------------------- project cards
PROJECTS = [  # key, name, status, description, three facts
    ("docsforge", "docsforge", "Production",
     "Open-source MCP server: name a library and it finds, verifies and harvests the official, version-specific docs "
     "for Claude Code, Cursor and Codex.",
     [("Stack", "Python · MCP · FastAPI"), ("Result", "91% of unseen names resolved"), ("Live", "docsforge.vercel.app")]),
    ("neuroassist", "neuroassist", "Capstone",
     "MRI in, report out: a 3D Attention U-Net segments the tumour on BraTS 2020, measures volumes and lobe "
     "involvement, and a RAG-grounded LLM drafts the report.",
     [("Stack", "3D Attention U-Net · RAG · Flask"), ("Programme", "Microsoft Elevate × GTU"), ("Data", "BraTS 2020 MRI")]),
    ("hospital", "hospital-management-system", "Live",
     "Django hospital system with role-based access for patients, appointments, billing, pharmacy and PDF reports.",
     [("Stack", "Django · Python"), ("Stars", "100, my most-starred repo"), ("Live", "Render")]),
    ("pcb", "pcb-defect-detection", "Live",
     "A fine-tuned YOLOv8 that finds defects on PCB images, one at a time or in batches.",
     [("Stack", "YOLOv8 · PyTorch · Streamlit"), ("Result", "mAP@0.5 above 85%"), ("Programme", "Intel® AI for Manufacturing")]),
]


def pill(cv: Canvas, right: float, y: float, label: str, size: float) -> float:
    w = measure(label, MONO, 500, size) + 30
    x = right - w
    cv.rect(x, y, w, 24, LIFT, SEAM, r=12)
    cv.add(f'<circle cx="{n(x + 13)}" cy="{n(y + 12)}" r="3.5" fill="{BLUE_HI}"/>')
    cv.text(x + 22, y + 16.5, label, size, BLUE_LO, MONO, 500)
    return w


def card(key: str, name: str, status: str, desc: str, facts: list, narrow: bool) -> None:
    W = NARROW if narrow else WIDE
    pad = 16 if narrow else 24
    cv = Canvas(W, 1000)
    cv.icon("box", pad, 16, 18, BLUE_HI)
    pw = pill(cv, W - pad, 13, status, 11 if narrow else 11.5)
    room = W - 2 * pad - 28 - pw - 10
    size = 14.5 if narrow else 16
    while size > 12 and measure(name, MONO, 500, size) > room:  # keep the real repository name; shrink before cutting
        size -= .5
    cv.text(pad + 28, 30, name, size, TEXT, MONO, 500)
    cv.line(0.5, 50, W - 0.5, 50)
    tsize, lh = (14, 20) if narrow else (15, 22)
    y = 80
    for line in wrap(desc, SANS, 400, tsize, W - 2 * pad):
        cv.text(pad, y, line, tsize, SOFT)
        y += lh
    y += 10
    if narrow:
        for k, v in facts:
            cv.text(pad, y, k.upper(), 10, MUTED, MONO, 500, tracking=1)
            cv.text(pad, y + 19, v, 13.5, TEXT)
            y += 44
        H = y - 4
    else:
        for (k, v), x in zip(facts, (pad, 300, 560)):
            cv.text(x, y, k.upper(), 10.5, MUTED, MONO, 500, tracking=1)
            cv.text(x, y + 21, v, 14, TEXT)
        H = y + 44
    cv.h = H
    body, defs = cv.parts, cv.defs
    cv.parts, cv.defs = [], []
    cv.panel()
    cv.parts += body
    cv.defs += defs
    facts_txt = "; ".join(f"{k}: {v}" for k, v in facts)
    finish(cv, f"card-{key}{'-narrow' if narrow else ''}", f"{name}, {status.lower()}", f"{desc} {facts_txt}.")


# ---------------------------------------------------------------- section labels
LABELS = [("work", "SELECTED WORK"), ("activity", "ACTIVITY")]


def label(key: str, text: str) -> None:
    for theme, col in (("dark", MUTED), ("light", LABEL_LIGHT)):
        w = measure(text, MONO, 500, 12, 1.6) + 2
        cv = Canvas(w, 18)
        cv.text(0, 13, text, 12, col, MONO, 500, tracking=1.6)
        finish(cv, f"label-{key}-{theme}", text.title())


def main() -> None:
    build_fonts()
    for b in BUTTONS:
        button(*b)
    for p in PROJECTS:
        card(*p, narrow=False)
        card(*p, narrow=True)
    for k, t in LABELS:
        label(k, t)
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:34} {p.stat().st_size:>7}")


if __name__ == "__main__":
    main()
