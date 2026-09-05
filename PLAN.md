# Plan: generate every sign variation in Australia/National (AS 1743) (and Australia/National (AS 1319))

Written 2026-09-04 after a full survey of the repo. This is the working plan for
producing a dimensionally correct SVG for every sign drawing in the standards,
in every size and handedness variant the standard lists.

---

## 1. What the repo contains today

| Area | Contents | Notes |
|---|---|---|
| `Australia/National (AS 1743)/Original PNGs/` | 873 PNGs | Dimensioned construction drawings from Australia/National (AS 1743), one per code (e.g. `TM2-4A.png`). ~753 px wide, dimensions legible. These ARE the "how to make" instructions. |
| `Australia/National (AS 1743)/SVGs/` | 78 SVGs | Hand-built in Illustrator. Text outlined to paths. Not at mm scale (e.g. a 600 mm sign is 64 units wide). Named descriptively, not by code. |
| `Australia/National (AS 1319)/Original PNGs/` | 57 PNGs | Mostly small raster pictograms (223 px), plus layout-rule figures (D1–D6), colour chart (A1), and shape figures. No per-sign dimensioned drawings. |
| `Australia/National (AS 1319)/SVGs/` | 16 SVGs | Danger / Prohibition / Safety text signs built from the three templates. |
| `Australia/National (AS 1744)/Australia/National (AS 1744).txt` | Text of the alphabet standard | Contains the six spacing tables (Series B, C, D, E, E Mod, F) at 100 mm cap height. |
| `Fonts/fhwa-series-font-family/` | 78 OTFs | FHWA Series B–F + E Modified, 13 tracking variants each (`minus100` … `plus0` … `plus100`). `plus0` matches the AS 1744 tables exactly (verified, see §3). |
| `Fonts/PragmaticaCTT-Bold/` | 4 TTFs | Helvetica-style face used for the AS 1319 signs. |
| `Design Templates/` | 5 SVGs | Speed sign, speed-with-text, Danger, Warning, Prohibition templates. |

There is no README, manifest, or code→filename mapping. Fonts are not installed
system-wide, so `<text>` elements do not render outside Illustrator; that is why
the existing SVGs outline text, and the generator will do the same.

### Classification of the 873 AS 1743 drawings

| Family | Count | What it is | In scope? |
|---|---|---|---|
| TM1–TM10 | 199 | Temporary (roadwork) signs, mostly text on yellow, some arrows/symbols | Yes |
| G1–G11 | 187 | Guide / direction signs (green, brown, blue, white). Multi-panel, mixed series, lower case E Mod, route shields, arrows | Yes, hardest |
| R1–R9 | 153 | Regulatory (stop, give way, speed, parking, no entry, etc.) | Yes |
| W1–W9 | 139 | Warning diamonds and supplementary plates (W8) | Yes |
| T1–T8 | 65 | Temporary signs, larger format (e.g. T1-1 ROADWORK AHEAD 1800×600) | Yes |
| GE1–GE11 | 52 | Freeway / expressway guide signs, service signs | Yes |
| S1–S27 | 24 | Symbol outlines on a grid (cross, tent, etc.). Components, not signs | Yes, as a symbol library |
| D4-x | 8 | Hazard markers, chevrons, diagonal stripes | Yes |
| RM / WM / GM | 17 | Regulatory/warning/guide variants for specific uses (e.g. RM2-4A No Entry 600×600) | Yes |
| TS1–TS7 | 7 | Tourist symbol outlines on a grid | Yes, symbol library |
| MS01–MS03 | 3 | Misc symbols on a grid (EV charging car) | Yes, symbol library |
| TRA | 1 | Tourist route marker emblems TRA/TRB with a 5-size table | Yes |
| 3-1…3-6, 4-1 | 8 | Figures: symbol-evaluation flowchart, arrow proportions, grid geometry | No (reference only) |
| A1, B1, B2, C2a/b, D1, D2, E1, E2 | 9 | Test forms, guide-sign anatomy, layout figures | No (reference only) |

Roughly 830 of the 873 drawings are signs or symbols to produce. Each sign
drawing typically carries a "Sign sizes, mm" table with 2–4 sizes (A/B/C/D) and
some have (L)/(R) mirrors, so the finished set will be on the order of
2,000–2,500 SVG files.

---

## 2. What counts as "a variation"

One output file per combination of:

1. **Code** (e.g. `W1-1`)
2. **Size letter** from the drawing's size table (A/B/C/D…). The illustrated size is marked "(Illust.)".
3. **Handedness** (L)/(R) where the drawing shows or names both.
4. **Legend value** where the drawing says "Varies" or "Variable" (speed numerals 5–130, km/h plates, TRB numerals 1–9, etc.). Generate the standard set, e.g. speeds 5,10,20,…,130.

Naming: `<code><size>(<hand>)[_<value>].svg`, e.g. `W1-1B(L).svg`, `R4-1B_60.svg`,
`TM2-4A.svg`. Existing descriptive names are preserved through a mapping column
in the manifest, not by renaming.

---

## 3. Toolchain (verified 2026-09-04)

| Tool | Status | Role |
|---|---|---|
| Python 3.14 + venv with `fonttools`, `pillow` | Works | Generator: outline text from the OTFs, emit SVG |
| Inkscape 1.4.3 CLI (`/Applications/Inkscape.app/Contents/MacOS/inkscape`) | Works | Render SVG→PNG for verification; bitmap tracing |
| `potrace` (via `brew install potrace`) | Not yet installed | Trace symbol grids to vector |
| Adobe Illustrator 2026 | Installed | Manual cleanup of traced symbols only |

**Font facts that drive the generator**

- Units per em 10000, cap height 8000. To set letters at height H mm, scale glyph units by `H / 8000`.
- The `plus0` tracking variant reproduces the AS 1744 spacing tables. Proof: TM2-4A "ROAD" at 110 C computed 303.7 mm ink width (drawing: 303); "CLOSED" 451.2 mm (drawing: 450). Other variants (`minus10`, `plus10`…) change advance widths only; use them only where a drawing says "medium/condensed spacing".
- Every AS 1743 dimension line that spans a word is therefore a free automated check.

**Colours in use** (keep these unless Russell decides otherwise):

| Use | Hex | Seen in |
|---|---|---|
| Red annulus / regulatory | `#ed1c24` | speed signs, No Entry |
| Yellow ground (temporary / warning) | `#ffe40d` | ROADWORK signs |
| Orange ground | `#f58020` | Safety station |
| Green ground (guide) | `#0b804c` | existing guide-style signs |
| Blue ground (service / info) | `#3a53a4` | TOILET_BLUE |
| Brown (tourist) | not yet used | needs a value, propose `#754c24` |
| Black / white | `#000` / `#fff` | |

---

## 4. Phases

### Phase 0 — Scaffolding (half a day)

- Add `tools/` (generator scripts), `specs/` (one YAML per drawing), `symbols/` (vector symbol library), `generated/` (output, mirrored family folders), `manifest.csv`.
- Adopt **1 SVG unit = 1 mm**, `width`/`height` in mm, `viewBox` at real size. This differs from the existing Illustrator files; they stay untouched until Phase 7.
- Commit the Python requirements and a `Makefile`/script that runs generate → render → contact sheet.

### Phase 1 — Inventory (the long manual read)

Build `manifest.csv` with one row per drawing:

`code, family, kind (sign|symbol|figure|composite), illustrated_size, size_table, hands, ground_colour, legend_colour, border, corner_radius, lines (text|series|height), symbols_used, grid_unit_mm, varies_fields, existing_svg, notes`

Method: read PNGs in batches of ~10 with vision, transcribe dimensions. Run
4 parallel agents split by family (TM+T, R+RM+D4, W+WM, G+GE+GM+TRA). Each
agent writes its rows to a family CSV; merge at the end. Budget: ~85 batches.

Deliverable: the complete list of variations (the number the rest of the plan
is measured against) and every drawing tagged with its symbol dependencies.

### Phase 2 — Spec schema and generator

A drawing becomes a small YAML spec. Example for TM2-4A:

```yaml
code: TM2-4A
shape: rect
size: [600, 600]
sizes: {A: [600, 600]}
ground: "#fff"
border: {width: 25, colour: "#000"}
lines:
  - {text: ROAD,   series: C, height: 110, top: 130, expect_width: 303}
  - {text: CLOSED, series: C, height: 110, top: 360, expect_width: 450}
```

Generator features, in build order:

1. Shapes: rounded rect, diamond (rotated square with R50 corners), circle,
   octagon (R1-1), triangle (R1-2), pentagon shield (G8-9, TRA), stripe
   boards (D4-3), multi-panel guide boards with edge strip and panel corners.
2. Borders: solid border inset, white edge strip + inner border (guide signs).
3. Text: series B/C/D/E/Emod/F, per-line height, centred or left/right aligned,
   colour, optional tracking variant, `expect_width` assertion.
4. Symbols: place a library symbol by grid unit (`50 □ 50` means one grid
   square = 50 mm) at a given anchor; mirror for (R).
5. Numerals: speed annulus (R4-1 style) with numeral series rule
   ("2 numerals plus 110 → 240 D, 3 numerals → 240 C").
6. Size variants: scale the illustrated design by the size ratio, then snap
   letter heights to the nearest AS 1743 standard height and re-centre; flag
   in the manifest when the drawing gives per-size letter heights instead.
7. Output: text outlined to `<path>`, one `<g>` per element with `id`s, mm
   units, no Illustrator cruft. Also emit a PNG preview.

### Phase 3 — Symbol library

Sources: S1–S27, TS1–TS7, MS01–MS03 (whole drawings), plus the small grid
insets inside sign drawings (arrows in W1/TM5/TM10/G9, bicycle in GM9-58A,
telephone in GE7-8, chevrons, etc.). Estimate 90–110 symbols.

Process per symbol:

1. Crop the grid region from the PNG (Pillow), count grid squares, read the
   grid unit from the "N □ N" legend.
2. Threshold, flood-fill the outline interior, `potrace` to SVG.
3. Normalise: translate to origin, scale so one grid square = 1 unit, store as
   `symbols/<id>.svg` with a `data-grid-mm` attribute holding the native mm.
4. Review each traced symbol against the drawing; hand-fix in Illustrator
   where tracing rounds corners (expect ~30 of them). Arrows with stated
   geometry (D4-x, 4-1 arrow proportions, G9-7 R14/R16/R33) should be drawn
   parametrically from the dimensions instead of traced.

### Phase 4 — Generate by family, easiest first

| Step | Families | Approx drawings | Needs |
|---|---|---|---|
| 4a | TM1, TM2, TM3, TM8, TM9, T1–T8 text-only, R5/R6/R7/R9 text, W5 text diamonds, W8 plates | ~380 | Phase 2 items 1–3 |
| 4b | R4-1 speeds, W8-2 km/h, TM4 speeds, TRB numerals, "Varies" fields | ~40 codes, ~300 files | Phase 2 item 5 |
| 4c | W1–W4, W6, W7, TM5, TM10, R2, R3, D4, RM, WM | ~200 | Phase 3 symbols |
| 4d | G1–G11, GE, GM, TRA route shields | ~245 | Multi-panel layout, E Mod lower case, shields, arrows |
| 4e | Size variants for everything above | ×2.5 | Phase 2 item 6 |

Each step ends with the verification loop in Phase 5 before moving on.

### Phase 5 — Verification loop (runs after every batch)

Automated, per file:

- Overall width/height equals the size table.
- Every `expect_width` (dimension line spanning a word) within ±2 mm.
- Symbol bounding box matches the grid extents from the drawing.
- SVG parses; no `<text>` elements remain; no fonts referenced.

Visual, per batch of 12:

- Render generated SVG with Inkscape, composite next to the original PNG
  (contact sheet), review by eye. Record `status` in the manifest:
  `draft | verified | needs-manual | blocked`.

### Phase 6 — Australia/National (AS 1319) (different model)

AS 1319 gives rules, not drawings: shape proportions (D1), layout ratios in
terms of letter height H (D2–D6), colours (A1), and 50-odd pictograms as low
resolution rasters (tB1–tB4 = the tables of prohibition, mandatory,
restriction, hazard, emergency and fire pictograms).

- Redraw each pictogram as clean vector (the 223 px rasters are too coarse to
  trace well; use them as reference and draw geometrically, or source ISO 7010
  equivalents where the pictogram is identical).
- Encode the 7 sign categories (Prohibition, Mandatory, Restriction, Hazard,
  Danger, Emergency, Fire) as parametric templates driven by H, matching the
  D1–D6 ratios. The three existing templates become instances of these.
- "Every variation" here = every pictogram × its category template, plus the
  wording signs already made. Wording is open-ended, so the generator takes a
  wording list (start with the 16 already produced).

### Phase 7 — Reconcile the 94 existing SVGs

- Map each existing SVG to a code in the manifest (obvious ones: `STOP_SIGN`
  = R1-1, `Normal Speed Signs/*` = R4-1, `ROADWORK_YELLOW_SQUARE` = TM1-1A,
  `ROADWORK_YELLOW_LONG` = T1-1, `NO_ENTRY` = RM2-4A/R2-4, `DETOUR_*` = TM5-1B).
- Regenerate them at mm scale from specs; keep the old files in place until
  the regenerated version is `verified`, then decide whether to replace or
  keep both (recommend: keep descriptive filenames as symlinks/copies of the
  code-named output so nothing downstream breaks).

---

## 5. Decisions for Russell

1. **Units**: switch all new output to 1 unit = 1 mm (recommended). Yes/no.
2. **Naming**: code-based filenames for generated output, descriptive names kept via the manifest (recommended).
3. **Size variants**: produce all listed sizes (recommended; nearly free once a spec exists) or only the illustrated size.
4. **Guide-sign legends**: reproduce the example legends exactly as drawn ("Liverpool", "Heathmont"…) for the standard set, with the generator able to take custom legends later (recommended).
5. **Brown and any missing colour values**: confirm hex values (table in §3).
6. **Figures** (3-x, 4-1, A1–E2): leave out of generation (recommended).
7. **AS 1319 pictograms**: redraw by hand vs. adopt ISO 7010 vectors where identical.

---

## 6. First three sessions

1. **Session 1**: Phase 0 scaffolding; install `potrace`; move the proof-of-concept generator (`TM2-4A`) into `tools/`; generate TM2 as a whole family (54 drawings, all text-only) end-to-end with the verification loop, to shake out the schema.
2. **Session 2**: Phase 1 inventory for TM + T + R families in parallel agents; start the symbol library with the arrows (parametric) and S1–S27.
3. **Session 3**: Inventory W + G + GE; generate 4a and 4b; contact-sheet review.

Effort guide: inventory ≈ 85 vision batches; symbol library ≈ 100 symbols
(≈ 30 hand-fixed); generation is scripted; verification ≈ 200 contact sheets
for ~2,300 files. Realistically 8–12 working sessions to reach a verified set
for AS 1743, then 2–3 for AS 1319.

---

## Status (updated 2026-09-04, evening)

* Phases 0–4 done for AS 1743: every drawing has a spec (`tools/specs/`), 261 symbols traced, ~1,265 SVGs generated
  into family folders, 68 non-sign drawings skipped and accounted for in the manifest.
* Rules changed from the original plan at Russell's direction: no size variants (only legend/hand variants), output
  grouped by family under `SVGs/`, header format = the speed-sign Illustrator exports, no metadata in SVGs,
  signs needing a decision go to `SVGs/intervene/`.
* Phase 5 (QA) done for every family (2026-09-05): 1,196 clean files; 50 drawings in `SVGs/intervene/` (see `INTERVENE_LIST.md` there).
* Arrows drawn geometrically (2026-09-05); Guide and Freeway families excluded from generation at Russell's request
  (specs kept); all intervene items accepted.
* TODO — AS 1319 (paused 2026-09-05): pictograms traced to `tools/symbols/as1319/` (31, from the standard's small
  rasters), generator drafted in `tools/as1319.py` (H/D rule layouts, DANGER header per C1, figure 3.1 arrows); specs
  not yet written; Russell's camera/video symbols still to be lifted from his NO_PHOTO/NO_VIDEO SVGs. Resume by writing
  `tools/specs/AS1319/*.json` and comparing against his 16 existing SVGs.
* International: see `International/REVIEW.md` (USA first, then NZ, then UK).
  * USA (2026-09-05): FHWA Standard Highway Signs sheets (2004 edition, 2012 supplement, 2024 releases 1–6) downloaded to
    `USA/Federal (MUTCD 2023)/Original PDFs/`; artwork lifted exactly from the vector PDFs by `tools/shs_extract.py` (see `tools/README.md`),
    organised into family folders under `USA/Federal (MUTCD 2023)/SVGs/` with `MANIFEST.csv`. Newer edition supersedes older for the same
    code. Open for Russell: manifest rows noted "check" (size row chosen by rule where the 2024 tables have no
    conventional-road marker), guide signs drawn at sheet scale (no size table), and `SVGs/intervene/INTERVENE_LIST.md`.
  * NZ (2026-09-05): NZTA sign-specifications register crawled with `tools/nz_crawl.py` (Russell passes the site's
    Imperva check once in the Browser pane; the tools reuse that session) into `New Zealand/National (TCD Manual)/` (`REGISTER.csv`,
    `Original EPS/`); `tools/nz_extract.py` lifts the EPS artwork (1:10, legends outlined) into `SVGs/<family>/` with
    `MANIFEST.csv`. Fonts per TCD Manual Part 1 §5.3.1: AS 1744 Series A–E + modified E lower case, Transport Medium NZ
    for parking text and metric abbreviations (not needed: legends are outlined).
  * TODO — UK after NZ.
* TODO — reconcile the old `SVGs/` folder against the generated set.
* Layout (2026-09-06, agreed with Russell): country → jurisdiction pack → `Original …/` + `SVGs/<family>/`:
  `Australia/National (AS 1743)`, `Australia/<State>` (all eight states/territories, P1), `USA/Federal (MUTCD 2023)`,
  `USA/<State>` (major states first, minor states as tickets), `New Zealand/National (TCD Manual)`, `UK/<Region>`.
  Work is tracked in `Tickets/` (`python3 Tickets/tk.py list`, Akimbo format); Linear is not used.
