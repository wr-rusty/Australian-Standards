---
id: SGN-013
title: USA/Michigan: state sign pack
status: open
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

Build `USA/Michigan/` with the state-specific signs from MMUTCD + Michigan Standard Highway Signs; the federal MUTCD pack already covers the national signs.

## Evidence

- https://mdotjboss.state.mi.us/TSSD/ — Traffic Signing > Standard Highway Signs

## Fix

Download the state's sign sheets into `USA/Michigan/Original PDFs/`; vector PDFs go through the SHS-style extractor, others through the spec route; family folders + MANIFEST.csv; SOURCES.md with licence (state DOT terms).

## Verify

Review sheets checked; corner check clean; STATES.csv row updated with adoption status and pack path.

## Log

- 2026-09-06 — filed.
