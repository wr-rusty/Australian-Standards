---
id: SGN-011
title: USA/Minnesota: state sign pack
status: open
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-06
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
