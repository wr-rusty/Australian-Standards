---
id: SGN-004
title: Australia/WA: state sign pack
status: open
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

Build `Australia/WA/` with the WA-specific signs (those not in AS 1743, or drawn differently) from Main Roads WA Signs Index. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.mainroads.wa.gov.au/technical-commercial/technical-library/signs-index/ — categories with per-sign pages; Specification 601 Signs

## Fix

Download the register into `Australia/WA/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
