---
id: SGN-065
title: Processing/USA/Federal: review the 'check' size rows and page-scale guide signs in MANIFEST.csv
status: open
priority: P2
area: qa
project: usa
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

The 2024 SHS tables have no conventional-road marker; 492 manifest rows carry a rule-chosen size ('check') and 102 guide signs are drawn at sheet scale. Russell to confirm the size rule or supply MUTCD Table 2B-1/2C-2 sizes.

## Evidence

- Complete/USA/Federal (MUTCD 2023)/SVGs/MANIFEST.csv — notes column
- tools/shs_extract.py choose_row()

## Fix

Decide the rule (or encode MUTCD tables 2B-1, 2C-2, 2D-x) and regenerate.

## Verify

No 'check' rows left, or each accepted in the Log.

## Log

- 2026-09-06 — filed.
- 2026-09-07 — Full review of the 1,441 SVGs: the letter I was being dropped from outlined legends by the background-mask rule (bg mis-read as black on white signs); rule now only fires at the panel edge. Reran all 11 sheet sets. Pack moved to Complete/.

- 2026-09-08: Russell reported cross-hairs in the top-right corner and white lines across green panels. Added rules in `is_annotation` (tools/shs_extract.py): corner cross-hair ticks, specks at any corner, hairline white dimension bars (thickness <= 1.2 pt, aspect >= 4) and white diagonal slivers on coloured panels. First two attempts dropped the letter I again (SCENIC VIEW -> "SCEN C V EW"); fixed by keying the bar rule on absolute hairline thickness rather than a fraction of the sign side. Full rerun of all 11 sets, 1,451 SVGs; three 48-sign samples plus the reported signs render clean.

- 2026-09-08: Russell asked to confirm the colours, especially yellows. Found the 2004-era sheets use a brighter yellow (#fff500) and different blue/green/red/orange/black from the 2024 sheets. `tools/shs_palette.py` normalises the whole pack to the 2024 Edition values (278 files recoloured); documented in Original PDFs/SOURCES.md.
