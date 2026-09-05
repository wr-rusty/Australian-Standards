# GE / GM / D4 / TRA transcription report

69 drawings (PNG files starting GE, GM, D4-, TRA) -> 70 spec files in tools/specs/GE (TRA.png gives TRA and TRB).
Counts by drawing: **38 spec**, **26 needs-symbol**, **5 skipped**.
Generator run: `tools/signgen.py tools/specs/GE/*.json` -> 65 files written; 2 width mismatches remain, both explained in the spec notes
(GE1-5-Example-B dashed numeral, GM9-89C LINES 2.1 %). Blocked (needs-symbol) specs do not get their text widths checked by the
generator (it stops at the first missing symbol), so every `expect` in the folder was also checked independently with the same font
code; the only remaining differences are the two above plus GE1-14 Sunhill (drawn 2394, 400 Emod gives 2281) and GM9-58A DISMOUNT
(drawn 483, 85 C gives 463), both flagged in notes.

Conventions found in the GE drawings and used throughout: green (or blue/red/brown) edge 70 outside a 70 white border (labelled 70/140;
50/100, 40/80, 30/60, 10/20 on the smaller signs); vertical chains on GE1-11/12/13/6, GE2-1-x, GE2-2, GE4-1, GE1-8-x are dimensioned to
**baselines** (cap top = baseline - height); mixed lines ("2 km", "1 km") are a 350/400 E numeral with a 300/320/340 Emod "km" on the
same baseline.

| Code | Name | Status | Flags |
|---|---|---|---|
| D4-1-1 | CHEVRONS_LEFT_WHITE_ON_BLACK_LONG_SKINNY | spec | 214 + 7x198 puts the first white tip at x=14 (picture shows it at the edge); last stripe reaches the right-hand corners so it is a path with the R25 corner arcs - generator has no clipping to the panel outline |
| D4-1-2 | CHEVRON_LEFT_WHITE_ON_BLACK_SQUARE | spec | |
| D4-2-2 | CHEVRONS_UP_WHITE_ON_BLACK_TALL | spec | first apex at the top edge (200/200), 113 perpendicular = 160 vertical |
| D4-2-3 | CHEVRONS_BOTH_WAYS_WHITE_ON_BLACK_LONG_SKINNY | spec | |
| D4-3(L,R) | DIAGONAL_STRIPES_BLACK_ON_WHITE_TALL | spec | chain 64|64|71 anchored at the top-right corner; drawing labels the second white 64 but 4x71 + 3x64 = 476 = the 477 diagonal and matches the picture, so 71 used for all whites (see notes) |
| D4-5-1 | STRIPES_BLACK_ON_WHITE_WIDE | spec | 1800x400 (4.5:1) |
| D4-5-2 | STRIPES_RED_ON_WHITE_WIDE | spec | |
| D4-6 | CHEVRON_LEFT_BLACK_ON_YELLOW_TALL | spec | arms are 270 across x 345 down, not 45 degrees |
| D4-7(L,R) | CHEVRON_{speed}_KMH_BLACK_ON_YELLOW_LONG | spec | numerals 'Varies': right-aligned 35 from the far edge (L) / left 35 (R) using text mirror; '65' in 400 E is 716, wider than the 673 dashed box; speed values 15..95 assumed (advisory speeds) |
| GE1-11 | MONASH_HAWKER_A25_M10_2KM_GREEN_LONG | needs-symbol arrow_up_exit_diag_left_1870x2050 | |
| GE1-12 | COCKFOSTERS_M10_MONASH_HAWKER_A25_1KM_GREEN_TALL | needs-symbol arrow_up_exit_diag_left_1870x4300 | '1 km' chain sums 4449 |
| GE1-13 | B205_HOLLEY_STREET_LEFT_LANE_GREEN_LONG | spec | vertical chain 840|300|800|650|460 sums 3050 for a 2950 sign - bottom margin comes out 360; HOLLEY STREET word gap derived (309) from the 4806 total |
| GE1-14 | A81_SUNHILL_M8_HAWKER_PLUMPTON_4_ARROWS_GREEN_WIDE_SKINNY | needs-symbol arrow_straight_up_1000x528 arrow_up_and_curve_left_1300x1000 arrow_curve_up_left_800 | drawn rotated 90 deg, transcribed in the sign frame (15250x3100); length chain sums 15226; Sunhill 2394 vs 2281; sub-panels with R100 corners done as green polygons on white; 1025|525|340 chain and 300 E/350 E labels have no drawn legend (caption mentions an ONLY panel) |
| GE1-15 | A1_MURRAY_CURVED_EXIT_GREEN_LONG | needs-symbol arrow_curve_left_flyover_4805x3245 | 'Murray' is 320 Emod rotated 90 deg inside a boxed label within the diagram - **rotated text not supported**, left inside the symbol; 2192/2653 split not tied to a feature |
| GE1-16 | M3_CITY_2_ARROWS_GREEN_LONG | needs-symbol arrow_straight_up_1000x528 | rotated drawing; only the upper sign is fully dimensioned (4420x3155); M3-City gap not dimensioned - 400 used (the gap GE1-19 gives for the same legend); lower sign ('Varies') not transcribed |
| GE1-17 | A77_AIRPORT_DR_LANCEFIELD_GREEN_SQUARE | needs-symbol arrow_curve_up_left_800 | road-name panel width not stated (150 + ink + 150) |
| GE1-18 | EXIT_1_KM_GREEN_WIDE | spec | width 'Varies' with the numeral - **generator cannot vary the panel size with the legend**, written for '1' (3258 wide); 360|400|360 sums 1120 for the 1150 height; border widths not dimensioned (70/70 assumed as the series) |
| GE1-19 | M80_RING_ROAD_M3_CITY_SEYMOUR_GEELONG_4_ARROWS_GREEN_WIDE | needs-symbol arrow_straight_up_2500x530 arrow_up_and_curve_left_2500x1309 arrow_double_curve_up_left_1155 arrow_curve_up_left_1004x803 | rotated drawing; width 12720 (text chains) vs 13002 (arrow chain); arrow-row chain 430|300|700|1215|515 does not close; curved arrows' vertical positions and Seymour/Geelong x positions not dimensioned (taken from the picture, see notes) |
| GE1-5-Example-A | - | skipped: image resolution too low (189x214 px) to read the dimensions | it is a fully dimensioned GE1-5 (A25 / HAWKER STREET / Plumpton / EXIT 1 km, 4500 wide) - needs a better scan |
| GE1-5-Example-B | A53_MIDLANDS_HWY_SWAN_CK_MANSFIELD_EXIT_2KM_GREEN | spec | drawing is titled GE1-5 and fully dimensioned; dashed numeral 2 drawn 171 but 180 E gives 146; MIDLANDS HWY / Swan Ck word gaps derived from the stated totals |
| GE1-6 | A36_QUEENSTOWN_ROAD_HEATHMONT_EXIT_1KM_2_LEFT_LANES_GREEN | spec | |
| GE1-8-1 | BENDIGO_THIS_EXIT_GREEN_LONG | spec | |
| GE1-8-2 | BENDIGO_NEXT_EXIT_GREEN_LONG | spec | |
| GE1-8-3 | GOSFORD_NEXT_2_EXITS_GREEN_LONG | spec | |
| GE1-8-4-Example-A | - | skipped: example assembly, not fully dimensioned (width Varies) | exit-panel detail 600x600 R80 is dimensioned |
| GE1-8-4-Example-B | - | skipped: example assembly, not fully dimensioned (width Varies) | |
| GE1-8-4-Example-C | - | skipped: example assembly, not fully dimensioned (width Varies) | |
| GE1-9 | CITY_EXITS_A1_MONASH_DR_B15_FREEMAN_WAY_GREEN_LONG | spec | header/body sub-panels R60 as green polygons on white; row 3 chain (200|550|200|2034|172|519|200) sums 3875 for a 3750 sign - the 172 gap is not honoured; middle row position inferred from the 420 chain point |
| GE11-1 | LIZARD_FARM_THIS_EXIT_BROWN_WIDE | spec | |
| GE11-2 | LIZARD_FARM_USE_HOLLEY_EXIT_BROWN_LONG | spec | |
| GE2-1-1 | GREENS_ROAD_A69_MONASH_HAWKER_EXIT_GREEN_LONG | needs-symbol arrow_diag_up_left_660 | GREENS ROAD word gap derived from the 3185 total |
| GE2-1-2 | A69_MONASH_HAWKER_EXIT_GREEN_LONG | needs-symbol arrow_diag_up_left_505 | arrow detail quotes a 550 head in a 505 box |
| GE2-1-3 | A93_TAMBALANGA_HONEYFORD_EXIT_GREEN_LONG | needs-symbol arrow_diag_up_left_505 | |
| GE2-1-4 | MILLERS_RD_EXIT_A14_ARROW_GREEN_TALL | needs-symbol arrow_diag_up_left_660 | **rotated text not supported**: MILLERS RD (in panel), EXIT and A14 all read upward and are not placed (positions in notes); 4529 not tied to a feature |
| GE2-2 | M1_LAMBERTON_UP_ARROW_GREEN_WIDE | needs-symbol arrow_straight_up_835x547 | 4340 read as the arrow centreline |
| GE2-3 | EXIT_DIAG_ARROW_GREEN_SQUARE | needs-symbol arrow_diag_up_right_406 | |
| GE2-6-1 | EXIT_18_GREEN_ON_WHITE_SQUARE | spec | numerals vary (18 drawn) |
| GE2-6-2 | EXIT_47_GREEN_ON_WHITE_LONG | spec | numerals vary (47 drawn) |
| GE2-7 | EXIT_18_PANEL_DIAG_ARROW_GREEN_TALL | needs-symbol arrow_diag_up_left_406 | two-alphanumeric panel (1020) written; three-alphanumeric variant is 1340 wide |
| GE4-1 | M14_ROWE_FWY_MONASH_53_AUGUSTA_276_GREEN_LONG | spec | ROWE FWY word gap derived from the 1408 total |
| GE6-10 | END_FREEWAY_1_KM_GREEN_LONG | spec | |
| GE6-2 | PROHIBITED_ON_FREEWAY_LIST_WHITE_TALL | spec | height 'varies according to legend' (1300 drawn); width chains are stacked out of line order (856 = PROHIBITED, 700 = FREEWAY) |
| GE6-8 | NEXT_SERVICE_25_KM_BLUE_WIDE | spec | |
| GE6-9 | END_FREEWAY_2_KM_GREEN_LONG | spec | |
| GE7-1-3 | FUEL_FOOD_BED_THIS_EXIT_BLUE_LONG | needs-symbol service_fuel service_food service_accommodation | |
| GE7-10-3 | FUEL_FOOD_BED_BLUE_LONG | needs-symbol service_fuel service_food service_accommodation | |
| GE7-11-3 | FUEL_FOOD_BED_USE_HOLLEY_EXIT_BLUE_LONG | needs-symbol service_fuel service_food service_accommodation | HOLLEY EXIT 'Varies', word gap not stated |
| GE7-3-2 | PICNIC_TRUCK_PARKING_8_KM_BLUE_LONG | needs-symbol service_picnic_area service_truck_parking | |
| GE7-3-5 | INFO_BAY_2_KM_BLUE_SQUARE | needs-symbol service_info_bay | symbol width 'Varies' (height 1280 by subtraction) |
| GE7-4-1 | PICNIC_1_KM_LEFT_LANE_BLUE_LONG | needs-symbol service_picnic_area | numeral centred in its 389 dashed box |
| GE7-5-3 | FUEL_FOOD_TOILETS_DIAG_ARROW_BLUE_TALL | needs-symbol service_fuel service_food service_toilets arrow_diag_up_left_487 | |
| GE7-5-5 | - | skipped: size Varies (depends on the undimensioned i BAY symbol) | |
| GE7-8(L) | TELEPHONE_ARROW_LEFT_BLUE_TALL | needs-symbol service_telephone arrow_left_120x80 | border position ambiguous (5/15 vs 20|160|20); read as GE7-9 (white 5, inner edge at 15) |
| GE7-8(R) | TELEPHONE_ARROW_RIGHT_BLUE_TALL | needs-symbol service_telephone arrow_left_120x80 | mirror of (L) via flip |
| GE7-9 | 600_M_BLUE_LONG | spec | '20' under the 84/38 join read as the gap |
| GE9-15 | WRONG_WAY_RED_LONG | spec | |
| GE9-23-1 | WHITE_CROSS_GREEN_SQUARE | spec | bars run into the corners: corner vertices given the R50 panel radius |
| GE9-23-2 | WHITE_CROSS_300_M_GREEN_TALL | spec | bottom chain = | Varies | 40 | 400 | = : the 400 cannot be the width of 'm' (85 Emod) and is not used |
| GE9-24-1 | E_GREEN_SQUARE | spec | |
| GE9-24-2 | E_ARROW_GREEN_SQUARE | needs-symbol arrow_left_300x87 | one spec with hands L/R (one PNG) |
| GE9-3 | REDUCE_SPEED_NOW_RED_LONG | spec | |
| GM9-40-2A | LOCAL_TRAFFIC_ONLY_WHITE_SQUARE | spec | |
| GM9-58A | BICYCLE_DISMOUNT_WHITE_SQUARE | needs-symbol gm9-58a_bicycle | DISMOUNT drawn 483 but 85 C gives 463; 117|366|117 chain unexplained |
| GM9-79D | {speed}_AHEAD_WHITE_TALL | spec | 215/265 are the inner/outer radii of the annulus centred 330 from the top; speed values 20..110 |
| GM9-89C | NO_LINES_DO_NOT_OVERTAKE_WHITE_LONG | spec | the two upper width chains are drawn against the wrong lines (188/422 fits NO LINES, 184/277 fits DO NOT); NO LINES chain sums 1210; LINES 413 vs 422 |
| GM9-90B | DO_NOT_OVERTAKE_WHITE_LONG_SKINNY | spec | drawing gives different gaps (60, 52) between the three words - **per-word gaps not supported**, 60 used |
| GM9-91B | AT_INTERSECTION_WHITE_LONG_SKINNY | spec | |
| GM9-92B | AT_SIGNALS_WHITE_LONG_SKINNY | spec | |
| TRA (TRA.png) | TOURIST_DRIVE_ROUTE_MARKER_BROWN | needs-symbol tra_arrow_up | pentagon as polygons with per-vertex radii (R66 apex, R33 others), 8 white border (the '8' dim), brown inset computed; 24 gap above the arrow by subtraction; the generator draws a white 240 square behind the pentagon (no non-rectangular sheet outline) |
| TRB (TRA.png) | TOURIST_DRIVE_{n}_ROUTE_MARKER_BROWN | needs-symbol trb_arrow_up | numeral 67 E, n = 1..9 |

## Generator features needed (not worked around by guessing)
1. **Clipping of elements to the panel outline.** Stripes/bars that run into a rounded corner (D4-1-1 right end, GE9-23-x) have to be entered as a hand path with the corner arcs or given the panel radius on the corner vertices. A general `clip: panel` on polygons/paths would remove that.
2. **Rotated text** (90 deg, reading upward): GE1-15 'Murray', GE2-1-4 'MILLERS RD' / 'EXIT' / 'A14'. Those legends are described in notes but not drawn.
3. **Panel size that follows a `vary` value** (GE1-18 width = 3138 + numeral ink; GE2-6-2 / GE7-3-x / GE7-4-1 numerals also 'Varies' but at a fixed panel size).
4. **Per-word gaps** in a `words` line (GM9-90B 60/52; GE1-9 route number / name / distance columns solved with separate elements).
5. Text width checks are skipped for a spec once a symbol is missing (build raises before the checks); an independent check was run for this folder.
6. Running the generator on one folder rewrites `AS 1743-2023/Processed/MANIFEST.csv` with that folder's rows only.

## Symbols to trace (ids used, all with dimensions copied into the spec `symbols` desc)
arrow_up_exit_diag_left_1870x2050 (GE1-11), arrow_up_exit_diag_left_1870x4300 (GE1-12), arrow_straight_up_1000x528 (GE1-14/16),
arrow_up_and_curve_left_1300x1000 (GE1-14), arrow_curve_up_left_800 (GE1-14/17), arrow_curve_left_flyover_4805x3245 (GE1-15),
arrow_straight_up_2500x530 / arrow_up_and_curve_left_2500x1309 / arrow_double_curve_up_left_1155 / arrow_curve_up_left_1004x803 (GE1-19),
arrow_diag_up_left_660 (GE2-1-1/2-1-4), arrow_diag_up_left_505 (GE2-1-2/2-1-3), arrow_straight_up_835x547 (GE2-2), arrow_diag_up_right_406 (GE2-3),
arrow_diag_up_left_406 (GE2-7), arrow_diag_up_left_487 (GE7-5-3), arrow_left_120x80 (GE7-8), arrow_left_300x87 (GE9-24-2),
service_fuel / service_food / service_accommodation (GE7-1-3, 7-10-3, 7-11-3, 7-5-3), service_toilets (GE7-5-3), service_picnic_area (GE7-3-2, 7-4-1),
service_truck_parking (GE7-3-2), service_info_bay (GE7-3-5), service_telephone (GE7-8), gm9-58a_bicycle, tra_arrow_up (66x107), trb_arrow_up (50x74).
