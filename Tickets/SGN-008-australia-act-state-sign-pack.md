---
id: SGN-008
title: Australia/ACT: state sign pack
status: blocked
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Australia/ACT/` with the ACT-specific signs (those not in AS 1743, or drawn differently) from Transport Canberra and City Services MITS-14 Road signs. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.cityservices.act.gov.au/__data/assets/pdf_file/0007/1387150/MITS-14-Road-signs-1-0.pdf; MIS-12 Guide signs; TCCS drafting standard sign blocks

## Fix

Download the register into `Australia/ACT/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — MITS-14 Road signs (July 2019, 37 pages) downloaded to `Australia/ACT/Original PDFs/`: it is a construction specification referencing AS 1742/1743 codes, with no ACT-specific sign drawings. ACT likely adopts the national pack; check MIS-12 Guide signs and TCCS sign blocks before closing.
- 2026-09-06 — TCCS ACTSD sign drawings downloaded (39 sheets). Parking-sign sheets 3701–3735 are scans; 3720/3724 vector → `tools/act_extract.py` gives 5 pay-parking SVGs. ACT otherwise uses the national set. Status → blocked on TCCS CAD originals for the parking faces.
- 2026-09-05 — status → blocked.
