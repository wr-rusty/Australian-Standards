---
id: SGN-007
title: Australia/NT: state sign pack
status: blocked
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Australia/NT/` with the NT-specific signs (those not in AS 1743, or drawn differently) from NT Department of Infrastructure, Planning and Logistics sign standards. Russell's users work in every state, so every state pack is P1.

## Evidence

- no register located yet — search DIPL standard drawings / NT Road Rules signage; may adopt AS 1743 as is

## Fix

Download the register into `Australia/NT/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — DLI civil standard drawings have a 'Road furniture and signs CS 3500–3599' series (NT speed limit sign, school zone, road closure, truck bay, rest area / tourist advance signs, hazard markers) plus CS 3400–3449 traffic control devices; listed in SOURCES.md. Same bot wall as TAS: needs the PDFs saved by hand.
- 2026-09-05 — status → blocked.
