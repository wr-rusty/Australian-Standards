# G1-G8 guide signs - transcription report

79 drawings, 81 spec files (G3-4 and G8-12-1 each carry two variants): 39 spec, 39 needs-symbol, 3 skipped.

Run: `signgen.py tools/specs/G/G[1-8]-*.json` -> 39 files written; every remaining width mismatch is explained in the spec's notes and listed below. BLOCKED lines are the missing symbol artwork. Note: the generator rewrites `AS 1743-2023/Processed/MANIFEST.csv` from the specs it is given, so after this run it lists only the G1-G8 rows.

| code | name | status | flags |
|---|---|---|---|
| G1-1 | A30_SYDNEY_A85_PLUMPTON_HAWKER_GREEN | needs-symbol g1-1_arrow_straight | drawing rotated 90 deg on the page (transcribed upright 2600x1510); right chain 1279 is a misprint for the 1239 road-name panel (chain sums to 2640); top chain 320+900+290 has a line at 1220 that matches no element; stacked panels need per-vertex radii (polygons on white ground). |
| G1-2 | HOLLEY_A15_SUNNYSIDE_MARTINS_CK_GREEN | needs-symbol g1-2_arrow_curved_right, g1-2_arrow_left | stacked panels built as polygons with per-vertex radii on a white ground; 'Martins Ck' word gap 123 derived from the 1351 total. |
| G1-3 | A30_SYDNEY_A85_HAWKER_PLUMPTON_DIAGRAM_GREEN | spec | rotated drawing; chain 158+1262+704+1262+163 = 3549 (1 mm short); intersection diagram drawn as a polygon with R30 at the concave corners only. |
| G1-4 | A40_MT_MARTIN_HWY_SUNNYSIDE_MARY_HILL_HAWKER_GREEN | needs-symbol g1-2_arrow_left | right chain 130+180+200+450+280+160 = 1400 for a 1460 sign - the 180 must be the 240 panel height; MT MARTIN HWY 120 D is 1335 by AS 1744 vs drawing 1260 (6%); 'Mary Hill' gap 112 derived. |
| G1-5 | A30_SYDNEY_A85_HAWKER_PLUMPTON_ROUNDABOUT_GREEN | needs-symbol g1-5_roundabout | rotated drawing; top chain gives the roundabout 1330 high but its detail gives 1270 (used); roundabout detail is dimensioned in the rotated orientation. |
| G1-6 | A32_MELBOURNE_BURKE_RD_MARTINS_CK_B97_HOLLEY_GREEN_TALL | needs-symbol g1-2_arrow_left, g1-6_arrow_left_334 | drawing's 1351/1289 rows are swapped relative to AS 1744 (Melbourne = 1289, Martins Ck = 1351); left arrow 335 on the sign vs 334 in the detail; 20 white rule drawn as a rect. |
| G1-7 | BIRDVILLE_A95_THOMAS_WAY_PLUMPTON_B269_DIAGRAM_GREEN | needs-symbol g1-7_diagram_through_left_exit | only Birdville right (160), Plumpton/B269 left (260) and the diagram's right/bottom margins are dimensioned: A95 x, road-name panel x, diagram size (750x1750 read off the 100 grid) are pixel estimates; no ink widths given. |
| G2-1 | SALTASH_HWY_A75_HAWKER_GREEN_FINGERBOARD | spec | 'Total width'/'Varies' - width built from AS 1744 widths (2485); chevron tip/top-left corner not dimensioned (405 confirmed only by measuring); the diagonal 236 dimension could not be tied to anything; pointed sign built as offset polygons. |
| G2-2(a) | DELORAINE_GREEN_WIDE_SKINNY | needs-symbol g1-1_arrow_straight | diagonal arrow boxed 203x203 in the drawing, inconsistent with the 250x220 arrow detail rotated 45 deg (~332); placed at detail size on the box centre. |
| G2-2(b) | SMITH_RD_GREEN_WIDE_SKINNY | needs-symbol g1-2_arrow_left | panel width given as 1200 / 1120 / 80/932/80 and 80/160/80 in a 240 panel; sign chain sums to 1810 not 1850; diagonal arrow box 207x207 vs 251x220 detail. |
| G2-4 | SALTASH_HIGHWAY_HAWKER_A79_PLUMPTON_GREEN_DOUBLE_FINGERBOARD | spec | rotated drawing; long chain sums to 4376 (1168 taken as 1192 for Plumpton, per AS 1744 and G1-3); double-pointed outline as offset polygons; chevrons as polygons from the detail (570/300/226/235). |
| G2-5 | GRANGE_ROAD_COCKFOSTERS_A17_GREEN | needs-symbol g1-6_arrow_left_334 | arrow 335 on the sign vs 334 detail. |
| G3-3 | 18_NARRABRI_A39_GREEN_FINGERBOARD | spec | '18' in 140 E computes 183.5 vs 189 (2.9%); chevron detail (94 run, 92 perpendicular) puts the chevron tip at 59, inside the 105 point run - consistent with the drawing; no top margin stated (text centred). |
| G3-4 | POLICE_ROAD_WHITE | spec | two variants in one drawing (NEWELL HIGHWAY one-line, POLICE ROAD two-line) -> two spec files with code G3-4; widths 'Varies' built from AS 1744; R40 only stated on the two-line variant. |
| G3-4 | NEWELL_HIGHWAY_WHITE | spec | two variants in one drawing (NEWELL HIGHWAY one-line, POLICE ROAD two-line) -> two spec files with code G3-4; widths 'Varies' built from AS 1744; R40 only stated on the two-line variant. |
| G3-5 | SUNNYSIDE_RD_WHITE_FINGERBOARD | spec | width 'Varies' (1566 built); chevron run 61/perp 60 gives 136.5 overall so its tip sits 57 short of the sign tip; GENERATOR GAP: white pointed sign on white ground has no outline (keyline only follows the rect shape). |
| G3-6 | C383_BORALMA_15_GREEN_FINGERBOARD | spec | width 'Varies' (1609 built); chevron V run not stated (61 taken from G3-5); caption mentions a border that is not drawn/dimensioned. |
| G3-7 | C383_GREEN_ROUTE_PLATE | spec | width 'Varies' (412 built). |
| G3-8-1 | SMITH_ST_LEFT_ARROW_WHITE | needs-symbol g3-8-1_arrow_left | width 'Varies' (1148 built); arrow vertical position not stated (centred). |
| G3-8-2 | SMITH_ST_BOTH_ARROWS_WHITE | needs-symbol g3-8-1_arrow_left | width 'Varies' (1354 built); arrows centred vertically. |
| G3-8-3 | VICTORIA_ST_ARROW_WHITE | needs-symbol g3-8-3_arrow_left | hands L/R; width 'Varies' (1151); arrow shaft/head not dimensioned (50 grid only). |
| G3-8-4 | VICTORIA_ST_DOUBLE_ARROW_WHITE | needs-symbol g3-8-4_arrow_double | width 'Varies' (1151); double arrow not dimensioned beyond 640x150. |
| G4-1 | A53_MIDLAND_HWY_HAWKER_TORONTO_MT_MARTIN_GREEN | spec | panel width 1233 (heading) / 1243 (chain, sums to 2163) / 60/1060/60 = 1180 (used, satisfies the chain); MIDLAND HWY 120 D is 1136 by AS 1744 vs 1060; parentheses placed as separate glyphs to honour the 85 chain segments; 'Mt Martin' gap 110 derived. |
| G5-1(a) | - | skipped: figure: double street-name blade assembly (NEW / STANDARD ST) - lengths L1/L2 and notes per AS 1742.5, no fixed dimensions |  |
| G5-1(b) | - | skipped: figure: street-name blade with council logo placeholder (STANDARD ST) - length and logo not dimensioned (recommended max per AS 1742.5) |  |
| G5-1(c) | - | skipped: figure: over-long street name example (OVERLONGNAME ST) - letter width reduced to fit, length per AS 1742.5 |  |
| G5-1(d) | PIT_ST_WHITE_BLADE | spec | no margins stated (text centred in the 500 min length). |
| G5-10 | NO_THROUGH_ROAD_YELLOW_PLATE | spec | horizontal positions of NO / THROUGH / ROAD not stated (pixel estimates); 10 edge strips not drawn. |
| G5-11 | PRIDE_ST_BEST_ST_VIA_SERVICE_ROAD_WHITE | needs-symbol g5-11_arrow_diag_up_left |  |
| G5-13 | ZOO_BROWN_FINGERBOARD | spec | width from 500 min chain (525). |
| G5-14 | FOOTBALL_GROUND_BLUE_TWO_LINE | spec | width from chain (967); joint line between sections not drawn. |
| G5-1A | STANDARD_ST_WHITE_BLADE | spec | 10 edge strips (double line) top/bottom with no colour stated - not drawn; length = 100 bracket + ink + 20 min. |
| G5-1B | STANDARD_ST_WHITE_BLADE_LARGE | spec | as G5-1A (133 bracket). |
| G5-2 | STANDARD_ST_1-5_17-43_WHITE_BLADE | spec | as G5-1A; 10+100+50+10 = 170 of 200 (30 gap implied); length not stated (G5-1A margins). |
| G5-3 | STANDARD_ST_1-43_WHITE_BLADE | spec | as G5-1A; right chain 10+50+10+50+10 = 130 of 150; length not stated. |
| G5-4 | CITY_OF_PRIDE_STANDARD_ST_WHITE_BLADE | spec | as G5-1A; CITY OF PRIDE x not stated (centred); length not stated. |
| G5-6 | TO_STANDARD_ST_WHITE_BLADE | spec | length and end margins not stated (G5-1A margins assumed). |
| G5-7 | PEDESTRIAN_WHEELCHAIR_PARKING_BLUE_FINGERBOARD | needs-symbol g5-7_chevron, s22_wheelchair, w6-1_pedestrians | pointed blue fingerboard as offset polygons; chevron run/thickness not dimensioned (90 wide, 170 high only); P drawn as a 100 E letter (note cites symbol S14); pedestrians/wheelchair symbols by reference only. |
| G5-8 | TOWN_HALL_PEDESTRIAN_BLUE | needs-symbol g5-8_arrow_diag_up_right, w6-1_pedestrians | arrow not dimensioned beyond its 115x115 box; Hall alignment under Town not stated. |
| G5-9 | 17-43_WHITE_NUMBER_PLATE | spec | width not stated (ink + 15 margins). |
| G6-1 | ECHUCA_WHITE | spec | corner radius not stated. |
| G6-2 | SWAN_RIVER_WHITE | spec | corner radius not stated. |
| G6-3 | STATE_BORDER_SOUTH_AUSTRALIA_WHITE | spec | STATE BORDER 764 vs AS 1744 792 (3.6%). |
| G6-4 | AUSTRALIAN_CAPITAL_TERRITORY_WHITE | spec |  |
| G6-5 | CITY_OF_ALBURY_SHIRE_OF_HUME_WHITE | spec | CITY OF 406 / SHIRE OF 482 vs AS 1744 435 / 508 (5-7%); 10 strip between panels drawn black (colour not stated). |
| G6-6 | MOONBI_RANGE_914_M_WHITE | spec | MOONBI 687 / RANGE 605 vs AS 1744 668 / 586 (3%). |
| G7-1-1 | PICNIC_300M_ON_LEFT_BLUE_TALL | needs-symbol g7_picnic |  |
| G7-1-2 | PICNIC_TOILETS_300M_ON_LEFT_BLUE | needs-symbol g7_picnic, g7_toilets |  |
| G7-10-1 | NO_FUEL_NEXT_144KM_BLUE_TALL | needs-symbol g7_fuel | km labelled 120 Emod but its 289 width is the 140 Emod width (rendered 140 Emod). |
| G7-11 | PARKING_RIGHT_ARROW_BLUE_WIDE_SKINNY | needs-symbol g7-11_arrow_right | no corner radius stated. |
| G7-12 | PENRITH_PARK_AND_RIDE_BLUE | needs-symbol g1-1_arrow_straight | P 320 E stated 250 wide vs AS 1744 259 (3.7%). |
| G7-13 | HELP_PHONE_BLUE_SQUARE | needs-symbol g7_phone | symbol box chained 400/200 from the sign edge (x 0-400); HELP 80 C 230 vs AS 1744 214 (7%), PHONE 80 B 237 vs 230. |
| G7-14-1 | PICNIC_3KM_BLUE | needs-symbol g7_picnic | picnic box width 'Varies' (375 square assumed); km 203 vs 207 (2%). |
| G7-2-3 | PICNIC_BBQ_TOILETS_300M_ON_RIGHT_BLUE | needs-symbol g7_bbq, g7_picnic, g7_toilets |  |
| G7-3-4 | FIRST_AID_FUEL_CARAVAN_RESTAURANT_LEFT_ARROW_BLUE_TALL | needs-symbol g1-2_arrow_left, g7_caravan, g7_cutlery, g7_first_aid, g7_fuel | arrow height not stated (308 = 251x220 arrow scaled to 350); upper chain 115/420/70/280/115 could not be tied to the symbols. |
| G7-4-3 | RESTAURANT_BED_FUEL_CHEVRON_BLUE_FINGERBOARD | needs-symbol g7_bed, g7_cutlery, g7_fuel | filename G7-4-3, drawing G7-4-3(R): spec has hands L/R drawn R; pointed sign as offset polygons; chevron as polygon from the 100-grid detail. |
| G7-5-2 | CHEVRON_500M_FUEL_BLUE_FINGERBOARD | needs-symbol g7_fuel | drawing G7-5-2(L): hands L/R drawn L; two 'Varies' gaps resolved from the 2000 total; chevron tip taken at the 110 chain figure; no corner radii stated. |
| G7-6-1 | PARKING_P_BLUE_SQUARE | needs-symbol s14_parking_p | filename G7-6-1, drawing G7-6-1A; P as symbol S14. |
| G7-7-1 | PICNIC_TURN_LEFT_300M_BLUE_TALL | needs-symbol g7_picnic |  |
| G7-8-2 | FUEL_RESTAURANT_TURN_RIGHT_300M_BLUE | needs-symbol g7_cutlery, g7_fuel |  |
| G7-9-1 | NEXT_PICNIC_55KM_BLUE | needs-symbol g7_picnic |  |
| G8-10-1 | END_A70_GREEN | spec |  |
| G8-10-2 | END_A70_GREEN_WIDE | spec |  |
| G8-10-3 | END_M79_START_A79_GREEN_TALL | spec |  |
| G8-11-1 | C253_UP_ARROW_GREEN | needs-symbol g8-11-1_arrow_up | arrow 135 on the sign vs 137 detail. |
| G8-11-2 | C253_GREEN_LONG | spec |  |
| G8-12-1 | OD1_RIGHT_ARROW_BLUE | needs-symbol g8-12-1_arrow_up | two variants in one drawing (up arrow / right arrow) -> two spec files with code G8-12-1; numeral '1' width 'Varies'. |
| G8-12-1 | OD1_UP_ARROW_BLUE | needs-symbol g8-12-1_arrow_up | two variants in one drawing (up arrow / right arrow) -> two spec files with code G8-12-1; numeral '1' width 'Varies'. |
| G8-12-2 | CHEVRON_OD1_BLUE_FINGERBOARD | spec | pointed sign as offset polygons (point/obtuse radii not stated); chevron from the 50-grid detail. |
| G8-12-3 | START_OD1_BLUE | spec |  |
| G8-12-4 | END_OD1_BLUE | spec |  |
| G8-9-1 | ROUTE_SHIELD_UP_ARROW_BROWN | needs-symbol g8-9-1_arrow_up | shield as polygon with per-vertex radii; arrow only sized 106x160 on an 18 grid. |
| G8-9-10 | ROUTE_2_WINERY_LEFT_ARROW_BROWN_TALL | needs-symbol g8-9-7_arrow_left, g8_grapes |  |
| G8-9-11 | END_ROUTE_2_BROWN_TALL | spec |  |
| G8-9-12 | END_ROUTE_2_WINERY_BROWN_TALL | needs-symbol g8_grapes |  |
| G8-9-3 | ROUTE_SHIELD_END_BROWN | spec | END top 75 (left chain) vs baseline 165 (right chain) - 10 mm inconsistency. |
| G8-9-4(L) | TOURIST_DRIVE_TURN_LEFT_300M_BROWN | spec |  |
| G8-9-5(L) | CHEVRON_ROUTE_6_TOURIST_DRIVE_BROWN_FINGERBOARD | spec | pointed sign as offset polygons (tip radius not stated); chevron per note a = G7-4-3 geometry (379 overall vs the 385 chain figure); emblem built from the detail (12 white line). |
| G8-9-6 | TOURIST_DRIVE_LENGTH_6KM_START_6_BROWN | spec |  |
| G8-9-7 | ROUTE_6_LEFT_ARROW_BROWN_TALL | needs-symbol g8-9-7_arrow_left |  |
| G8-9-8 | UP_ARROW_WINERY_SHIELD_BROWN_TALL | needs-symbol g8-9-8_arrow_up, g8_grapes | grapes emblem size inside the shield not dimensioned. |

## Width mismatches left (drawing figure kept as `expect`, AS 1744 width in brackets)
G1-4 MT MARTIN HWY 1260 (1335); G3-3 '18' 189 (183.5); G4-1 MIDLAND HWY 1060 (1136); G6-3 STATE BORDER 764 (792); G6-5 CITY OF 406 (435), SHIRE OF 482 (508); G6-6 MOONBI 687 (668), RANGE 605 (586); G7-12 P 250 (259); G7-13 HELP 230 (214), PHONE 237 (230); G7-14-1 km 203 (207).

## Generator features needed / gaps
* Symbol placement skips the width check (BLOCKED specs report no `expect` results); widths for those specs were checked with an external script.
* A white polygon-shaped sign (G3-5 pointed white fingerboard) has no outline: `keyline` only follows the built-in shape, not polygon elements.
* Stacked guide signs (G1-1, G1-2, G1-6) and pointed fingerboards (G2-1, G2-4, G5-7, G7-4-3, G7-5-2, G8-9-5, G8-12-2) had to be built from polygons with per-vertex radii and hand-computed offset polygons for the edge/border; an `edge`/`border` that follows a polygon outline would remove the hand arithmetic.
* Text `expect` for a two-word line whose drawing gives only the total (Martins Ck, Mary Hill, Mt Martin) is recorded as `expect_total` (ignored by the generator) with the gap derived from it.
* Lower-case-only words on a shared baseline ('m', 'km') are placed by giving `top` = baseline - height; a `baseline` key would be clearer.
* Drawings that contain two variants under one code (G3-4, G8-12-1) produce two manifest rows with the same code.
* No rasteriser in the venv; spot checks were done with cairosvg installed into the scratch venv.

## Drawings whose true orientation differs from the page
G1-1, G1-3, G1-5 and G2-4 are drawn rotated 90 deg (text reads bottom-to-top); all four are transcribed upright (rotate the page clockwise). The G1-3 and G1-5 symbol details are drawn in the page orientation, the G1-1 arrow detail in the true orientation.
