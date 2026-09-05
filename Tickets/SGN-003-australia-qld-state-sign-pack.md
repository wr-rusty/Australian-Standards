---
id: SGN-003
title: Australia/QLD: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Australia/QLD/` with the QLD-specific signs (those not in AS 1743, or drawn differently) from TMR Queensland MUTCD Q-series and TC signs. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.tmr.qld.gov.au/business-industry/Technical-standards-publications/TC-signs — full collection ZIP (188 MB), updated quarterly; site refuses scripted requests (403), download through the Browser pane

## Fix

Download the register into `Australia/QLD/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-05 — status → in-progress.
- 2026-09-06 — TC signs collection (June 2026, 1,173 sheets) downloaded; `tools/qld_extract.py` produced 790 SVGs in 36 category folders (`Australia/QLD/SVGs/MANIFEST.csv`: 264 sheets have no readable size and are drawn at 1:10 with a check note; 19 sheets superseded or without a drawing). Q-series (488-page book) not yet extracted.
- 2026-09-06 — Q-series book (q-series.pdf, 488 pages, one sign per page with a TC-style title block): codes like D4-1-1-Q03, G9-Q14_7, GE9-Q02, W5-Q07; the extractor's frame filter took the sheet frame on many pages (fixed: a closed outline covering half the drawing area is the frame). Driver still to write: iterate pages, code regex `[A-Z]{1,3}\d{0,2}(-\d+){0,3}-Q\d+(_\d+)?`, name from the title block.
