---
id: SGN-003
title: Australia/QLD: state sign pack
status: open
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

Build `Australia/QLD/` with the QLD-specific signs (those not in AS 1743, or drawn differently) from TMR Queensland MUTCD Q-series and TC signs. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.tmr.qld.gov.au/business-industry/Technical-standards-publications/TC-signs — full collection ZIP (188 MB), updated quarterly; site refuses scripted requests (403), download through the Browser pane

## Fix

Download the register into `Australia/QLD/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
