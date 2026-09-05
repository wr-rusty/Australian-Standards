---
id: SGN-017
title: USA/Florida: state sign pack
status: open
priority: P1
area: sources
project: usa
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

Build `USA/Florida/` with the state-specific signs from FDOT supplement + Florida-specific signs; the federal MUTCD pack already covers the national signs.

## Evidence

- https://www.fdot.gov/traffic/trafficservices/faq-signing.shtm; FDOT Standard Plans index 700

## Fix

Download the state's sign sheets into `USA/Florida/Original PDFs/`; vector PDFs go through the SHS-style extractor, others through the spec route; family folders + MANIFEST.csv; SOURCES.md with licence (state DOT terms).

## Verify

Review sheets checked; corner check clean; STATES.csv row updated with adoption status and pack path.

## Log

- 2026-09-06 — filed.
