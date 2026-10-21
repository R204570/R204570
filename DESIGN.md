---
name: R204570 Console
description: Raj Patel's GitHub profile README drawn as a formal developer console in blue and black, with film grain, one accent and one breathing dot.
colors:
  ground: "#0D1117"
  panel: "#121821"
  lift: "#18202B"
  seam: "#232C38"
  text: "#E6EDF3"
  soft: "#C3CDD8"
  muted: "#8B949E"
  blue: "#1F6FEB"
  blue-hi: "#58A6FF"
  blue-lo: "#79C0FF"
  white: "#FFFFFF"
  label-light: "#59636E"
typography:
  display:
    fontFamily: "Geist, sans-serif"
    fontSize: "66px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-2px"
  display-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "46px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-1.4px"
  stat:
    fontFamily: "Geist, sans-serif"
    fontSize: "22px"
    fontWeight: 600
    lineHeight: 1
  lede:
    fontFamily: "Geist, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: "26px"
  lede-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "15.5px"
    fontWeight: 400
    lineHeight: "22px"
  body:
    fontFamily: "Geist, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: "22px"
  body-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "20px"
  title:
    fontFamily: "Geist, sans-serif"
    fontSize: "14px"
    fontWeight: 500
  value:
    fontFamily: "Geist, sans-serif"
    fontSize: "14px"
    fontWeight: 400
  unit:
    fontFamily: "Geist, sans-serif"
    fontSize: "13px"
    fontWeight: 400
  repo:
    fontFamily: "Geist Mono, monospace"
    fontSize: "16px"
    fontWeight: 500
  command:
    fontFamily: "Geist Mono, monospace"
    fontSize: "13px"
    fontWeight: 400
  data:
    fontFamily: "Geist Mono, monospace"
    fontSize: "12.5px"
    fontWeight: 400
  data-small:
    fontFamily: "Geist Mono, monospace"
    fontSize: "11px"
    fontWeight: 400
  tag:
    fontFamily: "Geist Mono, monospace"
    fontSize: "11.5px"
    fontWeight: 500
  label:
    fontFamily: "Geist Mono, monospace"
    fontSize: "11px"
    fontWeight: 500
    letterSpacing: "1.4px"
  key:
    fontFamily: "Geist Mono, monospace"
    fontSize: "10.5px"
    fontWeight: 500
    letterSpacing: "1px"
  section-label:
    fontFamily: "Geist Mono, monospace"
    fontSize: "12px"
    fontWeight: 500
    letterSpacing: "1.6px"
rounded:
  bar: "2px"
  box: "8px"
  panel: "12px"
  pill: "12px"
spacing:
  icon-gap: "8px"
  stage-gap: "14px"
  gutter-narrow: "16px"
  grid: "22px"
  row-narrow: "22px"
  gutter: "24px"
  row: "24px"
  inset: "32px"
components:
  hero:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.display}"
    rounded: "{rounded.panel}"
    width: "830px"
    height: "550px"
  hero-narrow:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.display-narrow}"
    rounded: "{rounded.panel}"
    width: "360px"
    height: "870px"
  now-shipping:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    typography: "{typography.command}"
    rounded: "{rounded.box}"
    width: "456px"
    height: "56px"
  now-shipping-narrow:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.box}"
    width: "328px"
    height: "56px"
  live-strip:
    textColor: "{colors.blue}"
    typography: "{typography.label}"
    width: "456px"
    height: "64px"
  pipeline-stage:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    typography: "{typography.title}"
    rounded: "{rounded.box}"
    padding: "12px"
    width: "116px"
    height: "96px"
  button-primary:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.white}"
    typography: "{typography.title}"
    rounded: "{rounded.box}"
    padding: "0 16px 0 14px"
    height: "36px"
  button-secondary:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    typography: "{typography.title}"
    rounded: "{rounded.box}"
    padding: "0 16px 0 14px"
    height: "36px"
  status-pill:
    backgroundColor: "{colors.lift}"
    textColor: "{colors.blue-lo}"
    typography: "{typography.tag}"
    rounded: "{rounded.pill}"
    padding: "0 8px 0 22px"
    height: "24px"
  project-card:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.soft}"
    typography: "{typography.body}"
    rounded: "{rounded.panel}"
    padding: "0 24px"
    width: "830px"
  project-card-narrow:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.soft}"
    typography: "{typography.body-narrow}"
    rounded: "{rounded.panel}"
    padding: "0 16px"
    width: "360px"
  section-label-dark:
    textColor: "{colors.muted}"
    typography: "{typography.section-label}"
    height: "18px"
  section-label-light:
    textColor: "{colors.label-light}"
    typography: "{typography.section-label}"
    height: "18px"
  activity:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.stat}"
    rounded: "{rounded.panel}"
    padding: "0 24px"
    width: "830px"
    height: "500px"
  activity-narrow:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.stat}"
    rounded: "{rounded.panel}"
    padding: "0 16px"
    width: "360px"
    height: "552px"
---

# Design System: R204570 Console

<!-- Recorded from the built world on 2026-10-21. Ground truth is scripts/console.py, scripts/hero.py,
     scripts/build_assets.py, scripts/activity.py and the 22 SVGs in assets/. Product truth lives in PRODUCT.md. -->

## Overview

**Creative North Star: "The Well-Run Console"**

The profile is a formal developer console, not a themed costume: a dashboard of shipped systems in blue and black. Every visual is an SVG panel drawn by Python (`scripts/console.py` is the shared kit), because GitHub strips CSS and JS from READMEs. Each panel is the same object: GitHub's own dark ground, a 1px seam around a 12px-radius frame, a faint dot grid, fine film grain, and content set in two faces, Geist for words and Geist Mono for data. Blue is the only accent, and one dot on the whole page breathes.

The register is "somewhat formal" (PRODUCT.md, confirmed by the user). Density is dashboard-like but calm: short labels, key/value rows, numbers set large, sentences kept to one or two lines. Personality lives in a few precise details: the grain speckled into the lit marks (the name, the numbers, the bars, the Résumé fill), the live 26-week strip and 52-week chart redrawn twice a day by a GitHub Action, the "idea to deployed" pipeline, and the hidden flag for security people. Two earlier worlds were rejected outright, stacked medical imaging and a demoscene cracktro title screen; nothing from either survives.

Panels stay opaque dark in both GitHub themes on purpose. In dark mode they sit flush with the page; in light mode they read as embedded console screens. Only the section labels, which sit directly on GitHub's ground, swap between a dark and a light drawing.

**Key Characteristics:**
- One object, repeated: dark ground, 1px seam, 12px frame, 22px dot grid, grain.
- Geist for words, Geist Mono for data; uppercase only on small tracked mono field labels.
- Blue is the only hue, in three tones with fixed jobs; one solid blue fill (Résumé).
- Exactly one animation: the hero's availability dot breathing; still under reduced motion.
- Every scaled panel exists twice: 830px wide and a recomposed 360px narrow drawing.
- Live panels (hero, activity) are redrawn twice a day; all other panels are static builds.

## Colors

Near-black slate neutrals stepped by tone, one blue in three tones, and a single light-theme grey for labels that sit on GitHub's white page. Token names match the constants in `scripts/console.py` (`GROUND`, `PANEL`, `LIFT`, `SEAM`, `TEXT`, `SOFT`, `MUTED`, `BLUE`, `BLUE_HI`, `BLUE_LO`, `WHITE`, `LABEL_LIGHT`).

### Primary
- **Signal Blue** (blue): solid fills only. The Résumé button, the chart bars (opacity scales with volume, from .45 in the activity chart and .5 in the hero strip up to 1), the pipeline connectors, and the hero's radial wash (at 22% fading to 0). 4.08:1 against the ground as a non-text mark; white type on it measures 4.63:1.
- **Live Blue** (blue-hi): marks of state and kind. Every status dot (the breathing dot, the now-shipping dot, the activity "Live" dot, the pill dots), the stage icons in the pipeline, the box icon on each project card, the event icons in the activity feed. 7.49:1 on the ground, 6.49:1 on lift.
- **Readout Blue** (blue-lo): blue that must read as text. "Available" in the profile column, "docsforge" in the now-shipping line, status pill labels, the "Busiest week" annotation, and the single peak bar in each chart. 9.73:1 on the ground, 9.16:1 on panel, 8.43:1 on lift. Note the naming trap: `BLUE_LO` is the *lighter* of the two light blues.

### Neutral
- **Console Black** (ground): every panel's ground; it is GitHub's own dark page colour, so panels sit flush in dark mode. Also the masking discs behind the narrow pipeline's stage icons.
- **Raised Slate** (panel): boxes inside a panel: the now-shipping box, the pipeline stages, secondary buttons. 1.06:1 over the ground; the seam does the separating.
- **Lift Slate** (lift): the status pill only, one step above panel.
- **Seam Steel** (seam): every 1px seam, frame and box border, the chart baseline, and zero-contribution week stubs. 1.34:1 on the ground: structural and decorative, never the only carrier of meaning.
- **Console White** (text): names, values, stage names, stat numbers, the title-bar status. 16.0:1 on the ground, 15.1:1 on panel.
- **Soft Steel** (soft): body copy on the ground: the hero pitch and card descriptions. 11.8:1 on the ground, 9.4:1 at the brightest point of the hero wash.
- **Key Grey** (muted): keys, labels, units, dates, tool lists, secondary icons, the title-bar path. 6.15:1 on the ground, 5.79:1 on panel, 4.91:1 at the brightest point of the hero wash.
- **Button White** (white): icon and label on the Résumé fill, nowhere else.
- **Light-Theme Label Grey** (label-light): the section labels' light-theme drawing, on GitHub's white page (6.11:1). Key Grey would only reach 3.08:1 there, which is why the pair exists.

### Named Rules
**The One Accent Rule.** Blue is the only hue on the page. Signal Blue fills, Live Blue marks state, Readout Blue is text. No green for "online", no red, no amber; state is said in blue tones and words.

**The One Solid Blue Rule.** The Résumé button is the only solid blue surface. Every other action is a Raised Slate box with a seam.

**The Opaque Console Rule.** Panels are opaque Console Black in both GitHub themes. Only content that sits directly on GitHub's page (the section labels) gets a dark/light pair via `prefers-color-scheme`.

## Typography

**Display Font:** Geist (variable font from google/fonts, instanced at 400, 500, 600)
**Body Font:** Geist
**Label/Mono Font:** Geist Mono (instanced at 400, 500)

Both faces are SIL OFL 1.1 (`scripts/fonts/OFL.txt`) and are embedded in every SVG as WOFF2 data URIs, so panels render identically wherever GitHub shows them. Static panels embed exact per-panel subsets; the live panels embed the committed basic-latin subsets (`scripts/fonts/*.woff2`). Kept OpenType features: `kern`, `liga`, `calt`, `tnum`. Text outside the panels (the link rows, the "More work" line, the Hidden part) is GitHub's own sans and is not part of this system.

**Character:** a neutral, engineered grotesk for anything a person reads as language, and its monospace twin for anything a machine would print. The pairing is what makes the page read as a console without costume.

### Hierarchy
- **Display** (Geist 600, 66px, tracking -2px ≈ -0.03em; narrow 46px, -1.4px): the name "Raj Patel" only, Console White, speckled.
- **Stat** (Geist 600, 22px; narrow 21px): the four activity numbers, speckled; followed by a **Unit** in Key Grey.
- **Lede** (Geist 400, 18px on a 26px pitch; narrow 15.5px on 22px): the hero pitch in Soft Steel, wrapped to 450px (narrow 328px), two lines.
- **Body** (Geist 400, 15px on 22px; narrow 14px on 20px): card descriptions in Soft Steel, wrapped to the card's inner width.
- **Title** (Geist 500, 14px): pipeline stage names and button labels.
- **Value** (Geist 400, 14px): card fact values and feed sentences; the hero's profile and credential values sit a half-step down at 13.5px (narrow 13px), right-aligned.
- **Unit** (Geist 400, 13px; narrow 12.5px): stat units and the "idea to deployed" gloss, Key Grey.
- **Repo** (Geist Mono 500, 16px; narrow 14.5px): repository names on cards, shrinking by 0.5px steps down to 12px before anything is cut.
- **Command** (Geist Mono 400, 13px; narrow 11.5px): the now-shipping line; "docsforge" steps to 500 in Readout Blue; the `$ pipx install docsforge` line is 1px smaller in Key Grey.
- **Data** (Geist Mono 400, 12.5px; narrow 11.5 to 12px): title-bar paths, profile and credential keys, the strip total, feed dates (12px).
- **Data small** (Geist Mono 400, 11px; axis ticks 10.5px): pipeline tool lists, status bar, chart axis, the busiest-week note.
- **Tag** (Geist Mono 500, 11.5px; narrow 11px): status pill labels, sentence case, Readout Blue.
- **Label** (Geist Mono 500, 11px, uppercase, tracking 1.4px ≈ 0.13em; narrow 10.5px, 1.3px): panel section labels: PROFILE, CREDENTIALS, PIPELINE, LAST 26 WEEKS, LATEST.
- **Key** (Geist Mono 500, 10.5px, uppercase, tracking 1px ≈ 0.1em; narrow 10px): field keys above values: STACK, RESULT, LIVE, CONTRIBUTIONS, LONGEST STREAK.
- **Section label** (Geist Mono 500, 12px, uppercase, tracking 1.6px ≈ 0.13em): the README's h3 images, SELECTED WORK and ACTIVITY.

### Named Rules
**The Words and Data Rule.** Geist sets what a person reads as language (the name, sentences, values, stage names). Geist Mono sets what a machine would print (paths, keys, dates, counts in captions, tool lists, commands, repository names, labels). Never swap them for effect.

**The Field Label Rule.** Uppercase appears only in Geist Mono 500 at 10 to 12px with positive tracking, and only to name a field or a section. A label never sits above a larger headline as a kicker.

**The Measured Text Rule.** Every string is placed with `measure()`, `wrap()` or `fit()` from `console.py`, which use advance widths from `scripts/fonts/metrics.json` without kerning; leave a few pixels of slack. A character outside the committed set (`BASIC` in `build_assets.py`: ASCII plus `·×→↗•★–—…’é®`) has no metrics and no glyph in the live subsets until it is added there and the build is rerun.

## Layout

The README is a single column about 830px wide on desktop and about 360px on phones (PRODUCT.md, Operating Context). Panels are drawn to exactly those widths: an 830px viewBox for wide and a 360px viewBox for narrow, displayed at natural size. GitHub's markdown supplies only the vertical flow between images.

**Spacing rhythm.** Panel gutter 24px wide and 16px narrow; the hero's left column is inset 30 to 32px. Key/value rows step 24px wide and 22px narrow. The dot grid is a 22px lattice. Pipeline stages sit 14px apart; icon-to-label gap is 8px; icons are 15 to 18px. Title bars are 44px tall wide (40px on the narrow hero), each closed by a full-width seam.

**Wide hero (830 x 550).** Title bar 0 to 44. A vertical seam at x=520 splits the body down to y=384: left column (x 32 to 488, 456px) holds the name (baseline 134), the two-line pitch (from baseline 174), the now-shipping box (56px tall) and the live strip; right column (x 544 to 806) holds PROFILE (four rows from baseline 104) and CREDENTIALS (four rows from 254), keys left in mono, values right-aligned in sans. A full-width seam at 384 opens the pipeline band: label at 414, six 116 x 96px stages from y=430, joined by 14px blue connectors at mid-height.

**Narrow hero (360 x 870).** One column, recomposed rather than shrunk: title bar (40px, no folder icon, status shortened to "Open to AI roles"), name, pitch, now-shipping box (328px), strip (328px), then PROFILE, CREDENTIALS and PIPELINE stacked between seams. The pipeline becomes a vertical list on a 34px pitch: a blue line runs down x=24 through the stage icons (each on a 10px Console Black disc), stage name at x=42, tools joined by " · " at x=124.

**Cards.** Header row 50px (icon, repo name, status pill), seam, description from baseline 80, then three facts. Wide: facts in columns at x=24, 300 and 560, key above value; height 156px for a one-line description, 178px for two. Narrow: facts stacked on a 44px pitch; heights 258 to 298px.

**Activity (830 x 500 with three feed events; 360 x 552 narrow).** Title bar 44; chart from y=74 to a baseline at 190 with month ticks below; seam; four stat cells in a row separated by short vertical seams (narrow: a 2 x 2 grid on a 58px pitch with one vertical seam); seam; LATEST with up to three event rows on a 30px pitch; seam; status bar. Height follows the feed: fewer events, shorter panel.

### README markup pattern and source order
Every scaled panel is one line, wrapped in its link:

```html
<a href="TARGET"><picture><source media="(max-width: 600px)" srcset="./assets/NAME-narrow.svg"><img src="./assets/NAME.svg" alt="Complete text equivalent"></picture></a><br>
[Live site](URL) · [Source](URL)
```

Section labels are h3 elements holding a theme pair:

```html
<h3><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/label-KEY-dark.svg"><img src="./assets/label-KEY-light.svg" alt="Section name"></picture></h3>
```

Source order in README.md:
1. The DIRECTION CONTRACT comment (first HTML comment).
2. The hidden part's stage-1 comment (second HTML comment).
3. Hero panel, linked to the portfolio.
4. Button row in a `<p>`, one `<a><img></a>` per line: Résumé (primary) first, then Email, LinkedIn, Portfolio, Kaggle, Medium. Buttons and labels are natural-size images and have no narrow drawings; the row wraps on phones.
5. "Selected work" label.
6. Four project cards in order DocsForge, NeuroAssist, Hospital Management System, PCB defect detection, each linked to its repository and followed by `<br>` and a markdown link row.
7. A `<sub>` "More work" line of further repositories.
8. "Activity" label.
9. Activity panel, linked to `.github/workflows/activity.yml`.
10. `<details>` "Hidden part · for security people".

### Named Rules
**The Two Drawings Rule.** Every panel that would otherwise scale gets a 360px `-narrow` drawing, recomposed for the phone column (stacked facts, vertical pipeline, 2 x 2 stats), and served by `<source media="(max-width: 600px)">`. Never rely on GitHub shrinking an 830px drawing.

**The One-Line Picture Rule.** A `<picture>` block stays on a single line. Multi-line picture blocks inside a link break on GitHub.

## Elevation & Depth

The system is flat. Depth comes from tone and line: Console Black ground, Raised Slate boxes one step up, Lift Slate for the pill, and a 1px Seam Steel stroke around every frame and box. There are no shadows anywhere. Atmosphere comes from three textures drawn by `Canvas.panel()` and one drawn into marks by `Canvas.speckle()`:

- **Dot grid:** a 22px pattern of 0.75px dots in Console White at 7% opacity, clipped to the frame.
- **Grain:** desaturated fractal noise (base frequency 0.9, 2 octaves, seed 7) mapped to 0 to 14% alpha, clipped to the frame.
- **Blue wash (hero only):** a radial gradient of Signal Blue from 22% to 0, centred at (150, 110) with a 430px radius on the wide hero and (80, 90) with 300px on the narrow one.
- **Speckle:** fractal noise (base frequency 0.95, 2 octaves, seed 11) toned to 0.5 to 1.25, clipped to the mark and multiplied over it, so specks darken a mark by up to half. Applied to the hero name, the stat numbers, every chart bar, and the Résumé fill. The darkest speck in Console White type measures about 4.15:1 on the ground, which is why it is reserved for large type.

### Named Rules
**The Seam Not Shadow Rule.** Separation is a 1px seam and one tonal step. No drop shadows, glows, blurs or glass.

**The Grain in the Light Rule.** Grain lives on every ground; speckle lives only in large lit marks (display type, stat numbers, bars, the one solid blue fill). Never speckle text under about 21px, secondary copy, or icons.

## Shapes

Quiet, engineered geometry. Frames have a 12px radius; boxes inside them (now-shipping box, pipeline stages, buttons) have 8px; the status pill is fully round (12px on a 24px height). Chart bars carry a hint of rounding (2px wide activity, 1px narrow activity, 1.5px in the hero strip). Every stroke is 1px Seam Steel unless it is a pipeline connector; frames sit on a half-pixel inset and chart baselines on a half-pixel offset so they land crisp. Icons are one family: line icons after Lucide on a 24px grid, drawn at 15 to 18px with a 1.75px stroke at any size, round caps and joins (`ICONS` in `console.py`: file, mail, linkedin, globe, chart, book, check, box, commit, merge, dot, folder, pin, and the stage set database, cpu, bot, server, rocket, shield).

## Components

### Source and regeneration
- `scripts/console.py`: palette, `Canvas` (text, rect, line, icon, dot, pulse, speckle, panel, svg), icons, `measure`/`wrap`/`fit`, `font_css`. Standard library only.
- `scripts/hero.py`: the hero, wide and narrow. Called by `activity.py` because it carries live data.
- `scripts/build_assets.py`: instances and subsets Geist and Geist Mono with fontTools (fetched once into the git-ignored `scripts/fonts/src/`), writes the committed WOFF2 subsets and `metrics.json`, then draws the buttons, cards (wide and narrow) and section labels.
- `scripts/activity.py` + `.github/workflows/activity.yml`: draws `assets/activity*.svg` and `assets/hero*.svg` from the contribution calendar (GraphQL with `GITHUB_TOKEN`, else the public calendar page) and the public events feed. The Action runs at 06:41 and 18:41 UTC, on manual dispatch, and on pushes that touch `activity.py`, `console.py`, `hero.py`, `scripts/fonts/**` or the workflow, and commits only those four SVGs.

To regenerate:

```sh
pip install fonttools brotli
python3 scripts/build_assets.py      # fonts, metrics, buttons, cards, labels
python3 scripts/activity.py          # hero and activity, live data
python3 scripts/activity.py --demo --out-dir /tmp/preview   # offline preview with synthetic data
```

A palette or type change in `console.py` must be followed by both commands; the Action only redraws the live panels, so skipping `build_assets.py` leaves static and live panels in different colours.

### Panel (the shared frame)
- **Character:** one console object, reused for hero, cards and activity.
- **Anatomy:** frame at a 0.5px inset, 12px radius, Console Black fill; optional blue wash; dot grid; grain; 1px Seam Steel stroke on top. A title bar (where present) is 44px with a 15px folder icon in Key Grey, a mono path (`r204570 / profile`, `r204570 / activity`) at 12.5px Key Grey, a status at the right in Console White, and a full-width seam beneath. Sections inside are split by full-width seams.
- **Accessibility:** every SVG is `role="img"` with `<title>` and `<desc>` (the desc carries the full data, live numbers included) and the README `<img alt>` repeats the content without live numbers.

### Hero
- **Character:** the first viewport: who, what, proof, availability.
- **Title-bar status:** "Open to AI roles · freelance" (narrow: "Open to AI roles") in Geist Mono 12.5px Console White, led by the breathing dot.
- **Body:** Display name, Lede pitch, now-shipping box, live strip, profile and credentials column, pipeline band (see Layout for geometry).

### Breathing dot (motion)
- **Shape:** a 3.5px Live Blue dot (3px narrow) with a halo circle at 2.2x radius, 18% opacity at rest.
- **Motion:** the halo scales from 0.5 to 1.25 while fading from 35% to 0, over 2.4s, ease-out, infinite.
- **Reduced motion:** every SVG ships `@media (prefers-reduced-motion: reduce) { * { animation: none !important } }`; the dot then sits still with a static faint halo.

**The One Breath Rule.** One thing moves on the whole page: the hero's availability dot. Every other status dot (now-shipping, activity "Live", pill dots) is a static 3.5px Live Blue circle. Never add a second animation.

### Now-shipping box
- **Shape:** Raised Slate, seam border, 8px radius, 56px tall, full column width (456px wide, 328px narrow).
- **Content:** a static Live Blue dot at (20, 20); "now shipping" in Command Console White, "docsforge" in Command 500 Readout Blue, "in production" in Key Grey; beneath it `$ pipx install docsforge` 1px smaller in Key Grey.

### Live strip
- **Character:** proof of activity inside the first viewport.
- **Content:** "LAST 26 WEEKS" (Label, Key Grey) left; "N contributions" (mono, 1.5px larger than the label, Console White) right-aligned; 26 weekly bars from 12px below the label down to a seam baseline 52px lower.
- **Bars:** height follows the square root of the week's count over the peak (minimum 3px); Signal Blue at 50 to 100% opacity by volume; the peak week solid Readout Blue; zero weeks are 2px Seam Steel stubs. 3px gutters, 1.5px radius, all speckled.

### Pipeline stage
- **Wide:** Raised Slate box, seam border, 8px radius, 116 x 96px. A 16px stage icon in Live Blue at (12, 12), stage name in Title Console White beside it, three tools below in Data small Key Grey on a 16px pitch. Stages joined by 14px Signal Blue connectors at mid-height. Section header "PIPELINE" (Label) plus "idea to deployed" (Unit).
- **Narrow:** no boxes. A vertical Signal Blue line through the six icons, each icon on a Console Black disc, stage name in Title, tools on one line in Data small Key Grey separated by " · ".
- **Stages:** Data (database), Model (cpu), Agent (bot), Backend (server), Ship (rocket), Secure (shield).

### Buttons
- **Shape:** gently rounded box (8px radius), 36px tall, width fitted to the label: 14px left pad, 16px icon, 8px gap, label, 16px right pad.
- **Primary (Résumé only):** Signal Blue fill, speckled; icon and label in Button White; label in Title (Geist 500 14px).
- **Secondary (Email, LinkedIn, Portfolio, Kaggle, Medium):** Raised Slate fill, Seam Steel border, icon in Key Grey, label in Console White.
- **Hover / Focus:** none drawn. Buttons are images inside links; GitHub supplies the link focus ring. Do not simulate hover.

### Status pill
- **Style:** Lift Slate fill, Seam Steel border, fully round, 24px tall; a 3.5px Live Blue dot at 13px from the left; label in Tag (Geist Mono 500, 11.5px; 11px narrow) Readout Blue, sentence case: Production, Capstone, Live.
- **Placement:** top-right of each project card's header row.

### Project card
- **Corner Style:** panel frame, 12px radius, no title-bar path.
- **Header:** 18px box icon in Live Blue, repository name in Repo Console White (shrinks before truncating; the real repository name is never cut), status pill right; seam at 50px.
- **Body:** description in Body Soft Steel; then three facts, each a Key (Key Grey, uppercase) above a Value (Console White). Wide: three columns. Narrow: stacked.
- **Links:** the image links to the repository; live sites and source sit in a markdown row under the card, because links inside SVGs do not work.

### Section label
- **Style:** Section label type (Geist Mono 500, 12px, uppercase, tracking 1.6px), 18px tall, no frame. Dark drawing in Key Grey, light drawing in Light-Theme Label Grey, swapped by `prefers-color-scheme` inside an h3.

### Activity panel
- **Title bar:** `r204570 / activity` path; right side "Live · synced Mon D" led by a static Live Blue dot.
- **Chart:** 52 weekly bars from y=74 to a baseline at 190; height by square root of volume (minimum 4px); Signal Blue at 45 to 100% opacity, the peak week solid Readout Blue; zero weeks as Seam Steel stubs; 4px gaps and 2px radius wide, 1.6px gaps and 1px radius narrow; all speckled. The peak is annotated in Data small Readout Blue ("Busiest week · N contributions", narrow "N that week"), flipped to end-anchored when the peak is in the right half. Month ticks (10.5px mono Key Grey) are placed from the right edge back with a 44px (narrow 48px) minimum spacing, and "Today" closes the axis.
- **Stats:** CONTRIBUTIONS, LONGEST STREAK, ACTIVE DAYS, BUSIEST DAY: a Key above a speckled Stat number with a Unit beside it. Four columns divided by short vertical seams; 2 x 2 on narrow.
- **Feed:** "LATEST" (Label), up to three events: 16px Live Blue icon (commit, merge, dot), sentence in Value Console White truncated with an ellipsis by `fit()`, date right-aligned in Data Key Grey. Empty state: "No public events this week." in Key Grey. With no contributions at all, the chart area reads "No public activity in the last 52 weeks".
- **Status bar:** "r204570 · Ahmedabad, IN · UTC+5:30" left and "Redrawn twice a day by GitHub Actions" right, Data small Key Grey (narrow keeps only the right-hand line).

### Hidden part
- **Markup:** a `<details>` block at the end of the README with a short brief and a finder count.
- **Layers:** stage 1 is the README's second HTML comment; stage 2 is an HTML comment carried only by `assets/hero.svg` (the wide hero), emitted by `hero.wide()` through `Canvas.svg(comment=...)`. Regeneration keeps it only while that argument stays in place; never strip comments when optimising SVGs, and never move the note anywhere visible.

## Do's and Don'ts

### Do:
- **Do** change colours, type and icons in `scripts/console.py`, then run both `build_assets.py` and `activity.py`; never hand-edit `assets/*.svg` (the Action overwrites the hero and activity twice a day).
- **Do** draw every new panel with `Canvas.panel()` at 830px, with a recomposed 360px `-narrow` twin served by `<source media="(max-width: 600px)">`, on one line inside its link.
- **Do** keep Blue to its three jobs: Signal Blue (#1F6FEB) fills, Live Blue (#58A6FF) state marks and icons, Readout Blue (#79C0FF) blue text.
- **Do** set words in Geist and data in Geist Mono, and place every string with `measure()`, `wrap()` or `fit()`.
- **Do** give every image an alt that is a complete text equivalent, and keep live numbers out of README alt text (only the SVGs are redrawn).
- **Do** put links that matter in a markdown row under the image; an SVG cannot carry a working link.
- **Do** add any new character to `BASIC` in `build_assets.py` and rerun it before a live panel uses it.
- **Do** preview with `python3 scripts/activity.py --demo --out-dir <somewhere outside assets>`.

### Don't:
- **Don't** add a second hue: no green "online", red error or amber warning; state is blue and words.
- **Don't** add a second solid blue fill or a second primary button; Résumé is the one.
- **Don't** animate anything besides the hero's availability dot, and don't remove the reduced-motion rule from `Canvas.svg()`.
- **Don't** add shadows, glows, blur, glass, or gradients other than the hero's blue wash.
- **Don't** make panels transparent or redraw them light for GitHub's light theme; only section labels swap.
- **Don't** speckle small text, secondary copy or icons.
- **Don't** put a mono uppercase label above a larger headline as a kicker; labels name fields and sections.
- **Don't** split a `<picture>` block across lines.
- **Don't** truncate a repository name; shrink it.
- **Don't** commit `--demo` output into `assets/`.
- **Don't** bring back the rejected worlds (stacked medical imaging, the cracktro title screen) or any playful costume; the register is somewhat formal.

### Known defects (recorded, not rules)
- The faintest chart bars (45% opacity in the activity chart, about 1.7:1; 50% in the hero strip, about 1.9:1) and the Seam Steel zero-week stubs (1.34:1) fall below 3:1 non-text contrast. The totals, stats, desc and alt carry the data, so this is tolerated; it is not a value to reuse for a mark that carries meaning on its own.
- Phone rendering was verified on github.com at a 500px window (system dark), which serves the 360px drawings. The GitHub mobile app was not tested; if it ignores `<source media>`, it falls back to the wide drawing scaled down.
