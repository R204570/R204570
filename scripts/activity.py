#!/usr/bin/env python3
"""
activity.py: draws the profile's live activity panel from the GitHub contribution calendar.

One blue bar per day for the last 52 weeks (weekly bars on a phone), the real totals, and the
latest public events. Standard library only, so the Action needs no installs; type comes from the
committed font subsets in scripts/fonts.

  python scripts/activity.py --user R204570      # live: GraphQL with GITHUB_TOKEN, else the public calendar page
  python scripts/activity.py --demo              # offline preview from synthetic data
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
from console import (BLUE, BLUE_HI, BLUE_LO, MONO, MUTED, SANS, SEAM, TEXT, Canvas, fit, measure, n)  # noqa: E402

DAYS = 364
WIDE, NARROW = 830, 360
UA = {"User-Agent": "r204570-activity"}
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


def events(user: str, token: str | None) -> list[tuple[dt.date, str, str]]:
    """Latest public events as (date, icon, sentence). Branch creation is noise and is skipped."""
    try:
        raw = json.loads(_get(f"https://api.github.com/users/{user}/events/public?per_page=40", token))
    except Exception as e:  # the list is garnish; the chart must still draw
        print(f"events unavailable: {e}", file=sys.stderr)
        return []
    out, seen = [], set()
    for ev in raw:
        full = ev["repo"]["name"]
        repo = full.split("/", 1)[1] if full.lower().startswith(user.lower() + "/") else full
        p, kind = ev.get("payload", {}), ev["type"]
        if kind == "PushEvent":
            k = p.get("size") or p.get("distinct_size")
            item = ("commit", f"Pushed {k} commit{'s' if k != 1 else ''} to {repo}" if k else f"Pushed to {repo}")
        elif kind == "PullRequestEvent":  # one line per pull request, its latest meaningful state
            if p.get("action") not in ("opened", "closed", "reopened", "merged"):
                continue
            num = p.get("number") or p.get("pull_request", {}).get("number")
            if (repo, num) in seen:
                continue
            seen.add((repo, num))
            # the API now reports merges as their own action; older payloads carry a merged flag on close
            merged = p["action"] == "merged" or (p["action"] == "closed" and p.get("pull_request", {}).get("merged"))
            item = ("merge", f"{'Merged' if merged else p['action'].capitalize()} PR #{num} in {repo}")
        elif kind == "IssuesEvent":
            item = ("dot", f"{p.get('action', 'Updated').capitalize()} issue #{p.get('issue', {}).get('number')} in {repo}")
        elif kind == "ReleaseEvent":
            item = ("dot", f"Released {p.get('release', {}).get('tag_name', '')} of {repo}")
        elif kind == "CreateEvent" and p.get("ref_type") in ("repository", "tag"):
            item = ("dot", f"Created {repo}" if p.get("ref_type") == "repository" else f"Tagged {p.get('ref')} in {repo}")
        elif kind == "PullRequestReviewEvent":
            item = ("merge", f"Reviewed PR #{p.get('pull_request', {}).get('number')} in {repo}")
        elif kind == "WatchEvent":
            item = ("dot", f"Starred {repo}")
        else:
            continue
        if item[1] in seen:
            continue
        seen.add(item[1])
        out.append((dt.date.fromisoformat(ev["created_at"][:10]), *item))
        if len(out) == 3:
            break
    return sorted(out, key=lambda e: e[0], reverse=True)


def demo() -> tuple[list[tuple[dt.date, int]], list[tuple[dt.date, str, str]]]:
    rng = random.Random(204570)
    today = dt.date.today()
    series = []
    for i in range(DAYS):
        d = today - dt.timedelta(days=DAYS - 1 - i)
        wave = .5 + .5 * math.sin(i / 23)
        series.append((d, 0 if rng.random() > .25 + .6 * wave else int(rng.expovariate(.25) * (.4 + wave))))
    feed = [(today, "commit", "Pushed 3 commits to DocsForge"), (today - dt.timedelta(days=1), "merge", "Merged PR #20 in DocsForge"),
            (today - dt.timedelta(days=4), "dot", "Created R204570")]
    return series, feed


# ---------------------------------------------------------------- numbers
def stats(series: list[tuple[dt.date, int]]) -> dict:
    counts = [c for _, c in series]
    run = best = 0
    for c in counts:
        run = run + 1 if c else 0
        best = max(best, run)
    peak_i = max(range(len(counts)), key=counts.__getitem__)
    return dict(total=sum(counts), best=best, peak=counts[peak_i], peak_i=peak_i, peak_day=series[peak_i][0],
                active=sum(1 for c in counts if c))


def day(d: dt.date) -> str:
    return f"{d.strftime('%b')} {d.day}"


# ---------------------------------------------------------------- drawing
def render(user: str, series: list[tuple[dt.date, int]], feed: list, synced: str, narrow: bool = False) -> str:
    W = NARROW if narrow else WIDE
    pad = 16 if narrow else 24
    series = series[-DAYS:]
    counts = [c for _, c in series]
    st = stats(series)
    cv = Canvas(W, 1000)
    body_start = len(cv.parts)

    # header
    cv.text(pad, 28, "ACTIVITY", 11, MUTED, MONO, 500, tracking=1.4)
    live = f"Live · synced {synced}"
    cv.text(W - pad, 28, live, 12, TEXT, MONO, anchor="end")
    cv.pulse(W - pad - measure(live, MONO, 400, 12) - 13, 24, 3.5)
    cv.line(0.5, 44, W - 0.5, 44)

    # chart
    top, base = 74, 190
    span = base - top - 8
    if not st["total"]:
        cv.text(W / 2, (top + base) / 2, "No public activity in the last 52 weeks", 14, MUTED, anchor="middle")
    else:  # one bar per week; brightness follows volume, the busiest week is the lightest blue
        weeks = [sum(counts[i:i + 7]) for i in range(0, len(counts), 7)]
        wp = max(weeks)
        step = (W - 2 * pad) / len(weeks)
        gap = 1.6 if narrow else 4
        pk = max(range(len(weeks)), key=weeks.__getitem__)
        for i, v in enumerate(weeks):
            h = 2 if not v else 4 + (span - 4) * math.sqrt(v / wp)
            col, op = (SEAM, 1) if not v else ((BLUE_LO, 1) if i == pk else (BLUE, .45 + .55 * math.sqrt(v / wp)))
            cv.rect(pad + i * step + gap / 2, base - h, step - gap, h, col, r=1 if narrow else 2, extra=f' opacity="{op:.2f}"')
        lab = f"{weeks[pk]} that week" if narrow else f"Busiest week · {weeks[pk]} contributions"
        px = pad + pk * step + step / 2
        right = px > W / 2
        cv.text(px + (step / 2 if right else -step / 2), top - 8, lab, 11, BLUE_LO, MONO, anchor="end" if right else "start")
    cv.line(pad, base + .5, W - pad, base + .5)

    # month labels, placed from the right edge back so the latest months always get one
    step = (W - 2 * pad) / len(series)
    gap, room, last = (48 if narrow else 44), W - pad - measure("Today", MONO, 400, 10.5) - 12, 1e9
    for i in range(len(series) - 1, -1, -1):
        d, x = series[i][0], pad + i * step
        if d.day == 1 and x >= pad + 10 and x + 12 < room and last - x >= gap:
            cv.text(x, base + 20, d.strftime("%b"), 10.5, MUTED, MONO, anchor="middle")
            last = x
    cv.text(W - pad, base + 20, "Today", 10.5, MUTED, MONO, anchor="end")
    cv.line(0.5, base + 36, W - 0.5, base + 36)

    # the numbers
    cells = [("CONTRIBUTIONS", f"{st['total']:,}", "in 52 weeks"), ("LONGEST STREAK", f"{st['best']}", "days"),
             ("ACTIVE DAYS", f"{st['active']}", "of 364"), ("BUSIEST DAY", f"{st['peak']}", f"on {day(st['peak_day'])}")]
    y0 = base + 36
    if narrow:
        cw = (W - 2 * pad) / 2
        for k, (key, val, unit) in enumerate(cells):
            cx, cy = pad + (k % 2) * cw, y0 + 26 + (k // 2) * 58
            cv.text(cx, cy, key, 10, MUTED, MONO, 500, tracking=1)
            cv.text(cx, cy + 27, val, 21, TEXT, SANS, 600)
            cv.text(cx + measure(val, SANS, 600, 21) + 6, cy + 27, unit, 12.5, MUTED)
        cv.line(pad + cw - 8, y0 + 12, pad + cw - 8, y0 + 120)
        y = y0 + 132
    else:
        cw = (W - 2 * pad) / 4
        for k, (key, val, unit) in enumerate(cells):
            cx = pad + k * cw
            if k:
                cv.line(cx - 12, y0 + 12, cx - 12, y0 + 66)
            cv.text(cx, y0 + 30, key, 10.5, MUTED, MONO, 500, tracking=1)
            cv.text(cx, y0 + 58, val, 22, TEXT, SANS, 600)
            cv.text(cx + measure(val, SANS, 600, 22) + 7, y0 + 58, unit, 13, MUTED)
        y = y0 + 80
    cv.line(0.5, y, W - 0.5, y)

    # latest public activity
    y += 28
    cv.text(pad, y, "LATEST", 11, MUTED, MONO, 500, tracking=1.4)
    y += 12
    if not feed:
        y += 22
        cv.text(pad, y, "No public events this week.", 13.5, MUTED)
        y += 14
    for d, icon, s in feed:
        y += 30
        date = day(d)
        dw = measure(date, MONO, 400, 12)
        cv.icon(icon, pad, y - 13, 16, BLUE_HI)
        cv.text(pad + 26, y, fit(s, SANS, 400, 14, W - 2 * pad - 26 - dw - 16), 14, TEXT)
        cv.text(W - pad, y, date, 12, MUTED, MONO, anchor="end")
    y += 22
    cv.line(0.5, y, W - 0.5, y)

    # status bar
    y += 24
    if narrow:
        cv.text(pad, y, "Redrawn twice a day by GitHub Actions", 11, MUTED, MONO)
    else:
        cv.text(pad, y, "r204570 · Ahmedabad, IN · UTC+5:30", 11.5, MUTED, MONO)
        cv.text(W - pad, y, "Redrawn twice a day by GitHub Actions", 11.5, MUTED, MONO, anchor="end")
    H = y + 18

    cv.h = H
    body = cv.parts[body_start:]
    cv.parts = []
    cv.panel()
    cv.parts += body
    feed_txt = "; ".join(f"{day(d)}: {s}" for d, _, s in feed)
    desc = (f"{st['total']} contributions in the last 52 weeks; longest streak {st['best']} days; {st['active']} active days; "
            f"busiest day {day(st['peak_day'])} with {st['peak']}. Latest: {feed_txt or 'none'}. Synced {synced}.")
    return cv.svg(f"Activity: {user}, last 52 weeks", desc)


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
    (out / "activity.svg").write_text(render(a.user, series, feed, synced), encoding="utf-8")
    (out / "activity-narrow.svg").write_text(render(a.user, series, feed, synced, narrow=True), encoding="utf-8")
    s = stats(series[-DAYS:])
    print(f"activity: {s['total']} contributions, longest streak {s['best']}d, busiest {s['peak']}, {len(feed)} events")


if __name__ == "__main__":
    main()
