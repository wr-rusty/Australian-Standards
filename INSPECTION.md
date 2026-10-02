# Inspecting a sign pack

For the person checking generated signs before a pack moves from `Processing/` to `Complete/`. One inspection
ticket exists per pack (area `qa`, title "Inspect …"); record findings in that ticket's Log, do not fix silently.

## What you are checking

Every SVG must be the sign its source says it is: right shape and size, border and edge widths, colours, legend
wording, letter series and height, position of every line and symbol, nothing extra, nothing missing, transparent
outside the sign outline.

| Pack type | Source to compare against | Where |
|---|---|---|
| Spec-driven (AS 1743, NSW, QLD, SA, TAS, NT) | the standard drawing / design sheet | `<pack>/Original PNGs/<code>.png` (or `Original PDFs/`) |
| Converted official artwork (UK, France, Germany, NZ, US federal) | the authority's own artwork | `<pack>/Original EPS|SVG|PDFs/…` |

Each pack's `SVGs/MANIFEST.csv` (or `SVGs (generated)/MANIFEST.csv`) has one row per sign: code, file, size, a
`check` column (width mismatches against the drawing), and `notes` saying what was read from the sheet, what was
decided, and what disagrees. Rows with no file are skips; the reason is in the row.

## How

1. Open the pack's contact sheets (one image per family; ask for them to be rendered if missing) and scan for anything
   that looks wrong: cut-off text, legend touching a border, missing border, filled-in symbol holes, stray marks,
   a white box behind a non-rectangular sign.
2. For each sign in doubt, and for a sample of at least one in ten otherwise, lay it over its source:

   ```bash
   python3 tools/compare_drawing.py out.png CODE            # AS 1743 and state packs; CODE=value for variants
   python3 tools/compare_drawing.py out.png "CODE@0,0,0.4,0.3"   # zoom on a corner to judge border widths
   ```

   Green = generated and drawing agree, red = drawing only, blue = generated only. A dashed "varies" placeholder on
   the drawing will show as a mismatch; that is expected.
3. Read the manifest notes for that sign. A note that says the sheet and the font disagree, or that a value was
   assumed, is a decision to confirm, not a defect.
4. Variants: where the sheet says "insert appropriate value", the generated values are the sheet's example plus
   values in common use. Confirm they are real values for that jurisdiction; say which to drop.

## What to record

In the inspection ticket's Log, one line per finding: `CODE — what is wrong — what the source shows`. Then one of:
**fix** (the SVG disagrees with its source), **decide** (the source is ambiguous or wrong; Russell decides),
**ok as noted** (the manifest note already explains it). Finish with the count inspected, the count sampled by
overlay, and whether the pack can move to `Complete/`.

## Not defects

* The SVG header: `width`/`height` in mm are the viewBox in points × 25.4/72, viewBox 1 pt = 1 cm of sign, one
  `<g transform="scale(0.1)">`. This matches Russell's Illustrator exports and is deliberate.
* No size variants: one file per sign at the illustrated size.
* Guide and Freeway families are excluded on purpose; example and site-specific sheets are skipped on purpose.
* State packs hold only state-specific signs; a code that exists in the national pack is a manifest pointer, not a file.
