"""The hero card, wide (830px) and narrow (360px): white type on the grainy blue-and-black surface.

Drawn by scripts/activity.py on every run, because it carries a live strip of the last 26 weeks.
Standard library only; type comes from the committed subsets in scripts/fonts.
"""
from __future__ import annotations

import math

from console import (GLASS, MONO, ON_BLUE, ON_BLUE_LABEL, ON_BLUE_SOFT, SANS, WHITE, Canvas, measure, n, wrap)

# The hidden part's second layer. Only the shifted note lives in this repo.
NOTE = "ENW{u1qq3a_c4eg_hay0px3q}"

SKY = "#93C5FD"  # the one blue that reads as blue text on the blue surface
PITCH = "AI engineer building agents, vision models and the software around them, from idea to deployed."
PROFILE = [("Based in", "Ahmedabad, India", ON_BLUE), ("Focus", "Agentic AI · Computer vision", ON_BLUE),
           ("Open to", "AI Engineering, Data Science", ON_BLUE), ("Freelance", "Available", SKY)]
CREDENTIALS = [("2026", "Microsoft Elevate × GTU"), ("2026", "B.E. IT, Data Science hons"),
               ("2025", "Intel® AI for Manufacturing"), ("CPTE", "Penetration testing engineer")]
TITLE = "Raj Patel, AI engineer"
HAIR = ' stroke="#FFFFFF" stroke-opacity=".16" shape-rendering="crispEdges"'


def describe(total26: int) -> str:
    return (f"Raj Patel (R204570). {PITCH} Now shipping DocsForge, an open-source MCP server in production "
            "(pipx install docsforge). Based in Ahmedabad, India; open to AI Engineering, Agentic AI and Data Science roles, "
            "and to freelance work. Credentials: Microsoft Elevate × GTU (2026), B.E. Information Technology with Data Science "
            f"honours (2026), Intel AI for Manufacturing (2025), CPTE. {total26} contributions in the last 26 weeks.")


def hair(cv: Canvas, x1, y1, x2, y2) -> None:
    cv.add(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"{HAIR}/>')


def command_box(cv: Canvas, x: float, y: float, w: float, mono: float) -> None:
    cv.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="56" rx="10" fill="{GLASS}" fill-opacity=".55" '
           'stroke="#FFFFFF" stroke-opacity=".16"/>')
    cv.dot(x + 20, y + 20, 3.5, SKY)
    lead = "now shipping  "
    cv.text(x + 34, y + 24.5, lead, mono, ON_BLUE, MONO)
    lw = measure(lead, MONO, 400, mono)
    cv.text(x + 34 + lw, y + 24.5, "docsforge", mono, SKY, MONO, 500)
    cv.text(x + 34 + lw + measure("docsforge  ", MONO, 500, mono), y + 24.5, "in production", mono, ON_BLUE_LABEL, MONO)
    cv.text(x + 34, y + 43, "$ pipx install docsforge", mono - 1, ON_BLUE_LABEL, MONO)


def strip(cv: Canvas, x: float, y: float, w: float, weeks: list[int], label_size: float, bar_h: float) -> float:
    """Live cell: the last 26 weeks as white bars on the blue, a recent pulse. The activity panel
    below owns the full-year detail. Returns the bottom edge."""
    cv.text(x, y, "LAST 26 WEEKS", label_size, ON_BLUE_LABEL, MONO, 500, tracking=1.4 if label_size >= 11 else 1.3)
    cv.text(x + w, y, f"{sum(weeks):,} contributions", label_size + 1.5, ON_BLUE, MONO, anchor="end")
    top = y + 12
    base = top + bar_h
    peak = max(weeks) or 1
    step = w / len(weeks)
    bars = []
    for i, v in enumerate(weeks):
        h = 2 if not v else 3 + (base - top - 3) * math.sqrt(v / peak)
        op = .28 if not v else .45 + .55 * math.sqrt(v / peak)
        bars.append(f'<rect x="{n(x + i * step + 1.5)}" y="{n(base - h)}" width="{n(step - 3)}" height="{n(h)}" rx="1.5" '
                    f'fill="{WHITE}" opacity="{op:.2f}"/>')
    cv.add(f"<g{cv.speckle()}>{''.join(bars)}</g>")
    return base


def kv(cv: Canvas, x: float, right: float, y: float, rows, step: float, ksize: float, vsize: float) -> float:
    for k, v, col in rows:
        cv.text(x, y, k, ksize, ON_BLUE_LABEL, MONO)
        cv.text(right, y, v, vsize, col, anchor="end")
        y += step
    return y


def wide(weeks: list[int]) -> str:
    W, H = 830, 410
    cv = Canvas(W, H)
    cv.grainy(0.5, 0.5, W - 1, H - 1, r=16, glows=((.16, 1.18, .85), (.96, -.25, .55)), seed=4)
    cv.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#FFFFFF" stroke-opacity=".14"/>')
    # title bar: the page's one breathing dot says who is available
    cv.icon("folder", 24, 15, 15, ON_BLUE_LABEL)
    cv.text(46, 27, "r204570 / profile", 12.5, ON_BLUE_LABEL, MONO)
    status = "Open to AI roles · freelance"
    cv.text(W - 24, 27, status, 12.5, ON_BLUE, MONO, anchor="end")
    cv.pulse(W - 24 - measure(status, MONO, 400, 12.5) - 14, 23, 3.5, SKY)
    hair(cv, 0.5, 44.5, W - 0.5, 44.5)
    # identity
    cv.text(28, 146, "Raj Patel", 78, ON_BLUE, SANS, 600, tracking=-2.6, extra=cv.speckle())
    y = 190
    for line in wrap(PITCH, SANS, 400, 18.5, 460):
        cv.text(32, y, line, 18.5, ON_BLUE_SOFT)
        y += 27
    command_box(cv, 32, y - 6, 468, 13)
    # profile and credentials
    hair(cv, 524.5, 44.5, 524.5, 300)
    cv.text(548, 78, "PROFILE", 11, ON_BLUE_LABEL, MONO, 500, tracking=1.4)
    kv(cv, 548, 806, 102, PROFILE, 24, 12.5, 13.5)
    cv.text(548, 212, "CREDENTIALS", 11, ON_BLUE_LABEL, MONO, 500, tracking=1.4)
    kv(cv, 548, 806, 236, [(k, v, ON_BLUE) for k, v in CREDENTIALS], 24, 12.5, 13.5)
    # live strip across the foot of the card
    hair(cv, 0.5, 316.5, W - 0.5, 316.5)
    strip(cv, 32, 344, W - 64, weeks, 11, 40)
    return cv.svg(TITLE, describe(sum(weeks)), comment=f"hidden part :: {NOTE}")


def narrow(weeks: list[int]) -> str:
    W = 360
    cv = Canvas(W, 2000)
    body: list[str] = []
    cv.text(16, 26, "r204570", 11.5, ON_BLUE_LABEL, MONO)
    status = "Open to AI roles"
    cv.text(W - 16, 26, status, 11.5, ON_BLUE, MONO, anchor="end")
    cv.pulse(W - 16 - measure(status, MONO, 400, 11.5) - 12, 22, 3, SKY)
    hair(cv, 0.5, 40.5, W - 0.5, 40.5)
    cv.text(14, 104, "Raj Patel", 52, ON_BLUE, SANS, 600, tracking=-1.6, extra=cv.speckle())
    y = 138
    for line in wrap(PITCH, SANS, 400, 15.5, 328):
        cv.text(16, y, line, 15.5, ON_BLUE_SOFT)
        y += 22
    command_box(cv, 16, y - 4, 328, 11.5)
    y = strip(cv, 16, y + 86, 328, weeks, 10.5, 40) + 30
    hair(cv, 0.5, y - 12.5, W - 0.5, y - 12.5)
    cv.text(16, y + 10, "PROFILE", 10.5, ON_BLUE_LABEL, MONO, 500, tracking=1.3)
    y = kv(cv, 16, W - 16, y + 34, PROFILE, 22, 12, 13) + 16
    cv.text(16, y, "CREDENTIALS", 10.5, ON_BLUE_LABEL, MONO, 500, tracking=1.3)
    y = kv(cv, 16, W - 16, y + 24, [(k, v, ON_BLUE) for k, v in CREDENTIALS], 22, 12, 13)
    H = y + 4
    cv.h = H
    body, defs = cv.parts, cv.defs
    cv.parts, cv.defs = [], []
    cv.grainy(0.5, 0.5, W - 1, H - 1, r=16, glows=((.1, 1.05, 1.1), (1.0, -.05, .7)), seed=4)
    cv.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#FFFFFF" stroke-opacity=".14"/>')
    cv.parts += body
    cv.defs += defs
    return cv.svg(TITLE, describe(sum(weeks)))
