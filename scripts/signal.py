#!/usr/bin/env python3
"""
signal.py: draws the profile's live signal from the GitHub contribution calendar.

Every day of the last 52 weeks is one column of dust; the busier the day, the more motes and
the wider they scatter, so the year reads as a drifting wave. Below it: one sentence of real
totals and the three latest public events. Standard library only, so the Action needs no installs.

  python scripts/signal.py --user R204570               # live: GraphQL with GITHUB_TOKEN, else the public calendar page
  python scripts/signal.py --demo                       # offline preview from synthetic data
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bitmap as bm  # noqa: E402
from bitmap import n  # noqa: E402

DAYS = 364
W, H = 830, 340
UA = {"User-Agent": "r204570-signal"}
QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar { weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


# ---------------------------------------------------------------- data
def _get(url: str, token: str | None, data: bytes | None = None) -> bytes:
    headers = dict(UA)
    if token:
        headers["Authorization"] = f"bearer {token}"
    if data:
        headers["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=30) as r:
        return r.read()


def calendar_graphql(user: str, token: str) -> list[tuple[dt.date, int]]:
    now = dt.datetime.now(dt.timezone.utc)
    body = json.dumps({"query": QUERY, "variables": {
        "login": user,
        "from": (now - dt.timedelta(days=DAYS + 7)).strftime("%Y-%m-%dT00:00:00Z"),
        "to": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }}).encode()
    payload = json.loads(_get("https://api.github.com/graphql", token, body))
    if payload.get("errors"):
        raise RuntimeError(f"GraphQL: {payload['errors']}")
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return sorted((dt.date.fromisoformat(d["date"]), d["contributionCount"]) for w in weeks for d in w["contributionDays"])


def calendar_page(user: str) -> list[tuple[dt.date, int]]:
    """The public calendar fragment github.com renders on profiles; no token needed."""
    html = _get(f"https://github.com/users/{user}/contributions", None).decode("utf-8", "replace")
    by_id = {}
    for cell in re.findall(r"<td[^>]*data-date=[^>]*>", html):
        d, i = re.search(r'data-date="([\d-]+)"', cell), re.search(r'\bid="([^"]+)"', cell)
        if d and i:
            by_id[i.group(1)] = d.group(1)
    out = {}
    for tid, label in re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        if tid in by_id:
            m = re.match(r"\s*(\d+|No) contribution", label)
            out[dt.date.fromisoformat(by_id[tid])] = 0 if not m or m.group(1) == "No" else int(m.group(1))
    if not out:
        raise RuntimeError("calendar page had no readable days")
    return sorted(out.items())


def events(user: str, token: str | None) -> list[tuple[dt.date, str]]:
    try:
        raw = json.loads(_get(f"https://api.github.com/users/{user}/events/public?per_page=40", token))
    except Exception as e:  # the feed is garnish; the graph must still draw
        print(f"events unavailable: {e}", file=sys.stderr)
        return []
    out, seen = [], set()
    for ev in raw:
        repo = ev["repo"]["name"].split("/", 1)[-1].lower() if ev["repo"]["name"].lower().startswith(user.lower() + "/") else ev["repo"]["name"].lower()
        p, kind = ev.get("payload", {}), ev["type"]
        if kind == "PushEvent":
            k = p.get("size") or p.get("distinct_size")
            s = f"pushed {k} commit{'s' if k != 1 else ''} to {repo}" if k else f"pushed to {repo}"
        elif kind == "PullRequestEvent":
            num = p.get("number") or p.get("pull_request", {}).get("number")
            merged = p.get("pull_request", {}).get("merged")
            verb = "merged" if p.get("action") == "closed" and merged else p.get("action", "updated")
            s = f"{verb} pr #{num} in {repo}"
        elif kind == "CreateEvent":  # branches are noise; repositories and tags are news
            ref_type = p.get("ref_type")
            if ref_type == "repository":
                s = f"created {repo}"
            elif ref_type == "tag":
                s = f"tagged {p.get('ref')} in {repo}"
            else:
                continue
        elif kind == "ReleaseEvent":
            s = f"released {p.get('release', {}).get('tag_name', '')} of {repo}"
        elif kind == "IssuesEvent":
            s = f"{p.get('action', 'updated')} issue #{p.get('issue', {}).get('number')} in {repo}"
        elif kind == "PullRequestReviewEvent":
            s = f"reviewed pr #{p.get('pull_request', {}).get('number')} in {repo}"
        elif kind == "WatchEvent":
            s = f"starred {repo}"
        elif kind == "ForkEvent":
            s = f"forked {repo}"
        else:
            continue
        s = s.lower()
        if s in seen:
            continue
        seen.add(s)
        out.append((dt.date.fromisoformat(ev["created_at"][:10]), s))
        if len(out) == 3:
            break
    return sorted(out, key=lambda e: e[0], reverse=True)


def demo() -> tuple[list[tuple[dt.date, int]], list[tuple[dt.date, str]]]:
    rng = random.Random(204570)
    today = dt.date.today()
    series = []
    for i in range(DAYS):
        d = today - dt.timedelta(days=DAYS - 1 - i)
        wave = .5 + .5 * math.sin(i / 23)
        series.append((d, 0 if rng.random() > .25 + .6 * wave else int(rng.expovariate(.25) * (.4 + wave))))
    feed = [(today, "pushed 3 commits to docsforge"), (today - dt.timedelta(days=1), "merged pr #20 in docsforge"),
            (today - dt.timedelta(days=4), "created r204570")]
    return series, feed


# ---------------------------------------------------------------- numbers
def stats(series: list[tuple[dt.date, int]]) -> dict:
    counts = [c for _, c in series]
    run = best = 0
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    peak_i = max(range(len(counts)), key=counts.__getitem__)
    return dict(total=sum(counts), best=best, peak=counts[peak_i], peak_day=series[peak_i][0],
                active=sum(1 for c in counts if c))


def day(d: dt.date) -> str:
    return f"{d.strftime('%b').lower()} {d.day}"


# ---------------------------------------------------------------- drawing
def render(theme: dict, user: str, series: list[tuple[dt.date, int]], feed: list[tuple[dt.date, str]], synced: str) -> str:
    t = theme
    series = series[-DAYS:]
    counts = [c for _, c in series]
    st = stats(series)
    step = W / len(series)
    mid, reach = 92, 66  # centre line of the wave and how far a mote may stray from it
    o = []

    o.append(f'<rect class="blink" x="0" y="4" width="8" height="8" fill="{t["signal"]}"/>')
    o.append(bm.text(f"synced {synced}  ·  {user.lower()}  ·  last 52 weeks", 16, 2, 2, t["d2"]))

    if st["total"] == 0:  # flatline: say so in reversed cells
        msg, c = "NO SIGNAL", 6
        mw = bm.width(msg, c, 2)
        x0, y0 = (W - mw) / 2, mid - 4 * c
        o.append(f'<defs><mask id="rev"><rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>'
                 f'<path d="{bm.path(msg, x0, y0, c, 2)}" fill="#000"/></mask></defs>'
                 f'<rect x="{n(x0 - 2 * c)}" y="{n(y0 - 2 * c)}" width="{n(mw + 4 * c)}" height="{n(11 * c)}" fill="{t["ink"]}" mask="url(#rev)"/>')
    else:
        rng = random.Random(7)
        peak = max(counts)
        planes = {"quiet": [], "d3": [], "d2": [], "ink": [], "signal": []}
        for i, c in enumerate(counts):
            x = i * step + step / 2
            if not c:  # quiet days settle as a few loose motes, not a drawn line
                if rng.random() < .55:
                    planes["quiet"].append((x + rng.uniform(-step, step), mid + rng.gauss(0, 2.2), 1.4))
                continue
            k = 3 + round(4 * math.sqrt(c))
            spread = 5 + (reach / 2.6) * math.sqrt(c / peak)
            for _ in range(k):
                y = mid + max(-reach, min(reach, rng.gauss(0, spread)))
                plane = "signal" if c == peak else rng.choices(("d3", "d2", "ink"), (.55, .33, .12))[0]
                planes[plane].append((x + rng.gauss(0, step * 1.2), y, 1.8 if plane == "d3" else 2))
        for plane, motes in planes.items():
            if motes:
                d = "".join(f"M{n(x - s / 2)} {n(y - s / 2)}h{n(s)}v{n(s)}h{n(-s)}z" for x, y, s in motes)
                fill, op = (t["d3"], ' opacity=".5"') if plane == "quiet" else (t[plane], ' opacity=".9"' if plane == "d3" else "")
                o.append(f'<path d="{d}" fill="{fill}"{op}/>')
        o.append(f'<rect class="blink" x="{n(W - 6)}" y="{mid - 9}" width="6" height="18" fill="{t["signal"]}"/>')

    # month marks along the bottom of the field
    marks = []
    for i, (d, _) in enumerate(series):
        if d.day == 1 and 24 < i < len(series) - 24:
            marks.append(bm.text(d.strftime("%b").lower(), i * step, mid + reach + 12, 2, t["d3"], anchor="middle"))
    o.append("".join(marks))
    o.append(bm.text("today", W, mid + reach + 12, 2, t["d2"], anchor="end"))

    # one sentence of real numbers, then the feed
    y = mid + reach + 44
    if st["total"]:
        o.append(bm.text(f"{st['total']:,} contributions in 52 weeks", 0, y, 3, t["ink"]))
        o.append(bm.text(f"longest run {st['best']} days  ·  busiest day {st['peak']}, {day(st['peak_day'])}  ·  "
                         f"{st['active']} active days", 0, y + 32, 2, t["d1"]))
    else:
        o.append(bm.text("no public contributions in the last 52 weeks", 0, y, 3, t["ink"]))
    for j, (d, s) in enumerate(feed):
        fy = y + 64 + j * 22
        o.append(bm.text(day(d), 0, fy, 2, t["d3"]))
        o.append(bm.text(s, 84, fy, 2, t["d2"]))

    css = ".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    desc = (f"{st['total']} contributions in the last 52 weeks; longest run {st['best']} days; busiest day {st['peak']} on "
            f"{st['peak_day'].isoformat()}. Latest: " + "; ".join(f"{day(d)} {s}" for d, s in feed) + f". Synced {synced}.")
    return bm.svg(W, H, "".join(o), f"Signal: {user}'s contributions, last 52 weeks", desc, css)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", default=os.environ.get("GITHUB_REPOSITORY_OWNER", "R204570"))
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parent.parent / "assets"))
    ap.add_argument("--demo", action="store_true", help="synthetic data, no network")
    a = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if a.demo:
        series, feed = demo()
    else:
        try:
            series = calendar_graphql(a.user, token) if token else calendar_page(a.user)
        except Exception as e:
            if not token:
                raise
            print(f"GraphQL failed ({e}); falling back to the calendar page", file=sys.stderr)
            series = calendar_page(a.user)
        feed = events(a.user, token)

    synced = day(dt.datetime.now(dt.timezone.utc).date())
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for t in bm.THEMES:
        (out / f"signal-{t['name']}.svg").write_text(render(t, a.user, series, feed, synced), encoding="utf-8")
    s = stats(series[-DAYS:])
    print(f"signal: {s['total']} contributions · longest run {s['best']}d · busiest {s['peak']} · {len(feed)} events")


if __name__ == "__main__":
    main()
