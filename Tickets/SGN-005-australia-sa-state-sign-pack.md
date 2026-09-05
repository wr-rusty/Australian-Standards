---
id: SGN-005
title: Australia/SA: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Australia/SA/` with the SA-specific signs (those not in AS 1743, or drawn differently) from DIT Standard Road Sign Index. Russell's users work in every state, so every state pack is P1.

## Evidence

- http://www.dteiapps.com.au/signindx/ (Department Standard Road Sign Index) and https://dit.sa.gov.au/standards/standards-guidelines

## Fix

Download the register into `Australia/SA/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — SA Standard Road Sign Index is an Angular app over an AWS API (api/v1/signs, /series, /references): 1,211 signs, 1,023 with a PDF at signindex.dit.sa.gov.au/assets/signs/pdf/<id>.pdf (vector, no text). Register written to `Australia/SA/REGISTER.csv`; PDFs downloading to `Australia/SA/Original PDFs/`. Licence: CC BY 3.0 AU (site footer).
- 2026-09-05 — status → in-progress.
- 2026-09-06 — first full run: 755 SVGs from 685 PDFs (`Australia/SA/SVGs`, series folders), sizes from the register; 57 sheets gave no drawing; 137 flagged where drawn proportions differ from the register size.
- 2026-09-06 — rerun: 702 SVGs; shared symbol sheets filed once (symbols on all-outlined sheets not told apart — check); 60% grey rendered as white per the sheets' colour legend.
