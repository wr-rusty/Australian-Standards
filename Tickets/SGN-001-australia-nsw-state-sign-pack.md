---
id: SGN-001
title: Processing/Australia/NSW: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Processing/Australia/NSW/` with the NSW-specific signs (those not in AS 1743, or drawn differently) from Transport for NSW traffic sign register. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.transport.nsw.gov.au/operations/roads-and-waterways/traffic-signs — one page per sign with a design plan for most signs; G series site-specific

## Fix

Download the register into `Processing/Australia/NSW/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-05 — status → in-progress.
- 2026-09-06 — register crawled: 1,662 signs, 1,162 with a design plan PDF (`Processing/Australia/NSW/REGISTER.csv`). Sheet extractor handles the modern plans well (text in FHWA fonts, stated 'W x H'); the older CAD exports (all text outlined, sideways sheets, several sizes per sheet, triangulated shapes, stroked outlines) still lose borders and keep dimension figures — see the manifest notes and the review sheets. Full run started; results to be QA'd.
- 2026-09-06 — first full run: 1,574 SVGs from 1,162 plans (`Processing/Australia/NSW/SVGs`, 8 families); 163 plans gave no drawing (old line-drawn sheets), 721 have no readable size (outlined figures; flagged 'check'), 208 have an assumed white background. 874 are NSW-only codes. Rerun due with the later extractor fixes (tessellated exports, frame filter).
- 2026-09-06 — rerun with the fixed extractor: 1,345 SVGs (multi-size sheets folded to the largest, tessellated exports unioned); 206 plans still give no drawing and 632 have no readable size — the old line-drawn sheets remain the open problem.
- 2026-09-06 — review of the rerun: modern and old sheets both render; left for the next pass: outlined dimension figures (e.g. 'R488', '1200') kept when they sit inside or beside the sign hull, and the same sign at 3–4 sizes not folded because those figures differ per copy — drop small all-black digit clusters near the panel edge before comparing signatures.
- 2026-09-06 — Rerun with the union/legend fixes, then deduplicated against the national pack: 454 SVGs removed (281 shared codes such as R1-1); 855 NSW-only signs kept. Do not redraw national codes again.
- 2026-09-08 — Spec-driven rebuild continued (`tools/specs/NSW/`, output `Processing/Australia/NSW/SVGs (generated)/`, own MANIFEST.csv; `signgen.py` PACKS routing, `trace_symbol.py --pack/--render-pngs`, `compare_drawing.py` pack sheets). Proof the AS 1743 output is untouched by the pack routing: `signgen.py R/R1-1.json W/W1-1.json` regenerated R1-1 and W1-1(L)/(R) byte-identical to the committed files (only the national MANIFEST.csv changed, because a partial run always rewrites it with just the specs given — pre-existing behaviour; restored from a backup). 26 new Regulatory specs written from the design plans this session (25 signs + R4-1-1n skipped as an example-only gateway treatment): R3-202n, R4-4-1n, R4-205n, R4-11-1n, R4-239n, R4-212n (40/60/80/100), R2-4n, R2-5n, R2-6n(L), R2-6n(R), R7-224n, R7-234n, R4-229n and R4-220n (40/60/80/90/100), R4-1n_VMS and R4-212n_VMS (40-110), R4-236n, R4-236-1n, R4-237n, R4-237-1n, R4-238n, R7-220n, R7-223n, R7-230n, R7-233n. Symbols traced from the sheets: nsw_r2-5n_u_turn_arrow, nsw_r2-6n_left_turn_arrow (flipped for (R)), nsw_r4-236n_pedestrians, nsw_r4-238n_rain_cloud (new tracer option `keep_specks` keeps the rain strokes that the edge-speck filter dropped); the R4-4-1n child/car, the T2/T3 blobs, transit-lane car and repeater arrows are the plans' own vector paths. Totals now 62 specs, 86 SVGs (all Regulatory Signs), 7 nsw_* symbols. Overlay check (compare_drawing) on every new sign: scores 0.02-0.21 (R4-11-1n 0.21 after finding the ring is 36 wide, not the 70 in the chain; R4-238n 0.11 after the drawing's outline proved 5 % taller than its stated 3960 — panel_px set to the true-scale box); dashed 'variable' numerals score 0.33-0.36 as expected. Width checks: only the T2/T3 legends (plan glyphs vs FHWA spacing, 2-7 %) and the R4-236n/237n '40' (2.5 %) differ, explained in notes; R9-306n/308n/309n/206n remain from the earlier pass. Readings recorded in notes: RMS sheets dimension edge / edge + border (12/36 = 12 + 24 etc., confirmed by pixel measurement); T2/T3 at 210 on the transit-lane signs is Series C by measurement although the legend says D; R4-238n(D) numerals are 480 E as the legend states. Remaining NSW-only Regulatory codes without a spec (31): school zones R4-230n, R4-230-1-2n, R4-231n, R4-235n, R4-235-1n, R4-235-1-1n, R4-235-1-2n (two-panel fluorescent yellow-green signs with superscript times); bus-lane series r7-1-1-1n..R7-1-1-8n, R7-8-1n..R7-8-7n, R7-1-6-1n (old outlined sheets, no stated size); diagrammatic R9-208n, R9-210n, R9-211-1n, R9-211-2n; R9-216n, R9-232n, R4-246n (lettered table), R2-19-1n (on the g9-73-1n_l sheet). Other families (Warning 203, Guide 206, Temporary 167, Service 95, Freeway 31, Parking 25, Hazard 4 NSW-only codes) not started.
