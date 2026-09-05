---
id: SGN-001
title: Australia/NSW: state sign pack
status: open
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

Build `Australia/NSW/` with the NSW-specific signs (those not in AS 1743, or drawn differently) from Transport for NSW traffic sign register. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.transport.nsw.gov.au/operations/roads-and-waterways/traffic-signs — one page per sign with a design plan for most signs; G series site-specific

## Fix

Download the register into `Australia/NSW/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
