---
id: SGN-002
title: Australia/VIC: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Australia/VIC/` with the VIC-specific signs (those not in AS 1743, or drawn differently) from Department of Transport and Planning (VicRoads) sign drawings. Russell's users work in every state, so every state pack is P1.

## Evidence

- VicRoads Manual of Standard Drawings for Road Signs; Traffic Engineering Manual Vol 2 ch 6 — locate the current download on vicroads.vic.gov.au

## Fix

Download the register into `Australia/VIC/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — Victoria's drawings are not online as a register: the 'VicRoads Manual of Standard Drawings for Road Signs' (2004) and TEM Vol 3 are listed in the DTP technical publications catalogue (vic.gov.au/dtp-technical-publications, JS search; catalogue spreadsheet). Locate the current download or request it from StandardsManagementRD@transport.vic.gov.au.
- 2026-09-05 — status → blocked.
- 2026-09-06 — Unblocked: the DTP Engineering Standards Catalogue lists 'TEM Vol 2 Part 2.17 – Supplement to AS 1743:2023 Road signs – Specifications v2.0' (370 pages, one V-series drawing per page) and TEM Vol 3 Part 2.12 tourist/service signs. Downloaded to `Australia/VIC/Original PDFs/`; `tools/vic_extract.py` (pages turned 90°, names from the index tables) → ~320 SVGs; 172 without a readable size (check). Legends are live Times text with per-letter spans — the extractor now keeps big single letters as legend.
- 2026-09-05 — status → in-progress.
- 2026-09-06 — Full run: 319 SVGs in 11 families (`Australia/VIC/SVGs`), 18 pages without a drawing, 172 size checks (no readable dimension figure → drawn at 1:10). Review sheets checked: legends complete after the big-letter fix.
