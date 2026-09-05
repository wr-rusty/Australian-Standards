---
id: SGN-009
title: USA/California: state sign pack
status: in-progress
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `USA/California/` with the state-specific signs from CA MUTCD + Caltrans Sign Specification Drawings (PDF per CA-coded sign, ~300); the federal MUTCD pack already covers the national signs.

## Evidence

- https://dot.ca.gov/programs/safety-programs/sign-specs — PDF only, path /-/media/dot-media/programs/safety-programs/documents/signs/<series>/<file>-a11y.pdf; curl works

## Fix

Download the state's sign sheets into `USA/California/Original PDFs/`; vector PDFs go through the SHS-style extractor, others through the spec route; family folders + MANIFEST.csv; SOURCES.md with licence (state DOT terms).

## Verify

Review sheets checked; corner check clean; STATES.csv row updated with adoption status and pack path.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — Caltrans sign-spec index crawled (487 PDFs, `USA/California/REGISTER.csv`), downloading into `Original PDFs/<series>/`. About half are scanned images (OCR layer, no vectors) — those need tracing or a vector copy from Caltrans; the vector half can go through the sheet extractor.
- 2026-09-05 — status → in-progress.
- 2026-09-05 — `tools/ca_extract.py`: 245 SVGs from the 246 vector sheets (two-tone sheets recoloured from the COLORS note; sizes from the SIGN SIZE table). 228 scanned sheets listed without files — need vector copies or tracing. Sheet extractor fixes along the way (converter-merged text paths, compound-path explode, arrowheads at panel edges, scattered-letter blocks, big panels vs sheet frame). 200 check rows. Review sheets checked.
