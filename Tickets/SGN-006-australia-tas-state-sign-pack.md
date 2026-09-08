---
id: SGN-006
title: Processing/Australia/TAS: state sign pack
status: blocked
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Processing/Australia/TAS/` with the TAS-specific signs (those not in AS 1743, or drawn differently) from Department of State Growth standard drawings — signs. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.transport.tas.gov.au/roadworks/contractor_and_industry_information/standard_drawings; Tasmanian Roadside Signs Manual

## Fix

Download the register into `Processing/Australia/TAS/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — Transport Tasmania's standard drawings page (transport.tas.gov.au, blocks scripted requests) has a Signs section: SD-087-005 to SD-087-032 (sign standard drawings), 'Signage Guidelines and Drawings' PDF, G/10/649 frost/ice/snow warning sign, fingerboard details 3403-5/P406-1. Few Tasmania-only sign faces; download through the Browser pane when the pack is built.
- 2026-09-06 — Signs section link list captured (17 PDFs, see SOURCES.md). curl and the pane's cookies both get the bot-check page; the pane hands each PDF to a save dialog — needs Russell to click save (or download by hand) into `Processing/Australia/TAS/Original PDFs/`.
- 2026-09-05 — status → blocked.

- 2026-09-08 — Russell saved the drawings through the browser pane (site bot wall). 15 sign-face drawings + 6 mounting-detail sheets in Original PDFs/. Black line-work sheets: build spec-driven (tools/specs/TAS/, pack routing as for NSW), not by extraction.
- 2026-09-08 — Spec-driven build done. `tools/signgen.py` PACKS gained TAS (out `SVGs (generated)`, png/pdf folders, no register, credit line); `tools/trace_symbol.py --render-pngs` now works without a register (walks the PDF folder) and takes `--turn` for sheets the upright guess gets wrong (P70-2, P71-2, P411-1, P514, 444A, 445A, 484, 351B needed -90); symbol sources may name the sheet (`drawing`). 19 specs in `tools/specs/TAS/`: 15 SVGs generated (P70-2, P71-2, P92, W5-118, T1-105, P514, W5-103, W6-101, W6-102, T1-101A/B, W5-102, R4-1(50)SZ, 649 panels A/B); G9-101 excluded (G9 family, as national); skipped P406-1 (fingerboard templates), P411-1 (details), 649 options (logos). Symbols traced: tas_w6-101_bus_child, tas_g9-101_truck; W5-20 car reused for the slippery signs. Overlays (compare_drawing, contact sheet inspected): all rows/panels/symbols align; the sheets' spacing is ~7 % wider than AS 1744 so width checks flag most words (kept plus0, noted); R4-1(50)SZ ring drawn smaller than R4-1 (AS 1743 geometry used, noted). Copyright page behind the bot wall: terms not captured.
