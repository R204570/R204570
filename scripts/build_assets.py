"""Rebuilds the static profile SVGs (scan, atlas, weave, thread). Edit the text in here, then run: python3 scripts/build_assets.py"""
import base64, math, random, codecs, sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"
OUT.mkdir(parents=True, exist_ok=True)

def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()

FONT_CSS = f"""
@font-face{{font-family:'JBM';font-weight:400;src:url(data:font/woff;base64,{b64(FONTS/'jbm-400.woff')}) format('woff')}}
@font-face{{font-family:'JBM';font-weight:700;src:url(data:font/woff;base64,{b64(FONTS/'jbm-700.woff')}) format('woff')}}
"""
SERIF_CSS = f"""@font-face{{font-family:'ISI';font-style:italic;src:url(data:font/woff;base64,{b64(FONTS/'is-italic.woff')}) format('woff')}}"""
MONO = "'JBM','JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# palette ---------------------------------------------------------------
BG, LINE, DIM, FAINT, TXT = "#07090D", "#1A2130", "#7D8899", "#3A4352", "#E8ECF1"
CYAN, GREEN, YELLOW, RED = "#4FD8EB", "#2BD47A", "#FFD23F", "#FF4D5E"

def f(x): return f"{x:.1f}".rstrip("0").rstrip(".")

def closed_path(pts):
    n = len(pts); d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[(i+1)%n], pts[(i+2)%n]
        c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d += f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d + "Z"

def open_path(pts):
    pts = [pts[0]] + pts + [pts[-1]]
    d = f"M{f(pts[1][0])},{f(pts[1][1])}"
    for i in range(1, len(pts)-2):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
        c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d += f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d

class Wobble:
    """Smooth periodic noise on a circle."""
    def __init__(self, rng, terms):  # terms: list of (k, amp)
        self.t = [(k, a, rng.uniform(0, 2*math.pi)) for k, a in terms]
    def __call__(self, th):
        return sum(a*math.sin(k*th+ph) for k, a, ph in self.t)

def ellipse_pts(cx, cy, rx, ry, wob, n=180, scale=1.0):
    pts = []
    for i in range(n):
        th = 2*math.pi*i/n
        r = scale*(1+wob(th))
        pts.append((cx+rx*r*math.cos(th), cy+ry*r*math.sin(th)))
    return pts

def blob(cx, cy, r, rng, n=40, rough=0.12):
    w = Wobble(rng, [(2, rough*.6), (3, rough*.5), (5, rough*.35), (7, rough*.2)])
    return closed_path(ellipse_pts(cx, cy, r, r*0.92, w, n))

# ======================================================================
# 1. HERO — MRI viewport + radiology report
# ======================================================================
def build_scan():
    rng = random.Random(204570)
    W, H = 840, 440
    VX, VY, VS = 14, 14, 412
    cx, cy = VX+VS/2, VY+VS/2 + 2
    RX, RY = 134, 172

    o = []
    # --- skull & brain layers (axial T1ce look) ---
    scalp_w = Wobble(rng, [(2, .012), (3, .01), (5, .006)])
    scalp = ellipse_pts(cx, cy, RX, RY, scalp_w, 160)
    bone = ellipse_pts(cx, cy, RX, RY, scalp_w, 160, .935)
    csf = ellipse_pts(cx, cy, RX, RY, scalp_w, 160, .895)
    gyr = Wobble(rng, [(2, .01), (3, .012), (29, .014), (41, .01), (57, .007)])
    cortex = ellipse_pts(cx, cy, RX*.875, RY*.875, gyr, 260)
    wm_w = Wobble(rng, [(2, .02), (3, .02), (19, .05), (31, .04), (47, .025)])
    wm = ellipse_pts(cx, cy, RX*.66, RY*.68, wm_w, 260)

    o.append(f'<path d="{closed_path(scalp)}" fill="url(#scalpG)"/>')
    o.append(f'<path d="{closed_path(bone)}" fill="#15181d"/>')
    o.append(f'<path d="{closed_path(csf)}" fill="#2a2e35"/>')
    o.append(f'<path d="{closed_path(cortex)}" fill="url(#gmG)"/>')
    o.append(f'<path d="{closed_path(wm)}" fill="url(#wmG)"/>')

    # deep gray nuclei
    for s in (-1, 1):
        o.append(f'<ellipse cx="{f(cx+s*44)}" cy="{f(cy+6)}" rx="12" ry="28" fill="#737a84" opacity=".55" transform="rotate({s*-8} {f(cx+s*44)} {f(cy+6)})"/>')
        o.append(f'<ellipse cx="{f(cx+s*17)}" cy="{f(cy+20)}" rx="10" ry="16" fill="#7c838c" opacity=".5"/>')

    # sulci
    sul = []
    N = 58
    for i in range(N):
        th = 2*math.pi*i/N + rng.uniform(-.04, .04)
        if abs(math.cos(th)) < .08:  # leave the midline fissure clean
            continue
        r0 = .875*(1+gyr(th))*.995
        depth = rng.uniform(.74, .86)
        pts = []
        for k in range(5):
            t = k/4
            r = r0 - (r0-depth*r0)*t
            ang = th + rng.uniform(-.035, .035)*(1 if k else 0) + .02*math.sin(t*5+i)
            pts.append((cx+RX*r*math.cos(ang), cy+RY*r*math.sin(ang)))
        sul.append(open_path(pts))
    o.append(f'<path d="{" ".join(sul)}" fill="none" stroke="#1f2328" stroke-width="2.1" stroke-linecap="round" opacity=".9"/>')
    # midline fissure
    top = cy-RY*.875*(1+gyr(-math.pi/2)); bot = cy+RY*.875*(1+gyr(math.pi/2))
    o.append(f'<path d="M{f(cx)},{f(top+1)} C{f(cx+2)},{f(top+30)} {f(cx-2)},{f(cy-90)} {f(cx)},{f(cy-66)} M{f(cx)},{f(cy+80)} C{f(cx+2)},{f(cy+110)} {f(cx-1)},{f(bot-30)} {f(cx)},{f(bot-1)}" fill="none" stroke="#14171b" stroke-width="3.2" stroke-linecap="round"/>')

    # lateral ventricles
    cl = [(-5, -60, 4), (-15, -50, 9), (-21, -28, 8), (-20, 2, 6), (-22, 28, 7), (-30, 54, 8), (-37, 72, 3)]
    for s in (1, -1):
        left, right = [], []
        for j, (x, y, w) in enumerate(cl):
            x2, y2 = cl[min(j+1, len(cl)-1)][:2]; x1, y1 = cl[max(j-1, 0)][:2]
            dx, dy = (x2-x1), (y2-y1); L = math.hypot(dx, dy) or 1
            nx, ny = -dy/L, dx/L
            left.append((cx+s*(x+nx*w), cy+y+ny*w)); right.append((cx+s*(x-nx*w), cy+y-ny*w))
        o.append(f'<path d="{closed_path(left+right[::-1])}" fill="#0c0e11"/>')

    # lesion as it appears on the scan (before segmentation)
    tx, ty = cx-60, cy-50
    lr = random.Random(7)
    o.append(f'<path d="{blob(tx, ty, 40, lr, rough=.16)}" fill="#8d949c" opacity=".35"/>')
    o.append(f'<path d="{blob(tx, ty, 22, lr, rough=.14)}" fill="#e4e8ec" opacity=".9"/>')
    o.append(f'<path d="{blob(tx, ty, 14, lr, rough=.18)}" fill="#2a2e33"/>')

    anatomy = "\n".join(o)
    skull_clip = closed_path(scalp)

    # --- segmentation overlay (BraTS label colours) ---
    sr = random.Random(7)
    ed = blob(tx, ty, 40, sr, rough=.16); et = blob(tx, ty, 22, sr, rough=.14); nc = blob(tx, ty, 14, sr, rough=.18)
    seg = f'''
      <path d="{ed}" fill="{GREEN}" fill-opacity=".34" stroke="{GREEN}" stroke-width="1" stroke-opacity=".9"/>
      <path d="{et} {nc}" fill="{YELLOW}" fill-rule="evenodd" fill-opacity=".72" stroke="{YELLOW}" stroke-width=".8"/>
      <path d="{nc}" fill="{RED}" fill-opacity=".75" stroke="{RED}" stroke-width=".8"/>'''

    # --- ROI annotation ---
    bx0, by0, bx1, by1 = tx-48, ty-46, tx+48, ty+46
    br = 9
    brackets = (f"M{bx0},{by0+br}V{by0}H{bx0+br} M{bx1-br},{by0}H{bx1}V{by0+br} "
                f"M{bx1},{by1-br}V{by1}H{bx1-br} M{bx0+br},{by1}H{bx0}V{by1-br}")
    roi = f'''
      <path d="{brackets}" fill="none" stroke="{CYAN}" stroke-width="1.4"/>
      <rect x="{f(bx0)}" y="{f(by0-19)}" width="166" height="14" rx="2" fill="#000" fill-opacity=".72"/>
      <text x="{f(bx0+5)}" y="{f(by0-9)}" class="m" font-size="9" fill="{CYAN}" font-weight="700" letter-spacing=".6">ROI-1 CURIOSITY (ENHANCING)</text>
      <line x1="{f(tx-21)}" y1="{f(ty+27)}" x2="{f(tx+21)}" y2="{f(ty+27)}" stroke="{CYAN}" stroke-width=".9"/>
      <line x1="{f(tx-21)}" y1="{f(ty+24)}" x2="{f(tx-21)}" y2="{f(ty+30)}" stroke="{CYAN}" stroke-width=".9"/>
      <line x1="{f(tx+21)}" y1="{f(ty+24)}" x2="{f(tx+21)}" y2="{f(ty+30)}" stroke="{CYAN}" stroke-width=".9"/>
      <text x="{f(tx)}" y="{f(ty+37)}" class="m" font-size="8" fill="{CYAN}" text-anchor="middle">31.4 mm</text>'''

    # rulers / crosshair
    ticks = "".join(f'<line x1="{VX+6}" x2="{VX+(12 if k % 5 == 0 else 9)}" y1="{150+k*7}" y2="{150+k*7}"/>' for k in range(21))

    # --- typed impression lines ---
    lines = ["builds agents that actually use tools",
             "trains models that see inside skulls",
             "ships to prod, not just to main"]
    cw = 7.5  # JBM @ 12.5px advance
    typed, clips = [], []
    t0 = 1.2
    for i, s in enumerate(lines):
        n = len(s) + 2
        dur = n*0.045
        widths = ";".join(f(k*cw) for k in range(n+1))
        clips.append(f'<clipPath id="ty{i}"><rect x="446" y="{282+i*21}" height="18" width="0"><animate attributeName="width" values="{widths}" dur="{dur:.2f}s" begin="{t0:.2f}s" calcMode="discrete" fill="freeze"/></rect></clipPath>')
        typed.append(f'<text x="446" y="{296+i*21}" class="m" font-size="12.5" clip-path="url(#ty{i})"><tspan fill="{GREEN}" font-weight="700">&gt;</tspan><tspan fill="{TXT}"> {s}</tspan></text>')
        t0 += dur + .35
    cursor_y = 282 + 2*21
    cursor_x = 446 + (len(lines[-1])+2)*cw + 2

    # dice bars
    dice = [("WT", .91, GREEN, "whole tumour"), ("TC", .87, RED, "tumour core"), ("ET", .84, YELLOW, "enhancing")]
    bars = []
    for i, (lab, v, col, desc) in enumerate(dice):
        y = 384 + i*15
        bars.append(f'''<text x="446" y="{y+5}" class="m" font-size="9.5" fill="{DIM}" font-weight="700">{lab}</text>
      <rect x="470" y="{y-1}" width="190" height="6" rx="3" fill="#111722"/>
      <rect x="470" y="{y-1}" height="6" rx="3" fill="{col}" width="0"><animate attributeName="width" from="0" to="{f(190*v)}" dur="1.1s" begin="{.5+i*.18:.2f}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>
      <text x="670" y="{y+5}" class="m" font-size="10" fill="{TXT}" font-weight="700">{v:.2f}</text>
      <text x="704" y="{y+5}" class="m" font-size="9" fill="{FAINT}">{desc}</text>''')

    flag = "RAJ{s0urc3_r34d3r_d3t3ct3d}"
    note = codecs.encode(flag, "rot13")

    fields = [("PATIENT ID", "R204570"), ("LOCATION", "Ahmedabad, IN · UTC+5:30"),
              ("HISTORY", "Intel · Microsoft Elevate · GTU"), ("REFERRAL", "open to AI roles + freelance")]
    field_svg = "".join(
        f'<text x="446" y="{186+i*20}" class="m" font-size="9.5" fill="{DIM}" letter-spacing="1.2">{k}</text>'
        f'<text x="556" y="{186+i*20}" class="m" font-size="12" fill="{TXT}">{v}</text>' for i, (k, v) in enumerate(fields))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Raj Patel — case R204570</title>
<desc id="d">An animated MRI viewer: a scanner line sweeps an axial brain slice and reveals a BraTS-coloured segmentation labelled "curiosity (enhancing)". Beside it, a radiology report for Raj Patel, AI engineer in Ahmedabad.</desc>
<!-- radiologist's note, not for the chart: {note} -->
<style>{FONT_CSS}{SERIF_CSS}
.m{{font-family:{MONO}}}
.blink{{animation:bl 1.05s steps(1) infinite}}
@keyframes bl{{50%{{opacity:0}}}}
.pulse{{animation:pu 2.4s ease-in-out infinite}}
@keyframes pu{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.blink,.pulse{{animation:none}}}}
</style>
<defs>
  <radialGradient id="scalpG" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#c9cfd6"/><stop offset=".85" stop-color="#aab1b9"/><stop offset="1" stop-color="#6f767e"/></radialGradient>
  <radialGradient id="gmG" cx="50%" cy="46%" r="58%"><stop offset="0" stop-color="#6a717a"/><stop offset="1" stop-color="#545a62"/></radialGradient>
  <radialGradient id="wmG" cx="50%" cy="48%" r="60%"><stop offset="0" stop-color="#a7adb5"/><stop offset=".8" stop-color="#959ba3"/><stop offset="1" stop-color="#868c95"/></radialGradient>
  <radialGradient id="vig" cx="50%" cy="50%" r="62%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".28"/></linearGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.15" numOctaves="2" seed="11" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
  <filter id="soft" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation=".55"/></filter>
  <clipPath id="vp"><rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" rx="8"/></clipPath>
  <clipPath id="skull"><path d="{skull_clip}"/></clipPath>
  <clipPath id="reveal"><rect x="{VX}" y="{VY}" width="{VS}" height="0">
    <animate attributeName="height" values="0;{VS};{VS};{VS}" keyTimes="0;.45;.96;1" dur="10s" repeatCount="indefinite"/></rect></clipPath>
  {"".join(clips)}
</defs>

<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{LINE}"/>

<!-- ============ VIEWPORT ============ -->
<g clip-path="url(#vp)">
  <rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" fill="#000"/>
  <g filter="url(#soft)">{anatomy}</g>
  <rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" filter="url(#grain)" opacity=".13" clip-path="url(#skull)"/>
  <rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" fill="url(#vig)"/>

  <g clip-path="url(#reveal)">
    <g>{seg}
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.88;.96;1" dur="10s" repeatCount="indefinite"/>
    </g>
  </g>
  <g opacity="0">{roi}
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;.45;.5;.88;.94;1" dur="10s" repeatCount="indefinite"/>
  </g>

  <g stroke="{CYAN}" stroke-opacity=".22" stroke-width=".8" stroke-dasharray="3 5">
    <line x1="{VX}" x2="{VX+VS}" y1="{f(ty)}" y2="{f(ty)}"/><line y1="{VY}" y2="{VY+VS}" x1="{f(tx)}" x2="{f(tx)}"/>
  </g>
  <g stroke="#cfd5dc" stroke-opacity=".55" stroke-width=".8">{ticks}</g>

  <!-- scanner beam -->
  <g>
    <rect x="{VX}" y="{VY-46}" width="{VS}" height="46" fill="url(#beam)"/>
    <rect x="{VX}" y="{VY-1.5}" width="{VS}" height="1.6" fill="{CYAN}"/>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 {VS};0 {VS}" keyTimes="0;.45;1" dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.45;.46;1" dur="10s" repeatCount="indefinite"/>
  </g>

  <!-- DICOM overlay -->
  <g class="m" font-size="10" fill="#d5dae1" fill-opacity=".86">
    <text x="{VX+12}" y="{VY+20}" font-weight="700">PATEL^RAJ</text>
    <text x="{VX+12}" y="{VY+34}">ID R204570</text>
    <text x="{VX+12}" y="{VY+48}">AHMEDABAD · IN</text>
    <text x="{VX+VS-12}" y="{VY+20}" text-anchor="end" font-weight="700">GTU · SAL ETI</text>
    <text x="{VX+VS-12}" y="{VY+34}" text-anchor="end">AX T1ce 3D</text>
    <text x="{VX+VS-12}" y="{VY+48}" text-anchor="end">IM 77/155</text>
    <text x="{VX+12}" y="{VY+VS-38}">3D ATTN U-NET</text>
    <text x="{VX+12}" y="{VY+VS-24}">BraTS 2020</text>
    <text x="{VX+12}" y="{VY+VS-10}">W 400  L 40</text>
    <text x="{VX+VS-12}" y="{VY+VS-38}" text-anchor="end" font-weight="700">Dx CHRONIC CURIOSITY</text>
    <text x="{VX+VS-12}" y="{VY+VS-24}" text-anchor="end">Px KEEPS SHIPPING</text>
    <text x="{VX+VS-12}" y="{VY+VS-10}" text-anchor="end">SE 2026</text>
  </g>
  <g class="m" font-size="11" font-weight="700" fill="{CYAN}" fill-opacity=".8" text-anchor="middle">
    <text x="{VX+VS/2}" y="{VY+16}">A</text><text x="{VX+VS/2}" y="{VY+VS-6}">P</text>
    <text x="{VX+24}" y="{f(cy+4)}">R</text><text x="{VX+VS-24}" y="{f(cy+4)}">L</text>
  </g>
</g>
<rect x="{VX}" y="{VY}" width="{VS}" height="{VS}" rx="8" fill="none" stroke="#1d2533"/>

<!-- ============ REPORT ============ -->
<g class="m">
  <circle cx="450" cy="34" r="3.2" fill="{RED}" class="pulse"/>
  <text x="460" y="38" font-size="10" font-weight="700" fill="{CYAN}" letter-spacing="2">RADIOLOGY REPORT</text>
  <text x="826" y="38" font-size="10" fill="{DIM}" letter-spacing="1.5" text-anchor="end">CASE R204570</text>
  <line x1="446" x2="826" y1="50" y2="50" stroke="{LINE}"/>
</g>
<text x="443" y="120" font-family="'ISI','Instrument Serif',Georgia,serif" font-style="italic" font-size="70" fill="#F3F5F8" letter-spacing="-.5">Raj Patel</text>
<text x="446" y="150" class="m" font-size="12" fill="#9AA4B2">AI engineer · agentic systems · medical imaging</text>
{field_svg}
<text x="446" y="272" class="m" font-size="9.5" fill="{DIM}" letter-spacing="1.2">IMPRESSION</text>
{"".join(typed)}
<g opacity="0"><set attributeName="opacity" to="1" begin="{t0-.3:.2f}s" fill="freeze"/><rect x="{f(cursor_x)}" y="{cursor_y+3}" width="7.5" height="14" fill="{GREEN}" class="blink"/></g>
<text x="446" y="368" class="m" font-size="9.5" fill="{DIM}" letter-spacing="1.2">NEUROASSIST · DICE</text>
{"".join(bars)}
</svg>'''
    (OUT/"scan.svg").write_text(svg)
    return flag, note

# ======================================================================
# 2. LOBE ATLAS — skills mapped onto a lateral brain
# ======================================================================
def build_atlas():
    rng = random.Random(42)
    W, H = 840, 392
    OX, OY = 250, 54

    cerebrum = [(18,138),(12,104),(22,70),(48,38),(88,15),(140,5),(195,7),(245,21),(290,49),(322,87),(334,127),
                (327,159),(302,178),(262,187),(222,191),(180,197),(140,197),(110,187),(95,171),(89,153),(70,150),(45,152),(26,148)]
    cereb = ellipse_pts(270, 207, 54, 30, Wobble(rng, [(2,.03),(3,.03)]), 60)
    stem = [(204,182),(232,178),(238,212),(240,250),(234,262),(216,262),(212,236),(206,206)]

    regions = {
        "frontal":   [(-20,-20),(176,-20),(170,40),(157,92),(142,140),(115,146),(88,152),(-20,166)],
        "parietal":  [(176,-20),(296,-20),(284,36),(277,80),(273,112),(236,104),(216,120),(178,131),(142,140),(157,92),(170,40)],
        "occipital": [(296,-20),(400,-20),(400,280),(262,280),(262,186),(268,150),(273,112),(277,80),(284,36)],
        "temporal":  [(88,152),(115,146),(142,140),(178,131),(216,120),(236,104),(273,112),(268,150),(262,186),(262,280),(-20,280),(-20,166)],
    }
    def poly(p): return "M" + " L".join(f"{f(x)},{f(y)}" for x, y in p) + "Z"

    lobes = [  # key, centroid(local), blob r, label side, label y, title, line1, line2, anchor(local)
        ("frontal",   (78, 82), 78,  "L", 92,  "FRONTAL — reasoning",       "Agentic AI · RAG · tool use",  "MCP servers · Claude Code",     (70, 70)),
        ("parietal",  (226, 62), 62, "R", 84,  "PARIETAL — integration",    "FastAPI · Django · Flask",     "Postgres+pgvector · Redis",     (222, 56)),
        ("occipital", (304, 122), 52,"R", 172, "OCCIPITAL — vision",        "PyTorch · TensorFlow",         "YOLOv8 · OpenCV · 3D U-Net",    (306, 120)),
        ("cerebellum",(270, 208), 50,"R", 262, "CEREBELLUM — coordination", "Streamlit · Node.js · GCP",    "Render · Vercel · Netlify",     (290, 212)),
        ("brainstem", (224, 232), 34,"L", 330, "BRAINSTEM — survival",      "CPTE · STRIDE threat models",  "OWASP LLM Top 10 · DPDP",       (224, 240)),
        ("temporal",  (176, 162), 64,"L", 230, "TEMPORAL — language",       "LLMs/SLMs · NLP · Hugging Face","pandas · NumPy · scikit-learn",(160, 168)),
    ]
    CYCLE = 12.0; SLOT = CYCLE/len(lobes)

    def kt(i):
        n = len(lobes); a = i/n; b = (i+1)/n
        ts = [0, a, min(a+.02, 1), max(b-.02, 0), b, 1]
        vs = [0, 0, 1, 1, 0, 0]
        if i == 0: vs[0] = 0
        return ";".join(f"{t:.3f}" for t in ts), ";".join(str(v) for v in vs)

    # gyri texture: streamlines through a smooth angle field, so folds run parallel and rarely cross
    fr = random.Random(9)
    terms = [(fr.uniform(-.07, .07), fr.uniform(-.07, .07), fr.uniform(0, 6.3), fr.uniform(.9, 1.5)) for _ in range(5)]
    def field(x, y): return sum(a*math.sin(kx*x + ky*y + ph) for kx, ky, ph, a in terms)
    gy = []
    for _ in range(150):
        x, y = fr.uniform(10, 335), fr.uniform(5, 195)
        pts = [(x, y)]; sgn = fr.choice((-1, 1))
        for _ in range(fr.randint(6, 12)):
            a = field(x, y)*1.6
            x += 5*math.cos(a)*sgn; y += 5*math.sin(a)*sgn
            pts.append((x, y))
        gy.append(open_path(pts))
    folia = "".join(f'<path d="M{f(222+k*2)},{f(188+k*7)} Q270,{f(180+k*8+ (6 if k%2 else 2))} {f(322-k*3)},{f(194+k*6)}"/>' for k in range(1, 6))

    blobs, blobs2, labels, dots = [], [], [], []
    for i, (key, (gx, gyy), r, side, ly, title, l1, l2, (ax, ay)) in enumerate(lobes):
        keyt, vals = kt(i)
        anim = f'<animate attributeName="opacity" values="{vals}" keyTimes="{keyt}" dur="{CYCLE}s" repeatCount="indefinite"/>'
        clip = "cereb" if key == "cerebellum" else "stem" if key == "brainstem" else f"lobe-{key}"
        g = f'<g clip-path="url(#{clip})" opacity="0"><circle cx="{gx}" cy="{gyy}" r="{r}" fill="url(#hot)"/>{anim}</g>'
        (blobs if clip.startswith("lobe") else blobs2).append(g)
        X, Y = OX+ax, OY+ay
        if side == "L":
            tx, anchor, ex = 236, "end", 244
        else:
            tx, anchor, ex = 604, "start", 596
        leader = f'M{f(X)},{f(Y)} L{f(ex + (12 if side=="L" else -12))},{ly-4} H{ex}'
        dots.append(f'<path d="{leader}" fill="none" stroke="#3A4558" stroke-width="1"/>'
                    f'<g opacity="0"><path d="{leader}" fill="none" stroke="#FFB020" stroke-width="1.2"/>{anim}</g>'
                    f'<circle cx="{f(X)}" cy="{f(Y)}" r="3" fill="{BG}" stroke="#8C98AA" stroke-width="1.2"/>'
                    f'<g opacity="0"><circle cx="{f(X)}" cy="{f(Y)}" r="3.6" fill="#FFF3B0"/>{anim}</g>')
        labels.append(f'''<g class="m" text-anchor="{anchor}">
    <text x="{tx}" y="{ly}" font-size="10" font-weight="700" letter-spacing="1.4" fill="#6F7B8C">{title}</text>
    <g opacity="0"><text x="{tx}" y="{ly}" font-size="10" font-weight="700" letter-spacing="1.4" fill="#FFB020">{title}</text>{anim}</g>
    <text x="{tx}" y="{ly+18}" font-size="12" fill="#DDE3EA">{l1}</text>
    <text x="{tx}" y="{ly+34}" font-size="12" fill="#AEB7C3">{l2}</text>
  </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Lobe atlas — Raj's skills</title>
<desc id="d">A lateral brain whose lobes light up in turn, each mapped to a skill area: frontal = agentic AI, RAG, MCP; parietal = FastAPI, Django, Postgres; occipital = computer vision; temporal = language models and data; cerebellum = deployment; brainstem = security.</desc>
<style>{FONT_CSS}.m{{font-family:{MONO}}}</style>
<defs>
  <radialGradient id="hot"><stop offset="0" stop-color="#FFF6C2"/><stop offset=".28" stop-color="#FFC531"/><stop offset=".6" stop-color="#FF5A2C" stop-opacity=".85"/><stop offset="1" stop-color="#C21F3A" stop-opacity="0"/></radialGradient>
  <linearGradient id="tissue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3948"/><stop offset="1" stop-color="#1A222D"/></linearGradient>
  <clipPath id="cer"><path d="{closed_path(cerebrum)}"/></clipPath>
  <clipPath id="cereb"><path d="{closed_path(cereb)}"/></clipPath>
  <clipPath id="stem"><path d="{closed_path(stem)}"/></clipPath>
  {"".join(f'<clipPath id="lobe-{k}"><path d="{poly(p)}"/></clipPath>' for k, p in regions.items())}
</defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{LINE}"/>
<text x="20" y="32" class="m" font-size="12" font-weight="700" fill="{CYAN}">build_lobe_atlas<tspan fill="{DIM}">(</tspan><tspan fill="{TXT}">raj</tspan><tspan fill="{DIM}">)</tspan></text>
<text x="820" y="32" class="m" font-size="10" fill="{DIM}" text-anchor="end" letter-spacing="1">fMRI · hot = firing now</text>

<g transform="translate({OX} {OY})">
  <path d="{closed_path(stem)}" fill="url(#tissue)" stroke="#3A4558" stroke-width="1.2"/>
  <path d="{closed_path(cereb)}" fill="url(#tissue)" stroke="#3A4558" stroke-width="1.2"/>
  <g fill="none" stroke="#0F141B" stroke-width="1.6" clip-path="url(#cereb)">{folia}</g>
  <g style="mix-blend-mode:screen">{"".join(blobs2)}</g>
  <path d="{closed_path(cerebrum)}" fill="url(#tissue)" stroke="#3A4558" stroke-width="1.4"/>
  <g style="mix-blend-mode:screen"><g clip-path="url(#cer)">{"".join(blobs)}</g></g>
  <g clip-path="url(#cer)" fill="none" stroke-linecap="round">
    <path d="{" ".join(gy)}" stroke="#0E131A" stroke-width="2.4" opacity=".75"/>
    <path d="{" ".join(gy)}" stroke="#4A5869" stroke-width=".8" opacity=".45" transform="translate(-.8 -.8)"/>
    <path d="M176,-2 C172,40 160,90 142,140 M88,152 C130,140 180,132 216,120 C228,114 234,108 238,102 M284,36 C278,80 270,140 262,188" stroke="#0A0E13" stroke-width="3.2"/>
  </g>
</g>
{"".join(dots)}
{"".join(labels)}
<text x="820" y="378" class="m" font-size="9.5" fill="{FAINT}" text-anchor="end">6 regions · 2s each · loops forever</text>
</svg>'''
    (OUT/"atlas.svg").write_text(svg)

# ======================================================================
# 3. WEAVE — footer + thin divider
# ======================================================================
def weave(W, H, rows, label=None, gold_row=None, pitch=12):
    cols = W//pitch + 2
    th = pitch*0.74
    weft_cols = ["#184C57", "#195A50", "#1D506A", "#163F50"]
    o = []
    # warp (vertical, under everything first)
    for c in range(cols):
        x = c*pitch
        o.append(f'<rect x="{f(x+(pitch-th)/2)}" y="0" width="{f(th)}" height="{H}" fill="url(#warp)"/>')
    for r in range(rows):
        y = r*pitch + (pitch-th)/2
        col = "url(#goldG)" if r == gold_row else weft_cols[r % len(weft_cols)]
        o.append(f'<rect x="0" y="{f(y)}" width="{W}" height="{f(th)}" rx="{f(th/2)}" fill="{col}"/>')
        o.append(f'<rect x="0" y="{f(y)}" width="{W}" height="{f(th)}" fill="url(#weftShade)"/>')
        for c in range(cols):
            if (r + c) % 2 == 0:  # warp crosses over the weft here
                x = c*pitch + (pitch-th)/2
                o.append(f'<rect x="{f(x)}" y="{f(y-1.5)}" width="{f(th)}" height="{f(th+3)}" rx="2" fill="url(#warp)"/>')
    return "\n".join(o)

def build_weave():
    W, H, P = 840, 132, 12
    rows = H//P
    gold = 2
    fabric = weave(W, H, rows, gold_row=gold, pitch=P)
    gy = gold*P + P/2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">Woven in Ahmedabad — the Manchester of the East</title>
<style>{FONT_CSS}.m{{font-family:{MONO}}}</style>
<defs>
  <linearGradient id="warp" x1="0" x2="1"><stop offset="0" stop-color="#0E131B"/><stop offset=".5" stop-color="#2A3443"/><stop offset="1" stop-color="#0E131B"/></linearGradient>
  <linearGradient id="weftShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset=".45" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></linearGradient>
  <linearGradient id="goldG" x1="0" x2="1"><stop offset="0" stop-color="#8A6A14"/><stop offset=".5" stop-color="#E9B949"/><stop offset="1" stop-color="#8A6A14"/></linearGradient>
  <linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="glint" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="mx"><rect width="{W}" height="{H}" fill="url(#fadeX)"/></mask>
  <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g mask="url(#mx)" opacity=".9">{fabric}
    <rect x="-200" y="0" width="160" height="{H}" fill="url(#glint)">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="{W+240} 0" dur="7s" repeatCount="indefinite"/>
    </rect>
    <g>
      <ellipse cx="0" cy="{f(gy)}" rx="16" ry="4.2" fill="#F6D27A"/>
      <ellipse cx="0" cy="{f(gy)}" rx="30" ry="7" fill="#F6D27A" opacity=".25"/>
      <animateTransform attributeName="transform" type="translate" values="-40 0;{W+40} 0;{W+40} 0" keyTimes="0;.7;1" dur="6s" repeatCount="indefinite"/>
    </g>
  </g>
  <rect x="{W/2-232}" y="{H/2-17}" width="464" height="34" rx="17" fill="{BG}" stroke="#2A3443"/>
  <text x="{W/2}" y="{H/2+4}" class="m" font-size="11" font-weight="700" fill="#E9B949" text-anchor="middle" letter-spacing="2.6">WOVEN IN AHMEDABAD<tspan fill="{DIM}" font-weight="400"> · THE MANCHESTER OF THE EAST</tspan></text>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/>
</svg>'''
    (OUT/"weave.svg").write_text(svg)

    # thin divider: two rows of weave, gold shuttle passes
    W2, H2, P2 = 840, 14, 7
    fab = weave(W2, H2, 2, gold_row=1, pitch=P2)
    svg2 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}" width="{W2}" height="{H2}" role="img" aria-label="woven divider">
<defs>
  <linearGradient id="warp" x1="0" x2="1"><stop offset="0" stop-color="#0E131B"/><stop offset=".5" stop-color="#2A3443"/><stop offset="1" stop-color="#0E131B"/></linearGradient>
  <linearGradient id="weftShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".5"/><stop offset=".45" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>
  <linearGradient id="goldG" x1="0" x2="1"><stop offset="0" stop-color="#8A6A14"/><stop offset=".5" stop-color="#E9B949"/><stop offset="1" stop-color="#8A6A14"/></linearGradient>
  <linearGradient id="fadeX" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff"/><stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="mx"><rect width="{W2}" height="{H2}" fill="url(#fadeX)"/></mask>
</defs>
<g mask="url(#mx)">{fab}
  <ellipse cx="0" cy="{P2*1.5}" rx="10" ry="2.4" fill="#F6D27A"><animateTransform attributeName="transform" type="translate" values="-20 0;{W2+20} 0;{W2+20} 0" keyTimes="0;.6;1" dur="5s" repeatCount="indefinite"/></ellipse>
</g>
</svg>'''
    (OUT/"thread.svg").write_text(svg2)

if __name__ == "__main__":
    flag, note = build_scan()
    build_atlas()
    build_weave()
    for p in sorted(OUT.glob("*.svg")):
        print(p.name, p.stat().st_size)
    print("FLAG", flag, "NOTE", note)
