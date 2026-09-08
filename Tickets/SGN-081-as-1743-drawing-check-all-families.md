---
id: SGN-081
title: AS 1743 drawing check: all families
status: open
priority: P1
area: content
project: none
created: 2026-09-08
updated: 2026-09-08
source: manual
---

## Summary

Every generated AS 1743 sign (R, W, TM, T, GE/D4, MISC; G excluded by decision) was laid over its standard drawing
(`Complete/Australia/National (AS 1743)/Original PNGs/<CODE>.png`) with `tools/drawing_check.py` (whole family, ranked
by differing ink) and `tools/compare_drawing.py` (single sign, zoom overlays). Real mismatches were traced back to the
drawing, the spec corrected with a dated note, the SVG regenerated and re-checked. This ticket is the complete record
of the check (part 1 = R and W, committed as "AS 1743 drawing check (part 1)"; part 2 = TM, T, GE, MISC and the
spot-checks below).

## Evidence

- Overlays: red = drawing only, blue = generated only, green = both. Score = differing ink / drawing ink, ignoring
  differences within 2 px. Dashed "Varies" placeholders, traced symbols and letter weight inflate the score, so the
  ranking was read by a person; anything above ~0.15 was looked at, and the questionable ones measured in mm
  (ink extents of each text line, band widths along a row, polygon edges row by row).
- Drawings' PNGs are 0.44 px/mm for most signs (one pixel = 2.3 mm), so offsets under ~5 mm are within the scan.

## Findings

### The border finding (applies to R and W)

On the drawings the "30" beside the border of a white regulatory sign (and the "30" on the yellow warning
diamonds) is the distance from the sign edge to the *inside* of the border: 10 white (or yellow) edge + 20 black
border, not a 30 border. Verified by zoom overlay on R9-8 and R2-10 (exact match) in part 1, and in this pass on
three warning diamonds by direct pixel measurement of the black band on a row at 25 % height (perpendicular
widths): W2-1 19.2 mm (spec 20), W5-20 19.2 (spec 20), W6-8 14.5 (spec 15, the 636 size drawn "23" = 8 + 15).
The manual tip overlays (drawing tip box from the yellow extent, R50 tip pull-in r(sqrt2-1)) show the generated
black band on the drawing's, green all round. ~200 specs changed 30 -> 20 in part 1 (dated note in each); W4-6
(no PNG of its own, taken from the W4-4 drawing) was still 30 and was changed to 20 in this pass.

### Per family

**R (regulatory, incl. RM and R5 parking)** — 168 specs, 159 generated, 158 compared, 1 not comparable
(R9-3A: no drawing). Scores: 28 at <= 0.05, 95 at 0.05–0.15, 35 above 0.15.
Corrected (part 1): border 30 -> 20 across the family (see above); R4-10 ring centre 287; R4-13 ring at 272;
R9-8 road name in Series C; RM4-1A and RM4-12D 3-digit numerals in Series C.
Remaining above 0.15 (from the part-1 run, not re-examined one by one in this pass): R2-3(R) 0.92 and R3-5(R) 0.91
(the (R) hand compared against a drawing that shows the (L) panel only or the other panel — detection, not the
sign); speed signs R4-1, R4-10, R4-11, R4-12, R4-13, R4-14, RM4-1A and the numeral plates R9-7-1, R9-7-2, R9-6-2,
R7-12, R6-16, R9-11-2, R6-4 (dashed "Varies" numerals in the drawing vs a real numeral); R6-25/R6-26 crossbucks
(rotated text on a red ground); the R5 parking plates (dense small text, letter weight); R7-2/R7-4/R7-6-x
(letter weight on 3:1 plates). None of these showed a border, series or placement error when the part-1 worst
sheet was read; they are listed so the next pass knows where the residue is.

**W (warning)** — 145 specs, 140 generated, 139 compared, 1 not comparable (W4-6, no PNG; drawn from W4-4).
Scores: 2 at <= 0.05, 26 at 0.05–0.15, 111 above 0.15 — but the family score is not meaningful: the diamond
locator in `compare_drawing.panel_box` misplaces nearly every yellow diamond (the same-coloured edge strip and
the symbol wedges confuse the ground box), so almost all diamonds land at 0.2–0.4 regardless of correctness.
The three diamonds measured by hand (above) match exactly. Detection failure, recorded below.
Corrected: border 30 -> 20 (part 1, whole family); W4-6 30 -> 20 (this pass).

**TM (temporary, multi-message)** — 204 specs, 199 generated and compared, 0 not comparable.
Scores before this pass: 174 at <= 0.05, 15 at 0.05–0.15, 10 above 0.15. Borders (25 black on yellow) measured
25 on every TM drawing (part-1 band scan). Corrected in this pass, all re-checked at 0.000–0.018 afterwards:
- TM1-50A WATCH FOR WANDERING ANIMALS: tops were 80/240/400 (the drawing's 80s read down from the top edge and
  sum to 580); the drawn lines measure 98/259/420, so the stack reads up from the 100 bottom margin: tops
  100/260/420.
- TM1-44C BURNING OFF AHEAD: AHEAD was Series E (expect 792); the drawn AHEAD measures 668 = 155 D, matching the
  drawing's "155 D" label — the 792 figure is the typo. Series D, expect 667.
- TM8-6A LOOK BOTH WAYS: LOOK was Series D (expect 322); the drawn LOOK measures 275 = 100 C, matching the
  drawing's "100 C" label — the 322 figure is the typo. Series C, expect 275.
- TM5-11C(L), TM5-11C(R), TM5-12C(L), TM5-12C(R) DETOUR FOR HEAVY/HIGH VEHICLES: the chevron was drawn with its
  notch at x 190 and vertical arm-end cuts at x 329. The drawing's chevron has parallel arm edges (both slope
  139:253) and horizontal end cuts at y 47 and 553; "75 | 115 | 139" is tip x 75, outer arm corner x 190, arm end
  x 329 (the arm is 139 thick horizontally), so the notch is at x 214. Polygon (75,300) (190,47) (329,47)
  (214,300) (329,553) (190,553), mirrored for (R).
Remaining above 0.15, all explained and left as they are: TM1-36B (0.33), TM1-28B (0.26), TM4-8B (0.19),
TM3-16-1A (0.14) — the drawing's dashed "Varies" box is wider than the real numeral, and the line is centred as a
whole per the drawing's "=" margins, so the fixed words shift by 15–20 mm against the drawing (overlay at the
drawing's own value confirms: TM1-36B=200, TM1-28B=2); TM2-17C END ROADWORK (0.17): ROADWORK's ink is drawn 10 mm
right of centre in the drawing while its width matches (1048) and the drawing states 77 | 1045 | 78 — draughting,
spec kept centred; TM9-2A EVENT and TM1-10A HAZARD: 8–9 mm right in the drawing, widths match — same; TM8-2B(L)/(R)
(0.15): letter weight only, line extents match within 3 mm.

**T (temporary, single)** — 67 specs, 65 generated and compared, 0 not comparable after the detector fixes.
Scores after this pass: 59 at <= 0.05, 3 at 0.05–0.15, 3 above 0.15. Borders measured 25 throughout.
No spec corrected. Remaining above 0.15: T1-29 (0.25), T1-16 (0.18), T1-28 (0.16) — dashed "Varies" numeral,
as for TM. Verified by measurement rather than overlay: T5-7 chevron marker (drawing height given as a range
1140–1200; the drawn stack on the centre column is 130 | 77 | 115+56+115 | 77 | 50 | 77 | 115+56+115 | 77 | 130
= 1198, the spec within 3 mm; the sign's pixel box is pinned in the spec as `panel_px` because the locator
cannot find it, and the overlay then scores 0.013).

**GE (hazard markers D4 and tourist emblems; GE*/GM* guide and freeway signs are excluded from generation)** —
72 specs, 11 generated, 10 compared, 1 not comparable (TRB: its drawing is the TRB emblem on TRA.png; no
`drawing` hook for AS 1743 specs yet).
Scores after this pass: 8 at <= 0.05, 1 at 0.05–0.15 (TRA 0.081), 1 above 0.15 (D4-7).
Corrected: D4-3 (diagonal stripes, L/R): the spec had three 64-mm black bands with 128 mm of white between them,
phased from x 34.08 on the top edge. The drawing (rows 3/150/225/300/440/447 measured) has equal 64 black / 64
white stripes (pitch 181 horizontal) with a stripe's upper edge meeting the left edge at y 71 (the drawing's
"71"), which also leaves two small corner triangles (top-right, bottom-left, mostly under the R25). Rewritten as
five polygons from the bands; re-checked at 0.024.
Remaining: D4-7(L) (0.41): the "65" is a dashed placeholder and the km/h slash glyph in the FHWA E-modified font
sits differently from the drawing's; the chevron matches. TRA (colour fit, ~0.08): shape and arrow match; the
drawing's white rim looks ~3 mm narrower than the spec's 8.67 inset but the fit is only good to ±3 mm — unsure,
left as drawn (the drawing's "8" agrees with the spec).

**MISC** — 51 specs, all `skip` (symbol sources S*, TS*, MS*, figures, tables). Nothing generated, nothing to check.

### Detection failures and tool changes (tools/compare_drawing.py)

- Diamonds: `panel_box` misplaces yellow diamonds (W family) — the family score is unusable for diamonds; the
  border check for W was done by direct band measurement and the manual tip overlay script instead. Open.
- Handed pair PNG: `drawing_for` preferred CODE.png over CODE(L,R).png, so T5-1(L,R) was compared with the
  straight-arrow T5-1.png. Fixed: a PNG named for the hands wins (T5-1(L) now 0.000).
- Coloured grounds cut into wedges by big black symbols (T5-4, T5-5, T5-7): the ground box was a wedge. Fixed:
  when the ground box's aspect is off by > 10 %, the black border band, else the drawing's thin outline, boxes the
  sign (T5-4 0.000, T5-5 0.000). T5-7 (no border, no outline) is pinned with `panel_px` in its spec.
- Striped white signs (D4-3, D4-5-1): `outline_box` rejected the outline as not hollow (stripes joined to it) and
  kept only the first 24 long columns (all inside the first stripe). Fixed: hollowness 0.5 -> 0.8, extreme 12 + 12
  long runs, minimum outline width 0.25 -> 0.1 of the image (a narrow panel on a two-hand drawing). D4-5-1 0.026,
  D4-3(L) 0.024.
- Transparent grounds (TRA): no outline to find. Added `colour_fit` (bbox of the sign's biggest coloured element
  in the drawing and in a trial render); `panel_box` skips the outline search for ground "none" so a table cell on
  the sheet is not taken for the sign.
- Still failing: R2-3(R) and R3-5(R) (the drawn hand's panel choice on a one-panel drawing); TRB (no drawing
  hook); all W diamonds (above).
- Hazard for anyone regenerating single specs: `signgen.py` rewrites the pack's MANIFEST.csv with only the rows
  of the current run. The rows of the 10 regenerated signs were merged back into the saved 1306-row manifest with
  a scratch script; a merge (or a full rerun) is needed after every partial regeneration.

## Fix

Spec corrections above (dated notes in each spec's `notes`), SVGs regenerated for TM1-50A, TM1-44C, TM8-6A,
TM5-11C(L/R), TM5-12C(L/R), W4-6, D4-3(L/R); MANIFEST.csv rows refreshed for those; detector changes in
`tools/compare_drawing.py`.

## Verify

- `python3 tools/compare_drawing.py out.png TM1-50A TM1-44C TM8-6A "TM5-12C(L)" D4-3 T5-4 T5-5 T5-7 "T5-1(L,R)" TRA`
  — every strip green with scores under 0.03 (TRA ~0.08).
- `WORST=12 python3 tools/drawing_check.py out T` and `... GE` — the only entries above 0.15 are the "Varies"
  placeholders (T1-29, T1-16, T1-28, D4-7) and TRA's colour fit.
- Open: a diamond locator (or a `panel_px` per W drawing) so the W family can be scored; a `drawing` hook for
  TRB; the R2-3(R)/R3-5(R) panel choice.

## Log

- 2026-09-08 — filed. Part 1 (R, W border finding, R4-10/R4-13/R9-8/RM4 fixes) committed as "AS 1743 drawing
  check (part 1)"; part 2 (TM, T, GE, MISC, W spot-check, detector fixes) done, not committed.
