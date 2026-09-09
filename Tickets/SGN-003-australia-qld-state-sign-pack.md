---
id: SGN-003
title: Processing/Australia/QLD: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Processing/Australia/QLD/` with the QLD-specific signs (those not in AS 1743, or drawn differently) from TMR Queensland MUTCD Q-series and TC signs. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.tmr.qld.gov.au/business-industry/Technical-standards-publications/TC-signs — full collection ZIP (188 MB), updated quarterly; site refuses scripted requests (403), download through the Browser pane

## Fix

Download the register into `Processing/Australia/QLD/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-05 — status → in-progress.
- 2026-09-06 — TC signs collection (June 2026, 1,173 sheets) downloaded; `tools/qld_extract.py` produced 790 SVGs in 36 category folders (`Processing/Australia/QLD/SVGs/MANIFEST.csv`: 264 sheets have no readable size and are drawn at 1:10 with a check note; 19 sheets superseded or without a drawing). Q-series (488-page book) not yet extracted.
- 2026-09-06 — Q-series book (q-series.pdf, 488 pages, one sign per page with a TC-style title block): codes like D4-1-1-Q03, G9-Q14_7, GE9-Q02, W5-Q07; the extractor's frame filter took the sheet frame on many pages (fixed: a closed outline covering half the drawing area is the frame). Driver still to write: iterate pages, code regex `[A-Z]{1,3}\d{0,2}(-\d+){0,3}-Q\d+(_\d+)?`, name from the title block.
- 2026-09-06 — Q-series book extracted page by page: 645 SVGs in `Processing/Australia/QLD/SVGs/Q-Series/` (28 index/notes pages skipped, 13 pages without a drawing). Multi-page PDFs are now split per page before Inkscape converts them.
- 2026-09-06 — Rerun with the union/legend fixes (1,291 SVGs); no codes shared with the national pack.
- 2026-09-09 — Spec-driven rebuild started (the NSW way). Dedupe first: `tools/dedupe_pack.py` against the national pack removed 0 SVGs (0 codes shared; the TC / Q-series codes are all QLD-only), 1,291 extraction SVGs kept. `PACKS["QLD"]` added to `tools/signgen.py` (out `SVGs (generated)`, png `Original PNGs`, pdf `Original PDFs`, no register, credit "© State of Queensland (Department of Transport and Main Roads), CC BY 4.0" per SOURCES.md); AS 1743 output proven unchanged (R1-1 regenerated, empty git diff). Regulatory-family sheets rendered upright at 200 dpi into `Original PNGs/<CODE>.png` (86 Q-series R/RM/RX pages named by code, 26 TC regulatory sheets with `_p2`… for later pages; 131 files, 34 MB) — the other families are not rendered yet. Specs in `tools/specs/QLD/`: 77 (51 signs built, 26 skips). Generated 150 SVGs (`SVGs (generated)/MANIFEST.csv`, 176 rows): 41 Q-series codes (R2-3-Q01, R2-3-Q02_1, R2-9-Q01, R2-Q02 L/R, R3-Q01, R4-040-Q06 1-3, R5-Q01, R6-020-Q01/Q02, R6-100-Q01, R6-100-Q03_2, R6-28-Q01, R6-3-Q01, R6-33-Q01, R6-6-Q01, R6-Q03_1, R7-10-Q01, R7-3-Q01_1 L/R, R7-3-Q02, R7-3-Q03, R7-Q01 L/R, R9-1-1-Q01, R9-Q04 1-3, R9-Q05 L/R, R9-Q06, RM1-2-Q01 A/C, RM4-Q01, RM4-1-Q01, RM6-Q01B_1, RM6-Q03 1-2, RM7-Q01, RM9-Q01 A/B, RM9-9-Q01 A/B) and 10 TC sheets (TC1838 L/R, TC1933, TC2071, TC2089, TC2228 1-2, TC2247, TC2255, TC2345, TC9998); speed signs vary 5-130 as R4-1. Every dimension from the sheet's lettered table (c = white edge, d = edge + border, read as AS 1743 does); the sheets give no letter widths, so word gaps were measured from the sheets' live text / drawing and are noted per spec; AS 1744 Series E reproduces R6-28-Q01's stated widths within 1 mm. Disagreements recorded in notes: R9-1-1-Q01 SCHOOL DAYS tabled 45E cannot fit (Series C matches the drawing), TC2071 table b 1600 vs chain 1200 (chain used), R9-Q04-3 class lines in Series C per the sheet's long-name rule. 12 symbols traced into `tools/symbols/qld_*.svg` (trams x2, car, motorcycle, caravan, skaters, e-scooter, lane-filtering scene, pedestrian, three arrows). Overlay-checked every built sheet with `tools/compare_drawing.py` (specs carry `panel_px` where the white-on-white sheet defeats detection) and a contact sheet inspected: text signs sit on the drawings; the prohibition slashes slope upper-right to lower-left on TC2247 / R6-100-Q01 / R6-020-Q01 (measured) and the other way on TC9998 / TC2345; the drawings are 'not to scale' so letter sizes on some sheets are drawn larger than tabled (TC2255, RM1-2-Q01) — the table rules. Skips (26, in the manifest): LED signs (R2-4-Q01 1-4, TC2204, TC2260, TC2220, TC2085), flag fittings (R3-3-Q01, TC9472), layouts / examples / detail pages (R1-2-Q01_2, R4-040-Q01_2, Q02_3, Q03_3, Q07_8, R6-Q03 2-3, R7-3-Q01_2, RX-5-Q01, RX-11-Q01), pavement symbol (R5-Q07 1-2), TC1670 (Helvetica legend), TC1936 (changeable backboard), TC1868 (vertical chain does not sum), RM6-Q01B_2 (no % glyph in the AS 1744 fonts). Remaining in the regulatory family (not spec'd yet): R1-2-Q01_1 (cane trams give way — R1-2 inset size not tabled), R4-040-Q01-Q05 (school zone / enhanced school zone with target boards and LEDs), R4-040-Q07 1-7 (township entry, town-name variable), R4-040-Q08-Q11 (PMD speed limits, beach conditions), R5-40-Q01 (EV parking, symbol per SQ07), R5-61-Q01 1-2, R5-62-Q01, R5-Q06 1-2 (parking signs), R6-8-Q01, R6-Q02 (hand banners), R6-100-Q02 (four 180 roundels), R6-100-Q03_1, RM6-Q02, TC1476, TC1568, TC1648, TC1688, TC1778, TC2231, TC2366, TC2367, TC9942; then the other families (warning, temporary, guide/tourist, parking, supplementary, Q-series D/G/GE/T/W/TM) and their PNGs.
- 2026-09-09 — Contact-sheet inspection of the generated set: the four prohibition signs whose symbols were traced from sheets that draw the slash off the sign centre (TC2247, R6-100-Q01 by about 24 mm; R6-020-Q01 / Q02 further) carry the sheet's white cut beside the centred slash, so they are routed to `SVGs (generated)/intervene/Regulatory Signs/` with the reason in the manifest (fix: trace the symbol from the grid inset without the cut, or decide to follow the sheet's slash position). TC9998, TC2345 and R6-100-Q03_2 (slash through the centre on their sheets) are clean.
