"""The hero console panel, wide (830px) and narrow (360px).

Drawn by scripts/activity.py on every run, because it carries a live strip of the last 26 weeks.
Standard library only; type comes from the committed subsets in scripts/fonts.
"""
from __future__ import annotations

import math

from console import (BLUE, BLUE_HI, BLUE_LO, GROUND, MONO, MUTED, PANEL, SANS, SEAM, SOFT, TEXT, Canvas, measure, n,
                     wrap)

# The hidden part's second layer. Only the shifted note lives in this repo.
NOTE = "ENW{u1qq3a_c4eg_hay0px3q}"

PITCH = "AI engineer building agents, vision models and the software around them, from idea to deployed."
PROFILE = [("Based in", "Ahmedabad, India", TEXT), ("Focus", "Agentic AI · Computer vision", TEXT),
           ("Open to", "AI Engineering, Data Science", TEXT), ("Freelance", "Available", BLUE_LO)]
CREDENTIALS = [("2026", "Microsoft Elevate × GTU"), ("2026", "B.E. IT, Data Science hons"),
               ("2025", "Intel® AI for Manufacturing"), ("CPTE", "Penetration testing engineer")]
PIPELINE = [("Data", "database", ["pandas", "NumPy", "scikit-learn"]), ("Model", "cpu", ["PyTorch", "YOLOv8", "3D U-Net"]),
            ("Agent", "bot", ["RAG", "tool use", "MCP servers"]), ("Backend", "server", ["FastAPI", "Django", "pgvector"]),
            ("Ship", "rocket", ["Render", "Vercel", "GCP"]), ("Secure", "shield", ["CPTE", "STRIDE", "OWASP LLM"])]
TITLE = "Raj Patel, AI engineer"


def describe(total26: int) -> str:
    return (f"Raj Patel (R204570). {PITCH} Now shipping DocsForge, an open-source MCP server in production "
            "(pipx install docsforge). Based in Ahmedabad, India; open to AI Engineering, Agentic AI and Data Science roles, "
            "and to freelance work. Credentials: Microsoft Elevate × GTU (2026), B.E. Information Technology with Data Science "
            f"honours (2026), Intel AI for Manufacturing (2025), CPTE. {total26} contributions in the last 26 weeks. Pipeline: "
            + "; ".join(f"{s}: {', '.join(t)}" for s, _, t in PIPELINE) + ".")


def command_box(cv: Canvas, x: float, y: float, w: float, mono: float) -> None:
    cv.rect(x, y, w, 56, PANEL, SEAM, r=8)
    cv.dot(x + 20, y + 20, 3.5)
    lead = "now shipping  "
    cv.text(x + 34, y + 24.5, lead, mono, TEXT, MONO)
    lw = measure(lead, MONO, 400, mono)
    cv.text(x + 34 + lw, y + 24.5, "docsforge", mono, BLUE_LO, MONO, 500)
    cv.text(x + 34 + lw + measure("docsforge  ", MONO, 500, mono), y + 24.5, "in production", mono, MUTED, MONO)
    cv.text(x + 34, y + 43, "$ pipx install docsforge", mono - 1, MUTED, MONO)


def strip(cv: Canvas, x: float, y: float, w: float, weeks: list[int], label_size: float, bar_h: float) -> float:
    """Live cell: the last 26 weeks as speckled blue bars, a recent pulse with no annotation (the
    activity panel below owns the full-year detail and the busiest-week call-out). Returns the bottom edge."""
    total = sum(weeks)
    cv.text(x, y, "LAST 26 WEEKS", label_size, MUTED, MONO, 500, tracking=1.4 if label_size >= 11 else 1.3)
    cv.text(x + w, y, f"{total:,} contributions", label_size + 1.5, TEXT, MONO, anchor="end")
    top = y + 10
    base = top + bar_h
    peak = max(weeks) or 1
    step = w / len(weeks)
    bars = []
    for i, v in enumerate(weeks):
        h = 2 if not v else 3 + (base - top - 3) * math.sqrt(v / peak)
        fill = SEAM if not v else BLUE
        op = 1 if not v else .5 + .5 * math.sqrt(v / peak)
        bars.append(f'<rect x="{n(x + i * step + 1.5)}" y="{n(base - h)}" width="{n(step - 3)}" height="{n(h)}" rx="1.5" '
                    f'fill="{fill}" opacity="{op:.2f}"/>')
    cv.add(f"<g{cv.speckle()}>{''.join(bars)}</g>")
    cv.line(x, base + .5, x + w, base + .5)
    return base


def wide(weeks: list[int]) -> str:
    W, seam_y = 830, 344
    H = seam_y + 150
    cv = Canvas(W, H)
    cv.panel(glow=(150, 110, 430))
    # title bar: the page's one breathing dot says who is available
    cv.icon("folder", 24, 15, 15, MUTED)
    cv.text(46, 27, "r204570 / profile", 12.5, MUTED, MONO)
    status = "Open to AI roles · freelance"
    cv.text(W - 24, 27, status, 12.5, TEXT, MONO, anchor="end")
    cv.pulse(W - 24 - measure(status, MONO, 400, 12.5) - 14, 23, 3.5)
    cv.line(0.5, 44, W - 0.5, 44)
    # identity, now shipping, live strip
    cv.text(30, 126, "Raj Patel", 66, TEXT, SANS, 600, tracking=-2, extra=cv.speckle())
    y = 166
    for line in wrap(PITCH, SANS, 400, 18, 450):
        cv.text(32, y, line, 18, SOFT)
        y += 26
    command_box(cv, 32, y - 10, 456, 13)
    strip(cv, 32, y + 72, 456, weeks, 11, 36)
    # profile and credentials
    cv.line(520, 44, 520, seam_y)
    cv.text(544, 74, "PROFILE", 11, MUTED, MONO, 500, tracking=1.4)
    for i, (k, v, col) in enumerate(PROFILE):
        cv.text(544, 98 + i * 24, k, 12.5, MUTED, MONO)
        cv.text(806, 98 + i * 24, v, 13.5, col, anchor="end")
    cv.text(544, 210, "CREDENTIALS", 11, MUTED, MONO, 500, tracking=1.4)
    for i, (k, v) in enumerate(CREDENTIALS):
        cv.text(544, 234 + i * 24, k, 12.5, MUTED, MONO)
        cv.text(806, 234 + i * 24, v, 13.5, TEXT, anchor="end")
    cv.line(0.5, seam_y, W - 0.5, seam_y)
    # pipeline: how an idea becomes something deployed
    cv.text(32, seam_y + 26, "PIPELINE", 11, MUTED, MONO, 500, tracking=1.4)
    cv.text(32 + measure("PIPELINE", MONO, 500, 11, 1.4) + 12, seam_y + 26, "idea to deployed", 13, MUTED)
    gap, bw, by, bh = 14, (W - 64 - 5 * 14) / 6, seam_y + 38, 92
    for i, (stage, icon, tools) in enumerate(PIPELINE):
        bx = 32 + i * (bw + gap)
        if i:
            cv.line(bx - gap, by + 46, bx, by + 46, BLUE)
        cv.rect(bx, by, bw, bh, PANEL, SEAM, r=8)
        cv.icon(icon, bx + 12, by + 12, 16, BLUE_HI)
        cv.text(bx + 35, by + 25, stage, 14, TEXT, SANS, 500)
        for j, tool in enumerate(tools):
            cv.text(bx + 13, by + 52 + j * 16, tool, 11, MUTED, MONO)
    return cv.svg(TITLE, describe(sum(weeks)), comment=f"hidden part :: {NOTE}")


def narrow(weeks: list[int]) -> str:
    W = 360
    cv = Canvas(W, 2000)
    cv.text(16, 26, "r204570", 11.5, MUTED, MONO)
    status = "Open to AI roles"
    cv.text(W - 16, 26, status, 11.5, TEXT, MONO, anchor="end")
    cv.pulse(W - 16 - measure(status, MONO, 400, 11.5) - 12, 22, 3)
    cv.line(0.5, 40, W - 0.5, 40)
    cv.text(15, 98, "Raj Patel", 46, TEXT, SANS, 600, tracking=-1.4, extra=cv.speckle())
    y = 130
    for line in wrap(PITCH, SANS, 400, 15.5, 328):
        cv.text(16, y, line, 15.5, SOFT)
        y += 22
    command_box(cv, 16, y - 6, 328, 11.5)
    y = strip(cv, 16, y + 80, 328, weeks, 10.5, 40) + 30
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
    y += 28
    rows = [y + i * 34 for i in range(len(PIPELINE))]
    cv.line(24, rows[0] - 4, 24, rows[-1] - 4, BLUE)  # the flow runs under the stage marks
    for ry, (stage, icon, tools) in zip(rows, PIPELINE):
        cv.add(f'<circle cx="24" cy="{n(ry - 4)}" r="10" fill="{GROUND}"/>')
        cv.icon(icon, 16, ry - 12, 16, BLUE_HI)
        cv.text(42, ry + 1, stage, 14, TEXT, SANS, 500)
        cv.text(124, ry + 1, " · ".join(tools), 11.5, MUTED, MONO)
    cv.h = rows[-1] + 24
    body, defs = cv.parts, cv.defs
    cv.parts, cv.defs = [], []
    cv.panel(glow=(80, 90, 300))
    cv.parts += body
    cv.defs += defs
    return cv.svg(TITLE, describe(sum(weeks)))
