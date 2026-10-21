"""Shared pieces for every profile panel: palette, grain, icons, type and text measurement.

Standard library only, so the activity Action can import it. Fonts are Geist and Geist Mono
(SIL OFL 1.1, scripts/fonts/OFL.txt), embedded in each SVG as WOFF2 data so the panels render
the same everywhere GitHub shows them.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from xml.sax.saxutils import escape

FONTS = Path(__file__).resolve().parent / "fonts"

# palette ---------------------------------------------------------------------
# Blue and black. The ground is GitHub's own dark ground, so a panel sits flush in dark mode and
# reads as a dark embedded console in light mode. Blue is the only accent; it marks state and action.
GROUND = "#0D1117"
PANEL = "#121821"      # raised boxes inside a panel
LIFT = "#18202B"       # hover-level lift, used for pills and the command box
SEAM = "#232C38"       # 1px seams
TEXT = "#E6EDF3"
SOFT = "#C3CDD8"       # body copy on the ground
MUTED = "#8B949E"      # labels, keys, secondary text (6.2:1 on GROUND)
BLUE = "#1F6FEB"       # primary action, chart body
BLUE_HI = "#58A6FF"    # live state, links
BLUE_LO = "#79C0FF"    # values that need to read as blue text (9.7:1 on GROUND)
WHITE = "#FFFFFF"
LABEL_LIGHT = "#59636E"  # section labels on GitHub's light ground
# on the grainy blue surface (hero, card headers): white type, two quieter whites
NIGHT = "#03050B"      # the black the blue fades into
ELECTRIC = "#2563EB"   # the brightest blue of the glow
ON_BLUE = "#FFFFFF"
ON_BLUE_SOFT = "#DCE6FF"
ON_BLUE_LABEL = "#C3D3FF"  # small labels; 4.6:1 even where the glow is brightest
GLASS = "#050811"      # boxes laid on the blue, at ~50% opacity

SANS, MONO = "Geist", "Geist Mono"
FACES = {  # css family, weight -> committed basic-latin subset
    (SANS, 400): "geist-400.woff2",
    (SANS, 500): "geist-500.woff2",
    (SANS, 600): "geist-600.woff2",
    (MONO, 400): "geistmono-400.woff2",
    (MONO, 500): "geistmono-500.woff2",
}

_metrics: dict | None = None


def metrics() -> dict:
    global _metrics
    if _metrics is None:
        _metrics = json.loads((FONTS / "metrics.json").read_text(encoding="utf-8"))
    return _metrics


def measure(s: str, family: str, weight: int, size: float, tracking: float = 0) -> float:
    """Advance width in px (no kerning), `tracking` in px per glyph."""
    m = metrics()[f"{family}:{weight}"]
    upm, adv = m["upm"], m["adv"]
    fallback = adv.get("n", upm / 2)
    return sum(adv.get(ch, fallback) for ch in s) * size / upm + tracking * max(len(s) - 1, 0)


def wrap(s: str, family: str, weight: int, size: float, room: float) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and measure(trial, family, weight, size) > room:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def fit(s: str, family: str, weight: int, size: float, room: float) -> str:
    if measure(s, family, weight, size) <= room:
        return s
    while s and measure(s + "…", family, weight, size) > room:
        s = s[:-1]
    return s.rstrip() + "…"


def font_css(used: set[tuple[str, int]], sources: dict | None = None) -> str:
    """@font-face rules for the faces a panel uses. `sources` maps (family, weight) to WOFF2
    bytes (the static build passes exact subsets); otherwise the committed subsets are used."""
    out = []
    for fam, wt in sorted(used):
        data = sources[(fam, wt)] if sources and (fam, wt) in sources else (FONTS / FACES[(fam, wt)]).read_bytes()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url(data:font/woff2;base64,"
                   f"{base64.b64encode(data).decode()}) format('woff2')}}")
    return "".join(out)


# drawing helpers ---------------------------------------------------------------
def n(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Canvas:
    """Collects SVG markup and remembers which faces it used."""

    def __init__(self, w: float, h: float):
        self.w, self.h = w, h
        self.parts: list[str] = []
        self.defs: list[str] = []
        self.css: list[str] = []
        self.used: set[tuple[str, int]] = set()
        self.chars: dict[tuple[str, int], set[str]] = {}  # what each face must carry

    def add(self, s: str) -> None:
        self.parts.append(s)

    def text(self, x, y, s, size, fill=TEXT, family=SANS, weight=400, anchor="start", tracking=0, extra=""):
        self.used.add((family, weight))
        self.chars.setdefault((family, weight), set()).update(s)
        ls = f' letter-spacing="{n(tracking)}"' if tracking else ""
        an = f' text-anchor="{anchor}"' if anchor != "start" else ""
        self.add(f'<text x="{n(x)}" y="{n(y)}" font-family="{family}" font-weight="{weight}" font-size="{n(size)}" '
                 f'fill="{fill}"{an}{ls}{extra}>{escape(s)}</text>')

    def rect(self, x, y, w, h, fill="none", stroke=None, r=0, extra=""):
        st = f' stroke="{stroke}"' if stroke else ""
        rr = f' rx="{n(r)}"' if r else ""
        self.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{rr} fill="{fill}"{st}{extra}/>')

    def line(self, x1, y1, x2, y2, stroke=SEAM, extra=""):
        """A 1px seam, snapped to the device grid so it stays sharp at 1x."""
        self.add(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{stroke}" shape-rendering="crispEdges"{extra}/>')

    def icon(self, name, x, y, size=16, stroke=MUTED, width=1.75):
        k = size / 24
        self.add(f'<g transform="translate({n(x)} {n(y)}) scale({n(k)})" fill="none" stroke="{stroke}" '
                 f'stroke-width="{n(width / k)}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')

    def speckle(self) -> str:
        """Film grain in the lit marks themselves (type, bars, the primary fill): noise clipped to
        the shape and multiplied over it. Returns the attribute to put on an element or group."""
        if not any('id="speckle"' in d for d in self.defs):
            self.defs.append(
                '<filter id="speckle" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                '<feTurbulence type="fractalNoise" '
                'baseFrequency=".95" numOctaves="2" seed="11" result="noise"/><feColorMatrix in="noise" type="saturate" '
                'values="0" result="grey"/><feComponentTransfer in="grey" result="tone"><feFuncR type="linear" slope=".75" '
                'intercept=".5"/><feFuncG type="linear" slope=".75" intercept=".5"/><feFuncB type="linear" slope=".75" '
                'intercept=".5"/><feFuncA type="linear" slope="0" intercept="1"/></feComponentTransfer>'
                '<feComposite in="tone" in2="SourceGraphic" operator="in" result="clip"/>'
                '<feBlend in="SourceGraphic" in2="clip" mode="multiply"/></filter>')
        return ' filter="url(#speckle)"'

    def logo(self, d: str, x, y, size=16, fill=TEXT):
        """A Simple Icons mark (24px grid, filled)."""
        self.add(f'<path transform="translate({n(x)} {n(y)}) scale({n(size / 24)})" d="{d}" fill="{fill}"/>')

    def dot(self, cx, cy, r=3.5, fill=BLUE_HI):
        self.add(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"/>')

    def pulse(self, cx, cy, r=4, fill=BLUE_HI):
        """The one moving thing on the page: a live dot breathing. Still when motion is reduced."""
        self.add(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 2.2)}" fill="{fill}" opacity=".18" class="halo"/>'
                 f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}"/>')
        if ".halo" not in "".join(self.css):
            self.css.append(".halo{animation:halo 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center}"
                            "@keyframes halo{0%{opacity:.35;transform:scale(.5)}100%{opacity:0;transform:scale(1.25)}}")

    def panel(self, x=0.5, y=0.5, w=None, h=None, r=12, glow=None):
        """The console ground: GitHub's dark, a 1px seam, fine grain and a faint dot grid.
        `glow` places a soft blue wash at (cx, cy, radius)."""
        w = self.w - 1 if w is None else w
        h = self.h - 1 if h is None else h
        self.defs.append(
            '<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            '<feTurbulence type="fractalNoise" baseFrequency=".9" '
            'numOctaves="2" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
            '<feComponentTransfer><feFuncA type="table" tableValues="0 .14"/></feComponentTransfer></filter>'
            '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".75" '
            f'fill="{TEXT}" opacity=".07"/></pattern>'
            f'<clipPath id="pc"><rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(r)}"/></clipPath>')
        self.rect(x, y, w, h, GROUND, r=r)
        if glow:
            gx, gy, gr = glow
            self.defs.append(f'<radialGradient id="wash" cx="{n(gx)}" cy="{n(gy)}" r="{n(gr)}" gradientUnits="userSpaceOnUse">'
                             f'<stop offset="0" stop-color="{BLUE}" stop-opacity=".22"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>')
            self.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="url(#wash)" clip-path="url(#pc)"/>')
        self.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" fill="url(#dots)" clip-path="url(#pc)"/>')
        self.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" filter="url(#grain)" clip-path="url(#pc)"/>')
        self.rect(x, y, w, h, stroke=SEAM, r=r)

    def grainy(self, x, y, w, h, r=14, glows=((.12, 1.1, .8), (.92, -.15, .5)), seed=4, corners="all"):
        """The blue-and-black surface: black with soft electric-blue glows, under visible white and
        black film grain. `glows` are (cx, cy, radius) as fractions of the box. `corners`: "all"
        rounds every corner, "top" only the top two (a card header band)."""
        k = len([d for d in self.defs if 'id="g' in d])
        cid, wid, bid = f"gc{k}", f"gw{k}", f"gb{k}"
        if corners == "top":
            shape = (f'<path d="M{n(x)} {n(y + h)}V{n(y + r)}a{n(r)} {n(r)} 0 0 1 {n(r)} {n(-r)}H{n(x + w - r)}'
                     f'a{n(r)} {n(r)} 0 0 1 {n(r)} {n(r)}V{n(y + h)}Z"/>')
        else:
            shape = f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(r)}"/>'
        grads = []
        for i, (gx, gy, gr) in enumerate(glows):
            gid = f"g{k}r{i}"
            hot = ELECTRIC if i == 0 else "#3B82F6"
            grads.append(f'<radialGradient id="{gid}" cx="{n(x + gx * w)}" cy="{n(y + gy * h)}" r="{n(gr * w)}" gradientUnits="userSpaceOnUse">'
                         f'<stop offset="0" stop-color="{hot}" stop-opacity="{.95 if i == 0 else .7}"/>'
                         f'<stop offset=".45" stop-color="{BLUE}" stop-opacity="{.55 if i == 0 else .3}"/>'
                         f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>')
        self.defs.append(
            f'<clipPath id="{cid}">{shape}</clipPath>' + "".join(grads) +
            f'<filter id="{wid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency=".78" numOctaves="3" seed="{seed}" stitchTiles="stitch"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 3.2 0 0 0 -1.68"/></filter>'
            f'<filter id="{bid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
            f'<feTurbulence type="fractalNoise" baseFrequency=".78" numOctaves="3" seed="{seed + 31}" stitchTiles="stitch"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -3.2 0 0 0 1.5"/></filter>')
        box = f'x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" clip-path="url(#{cid})"'
        self.add(f'<rect {box} fill="{NIGHT}"/>')
        for i in range(len(glows)):
            self.add(f'<rect {box} fill="url(#g{k}r{i})"/>')
        self.add(f'<rect {box} fill="url(#dots)" opacity=".8"/>' if any('id="dots"' in d for d in self.defs) else "")
        self.add(f'<rect {box} filter="url(#{wid})" opacity=".42"/><rect {box} filter="url(#{bid})" opacity=".5"/>')

    def svg(self, title: str, desc: str = "", fonts: dict | None = None, comment: str = "") -> str:
        lab = "t d" if desc else "t"
        d = f'<desc id="d">{escape(desc)}</desc>' if desc else ""
        cm = f"\n<!-- {comment} -->" if comment else ""
        css = font_css(self.used, fonts) + "".join(self.css) + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(self.w)} {n(self.h)}" width="{n(self.w)}" '
                f'height="{n(self.h)}" role="img" aria-labelledby="{lab}">{cm}\n<title id="t">{escape(title)}</title>{d}'
                f"<style>{css}</style>{defs}\n{''.join(self.parts)}\n</svg>\n")


# icons -------------------------------------------------------------------------
# Line icons on a 24px grid, after Lucide (ISC licence), drawn in one stroke weight.
ICONS = {
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
            '<path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/>'
                '<circle cx="4" cy="4" r="2"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>'
           '<path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "commit": '<circle cx="12" cy="12" r="3"/><path d="M3 12h6"/><path d="M15 12h6"/>',
    "merge": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/>',
    "dot": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="1"/>',
    "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "external": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/>'
             '<path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "star": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "plug": '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/>'
              '<path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    # pipeline stages
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/>'
           '<path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/>'
           '<path d="M15 13v2"/><path d="M9 13v2"/>',
    "server": '<rect width="20" height="8" x="2" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><path d="M6 6h.01"/><path d="M6 18h.01"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>'
              '<path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>'
              '<path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
}
