# G9 / G10 / G11 drawings - transcription report

Generator run: `tools/signgen.py tools/specs/G/*.json` (106 files written across the G folder; every width mismatch below is explained in the spec notes).

| code | name | status | flags |
|---|---|---|---|
| G9-3(L) | LOW_BRIDGE_AHEAD_DETOUR_WHITE_LONG | needs-symbol g9-3_arrow_left | DETOUR labelled 120 D but stated width 686 = 120 E (E used, as G9-4); left stack 215 inconsistent (sum 907), arrow placed from the 67 bottom dim; 2.2 m line centred using font widths (63 dim unassigned). FEATURE: mixed-series words on one centred line (numeral + Emod unit) not supported - positions precomputed from font widths. |
| G9-3(R) | LOW_BRIDGE_AHEAD_DETOUR_WHITE_LONG | needs-symbol g9-3_arrow_left | as G9-3(L) |
| G9-4(L) | LOAD_LIMIT_ON_BRIDGE_DETOUR_WHITE_LONG | needs-symbol g9-3_arrow_left | 22 t centred above GROSS using font widths (FEATURE: mixed-series centred group). |
| G9-4(R) | LOAD_LIMIT_ON_BRIDGE_DETOUR_WHITE_LONG | needs-symbol g9-3_arrow_left | as G9-4(L) |
| G9-5-1(L) | DETOUR_FOR_HIGH_VEHICLES_WHITE_POINTED | spec | pointed outline drawn as polygons (FEATURE: no pointed-rectangle shape); chevron x taken from the 325 dim (tip to chevron right edge); bottom chain sums to 1302. |
| G9-5-1(R) | DETOUR_FOR_HIGH_VEHICLES_WHITE_POINTED | spec | as G9-5-1(L) |
| G9-5-2(L) | DETOUR_FOR_HEAVY_VEHICLES_WHITE_POINTED | spec | pointed polygons; chevron placement as G9-5-1 |
| G9-5-2(R) | DETOUR_FOR_HEAVY_VEHICLES_WHITE_POINTED | spec | as G9-5-2(L) |
| G9-5-3(L) | DETOUR_FOR_LONG_VEHICLES_WHITE_POINTED | spec | as G9-5-2(L) |
| G9-5-3(R) | DETOUR_FOR_LONG_VEHICLES_WHITE_POINTED | spec | as G9-5-2(L) |
| G9-5-4(L) | DETOUR_FOR_WIDE_VEHICLES_WHITE_POINTED | spec | as G9-5-2(L) |
| G9-5-4(R) | DETOUR_FOR_WIDE_VEHICLES_WHITE_POINTED | spec | as G9-5-2(L) |
| G9-7 | LIVERPOOL_A30_TURN_LEFT_GREEN_SQUARE | needs-symbol g9-7_arrow_turn_left |  |
| G9-8 | LIVERPOOL_A30_LEFT_LANE_GREEN_SQUARE | spec | LEFT LANE 1429 total: split as 621 + 117 gap + 691 (font word space would give 1523). |
| G9-9 | REDUCE_SPEED_RED_LONG | spec |  |
| G9-10 | SLOW_VEHICLE_LANE_AHEAD_WHITE_SQUARE | spec |  |
| G9-11 | SLOW_VEHICLE_LANE_2_km_AHEAD_WHITE_TALL | spec | 2 km group centred using font widths (FEATURE: mixed-series group). |
| G9-12 | SLOW_VEHICLES_USE_LEFT_LANE_WHITE_TALL | spec |  |
| G9-15 | FORM_1_LANE_WHITE_TALL | spec |  |
| G9-16 | FORM_2_LANES_WHITE_TALL | spec |  |
| G9-17 | WINDING_ROAD_ENDS_3_km_WHITE_WIDE | spec | ENDS 3 km group centred using font widths; numeral series not labelled (E assumed from ENDS). |
| G9-18 | NO_THROUGH_ROAD_WHITE_LONG | spec |  |
| G9-20 | ROAD_CLOSED_WHITE_LONG | spec |  |
| G9-21-1 | ROAD_SUBJECT_TO_FLOODING_INDICATORS_WHITE_WIDE | spec |  |
| G9-21-2 | ROAD_SUBJECT_TO_FLOODING_INDICATORS_WHITE_SQUARE | spec |  |
| G9-21-3 | ROAD_SUBJECT_TO_FLOODING_DO_NOT_ENTER_WHITE_RED_LONG | spec | lower stack sums to 1075 not 1100 (DO NOT ENTER placed by the top-down chain, pixel position about 585); DO NOT ENTER stated widths 8.5 percent wider than D 180 (width mismatch left, noted). Red lower panel drawn as a path. |
| G9-22-1 | FLOOD_DEPTH_GAUGE_2m_WHITE_TALL | spec | depth gauge: 125 Emod bracket drawn from the top edge but the chain puts the m cap top at 15; tick/baseline relation and the 25|140 callout ambiguous; 0.2-step labels at construction line x 37. Also carries G9-22-2 and G9-22-3 (same PNG) - specs written for those two codes as well. |
| G9-22-2 | FLOOD_DEPTH_GAUGE_4m_WHITE_TALL | spec | from G9-22-1.png (no own PNG) |
| G9-22-3 | FLOOD_DEPTH_GAUGE_6m_WHITE_TALL | spec | from G9-22-1.png (no own PNG) |
| G9-24-1 | SAFETY_RAMP_8.8_km_WHITE_WIDE | spec | 8.8 km group centred using font widths; decimal pitch stated 88 (font 80). |
| G9-24-2 | SAFETY_RAMP_8.8_km_WHITE_TALL | spec | width rows 690/950 swapped between SAFETY and RAMP on the drawing; decimal pitch stated 100 (font 80). |
| G9-25-1 | SAFETY_RAMP_80_m_WHITE_WIDE | spec | 80 m group centred using font widths. |
| G9-25-2 | SAFETY_RAMP_60_m_WHITE_TALL | spec | width rows swapped as G9-24-2. |
| G9-32 | RAILWAY_WHITE_WIDE_SKINNY | spec |  |
| G9-33 | CROSSING_WHITE_WIDE_SKINNY | spec |  |
| G9-36-1(L) | SAFETY_RAMP_ARROW_LEFT_WHITE_WIDE_SKINNY | needs-symbol g9-36_arrow_diag_up_left |  |
| G9-36-1(R) | SAFETY_RAMP_ARROW_RIGHT_WHITE_WIDE_SKINNY | needs-symbol g9-36_arrow_diag_up_left |  |
| G9-36-2 | SAFETY_RAMP_ARROW_WHITE_SQUARE | needs-symbol g9-36_arrow_diag_up_left | width rows 1106/1524 swapped between SAFETY and RAMP on the drawing. |
| G9-37 | OVERTAKING_LANE_300_m_AHEAD_WHITE_LONG | spec | 300 m AHEAD group centred using font widths. |
| G9-38 | OVERTAKING_LANE_6_km_AHEAD_WHITE_LONG | spec | 6 km AHEAD group centred using font widths. |
| G9-40-1 | LOCAL_TRAFFIC_ONLY_WHITE_LONG | spec |  |
| G9-40-2 | LOCAL_TRAFFIC_ONLY_ROADWORKS_WHITE_LONG | spec |  |
| G9-41 | UNSUITABLE_FOR_LARGE_VEHICLES_WHITE_LONG | spec |  |
| G9-42 | SUNNYSIDE_MARTINS_CREEK_GRANGE_HAWKER_GREEN_TALL | skipped: needs generator feature: rotated text - every legend line (Sunnyside, Martins Creek, A13, ... | FEATURE: rotated text (all lines 90 deg CCW) not supported; top x-chain sums to 4270 vs 3400. Dimensions transcribed in the spec. |
| G9-43-1 | LANE_ARROWS_STRAIGHT_STRAIGHT_RIGHT_RIGHT_GREEN_LONG | needs-symbol g9-43_arrow_right_turn g9-43_arrow_straight g9-43_arrow_straight_and_right | lane arrows as symbols (all dims in symbols desc). |
| G9-43-2 | LANE_ARROWS_LEFT_LEFT_RIGHT_RIGHT_GREEN_LONG | needs-symbol g9-43_arrow_left_and_right g9-43_arrow_left_turn g9-43_arrow_right_turn | lane arrows as symbols; 61 gap between lane line and centre arrow. |
| G9-43-3 | CITY_MT_GRAVATT_LANE_ARROWS_GREEN_LONG | needs-symbol g9-43_arrow_right_turn g9-43_arrow_straight g9-43_arrow_straight_and_right | City / Mt Gravatt centred as a group using font widths (=|Varies|180|Varies|=); right-turn arrow 565 tall taken bottom-aligned; dashed-line chain 5 short. |
| G9-43-4 | HIGH_ST_WSONS_RD_DCASTER_RD_AT_SIGNALS_GREEN_LONG | needs-symbol g9-43_arrow_left_turn g9-43_arrow_right_turn g9-43_arrow_straight_offset | left-turn arrow (550) vertical position not stated (top-aligned); W'SONS / D'CASTER stated widths 2.2-2.5 percent above C 100 (apostrophe spacing); separator + R40 drawn as two green sub-panels. |
| G9-46 | VERY_STEEP_CLIMB_8_km_AHEAD_NOT_SUITABLE_WHITE_LONG | spec | 8 km AHEAD group centred using font widths; two-panel sign drawn as black ground + two white R50 panels. |
| G9-47 | VERY_STEEP_CLIMB_NEXT_3_km_W5-13B_WHITE_LONG | needs-symbol w5-13b_steep_climb | black border width NOT stated (40 used from the pixel image / G9-46); NEXT stated 708 vs E 180 = 664 (mismatch left); W5-13B bounding box derived from the 750 side. |
| G9-48 | LOOK_FOR_TRAINS_WHITE_SQUARE | spec |  |
| G9-50 | SLOW_VEHICLE_TURNOUT_300_m_WHITE_SQUARE | spec | 300 m group centred using font widths; numeral series not labelled (D). |
| G9-51 | SLOW_VEHICLE_TURNOUT_ARROW_WHITE_TALL | needs-symbol g9-51_arrow_diag_up_left |  |
| G9-52(L) | ALTERNATIVE_ROUTE_FOR_TRUCKS_AND_BUSES_WHITE_POINTED | spec | tip inset and tip radius NOT dimensioned (138 / R50 as G9-5, pixel check 139); chevron arm thickness 84 is perpendicular -> horizontal offset 107, overall 210. |
| G9-52(R) | ALTERNATIVE_ROUTE_FOR_TRUCKS_AND_BUSES_WHITE_POINTED | spec | as G9-52(L) |
| G9-53 | VERY_STEEP_DESCENT_8_km_AHEAD_NOT_SUITABLE_WHITE_LONG | spec | as G9-46 |
| G9-54 | TAKE_TICKET_WHITE_LONG | spec |  |
| G9-55(L) | WAY_OUT_ARROW_LEFT_GREEN_WIDE_SKINNY | needs-symbol g9-55_arrow_left |  |
| G9-55(R) | WAY_OUT_ARROW_RIGHT_GREEN_WIDE_SKINNY | needs-symbol g9-55_arrow_left |  |
| G9-56 | WAY_OUT_TO_GEORGE_ST_ARROW_RIGHT_GREEN_LONG | needs-symbol g9-56_arrow_right | file G9-56.png is titled G9-56(R); 10|20 read as edge|border; GEORGE ST word space from the font. |
| G9-57 | WATCH_FOR_BICYCLES_WHITE_LONG | needs-symbol bicycle |  |
| G9-58 | BICYCLE_DISMOUNT_WHITE_SQUARE | needs-symbol bicycle |  |
| G9-60 | BICYCLE_ARROW_UP_LEFT_WHITE_TALL | needs-symbol bicycle g9-60_arrow_diag_up_left |  |
| G9-62 | BICYCLES_USE_RAMP_ARROW_WHITE_TALL | needs-symbol bicycle g9-62_arrow_diag_up_left | RAMP not centred (62|484|54) as drawn. |
| G9-63 | BICYCLES_CROSS_HERE_WITH_CARE_WHITE_SQUARE | needs-symbol bicycle g9-63_arrow_right | hands L/R from the note "Arrow may be left or right" (drawn R). |
| G9-64 | BICYCLES_USE_LEFT_SHOULDER_WHITE_LONG | needs-symbol bicycle |  |
| G9-65 | BICYCLES_MUST_EXIT_ARROW_WHITE_TALL | needs-symbol bicycle g9-62_arrow_diag_up_left |  |
| G9-66 | DISTANCE_PLATE_300_m_GREEN | skipped: no fixed dimensions: size, radius, numeral size and all widths are marked Varies (only 85 ... | all dimensions Varies - skipped. |
| G9-67-1 | KEEP_TRACKS_CLEAR_WHITE_SQUARE | spec |  |
| G9-67-2 | KEEP_TRACKS_CLEAR_GRID_WHITE_TALL | needs-symbol g9-67-2_yellow_grid_patch | two-colour symbol (black square + yellow lines) - symbol file must carry its own fills. |
| G9-68 | EMERGENCY_EXIT_PUSH_GATE_WHITE_LONG | spec |  |
| G9-69 | WRONG_WAY_GO_BACK_RED_LONG | spec | width rows 782/1228 swapped between WRONG and WAY on the drawing; white line as rect. |
| G9-70 | NO_STOPPING_ON_FREEWAY_WHITE_SQUARE | spec |  |
| G9-71 | SERVICE_ROAD_ENTRY_ARROW_WHITE_TALL | needs-symbol g9-71_arrow_diag_up_left | arrow x NOT dimensioned (centred; pixel check agrees). |
| G9-72 | LEFT_TURN_FROM_SERVICE_ROAD_ONLY_WHITE_LONG | spec |  |
| G9-73 | MERGE_RIGHT_ARROW_WHITE_SQUARE | needs-symbol g9-73_arrow_right | file G9-73.png is G9-73(R); width rows 629/738 swapped between MERGE and RIGHT; arrow x NOT dimensioned (centred, pixel check). |
| G9-73AA | MERGE_LEFT_ARROW_WHITE_SQUARE | needs-symbol g9-73aa_arrow_left | file is G9-73AA(L); arrow tip/barb radii not stated. |
| G9-74 | RAILWAY_CROSSING_NOT_IN_USE_WHITE_LONG | spec | width rows 497/444 swapped between RAILWAY and CROSSING. |
| G9-75 | LENGTH_LIMIT_AHEAD_80_m_OVERALL_DETOUR_WHITE_LONG | needs-symbol g9-3_arrow_left | one PNG shows (L) and (R): hands L/R with DETOUR mirror:true; 80 m OVERALL group centred using font widths. |
| G9-76 | NARROW_BRIDGE_AHEAD_3.6_m_DETOUR_WHITE_LONG | needs-symbol g9-3_arrow_left | as G9-75; decimal pitch stated 65 (font 55). |
| G9-77 | SLOWER_VEHICLES_USE_TURNOUTS_NEXT_60_km_WHITE_LONG | spec | NEXT 60 km group centred using font widths. |
| G9-78 | 300_m_WHITE_WIDE_SKINNY | spec | 300 m group centred using font widths. |
| G9-79 | {speed}_AHEAD_WHITE_TALL | spec | speed-rule numerals with vary; left chain 80|170|240 puts the numerals 5 above the annulus centre. |
| G9-80-1 | ON_RIGHT_WHITE_LONG_SKINNY | spec |  |
| G9-80-2 | ON_RIGHT_WHITE_LONG | spec |  |
| G9-82 | STEEP_DESCENT_W5-12B_RED_LONG | needs-symbol w5-12b_steep_descent | W5-12B vertical position NOT dimensioned (centred). |
| G9-83 | LONG_STEEP_DESCENT_NEXT_3.8_km_W5-12B_RED_LONG | needs-symbol w5-12b_steep_descent | W5-12B size NOT dimensioned (1010 as G9-82) and vertical position NOT dimensioned (centred); NEXT line centred in the 1874 area using font widths. |
| G9-84 | AFTER_SIGNALS_WHITE_LONG | spec |  |
| G9-85 | AFTER_ROUNDABOUT_WHITE_LONG | spec |  |
| G9-87-1 | NO_BUSES_WHITE_SQUARE | needs-symbol g9-87-1_bus | bus symbol height from the detail (125); annulus/bar as annulus + polygon. |
| G9-87-2 | NO_TRUCKS_WHITE_SQUARE | needs-symbol g9-87-2_truck | truck symbol bbox from the 108/90 dims. |
| G9-88 | PACIFIC_MWY_M1_KEMPSEY_PORT_MACQUARIE_WAUCHOPE_GREEN_TALL | skipped: needs generator feature: rotated text - every legend line and both PACIFIC MWY road-name p... | FEATURE: rotated text not supported; edge/border/radius not dimensioned. |
| G9-89 | NO_LINES_DO_NOT_OVERTAKE_WHITE_LONG | spec | all stated widths 2-3 percent below E 160 (mismatch left, noted). |
| G9-90-1 | EMERGENCY_STOPPING_BAY_500_m_AHEAD_WHITE_LONG | spec | 500 m group centred using font widths. |
| G9-90-2 | EMERGENCY_STOPPING_BAY_3_km_AHEAD_WHITE_LONG | spec | 3 km group centred using font widths. |
| G10-3 | W_4_ROUTE_MARKER_GREEN_SHIELD | spec | six variants on one drawing (W/4 written); shield drawn as inset polygons (FEATURE: no trapezoid shield shape / polygon offset). |
| G10-4 | NATIONAL_ROUTE_PLATE_GREEN_LONG_SKINNY | spec |  |
| G10-5 | W_4_NATIONAL_ROUTE_MARKER_GREEN_SHIELD | spec | six variants (W/4 written); 12|18 read as gap + white separator band; NATIONAL panel sides = shield border. |
| G11-1 | CAMERA_300_m_ON_LEFT_BROWN_TALL | needs-symbol camera | 300 m group centred using font widths; 20|40 read as edge|total. |
| G11-2 | MUSEUM_300_m_ON_RIGHT_BROWN_LONG | spec | 300 m group centred using font widths. |
| G11-3(L) | HISTORICAL_MARKER_ARROW_LEFT_BROWN_WIDE_SKINNY | needs-symbol g9-51_arrow_diag_up_left |  |
| G11-3(R) | HISTORICAL_MARKER_ARROW_RIGHT_BROWN_WIDE_SKINNY | needs-symbol g9-51_arrow_diag_up_left |  |
| G11-4(L) | SILVERBAND_FALLS_2_CHEVRON_BROWN_POINTED | spec | pointed polygons; chevron horizontal arm extent (about 102) derived from 271 overall and 151 perpendicular thickness. |
| G11-4(R) | SILVERBAND_FALLS_2_CHEVRON_BROWN_POINTED | spec | as G11-4(L) |
| G11-5 | SILVERBAND_FALLS_2_CHEVRON_BROWN_POINTED_NO_BORDER | spec | chevron INCONSISTENT: sign chain 302 wide vs detail 188|160 (348) with 126 thickness - 302 used with h 188; no corner radius stated; SILVERBAND right-aligned / FALLS centred under it. |
| G11-7 | HISTORICAL_MARKER_BURKES_TREE_TURN_LEFT_300_m_BROWN_LONG | spec | 90 gap above the numeral line not labelled (required by the total); 300 m group centred using font widths. |
| G11-8 | SUNRISE_TURN_RIGHT_300_m_GRAPES_BROWN_LONG | needs-symbol grapes | symbol box 30 from the top edge as dimensioned (overlaps the border band); 300 m group centred using font widths. |
| G11-9 | WHITSUNDAY_SERVICES_BROWN_BLUE_TALL | needs-symbol boat_ramp camping_tent_caravan fuel_pump | no horizontal text dimensions at all (all centred); mixed lines use the font word space; brown/blue edge split drawn with paths. |
| G11-10 | CAMERA_ARROW_LEFT_BROWN_TALL | needs-symbol camera g11-10_arrow_left | file G11-10.png titled G11-10(L); corner radius NOT stated. |
| G11-11 | WINERIES_OAKVALE_CHALMERS_SUNRISE_GRAPES_BROWN_LONG | needs-symbol grapes | destination / numeral widths vary (left- and right-aligned as dimensioned). |

Counts: spec 66, needs-symbol 41, skipped 3 (total 110; 108 PNGs + G9-22-2 and G9-22-3 which share G9-22-1.png).

## Generator features needed but missing
* Rotated (vertical) text: G9-42 and G9-88 skipped.
* Mixed-series words on one centred line (numeral + Emod unit, e.g. "2.2 m", "8 km AHEAD", "City ... Mt Gravatt"): positions precomputed from the FHWA font ink widths and written as left-aligned x; noted in every affected spec.
* Pointed (arrow-shaped) panels and the G10 trapezoid shield: drawn as inset polygons on a white ground (G9-5-x, G9-52, G11-4, G11-5, G10-3, G10-5).
* Sub-panel with square top corners and rounded bottom corners (G9-21-3 red panel) and the split brown/blue edge (G11-9): drawn with raw paths.
* Two-colour symbol (G9-67-2 black/yellow patch): symbol file must carry fills.

## Drawing inconsistencies
* Width rows swapped between the two lines: G9-24-2, G9-25-2, G9-36-2, G9-69, G9-73, G9-74.
* Series/width conflicts: G9-3 DETOUR (D labelled, E width), G9-21-3 DO NOT ENTER (+8.5 percent), G9-47 NEXT (+6.6 percent), G9-89 (all -2.4 percent), G9-43-4 apostrophe words (+2.2-2.5 percent).
* Chains that do not add up: G9-3 left stack (907), G9-5-1 bottom (1302), G9-21-3 lower stack (1075), G9-22 top 15, G9-43-3 dashed lines (5), G9-42 top chain (4270), G11-5 chevron (302 vs 348), G9-79 numeral top (5).
* Undimensioned positions/sizes (placed with the reasoning stated in notes): G9-5-x chevron x, G9-52 tip inset/radius, G9-47 border width, G9-71 / G9-73 arrow x, G9-82 / G9-83 W5-12B position (and size on G9-83), G9-43-4 left-turn arrow y, G11-10 radius, G11-9 all text x.
