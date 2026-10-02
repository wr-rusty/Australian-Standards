---
id: SGN-083
title: QLD: Temporary, Service/Tourist and Hazard marker families, and the leftover TC sheets
status: open
priority: P1
area: build
project: australia
created: 2026-10-02
updated: 2026-10-02
source: manual
---

## Summary

QLD has 491 generated signs (Regulatory, Speed, Parking, Warning). Temporary (Q-series T/TM and roadworks TC), Service/Tourist and Hazard markers are not started; a tail of Regulatory and warning TC sheets has no spec.

## Evidence

- Tickets/SGN-003 Log 2026-10-02 lists them: Regulatory R6-8-Q01, R6-Q02, RM6-Q02, TC1476, TC1568 1-6, TC1688, TC2231; skip rows needed for TC1778, TC2366, TC2367, TC9942, LED sheets TC2205, TC2210, TC2272-2278; warning TC1079, TC1346, TC1372, TC1767, TC1832 p3/p7-p10, TC1977, TC2351; rendered but not spec'd: stock and sugar-cane sheets (14), TC1073, 1074, 1267, 1356, 1574, 1709, 1747, 1756, 1774, 1802, 1806, 2250, 2258.
- Four W6-Q05 skip specs mislabel page numbers; qld_r6-100-q02_{bicycle,rollerskate,scooter,skateboard}.svg are unused.

## Fix

One spec per sheet in tools/specs/QLD, generate with signgen, overlay-check, skip with reasons; fix the W6-Q05 skip text; remove the unused symbols.

## Verify

Every QLD sheet outside Guide/Freeway has a spec or a skip row; manifest and folder agree; SGN-003 Log updated.

## Log

- 2026-10-02 — filed.
