# W5 / W6 / W7 / W8 transcription report (88 drawings; W5-1 pre-existing, untouched)

Status key: **spec** = complete, generator renders it; **needs-symbol** = complete except the listed symbol artwork
(tools/symbols/<id>.svg) which is placed by bounding box only. Nothing skipped.
Diamonds are drawn as bounding squares (side x 1.41421); all bottom "left | word | right" dims on the 750 diamonds sum to 1019,
i.e. they are measured between the R50-rounded tips, so `cx` = 20.73 + left + width/2 whenever a word is dimensioned off-centre.

| code | name | status | flags |
|---|---|---|---|
| W5-2 | OPENING_BRIDGE_YELLOW_DIAMOND | spec | |
| W5-6 | FORD_YELLOW_DIAMOND | spec | word drawn 24 mm right of centre (157/753/109); honoured with cx |
| W5-7-1 | FLOODWAY_YELLOW_DIAMOND | spec | 4 mm right of centre (160/708/150), cx |
| W5-7-2 | FLOODWAYS_YELLOW_DIAMOND | spec | 3 mm right of centre (118/789/112), cx |
| W5-8 | LOW_LEVEL_BRIDGE_YELLOW_DIAMOND | spec | LEVEL bottom 13 *below* the centreline (checked on the illustration) |
| W5-9 | DIP_YELLOW_DIAMOND | spec | 11 mm right of centre (237/568/215), cx |
| W5-10 | HUMP_YELLOW_DIAMOND | spec | hump drawn as a `path` from the fully dimensioned inset (738 x 184, bar 56, R250) |
| W5-11 | CREST_YELLOW_DIAMOND | spec | |
| W5-12 | STEEP_DESCENT_YELLOW_DIAMOND | needs-symbol w5-12_car_steep_descent | no placement dims on the sign; centred (illustration shows it centred) |
| W5-13 | STEEP_ASCENT_YELLOW_DIAMOND | needs-symbol w5-13_car_steep_ascent | as W5-12 |
| W5-14 | GATE_YELLOW_DIAMOND | spec | |
| W5-16 | GRID_YELLOW_DIAMOND | spec | |
| W5-18 | ROAD_ENDS_YELLOW_DIAMOND | spec | both words ~11 mm right of centre, cx |
| W5-19 | GRAVEL_ROAD_YELLOW_DIAMOND | spec | GRAVEL 7 mm right of centre, cx |
| W5-20 | SLIPPERY_YELLOW_DIAMOND | needs-symbol w5-20_slippery_car | overall bbox not stated; 605 x 553 measured (left/bottom dims stated) |
| W5-22 | TRUCKS_YELLOW_DIAMOND | needs-symbol w5-22_truck | height not stated (cab roof above the 195 body); 280 from grid |
| W5-29 | KANGAROOS_YELLOW_DIAMOND | needs-symbol w5-29_kangaroo | |
| W5-30 | AIRCRAFT_YELLOW_DIAMOND | needs-symbol w5-30_aircraft | inset 560/646 are along the 16-degree axes; bbox width 600 measured |
| W5-33 | SLOW_POINT_YELLOW_DIAMOND | spec | 31 is centreline-to-POINT-top; SLOW 11 mm left of centre, cx |
| W5-34 | MERGING_TRAFFIC_YELLOW_DIAMOND | needs-symbol w5-34_merge_arrow | one PNG, hands L/R (drawn L) |
| W5-35 | LANE_MERGE_YELLOW_DIAMOND | needs-symbol w5-35_lane_merge | 900 diamond (Illust. C); hands L/R; left extent not stated, 247/698 measured |
| W5-36 | FIRE_STATION_YELLOW_DIAMOND | spec | no offset dim; STATION top sits on the centreline (drawing + illustration) |
| W5-37 | AMBULANCE_STATION_YELLOW_DIAMOND | spec | 125 B / 125 C; AMBULANCE bottom on the centreline (drawing + illustration) |
| W5-38 | CATTLE_YELLOW_DIAMOND | needs-symbol w5-38_cattle | |
| W5-41 | TRAM_YELLOW_DIAMOND | needs-symbol w5-41_tram | overall height not stated; 330 from grid |
| W5-42 | FALLING_ROCKS_YELLOW_DIAMOND | needs-symbol w5-42_falling_rocks | hands L/R (drawn L); wedge tip at the diamond's left corner |
| W5-43 | UNEVEN_SURFACE_YELLOW_DIAMOND | spec | SURFACE 9.5 mm left of centre, cx |
| W5-44 | CAMELS_YELLOW_DIAMOND | needs-symbol w5-44_camel | drawing inconsistency: 221 above + 221 below = 442 but symbol is 432 (illustration: bottom 211); top dim used |
| W5-45 | EMUS_YELLOW_DIAMOND | needs-symbol w5-45_emu | |
| W5-46 | HORSES_YELLOW_DIAMOND | needs-symbol w5-46_horse | |
| W5-47 | KOALAS_YELLOW_DIAMOND | needs-symbol w5-47_koala | |
| W5-48 | WOMBATS_YELLOW_DIAMOND | needs-symbol w5-48_wombat | |
| W5-49 | WILD_ANIMALS_YELLOW_DIAMOND | spec | 20 is ANIMALS-top-to-centreline (above); ANIMALS 6 mm right, cx |
| W5-50 | TRACTORS_YELLOW_DIAMOND | needs-symbol w5-50_tractor | overall height not stated; 385 from grid; width 545 = 42+24+196+220+63 |
| W5-51 | DEER_YELLOW_DIAMOND | needs-symbol w5-51_deer | |
| W5-52 | CASSOWARIES_YELLOW_DIAMOND | needs-symbol w5-52_cassowary | |
| W5-53 | HORSE_RIDERS_YELLOW_DIAMOND | needs-symbol w5-53_horse_rider | |
| W5-54 | MOTORCYCLE_SLIPPERY_YELLOW_DIAMOND | needs-symbol w5-54_motorcycle_slippery | |
| W5-55-1 | CONCEALED_DRIVEWAY_YELLOW_DIAMOND | spec | |
| W5-55-2 | CONCEALED_DRIVEWAYS_YELLOW_DIAMOND | spec | |
| W5-56 | WILDLIFE_YELLOW_DIAMOND | spec | WIDTH MISMATCH: stated 669 vs 150 C = 726 (illustration measures ~721, agrees with 150 C); noted, series kept |
| W6-1 | PEDESTRIANS_YELLOWGREEN_DIAMOND | needs-symbol w6-1_pedestrians | yellow-green ground |
| W6-2 | PEDESTRIAN_CROSSING_AHEAD_YELLOWGREEN_DIAMOND | needs-symbol w6-2_legs | arrow as polygon (R8 barb tips not applied: polygon radius is all-or-nothing); annulus R225/R210; legs bbox measured (~328 x 240); 45-degree arrow variant not generated |
| W6-3 | CHILDREN_YELLOWGREEN_DIAMOND | needs-symbol w6-3_children | |
| W6-7 | BICYCLES_YELLOW_DIAMOND | needs-symbol w6-7_bicycle | overall bbox not stated (inset gives construction dims); 650 x 428 measured |
| W6-8 | ROAD_AHEAD_YELLOW_DIAMOND | spec | 450 diamond (Illust. B), R30 / 8 / 23 |
| W6-9 | SHARED_PATH_YELLOW_DIAMOND | needs-symbol w6-9_pedestrian w6-9_bicycle | 600 diamond (Illust. A); bicycle top on the centreline |
| W6-10 | BICYCLE_GRATE_HAZARD_YELLOW_DIAMOND | needs-symbol w6-10_cyclist_grate | 600 diamond (Illust. C) |
| W6-11 | BICYCLE_SLIPPERY_YELLOW_DIAMOND | needs-symbol w6-11_bicycle_slippery | 600 diamond |
| W6-12 | BICYCLE_STEEP_DESCENT_YELLOW_DIAMOND | needs-symbol w6-12_bicycle_descent | 600 diamond |
| W6-13 | BICYCLE_STEEP_ASCENT_YELLOW_DIAMOND | needs-symbol w6-13_bicycle_ascent | 600 diamond |
| W7-2-2 | {tracks}_TRACKS_WHITE_WIDE_SKINNY | spec | 1000 x 150 white, no border shown; numeral varies 2-6 (values chosen) |
| W7-4 | RAILWAY_CROSSING_LIGHTS_YELLOW_DIAMOND | needs-symbol w7-4_crossbuck_lights | overall height not stated (inset 480 is from the post top); 540 measured; width 400 from arm geometry |
| W7-7 | TRAIN_YELLOW_DIAMOND | needs-symbol w7-7_train | hands L/R; overall height not stated; 580 measured |
| W7-8 | RAILWAY_CROSSING_AHEAD_YELLOW_DIAMOND | needs-symbol w7-8_rail_crossing | no placement dims; centred (illustration confirms) |
| W7-9 | RAILWAY_CROSSING_SKEW_YELLOW_DIAMOND | needs-symbol w7-9_rail_crossing_skew | hands L/R; width and placement not stated; 534 wide, centred (measured) |
| W7-12 | SIDE_ROAD_RAILWAY_YELLOW_DIAMOND | needs-symbol w7-12_side_road_rail | PNG shows (R) with dims: drawn_hand R; vertical placement not stated, centred |
| W7-13 | CROSS_ROAD_RAILWAY_YELLOW_DIAMOND | needs-symbol w7-13_cross_road_rail | drawn_hand R; no placement dims, centred |
| W7-14-4 | LOOK_FOR_TRAINS_{tracks}_TRACKS_WHITE_TALL | needs-symbol w7-14_train | 300 x 450 white, R25, 5 edge + 10 border; GENERATOR: numeral (30 E) + TRACKS (30 D) group cannot be centred as one unit (see flags); word gap for FOR TRAINS derived from the 232 total |
| W7-14-5 | LOOK_FOR_TRAINS_WHITE_TALL | needs-symbol w7-14_train | |
| W7-14-6 | DO_NOT_CROSS_LIGHTS_{tracks}_TRACKS_WHITE | spec | 450 x 400 white; word gaps derived from line totals; numeral/TRACKS group as W7-14-4; single-track version (70 pitch, no TRACKS line) not generated |
| W7-15 | RAILWAY_GATE_YELLOW_DIAMOND | spec | GATE 9 mm left of centre, cx |
| W7-17 | T_JUNCTION_RAILWAY_YELLOW_DIAMOND | needs-symbol w7-17_t_junction_rail | hands L/R; inset height 475 vs illustration ~486 (10 mm) |
| W8-2 | {speed}_KMH_YELLOW | spec | numerals 240 E "medium spacing" -> tracking minus10; km/h 85 Emod; values 15-110 step 5 |
| W8-3 | ON_SIDE_ROAD_YELLOW | needs-symbol w8-3_arrow | hands L/R (drawn L); arrow 400 x 100 as symbol (29/9 notch not resolvable as a polygon) |
| W8-5 | {dist}_M_YELLOW_WIDE | spec | GENERATOR: numeral 140 E + "m" 120 Emod group centring (fixed x for "100"); "m" Emod cap height on the numeral baseline |
| W8-7 | WHEN_WET_YELLOW | spec | WHEN 6 mm left of centre, cx |
| W8-8 | WHEN_FROSTY_YELLOW | spec | FROSTY 7.5 mm right, cx |
| W8-9 | UNDER_SNOW_YELLOW | spec | cx 377.5 / 374.5 |
| W8-13 | PLAYGROUND_YELLOWGREEN | spec | yellow-green |
| W8-14 | SCHOOL_YELLOWGREEN_WIDE | spec | |
| W8-15 | MERGE_RIGHT_YELLOW | needs-symbol w8-3_arrow | W8-3 arrow flipped h |
| W8-16 | ONE_LANE_YELLOW | spec | |
| W8-17-1 | NEXT_{km}_KM_YELLOW | spec | GENERATOR: numeral 125 E + km 105 Emod group centring (fixed x for "33"; 1-digit values off-centre) |
| W8-17-2 | NEXT_{m}_M_YELLOW | spec | as W8-17-1 |
| W8-18 | AGED_YELLOWGREEN_WIDE | spec | |
| W8-19 | BLIND_YELLOWGREEN_WIDE | spec | |
| W8-20 | DISABLED_YELLOWGREEN_WIDE | spec | |
| W8-21 | BOGGY_WHEN_WET_YELLOW_SQUARE | spec | WIDTH MISMATCH x3: stated 406/501/316 vs 140 D/E/E = 601/569/398; the drawing's own illustration measures ~593/564/437, so the stated widths are wrong; series kept |
| W8-22 | CROSSING_AHEAD_YELLOWGREEN | spec | |
| W8-23 | TWO_WAY_ARROW_YELLOW_WIDE | needs-symbol w8-23_double_arrow | vertical placement not stated; centred |
| W8-24 | PRESCHOOL_YELLOWGREEN_WIDE | spec | |
| W8-25 | REFUGE_ISLAND_YELLOWGREEN | spec | |
| W8-26 | ADDED_LANE_YELLOW | spec | 900 x 600 (Illust. C), R60 / 15 / 45 |
| W8-27 | PREPARE_TO_STOP_RED_LONG | spec | red ground, white letters, no border |
| W8-28 | CROSSING_RAMP_YELLOW | spec | RAMP 5.5 mm right, cx |
| W8-29 | ON_BRIDGE_WHEN_FROSTY_YELLOW_TALL | spec | 750 x 900; baselines 220 + 195 pitch |
| W8-30 | CURVE_TIGHTENS_YELLOW | spec | |

## Counts
* spec: 46 (incl. W5-10 drawn as a path and W6-2 whose arrow/annulus are drawn; W6-2 still needs its legs symbol and is counted below)
* needs-symbol: 42 (40 distinct symbol ids; w7-14_train and w8-3_arrow are shared)
* skipped: 0

## Flags
### Drawing inconsistencies
* W5-56: stated WILDLIFE width 669 vs 150 C = 726 (illustration ~721). Generator mismatch left, explained in notes.
* W8-21: stated widths 406 / 501 / 316 vs 140 D / 140 E / 140 E = 601 / 569 / 398 (illustration ~593 / 564 / 437). Three generator mismatches left, explained in notes.
* W5-44: 221 above + 221 below the centreline = 442 but the camel is 432 high.
* W7-17: inset height 475 vs illustrated ~486.
* Several diamonds dimension a word a few mm off-centre (W5-6 24 mm, W5-9 11 mm, W5-18 11 mm, ...); honoured with `cx` as drawn.

### Dimensions missing from the drawings (bbox/placement taken from the 37.5 grid inset or measured on the illustration, stated in each spec's notes)
* Overall symbol bbox not stated: W5-20, W5-22 (height), W5-30 (width), W5-35 (left extent), W5-41 (height), W5-50 (height), W6-2 (legs), W6-7, W7-4 (height), W7-7 (height), W7-9 (width).
* Symbol placement on the sign not stated: W5-12, W5-13, W7-8, W7-9, W7-13, W7-12 (vertical), W8-23 (vertical) — all shown centred on the illustration and placed centred.
* W5-36 / W5-37: no explicit offset from the centreline; the line stack's edge coincides with the centreline on the drawing.

### Generator features needed (not worked around by guessing)
1. **Mixed series/height within one line** (`words` with per-word `series`/`height`), or **group centring of several elements**: W7-14-4, W7-14-6 (numeral 30 E + TRACKS 30 D), W8-5 (140 E + 120 Emod), W8-17-1 / W8-17-2 (125 E + 105 Emod). Written as two elements at fixed x computed for the illustrated numeral, so other `vary` values are off-centre by half the width difference.
2. **Per-corner radius on polygons**: W6-2 arrow has R8 barb tips only (polygon radius applies to every corner, so none applied).
3. **Alternate layouts of one drawing**: W7-14-6 single-track version (line pitch 70, TRACKS line removed) and the W6-2 45-degree arrow option are not expressible with `vary`.
4. Nice-to-have: word-space gap could be derived automatically from a stated total width (done by hand here: FOR TRAINS, DO NOT CROSS, WHILE LIGHTS, ARE DISPLAYED, OR ALARM).

### Other decisions
* PNGs named `W5-34(L)`, `W5-35(L)`, `W7-7(L)`, `W7-9(L)` each show BOTH the (L) and (R) sign (there is no separate (R) PNG), so they are written as one spec each with `hands: [L, R]` under the plain code (`W5-34.json` etc.), which generates `..._W5-34(L).svg` and `..._W5-34(R).svg`. W5-42, W7-12, W7-13, W7-17 and W8-3 likewise show both hands in one PNG (plain filename).
* `vary` value lists chosen where the drawing says "Varies": W7-2-2 / W7-14-4 / W7-14-6 tracks 2-6; W8-2 advisory speeds 15-110 step 5; W8-5 / W8-17-2 distances 50-500; W8-17-1 km 1-50.
* Lower-case Emod text (km/h, km, m) is set with the stated number as the capital height and the baseline shared with the numerals; the resulting ink widths match the drawings (356/357, 216/217, 131/132, 115/116), which supports that reading.
* W7-2-2 and W8-27 have no border (none drawn/captioned).
