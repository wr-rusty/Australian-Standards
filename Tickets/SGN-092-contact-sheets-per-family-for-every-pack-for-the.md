---
id: SGN-092
title: Contact sheets per family for every pack, for the inspectors
status: open
priority: P1
area: tools
project: repo
created: 2026-10-02
updated: 2026-10-02
source: manual
---

## Summary

Inspection will be handed to someone else (INSPECTION.md). They need one image per family per pack, on a grey ground, labelled by code, regenerated on demand.

## Evidence

- tools/pack_sheets.py and tools/svg_sheets.py exist for the older packs; the generated state sets and the European packs have none in the repo.

## Fix

One command renders <pack>/Review/<family>.png for any pack; run it for every pack listed in the inspection tickets.

## Verify

Each inspection ticket links its contact sheets.

## Log

- 2026-10-02 — filed.
