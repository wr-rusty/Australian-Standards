---
id: SGN-011
title: USA/Minnesota: state sign pack
status: in-progress
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `USA/Minnesota/` with the state-specific signs from MN MUTCD + MnDOT Standard Signs and Markings Manual; the federal MUTCD pack already covers the national signs.

## Evidence

- https://www.dot.state.mn.us/trafficeng/publ/signsmanual/index.html — supplement to FHWA SHS with Minnesota-specific designs

## Fix

Download the state's sign sheets into `USA/Minnesota/Original PDFs/`; vector PDFs go through the SHS-style extractor, others through the spec route; family folders + MANIFEST.csv; SOURCES.md with licence (state DOT terms).

## Verify

Review sheets checked; corner check clean; STATES.csv row updated with adoption status and pack path.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — MnDOT Standard Signs and Markings Manual sections located (edocs-public docIds) and downloading into `USA/Minnesota/Original PDFs/`; structure to inspect (expected SHS-style vector sheets).
- 2026-09-05 — status → in-progress.
- 2026-09-06 — edocs-public.dot.state.mn.us times out for curl (no TCP response within 60 s, http and https); the 14 section links are recorded in `USA/Minnesota/SOURCES.md`. Try again later, from another network, or through the Browser pane (save prompts).
