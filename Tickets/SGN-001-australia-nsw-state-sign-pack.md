---
id: SGN-001
title: Australia/NSW: state sign pack
status: in-progress
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
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
- 2026-09-05 — status → in-progress.
- 2026-09-06 — register crawled: 1,662 signs, 1,162 with a design plan PDF (`Australia/NSW/REGISTER.csv`). Sheet extractor handles the modern plans well (text in FHWA fonts, stated 'W x H'); the older CAD exports (all text outlined, sideways sheets, several sizes per sheet, triangulated shapes, stroked outlines) still lose borders and keep dimension figures — see the manifest notes and the review sheets. Full run started; results to be QA'd.
- 2026-09-06 — first full run: 1,574 SVGs from 1,162 plans (`Australia/NSW/SVGs`, 8 families); 163 plans gave no drawing (old line-drawn sheets), 721 have no readable size (outlined figures; flagged 'check'), 208 have an assumed white background. 874 are NSW-only codes. Rerun due with the later extractor fixes (tessellated exports, frame filter).
