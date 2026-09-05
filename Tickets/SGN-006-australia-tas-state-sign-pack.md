---
id: SGN-006
title: Australia/TAS: state sign pack
status: blocked
priority: P1
area: sources
project: australia
created: 2026-09-06
updated: 2026-09-05
source: manual
---

## Summary

Build `Australia/TAS/` with the TAS-specific signs (those not in AS 1743, or drawn differently) from Department of State Growth standard drawings — signs. Russell's users work in every state, so every state pack is P1.

## Evidence

- https://www.transport.tas.gov.au/roadworks/contractor_and_industry_information/standard_drawings; Tasmanian Roadside Signs Manual

## Fix

Download the register into `Australia/TAS/Original .../`, extract or transcribe into `SVGs/<family>/` with a manifest (same rules as the national set: exact artwork where vector, spec route where only dimensioned drawings), note licence terms in SOURCES.md.

## Verify

Review sheets checked; corner transparency check clean; MANIFEST.csv lists every code; state-only codes not duplicated from the national pack.

## Log

- 2026-09-06 — filed.
- 2026-09-06 — Transport Tasmania's standard drawings page (transport.tas.gov.au, blocks scripted requests) has a Signs section: SD-087-005 to SD-087-032 (sign standard drawings), 'Signage Guidelines and Drawings' PDF, G/10/649 frost/ice/snow warning sign, fingerboard details 3403-5/P406-1. Few Tasmania-only sign faces; download through the Browser pane when the pack is built.
- 2026-09-06 — Signs section link list captured (17 PDFs, see SOURCES.md). curl and the pane's cookies both get the bot-check page; the pane hands each PDF to a save dialog — needs Russell to click save (or download by hand) into `Australia/TAS/Original PDFs/`.
- 2026-09-05 — status → blocked.
