---
id: SGN-009
title: USA/California: state sign pack
status: open
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-06
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
