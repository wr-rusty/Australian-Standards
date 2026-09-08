---
id: SGN-060
title: UK/England: sign pack
status: blocked
priority: P2
area: sources
project: uk
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

Build `UK/England/` from the TSRGD working drawings (vector PDFs, x-height tile layouts). Blocked on a commercial licence for the Transport Medium/Heavy and Motorway typefaces before any text sign can be produced for a commercial platform.

## Evidence

- TSRGD 2016 working drawings (OGL v3) https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-3 (schedules 2–16)
- International/REVIEW.md — UK section

## Fix

Obtain the font licence (URW++ Transport or K-Type Transport New); add an x-height tile-layout mode to the generator; extract symbols from the working drawings; produce family folders + manifest.

## Verify

Font licence on file; review sheets checked against the working drawings.

## Log

- 2026-09-06 — filed.

- 2026-09-08 — Rebuilt from the DfT's own coloured EPS artwork ("Traffic sign images", OGL v3) instead of the line-work drawings: `tools/uk_eps.py`, 658 SVGs in the 18 DfT categories; sizes from the working drawings via `tools/uk_sizes.py` (137 with a stated size, the rest nominal at 1 pt = 10 mm, said in the manifest). Awaiting Russell's review before Complete/.
