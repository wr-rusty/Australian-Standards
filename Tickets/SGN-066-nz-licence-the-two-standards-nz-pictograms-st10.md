---
id: SGN-066
title: NZ: licence the two Standards NZ pictograms (ST10 Look out, ST11 Photography)
status: open
priority: P2
area: licence
project: nz
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

NZTA withholds these two NZS 8603 symbols; the pack lifts them from NZTA's tourist sheets. Distribution on the platform should be covered by a Standards NZ licence or confirmation from NZTA.

## Evidence

- Complete/New Zealand/National (TCD Manual)/SVGs/MANIFEST.csv rows ST10, ST11
- NZTA copyright statement on the register

## Fix

Ask Standards NZ / NZTA; record the outcome in SOURCES.md.

## Verify

Written permission or licence on file.

## Log

- 2026-09-06 — filed.
- 2026-09-05 — NZ pass: ST03 and ST07 were stroked line art (no fills) — the extractor now outlines strokes with Inkscape and reads those (552 SVGs). SG01's register EPS is only a size frame (the state highway shield artwork is not published there); GA11/GA12 'example' rows are examples without artwork; the two Airport route entries (ids 740/741) have no files on the register and the page is behind the Imperva check — needs Russell in the browser pane. The rerun also fixed 40-odd signs whose second identical-bbox shape had been deduplicated away (e.g. RL3N diagonal cross).
- 2026-09-07 — Register swept by entry id (tools/nz_sweep.py): 687 entries the category listings never showed (RS1 speed limits, RS2/RS3, stop, give way, priority, no-stopping, alignment warnings…) → 1,266 signs. Dimensioned drawings (AB6/AB7 camera areas, PP21/PP31 parking, GA23) now read whole via the sheet extractor. Russell: signs look good. Moved to Complete/.
