# TM3 / TM4 / TM5 transcription report

47 drawings: 38 spec, 9 needs-symbol, 0 skipped. Generator (tools/signgen.py on tools/specs/TM/*.json): one width
mismatch remains, TM3-12C OVERTAKE, by design (the drawing's own number is wrong; see notes in the spec).

Conventions used: 1200x300 = LONG_SKINNY, 1200x600 = LONG, 600x600 = SQUARE. All panels are 25 black border, no radius, no edge.
Where a drawing's row of widths does not sum to the panel width, the wrong number was identified from the other numbers in the row
(e.g. width = panel - margins - gap - other word) and cross-checked against AS 1744 spacing; the derived value is in `expect` and the
drawing's figure is quoted in `notes`. Where the drawing's series letter disagrees with its own stated widths, the series that reproduces
the widths was used and the label quoted in `notes`. Nothing was estimated by eye.

| code | name | status | flags |
|---|---|---|---|
| TM3-3A | SLIPPERY_YELLOW_SQUARE | needs-symbol tm3-3a_slippery_car | box 85/430/85 x 112/375/113 |
| TM3-6A | SOFT_EDGES_YELLOW_SQUARE | spec | |
| TM3-6B | SOFT_EDGES_YELLOW_LONG_SKINNY | spec | |
| TM3-7A | ROUGH_SURFACE_YELLOW_SQUARE | spec | |
| TM3-7B | ROUGH_SURFACE_YELLOW_LONG_SKINNY | spec | |
| TM3-9A | LOOSE_STONES_SYMBOL_YELLOW_SQUARE | needs-symbol tm3-9a_loose_stones | box 75/450/75 x 196/207/197 |
| TM3-11C | NEW_WORK_NO_LINES_MARKED_YELLOW_LONG | spec | DRAWING: the two top width rows are the reverse of the usual order (inner row 158/328/64/452/158 is NEW WORK, outer row 230/206/80/454/230 is NO LINES); NEW WORK row sums to 1160 not 1200 (margins should be 178) |
| TM3-12C | NO_LINES_DO_NOT_OVERTAKE_UNLESS_SAFE_YELLOW_LONG | spec | DRAWING (several): vertical stack has no gap dimension between lines 1-2 and sums to 615 without it; drawn gaps are ~35 (600-57-58-4x95 = 105 = 3x35) so 35 used, the two '60' labels are wrong. DO NOT row 346/507/69/262/347 sums to 1531: '507' is a typo, DO = 176 derived. UNLESS SAFE row 267/542/61/357/268 sums to 1495: the 267/268 margins are copied from the OVERTAKE row, should be 120. OVERTAKE row 267/665/268 is TM3-11C's MARKED row; OVERTAKE 95 E is 732 by AS 1744 -> expect kept at the drawing's 665, generator mismatch is expected |
| TM3-13A | GRAVEL_ROAD_YELLOW_SQUARE | spec | DRAWING: GRAVEL row 55/358/56 sums to 469; margins are right, 358 is ROUGH's width; GRAVEL = 489 derived (= AS 1744) |
| TM3-13B | GRAVEL_ROAD_YELLOW_LONG_SKINNY | spec | DRAWING: row 122/627/71/358/122 sums to 1300; GRAVEL = 527 derived ('627' typo; AS 1744 528) |
| TM3-14A | LOOSE_SURFACE_YELLOW_SQUARE | spec | |
| TM3-14B | LOOSE_SURFACE_YELLOW_LONG_SKINNY | spec | |
| TM3-16-1A | {speed}_KM_H_YELLOW_SQUARE | spec | numerals 160 E per drawing (not the R4-1 D/C rule), vary 5-130; km/h 110 Emod, width 460 checks |
| TM3-17A | NO_LINES_YELLOW_SQUARE | spec | |
| TM3-18A | LINE_MARKING_YELLOW_SQUARE | spec | LINE 120 C / MARKING 120 B as drawn |
| TM3-18B | LINE_MARKING_YELLOW_LONG_SKINNY | spec | |
| TM3-19B | LOOSE_STONES_YELLOW_LONG_SKINNY | spec | |
| TM3-20A | WET_BITUMEN_YELLOW_SQUARE | spec | DRAWING: WET labelled 160 C but stated width 377 is Series D (D 378, C 322); D used |
| TM3-21A | WATER_OVER_ROAD_YELLOW_SQUARE | spec | width rows are in reverse order (409 = WATER, 321 = OVER) |
| TM3-22B | DUE_TO_FLOODING_YELLOW_LONG_SKINNY | spec | GENERATOR: word gaps differ (54, 66) but a text element has one `gap`; entered as two left-aligned elements (x 70 and x 549) from the drawing's dims. A per-pair `gaps` list would let this be one centred element |
| TM3-23B | FALLEN_ROCKS_YELLOW_LONG_SKINNY | spec | DRAWING: row 85/406/81/452/86 sums to 1110; FALLEN = 496 derived ('406' typo; AS 1744 506) |
| TM3-24A | ROAD_FLOODED_YELLOW_SQUARE | spec | DRAWING: both lines labelled 120 D but widths 331 / 466 are 120 C / 120 B (D would be 402 / 573); C and B used (same pattern as TM3-18A) |
| TM3-25A | DEEP_EDGE_DROP_YELLOW_SQUARE | spec | |
| TM4-3C | END_BLASTING_AREA_RED_LONG | spec | white letters on red, black border |
| TM4-5C | POWER_LINE_WORKS_IN_PROGRESS_YELLOW_LONG | spec | |
| TM4-6A | SMOKE_HAZARD_YELLOW_SQUARE | spec | |
| TM4-6B | SMOKE_HAZARD_YELLOW_LONG_SKINNY | spec | |
| TM4-8A | UHF_CHANNEL_YELLOW_SQUARE | spec | channel number varies: drawing shows a dashed 4-digit '8888' placeholder (110 D, 'Varies'); transcribed literally as 8888 per instructions - decide what real values to vary over (UHF CB channels are 1-80). DRAWING: UHF/CHANNEL labelled 100 D but widths 207/498 are Series C (D = 246/598); C used |
| TM4-8B | UHF_CHANNEL_YELLOW_LONG_SKINNY | spec | placeholder '888' 100 C transcribed literally. GENERATOR: whole group '= 207 52 498 75 Varies =' is centred but gaps differ; entered as two left-aligned elements with x 88 computed from the font width of '888' (192) - a group-centring / per-pair gaps feature would avoid the hand calculation, and any other channel value shifts the group |
| TM4-9A | BUSH_FIRE_YELLOW_SQUARE | spec | |
| TM4-9B | BUSH_FIRE_YELLOW_LONG_SKINNY | spec | DRAWING: labelled 130 C but widths 421/344 are Series D (C = 358/293); D used |
| TM4-10A | HAZARDOUS_MATERIAL_YELLOW_SQUARE | spec | DRAWING: HAZARDOUS row 51/362/51 sums to 464; HAZARDOUS = 498 derived ('362' typo; AS 1744 497) |
| TM5-1B(L) | DETOUR_LEFT_YELLOW_LONG_SKINNY | needs-symbol tm5-1b_arrow_left | arrow box 182x182 at (124,59); DETOUR 120 E left-aligned at 406 |
| TM5-1B(R) | DETOUR_RIGHT_YELLOW_LONG_SKINNY | needs-symbol tm5-1b_arrow_left | same artwork with flip h at (894,59) |
| TM5-1B(S) | DETOUR_STRAIGHT_YELLOW_LONG_SKINNY | needs-symbol tm5-1b_arrow_up | arrow box 160x182 at (916,59) |
| TM5-6A | LEFT_ARROW_YELLOW_SQUARE | needs-symbol tm5-6a_arrow_left | inset gives head 262 x 400, shaft 192 x 125, R18 tip, notch 35/92 but not every vertex is fixed, so symbol not polygon |
| TM5-7A | DETOUR_YELLOW_SQUARE | spec | DRAWING: stray bottom row 92/415/93 with no legend line (TM4-6A's HAZARD row); ignored |
| TM5-7B | DETOUR_YELLOW_LONG_SKINNY | spec | |
| TM5-8B | LEFT_ARROW_YELLOW_LONG_SKINNY | needs-symbol tm5-8b_arrow_left | box 900x220 at (150,40); only the 50 grid given |
| TM5-9A | ON_SIDE_ROAD_YELLOW_SQUARE | spec | |
| TM5-9B | ON_SIDE_ROAD_YELLOW_LONG_SKINNY | spec | three words, equal gaps 65 |
| TM5-10B(L) | ON_SIDE_ROAD_LEFT_YELLOW_LONG_SKINNY | needs-symbol tm5-10b_arrow_left | arrow box 166x145 at (75,78); text 110 C left-aligned at 291 |
| TM5-10B(R) | ON_SIDE_ROAD_RIGHT_YELLOW_LONG_SKINNY | needs-symbol tm5-10b_arrow_left | same artwork flip h at (959,78) |
| TM5-11C(L) | DETOUR_FOR_HEAVY_VEHICLES_LEFT_YELLOW_LONG | spec | chevron as polygon: tip (75,300), notch (190,300), arm ends vertical at x 329, outer corners y 47/553; inner-end y 161.55/438.45 ASSUMES inner edges parallel to outer (not stated) - switch to a symbol if not accepted. FOR 80 C shares DETOUR's baseline (top 170) |
| TM5-11C(R) | DETOUR_FOR_HEAVY_VEHICLES_RIGHT_YELLOW_LONG | spec | mirror of (L), coordinates entered explicitly (separate PNG, no `hands`) |
| TM5-12C(L) | DETOUR_FOR_HIGH_VEHICLES_LEFT_YELLOW_LONG | spec | same chevron assumption as TM5-11C |
| TM5-12C(R) | DETOUR_FOR_HIGH_VEHICLES_RIGHT_YELLOW_LONG | spec | mirror of (L) |

## Symbols needed (tools/symbols/<id>.svg)
tm3-3a_slippery_car, tm3-9a_loose_stones, tm5-1b_arrow_left, tm5-1b_arrow_up, tm5-6a_arrow_left, tm5-8b_arrow_left, tm5-10b_arrow_left.

## Generator features that would have helped (not worked around by guessing)
* Per-pair word gaps on one text element (`gaps: [54, 66]`), used by TM3-22B and TM4-8B (and TM5-11C/12C if DETOUR ... FOR were treated as one line).
* Centring a group of mixed-gap words as a whole (TM4-8B), so the left x need not be computed from the font width by hand.
* A `series` for numerals stated as E (TM3-16-1A) is fine as plain `"E"`; no change needed, noted only because `"speed"` hard-codes D/C.
