---
id: SGN-091
title: Turn the pack-builder working scripts into maintained tools
status: open
priority: P2
area: tools
project: repo
created: 2026-10-02
updated: 2026-10-02
source: manual
---

## Summary

The QLD TC-sheet builder and the SA artwork builder exist only as terse scratch scripts (copied to tools/pack_builders/2026-10-02). The specs regenerate without them, but nobody could repeat or extend those builds.

## Evidence

- tools/pack_builders/README.md.

## Fix

Fold the useful parts (sheet vectors to spec paths, even-odd winding fix, ink-matched legend placement, contact sheets per family) into documented tools.

## Verify

tools/README.md describes them; a new sheet can be built with one command.

## Log

- 2026-10-02 — filed.
