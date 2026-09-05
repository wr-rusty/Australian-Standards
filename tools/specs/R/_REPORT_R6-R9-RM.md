# R6 / R7 / R8 / R9 / RM drawings — transcription report

96 drawings, 96 specs written (`tools/specs/R/<CODE>.json`). Status: **70 spec**, **26 needs-symbol**, **0 skipped**.
Generator run: `tools/signgen.py tools/specs/R/*.json` -> 130 files written; every remaining width mismatch is explained below and in that spec's `notes`.
"Illust." size used throughout; where a size table exists the illustrated variant is named in `notes`.

## Per drawing

| code | name | status | flags |
|---|---|---|---|
| R6-1 | NO_OVERTAKING_OR_PASSING_WHITE_TALL | spec | |
| R6-2 | NO_OVERTAKING_ON_BRIDGE_WHITE_TALL | spec | |
| R6-3 | BRIDGE_LOAD_LIMIT_80_t_GROSS_WHITE_TALL | spec | tonnes vary (80 shown). Drawing: t width 52 but "85 Emod" gives 44 (52 = Emod 100) — stated 85 kept, width mismatch remains. |
| R6-4 | GROSS_LOAD_LIMIT_80_t_WHITE_TALL | spec | tonnes vary (80 shown). |
| R6-6 | STOP_HERE_ON_RED_SIGNAL_RED_TALL | spec | Top dimension lines assigned nearest-first (STOP 316, HERE 324); the other way round mismatches AS 1744 by 2.5 %. |
| R6-7 | STOP_ORANGE_ROUND | spec | |
| R6-8 | STOP_RED_ROUND | spec | |
| R6-9 | STOP_ON_RED_SIGNAL_WHITE_TALL | spec | |
| R6-10-1 | NO_BUSES_WHITE_SQUARE | needs-symbol r6-10-1_bus | Annulus and 45° bar drawn (annulus + polygon with corners on R294). |
| R6-10-2 | NO_TRUCKS_WHITE_SQUARE | needs-symbol r6-10-2_truck | |
| R6-10-3 | NO_BICYCLES_WHITE_SQUARE | needs-symbol r6-10-3_bicycle | R6-10-3B (600) is the illustrated size. |
| R6-11 | LOW_CLEARANCE_8.8_m_WHITE_WIDE | spec | metres vary (8.8 shown). Decimal point spaced 28/28/28 as drawn, via runs 8 . 8 m. |
| R6-12 | CLEARANCE_3.3_m_WHITE_WIDE | spec | metres vary (3.3 shown). |
| R6-13 | NO_PEDESTRIANS_BICYCLES_ANIMALS_WHITE_TALL | spec | |
| R6-14 | STOP_HERE_ON_RED_ARROW_RED_TALL | spec | STOP 316 / HERE 324 as R6-6. |
| R6-15 | NO_PEDESTRIANS_WHITE_SQUARE | needs-symbol r6-15_pedestrian | Size table labels the illustrated 450 size "R6-14B" (typo). Bar carries an unexplained "29" beside its 38 width (not the half-width) — bar drawn centred, 38 wide. |
| R6-16 | LOW_CLEARANCE_3.6_m_WHITE_WIDE_SKINNY | spec | metres vary (3.6 shown). Numeral series not stated separately (D taken from the line note); drawing gives a 315 block for the variable numerals — used as a `slot`. |
| R6-17 | BRIDGE_LOAD_LIMIT_PER_AXLE_GROUP_WHITE_LONG | spec | tonnes vary (8/10/15 shown). Only whole-line widths given; word gaps derived (78.6, 26.2, 60.9, 70.5). TRI-AXLE drawn 435 but 80 D gives 528 — no per-word expect set. Numeral-to-t gap NOT dimensioned — 30 used (as R6-3). |
| R6-18 | BUSES_MUST_ENTER_WHITE_TALL | spec | |
| R6-19 | START_FREEWAY_GREEN_LONG | spec | |
| R6-20 | FREEWAY_ENTRANCE_GREEN_LONG | spec | |
| R6-21 | END_FREEWAY_GREEN_LONG | spec | |
| R6-22 | TRUCKS_AND_BUSES_MUST_USE_LOW_GEAR_WHITE | spec | |
| R6-23 | END_TRUCK_AND_BUS_LOW_GEAR_AREA_WHITE | spec | Drawing: & = 100 wide at 115 C; FHWA font & = 115 — width mismatch remains. |
| R6-25 | RAILWAY_CROSSING_CROSSBUCK_RED_LONG | needs-symbol r6-25_crossbuck | GENERATOR: no rotated text (letters run along the arms, non-standard spacing). Whole crossbuck (arms 1265/1035 × 212, 25 black border, 108 D letters) placed as one symbol filling the inner panel; arm angle/positions not fully resolvable from the dims read (74/106/990/180, 186/448/226, 394/378, 90, 11/14). |
| R6-26 | TRAMWAY_CROSSING_CROSSBUCK_RED_LONG | needs-symbol r6-26_crossbuck | As R6-25. |
| R6-27 | TRUCKS_MUST_ENTER_WHITE_TALL | spec | |
| R6-28 | TRUCKS_USE_LEFT_LANE_WHITE_SQUARE | spec | |
| R6-29 | KEEP_LEFT_UNLESS_OVERTAKING_WHITE_LONG | spec | R6-29C (2400×1200) illustrated. |
| R6-30 | MEDIAN_TURNING_LANE_WHITE_TALL | needs-symbol r6-30_curve_arrow_down_left, r6-30_curve_arrow_up_right | Arrow heights (274) dimensioned; widths and x-positions are NOT — width read from the 60 grid (~270) and centred. |
| R6-31 | BUS_GIVE_WAY_DECAL_WHITE_SQUARE | needs-symbol r6-31_bus_arrow_car (multi-colour) | Corner radius not stated (drawn rounded) — none applied. GIVE/WAY "centred on car graphic": car centre not dimensioned, read from the 22.5 grid (x 339). |
| R6-32 | END_KEEP_LEFT_UNLESS_OVERTAKING_WHITE | spec | |
| R6-33 | OVERALL_LENGTH_LIMIT_26_m_WHITE_TALL | spec | metres vary (26 shown). Top dimension lines assigned nearest-first (OVERALL 1024, LENGTH 852). |
| R7-1-1 | BUS_LANE_WHITE_TALL | needs-symbol r7-1-1_bus | |
| R7-1-3 | TRUCK_LANE_WHITE_TALL | needs-symbol r7-1-3_truck | |
| R7-1-4 | BICYCLE_LANE_WHITE_TALL | needs-symbol r7-1-4_bicycle | |
| R7-1-5 | TRAM_LANE_WHITE_TALL | needs-symbol r7-1-5_tram | |
| R7-1-6 | BUS_AND_OTHER_VEHICLE_LANE_WHITE_TALL | needs-symbol r7-1-1_bus | The "symbol for other vehicle type" is only a dashed placeholder box (180 high, variable width) — nothing placed there. |
| R7-2 | AHEAD_WHITE_WIDE | spec | Drawing says 100 E but AHEAD at E = 512 (4 mm clear of the border); drawn width 410 is closest to D (430) — D used, 5 % mismatch remains. |
| R7-3 | LEFT_OR_RIGHT_LANE_WHITE_LONG | spec | One drawing, both hands, different words (LEFT/RIGHT) — hand-keyed text elements. GENERATOR: no per-hand name substitution, so both files share one name. |
| R7-4 | END_WHITE_WIDE | spec | |
| R7-5 | DOWN_ARROW_WHITE_LONG | spec | Arrow as polygon from 396/272/88/196/36. R10 barb corners not applied (polygon radius is all-or-nothing). |
| R7-6-1(L) | LEFT_LANE_WHITE_WIDE | spec | |
| R7-6-1(R) | RIGHT_LANE_WHITE_WIDE | spec | |
| R7-6-2 | KERB_LANE_WHITE_WIDE | spec | |
| R7-6-3 | CENTRE_LANE_WHITE_LONG_SKINNY | spec | |
| R7-6-4 | THIS_LANE_DOWN_ARROW_WHITE_LONG_SKINNY | spec | Arrow as polygon (stem tapers 68→50, corners 141 above the tip, junction 17 lower). |
| R7-7-1 | T2_TRANSIT_LANE_WHITE_TALL | needs-symbol r7-7-1_t2_badge (red/white), r7-7_car_2 | Badge height not dimensioned here (207 on R7-9-1). |
| R7-7-2 | T3_TRANSIT_LANE_WHITE_TALL | needs-symbol r7-7-2_t3_badge, r7-7_car_3 | |
| R7-8 | BUS_ONLY_WHITE_TALL | needs-symbol r7-1-1_bus | Red panel width given as 50\|515\|50 (= 615 on a 600 sign) — 500 used. |
| R7-9-1 | END_T2_TRANSIT_LANE_WHITE_SQUARE | needs-symbol r7-7-1_t2_badge, r7-7_car_2 | |
| R7-9-2 | END_T3_TRANSIT_LANE_WHITE_SQUARE | needs-symbol r7-7-2_t3_badge, r7-7_car_3 | |
| R7-10 | TRAM_ONLY_WHITE_TALL | needs-symbol r7-1-5_tram | Same 50\|515\|50 panel inconsistency as R7-8 — 500 used. |
| R7-11-1 | TWO_WAY_ARROW_WHITE_WIDE | spec | Arrow polygon from 456/106/67/9/25; R5 barb tips not applied. |
| R7-11-2 | LEFT_ARROW_WHITE_WIDE | spec | |
| R7-11-3 | RIGHT_ARROW_WHITE_WIDE | spec | |
| R7-12 | 300_m_AHEAD_WHITE_LONG | spec | metres vary (300 shown). Drawing: m = 73 wide at "50 Emod" (font 55; 73 = Emod 66) — stated 50 kept, mismatch remains. |
| R8-1 | BICYCLES_ONLY_WHITE_TALL | needs-symbol r7-1-4_bicycle | |
| R8-2(b) | PEDESTRIANS_AND_BICYCLES_WHITE_TALL | needs-symbol r8-2_pedestrian, r8-2_bicycle | Drawing titled R8-2 (file R8-2(b)). No text. |
| R8-3 | BICYCLES_PEDESTRIANS_ONLY_ONLY_WHITE_SQUARE | needs-symbol r8-3_bicycle, r8-3_pedestrian | Both hands in one drawing; symbols face left in both hands so they are placed per hand with mirror:false rather than auto-mirrored. |
| R9-1-1 | 7-9_30_AM_MON-FRI_WHITE_LONG | spec | times vary. Dashes drawn as dimensioned rects (30×12, 30×8). AM drawn 75 wide vs AS 1744 80 (R9-1-2 gives 80) — mismatch remains. |
| R9-1-2 | 7-9_AM_4_30-6_30_PM_MON-FRI_WHITE_SQUARE | spec | times vary. Line-2 horizontal string sums to 447 (right group anchored from the right margin); left vertical string sums to 445 (MON-FRI centred on its dimensioned dash instead). |
| R9-1-3 | AT_ALL_TIMES_WHITE_LONG | spec | |
| R9-2 | BUSES_EXCEPTED_WHITE_LONG | spec | |
| R9-3A | BICYCLES_EXCEPTED_WHITE_LONG | spec | Drawing R9-3(A, B, C); A illustrated. |
| R9-3D | BICYCLES_EXCEPTED_WHITE_WIDE_SKINNY | spec | |
| R9-4 | AUTHORISED_VEHICLES_EXCEPTED_WHITE_LONG | spec | |
| R9-5 | ON_FREEWAY_WHITE_LONG | spec | |
| R9-6-1 | NEXT_300_m_WHITE_WIDE | spec | metres vary (300 shown). |
| R9-6-2 | NEXT_80_m_WHITE_LONG | spec | metres vary (80 shown). |
| R9-7-1 | NEXT_5_km_WHITE_WIDE_SKINNY | spec | Drawing shows an EMPTY numeral box (no value) — "5" used as on R9-7-2; varies. |
| R9-7-2 | NEXT_5_km_WHITE_LONG | spec | km vary (5 shown). |
| R9-8 | AT_PACIFIC_HIGHWAY_WHITE_SQUARE | spec | Road-name lines "letter series to suit", widths "Varies" — D assumed, PACIFIC HIGHWAY as shown. AT drawn 148 vs font 153 (3 %). |
| R9-9 | ONE_LANE_WHITE_LONG | spec | |
| R9-10-1 | VEHICLES_OVER_8.8_t_GVM_WHITE_LONG | spec | tonnes vary. Vertical string 60/100/50/100/60/80/60 sums to 510 on a 500 sign — tops used from the top edge. |
| R9-10-2 | OVER_8.8_t_GVM_WHITE_LONG | spec | tonnes vary. |
| R9-11-1 | VEHICLES_OVER_5.1_m_LONG_WHITE_LONG | spec | metres vary; same 510 vertical inconsistency. |
| R9-11-2 | OVER_5.1_m_LONG_WHITE_LONG | spec | |
| R9-12-1 | VEHICLES_OVER_4.2_m_HIGH_WHITE_LONG | spec | metres vary; same 510 vertical inconsistency. |
| R9-12-2 | OVER_4.2_m_HIGH_WHITE_LONG | spec | |
| R9-13-1 | VEHICLES_OVER_2.5_m_WIDE_WHITE_LONG | spec | metres vary; same 510 vertical inconsistency. |
| R9-13-2 | OVER_2.5_m_WIDE_WHITE_LONG | spec | |
| R9-15 | ON_BRIDGE_WHITE_LONG | spec | |
| R9-16 | SERVICE_ROAD_WHITE_LONG | spec | |
| R9-17 | ON_RAMP_WHITE_LONG | spec | |
| R9-18 | TO_TRAFFIC_FROM_LEFT_WHITE_LONG | spec | |
| R9-19 | GIVE_WAY_IF_GOING_STRAIGHT_AHEAD_WHITE_LONG | spec | Red-bordered GIVE WAY sub-panel as two `panel` elements (red R24 + white R6). Text-block top: left chain 310 vs right chain 312 — 310 used. Broken arrow as polygon + two rects; dashes end at 678 vs dimensioned 680; R9 tip not applied. |
| RM2-14A(L) | LEFT_TURN_ONLY_WHITE_SQUARE | needs-symbol rm2-14a_curve_arrow_left | Vertical string 75/309/60/90/75 sums to 609 on a 600 sign — placed from the top. Square corners, 25 border, no edge. |
| RM2-14A(R) | RIGHT_TURN_ONLY_WHITE_SQUARE | needs-symbol rm2-14a_curve_arrow_left (flip h) | Its grid inset shows the same left-turn arrow. |
| RM2-4A | NO_ENTRY_WHITE_SQUARE | spec | Circle 539 dia / bar 458×91 drawn. ENTRY dimensioned 120\|368\|112 (centre 304) — followed. NO drawn 141 vs font 148 (5 %, as on R2-4). |
| RM2-6A(L) | NO_LEFT_TURN_WHITE_SQUARE | needs-symbol rm2-6a_no_left_turn (multi-colour) | Only the 539 outer diameter is dimensioned; annulus/bar widths and the arrow are grid-only, so the whole device is one symbol. |
| RM2-6A(R) | NO_RIGHT_TURN_WHITE_SQUARE | needs-symbol rm2-6a_no_left_turn (flip h) | |
| RM4-12D | END_{speed}_SPEED_WHITE_TALL | spec | speed varies (60 shown; 10–110). Black annulus R265/R215 at (300,575). Drawing states 220 D for the numerals (not the R4-1 speed rule). Folder Speed Signs/End. |
| RM4-1A | {speed}_SPEED_WHITE_SQUARE | spec | speed varies (60 shown; 10–110). Red annulus R265/R215. Series D as stated. Folder Speed Signs/Normal Speed Signs. |
| RM6-1C | NO_OVERTAKING_OR_PASSING_WHITE_LONG | spec | |
| RM6-6C | STOP_HERE_ON_RED_SIGNAL_RED_LETTERS_WHITE_LONG | spec | |

## Remaining generator width mismatches (all explained above and in `notes`)
R6-3 t (44 vs 52), R6-23 & (115 vs 100), R7-12 m (55 vs 73), R7-2 AHEAD (430 vs 410, series D chosen over the drawing's E), R9-1-1 AM (80 vs 75), R9-8 AT (153 vs 148), RM2-4A NO (148 vs 141). R2-4 NO is a pre-existing spec, not part of this batch.

## Generator features needed but missing
* **Rotated text** (R6-25, R6-26): letters set along the crossbuck arms. Only workaround was to make the whole crossbuck a symbol.
* **Per-hand name substitution** (R7-3): one spec with hands L/R whose legend differs (LEFT/RIGHT) cannot give the two outputs different names.
* **Partial polygon rounding** (R7-5 R10, R7-11-x R5, R9-19 R9): drawings round only the barb corners/tip; `radius` rounds every vertex, so 0 was used.
* Symbol bbox needs the drawing to dimension both axes: R6-30 (arrow widths/x) and R6-31 (everything, incl. the text centre) fall back to reading the grid inset.

## Drawing inconsistencies found
R6-15 size-table label "R6-14B"; R6-15 bar "29"; R7-8/R7-10 panel 50|515|50 on a 600 sign; R9-1-2 strings 447/445; R9-10-1, R9-11-1, R9-12-1, R9-13-1 vertical strings 510 on 500; RM2-14A vertical 609 on 600; R9-19 310 vs 312 and 678 vs 680; R7-2 series label; R7-12 m width; R6-3 t width; R9-1-1 AM width; R9-7-1 empty numeral box; R6-17 TRI-AXLE 435 and undimensioned numeral-to-t gap; R6-6/R6-14/R6-33 dimension-line order (resolved nearest-first).
