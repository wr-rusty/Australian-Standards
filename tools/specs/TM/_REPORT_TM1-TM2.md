# TM1 / TM2 transcription report (AS 1743-2023)

97 drawings. Status: 86 spec, 11 needs-symbol, 0 skipped.
Generator run (`tools/signgen.py tools/specs/TM/TM1-*.json tools/specs/TM/TM2-*.json`): 86 files written; the 2 remaining width
mismatches (TM1-10A, TM1-27C) are drawing dimensions inconsistent with AS 1744 spacing and are explained in those specs' notes.
Specs for TM1-1A/1B/1C, TM2-4A/4B/4C, TM2-17A were pre-existing and left untouched.

| Code | Name | Status | Flags |
|---|---|---|---|
| TM1-1A | ROADWORK_YELLOW_SQUARE | spec (pre-existing) | |
| TM1-1B | ROADWORK_YELLOW_LONG_SKINNY | spec (pre-existing) | |
| TM1-1C | ROADWORK_YELLOW_LONG | spec (pre-existing) | |
| TM1-2A | BRIDGE_WORK_AHEAD_YELLOW_SQUARE | spec | two top dim rows (350, 450) assigned by width: BRIDGE 450, WORK 350 |
| TM1-2C | BRIDGEWORK_AHEAD_YELLOW_LONG | spec | |
| TM1-3-1A | ROAD_PLANT_AHEAD_YELLOW_SQUARE | spec | |
| TM1-3-1C | ROAD_PLANT_AHEAD_YELLOW_LONG | spec | DRAWING: line 1 labelled 155 D but widths 427/514 are Series C (D would total 1227 > sign width); C used |
| TM1-4A | GRADER_AHEAD_YELLOW_SQUARE | spec | |
| TM1-4C | GRADER_AHEAD_YELLOW_LONG | spec | DRAWING: GRADER labelled 155 D but width 919 is Series E (D = 780); E used |
| TM1-5A | WORKER_ORANGE_SQUARE | needs-symbol tm1-5a_worker | |
| TM1-5C | WORKER_ORANGE_LONG | needs-symbol tm1-5a_worker | same symbol as TM1-5A, bbox 325,67 547x466 |
| TM1-6A | DETOUR_AHEAD_YELLOW_SQUARE | spec | |
| TM1-6B | DETOUR_AHEAD_YELLOW_LONG_SKINNY | spec | |
| TM1-10A | TRAFFIC_HAZARD_YELLOW_SQUARE | spec | DRAWING: TRAFFIC 100 C dimensioned 412; AS 1744 gives 428 and TM1-46A dimensions the same word 426 (412 = DETOUR on TM1-6A). Width mismatch explained in notes |
| TM1-10C | TRAFFIC_HAZARD_YELLOW_LONG | spec | |
| TM1-18A | PREPARE_TO_STOP_RED_SQUARE | spec | DRAWING: caption says "red letters on red ground"; letters drawn white, white used |
| TM1-18B | PREPARE_TO_STOP_RED_LONG_SKINNY | spec | caption as 18A; word gaps differ (70/75) so words placed left-aligned from cumulative dims (see GENERATOR note 1) |
| TM1-25C | ROADWORK_ON_SIDE_ROAD_YELLOW_LONG | spec | line 2 gaps differ (90/93): words placed left-aligned from cumulative dims (GENERATOR note 1) |
| TM1-27C | ROAD_PLANT_ON_SIDE_ROAD_YELLOW_LONG | spec | line 2 gaps differ (79/78): left-aligned placement (GENERATOR note 1). DRAWING: ON 185 / SIDE 324 (140 C) vs AS 1744 189 / 331 (~2 %), explained in notes |
| TM1-28A | NEXT_2_KM_YELLOW_SQUARE | spec | numeral varies (drawn 2 used). Numeral vertical position not dimensioned: baseline-aligned with km assumed. Line hand-centred (GENERATOR note 2) |
| TM1-28B | NEXT_2_KM_YELLOW_LONG_SKINNY | spec | numeral varies (drawn 2 used). DRAWING: gap numeral-km not dimensioned (=|368|75|Varies|175|=); 45 taken from TM1-28A. Hand-centred (GENERATOR note 2) |
| TM1-30A | TRAFFIC_SIGNALS_YELLOW_SQUARE | needs-symbol tm1-30a_traffic_signals | |
| TM1-32A | SIDE_ROAD_CLOSED_YELLOW_SQUARE | spec | |
| TM1-34A | TRAFFIC_CONTROLLER_ORANGE_SQUARE | needs-symbol tm1-34a_traffic_controller | |
| TM1-35C | STOP_HERE_WHEN_REDIRECTED_WHITE_LONG | spec | DRAWING: STOP HERE labelled 150 C but widths 468/478 are Series D (C = 395/405); D used |
| TM1-36B | 200_M_AHEAD_YELLOW_LONG_SKINNY | spec | numeral varies (drawn 200 used). DRAWING INCONSISTENT: vertical dims 115 / 120 D / 100 sum to 335 not 300 (115 and 100 copied from TM1-28B); illustration shows the line centred, so top 90 used - please confirm. Hand-centred line (GENERATOR note 2) |
| TM1-37C | SURVEYORS_AHEAD_ORANGE_LONG | spec | |
| TM1-38A | SPEED_HUMP_AHEAD_YELLOW_SQUARE | needs-symbol tm1-38a_speed_hump_ahead | arrow + hump dimensioned as one 426x344 group; hump artwork probably same as TM2-51A |
| TM1-39A | SIGNAL_WORKS_AHEAD_YELLOW_SQUARE | spec | two top dim rows (427, 458) assigned by width: SIGNAL 458, WORKS 427 |
| TM1-40A | LINE_MARKING_AHEAD_YELLOW_SQUARE | spec | DRAWING: caption says orange ground, drawing coloured yellow; yellow used |
| TM1-41A | MOWING_AHEAD_YELLOW_SQUARE | spec | |
| TM1-42A | TRAM_WORKS_AHEAD_YELLOW_SQUARE | spec | |
| TM1-43A | ROAD_CLOSED_AHEAD_YELLOW_SQUARE | spec | |
| TM1-43C | ROAD_CLOSED_AHEAD_YELLOW_LONG | spec | |
| TM1-44A | BURNING_OFF_AHEAD_YELLOW_SQUARE | spec | |
| TM1-44C | BURNING_OFF_AHEAD_YELLOW_LONG | spec | DRAWING: lines labelled 150 D / 155 D but widths are 150 C (705/291) and 155 E (792); C and E used |
| TM1-45A | TRAFFIC_INCIDENT_AHEAD_YELLOW_SQUARE | spec | two top dim rows (488, 512) assigned by width: TRAFFIC 512 (D), INCIDENT 488 (C) |
| TM1-45C | TRAFFIC_INCIDENT_AHEAD_YELLOW_LONG | spec | two top dim rows (733, 669) assigned by width: TRAFFIC 669, INCIDENT 733 |
| TM1-46A | QUEUED_TRAFFIC_AHEAD_YELLOW_SQUARE | spec | |
| TM1-47A | QUEUED_TRAFFIC_YELLOW_SQUARE | needs-symbol tm1-47a_queued_cars | symbol has red tail lights (colour inside artwork) |
| TM1-49A | ROAD_SIDE_HAZARD_YELLOW_SQUARE | spec | |
| TM1-50A | WATCH_FOR_WANDERING_ANIMALS_YELLOW_SQUARE | spec | DRAWING INCONSISTENT: vertical dims 80/80/80/80/80/80/100 sum to 580; tops taken from the top edge (80, 240, 400) |
| TM1-51B | AHEAD_YELLOW_LONG_SKINNY | spec | |
| TM2-4A | ROAD_CLOSED_WHITE_SQUARE | spec (pre-existing) | |
| TM2-4B | ROAD_CLOSED_WHITE_LONG_SKINNY | spec (pre-existing) | |
| TM2-4C | ROAD_CLOSED_WHITE_LONG | spec (pre-existing) | |
| TM2-17A | END_ROAD_WORK_YELLOW_SQUARE | spec (pre-existing) | |
| TM2-17C | END_ROADWORK_YELLOW_LONG | spec | |
| TM2-23A | END_DETOUR_YELLOW_SQUARE | spec | |
| TM2-23C | END_DETOUR_YELLOW_LONG | spec | |
| TM2-24A | TWO_WAY_ARROWS_YELLOW_SQUARE | needs-symbol tm2-24a_two_way_arrows | |
| TM2-25A | TRUCK_YELLOW_SQUARE | needs-symbol tm2-25a_truck | |
| TM2-26A | ROAD_WORK_YELLOW_SQUARE | spec | |
| TM2-26B | ROADWORK_YELLOW_LONG_SKINNY | spec | name collides with TM1-1B's (code suffix keeps files distinct) |
| TM2-26C | ROADWORK_YELLOW_LONG | spec | name collides with TM1-1C's (code suffix keeps files distinct) |
| TM2-27A | BRIDGE_WORK_YELLOW_SQUARE | spec | |
| TM2-27B | BRIDGEWORK_YELLOW_LONG_SKINNY | spec | |
| TM2-27C | BRIDGEWORK_YELLOW_LONG | spec | |
| TM2-28A | END_BRIDGE_WORK_YELLOW_SQUARE | spec | DRAWING: END, BRIDGE labelled 100 C but widths 240/452 are Series D; D used |
| TM2-29A | TRENCHING_WORKS_YELLOW_SQUARE | spec | |
| TM2-29B | TRENCHING_WORKS_YELLOW_LONG_SKINNY | spec | |
| TM2-30B | MOWING_YELLOW_LONG_SKINNY | spec | |
| TM2-31A | LITTER_COLLECTION_YELLOW_SQUARE | spec | |
| TM2-31B | LITTER_COLLECTION_YELLOW_LONG_SKINNY | spec | |
| TM2-32A | UTILITY_REPAIRS_YELLOW_SQUARE | spec | |
| TM2-32B | UTILITY_REPAIRS_YELLOW_LONG_SKINNY | spec | |
| TM2-33A | EMERGENCY_WORKS_YELLOW_SQUARE | spec | |
| TM2-33B | EMERGENCY_WORKS_YELLOW_LONG_SKINNY | spec | |
| TM2-34A | SURVEY_WORKS_YELLOW_SQUARE | spec | |
| TM2-35B | SURVEYORS_ORANGE_LONG_SKINNY | spec | |
| TM2-36A | ROAD_PLATES_IN_USE_YELLOW_SQUARE | spec | |
| TM2-36C | ROAD_PLATES_IN_USE_YELLOW_LONG | spec | |
| TM2-37A | POWER_LINE_WORKS_YELLOW_SQUARE | spec | DRAWING: POWER, LINE labelled 100 C but widths 415/271 are Series D; D used |
| TM2-37C | POWERLINE_WORKS_YELLOW_LONG | spec | DRAWING: both lines labelled 140 C but widths 984/598 are Series D; D used |
| TM2-38A | ON_RAMP_YELLOW_SQUARE | spec | |
| TM2-38B | ON_RAMP_YELLOW_LONG_SKINNY | spec | |
| TM2-39A | MERGE_LEFT_YELLOW_SQUARE | spec | |
| TM2-39B | MERGE_LEFT_YELLOW_LONG_SKINNY | spec | |
| TM2-40A | MERGE_RIGHT_YELLOW_SQUARE | spec | |
| TM2-40B | MERGE_RIGHT_YELLOW_LONG_SKINNY | spec | |
| TM2-41A | LOCAL_ACCESS_ONLY_YELLOW_SQUARE | spec | |
| TM2-42A | SLOW_MOVING_VEHICLE_YELLOW_SQUARE | spec | |
| TM2-43A | SIDE_ROAD_CLOSED_YELLOW_SQUARE | spec | same legend as TM1-32A with a different vertical layout (80/70/70/80 vs 85/65/65/85) |
| TM2-44A | CHANGED_TRAFFIC_CONDITIONS_YELLOW_SQUARE | spec | two top dim rows (427, 499) assigned by width: CHANGED 499, TRAFFIC 427 |
| TM2-45A | OVERSIZE_VEHICLE_YELLOW_SQUARE | spec | DRAWING: labelled 95 D but widths 485/428 are Series C; C used |
| TM2-46A | HEAVY_VEHICLES_YELLOW_SQUARE | spec | |
| TM2-47A | HIGH_VEHICLES_YELLOW_SQUARE | spec | |
| TM2-48A | TRAFFIC_SIGNALS_NOT_IN_USE_YELLOW_SQUARE | needs-symbol tm1-30a_traffic_signals | red cross drawn as two polygons (500 x 25, 40 deg included); crossing point not dimensioned, panel centre assumed. Caption says "black symbol", bars drawn red |
| TM2-49A | SIGNALS_NOT_IN_USE_YELLOW_SQUARE | spec | |
| TM2-50A | SIGNALS_UNDER_REPAIR_YELLOW_SQUARE | spec | |
| TM2-51A | SPEED_HUMP_YELLOW_SQUARE | needs-symbol tm2-51a_speed_hump | DRAWING INCONSISTENT: vertical dims 50/107/50 sum to 207; illustration centred, y = 246.5 used |
| TM2-52A | BOOM_GATE_YELLOW_SQUARE | needs-symbol tm2-52a_boom_gate | red disc and hatched arm inside the artwork; caption says "black symbol" |
| TM2-53A | KEEP_TRACKS_CLEAR_YELLOW_SQUARE | spec | |
| TM2-54A | TRAM_ONLY_YELLOW_SQUARE | spec | DRAWING: labelled 100 D but widths 397/399 are Series E (TRAM 100 E = 397 on TM2-55A, 100 D = 330 on TM1-42A); E used |
| TM2-55A | TRAM_WORKS_YELLOW_SQUARE | spec | |
| TM2-56A | END_TRAM_WORKS_YELLOW_SQUARE | spec | |
| TM2-57C | FOR_ROADWORK_ENQUIRIES_YELLOW_LONG | spec | phone number varies; drawn placeholder 12345678 used. PH: left-aligned at 146, number centred between end of PH: and right edge (cx 771) per "=|Varies|=" |

## Generator features needed (not worked around by guessing)

1. **Unequal gaps between words on one line.** `words`/`gap` supports a single gap. TM1-18B (70/75), TM1-25C (90/93), TM1-27C (79/78)
   are written as separate left-aligned `text` elements at x positions summed from the drawing's cumulative dims. A `gaps: [..]`
   list on a `words` element would let these be centred normally.
2. **Per-word series / height on one line.** TM1-28A, TM1-28B (numeral 100 E + km 85 Emod) and TM1-36B (numeral 120 E + m 100 Emod
   + AHEAD 120 D) mix series and heights on one baseline. They are written as separate left-aligned elements whose x positions
   were hand-centred using the generator's own ink widths (numeral 2 @100 E = 81.0, 200 @120 E = 343.4) plus the drawing's
   gaps and word widths; the arithmetic is in each spec's notes. Because the numeral varies, these cannot use `vary` until the
   generator can centre a mixed-series line itself (e.g. `words` entries as objects `{text, series, height, top}`).
3. Nothing else missing; polygons covered the TM2-48A cross bars.

## Drawing inconsistencies summary
* Series label vs dimensioned width (width wins, noted in spec): TM1-3-1C, TM1-4C, TM1-35C, TM1-44C, TM2-28A, TM2-37A, TM2-37C, TM2-45A, TM2-54A.
* Width not matching AS 1744 spacing (drawing kept, mismatch explained): TM1-10A (TRAFFIC 412 vs 428), TM1-27C (ON/SIDE ~2 %).
* Vertical dims do not sum to the panel height: TM1-36B (335/300), TM1-50A (580/600), TM2-51A (207/600).
* Caption colour vs drawing: TM1-18A/18B (letters white not red), TM1-40A (ground yellow not orange), TM2-48A / TM2-52A / TM1-47A (red parts in "black" symbols).
* Undimensioned values needed: TM1-28A numeral vertical position (baseline assumed), TM1-28B numeral-km gap (45 from TM1-28A), TM2-48A cross centre (panel centre).
