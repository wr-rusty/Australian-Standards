---
id: SGN-010
title: USA/Texas: state sign pack
status: open
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-06
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
