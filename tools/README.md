# tools

Pipeline that turns the Australia/National (AS 1743) drawings into SVGs under `Australia/National (AS 1743)/SVGs/`.

```bash
python3 -m venv .venv && .venv/bin/pip install fonttools pillow   # once; potrace via `brew install potrace`
.venv/bin/python tools/trace_symbol.py --spec 'tools/specs/*/*.json'   # symbols from the drawings -> tools/symbols/
.venv/bin/python tools/mark_intervene.py                                # QA reports -> "intervene" fields on specs
.venv/bin/python tools/signgen.py                                       # all specs -> Processed/ (+ MANIFEST.csv)
.venv/bin/python tools/contact_sheets.py 'tools/specs/TM/*.json' /tmp/sheets   # review sheets: drawing | generated
.venv/bin/python tools/lint_specs.py 'tools/specs/[TRW]*/*.json'        # margin/gap sanity check on hand-placed text
```

| File | Role |
|---|---|
| `SPEC_GUIDE.md` | The spec format and the rules for transcribing a drawing. Read before writing or editing specs. |
| `specs/<FAMILY>/<CODE>.json` | One spec per drawing (TM, T, R, W, G, GE, MISC). `_REPORT_*.md` = transcription notes, `_QA_REPORT.md` = review results. |
| `signgen.py` | Generator. Outlines text from the FHWA fonts with AS 1744 spacing (hyphen re-spaced per the table), builds shapes, places symbols, checks stated widths (±2 %), writes `MANIFEST.csv`. |
| `trace_symbol.py` | Traces a symbol from a drawing: finds the sign's ground by colour (or the black ring on white signs), maps the spec's mm box, masks to the ground shape, upsamples, potrace, per-colour layers if asked. Options per symbol entry are listed in the guide. |
| `symbols/<id>.svg` | Traced symbol artwork in mm (viewBox = ink extent). Fill `currentColor` unless the symbol carries its own colours. |
| `contact_sheets.py` | Renders each sign beside its drawing for visual review. |
| `lint_specs.py` | Flags left-aligned lines with unequal margins or tiny gaps (catches x typos the width check cannot). |
| `mark_intervene.py` | Reads the QA reports; every `CODE — ISSUE (...)` line sets `"intervene"` on that spec. |

## Output layout (`Australia/National (AS 1743)/SVGs/`)

Family folders: Regulatory Signs, Parking Signs (R5), Speed Signs/…, Warning Signs, Temporary Signs, Guide Signs,
Service Signs (G7), Tourist Signs (G11, TRA/TRB), Freeway Signs (GE), Hazard Markers (D4). Filenames are
`<NAME>_<CODE>[(L|R)].svg` in the style of the older `SVGs/` folder.

`intervene/<family>/` holds every sign that needs a human decision: a QA ISSUE, or a stated width the fonts
cannot reproduce. The reason is in `MANIFEST.csv` (`intervene` column) and in the spec's `notes`.

SVG header matches the Illustrator speed-sign exports (`width`/`height` in mm at 72 pt/in, viewBox in points,
1 pt = 1 cm of drawn sign). No comments or metadata are written into the SVGs.

## Conventions
* One file per drawing at the illustrated size; variants only for values the drawing marks as varying (speeds,
  distances, channels) and for (L)/(R). No size-table variants.
* Nothing not on the drawing is added. Drawing dimensions that contradict AS 1744 spacing are kept as `expect`,
  flagged by the width check, explained in `notes`, and routed to `intervene`.
* Templates in `Design Templates/` supply the base geometry; their hairline keyline and `minus10` numeral tracking
  are off by default (`"keyline": true`, `"tracking": "minus10"` to enable).

## MUTCD (USA) — `USA/Federal (MUTCD 2023)/`

Source: FHWA Standard Highway Signs sheets in `USA/Federal (MUTCD 2023)/Original PDFs/` (2004 edition, 2012 supplement, 2024
releases 1–6; see `SOURCES.md` there). The sheets are vector PDFs, so the artwork is lifted exactly rather than redrawn.

* `shs_extract.py <pdf> <set> [pages]` — one sheet set: for each sign label on a page it takes the panel and every fill
  inside the panel's outline (page paint order kept), drops dimension lines, arrowheads, dimension-letter masks and
  anything outside the outline, re-outlines legends set in the embedded FHWA fonts with the repo's Series fonts (2004/2012
  sheets; the 2024 sheets are already outlined), and scales the drawing from the size table: the conventional-road row
  where the sheet marks one, else the size those editions record for the code (`shs_conventional_sizes.json`), else a
  documented default written to the manifest with "check". Left/right variants drawn as thumbnails are scaled from the
  same table; variants not drawn at all are mirrored when the sign has no legend. Signs it cannot finish (duplicate shapes
  in FHWA's drawing, legends in a font it cannot outline) go to `SVGs/intervene/`.
* `shs_run.py [sheets_dir]` — runs every set into `USA/Federal (MUTCD 2023)/SVGs/<set>/` with `_extract_manifest.csv`
  (code, name, file, drawn size, table A, page, note, panel rect) and builds review sheets.
* `shs_sheets.py` — review sheets: page crop beside the extracted SVG, 12 pairs per image, driven by the manifest.
* `shs_organise.py` — merges the sets into family folders (Regulatory, Parking, Warning, Temporary Traffic Control,
  School, Route Markers, Guide, Object Markers, Emergency Management); a code drawn in a newer edition supersedes the
  older drawing; writes `USA/Federal (MUTCD 2023)/SVGs/MANIFEST.csv` and `intervene/INTERVENE_LIST.md`.
* `corner_check.py <folder> <report.csv>` — renders every SVG on magenta and lists files whose corners are painted
  (transparency check outside rounded, diamond and octagon outlines).

Sizes: one file per drawing at the conventional-road size. Guide signs with no size table are drawn at the sheet's own
scale (1 pt = 0.1 in) and say so in the manifest.

## New Zealand — `New Zealand/National (TCD Manual)/`

Source: the NZTA sign-specifications register (Traffic Control Devices Manual), one entry per sign with an EPS drawing
(Illustrator, 1:10, legends outlined) and a dimensions/colours table. NZTA states the files may be used commercially
without approval. The site sits behind Imperva bot protection: a person passes the check once in the Browser pane, and
the tools then reuse that session cookie.

* `nz_crawl.py` — crawls the register (10 categories, 500 signs) into `REGISTER.csv` and downloads every EPS and
  non-labelled GIF into `Original EPS/<category>/`. Needs `NZTA_COOKIE` and `NZTA_UA` from the browser session.
* `nz_extract.py` — Ghostscript turns each EPS into a PDF; fills are lifted exactly and scaled ×10 to real size. Sheets
  holding several panels (assemblies, the same sign at several sizes, margin labels) are split per panel: the same
  drawing at several sizes keeps the largest and says so; anything outside a panel's outline is dropped. Output in
  `SVGs/<family>/` with `MANIFEST.csv` (drawn size beside the register's dimensions; mismatches and ignored live text or
  strokes are noted).

Fonts (TCD Manual Part 1 §5.3.1): AS 1744 Series A–E and modified E lower case, plus "Transport Medium NZ" for parking
sign text and metric abbreviations. The EPS legends are already outlined, so no font is needed to reproduce them.

## State registers — `tools/sheet_extract.py`

Generic extractor for CAD-style sign design sheets (NSW design plans, QLD TC signs): Inkscape converts every glyph to a
path (the embedded sign fonts are the authority for the letterforms), the original PDF's text says where the title
block, notes and dimension figures are, and fills are clustered into drawings, cleaned of annotations, scaled from the
sheet's stated size / dimension / table / scale, and written with the usual header. Line-drawn sheets get white panels
from closed outlines, thick strokes become bands, triangulated CAD exports are unioned (Shapely), sideways sheets are
turned upright. Text merged into one path by the converter is split back into its marks (annotation glyphs dropped,
holes kept with their shape), arrowheads and ticks at the panel edge are dropped, and a drawing that fills most of the
sheet is told from the sheet frame by its margins. Drivers: `qld_extract.py` (TC sign categories →
`Australia/QLD/SVGs/<Category>/`), `nsw_extract.py` (register → `Australia/NSW/SVGs/<family>/`), `sa_extract.py`
(register sizes; 60% grey rendered white), `ca_extract.py` (Caltrans two-tone sheets recoloured from their COLORS note,
sizes from the SIGN SIZE table; scanned sheets listed without files). Review sheets: `pack_sheets.py <pack> <out>`
(sources may carry `#page=N`).

### Texas — `tools/tx_extract.py`

TxDOT's SHSD 2012 sheets follow the FHWA SHS layout, so the MUTCD extractor runs with Texas code patterns and family
rules (CW → temporary traffic control, SW → school, TX → guide, RS- → `Symbols and Arrows`). Legend text in fonts the
repo has no outlines for (Clearview, Highway *Plus) is outlined from the sheet's embedded font programs
(`shs_extract.embedded_legend`, via `nz_extract.glyph_items`); only fonts the sheet does not embed go to `intervene/`.
