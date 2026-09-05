---
id: SGN-010
title: USA/Texas: state sign pack
status: in-progress
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `USA/Texas/` with the state-specific signs from TMUTCD + Standard Highway Sign Designs for Texas (SHSD 2012 rev 4); the federal MUTCD pack already covers the national signs.

## Evidence

- https://www.txdot.gov/business/resources/traffic-design-standards/highway-sign-designs.html — section PDFs on ftp.dot.state.tx.us/pub/txdot-info/trf/shsd/2012/

## Fix

Download the state's sign sheets into `USA/Texas/Original PDFs/`; vector PDFs go through the SHS-style extractor, others through the spec route; family folders + MANIFEST.csv; SOURCES.md with licence (state DOT terms).

## Verify

Review sheets checked; corner check clean; STATES.csv row updated with adoption status and pack path.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — SHSD 2012 rev 4 sections 1–13 downloaded (`USA/Texas/Original PDFs/`); the sheets match the FHWA SHS layout, so `tools/tx_extract.py` runs the MUTCD extractor with Texas code patterns (R1-2bTP, R7-107R (L,DBL), 11 pt labels). Full run in progress.
- 2026-09-05 — status → in-progress.
