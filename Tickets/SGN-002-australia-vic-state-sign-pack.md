---
id: SGN-002
title: Australia/VIC: state sign pack
status: blocked
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
