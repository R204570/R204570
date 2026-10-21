"""Builds the static profile panels: python3 scripts/build_assets.py

Needs fontTools and brotli (pip install fonttools brotli). It fetches Geist and Geist Mono from
google/fonts once (cached in scripts/fonts/src, not committed), writes the basic-latin subsets and
metrics the live activity panel uses, then draws every static panel. The activity panel itself is
drawn by scripts/activity.py, which needs only the standard library.

Each panel that would shrink on a phone also gets a -narrow drawing at 360px; the README's
<picture> elements pick it under 600px.
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
from console import (BLUE, BLUE_HI, BLUE_LO, LABEL_LIGHT, LIFT, MONO, MUTED, PANEL, SANS, SEAM, SOFT,  # noqa: E402
                     TEXT, WHITE, Canvas, measure, n, wrap)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
WIDE, NARROW = 830, 360

SOURCES = {
    SANS: "https://raw.githubusercontent.com/google/fonts/main/ofl/geist/Geist%5Bwght%5D.ttf",
    MONO: "https://raw.githubusercontent.com/google/fonts/main/ofl/geistmono/GeistMono%5Bwght%5D.ttf",
}
BASIC = "".join(chr(c) for c in range(32, 127)) + "·×→↗•★–—…’é®"

# The hidden part's second layer. Only the shifted note lives in this repo.
NOTE = "ENW{u1qq3a_c4eg_hay0px3q}"


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


def finish(cv: Canvas, name: str, title: str, desc: str = "", comment: str = "") -> None:
    exact = {k: woff2(*k, "".join(sorted(v))) for k, v in cv.chars.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(cv.svg(title, desc, exact, comment), encoding="utf-8")


# ---------------------------------------------------------------- content
PITCH = "AI engineer building agents, vision models and the software around them, from idea to deployed."
PROFILE = [("Based in", "Ahmedabad, India", TEXT), ("Focus", "Agentic AI · Vision", TEXT),
           ("Open to", "AI · Agentic · DS roles", TEXT), ("Freelance", "Available", BLUE_LO)]
CREDENTIALS = [("2026", "Microsoft Elevate × GTU"), ("2026", "B.E. IT, Data Science hons"),
               ("2025", "Intel® AI for Manufacturing"), ("CPTE", "Penetration testing engineer")]
PIPELINE = [("Data", ["pandas", "NumPy", "scikit-learn"]), ("Model", ["PyTorch", "YOLOv8", "3D U-Net"]),
            ("Agent", ["RAG", "tool use", "MCP servers"]), ("Backend", ["FastAPI", "Django", "pgvector"]),
            ("Ship", ["Render", "Vercel", "GCP"]), ("Secure", ["CPTE", "STRIDE", "OWASP LLM"])]
HERO_TITLE = "Raj Patel, AI engineer"
HERO_DESC = (f"Raj Patel (R204570). {PITCH} Now shipping DocsForge, an open-source MCP server in production. "
             "Based in Ahmedabad, India; open to AI Engineering, Agentic AI and Data Science roles, and to freelance work. "
             "Credentials: Microsoft Elevate × GTU (2026), B.E. Information Technology with Data Science honours (2026), "
             "Intel AI for Manufacturing (2025), CPTE. Pipeline: " +
             "; ".join(f"{s}: {', '.join(t)}" for s, t in PIPELINE) + ".")


def command_box(cv: Canvas, x: float, y: float, w: float, mono: float) -> None:
    cv.rect(x, y, w, 56, PANEL, SEAM, r=8)
    cv.pulse(x + 20, y + 20, 3.5)
    lead = "now shipping  "
    cv.text(x + 34, y + 24.5, lead, mono, TEXT, MONO)
    cv.text(x + 34 + measure(lead, MONO, 400, mono), y + 24.5, "docsforge", mono, BLUE_LO, MONO, 500)
    cv.text(x + 34, y + 43, "open-source MCP server · in production", mono - 1, MUTED, MONO)


def hero() -> None:
    W, H = WIDE, 470
    cv = Canvas(W, H)
    cv.panel(glow=(150, 110, 430))
    # title bar
    cv.icon("folder", 24, 15, 15, MUTED)
    cv.text(46, 27, "r204570 / profile", 12.5, MUTED, MONO)
    status = "Open to AI roles · freelance"
    cv.text(W - 24, 27, status, 12.5, TEXT, MONO, anchor="end")
    cv.pulse(W - 24 - measure(status, MONO, 400, 12.5) - 14, 23, 3.5)
    cv.line(0.5, 44, W - 0.5, 44)
    # identity
    cv.text(30, 134, "Raj Patel", 66, TEXT, SANS, 600, tracking=-2)
    y = 174
    for line in wrap(PITCH, SANS, 400, 18, 450):
        cv.text(32, y, line, 18, SOFT)
        y += 26
    command_box(cv, 32, y + 10, 456, 13)
    # profile and credentials
    cv.line(520, 44, 520, 306)
    cv.text(544, 74, "PROFILE", 11, MUTED, MONO, 500, tracking=1.4)
    for i, (k, v, col) in enumerate(PROFILE):
        cv.text(544, 98 + i * 22, k, 12.5, MUTED, MONO)
        cv.text(806, 98 + i * 22, v, 13.5, col, anchor="end")
    cv.text(544, 200, "CREDENTIALS", 11, MUTED, MONO, 500, tracking=1.4)
    for i, (k, v) in enumerate(CREDENTIALS):
        cv.text(544, 224 + i * 22, k, 12.5, MUTED, MONO)
        cv.text(806, 224 + i * 22, v, 13.5, TEXT, anchor="end")
    cv.line(0.5, 306, W - 0.5, 306)
    # pipeline: how an idea becomes something deployed
    cv.text(32, 336, "PIPELINE", 11, MUTED, MONO, 500, tracking=1.4)
    cv.text(32 + measure("PIPELINE", MONO, 500, 11, 1.4) + 12, 336, "idea to deployed", 13, MUTED)
    gap, bw, by, bh = 14, (W - 64 - 5 * 14) / 6, 352, 96
    for i, (stage, tools) in enumerate(PIPELINE):
        bx = 32 + i * (bw + gap)
        if i:
            cv.line(bx - gap, by + 46, bx, by + 46, BLUE)
        cv.rect(bx, by, bw, bh, PANEL, SEAM, r=8)
        cv.icon("check", bx + 12, by + 12, 16, BLUE_HI)
        cv.text(bx + 35, by + 25, stage, 14, TEXT, SANS, 500)
        for j, tool in enumerate(tools):
            cv.text(bx + 13, by + 52 + j * 16, tool, 11, MUTED, MONO)
    finish(cv, "hero", HERO_TITLE, HERO_DESC, comment=f"hidden part :: {NOTE}")


def hero_narrow() -> None:
    W = NARROW
    cv = Canvas(W, 2000)
    cv.text(16, 26, "r204570", 11.5, MUTED, MONO)
    status = "Open to AI roles"
    cv.text(W - 16, 26, status, 11.5, TEXT, MONO, anchor="end")
    cv.pulse(W - 16 - measure(status, MONO, 400, 11.5) - 12, 22, 3)
    cv.line(0.5, 40, W - 0.5, 40)
    cv.text(15, 98, "Raj Patel", 46, TEXT, SANS, 600, tracking=-1.4)
    y = 130
    for line in wrap(PITCH, SANS, 400, 15.5, 328):
        cv.text(16, y, line, 15.5, SOFT)
        y += 22
    command_box(cv, 16, y + 6, 328, 12)
    y += 90
    cv.line(0.5, y - 14, W - 0.5, y - 14)
    cv.text(16, y + 8, "PROFILE", 10.5, MUTED, MONO, 500, tracking=1.3)
    y += 32
    for k, v, col in PROFILE:
        cv.text(16, y, k, 12, MUTED, MONO)
        cv.text(W - 16, y, v, 13, col, anchor="end")
        y += 22
    y += 14
    cv.text(16, y, "CREDENTIALS", 10.5, MUTED, MONO, 500, tracking=1.3)
    y += 24
    for k, v in CREDENTIALS:
        cv.text(16, y, k, 12, MUTED, MONO)
        cv.text(W - 16, y, v, 13, TEXT, anchor="end")
        y += 22
    cv.line(0.5, y + 2, W - 0.5, y + 2)
    y += 30
    cv.text(16, y, "PIPELINE", 10.5, MUTED, MONO, 500, tracking=1.3)
    cv.text(16 + measure("PIPELINE", MONO, 500, 10.5, 1.3) + 10, y, "idea to deployed", 12.5, MUTED)
    y += 26
    rows = [y + i * 34 for i in range(len(PIPELINE))]
    cv.line(24, rows[0] - 4, 24, rows[-1] - 4, BLUE)  # the spine runs under the checks
    for ry, (stage, tools) in zip(rows, PIPELINE):
        cv.add(f'<circle cx="24" cy="{n(ry - 4)}" r="9" fill="{C.GROUND}"/>')
        cv.icon("check", 16, ry - 12, 16, BLUE_HI)
        cv.text(42, ry + 1, stage, 14, TEXT, SANS, 500)
        cv.text(124, ry + 1, " · ".join(tools), 11.5, MUTED, MONO)
    H = rows[-1] + 24
    cv.h = H
    body = cv.parts
    cv.parts = []
    cv.panel(glow=(80, 90, 300))
    cv.parts += body
    finish(cv, "hero-narrow", HERO_TITLE, HERO_DESC)


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
    if primary:
        cv.rect(0.5, 0.5, w - 1, 35, BLUE, r=8)
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


def pill(cv: Canvas, right: float, y: float, label: str, size: float) -> None:
    w = measure(label, MONO, 500, size) + 30
    x = right - w
    cv.rect(x, y, w, 24, LIFT, SEAM, r=12)
    cv.add(f'<circle cx="{n(x + 13)}" cy="{n(y + 12)}" r="3.5" fill="{BLUE_HI}"/>')
    cv.text(x + 22, y + 16.5, label, size, BLUE_LO, MONO, 500)


def card(key: str, name: str, status: str, desc: str, facts: list, narrow: bool) -> None:
    W = NARROW if narrow else WIDE
    pad = 16 if narrow else 24
    cv = Canvas(W, 1000)
    body: list = []
    cv.icon("box", pad, 16, 18, BLUE_HI)
    cv.text(pad + 28, 30, name if not narrow or len(name) < 22 else name.replace("-management-system", " ms").replace("-defect-detection", " defects"),
            14.5 if narrow else 16, TEXT, MONO, 500)
    pill(cv, W - pad, 13, status, 11 if narrow else 11.5)
    cv.line(0.5, 50, W - 0.5, 50)
    size, lh = (14, 20) if narrow else (15, 22)
    y = 80
    for line in wrap(desc, SANS, 400, size, W - 2 * pad):
        cv.text(pad, y, line, size, SOFT)
        y += lh
    y += 10
    if narrow:
        for k, v in facts:
            cv.text(pad, y, k.upper(), 10, MUTED, MONO, 500, tracking=1)
            cv.text(pad, y + 19, v, 13.5, TEXT)
            y += 44
        H = y - 4
    else:
        cols = (pad, 300, 560)
        for (k, v), x in zip(facts, cols):
            cv.text(x, y, k.upper(), 10.5, MUTED, MONO, 500, tracking=1)
            cv.text(x, y + 21, v, 14, TEXT)
        H = y + 44
    cv.h = H
    body = cv.parts
    cv.parts = []
    cv.panel()
    cv.parts += body
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
    hero()
    hero_narrow()
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
