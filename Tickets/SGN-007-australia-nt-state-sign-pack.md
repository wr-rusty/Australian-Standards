---
id: SGN-007
title: Processing/Australia/NT: state sign pack
status: blocked
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Processing/Australia/NT/` with the NT-specific signs (those not in AS 1743, or drawn differently) from NT Department of Infrastructure, Planning and Logistics sign standards. Russell's users work in every state, so every state pack is P1.

## Evidence

- no register located yet — search DIPL standard drawings / NT Road Rules signage; may adopt AS 1743 as is

## Fix

Download the register into `Processing/Australia/NT/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — DLI civil standard drawings have a 'Road furniture and signs CS 3500–3599' series (NT speed limit sign, school zone, road closure, truck bay, rest area / tourist advance signs, hazard markers) plus CS 3400–3449 traffic control devices; listed in SOURCES.md. Same bot wall as TAS: needs the PDFs saved by hand.
- 2026-09-05 — status → blocked.

- 2026-09-08 — Russell saved the 24 NT drawings through the browser pane (bot wall). Line-work sheets: spec-driven build (tools/specs/NT/) once the pack routing from the NSW rebuild lands.
- 2026-09-08 — Spec-driven build done (PACKS entry NT, sheets rendered with `--render-pngs NT`; the CS35xx landscape sheets needed `--turn 0`). 25 specs in `tools/specs/NT/`: 8 SVGs (CS1557, CS3504 x4 speeds, CS3505, CS3507A/B); pointers to the national pack for CS3503 (W6-3), CS3509 (R4-1/R4-11), CS3511-3513 (G7-3-1/3-2/1-2/4-2), CS3514 (G11-1/2/4/7), CS3516/3517 (D4-1-1); skipped CS3503 school-zone panel and CS3506 (undimensioned / NTS), CS3510-3514 NT message plates (TraSiCAD templates), CS3518 hardware, project/advertising sheets. Symbol nt_cs3507_truck traced; W3-3 pictogram reused. Overlays clean (CS1557: sheet draws the diamond ~1400 against the stated 1365, kept 1365; CAD text letter-spaced wider than AS 1744 on CS1557/CS3507, no width checks). Copyright page 403: terms not captured.
