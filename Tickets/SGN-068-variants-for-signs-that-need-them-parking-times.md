---
id: SGN-068
title: Variants for signs that need them (parking times, NZ signs composed from the symbol set)
status: open
priority: P1
area: content
project: none
created: 2026-09-08
updated: 2026-09-08
source: manual
---

## Summary

(what is wrong and why it matters)

## Evidence

- (sources, URLs, files — verified)

## Fix

(the concrete change)

## Verify

(how we know it is done)

## Log

- 2026-09-08 — filed.

## What Russell asked (2026-09-08)

"Add to the todo that we need to ensure we are providing all variants of signs that need it. I don't mean every single
street sign — the example street signs (like 'Auckland this turn') are fine as examples; these signs are made ad hoc
when needed and we can't make every sign under the sun. But signs like parking times etc. we should make some of the
variants. Especially NZ: I believe the symbols are there to make actual signs."

## Scope

* Per pack, list the sign families that are templates with meaningful variants (parking time plates, clearways,
  speed-limit values, distance plaques, lane-use combinations) and produce a sensible set of the real variants, not
  one example each.
* NZ: use the symbol/arrow/legend components in the TCD register to compose the actual signs the manual specifies
  (parking P-series time variants, RP-series, etc.).
* Do not attempt every street-name/destination sign; keep the example ones.
* Each variant is one file, named by its code and the variant value; no size variants.

## NZ inventory (2026-09-08)

Sources: `Complete/New Zealand/National (TCD Manual)/REGISTER.csv` (NZTA sign-specification register — each row carries the
TCD Rule sign number and its component list, e.g. "R6-30 (Components: R6-1C.2-4)", the dimension letters and the letter
series such as "`P` 100E Numerals 75D Arrow Type B") and the extracted artwork in `SVGs/Parking Signs/`. NZTA supplies
one filled example per family (P30, or P60/P120 for zone signs), never a blank plate or a numeral sheet; the components
named in the register (R6-1C P-symbol, R6-1T time numerals, R6-2 class symbol, R6-3 times legend, R6-4 arrow) are what
the drawn example is built from. The TCD Manual Part 13 text could not be read this session (nzta.govt.nz is behind
Imperva for curl/WebFetch and the in-app browser refused the domain; legislation.govt.nz and drivingtests.co.nz answer
403; web.archive.org is not reachable from Claude Code), so the time-limit set is evidenced by the register examples
(30/60/120) plus council schedules made under the Rule/Manual: QLDC Traffic and Parking Bylaw 2018 on-road restrictions
schedule (P5, P10, P15, P30, P60, P120, P180, P240 in regular use; P45/P90 one-offs — excluded), Gisborne DC Parking
Policy 2018 (P15/P30/P60/P120/P180 used; P2/P10/P20/P90 not to be used), Auckland Transport (P30/P60/P180). The 2011
draft of Part 13 advises against P5 in mobility (disabled) parks.

Font check before composing: the artwork numerals "3"/"0" at 75 mm measure 50.2/52.5 mm wide and 77.9 mm tall; the repo's
FHWA Series D face (= AS 1744 Series D) at 75 mm cap gives 51.1/53.3 mm wide, 77.6 mm tall — within 2 %, digit heights
identical, so the face supplies the digits the artwork lacks (4, 5, 8).

| Family (Rule sign) | Register code, size | NZTA supplies | Variant set | Built |
|---|---|---|---|---|
| Time restricted, standard hours (R6-30) | PP21 300x300 | P30, P60, P120 x (right, left, double arrow) = 9 | 5, 10, 15, 180, 240 | 15 |
| Non-standard hours (R6-31), `Mon-Fri` legend | PP22 300x360 | P30 x 3 arrows | 5, 10, 15, 60, 120, 180, 240 | 21 |
| Other times (R6-32), `Other Times` legend | PP22 300x360 | P30 x 3 arrows | same 7 | 21 |
| Bus parking time restricted (R6-53.2) | PP3 300x400, PP31 300x450 | P30 x (standard + 3 arrows) | same 7 | 28 |
| Shuttle parking time restricted (R6-54.2) | PP3 / PP31 | P30 x 4 | same 7 | 28 |
| Loading zone (R6-50; "Numeral 75D" is a listed component) | PP21 300x300, PP22 300x360 | P5 x 4 | 10, 15, 30 (council practice) | 12 |
| Parking zone signs | PZ21 400x450, PZ22 400x450, PZ12 300x430, PZ13 500x500, PZ22 300x430, PZ23 300x450 | P60 or P120, one each | 30, 60, 120, 180, 240 minus the drawn one | 24 |
| Disabled parking time restricted (R6, S37 symbol) | PP3 / PP31 | P30 x 4 | — | 0: base extractions are defective (stray dimension marks on PP3 standard and both PP31 single arrows; the double arrow lacks the white border; two "BLACK" fragment files are label debris) — re-extract the bases first, then rerun; P5 not appropriate for mobility parks anyway |
| EV parking time restricted (S31 symbol) | PP22 300x400 (P60), 300x460 (P120) | two examples with different heights | — | 0: no manual text on EV time values and the two layouts differ; not composed |
| Clearway single/two peak (R6-12.1/.2), No stopping specified period (R6-11), Bus stop specified times | PCH2, PCH3, PN13, P23 | one example each, hours in Transport Medium | site-specific hours, no defined set | 0 (not a template with a finite set; the am/pm/Mon-Fri glyphs exist in the artwork if a set is ever specified) |
| PZ11 "P$ / 60 / Zone" | PZ11 | two register examples merged in one drawing | — | 0: ambiguous base |
| No stopping for X km (R6-10.2) | PNS1 | 1–5 km | complete in register | — |
| Speed limits (RS1/RS1B/RS4) | RS1 10–90, RS2 100, RS4 110, RS1B 10–80 | complete in register | — | — |

How each variant is composed (`tools/nz_variants.py`, note recorded per manifest row): every path of the NZTA base SVG
(border, background, `P` 100E, class symbol, Transport Medium legend, arrow) is copied verbatim; only the numeral
outlines are replaced by the same digits set in Series D at 75 mm, on the base artwork's numeral baseline (derived from
the base digits' bottoms less the face's overshoot) and centred where the artwork centres its numerals (sign centre on
the stacked layouts). One-line layouts (`P120 Zone`) keep the artwork's P-to-numeral gap and re-centre the P + numerals
group as the artwork does (the `P` path gets a translate). Header, viewBox, size and colours are the base sign's.
Discrepancy noted: the bus PP31 arrow-right/double-arrow artwork numerals measure ~41 mm wide (Series C) although the
register says 75D; the variants follow the register (75D). Files: `<TITLE>_P<VALUE>_<CODE>.svg` beside the base.

## Log

- 2026-09-08 — filed from Russell's message while the UK national pack was being built.
- 2026-09-08 — NZ built: `tools/nz_variants.py` composed 149 time-limit variants into `SVGs/Parking Signs/` (PP21 standard hours 15, PP22 non-standard/other times 42, bus 28, shuttle 28, loading zone 12, PZ zone signs 24), one MANIFEST.csv row each with the composition note; contact sheet rendered and inspected, geometry re-checked against the bases (baseline and centring within 0.05 mm). Remaining: disabled-parking bases need re-extraction before their variants; EV, clearway and no-stopping time plates not composed (see inventory); other packs (AU/US/UK) not started.
