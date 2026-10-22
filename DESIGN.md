---
name: R204570 Console
description: Raj Patel's GitHub profile README drawn as a formal developer console in blue and black, on two grounds (dark console panels and a grainy electric-blue surface), with one accent family and one breathing dot.
colors:
  blue: "#1F6FEB"
  electric: "#1D4ED8"
  electric-soft: "#2563EB"
  blue-hi: "#58A6FF"
  blue-lo: "#79C0FF"
  sky: "#93C5FD"
  ground: "#0D1117"
  panel: "#121821"
  lift: "#18202B"
  ink: "#0B1220"
  seam: "#232C38"
  text: "#E6EDF3"
  soft: "#C3CDD8"
  muted: "#8B949E"
  white: "#FFFFFF"
  night: "#03050B"
  glass: "#050811"
  on-blue: "#FFFFFF"
  on-blue-soft: "#FFFFFF"
  on-blue-label: "#FFFFFF"
typography:
  display:
    fontFamily: "Geist, sans-serif"
    fontSize: "78px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-2.6px"
  display-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "52px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-1.6px"
  headline:
    fontFamily: "Geist, sans-serif"
    fontSize: "34px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-1px"
  headline-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "28px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-1px"
  stat:
    fontFamily: "Geist, sans-serif"
    fontSize: "22px"
    fontWeight: 600
    lineHeight: 1
  lede:
    fontFamily: "Geist, sans-serif"
    fontSize: "18.5px"
    fontWeight: 400
    lineHeight: "27px"
  lede-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "15.5px"
    fontWeight: 400
    lineHeight: "22px"
  tagline:
    fontFamily: "Geist, sans-serif"
    fontSize: "15.5px"
    fontWeight: 400
    lineHeight: "20px"
  tagline-narrow:
    fontFamily: "Geist, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "20px"
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
  row-title:
    fontFamily: "Geist, sans-serif"
    fontSize: "16px"
    fontWeight: 600
  title:
    fontFamily: "Geist, sans-serif"
    fontSize: "14px"
    fontWeight: 500
  chip:
    fontFamily: "Geist, sans-serif"
    fontSize: "12.5px"
    fontWeight: 500
  value:
    fontFamily: "Geist, sans-serif"
    fontSize: "14px"
    fontWeight: 400
  unit:
    fontFamily: "Geist, sans-serif"
    fontSize: "13px"
    fontWeight: 400
  command:
    fontFamily: "Geist Mono, monospace"
    fontSize: "13px"
    fontWeight: 400
  data:
    fontFamily: "Geist Mono, monospace"
    fontSize: "12.5px"
    fontWeight: 400
  flow:
    fontFamily: "Geist Mono, monospace"
    fontSize: "12px"
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
rounded:
  bar: "2px"
  box: "8px"
  panel: "12px"
  pill: "12px"
  card: "14px"
  hero: "16px"
spacing:
  icon-gap: "8px"
  chip-gap: "8px"
  gutter-narrow: "16px"
  grid: "22px"
  row-narrow: "22px"
  gutter: "24px"
  row: "24px"
  flow-gap: "26px"
  inset: "32px"
components:
  hero:
    backgroundColor: "{colors.night}"
    textColor: "{colors.on-blue}"
    typography: "{typography.display}"
    rounded: "{rounded.hero}"
    width: "830px"
    height: "410px"
  hero-narrow:
    backgroundColor: "{colors.night}"
    textColor: "{colors.on-blue}"
    typography: "{typography.display-narrow}"
    rounded: "{rounded.hero}"
    width: "360px"
    height: "626px"
  now-shipping:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.on-blue}"
    typography: "{typography.command}"
    width: "468px"
    height: "56px"
  now-shipping-narrow:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.on-blue}"
    width: "328px"
    height: "56px"
  live-strip:
    textColor: "{colors.on-blue}"
    typography: "{typography.label}"
    width: "766px"
    height: "60px"
  status-pill:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.on-blue}"
    typography: "{typography.tag}"
    rounded: "{rounded.pill}"
    padding: "0 8px 0 22px"
    height: "24px"
  flow-node:
    backgroundColor: "{colors.glass}"
    textColor: "{colors.on-blue}"
    typography: "{typography.flow}"
    rounded: "{rounded.box}"
    padding: "0 12px"
    height: "30px"
  card-header:
    backgroundColor: "{colors.night}"
    textColor: "{colors.on-blue}"
    typography: "{typography.headline}"
    rounded: "{rounded.card}"
    padding: "0 24px"
    height: "188px"
  project-card:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.soft}"
    typography: "{typography.body}"
    rounded: "{rounded.card}"
    padding: "0 24px"
    width: "830px"
    height: "362px"
  project-card-narrow:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.soft}"
    typography: "{typography.body-narrow}"
    rounded: "{rounded.card}"
    padding: "0 16px"
    width: "360px"
  chip:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    typography: "{typography.chip}"
    rounded: "{rounded.box}"
    padding: "0 12px 0 10px"
    height: "28px"
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
  more-row:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.row-title}"
    rounded: "{rounded.panel}"
    padding: "0 22px"
    width: "830px"
    height: "74px"
  more-row-narrow:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.row-title}"
    rounded: "{rounded.panel}"
    padding: "0 16px"
    width: "360px"
  stack:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.chip}"
    rounded: "{rounded.panel}"
    padding: "0 24px"
    width: "830px"
    height: "456px"
  stack-narrow:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
    typography: "{typography.chip}"
    rounded: "{rounded.panel}"
    padding: "0 16px"
    width: "360px"
    height: "732px"
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

<!-- Recorded from the built world on 2026-10-21 (second pass, after the grainy blue surface landed). Ground truth is
     scripts/console.py, scripts/hero.py, scripts/build_assets.py, scripts/activity.py, scripts/logos.json and the 40 SVGs
     in assets/. Product truth lives in PRODUCT.md. -->

## Overview

**Creative North Star: "The Well-Run Console"**

The profile is a formal developer console, not a themed costume: a dashboard of shipped systems in blue and black. Every visual is an SVG drawn by Python (`scripts/console.py` is the shared kit), because GitHub strips CSS and JS from READMEs. The system has two grounds and uses each for one job. The **grainy blue surface** (`Canvas.grainy()`) carries identity: the hero card and the header band of every project card, where a near-black Night is lit by two soft electric-blue glows entering from an edge, under visible white and black film grain, with type in three whites. The **console panel** (`Canvas.panel()`) carries detail: GitHub's own dark ground, a 1px seam around a 12px frame, a faint dot grid and fine grain, used for card bodies, the More work rows, the Tech stack and the Activity panel. Content is set in two faces, Geist for words and Geist Mono for data. Blue is the only hue, and one dot on the whole page breathes.

The register is "somewhat formal" (PRODUCT.md, confirmed by the user). Density is dashboard-like but calm: short labels, key/value rows, chips, numbers set large, sentences kept to one or two lines. Personality lives in a few precise details: the grain in the blue and in the lit marks (the name, the project names, the numbers, the bars, the Résumé fill), the live 26-week strip of white bars and the 52-week chart redrawn twice a day by a GitHub Action, the "how it works" flow drawn across each project header, monochrome technology marks, and the hidden flag for security people. Two earlier worlds were rejected outright, stacked medical imaging and a demoscene cracktro title screen; nothing from either survives.

Everything stays opaque in both GitHub themes on purpose. In dark mode the console panels sit flush with the page and the blue surfaces glow out of it; in light mode every panel reads as an embedded console screen. Nothing in the README swaps by theme: section headings are GitHub's own markdown `##` headings.

**Key Characteristics:**
- Two opaque grounds with fixed jobs: the grainy blue surface for identity (hero, project headers), the console panel for detail (card bodies, rows, stack, activity).
- Geist for words, Geist Mono for data; uppercase only on small tracked mono field labels.
- Blue is the only hue; each tone has one job, and Sky is the only blue that sits on the blue.
- One blue button (Résumé); the blue surface is a ground for identity, never an action.
- Exactly one animation: the hero's availability dot breathing; still under reduced motion.
- Every panel exists twice: 830px wide and a recomposed 360px narrow drawing; buttons are natural size.
- Live panels (hero, activity) are redrawn twice a day; all other panels are static builds.

## Colors

One blue family with fixed jobs, slate neutrals for the console, and a second set of neutrals (Night, Glass and three whites) for the grainy blue surface. Token names follow the constants in `scripts/console.py` (`BLUE`, `ELECTRIC`, `BLUE_HI`, `BLUE_LO`, `GROUND`, `PANEL`, `SEAM`, `TEXT`, `SOFT`, `MUTED`, `WHITE`, `NIGHT`, `GLASS`, `ON_BLUE`, `ON_BLUE_SOFT`, `ON_BLUE_LABEL`), with two exceptions: `electric-soft` is a literal inside `Canvas.grainy()`, and `sky` is a `SKY` literal defined twice, in `hero.py` and in `build_assets.py`; change both together. `console.py` still defines `LIFT` and `LABEL_LIGHT`, but nothing draws with them any more (the pill moved onto glass and the image section labels were removed), so they are not part of the system.

### Primary
- **Signal Blue** (blue): solid fills and glow bodies. The Résumé button, the activity chart bars (opacity scales with volume, 45% to 100%), and the 45% stop and fade-out of every glow on the grainy surface. 4.08:1 against the console ground as a non-text mark; white type on it measures 4.63:1.
- **Electric Blue** (electric): the hot centre of each surface's primary glow, at 95% opacity.
- **Electric Glow** (electric-soft): the hot centre of the secondary glow, at 70%.
- **Live Blue** (blue-hi): marks of state and kind on the console ground. The activity "Live" dot, the activity feed's event icons, the folder icon on each More work row. 7.49:1 on the ground.
- **Readout Blue** (blue-lo): blue that must read on the console ground. The activity peak bar and its "Busiest week" annotation, and every technology mark inside a chip (line icon or Simple Icons mark). 9.73:1 on the ground, 9.16:1 on Raised Slate. Naming trap: `BLUE_LO` is the *lighter* of the two light blues.
- **Sky** (sky): the only blue on the blue surface. The breathing availability dot, the now-shipping dot, the status-pill dots, "docsforge" in the command box, and "Available" in the profile column. 11.3:1 on Night and 7:1 or better where it is used (on Glass, or in the dark upper right of the hero); it drops to about 3.5:1 at a glow's brightest point, so it never sits there.

### Neutral
The console:
- **Console Black** (ground): every console panel's ground and every project card's body; it is GitHub's own dark page colour, so panels sit flush in dark mode.
- **Raised Slate** (panel): boxes on the console ground: chips and secondary buttons. 1.06:1 over the ground; the seam does the separating.
- **Seam Steel** (seam): every 1px seam, panel and card frame, chip and button border, the chart baseline, and zero-contribution week stubs in the activity chart. 1.34:1 on the ground: structural, never the only carrier of meaning.
- **Console White** (text): names, values, chip labels, button labels, stat numbers and the activity title-bar status on the console ground. 16.0:1 on the ground, 15.1:1 on Raised Slate.
- **Soft Steel** (soft): body copy on the console ground: card descriptions and More work descriptions. 11.8:1.
- **Key Grey** (muted): keys, labels, units, dates, axis ticks, title-bar paths and icons on the console ground, and the icon on every secondary button. 6.15:1 on the ground, 5.79:1 on Raised Slate.
- **Button White** (white): icon and label on the Résumé fill, and the bars of the hero's live strip.

The blue surface:
- **Night** (night): the black the glows fade into; the base fill of every grainy surface. White on it is 20.4:1.
- **Glass** (glass): boxes laid on the blue (the command box and flow nodes at 55% opacity, status pills at 60%), each with a white hairline at 16 to 22%. White type on Glass measures 13.8:1 or better even over a glow.
- **On-Blue White** (on-blue): content on the blue: the name, project names, the title-bar status, profile and credential values, the strip total, flow-node labels, pill labels. 6.1 to 6.4:1 at the brightest glow point of any surface.
- **On-Blue Soft** (on-blue-soft): sentences on the blue: the hero pitch and each project tagline. 4.9 to 5.2:1 at the brightest glow point.
- **On-Blue Label** (on-blue-label): small labels on the blue: title-bar paths, profile and credential keys, PROFILE, CREDENTIALS, LAST 26 WEEKS, "in production" and the install line, the hero's folder icon. 13.7:1 on Night but only 4.1 to 4.3:1 at a glow's brightest point; see Known defects.

### Named Rules
**The One Accent Rule.** Blue is the only hue on the page, with black and white as its partners. Signal Blue fills, Live Blue marks state on the console, Readout Blue is blue text on the console, Electric is the technology mark on a white chip, Sky is blue on the blue. No green for "online", no red, no amber, and no brand colours on technology marks; state is said in blue tones and words.

**The Two Palettes Rule.** Type on the grainy surface is only white (the three on-blue roles all resolve to #FFFFFF; hierarchy there comes from size, weight and mono labels), and Sky is only for marks, arrows and text inside a Glass box; type on the console ground uses only Console White, Soft Steel, Key Grey and the console blues. Never carry a colour across: Live Blue or Readout Blue vanish into the glow, and On-Blue Label is not a console grey.

**The One Blue Button Rule.** The Résumé button is the only button filled blue. Every other action is a Raised Slate box with a seam. The grainy blue surface is a ground for identity, never an action.

**The Opaque Console Rule.** Every panel is opaque (Console Black or Night) in both GitHub themes. Nothing is drawn twice for light and dark; headings are markdown, so GitHub themes them.

## Typography

**Display Font:** Geist (variable font from google/fonts, instanced at 400, 500, 600)
**Body Font:** Geist
**Label/Mono Font:** Geist Mono (instanced at 400, 500)

Both faces are SIL OFL 1.1 (`scripts/fonts/OFL.txt`) and are embedded in every SVG as WOFF2 data URIs, so panels render identically wherever GitHub shows them. Static panels embed exact per-panel subsets; the live panels embed the committed basic-latin subsets (`scripts/fonts/*.woff2`). Kept OpenType features: `kern`, `liga`, `calt`, `tnum`. Text outside the panels (the `##` section headings and the Hidden part) is GitHub's own sans and is not part of this system.

**Character:** a neutral, engineered grotesk for anything a person reads as language, and its monospace twin for anything a machine would print. The pairing is what makes the page read as a console without costume.

### Hierarchy
- **Display** (Geist 600, 78px, tracking -2.6px ≈ -0.033em; narrow 52px, -1.6px): the name "Raj Patel" only, On-Blue White, speckled.
- **Headline** (Geist 600, 34px, tracking -1px; narrow 28px): project names in each card header, On-Blue White, speckled. Shrinks by 1px steps until it fits the gutter; never truncated.
- **Stat** (Geist 600, 22px; narrow 21px): the four activity numbers, speckled; followed by a **Unit** in Key Grey.
- **Lede** (Geist 400, 18.5px on a 27px pitch; narrow 15.5px on 22px): the hero pitch in On-Blue Soft, wrapped to 460px (narrow 328px).
- **Tagline** (Geist 400, 15.5px; narrow 14px; 20px pitch): the one-line project tagline under each name, On-Blue Soft.
- **Body** (Geist 400, 15px on 22px; narrow 14px on 20px): card descriptions in Soft Steel, wrapped to the card's inner width. More work descriptions sit at 14.5px on one line (narrow: Body narrow, wrapped).
- **Row title** (Geist 600, 16px): the project name on each More work row, Console White.
- **Title** (Geist 500, 14px): button labels.
- **Chip** (Geist 500, 12.5px): technology names inside the white chips, Ink.
- **Value** (Geist 400, 14px; narrow 13.5px): card fact values and feed sentences; the hero's profile and credential values sit a half-step down at 13.5px (narrow 13px), right-aligned.
- **Unit** (Geist 400, 13px; narrow 12.5px): stat units, Key Grey.
- **Command** (Geist Mono 400, 13px; narrow 11.5px): the now-shipping line; "docsforge" steps to 500 in Sky; the `$ pipx install docsforge` line is 1px smaller in On-Blue Label.
- **Data** (Geist Mono 400, 12.5px; narrow 11.5 to 12px): title-bar paths and statuses, the hero's profile and credential keys, the strip total; card header paths and feed dates at 12px.
- **Flow** (Geist Mono 400, 12px; narrow 11px): the step names inside flow nodes, On-Blue White.
- **Data small** (Geist Mono 400, 11px; axis ticks 10.5px; activity status bar 11.5px wide): chart axis, busiest-week note, status bar.
- **Tag** (Geist Mono 500, 11.5px; narrow 11px): status pill labels, sentence case, On-Blue White.
- **Label** (Geist Mono 500, 11px, uppercase, tracking 1.4px ≈ 0.13em; narrow 10.5px, 1.3px): section labels inside panels: PROFILE, CREDENTIALS, LAST 26 WEEKS, LATEST; the Tech stack group names (AI / ML, AGENTS & LLMS ...) at 11px / 1.3px (narrow 10.5px / 1.2px).
- **Key** (Geist Mono 500, 10.5px, uppercase, tracking 1px ≈ 0.1em; narrow 10px): field keys above values: RESULT, LIVE, PROGRAMME, DATA, STARS, CONTRIBUTIONS, LONGEST STREAK.

### Named Rules
**The Words and Data Rule.** Geist sets what a person reads as language (names, sentences, values, chip and button labels). Geist Mono sets what a machine would print (paths, keys, dates, counts in captions, commands, pipeline steps, labels). Never swap them for effect.

**The Field Label Rule.** Uppercase appears only in Geist Mono 500 at 10 to 11px with positive tracking, and only to name a field or a group. A label never sits above a larger headline as a kicker. A title-bar path is a location, lowercase, and always shares its row with a status.

**The Measured Text Rule.** Every string is placed with `measure()`, `wrap()` or `fit()` from `console.py`, which use advance widths from `scripts/fonts/metrics.json` without kerning; leave a few pixels of slack. A character outside the committed set (`BASIC` in `build_assets.py`: ASCII plus `·×→↗•★–—…’é®`) has no metrics and no glyph in the live subsets until it is added there and the build is rerun.

## Layout

The README is a single column about 830px wide on desktop and about 360px on phones (PRODUCT.md, Operating Context). Panels are drawn to exactly those widths: an 830px viewBox for wide and a 360px viewBox for narrow, displayed at natural size. GitHub's markdown supplies only the vertical flow between images and the `##` headings.

**Spacing rhythm.** Panel gutter 24px wide and 16px narrow (More work rows 22px wide); the hero's left column is inset 28 to 32px. Key/value rows step 24px wide and 22px narrow. The dot grid on console panels is a 22px lattice. Icon-to-label gap is 8px; chips flow with 8px gaps on a 36px row pitch; flow nodes are joined by 26px arrow gaps and wrap on a 40px pitch. Title bars are 44px tall (40px on the narrow hero).

**Wide hero (830 x 410).** Title bar 0 to 44, closed by a full-width white hairline at 16%. A vertical hairline at x=524.5 splits the body down to y=300: left column holds the name (baseline 146, x=28), the two-line pitch (from baseline 190, x=32) and the now-shipping box (468 x 56); right column (x 548 to 806) holds PROFILE (label at 78, four rows from 102) and CREDENTIALS (label at 212, four rows from 236), keys left in mono, values right-aligned in sans. A full-width hairline at 316.5 opens the live strip across the foot: label at 344, 26 white bars from 356 down to 396, x 32 to 798.

**Narrow hero (360 x 626).** One column, recomposed rather than shrunk: title bar (40px, path shortened to `r204570`, no folder icon, status shortened to "Open to AI roles"), name, three-line pitch, now-shipping box (328px), the live strip (328px, 40px bars), a hairline, then PROFILE and CREDENTIALS stacked.

**Project cards (830 wide; 360 narrow; height follows the content).** A grainy header band: a title bar (folder icon, `r204570 / repo` path, status pill inside the bar, white seam at y=42.5; narrow shows the repo alone and a short status), the name (34px, 28px narrow, baseline 90 / 84), the tagline, then the flow of nodes (stage icon in Sky, lit Sky arrows) and air under it. A white hairline at 12% closes the band. The dark body: description, white technology chips, then two facts, key above value, at x=24 and x=470 (narrow: stacked). Each card and its buttons share one paragraph in the README (card, `<br>`, buttons).

**More work rows (830 x ~124; 360 narrow).** A 46px grainy blue tile (40px narrow) with the project's mark in white; title 20/600 (18 narrow) and a 16px description wrapped at 500px (15.5 narrow, full width); a facts column behind a seam at x=616 with two key/value pairs (narrow: two columns under the description). The MGMT model leads the list and has Notebook and Dataset buttons under it.

**Tech stack (830 wide; 360 narrow).** A grainy blue header band (104px; 100 narrow) with the title bar and a speckled white count line ("34 tools across 6 areas"), then six groups on the dark body (AI / ML, Agents & LLMs, Backend & data, Ship, Security, Languages), each separated by a seam inset to the gutters. Wide: group label at the gutter, white chips flowing from x=190. Narrow: label above its chips.

**Activity (830 wide; 360 narrow; height follows the feed).** The top of the panel is a grainy blue band holding the title bar (path, Sky live dot, "Live · synced"), the chart (52 white weekly bars, brightness by volume, the busiest week solid with a white call-out; 26-week view on the hero, full year here) and the month ticks, all in white. Below the band, on the dark body: four stat cells, LATEST with up to three project events, and the status bar.

### README markup pattern and source order
Every scaled panel is one line, wrapped in its link:

```html
<a href="TARGET"><picture><source media="(max-width: 600px)" srcset="./assets/NAME-narrow.svg"><img src="./assets/NAME.svg" alt="Complete text equivalent"></picture></a>
```

Link buttons are natural-size images in a `<p>`, one `<a><img></a>` per line:

```html
<p>
<a href="URL"><img src="./assets/btn-KEY.svg" alt="Label"></a>
</p>
```

Source order in README.md:
1. The DIRECTION CONTRACT comment (first HTML comment).
2. The hidden part's stage-1 comment (second HTML comment).
3. Hero panel, linked to the portfolio.
4. Profile button row: Résumé (primary) first, then Email, LinkedIn, Portfolio, Kaggle, Medium. The row wraps on phones.
5. `## Selected work`, then four project cards in order DocsForge, NeuroAssist, Hospital Management, PCB Defect Detection, each linked to its repository and followed by its own button row: Live site or Live demo, Source, and Contribute for DocsForge.
6. `## More work`: six linked rows (SAC AI Search, Reconciliation, ExpenseFlow, Cafe-POS, GearGuard, BraTS2020 MGMT).
7. `## Tech stack`: the stack panel, not linked.
8. `## Activity`: the activity panel, linked to `.github/workflows/activity.yml`.
9. `<details>` "Hidden part · for security people".

### Named Rules
**The Two Drawings Rule.** Every panel that would otherwise scale gets a 360px `-narrow` drawing, recomposed for the phone column (stacked facts, wrapped flows, chips under labels, 2 x 2 stats), and served by `<source media="(max-width: 600px)">`. Never rely on GitHub shrinking an 830px drawing.

**The One-Line Picture Rule.** A `<picture>` block stays on a single line. Multi-line picture blocks inside a link break on GitHub.

## Elevation & Depth

The system has no shadows. Depth comes from two grounds and the boxes laid on them.

**The console panel** (`Canvas.panel()`): a Console Black frame at a half-pixel inset, a 22px pattern of 0.75px Console White dots at 7% opacity, fine grain (desaturated fractal noise, base frequency 0.9, 2 octaves, seed 7, mapped to 0 to 14% alpha), and a 1px Seam Steel stroke on top. Boxes on it (chips, secondary buttons) are Raised Slate, one tonal step up, with a seam. `panel()` still accepts a `glow` wash, but nothing passes one any more.

**The grainy blue surface** (`Canvas.grainy()`): a Night fill under two radial glows, then two grain layers, all clipped to the frame (all four corners, or only the top two for a card header band).
- **Primary glow:** Electric Blue at 95% opacity, Signal Blue at 55% by 45% of the radius, gone at the edge. Its centre sits outside the box (below it on the hero and three cards, above it on Hospital Management), so the light enters from an edge. Hero wide (16%, 118%) with a radius of 85% of the width; hero narrow (10%, 105%) at 110%; cards at their own `glow` point with a 70% radius.
- **Secondary glow:** Electric Glow at 70%, Signal Blue at 30% by 45%, gone at the edge, in the opposite corner (hero wide (96%, -25%) at 55%; cards mirrored horizontally at -60% height with a 45% radius).
- **White specks:** fractal noise (base frequency 0.78, 3 octaves) turned into white with alpha 3.2·n − 1.68, at 42% opacity.
- **Black specks:** the same noise at seed + 31, black with alpha 1.5 − 3.2·n, at 50% opacity. Seeds: hero 4; each card 7 plus the length of its key.
- No dot grid reaches the blue surface.

On the blue, separation is a white hairline (12% under a card band, 14% around the hero frame, 16% for the hero's dividers and box strokes, 22% around pills and flow nodes) and Glass boxes: Glass at 55 to 60% opacity, no blur.

**Speckle** (`Canvas.speckle()`): fractal noise (base frequency 0.95, 2 octaves, seed 11) toned to 0.5 to 1.25, clipped to the mark and multiplied over it, so specks darken a mark by up to half. Applied to the hero name, the project names, the stat numbers, every bar in the hero strip and the activity chart, and the Résumé fill.

### Named Rules
**The Seam and Glass Rule.** On the console ground, separation is a 1px seam and one tonal step. On the blue, it is a white hairline and a Glass box. No drop shadows, no blur or backdrop filter anywhere, and glows exist only inside `grainy()`.

**The Grain in the Light Rule.** Grain lives on every ground (fine grey grain on the console, white and black specks on the blue); speckle lives only in large lit marks (display and headline type, stat numbers, bars, the one blue button). Never speckle text under about 21px, secondary copy, or icons.

## Shapes

Quiet, engineered geometry, rounder as the object grows: the hero frame has a 16px radius, project cards 14px (the header band rounds only its top corners to match), console panels (More work rows, Tech stack, Activity) 12px, the command box 10px, and boxes (buttons, chips, flow nodes) 8px; status pills are fully round (12px on a 24px height). Chart bars carry a hint of rounding (2px wide activity, 1px narrow activity, 1.5px in the hero strip). Strokes are 1px: Seam Steel on the console ground, white at low opacity on the blue; frames sit on a half-pixel inset and seams are drawn `crispEdges` so they land sharp.

Flow arrows are drawn, not typed: a 16px shaft with a 4px chevron head, white at 70%, 1.4px stroke, round caps and joins.

Icons are one family: line icons after Lucide on a 24px grid, drawn at 15 to 18px with a 1.75px stroke at any size, round caps and joins (`ICONS` in `console.py`; in use: file, mail, linkedin, globe, chart, book, external, users, folder, commit, merge, dot, and for chips plug, layers, bot, cpu, database, shield). Technology marks are Simple Icons paths (CC0, `simple-icons@15.0.0`, cached in `scripts/logos.json`), filled in one colour at 15px (16px on the Source button). When a mark is unreadable at that size, the technology gets a line icon instead: Kaggle uses the chart icon.

## Components

### Source and regeneration
- `scripts/console.py`: palette, `Canvas` (text, rect, line, icon, logo, dot, pulse, speckle, panel, grainy, svg), icons, `measure`/`wrap`/`fit`, `font_css`. Standard library only.
- `scripts/hero.py`: the hero, wide and narrow. Called by `activity.py` because it carries live data.
- `scripts/build_assets.py`: instances and subsets Geist and Geist Mono with fontTools (fetched once into the git-ignored `scripts/fonts/src/`), writes the committed WOFF2 subsets and `metrics.json`, fetches the Simple Icons marks once into `scripts/logos.json`, then draws the ten buttons, the four project cards, the six More work rows and the Tech stack panel, each wide and narrow except the buttons.
- `scripts/activity.py` + `.github/workflows/activity.yml`: draws `assets/activity*.svg` and `assets/hero*.svg` from the contribution calendar (GraphQL with `GITHUB_TOKEN`, else the public calendar page) and the public events feed. The Action runs at 06:41 and 18:41 UTC, on manual dispatch, and on pushes that touch `activity.py`, `console.py`, `hero.py`, `scripts/fonts/**` or the workflow, and commits only those four SVGs.

To regenerate:

```sh
pip install fonttools brotli
python3 scripts/build_assets.py      # fonts, metrics, logos, buttons, cards, more-work rows, stack
python3 scripts/activity.py          # hero and activity, live data
python3 scripts/activity.py --demo --out-dir /tmp/preview   # offline preview with synthetic data
```

A palette or type change in `console.py` must be followed by both commands; the Action only redraws the live panels, so skipping `build_assets.py` leaves static and live panels in different colours.

### Panel title bar
- **Console (Tech stack, Activity):** 44px, 15px folder icon in Key Grey, mono path (`r204570 / stack`, `r204570 / activity`) at 12.5px Key Grey, an optional status at the right in Console White led by a static Live Blue dot, and a full-width seam beneath.
- **Hero (on the blue):** the same shape in On-Blue Label and On-Blue White, the status led by the breathing Sky dot, closed by a white hairline.
- **Card header row:** path in On-Blue Label (no icon, no hairline) with the status pill at the right.
- **Accessibility:** every SVG is `role="img"` with `<title>` and `<desc>` (the desc carries the full data, live numbers included) and the README `<img alt>` repeats the content without live numbers.

### Hero
- **Character:** the first viewport: who, what, proof, availability, all on the grainy blue surface.
- **Title-bar status:** "Open to AI roles · freelance" (narrow: "Open to AI roles") in Geist Mono 12.5px On-Blue White, led by the breathing dot.
- **Body:** Display name, Lede pitch, now-shipping box, profile and credentials column, live strip (see Layout for geometry).

### Breathing dot (motion)
- **Shape:** a 3.5px Sky dot (3px narrow) with a halo circle at 2.2x radius, 18% opacity at rest.
- **Motion:** the halo scales from 0.5 to 1.25 while fading from 35% to 0, over 2.4s, ease-out, infinite.
- **Reduced motion:** every SVG ships `@media (prefers-reduced-motion: reduce) { * { animation: none !important } }`; the dot then sits still with a static faint halo.

**The One Breath Rule.** One thing moves on the whole page: the hero's availability dot. Every other status dot (now-shipping, status pills, activity "Live") is a static 3.5px circle. Never add a second animation.

### Now-shipping box
- **Shape:** Glass at 55% with a white hairline at 16%, 10px radius, 56px tall, column width (468px wide, 328px narrow).
- **Content:** a static Sky dot at (20, 20); "now shipping" in Command On-Blue White, "docsforge" in Command 500 Sky, "in production" in On-Blue Label; beneath it `$ pipx install docsforge` 1px smaller in On-Blue Label.

### Live strip
- **Character:** proof of activity inside the first viewport; the Activity panel below owns the full-year detail.
- **Content:** "LAST 26 WEEKS" (Label, On-Blue Label) left; "N contributions" (mono, 1.5px larger than the label, On-Blue White) right-aligned; 26 weekly bars from 12px below the label down to a baseline 40px lower.
- **Bars:** Button White; height follows the square root of the week's count over the peak (minimum 3px); opacity 45% to 100% by the same root; zero weeks are 2px stubs at 28%. 3px gutters, 1.5px radius, all speckled. No peak colour: the tallest bar is simply solid.

### Status pill
- **Style:** Glass at 60% with a white hairline at 22%, fully round, 24px tall, width fitted to the label; a 3.5px Sky dot 13px from the left; label in Tag (Geist Mono 500, 11.5px; 11px narrow) On-Blue White, sentence case: Production, Capstone, Live · 100 stars, Live demo.
- **Placement:** right end of each card's header row.

### Flow (how it works)
- **Character:** each project draws how it works, left to right, inside its header band.
- **Node:** Glass at 55% with a white hairline at 22%, 8px radius, 30px tall, 12px side padding, step name in Flow (Geist Mono 400, 12px; 11px narrow) On-Blue White.
- **Join:** a drawn arrow in the 26px gap between nodes; when the next node does not fit, the flow wraps to a new row 40px down with no arrow into its first node.

### Project card
- **Character:** identity on the blue, evidence on the console.
- **Header band:** grainy surface, top corners rounded to 14px, height set by its content: path and status pill, the speckled Headline name, the tagline, the flow. Each card has its own glow point, so no two bands are lit the same.
- **Body:** Console Black; description in Body Soft Steel; technology chips; two facts, each a Key (Key Grey, uppercase) above a Value (Console White). Wide: two columns. Narrow: stacked.
- **Frame:** 1px Seam Steel around the whole card, 14px radius, over a white 12% hairline where band meets body.
- **Links:** the image links to the repository; working links sit in a button row under the card, because links inside SVGs do not work.

**The Identity Band Rule.** A project card opens with a grainy header band that says what the thing is and how it works (path, status, name, tagline, flow) and closes with a console body that proves it (description, stack, facts). Facts never go on the blue.

### Chip
- **Style:** the white set. Solid white (#FFFFFF), no border, 8px radius, 28px tall; a 16px line icon (2px stroke) or a 15px Simple Icons mark in Electric (#1D4ED8) 10px from the left; label in Chip type, Ink (#0B1220, 18.6:1), from 32px; 12px right padding. Width is fitted to the label.
- **Use:** technologies on project cards and every item in the Tech stack. Chips flow left to right with 8px gaps and wrap inside their room. White is the third colour of the page: grain, type on the blue, chips, bars on the blue.

### Buttons
- **Shape:** gently rounded box (8px radius), 36px tall, width fitted to the label: 14px left pad, 16px icon, 8px gap, label, 16px right pad.
- **Primary (Résumé only):** Signal Blue fill, speckled; icon and label in Button White; label in Title (Geist 500 14px).
- **Secondary:** Raised Slate fill, Seam Steel border, icon in Key Grey, label in Console White. Profile row: Email, LinkedIn, Portfolio, Kaggle (chart icon), Medium. Per-card rows: Live site and Live demo (external-link icon), Source (the GitHub mark from Simple Icons), Contribute (users icon).
- **Hover / Focus:** none drawn. Buttons are images inside links; GitHub supplies the link focus ring. Do not simulate hover.

### More work row
- **Style:** a console panel (12px radius), Live Blue folder icon, Row title name in Console White, description in Soft Steel, language chip (right-aligned wide, below the description narrow). The whole row links to the repository.

### Tech stack panel
- **Style:** a console panel with a `r204570 / stack` title bar; six groups named in Label type Key Grey, each a flow of chips; groups divided by seams inset to the gutters. Not linked.

### Activity panel
- **Title bar:** `r204570 / activity` path; right side "Live · synced Mon D" in mono Console White led by a static Live Blue dot.
- **Chart:** 52 weekly bars from y=74 to a baseline at 190; height by square root of volume (minimum 4px); Signal Blue at 45 to 100% opacity, the peak week solid Readout Blue; zero weeks as Seam Steel stubs; 4px gaps and 2px radius wide, 1.6px gaps and 1px radius narrow; all speckled. The peak is annotated in Data small Readout Blue ("Busiest week · N contributions", narrow "N that week"), flipped to end-anchored when the peak is in the right half. Month ticks (10.5px mono Key Grey) are placed from the right edge back with a 44px (narrow 48px) minimum spacing, and "Today" closes the axis.
- **Stats:** CONTRIBUTIONS, LONGEST STREAK, ACTIVE DAYS, BUSIEST DAY: a Key above a speckled Stat number with a Unit beside it. Four columns divided by short vertical seams; 2 x 2 on narrow.
- **Feed:** "LATEST" (Label), up to three events: 16px Live Blue icon (commit, merge, dot), sentence in Value Console White truncated with an ellipsis by `fit()`, date right-aligned in mono Key Grey. Empty state: "No public events this week." in Key Grey. With no contributions at all, the chart area reads "No public activity in the last 52 weeks".
- **Status bar:** "r204570 · Ahmedabad, IN · UTC+5:30" left and "Redrawn twice a day by GitHub Actions" right, mono Key Grey (narrow keeps only the right-hand line).

### Hidden part
- **Markup:** a `<details>` block at the end of the README with a short brief and a finder count.
- **Layers:** stage 1 is the README's second HTML comment; stage 2 is an HTML comment carried only by `assets/hero.svg` (the wide hero), emitted by `hero.wide()` through `Canvas.svg(comment=...)`. Regeneration keeps it only while that argument stays in place; never strip comments when optimising SVGs, and never move the note anywhere visible.

## Do's and Don'ts

### Do:
- **Do** change colours, type and icons in `scripts/console.py` (and `SKY` in both `hero.py` and `build_assets.py`), then run both `build_assets.py` and `activity.py`; never hand-edit `assets/*.svg` (the Action overwrites the hero and activity twice a day).
- **Do** draw identity on `Canvas.grainy()` and detail on `Canvas.panel()`, at 830px with a recomposed 360px `-narrow` twin served by `<source media="(max-width: 600px)">`, on one line inside its link.
- **Do** keep each blue to its job: Signal Blue (#1F6FEB) fills and glow bodies, Live Blue (#58A6FF) state marks and icons on the console, Readout Blue (#79C0FF) blue text on the console, Electric (#1D4ED8) technology marks on the white chips, Sky (#93C5FD) anything blue on the blue.
- **Do** set type on the blue only in On-Blue White (content), On-Blue Soft (sentences) and On-Blue Label (small labels), and lay boxes on the blue as Glass with a white hairline.
- **Do** set words in Geist and data in Geist Mono, and place every string with `measure()`, `wrap()` or `fit()`.
- **Do** draw technology marks from Simple Icons in one colour, and fall back to a line icon when the mark is unreadable at 16px.
- **Do** give every image an alt that is a complete text equivalent, and keep live numbers out of README alt text (only the SVGs are redrawn).
- **Do** put links that matter in a button row under the card; an SVG cannot carry a working link.
- **Do** add any new character to `BASIC` in `build_assets.py` and rerun it before a live panel uses it.
- **Do** preview with `python3 scripts/activity.py --demo --out-dir <somewhere outside assets>`.

### Don't:
- **Don't** add a second hue: no green "online", red error or amber warning, and no brand colours on technology marks; state is blue and words.
- **Don't** fill a second button blue or make the blue surface clickable-looking; Résumé is the one blue action.
- **Don't** animate anything besides the hero's availability dot, and don't remove the reduced-motion rule from `Canvas.svg()`.
- **Don't** add drop shadows, blur or backdrop filters, or glows outside `grainy()`.
- **Don't** put console colours (Console White, Soft Steel, Key Grey, Live Blue, Readout Blue) on the blue surface, or on-blue whites on the console ground.
- **Don't** make panels transparent or draw light-theme variants; nothing swaps by theme.
- **Don't** speckle small text, secondary copy or icons.
- **Don't** put a mono uppercase label above a larger headline as a kicker; labels name fields and groups.
- **Don't** split a `<picture>` block across lines.
- **Don't** truncate a project name; shrink it.
- **Don't** put a small label at a glow's brightest point.
- **Don't** commit `--demo` output into `assets/`.
- **Don't** bring back the rejected worlds (stacked medical imaging, the cracktro title screen) or any playful costume; the register is somewhat formal.

### Known defects (recorded, not rules)
- The faintest bars fall below 3:1 non-text contrast: in the activity chart, 45% Signal Blue (about 1.7:1 on the ground) and the Seam Steel zero-week stubs (1.34:1); in the hero strip, 45% white (about 2.6:1 against the glow behind it) and the 28% zero-week stubs (about 1.85:1). The totals, stats, desc and alt carry the data, so this is tolerated; it is not a value to reuse for a mark that carries meaning on its own.
- Contrast of type on the blue was measured on rendered pixels: at the 95th percentile of the background beside the brightest-placed text (white grain specks included), L is about 0.146, where white holds 5.4:1. Any tint fell to 4.0 to 4.3:1 there, which is why every word on the blue is white. Re-measure if a glow moves closer to text or the grain gets stronger.
- This build was checked with github.com's rendered HTML for the README and the local SVGs (Edge, 900px and a 390px phone frame, both themes). The GitHub mobile app was not checked; if it ignores `<source media>`, it falls back to the wide drawings scaled down.
