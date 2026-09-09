---
id: SGN-005
title: Processing/Australia/SA: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Processing/Australia/SA/` with the SA-specific signs (those not in AS 1743, or drawn differently) from DIT Standard Road Sign Index. Russell's users work in every state, so every state pack is P1.

## Evidence

- http://www.dteiapps.com.au/signindx/ (Department Standard Road Sign Index) and https://dit.sa.gov.au/standards/standards-guidelines

## Fix

Download the register into `Processing/Australia/SA/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — SA Standard Road Sign Index is an Angular app over an AWS API (api/v1/signs, /series, /references): 1,211 signs, 1,023 with a PDF at signindex.dit.sa.gov.au/assets/signs/pdf/<id>.pdf (vector, no text). Register written to `Processing/Australia/SA/REGISTER.csv`; PDFs downloading to `Processing/Australia/SA/Original PDFs/`. Licence: CC BY 3.0 AU (site footer).
- 2026-09-05 — status → in-progress.
- 2026-09-06 — first full run: 755 SVGs from 685 PDFs (`Processing/Australia/SA/SVGs`, series folders), sizes from the register; 57 sheets gave no drawing; 137 flagged where drawn proportions differ from the register size.
- 2026-09-06 — rerun: 702 SVGs; shared symbol sheets filed once (symbols on all-outlined sheets not told apart — check); 60% grey rendered as white per the sheets' colour legend.
- 2026-09-06 — Rerun; deduplicated against the national pack: 94 SVGs removed (93 shared codes); 601 kept.
- 2026-09-09 — Spec-driven rebuild started (the way NSW / QLD are done); the extraction in `SVGs/` stays source material only. `SA` added to `PACKS` in `tools/signgen.py` (out `SVGs (generated)`, png `Original PNGs`, pdf, register, credit "© Government of South Australia (Department for Infrastructure and Transport), CC BY 3.0 AU"); AS 1743 output proven unchanged (R1-1 regenerated, SVG and MANIFEST hashes identical, git diff empty). All 685 sheets rendered upright at 200 dpi to `Original PNGs/<first code>.png` (pymupdf; the register has no `sign_no` column so `--render-pngs` was not used). The DIT sheets are fully dimensioned (letter series and heights, margins, ink widths, "=" offsets) — a far better source than the extraction.
  SA-only codes in the extraction manifest (rows with a file), by family: Regulatory 67 codes (12 of them AS 1743 codes at an A/B size, e.g. R2-5A, R9-1-1A — not SA-only), Parking 12 (2 national), Warning 93 (16 national), Temporary 138 (3), Service 84, Guide/Freeway 58 (excluded families), Hazard markers 11 (2), Symbol Series 32, Other 27.
  Regulatory family done first: 61 specs in `tools/specs/SA/` — 45 built (75 SVGs in `SVGs (generated)/Regulatory Signs`, `Speed Signs/End`, `Speed Signs/Normal Speed Signs`) and 16 skips (14 sheets that are AS 1743 codes at an A/B size → national pack; R2-SA61 composite of "modified" signs with no letter sizes; TES 13908(2) rail target-board assembly). Variants only where the sheet says "varies": speeds on R4-SA59/60/100/101/102/105/110, RM4-SA12; mass on R9-SA106C (4.5–22.5 t, not confirmed against SA practice); distance on R6-SA105A; gate number on R2-SA101; EXPRESSWAY / FREEWAY on R6-SA107/108; (L)/(R) on R2-SA102. Composites (R2-SA51-1/2, R2-SA60-1/2, R2-SA101, R2-SA103) reuse the national R2-4 / R2-5 / R2-6 / R9-1-1 / R9-1-2 elements the sheets cite, scaled into the sheets' boxes. Three symbols traced to `tools/symbols/sa_*` (R2-SA3 arrow, R6-SA104 skater, R8-SA100 horse and rider); R8-2 pedestrian/bicycle reused from the national set as the sheet says.
  Overlay check (`compare_drawing.py`, every built spec): green throughout after fixing the misreads it caught — the sheets list some width chains bottom line first (R4-SA59/60 END/ZONE, R2-SA57 RIGHT/LANE) and R6-SA13's chains are keyed by letter (A…L = AGRICULTURAL 970, B…S = BEYOND THIS 1025); R4-SA109's 80 D is the ring numeral and 55 D the words. Width check: 8 residual mismatches, all recorded in notes as the sheet's figures disagreeing with AS 1744 (R9-SA54A "&" 38 vs 45, R9-SA57A's AM/PM and 9/4 figures exchanged between lines, RM4-SA12A END 311 vs 340 in E). Contact sheet of all 75 inspected.
  Remaining in Regulatory: R3-SA58A (pentagon-topped school-zone sign with the W6-3 children symbol), R6-SA109A / 110A / 111A (wheeled-recreational-device pictograms from 10 mm grid insets — need tracing). Then Parking (R5-SA46-1/2 clearway, R5-SA100/101 part-time bus/bicycle lane, R5-SA163, R5-SA167), Warning, Temporary, Service, Hazard markers; and the register rows the extraction left without a file (e.g. R2-SA62, R4-SA61A, R6-SA66–68, R6-SA102/103/106A, R5-SA164–168) now have PNGs and can be spec'd.
