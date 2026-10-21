#!/usr/bin/env python3
"""
vitals.py — draws an ICU-style heart monitor from your GitHub contribution calendar.

Every day of the last 30 is one heartbeat; the R-spike height is that day's contributions.
Zero-commit days flatline. Pure standard library, so the Action needs no installs.

  python scripts/vitals.py --user R204570 --out assets/vitals.svg      # live (needs GITHUB_TOKEN)
  python scripts/vitals.py --demo --out assets/vitals.svg              # offline preview
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import math
import os
import random
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}"""

BG, LINE, DIM, FAINT, TXT = "#07090D", "#1A2130", "#7D8899", "#3A4352", "#E8ECF1"
GREEN, YELLOW, RED, ORANGE = "#2BD47A", "#FFD23F", "#FF4D5E", "#FF8A3D"
MONO = "'JBM','JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


# ---------------------------------------------------------------- data
def fetch(user: str, days: int, token: str) -> list[tuple[dt.date, int]]:
    now = dt.datetime.now(dt.timezone.utc)
    body = json.dumps({"query": QUERY, "variables": {
        "login": user,
        "from": (now - dt.timedelta(days=days + 7)).strftime("%Y-%m-%dT00:00:00Z"),
        "to": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "vitals.py"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    out = [(dt.date.fromisoformat(d["date"]), d["contributionCount"]) for w in weeks for d in w["contributionDays"]]
    out.sort()
    return out[-days:]


def demo(days: int) -> list[tuple[dt.date, int]]:
    rng = random.Random(204570)
    today = dt.date.today()
    out = []
    for i in range(days):
        d = today - dt.timedelta(days=days - 1 - i)
        base = rng.choice([0, 0, 1, 2, 3, 4, 6, 8, 11, 14, 19])
        out.append((d, base if d.weekday() != 6 or rng.random() < .4 else 0))
    return out


# ---------------------------------------------------------------- stats
def stats(series: list[tuple[dt.date, int]]) -> dict:
    counts = [c for _, c in series]
    total = sum(counts)
    active = sum(1 for c in counts if c)
    streak = 0
    for i, c in enumerate(reversed(counts)):
        if c:
            streak += 1
        elif i == 0:  # today not committed yet: don't break the streak
            continue
        else:
            break
    peak_i = max(range(len(counts)), key=counts.__getitem__) if counts else 0
    last7 = sum(counts[-7:])
    mean = total / max(len(counts), 1)
    last3 = sum(counts[-3:]) / 3
    ratio = active / max(len(counts), 1)
    if total == 0 or last7 == 0:
        rhythm, col = "ASYSTOLE · SEND COFFEE", RED
    elif last3 >= max(3 * mean, 5) and sum(counts[-3:]) >= 15:
        rhythm, col = "TACHYCARDIA · HACKATHON?", ORANGE
    elif ratio >= .6:
        rhythm, col = "SINUS RHYTHM · SHIPPING", GREEN
    elif ratio >= .3:
        rhythm, col = "STABLE · BUILDING", YELLOW
    else:
        rhythm, col = "BRADYCARDIA · DEEP WORK", YELLOW
    return dict(total=total, active=active, ratio=ratio, streak=streak,
                peak=counts[peak_i] if counts else 0, peak_day=series[peak_i][0] if series else None,
                rhythm=rhythm, rhythm_col=col)


# ---------------------------------------------------------------- drawing
def fmt(x: float) -> str:
    return f"{x:.1f}".rstrip("0").rstrip(".")


def ecg_path(counts: list[int], x0: float, base: float, step: float, max_amp: float) -> str:
    peak = max(counts) or 1
    rng = random.Random(7)
    d = [f"M{fmt(x0)},{fmt(base)}"]
    for i, c in enumerate(counts):
        x = x0 + i * step
        u = step / 20  # beat geometry is drawn on a 20-unit grid
        if c == 0:  # flat day: tiny noise, no beat
            for k in (5, 10, 15, 20):
                d.append(f"L{fmt(x + k*u)},{fmt(base + rng.uniform(-.6, .6))}")
            continue
        a = 10 + (max_amp - 10) * math.sqrt(c / peak)
        p, q, s, t = 3.2, 2 + .05*a, 3 + .12*a, min(4 + .09*a, 11)
        d += [f"L{fmt(x + 2.5*u)},{fmt(base)}",
              f"Q{fmt(x + 4.2*u)},{fmt(base - 2*p)} {fmt(x + 6*u)},{fmt(base)}",
              f"L{fmt(x + 7.6*u)},{fmt(base + q)}",
              f"L{fmt(x + 9.6*u)},{fmt(base - a)}",
              f"L{fmt(x + 11.6*u)},{fmt(base + s)}",
              f"L{fmt(x + 13*u)},{fmt(base)}",
              f"Q{fmt(x + 15.6*u)},{fmt(base - 2*t)} {fmt(x + 18.2*u)},{fmt(base)}",
              f"L{fmt(x + 20*u)},{fmt(base)}"]
    return "".join(d)


def font_css() -> str:
    css = []
    for w in (400, 700):
        p = HERE / "fonts" / f"jbm-{w}.woff"
        if p.exists():
            b = base64.b64encode(p.read_bytes()).decode()
            css.append(f"@font-face{{font-family:'JBM';font-weight:{w};src:url(data:font/woff;base64,{b}) format('woff')}}")
    return "".join(css)


def render(user: str, series: list[tuple[dt.date, int]], live: bool) -> str:
    W, H = 840, 240
    X0, X1, TOP, BOT = 20, 612, 52, 204
    base = 158
    counts = [c for _, c in series]
    n = max(len(counts), 1)
    step = (X1 - X0) / n
    st = stats(series)
    trace = ecg_path(counts, X0, base, step, max_amp=96)

    minor = "".join(f'<line x1="{fmt(x)}" x2="{fmt(x)}" y1="{TOP}" y2="{BOT}"/>' for x in range(X0, X1 + 1, 8)) + \
            "".join(f'<line y1="{y}" y2="{y}" x1="{X0}" x2="{X1}"/>' for y in range(TOP, BOT + 1, 8))
    major = "".join(f'<line x1="{fmt(x)}" x2="{fmt(x)}" y1="{TOP}" y2="{BOT}"/>' for x in range(X0, X1 + 1, 40)) + \
            "".join(f'<line y1="{y}" y2="{y}" x1="{X0}" x2="{X1}"/>' for y in range(TOP, BOT + 1, 40))

    ticks = []
    for i in sorted({0, 7, 14, 21, n - 1}):
        if i >= n:
            continue
        d = series[i][0]
        label = "today" if i == n - 1 else d.strftime("%b %d").replace(" 0", " ")
        x = X0 + i * step + step / 2
        anchor = "end" if i == n - 1 else "start" if i == 0 else "middle"
        ticks.append(f'<line x1="{fmt(x)}" x2="{fmt(x)}" y1="{BOT}" y2="{BOT + 5}" stroke="{FAINT}"/>'
                     f'<text x="{fmt(x + (step/2 if anchor == "end" else -step/2 if anchor == "start" else 0))}" y="{BOT + 18}" font-size="9.5" fill="{DIM}" text-anchor="{anchor}">{label}</text>')

    synced = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    status = f"LIVE · SYNCED {synced}" if live else "PREVIEW · RUN THE WORKFLOW"
    dur, kt = "8s", "0;.78;1"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Commit heartbeat — {user}</title>
<desc id="d">An ECG trace of the last {n} days of GitHub contributions: {st["total"]} contributions, {st["active"]} active days, current streak {st["streak"]} days, peak {st["peak"]} in a day. Rhythm: {st["rhythm"].lower()}.</desc>
<style>{font_css()}
.m{{font-family:{MONO}}}
.blink{{animation:bl 1.2s ease-in-out infinite}}
@keyframes bl{{50%{{opacity:.15}}}}
@media (prefers-reduced-motion:reduce){{.blink{{animation:none}}}}
</style>
<defs>
  <filter id="glow" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="2.6"/></filter>
  <linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>
</defs>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{BG}" stroke="{LINE}"/>
<g class="m">
  <text x="{X0}" y="34" font-size="11" font-weight="700" fill="{GREEN}" letter-spacing="2">COMMIT HEARTBEAT<tspan fill="{DIM}" font-weight="400" letter-spacing="1"> · {user} · LAST {n} DAYS</tspan></text>
  <circle cx="{W - 20 - len(status)*6.6 - 10}" cy="30" r="3.4" fill="{GREEN if live else YELLOW}" class="blink"/>
  <text x="{W - 20}" y="34" font-size="10" fill="{DIM}" text-anchor="end" letter-spacing=".6">{status}</text>
</g>

<g stroke="#0F1D17" stroke-width=".6">{minor}</g>
<g stroke="#163328" stroke-width=".9">{major}</g>

<path d="{trace}" fill="none" stroke="{GREEN}" stroke-opacity=".22" stroke-width="1.4" stroke-linejoin="round"/>
<g>
  <path d="{trace}" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000" fill="none" stroke="{GREEN}" stroke-width="4" stroke-opacity=".55" filter="url(#glow)">
    <animate attributeName="stroke-dashoffset" values="1000;0;0" keyTimes="{kt}" dur="{dur}" repeatCount="indefinite"/>
  </path>
  <path d="{trace}" pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000" fill="none" stroke="#7DF5B0" stroke-width="1.7" stroke-linejoin="round">
    <animate attributeName="stroke-dashoffset" values="1000;0;0" keyTimes="{kt}" dur="{dur}" repeatCount="indefinite"/>
  </path>
  <g>
    <circle r="7" fill="{GREEN}" opacity=".35" filter="url(#glow)"/><circle r="2.6" fill="#E9FFF2"/>
    <animateMotion path="{trace}" keyPoints="0;1;1" keyTimes="{kt}" calcMode="linear" dur="{dur}" repeatCount="indefinite"/>
  </g>
</g>
<rect x="{X0}" y="{TOP}" width="14" height="{BOT-TOP}" fill="url(#fadeL)"/>
<g class="m">{"".join(ticks)}</g>

<line x1="632" x2="632" y1="52" y2="216" stroke="{LINE}"/>
<g class="m">
  <text x="650" y="64" font-size="9.5" fill="{GREEN}" font-weight="700" letter-spacing="1.5">HR</text>
  <text x="674" y="64" font-size="9" fill="{FAINT}">contributions / {n}d</text>
  <text x="648" y="112" font-size="46" font-weight="700" fill="{GREEN}">{st["total"]}</text>
  <text x="650" y="148" font-size="9" fill="{DIM}" letter-spacing="1.2">STREAK</text>
  <text x="716" y="148" font-size="9" fill="{DIM}" letter-spacing="1.2">PEAK</text>
  <text x="772" y="148" font-size="9" fill="{DIM}" letter-spacing="1.2">ACTIVE</text>
  <text x="650" y="168" font-size="16" font-weight="700" fill="{TXT}">{st["streak"]}<tspan font-size="10" fill="{DIM}" font-weight="400">d</tspan></text>
  <text x="716" y="168" font-size="16" font-weight="700" fill="{TXT}">{st["peak"]}</text>
  <text x="772" y="168" font-size="16" font-weight="700" fill="{TXT}">{round(st["ratio"]*100)}<tspan font-size="10" fill="{DIM}" font-weight="400">%</tspan></text>
  <text x="650" y="200" font-size="9" fill="{DIM}" letter-spacing="1.2">RHYTHM</text>
  <text x="650" y="216" font-size="10" font-weight="700" fill="{st["rhythm_col"]}" letter-spacing=".4">{st["rhythm"]}</text>
</g>
</svg>'''


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", default=os.environ.get("GITHUB_REPOSITORY_OWNER", "R204570"))
    ap.add_argument("--out", default="assets/vitals.svg")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--demo", action="store_true", help="draw from synthetic data, no network")
    a = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if a.demo:
        series, live = demo(a.days), False
    elif not token:
        raise SystemExit("GITHUB_TOKEN not set (use --demo for an offline preview)")
    else:
        series, live = fetch(a.user, a.days, token), True

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(a.user, series, live), encoding="utf-8")
    s = stats(series)
    print(f"wrote {out} · {s['total']} contributions · streak {s['streak']}d · {s['rhythm']}")


if __name__ == "__main__":
    main()
