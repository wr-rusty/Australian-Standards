---
id: SGN-067
title: Repo: STATES.csv for the USA and a JURISDICTIONS.md map for the SitePilot upload
status: open
priority: P2
area: docs
project: repo
created: 2026-09-06
updated: 2026-09-06
source: manual
---

## Summary

The platform resolves a user's jurisdiction to packs. Provide a machine-readable map: country → jurisdiction → pack folder(s) and status.

## Evidence

- Proposed layout agreed 2026-09-06: Australia/<State>, USA/<State>, UK/<Region>, New Zealand/National

## Fix

Write USA/STATES.csv (51 rows) and JURISDICTIONS.md at the repo root; keep them updated as packs land.

## Verify

Every folder under Australia/, USA/, UK/, New Zealand/ appears in the map.

## Log

- 2026-09-06 — filed.
