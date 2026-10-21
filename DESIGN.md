---
name: R204570 Title Screen
description: Raj Patel's GitHub profile README, drawn as a cracktro title screen in one hand-drawn bitmap face over GitHub's own ground.
colors:
  signal-dark: "#FFB000"
  signal-light: "#B25E00"
  ink-dark: "#E6E2D6"
  ink-light: "#141414"
  d1-dark: "#BDB9AE"
  d1-light: "#4A4A4A"
  d2-dark: "#8C8A83"
  d2-light: "#6B6B6B"
  rear-dark: "#6E6C66"
  rear-light: "#8A8A8A"
  d3-dark: "#55534E"
  d3-light: "#A3A3A3"
  void-dark: "#0D1117"
  void-light: "#FFFFFF"
typography:
  display:
    fontFamily: "bitmap 5x7 (scripts/bitmap.py, drawn as SVG paths, no font file)"
    fontSize: "70px"
    lineHeight: "110px"
    letterSpacing: "10px"
  display-narrow:
    fontFamily: "bitmap 5x7 (scripts/bitmap.py, drawn as SVG paths, no font file)"
    fontSize: "35px"
    lineHeight: "56px"
    letterSpacing: "5px"
  headline:
    fontFamily: "bitmap 5x7 (scripts/bitmap.py, drawn as SVG paths, no font file)"
    fontSize: "28px"
    letterSpacing: "10px"
  title:
    fontFamily: "bitmap 5x7 (scripts/bitmap.py, drawn as SVG paths, no font file)"
    fontSize: "21px"
    lineHeight: "36px"
    letterSpacing: "3px"
  label:
    fontFamily: "bitmap 5x7 (scripts/bitmap.py, drawn as SVG paths, no font file)"
    fontSize: "14px"
    lineHeight: "22px"
    letterSpacing: "2px"
  label-spaced:
    fontFamily: "bitmap 5x7 (scripts/bitmap.py, drawn as SVG paths, no font file)"
    fontSize: "14px"
    letterSpacing: "4px"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI\", \"Noto Sans\", Helvetica, Arial, sans-serif"
    fontSize: "16px"
    lineHeight: 1.5
rounded:
  none: "0px"
spacing:
  cell-label: "2px"
  cell-title: "3px"
  cell-headline: "4px"
  cell-display-narrow: "5px"
  cell-display: "10px"
  leader-pitch: "8px"
  leader-gap: "16px"
  row-indent: "36px"
  row-indent-narrow: "26px"
components:
  hero:
    textColor: "{colors.ink-dark}"
    typography: "{typography.display}"
    width: "830px"
    height: "412px"
  hero-narrow:
    textColor: "{colors.ink-dark}"
    typography: "{typography.display-narrow}"
    width: "360px"
    height: "300px"
  link-prompt:
    textColor: "{colors.ink-dark}"
    typography: "{typography.label}"
    height: "24px"
  link-prompt-primary:
    textColor: "{colors.signal-dark}"
    typography: "{typography.label}"
    height: "24px"
  queue-row-front:
    textColor: "{colors.ink-dark}"
    typography: "{typography.headline}"
    width: "830px"
    height: "40px"
  queue-row-d1:
    textColor: "{colors.d1-dark}"
    typography: "{typography.headline}"
    width: "830px"
    height: "40px"
  queue-row-d2:
    textColor: "{colors.d2-dark}"
    typography: "{typography.headline}"
    width: "830px"
    height: "40px"
  queue-row-rear:
    textColor: "{colors.rear-dark}"
    typography: "{typography.headline}"
    width: "830px"
    height: "40px"
  queue-row-narrow:
    textColor: "{colors.ink-dark}"
    typography: "{typography.title}"
    width: "360px"
    height: "56px"
  section-label:
    textColor: "{colors.ink-dark}"
    typography: "{typography.label-spaced}"
    height: "20px"
  signal:
    textColor: "{colors.d2-dark}"
    typography: "{typography.label}"
    width: "830px"
  signal-narrow:
    textColor: "{colors.d2-dark}"
    typography: "{typography.label}"
    width: "360px"
  scroller:
    textColor: "{colors.d2-dark}"
    typography: "{typography.label}"
    width: "830px"
    height: "24px"
  scroller-narrow:
    textColor: "{colors.d2-dark}"
    typography: "{typography.label}"
    width: "360px"
    height: "24px"
---

# Design System: R204570 Title Screen

## Overview

**Creative North Star: "The Cracktro Title Screen"**

Raj Patel's GitHub profile is drawn as a demoscene title screen. One hand-drawn bitmap face rides its baselines over a void that is GitHub's own ground: every drawing is a transparent SVG, so the page behind it is the screen. In the dark theme the type is phosphor ivory with a faint bleed of light; in the light theme the same drawing prints in inverse video, ink on paper, with no glow. Behind the type, square dust motes drift in up to three planes, gathered into swept ribbons. In front, nothing travels except a blinking caret and, at the foot of the page, the closing greetings scroller.

Shipped work is a worked queue, and rank is depth. The front row is the brightest, the widest tracked, amber-marked and still; each row behind it steps down one brightness, tightens its tracking and lets its dotted leader drift faster, the way far layers move fastest in a parallax starfield. One signal amber is spent only where a visitor should act or where something is live. Nothing is enclosed by a rule or a box; the only filled cell behind a letter is a reversed cell, and it means failure.

The platform sets the edges. GitHub sanitises README HTML (no CSS, no JS), so every custom visual is an SVG image inside a `<picture>` that picks a theme pair and, under 600px, a dedicated 360px phone drawing set 1:1. Links inside an SVG do not work, so every link is markdown or an `<a>` around a picture. GitHub's own sans sets the markdown copy between the drawings and is never imitated inside them.

**Key Characteristics:**
- One bitmap face (5×7 on a 5×9 cell grid), drawn as merged pixel runs at 2, 3, 4, 5 and 10px cells.
- Transparent void; four text brightness steps per theme plus one dust step; one signal amber.
- Rank is depth: brightness, tracking and leader drift move together.
- Up to three dust planes: the rear plane drifts fastest, each step forward halves the rate, the type plane is still.
- No rules, no boxes, no radius, no shadows; a reversed cell means failure.
- Wide drawings at 830px, phone drawings at 360px set 1:1, switched at a 600px viewport.

## Colors

Two inverse-video ladders on a transparent void: a warm phosphor ladder for the dark theme, a neutral ink ladder for the light theme, and one amber per theme. Every value lives in `DARK` and `LIGHT` in `scripts/bitmap.py`; each step is named by depth, and contrast figures are against GitHub's ground.

### Primary
- **Signal Amber** (#FFB000 dark, 10.3:1 / #B25E00 light, 4.7:1): the single accent and the only colour that is not a depth. It marks the primary action (the `> résumé` prompt, caret and label), the front queue row (its `>` caret and status), and live markers: the masthead block, the four status bars, the hero caret, the signal's sync square, the signal's blinking now-bar and the motes of the busiest day.

### Neutral
- **Phosphor Ivory / Print Ink** (ink: #E6E2D6, 14.6:1 / #141414, 18.4:1): the front plane. The headline, masthead, status values, section-label heads, link-prompt labels, the front row's name, the signal total and the reversed failure cell.
- **Warm Ash / Graphite** (d1: #BDB9AE, 9.7:1 / #4A4A4A, 8.9:1): one step back. The hero subline, the signal's stat line(s) and the second queue row.
- **Smoke / Pencil Grey** (d2: #8C8A83, 5.5:1 / #6B6B6B, 5.3:1): two steps back, and the quietest step allowed for small text. Keys (STATUS, NOW), the ID line, label tails, non-primary prompt carets, the scroller, the signal header, month marks and feed, the third queue row, the near dust plane, the light theme's mid dust plane, and a third of the signal's motes.
- **Far Smoke / Far Grey** (rear: #6E6C66, 3.6:1 / #8A8A8A, 3.5:1): the rearmost text step, large-text contrast only. It carries the fourth queue row and nothing else.
- **Dust** (d3: #55534E, 2.5:1 / #A3A3A3, 2.5:1): never a letter. The far dust plane, the dark theme's mid plane, leader dots, quiet-day motes and the faintest signal motes.
- **GitHub Night / GitHub Paper** (void: #0D1117 / #FFFFFF): GitHub's own ground, recorded so contrast can be checked. No drawing paints it.

### Named Rules
**The One Amber Rule.** Signal amber is spent on three things only: the primary action, the front row of the queue, and live markers. A second amber element anywhere else dilutes the one place a visitor should act.

**The Transparent Void Rule.** No SVG paints a background. GitHub's ground is the screen, in both themes; the reversed failure cell is the only fill that sits behind letters.

**The Dust Is Not Ink Rule.** d3 never carries a letter. It is reserved for motes and leader dots, so anything set in it reads as atmosphere, not information.

## Typography

**Display Font:** the profile's bitmap face (hand-drawn 5×7 caps on a 5×9 cell grid, `scripts/bitmap.py`), drawn as SVG path runs; no font file and no `<text>` element.
**Body Font:** GitHub's markdown sans (-apple-system, "Segoe UI", "Noto Sans", Helvetica, Arial), set by the platform.
**Label/Mono Font:** the same bitmap face, at its smallest cell.

**Character:** one blocky, evenly weighted pixel face does every drawn job, from the 70px headline to the 14px scroller, so the hierarchy comes from cell size, brightness and tracking rather than a second family. GitHub's humanist sans carries the paragraphs between drawings and reads as the platform speaking, not the title screen.

### The cell grid
- Each glyph is 5 columns by 9 rows of square cells. Caps and ascenders use rows 0 to 6 (cap height is 7 cells), the x-height is rows 2 to 6, and descenders (g j p q y , ; _ |) drop into rows 7 and 8.
- Advance is (5 + track) cells, with a default track of 1 empty cell. Ink width is (characters × (5 + track) − track) × cell, and `start`, `middle` and `end` anchors measure that ink width, so right-aligned text ends exactly on the column edge.
- Every helper takes `y` as the top of row 0; the baseline is `y` + 7 cells. Horizontal runs of lit cells merge into one rectangle each, so the files stay small and crisp at any zoom.
- The set covers A–Z, a–z, é, 0–9, punctuation, × and a few drawn icons in the same grammar (· ★ ● ○ ▸ ↗ → ■). A missing character renders as `?`: add it to `_SPEC` (five characters per row, 7 to 9 rows) before using it.
- Sizes below are cap heights: `fontSize` is 7 × cell, and letter spacing is track × cell.

### Hierarchy
- **Display** (10px cell, 70px caps, 1-cell track, 110px baseline pitch): "i build ai / that ships" on the wide hero only. Lit cells split into three static opacity buckets (1, .95, .9 in dark; 1, .96, .92 in light) for a phosphor grain; in dark only, a copy blurred by 0.3 cell at 25% opacity bleeds light behind it. On a phone the same lines use **Display narrow** (5px cell, 35px caps, 56px pitch).
- **Headline** (4px cell, 28px caps): queue row names on the wide drawing. Tracking follows rank: 2.5, 1.75, 1 and 0.5 cells from front to rear.
- **Title** (3px cell, 21px caps, 1-cell track): the masthead "RAJ PATEL" (1.4-cell track), the wide hero subline (36px pitch), wide row statuses, row names on a phone (tracking still follows rank) and the signal total.
- **Label** (2px cell, 14px caps, 1-cell track, 20 to 22px pitch): link prompts, status values, the phone subline, phone row statuses, the scroller, the signal header, month marks, stats and feed. **Label spaced** (2-cell track) sets the uppercase keys: section labels, the ID line, STATUS and NOW.
- **Body** (GitHub sans, 16px, 1.5): row descriptions, the bold availability line, credentials, the stack lines (bold key · values) and captions in `<sub>`.

### Named Rules
**The One Face Rule.** Every drawn letter and symbol is the bitmap face, drawn as path runs. No second typeface, no `<text>`, no embedded font, and no imitation of GitHub's sans inside a drawing.

**The Two-Pixel Floor Rule.** No text cell renders below 2px. A drawing that would shrink a 2px cell on a phone gets its own 360px drawing set 1:1; drawings narrow enough to fit (link prompts up to 132px, labels up to 320px) stay at native size everywhere.

**The Lowercase Voice Rule.** Statements and values speak lowercase ("i build ai", "open to ai roles + freelance", "in production"). Uppercase belongs to the masthead name, the ID line, the keys STATUS and NOW, and section labels.

## Layout

A single column that GitHub supplies. Wide drawings are 830px, the profile README column; phone drawings are 360px. Everything starts flush at x = 0, and anything right-aligned (the hero's status block, row statuses, "today" under the signal) ends exactly on the drawing's right edge, so the column's two edges are the only alignment lines.

- **Phone switch.** A `(max-width: 600px)` viewport query selects the phone drawing. Hero, queue rows, signal and scroller have one; link prompts and section labels do not need one and wrap or sit at native size.
- **Heights hug the ink.** Link prompts are 24px tall, labels 20px, rows 40px (56px on a phone), the scroller 24px, the hero 412px (300px), the signal about 338px (340px) and growing with its feed. There are no spacer images: vertical rhythm between drawings is GitHub's own markdown flow (paragraph and h3 margins), plus one `<br>` before the scroller.
- **Inside a queue row.** The caret sits at 0, the name at 36px (26px on a phone), the leader runs from the name's end + 16px to the status's start − 16px, and the status ends on the right edge. On a phone the status drops under the name at 26px.
- **Page order as built.** Hero; link prompts on one line separated by `&emsp;` (they wrap on a phone); the bold availability line and credentials; QUEUE label and four rows, front to rear, each followed by its description and links; "Deeper in the queue" in `<sub>`; SIGNAL label, the signal and its caption; LAYERS label and the stack; the Hidden part `<details>`; the scroller.

### The picture block
Every drawing is one `<picture>` written on one line. Sources are tested in order and the first match wins, so the phone-dark source must come first:

```html
<a href="…"><picture><source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="./assets/NAME-narrow-dark.svg"><source media="(max-width: 600px)" srcset="./assets/NAME-narrow-light.svg"><source media="(prefers-color-scheme: dark)" srcset="./assets/NAME-dark.svg"><img src="./assets/NAME-light.svg" alt="…"></picture></a>
```

A drawing without a phone version drops the two narrow sources. The `<img>` is always the light wide file and carries the alt text, which says in a sentence what the drawing says. Section labels sit inside `<h3>` so the page keeps a real heading outline.

Multi-line blocks break, for three reasons:
- A line holding only an opening tag such as `<a href="…">` starts a raw-HTML block that runs to the next blank line with markdown switched off, so a queue row's `[repo](…)` links and `**contributors wanted:**` would print raw.
- Newlines and indentation inside `<a>` render as whitespace inside the link: an underlined gap beside the image.
- An indented continuation line after a blank line becomes a code block.

Written on one line, a row's picture opens a paragraph, so its `<br>`, description and markdown links render together as one block. The link prompts sit in a `<p>` block of pure HTML, one `<a>` per line, which is safe because nothing inside it needs markdown.

### Named Rules
**The Narrow Drawing Rule.** A phone never sees a wide drawing scaled down. Every drawing wider than 360px has a 360px twin set 1:1 that drops dust planes and leaders but keeps brightness steps and tracking.

**The One-Line Picture Rule.** One `<picture>` per line, sources in the order narrow-dark, narrow, dark, then the light `<img>`. No line breaks or indentation inside it.

## Elevation & Depth

There are no shadows and no elevation. Depth is planes and rank: the type plane is in front and holds still, dust planes sit behind it and drift left, and the queue's rank is expressed by how far back each row sits.

**Dust planes** (from `dust()` in `scripts/build_assets.py`; counts and durations are per 830px and scale with width, so speed in px/s is the same on a phone):
- **Near:** 2.4px motes, d2, opacity .7 dark / .6 light, 110 motes, 280s per width (about 3px/s).
- **Mid:** 1.8px motes, d3 dark / d2 light, opacity 1 / .9, 360 motes, 140s per width (about 6px/s).
- **Far:** 1.2px motes, d3, opacity .9 / .8, 1,600 motes, 70s per width (about 12px/s).

About 92% of motes sit on swept sine ribbons whose scatter widens and narrows twice per width; the rest are loose. Every term repeats over the drawing's width and a second copy sits one width to the right, so `translateX(−width)` loops without a seam. The random seed is 204570, so a rebuild is byte-stable. The phone hero keeps only the far plane.

**Rank ladder** (from `TRACK`, `LEAD_DRIFT` and `STEPS`):

| Depth | Row | Colour | Tracking | Leader drift |
|---|---|---|---|---|
| 0 (front) | docsforge | ink; caret and status amber | 2.5 cells | still |
| 1 | neuroassist | d1 | 1.75 cells | 8px per 5.4s |
| 2 | hospital ms | d2 | 1 cell | 8px per 2.7s |
| 3 (rear) | pcb inspection | rear | 0.5 cells | 8px per 1.35s |

The leaders continue the dust's speed chain: the depth-2 leader moves at the near plane's speed and the rear leader at the mid plane's, so the queue rows sit inside the same parallax field. On a phone the leaders go; brightness and tracking stay.

**Motion grammar.** Linear, infinite and transform-only for drift (`translateX`); `steps(1)` at 1.1s, off at 50%, for the caret and the signal's now-bar; the scroller travels at about 42px/s. Every animated drawing carries `@media (prefers-reduced-motion: reduce){*{animation:none!important}}`, which `bm.svg()` appends whenever a drawing has a style block.

### Named Rules
**The Rank Is Depth Rule.** Rank is shown by brightness step, tracking and leader drift together, never by one lever alone and never by size, weight or a badge. All four rows share one cell size.

**The Halving Rule.** The rear plane drifts fastest, and each step forward halves the rate, down to the front plane, which never moves. Type is that front plane: only the caret blinks, and only the closing scroller travels.

**The Inverse Video Rule.** The light theme is the same drawing in inverse video: identical geometry, counts and motion, with the ladder inverted from ink-on-night to ink-on-paper. The phosphor bleed exists only in the dark.

## Shapes

Square, filled and axis-aligned. Letters are runs of square cells; dust motes are squares (1.2, 1.8 and 2.4px in the hero; 1.4, 1.8 and 2px in the signal). The fixed marks keep to the same geometry: the hero caret is 3 × 3 cells sitting on the baseline one cell after the last glyph, the masthead block is 9px on the masthead's baseline, the signal's sync square is 8px, its now-bar 6 × 18px, the status bars 5px wide on a 7px pitch at 6, 9, 12 and 15px tall, and leader dots are 2 × 2px on an 8px pitch. There is no radius, no stroke, no outline and no circle outside the face's own drawn glyphs.

### Named Rules
**The No-Enclosure Rule.** Nothing is enclosed by a rule, a border, a box or a frame. A dotted leader connects a name to its status and stops 16px short of both; it never spans the column or underlines a heading. The signal draws no axis or baseline: quiet days settle as loose motes.

**The Square Mark Rule.** Every mark is a filled, axis-aligned square or rectangle. A new mark is built from cells, not drawn as a stroke or a curve.

## Components

Every component is generated by Python into `assets/` as a `-dark` / `-light` pair, plus `-narrow-dark` / `-narrow-light` where the Narrow Drawing Rule applies. Each file is a transparent SVG with `role="img"`, a `<title>`, and a `<desc>` where the drawing says more than its alt text.

### Hero (title screen)
The first viewport: who, what, status, in the face at its largest.
- **Wide (830 × 412):** masthead "RAJ PATEL" (title cells, 1.4-cell track, ink) at top left with the 9px amber block on its baseline; ID line "R204570 · AHMEDABAD, IN" below it (label spaced, d2). Top right, right-aligned: key STATUS (d2), the four amber status bars, "open to ai roles + freelance" (ink), key NOW (d2), "shipping docsforge" (ink). Then "i build ai" and "that ships" in display cells with the amber 3 × 3-cell caret blinking after "ships", and a two-line subline in title cells (d1). Three dust planes fill the band from 70px to the foot.
- **Phone (360 × 300):** the same masthead and ID line; the status bars move to the left with "open to roles + freelance" (ink) and "now shipping docsforge" (d2) beside them; the headline in display-narrow cells with its caret; the subline in three label lines (d1). Far dust plane only.
- **Link:** the whole hero links to the portfolio.
- **Hidden part:** the dark wide hero carries the hidden part's second layer as an XML comment, generated from `NOTE` in `scripts/build_assets.py`. Leave it to the script.

### Link prompt
A command-line prompt per destination, at native label size on every screen.
- **Anatomy:** `>` caret, one space, lowercase label; 24px tall, width to the ink (84 to 132px).
- **Default:** caret d2, label ink.
- **Primary:** caret and label signal amber. Only `> résumé` is primary.
- **States:** none of its own. GitHub gives images inside links no hover style; the link is the `<a>` around the picture.

### Queue row
One row per shipped project, ranked by depth (see the rank ladder).
- **Wide (830 × 40):** caret `>` (headline cells; amber on the front row, otherwise the row's step), name in headline cells at 36px with the rank's tracking, a d3 dotted leader clipped between name and status, and the status right-aligned in title cells with its baseline on the name's baseline (amber on the front row).
- **Phone (360 × 56):** caret and name in title cells at 26px with the rank's tracking; status in label cells under the name. No leader.
- **Below it, in markdown:** one description paragraph in GitHub sans, then links separated by " · ". The picture links to the repository.

### Section label
The heading of each section, set like a demo's part title.
- **Anatomy:** uppercase head in ink, two blank glyphs of air (32px), then "· TAIL" in d2; label-spaced cells; 20px tall, 264 to 320px wide.
- **Markup:** inside `<h3>`, alt text "Head: tail" ("Queue: shipped work").

### Signal
The live contribution graph, drawn as dust instead of a calendar grid.
- **Header:** 8px amber sync square, then in d2 label cells "synced oct 21 · r204570 · last 52 weeks" (phone: "52 weeks · synced oct 21").
- **Field:** 364 days, one column each across the width. A day with contributions throws 3 + 4√count motes around the centre line, scattering wider as the day gets busier relative to the peak; motes fall in d3 (55%, 1.8px), d2 (33%, 2px) or ink (12%, 2px), and the busiest day's motes are all amber. A quiet day leaves at most one loose 1.4px d3 mote at half opacity. The centre line sits at 92px with a 66px reach (phone: 74px, 46px). The amber now-bar blinks at the right edge.
- **Months:** lowercase month marks in d2 at the first of each month, at least 40px apart (46px on a phone, which shows every other month) and stopping short of "today", which is right-aligned.
- **Numbers:** the total in title cells (ink), then the longest run, the busiest day and active days in label cells (d1), on one line joined by " · " on wide and one per line on a phone; then the three latest public events in d2, with a date column on wide and none on a phone, trimmed with ".." to fit.
- **Markup:** linked to `.github/workflows/signal.yml`, with a one-sentence caption in `<sub>` below.

### Failure: NO SIGNAL
The one reversed cell in the system. When the 52-week total is zero, the field is replaced by "NO SIGNAL" (6px cells wide, 4px on a phone, 2-cell track) knocked out of an ink block that extends two cells past the letters on every side, so the letters show the void through the ink. The total line reads "no public contributions in 52 weeks" and there is no now-bar. A failed fetch is not drawn: the script exits with an error and the last good drawing stays in place.

### Scroller
The closing greetings line of a cracktro, and the only type that travels.
- **Anatomy:** the greetings text in d2 label cells, two copies end to end with a six-cell gap, translating left at about 42px/s (one 3,550px loop in 85s); 24px tall.
- **Wide and phone:** the same loop in an 830px or 360px window.

### Markdown copy
GitHub's sans carries everything that is read rather than seen: the bold availability line, credentials joined by " · ", row descriptions and links, "Deeper in the queue" in `<sub>`, the stack as bold keys followed by " · " and values, and the Hidden part `<details>`. It is plain first-person text with numbers; no emoji, no badges.

### Regenerating
- `python3 scripts/build_assets.py` writes the hero, link prompts, rows, labels and scroller: 42 files into `assets/` (pass a folder as the first argument to write elsewhere).
- `python3 scripts/signal.py --user R204570` writes the four signal files from the live calendar (GraphQL with `GITHUB_TOKEN`, otherwise the public calendar page). `--demo` draws synthetic data offline, and writes into `assets/` unless `--out-dir` points elsewhere.
- Palette, glyph and helper changes go in `scripts/bitmap.py`; run both scripts afterwards. Standard library only.
- `.github/workflows/signal.yml` redraws the signal at 06:41 and 18:41 UTC, on manual dispatch, and on pushes that touch `signal.py`, `bitmap.py` or the workflow, and commits only when the drawing changed. Its commit step stages `assets/signal-*.svg`, so the wide and phone drawings move together; any new signal variant must match that glob.

## Do's and Don'ts

### Do:
- **Do** spend signal amber only on the `> résumé` prompt, the front queue row's caret and status, and live markers (masthead block, status bars, hero caret, signal sync square, signal now-bar, busiest-day motes).
- **Do** give every drawing wider than 360px a 360px `-narrow` twin set 1:1, so every drawing ships as four files: `-dark`, `-light`, `-narrow-dark`, `-narrow-light`.
- **Do** write each `<picture>` on one line, with sources in the order narrow-dark, narrow, dark, then the light `<img>` carrying the alt text.
- **Do** show rank with all three levers at once: brightness step (ink, d1, d2, rear), tracking (2.5, 1.75, 1, 0.5 cells) and leader drift (still, 5.4s, 2.7s, 1.35s per 8px).
- **Do** keep dust behind type in at most three planes, rear fastest and halving at each step forward; phone drawings keep the far plane only.
- **Do** draw every letter and symbol in the bitmap face at a 2px cell or larger, adding missing glyphs to `_SPEC` in its 5-wide grammar.
- **Do** keep every SVG transparent, with `role="img"`, a title, and the reduced-motion guard on anything that moves.
- **Do** put links on the `<a>` around a picture or in markdown beside it.
- **Do** regenerate instead of hand-editing: `python3 scripts/build_assets.py` and `python3 scripts/signal.py`.
- **Do** mark failure with a reversed glyph cell, and use a reversed cell for nothing else.

### Don't:
- **Don't** enclose anything in a rule, border, box, frame or card, and don't separate sections with `<hr>` or `---`; leaders stop 16px short of the name and the status.
- **Don't** paint a background into any SVG; GitHub's ground is the void in both themes.
- **Don't** set a letter in d3, or anything except the rearmost queue row in rear.
- **Don't** let a phone scale a wide drawing down, or let any text cell render below 2px.
- **Don't** add a second typeface, a `<text>` element or an embedded font to a drawing, and don't imitate GitHub's sans inside one.
- **Don't** move type: no drifting, bouncing or fading letters, and no leader on the front row. The caret blinks and the closing scroller travels; nothing else in the type plane moves.
- **Don't** add glow, blur or shadow beyond the dark hero headline's phosphor bleed; the light theme has none.
- **Don't** round a corner or draw a stroke or a curve; marks are filled squares and rectangles.
- **Don't** add third-party stats cards, badges, shields or emoji; the signal is the only data graphic, and it is drawn in dust.
- **Don't** put a link inside an SVG; GitHub drops it.
- **Don't** edit, move, reformat or print the hidden part's layers: the README's second HTML comment and the dark hero's XML comment generated from `NOTE`.
