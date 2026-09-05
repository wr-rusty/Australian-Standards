---
id: SGN-065
title: USA/Federal: review the 'check' size rows and page-scale guide signs in MANIFEST.csv
status: open
priority: P2
area: qa
project: usa
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

The 2024 SHS tables have no conventional-road marker; 492 manifest rows carry a rule-chosen size ('check') and 102 guide signs are drawn at sheet scale. Russell to confirm the size rule or supply MUTCD Table 2B-1/2C-2 sizes.

## Evidence

- USA/Federal (MUTCD 2023)/SVGs/MANIFEST.csv — notes column
- tools/shs_extract.py choose_row()

## Fix

Decide the rule (or encode MUTCD tables 2B-1, 2C-2, 2D-x) and regenerate.

## Verify

No 'check' rows left, or each accepted in the Log.

## Log

- 2026-09-06 — filed.
