---
id: SGN-026
title: USA/District of Columbia: confirm adoption status and any state-specific signs
status: open
priority: P2
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

District of Columbia is not in the first US batch. Confirm on FHWA's MUTCD adoption page whether District of Columbia adopts the national MUTCD as is, with a state supplement, or has its own state MUTCD, and whether it publishes state-specific sign sheets. Only a pack with state-only signs needs building; otherwise record 'federal pack applies' in `USA/STATES.csv`.

## Evidence

- https://mutcd.fhwa.dot.gov/resources/state_info/ — FHWA state adoption list
- state DOT traffic engineering / standard sign publications

## Fix

Record the adoption status in `USA/STATES.csv`; if state-only sheets exist, download them and build `USA/District of Columbia/` like the major-state packs.

## Verify

STATES.csv row filled with source URL and status; pack built or 'federal pack applies' justified.

## Log

- 2026-09-06 — filed.
