---
id: SGN-086
title: VIC, WA and ACT: spec-driven rebuilds not started
status: open
priority: P1
area: build
project: australia
created: 2026-10-02
updated: 2026-10-02
source: manual
---

## Summary

NSW, QLD, SA, TAS and NT are rebuilt spec-driven. VIC (319 extracted, TEM Vol 2 Part 2.17 V-series), WA (1,190 extracted from DWG, colours uncertain) and ACT (5, scanned parking sheets) still hold only the rejected extractions.

## Evidence

- Tickets SGN-002, SGN-004, SGN-008; Processing/Australia/{VIC,WA,ACT}.

## Fix

Add PACKS entries, render sheets, write specs per family (Regulatory first), overlay-check; WA needs the colour decision in OPEN-ITEMS.md.

## Verify

Each pack has an 'SVGs (generated)' set with an exact manifest.

## Log

- 2026-10-02 — filed.
