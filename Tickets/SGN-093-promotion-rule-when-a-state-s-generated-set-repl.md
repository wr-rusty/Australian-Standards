---
id: SGN-093
title: Promotion rule: when a state's generated set replaces its extraction and moves to Complete
status: open
priority: P2
area: docs
project: repo
created: 2026-10-02
updated: 2026-10-02
source: manual
---

## Summary

State packs now hold two sets: the rejected extraction in SVGs/ and the spec-driven set in 'SVGs (generated)/'. Nothing says when the generated set becomes the pack, what happens to the extraction, or how the SitePilot upload picks the folder.

## Evidence

- README.md; Processing/Australia/{NSW,QLD,SA,TAS,NT}.

## Fix

The owner decides: after inspection passes, 'SVGs (generated)' becomes SVGs/, the extraction moves to an archive folder (not deleted), the pack moves to Complete/.

## Verify

README.md states the rule; one pack promoted as the worked example.

## Log

- 2026-10-02 — filed.
