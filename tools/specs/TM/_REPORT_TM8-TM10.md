# TM8 / TM9 / TM10 transcription report

55 drawings. Status: **spec** = renders and every text width matches the drawing; **needs-symbol** = spec complete but the generator is BLOCKED until `tools/symbols/<id>.svg` is traced (text widths on those signs were checked separately and match). No drawing skipped.

Generator run (`tools/signgen.py tools/specs/TM/TM8-*.json TM9-*.json TM10-*.json`): 24 files written, 0 width mismatches, 31 blocked on symbols.

| Code | Name | Status | Flags |
|---|---|---|---|
| TM8-1C | PEDESTRIANS_WATCH_YOUR_STEP_YELLOW_LONG | spec | |
| TM8-2B(L) | PEDESTRIANS_LEFT_YELLOW_LONG_SKINNY | needs-symbol tm8-2b_arrow | |
| TM8-2B(R) | PEDESTRIANS_RIGHT_YELLOW_LONG_SKINNY | needs-symbol tm8-2b_arrow | (R) uses the (L) arrow with `flip:h` (insets are mirror images) |
| TM8-3A | USE_OTHER_FOOTPATH_YELLOW_SQUARE | spec | DRAWING: all lines labelled 100 D but widths 156/271/424 are exactly 100 B (D would not fit); B used |
| TM8-4A | FOOTPATH_CLOSED_WHITE_SQUARE | spec | |
| TM8-5C | LOOK_BOTH_WAYS_TWO_WAY_TRAFFIC_YELLOW_LONG | needs-symbol tm8-5c_two_way_arrows | GENERATOR: TWO-WAY 65 D renders 439.6 vs drawing 368 - FHWA font hyphen has a 1.5 x cap-height advance (97.5 at 65) where the drawing leaves 368-157-177 = 34 for hyphen + spacing; no AS 1744 hyphen rule in the generator. Top-line gaps differ (39/37) so words placed by left edge |
| TM8-6A | LOOK_BOTH_WAYS_YELLOW_SQUARE | needs-symbol tm8-6a_two_way_arrows | DRAWING: LOOK labelled 100 C, width 322; C = 275, D = 329 - neither exact, D used (2.2 % off, will show as a width mismatch once the symbol exists) |
| TM8-7A | WATCH_YOUR_STEP_YELLOW_SQUARE | spec | |
| TM8-8A | PEDESTRIANS_SYMBOL_YELLOW_SQUARE | needs-symbol tm8-8a_pedestrians | extra 150/300/150 dimension under the sign not used |
| TM8-9A | FOOTPATH_CLOSED_AHEAD_YELLOW_SQUARE | spec | |
| TM8-10A | NARROW_FOOTPATH_AHEAD_YELLOW_SQUARE | spec | |
| TM8-11A | PATH_CLOSED_AHEAD_YELLOW_SQUARE | spec | DRAWING: PATH labelled 100 B but width 259 = 100 C; C used |
| TM8-12A | PATH_CLOSED_WHITE_SQUARE | spec | |
| TM8-13A | PEDESTRIAN_HAZARD_YELLOW_SQUARE | spec | DRAWING: HAZARD labelled 100 B but width 414 = 100 C (B = 340 as on TM8-13B); C used. PEDESTRIAN is 95 B, HAZARD 100, as drawn |
| TM8-13B | PEDESTRIAN_HAZARD_YELLOW_LONG_SKINNY | spec | |
| TM8-14A | CYCLING_HAZARD_YELLOW_SQUARE | spec | |
| TM8-14B | CYCLING_HAZARD_YELLOW_LONG_SKINNY | spec | DRAWING: labelled 100 B but widths 452/413 are 100 C (as TM8-14A); C used |
| TM8-15A | BICYCLE_LANE_CLOSED_AHEAD_YELLOW_SQUARE | spec | |
| TM8-16A | BICYCLE_LANE_CLOSED_WHITE_SQUARE | needs-symbol tm8-17a_bicycle | bicycle 295 x 195 has the same 1.51 aspect as TM8-17A's 454 x 300, so that id is reused at the smaller size |
| TM8-17A | BICYCLE_AHEAD_YELLOW_SQUARE | needs-symbol tm8-17a_bicycle | |
| TM8-18A | BICYCLE_SYMBOL_YELLOW_SQUARE | needs-symbol tm8-17a_bicycle | same 454 x 300 bicycle as TM8-17A |
| TM8-19C(L) | PEDESTRIANS_ACCESS_LEFT_YELLOW_LONG | needs-symbol tm8-2b_arrow tm8-19c_wheelchair | arrow heights not dimensioned (only width 168 and centrelines y 150 / 400): bbox 200 high so width governs. Lower arrow = same symbol flipped |
| TM8-19C(R) | PEDESTRIANS_ACCESS_RIGHT_YELLOW_LONG | needs-symbol tm8-2b_arrow tm8-19c_wheelchair | as (L); wheelchair not mirrored (inset faces right on both) |
| TM8-20B(L) | ACCESS_LEFT_YELLOW_LONG_SKINNY | needs-symbol tm8-2b_arrow tm8-19c_wheelchair | DRAWING: height labelled 600 but all vertical dims sum to 300 (4:1 drawn) - 1200 x 300 used. ACCESS labelled 100 C but width 494 = 100 D (TM8-19C labels it D); D used. Wheelchair height / vertical position not dimensioned (full-height bbox, width 188 governs) |
| TM8-20B(R) | ACCESS_RIGHT_YELLOW_LONG_SKINNY | needs-symbol tm8-2b_arrow tm8-19c_wheelchair | as (L) |
| TM9-1A | EVENT_AHEAD_YELLOWGREEN_SQUARE | spec | colour word YELLOWGREEN (not in the guide's list; matches the `yellowgreen` ground) |
| TM9-1B | EVENT_AHEAD_YELLOWGREEN_LONG_SKINNY | spec | DRAWING: 84+463+72+510+85 = 1214, not 1200 (widths themselves match 100 E) |
| TM9-2A | END_EVENT_YELLOWGREEN_SQUARE | spec | |
| TM9-2B | END_EVENT_YELLOWGREEN_LONG_SKINNY | spec | |
| TM9-3A | EVENT_IN_PROGRESS_YELLOWGREEN_SQUARE | spec | DRAWING: EVENT labelled B but width 325 = C; PROGRESS labelled C but width 440 = B (letters look swapped) - C/C/B used. IN width labelled 408 (254+408+254 = 916); expect set to 600-254-254 = 92 (= 100 C) |
| TM9-3B | EVENT_IN_PROGRESS_YELLOWGREEN_LONG_SKINNY | spec | DRAWING: labelled 100 E but widths 256/78/440 are exactly 100 B and letters are drawn condensed; B used. Gaps differ (60/68) so words placed by left edge |
| TM9-4B | EVENT_ON_SIDE_ROAD_YELLOWGREEN_LONG_SKINNY | spec | gaps differ (57/62/62): words placed by left edge |
| TM9-4C | EVENT_ON_SIDE_OF_ROAD_YELLOWGREEN_LONG | spec | bottom-line gaps differ (65/63/62): words placed by left edge |
| TM9-5B(L) | ON_SIDE_ROAD_LEFT_YELLOWGREEN_LONG_SKINNY | needs-symbol tm8-2b_arrow | arrow 166 x 145 identical to TM8-2B(L); id reused |
| TM9-5B(R) | ON_SIDE_ROAD_RIGHT_YELLOWGREEN_LONG_SKINNY | needs-symbol tm8-2b_arrow | flipped |
| TM9-6C | COMMUNITY_EVENT_AHEAD_YELLOWGREEN_LONG | spec | |
| TM9-7A | CYCLIST_YELLOWGREEN_SQUARE | needs-symbol tm9-7a_cyclist | |
| TM9-8A | RUNNER_YELLOWGREEN_SQUARE | needs-symbol tm9-8a_runner | |
| TM10-1A | UP_ARROW_YELLOW_SQUARE | needs-symbol tm10-1a_up_arrow | arrow width not dimensioned: 2 grid squares = 100 (per guide) |
| TM10-2A | LANE_CLOSED_BAR_YELLOW_SQUARE | spec | T symbol fully dimensioned - drawn as two `rect`s |
| TM10-3A | LEFT_LANE_CLOSED_YELLOW_SQUARE | needs-symbol tm10-1a_up_arrow | stem x only given as its 58 width; centred under the bar as on TM10-2A |
| TM10-4A | RIGHT_LANE_CLOSED_YELLOW_SQUARE | needs-symbol tm10-1a_up_arrow | as TM10-3A |
| TM10-5A | TWO_UP_ARROWS_YELLOW_SQUARE | needs-symbol tm10-1a_up_arrow | |
| TM10-6A | TWO_LANES_CLOSED_YELLOW_SQUARE | spec | rects; stems centred under bars (only widths given) |
| TM10-7A | LEFT_TURN_ARROW_LANE_CLOSED_YELLOW_SQUARE | needs-symbol tm10-7a_left_turn_arrow | outer top dims print as "5" but must be 50 (sum 600). Bar/stem as rects (stem 53 wide here) |
| TM10-8A | RIGHT_TURN_ARROW_LANE_CLOSED_YELLOW_SQUARE | needs-symbol tm10-7a_left_turn_arrow | mirror of 7A, symbol flipped |
| TM10-9A | LEFT_TURN_WEDGE_LANE_CLOSED_YELLOW_SQUARE | needs-symbol tm10-9a_left_turn_arrow_wedge | DRAWING: left stack 176+320+105 = 601. Arrow 198 / wedge 201 wide - one combined symbol, bbox 201 wide (wedge alone is not dimensioned) |
| TM10-10A | RIGHT_TURN_WEDGE_LANE_CLOSED_YELLOW_SQUARE | needs-symbol tm10-9a_left_turn_arrow_wedge | mirror of 9A (also 601), flipped |
| TM10-11A | CURVE_RIGHT_ARROW_YELLOW_SQUARE | needs-symbol tm10-11a_curve_arrow_right | |
| TM10-12A | CURVE_LEFT_ARROW_YELLOW_SQUARE | needs-symbol tm10-11a_curve_arrow_right | identical dims, inset is the mirror image - flipped |
| TM10-13A | TWO_LANE_SHIFT_LEFT_YELLOW_SQUARE | needs-symbol tm10-13a_two_lane_shift_left | DRAWING: 60+410+61 = 601 |
| TM10-14A | TWO_LANE_SHIFT_RIGHT_YELLOW_SQUARE | needs-symbol tm10-13a_two_lane_shift_left | mirror of 13A (also 601), flipped |
| TM10-15A | LANE_SHIFT_LEFT_YELLOW_SQUARE | needs-symbol tm10-15a_lane_shift_left | |
| TM10-16A | LANE_SHIFT_RIGHT_YELLOW_SQUARE | needs-symbol tm10-15a_lane_shift_left | mirror of 15A, flipped |
| TM10-17A | MERGE_RIGHT_ARROW_YELLOW_SQUARE | needs-symbol tm10-17a_merge_arrow | |

## Counts
* spec (renders, widths ok): 24
* needs-symbol: 31
* skipped: 0

## Symbols to trace (15 ids, all on the drawings' 50 mm grid insets)
tm8-2b_arrow (TM8-2B(L)), tm8-5c_two_way_arrows, tm8-6a_two_way_arrows, tm8-8a_pedestrians, tm8-17a_bicycle, tm8-19c_wheelchair (TM8-19C(L)), tm9-7a_cyclist, tm9-8a_runner, tm10-1a_up_arrow, tm10-7a_left_turn_arrow, tm10-9a_left_turn_arrow_wedge, tm10-11a_curve_arrow_right, tm10-13a_two_lane_shift_left, tm10-15a_lane_shift_left, tm10-17a_merge_arrow.
Reuse decisions (my judgement, not stated on the drawings): the (R) / right-hand variants use the (L) symbol with `flip:h`; the 166 x 145 arrow of TM8-2B is also used for TM9-5B (identical dims) and, at 168 wide, for TM8-19C / TM8-20B; the TM8-17A bicycle is reused for TM8-18A (identical) and TM8-16A (same aspect ratio, smaller). If any inset is found to differ, give that sign its own id.

## Flags summary
Drawing inconsistencies: TM8-3A, TM8-6A, TM8-11A, TM8-13A, TM8-14B, TM8-20B(L)/(R) (series letters vs stated widths; 20B height 600 vs 300); TM9-1B (dims sum 1214); TM9-3A (series swapped, IN width 408); TM9-3B (E vs B); TM10-9A/10A, TM10-13A/14A (601 vertical sums); TM10-7A/8A ("5" = 50).
Generator features missing: (1) AS 1744 hyphen width/spacing - TM8-5C TWO-WAY cannot match. (2) Per-word gaps on one line (the `words` element has a single `gap`) - worked around exactly by placing each word with `align:left,x` from the drawing (TM8-5C, TM9-3B, TM9-4B, TM9-4C). (3) Symbols whose height is not dimensioned (TM8-19C/20B arrows, TM8-20B wheelchair) rely on the bbox "fit and centre" behaviour; there is no "anchor on a centreline" option.
Undimensioned placements (noted in specs): TM10-3A/4A/6A stem x (centred under bar), TM10-1A-family arrow width (grid), TM8-8A extra 300 dimension unused.
