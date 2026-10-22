"""Builds the static profile panels: python3 scripts/build_assets.py

Needs fontTools and brotli (pip install fonttools brotli). It fetches Geist and Geist Mono from
google/fonts once (cached in scripts/fonts/src, not committed) and the technology marks from Simple
Icons once (cached in scripts/logos.json, committed, CC0), writes the basic-latin font subsets and
metrics the live panels use, then draws the buttons, project cards, more-work rows and the stack
panel. The hero and the activity panel carry live data, so scripts/activity.py draws those.

Every panel also gets a -narrow drawing at 360px; the README's <picture> elements pick it under 600px.
"""
from __future__ import annotations

import io
import json
import re
import sys
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import console as C  # noqa: E402
from console import (BLUE, BLUE_HI, BLUE_LO, GLASS, LIFT, MONO, MUTED, ON_BLUE, ON_BLUE_LABEL, ON_BLUE_SOFT, PANEL,  # noqa: E402
                     SANS, SEAM, SOFT, TEXT, WHITE, Canvas, measure, n, wrap)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
WIDE, NARROW = 830, 360
SKY = "#93C5FD"

SOURCES = {
    SANS: "https://raw.githubusercontent.com/google/fonts/main/ofl/geist/Geist%5Bwght%5D.ttf",
    MONO: "https://raw.githubusercontent.com/google/fonts/main/ofl/geistmono/GeistMono%5Bwght%5D.ttf",
}
BASIC = "".join(chr(c) for c in range(32, 127)) + "·×→↗•★–—…’é®"
ICON_SET = "https://cdn.jsdelivr.net/npm/simple-icons@15.0.0/icons/{}.svg"


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


# ---------------------------------------------------------------- technology marks
LOGO_SLUGS = ["python", "javascript", "typescript", "pytorch", "tensorflow", "scikitlearn", "opencv", "ultralytics",
              "huggingface", "pandas", "numpy", "fastapi", "django", "flask", "postgresql", "redis", "nodedotjs",
              "streamlit", "vercel", "netlify", "render", "googlecloud", "claude", "github", "kaggle"]
LOGOS_FILE = Path(__file__).resolve().parent / "logos.json"


def logos() -> dict[str, str]:
    """Simple Icons paths (CC0), fetched once and kept in scripts/logos.json."""
    have = json.loads(LOGOS_FILE.read_text(encoding="utf-8")) if LOGOS_FILE.exists() else {}
    missing = [s for s in LOGO_SLUGS if s not in have]
    for slug in missing:
        with urllib.request.urlopen(ICON_SET.format(slug), timeout=30) as r:
            have[slug] = re.search(r' d="([^"]+)"', r.read().decode("utf-8")).group(1)
    if missing:
        LOGOS_FILE.write_text(json.dumps(have, indent=0, sort_keys=True), encoding="utf-8")
    return have


LOGO: dict[str, str] = {}

# what each technology is drawn with: a Simple Icons slug, or one of our line icons
TECH = {
    "Python": "python", "JavaScript": "javascript", "TypeScript": "typescript", "PyTorch": "pytorch",
    "TensorFlow": "tensorflow", "scikit-learn": "scikitlearn", "OpenCV": "opencv", "YOLOv8": "ultralytics",
    "Hugging Face": "huggingface", "pandas": "pandas", "NumPy": "numpy", "FastAPI": "fastapi", "Django": "django",
    "Flask": "flask", "PostgreSQL": "postgresql", "Redis": "redis", "Node.js": "nodedotjs", "Streamlit": "streamlit",
    "Vercel": "vercel", "Netlify": "netlify", "Render": "render", "Google Cloud": "googlecloud", "Claude Code": "claude",
    "Kaggle": ":chart",
    "MCP": ":plug", "RAG": ":layers", "Tool use": ":bot", "LLMs & SLMs": ":cpu", "NLP": ":book", "pgvector": ":database",
    "3D U-Net": ":cpu", "CPTE": ":shield", "STRIDE": ":shield", "OWASP LLM Top 10": ":shield", "DPDP": ":shield",
}


def chip_width(label: str, size: float = 12.5) -> float:
    return 32 + measure(label, SANS, 500, size) + 12


def chip(cv: Canvas, x: float, y: float, label: str, size: float = 12.5) -> float:
    w = chip_width(label, size)
    cv.rect(x, y, w, 28, PANEL, SEAM, r=8)
    mark = TECH.get(label, ":box")
    if mark.startswith(":"):
        cv.icon(mark[1:], x + 10, y + 6, 16, BLUE_LO)
    else:
        cv.logo(LOGO[mark], x + 10, y + 6.5, 15, BLUE_LO)
    cv.text(x + 32, y + 18.5, label, size, TEXT, SANS, 500)
    return w


def chips(cv: Canvas, x: float, y: float, room: float, labels: list[str], gap: float = 8) -> float:
    """Flow chips left to right, wrapping inside `room`. Returns the bottom edge."""
    cx, cy = x, y
    for lab in labels:
        w = chip_width(lab)
        if cx > x and cx + w > x + room:
            cx, cy = x, cy + 28 + gap
        chip(cv, cx, cy, lab)
        cx += w + gap
    return cy + 28


# ---------------------------------------------------------------- buttons
BUTTONS = [  # key, label, icon (line icon or @logo), primary
    ("resume", "Résumé", "file", True),
    ("email", "Email", "mail", False),
    ("linkedin", "LinkedIn", "linkedin", False),
    ("portfolio", "Portfolio", "globe", False),
    ("kaggle", "Kaggle", "chart", False),
    ("medium", "Medium", "book", False),
    ("live", "Live site", "external", False),
    ("demo", "Live demo", "external", False),
    ("source", "Source", "@github", False),
    ("contribute", "Contribute", "users", False),
    ("notebook", "Notebook", "code", False),
    ("dataset", "Dataset", "database", False),
]


def button(key: str, label: str, icon: str, primary: bool) -> None:
    w = 14 + 16 + 8 + measure(label, SANS, 500, 14) + 16
    cv = Canvas(w, 36)
    fg, mark = (WHITE, WHITE) if primary else (TEXT, MUTED)
    if primary:  # the one solid blue on the page, with the same grain as the lettering
        cv.rect(0.5, 0.5, w - 1, 35, BLUE, r=8, extra=cv.speckle())
    else:
        cv.rect(0.5, 0.5, w - 1, 35, PANEL, SEAM, r=8)
    if icon.startswith("@"):
        cv.logo(LOGO[icon[1:]], 14, 10, 16, mark)
    else:
        cv.icon(icon, 14, 10, 16, mark)
    cv.text(38, 23, label, 14, fg, SANS, 500)
    finish(cv, f"btn-{key}", label)


# ---------------------------------------------------------------- project cards
PROJECTS = [
    dict(key="docsforge", repo="docsforge", name="DocsForge", status="Production",
         tagline="Open-source MCP server for official, version-specific docs",
         flow=[("library name", "book"), ("find docs", "search"), ("verify", "check"), ("harvest", "database"), ("MCP tools", "plug")],
         desc="Name a library and DocsForge finds its official documentation, verifies it, harvests it and serves it "
              "to Claude Code, Cursor, Codex and any other MCP client.",
         stack=["Python", "MCP", "FastAPI", "PostgreSQL"],
         facts=[("Result", "91% of never-seen names resolved first try"), ("Live", "docsforge.vercel.app")], glow=(.1, 1.3)),
    dict(key="neuroassist", repo="braintumor", name="NeuroAssist", status="Capstone",
         tagline="Brain-tumour MRI to a drafted clinical report",
         flow=[("MRI scan", "layers"), ("3D U-Net", "cpu"), ("volumes + lobes", "chart"), ("RAG report", "file")],
         desc="A 3D Attention U-Net segments the tumour on BraTS 2020 scans, measures volumes and lobe involvement, "
              "and a RAG-grounded LLM drafts the structured report.",
         stack=["Python", "3D U-Net", "RAG", "Flask", "PostgreSQL"],
         facts=[("Programme", "Microsoft Elevate × GTU"), ("Data", "BraTS 2020 MRI, NIfTI and DICOM")], glow=(.85, 1.35)),
    dict(key="hospital", repo="hospital-management-system", name="Hospital Management", status="Live · 100 stars", status_short="Live",
         tagline="Role-based hospital operations, end to end",
         flow=[("patient", "users"), ("appointment", "calendar"), ("billing", "card"), ("pharmacy", "pill"), ("PDF report", "file")],
         desc="A Django system for patients, appointments, billing and pharmacy, with role-based access and PDF reports. "
              "My most-starred repository.",
         stack=["Python", "Django"],
         facts=[("Stars", "100, with 4 forks"), ("Live", "Render")], glow=(.3, -.35)),
    dict(key="pcb", repo="pcb_defect_detection", name="PCB Defect Detection", status="Live demo",
         tagline="Fine-tuned YOLOv8 for circuit-board inspection",
         flow=[("PCB images", "image"), ("YOLOv8", "cpu"), ("defects found", "scan"), ("annotated ZIP", "download")],
         desc="Upload one PCB image or a batch; a fine-tuned YOLOv8 marks the defects, charts their distribution and "
              "exports the annotated images.",
         stack=["Python", "YOLOv8", "PyTorch", "Streamlit"],
         facts=[("Result", "mAP@0.5 above 85%"), ("Programme", "Intel® AI for Manufacturing")], glow=(.95, 1.3)),
]


def pill_on_blue(cv: Canvas, right: float, y: float, label: str, size: float) -> None:
    w = measure(label, MONO, 500, size) + 30
    x = right - w
    cv.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="24" rx="12" fill="{GLASS}" fill-opacity=".6" '
           'stroke="#FFFFFF" stroke-opacity=".22"/>')
    cv.dot(x + 13, y + 12, 3.5, SKY)
    cv.text(x + 22, y + 16.5, label, size, ON_BLUE, MONO, 500)


def flow(cv: Canvas, x: float, y: float, room: float, steps: list, size: float) -> float:
    """How the project works: glass nodes, each with its stage icon, joined by lit arrows; wraps
    inside `room`. Returns the bottom edge."""
    gap, h = 26, 32
    cx, cy = x, y
    for i, (s, icon) in enumerate(steps):
        w = 33 + measure(s, MONO, 400, size) + 12
        if i and cx + gap + w > x + room:
            cx, cy = x, cy + h + 10
        elif i:
            cv.add(f'<path d="M{n(cx + 4)} {n(cy + h / 2)}h{gap - 9}m-4 -4 4 4-4 4" fill="none" stroke="{SKY}" '
                   'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
            cx += gap
        cv.add(f'<rect x="{n(cx)}" y="{n(cy)}" width="{n(w)}" height="{h}" rx="8" fill="{GLASS}" fill-opacity=".6" '
               'stroke="#FFFFFF" stroke-opacity=".22"/>')
        cv.icon(icon, cx + 11, cy + 9, 14, SKY)
        cv.text(cx + 33, cy + 20.5, s, size, ON_BLUE, MONO)
        cx += w
    return cy + h


def card(p: dict, narrow: bool) -> None:
    W = NARROW if narrow else WIDE
    pad = 16 if narrow else 24
    cv = Canvas(W, 1400)
    body: list[str] = []
    # header band content (drawn after the surface; collected first so the band height is known)
    cv.icon("folder", pad, 14, 15, ON_BLUE_LABEL)
    # phones show just the repository and a short status, so the bar never collides with the pill
    cv.text(pad + 22, 26.5, p["repo"] if narrow else f"r204570 / {p['repo']}", 11.5 if narrow else 12, ON_BLUE_LABEL, MONO)
    pill_on_blue(cv, W - pad, 9, p.get("status_short", p["status"]) if narrow else p["status"], 11 if narrow else 11.5)
    cv.add(f'<line x1=".5" y1="42.5" x2="{n(W - .5)}" y2="42.5" stroke="#FFFFFF" stroke-opacity=".14" shape-rendering="crispEdges"/>')
    name_size = 28 if narrow else 34
    while measure(p["name"], SANS, 600, name_size, -1) > W - 2 * pad:
        name_size -= 1
    y = 84 if narrow else 90
    cv.text(pad - 1, y, p["name"], name_size, ON_BLUE, SANS, 600, tracking=-1, extra=cv.speckle())
    y += 24 if narrow else 27
    for line in wrap(p["tagline"], SANS, 400, 14.5 if narrow else 15.5, W - 2 * pad):
        cv.text(pad, y, line, 14.5 if narrow else 15.5, ON_BLUE_SOFT)
        y += 20
    band = flow(cv, pad, y + 6, W - 2 * pad, p["flow"], 11.5 if narrow else 12) + (18 if narrow else 22)
    head = cv.parts
    cv.parts = []
    # body
    tsize, lh = (14, 20) if narrow else (15, 22)
    y = band + 32
    for line in wrap(p["desc"], SANS, 400, tsize, W - 2 * pad):
        cv.text(pad, y, line, tsize, SOFT)
        y += lh
    y = chips(cv, pad, y + 2, W - 2 * pad, p["stack"]) + 26
    if narrow:
        for k, v in p["facts"]:
            cv.text(pad, y, k.upper(), 11.5, MUTED, MONO, 500, tracking=1)
            for line in wrap(v, SANS, 400, 14, W - 2 * pad):
                cv.text(pad, y + 20, line, 14, TEXT)
                y += 19
            y += 27
        H = y
    else:
        for (k, v), x in zip(p["facts"], (pad, 470)):
            cv.text(x, y, k.upper(), 11, MUTED, MONO, 500, tracking=1)
            cv.text(x, y + 21, v, 14.5, TEXT)
        H = y + 42
    body = cv.parts
    cv.parts = []
    cv.h = H
    defs = cv.defs
    cv.defs = []
    cv.rect(0.5, 0.5, W - 1, H - 1, C.GROUND, r=14)
    gx, gy = p["glow"]
    cv.grainy(0.5, 0.5, W - 1, band, r=14, glows=((gx, gy, .7), (1 - gx, -.6, .45)), seed=7 + len(p["key"]), corners="top")
    cv.add(f'<line x1=".5" y1="{n(band + .5)}" x2="{n(W - .5)}" y2="{n(band + .5)}" stroke="#FFFFFF" stroke-opacity=".12"/>')
    cv.parts += head + body
    cv.rect(0.5, 0.5, W - 1, H - 1, stroke=SEAM, r=14)
    cv.defs += defs
    facts = "; ".join(f"{k}: {v}" for k, v in p["facts"])
    steps = " → ".join(s for s, _ in p["flow"])
    finish(cv, f"card-{p['key']}{'-narrow' if narrow else ''}", f"{p['name']}, {p['status']}",
           f"{p['tagline']}. How it works: {steps}. {p['desc']} Stack: {', '.join(p['stack'])}. {facts}.")


# ---------------------------------------------------------------- more work
MORE = [  # key, name, description, lead mark (logo slug or :icon), two facts
    ("mgmt", "MGMT Methylation Model", "A 3D ResNet trained on all four MRI sequences to predict MGMT promoter methylation, on "
     "my own preprocessed BraTS dataset, with a NIfTI and DICOM conversion pipeline both ways.",
     "pytorch", [("Model", "BrainNet3D · 3D ResNet"), ("Task", "RSNA-MICCAI MGMT")]),
    ("sac", "SAC AI Search", "Describe a service in plain words and it finds the right GST service accounting code (SAC).",
     "python", [("Stack", "Python · AI search"), ("Licence", "Open source")]),
    ("reconciliation", "Reconciliation", "Wallet-balance reconciliation on an atomic compute-then-commit engine, with a Flask "
     "dashboard, CLI and batch runner.", "flask", [("Stack", "Flask · MS SQL Server"), ("Engine", "Compute, then commit")]),
    ("expenseflow", "ExpenseFlow", "Receipt to saved expense with AI extraction and a searchable history.",
     "javascript", [("Stack", "JavaScript"), ("Live", "Vercel")]),
    ("cafepos", "Cafe-POS", "Point of sale for cafes and restaurants, with a REST API behind it.",
     "django", [("Stack", "Django · DRF · PostgreSQL"), ("For", "Cafes and restaurants")]),
    ("gearguard", "GearGuard", "A full-featured web platform for maintenance and equipment management.",
     "django", [("Stack", "Django 5.2 · PostgreSQL"), ("Kind", "Web platform")]),
]


def tile(cv: Canvas, x: float, y: float, size: float, mark: str) -> None:
    cv.rect(x, y, size, size, LIFT, SEAM, r=10)
    m = size * .52
    if mark.startswith(":"):
        cv.icon(mark[1:], x + (size - m) / 2, y + (size - m) / 2, m, BLUE_LO)
    else:
        cv.logo(LOGO[mark], x + (size - m) / 2, y + (size - m) / 2, m, BLUE_LO)


def more_row(key: str, name: str, desc: str, mark: str, facts: list, narrow: bool) -> None:
    W = NARROW if narrow else WIDE
    cv = Canvas(W, 400)
    if narrow:
        pad = 16
        tile(cv, pad, 16, 40, mark)
        cv.text(pad + 54, 42, name, 18, TEXT, SANS, 600)
        y = 84
        for line in wrap(desc, SANS, 400, 15.5, W - 2 * pad):
            cv.text(pad, y, line, 15.5, SOFT)
            y += 22
        y += 12
        for (k, v), x in zip(facts, (pad, 186)):
            cv.text(x, y, k.upper(), 11.5, MUTED, MONO, 500, tracking=1)
            cv.text(x, y + 20, C.fit(v, SANS, 400, 13.5, 160), 13.5, TEXT)
        H = y + 40
    else:
        pad = 22
        tile(cv, pad, 22, 46, mark)
        cv.text(pad + 62, 46, name, 20, TEXT, SANS, 600)
        y = 74
        for line in wrap(desc, SANS, 400, 16, 500):
            cv.text(pad + 62, y, line, 16, SOFT)
            y += 23
        cv.line(616, 20, 616, max(y, 104) - 6)
        for i, (k, v) in enumerate(facts):
            cv.text(636, 40 + i * 44, k.upper(), 11, MUTED, MONO, 500, tracking=1)
            cv.text(636, 60 + i * 44, C.fit(v, SANS, 400, 14, W - 636 - pad), 14, TEXT)
        H = max(y + 10, 124)
    body = cv.parts
    cv.parts = []
    cv.h = H
    defs = cv.defs
    cv.defs = []
    cv.panel(r=12)
    cv.parts += body
    cv.defs += defs
    facts_txt = "; ".join(f"{k}: {v}" for k, v in facts)
    finish(cv, f"more-{key}{'-narrow' if narrow else ''}", name, f"{name}. {desc} {facts_txt}.")


# ---------------------------------------------------------------- tech stack
STACK = [
    ("AI / ML", ["PyTorch", "TensorFlow", "YOLOv8", "OpenCV", "3D U-Net", "scikit-learn", "Hugging Face", "pandas", "NumPy"]),
    ("Agents & LLMs", ["Claude Code", "MCP", "RAG", "Tool use", "LLMs & SLMs", "NLP"]),
    ("Backend & data", ["FastAPI", "Django", "Flask", "PostgreSQL", "pgvector", "Redis", "Node.js"]),
    ("Ship", ["Streamlit", "Vercel", "Netlify", "Render", "Google Cloud"]),
    ("Security", ["CPTE", "STRIDE", "OWASP LLM Top 10", "DPDP"]),
    ("Languages", ["Python", "JavaScript", "TypeScript"]),
]


def stack(narrow: bool) -> None:
    W = NARROW if narrow else WIDE
    pad = 16 if narrow else 24
    cv = Canvas(W, 2000)
    cv.icon("folder", pad, 15, 15, MUTED)
    cv.text(pad + 22, 28, "r204570 / stack", 12 if narrow else 12.5, MUTED, MONO)
    cv.line(0.5, 44, W - 0.5, 44)
    y = 66
    for i, (group, items) in enumerate(STACK):
        if i:
            cv.line(pad, y - 13, W - pad, y - 13)
        if narrow:
            cv.text(pad, y + 6, group.upper(), 11.5, MUTED, MONO, 500, tracking=1.3)
            y = chips(cv, pad, y + 16, W - 2 * pad, items) + 26
        else:
            cv.text(pad, y + 18.5, group.upper(), 11, MUTED, MONO, 500, tracking=1.3)
            y = chips(cv, 190, y, W - 190 - pad, items) + 26
    H = y - 6
    body = cv.parts
    cv.parts = []
    cv.h = H
    defs = cv.defs
    cv.defs = []
    cv.panel()
    cv.parts += body
    cv.defs += defs
    desc = "; ".join(f"{g}: {', '.join(i)}" for g, i in STACK)
    finish(cv, f"stack{'-narrow' if narrow else ''}", "Tech stack", desc + ".")


def main() -> None:
    build_fonts()
    LOGO.update(logos())
    for b in BUTTONS:
        button(*b)
    for p in PROJECTS:
        card(p, narrow=False)
        card(p, narrow=True)
    for m in MORE:
        more_row(*m, narrow=False)
        more_row(*m, narrow=True)
    stack(False)
    stack(True)
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:34} {p.stat().st_size:>7}")


if __name__ == "__main__":
    main()
