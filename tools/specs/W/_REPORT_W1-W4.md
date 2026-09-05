# W1 / W2 / W3 / W4 / W9 / WM3-2A — spec report

51 drawings (every PNG starting W1-, W2-, W3-, W4-, W9-, WM). 52 spec files (W4-6 added from the W4-4 drawing's lower diamond).
Counts: **spec 4** (text/polygon only, generated OK), **needs-symbol 46**, **skipped 1** (W1-8(alt), symbol sheet).
Generator run on `tools/specs/W/*.json`: no width mismatch on any of these codes (the 4 reported mismatches are W5–W8 specs by others).
All 750 diamonds: bounding square 1060.66, R50, 10 yellow edge, 30 black border; diamond centre c = 530.33. Every symbol box was
cross-checked against the drawn symbol by pixel measurement of the PNG (agreement within ~5 mm unless flagged).

| code | name | status | flags |
|---|---|---|---|
| W1-1 | {LEFT/RIGHT}_TURN_YELLOW_DIAMOND (hands L,R; drawn L) | needs-symbol w1-1_turn_arrow_l | fully dimensioned; box 500x485 from 60 / 260 offsets |
| W1-2 | {dir}_REVERSE_TURN_YELLOW_DIAMOND | needs-symbol w1-2_reverse_turn_arrow_l | fully dimensioned; 425x630 from 85 / 260 |
| W1-3 | {dir}_CURVE_YELLOW_DIAMOND | needs-symbol w1-3_curve_arrow_l | height 511 derived from inset geometry (not stated); inset geometry gives tip 372.4 from stem edge vs 375 (300+75) stated |
| W1-4 | {dir}_REVERSE_CURVE_YELLOW_DIAMOND | needs-symbol w1-4_reverse_curve_arrow_l | fully dimensioned; 435x615 from 80 / 260 (100 to tip axis consistent) |
| W1-5 | {dir}_WINDING_ROAD_YELLOW_DIAMOND | needs-symbol w1-5_winding_road_l | width 320 derived (2 x (30+R130)); height 800 = 595+205; bottom 375 |
| W1-7 | {dir}_HAIRPIN_BEND_YELLOW_DIAMOND | needs-symbol w1-7_hairpin_arrow_l | height 610 derived (415 + outer R195); 455 wide; 65 / 275 offsets |
| W1-8(alt) | — | skipped: symbol sheet (truck + 4 arrows, 150 grid) for W1-8-1..5 | all arrow/truck dims copied into the W1-8-x `symbols` descs |
| W1-8-1 | TRUCK_ROLLOVER_{speed}_KMH_YELLOW_TALL (L,R; vary) | needs-symbol w1-8_truck_rollover_l | 20 yellow edge + 40 black border read from "20"/"60" (pixel check); bottom row 185/Varies/220/220/185 is the W1-8-2..5 layout, not this sign — 25 drawn ~45 off-centre with no dim, centred in spec; km/h centred; vary values 15–95 chosen |
| W1-8-2 | TRUCK_ROLLOVER_CURVE_{speed}_YELLOW_TALL | needs-symbol w1-8_truck_rollover_l, w1-8_curve_arrow_l | numerals left-aligned at 185 (185/Varies/220/220/185); arrow 1130x1140 at 185..1315 |
| W1-8-3 | TRUCK_ROLLOVER_TURN_{speed}_YELLOW_TALL | needs-symbol w1-8_truck_rollover_l, w1-8_turn_arrow_l | as W1-8-2 |
| W1-8-4 | TRUCK_ROLLOVER_REVERSE_CURVE_{speed}_YELLOW_TALL | needs-symbol w1-8_truck_rollover_l, w1-8_reverse_curve_arrow_l | arrow 870x1230 at 445..1315 (445/870/185), gap 85 |
| W1-8-5 | TRUCK_ROLLOVER_HAIRPIN_{speed}_YELLOW_TALL | needs-symbol w1-8_truck_rollover_l, w1-8_hairpin_arrow_l | **drawing inconsistent**: chain 130+1336+69+45+1230+150 = 2960 (40 short); alt sheet says hairpin 1215 tall; drawn arrow bottom is aligned with numeral bottom (2850). Spec uses stated 45 gap + 1230 (bottom 2810) |
| W1-9-2 | EXIT_SPEED_CURVE_{speed}_YELLOW_TALL (L,R; vary) | needs-symbol w1-9-2_curve_arrow_l | 20 edge + 40 border (from 20/60, pixel check); right chain sums to 2400 and is used; left 310/125 does not reconcile with 200/190; text widths OK (612/940/544) |
| W1-9-3 | EXIT_SPEED_TURN_{speed}_YELLOW_TALL | needs-symbol w1-9-3_turn_arrow_l | as W1-9-2; arrow 650 wide |
| W1-9-4 | EXIT_SPEED_REVERSE_CURVE_{speed}_YELLOW_TALL (drawn R) | needs-symbol w1-9-4_reverse_curve_arrow_r | drawing illustrates the R hand; arrow 464 wide |
| W1-9-5 | EXIT_SPEED_HAIRPIN_{speed}_YELLOW_TALL | needs-symbol w1-9-5_hairpin_arrow_l | arrow 491 wide (454/491/455) |
| W1-10 | TRAM_{speed}_YELLOW_TALL (vary) | needs-symbol w1-10_tram | ring 20 thick (stated, pixel check); tram 300x160 not otherwise dimensioned (25 grid); vary values 10–60 chosen |
| W2-1 | CROSS_ROAD_YELLOW_DIAMOND | needs-symbol w2-1_crossroad | inset chain 240+155+80+235 = 710 vs sign 375+80+235 = 690 — sign used (pixel check agrees with 690) |
| W2-3 | T_INTERSECTION_YELLOW_DIAMOND | spec (polygon) | fully dimensioned T; crossbar bottom on centreline |
| W2-4 | SIDE_ROAD_YELLOW_DIAMOND (L,R) | needs-symbol w2-4_side_road_l | same 710/690 discrepancy as W2-1 |
| W2-7 | ROUNDABOUT_YELLOW_DIAMOND | needs-symbol w2-7_roundabout | box = R312 construction square centred; tracer must keep that square as viewBox (artwork extents asymmetric: -318..+288 / -304..+286) |
| W2-8 | STAGGERED_SIDE_ROADS_YELLOW_DIAMOND (L,R) | needs-symbol w2-8_staggered_side_roads_l | sign bottom row "200/55/55" contradicts inset 150/110/150 and the drawn symbol (410 wide) — inset used; 710/690 discrepancy |
| W2-9 | SIDE_ROAD_CURVE_OUTSIDE_YELLOW_DIAMOND (L,R) | needs-symbol w2-9_side_road_curve_l | **inset states 285 (arc centre) and 240 (arrowhead) but the drawn symbol matches R235 / 220 as W1-3** (tip 297 from centreline measured); no overall width/height on sign — derived from geometry |
| W2-10 | SIDE_ROAD_CURVE_INSIDE_YELLOW_DIAMOND (L,R) | needs-symbol w2-10_side_road_curve_inside_l | same 285/240 vs R235/220 flag; extents derived |
| W2-11(L) | STAGGERED_SIDE_ROADS_LEFT_CURVE_YELLOW_DIAMOND | needs-symbol w2-11_l | angles 37+20+20 = 77° (drawn symbol confirms 77°); W2-11(R) is 75° and has the arms in the other order (not a mirror); extents derived |
| W2-11(R) | STAGGERED_SIDE_ROADS_RIGHT_CURVE_YELLOW_DIAMOND | needs-symbol w2-11_r | 20+25+30 = 75°; extents derived |
| W2-12(L) | STAGGERED_SIDE_ROADS_LEFT_CURVE_YELLOW_DIAMOND | needs-symbol w2-12_l | mirror of W2-11(R) geometry (75°); extents derived |
| W2-12(R) | STAGGERED_SIDE_ROADS_RIGHT_CURVE_YELLOW_DIAMOND | needs-symbol w2-12_r | 37+20+20 = 77° as W2-11(L); extents derived |
| W2-13 | TWO_SIDE_ROADS_YELLOW_DIAMOND (L,R) | needs-symbol w2-13_two_side_roads_l | 710/690 discrepancy as W2-1 |
| W2-14 | T_INTERSECTION_ON_CURVE_YELLOW_DIAMOND (L,R; drawn R) | needs-symbol w2-14_t_on_curve_r | width 525 and bottom 340 / corner 30 stated; height 734 derived from inset (crossbar overhang 245 each side) |
| W2-15 | CROSS_ROAD_ON_CURVE_YELLOW_DIAMOND (L,R) | needs-symbol w2-15_crossroad_on_curve_l | extents derived (R235, 220 arrowhead) |
| W2-16 | CURVE_AND_STRAIGHT_YELLOW_DIAMOND (L,R) | needs-symbol w2-16_curve_and_straight_l | extents derived |
| W3-1 | STOP_SIGN_AHEAD_YELLOW_DIAMOND | needs-symbol w3-1_up_arrow (octagons drawn as polygons) | octagon corner radius not stated (square corners used); 12 white strip |
| W3-2 | GIVE_WAY_SIGN_AHEAD_YELLOW_DIAMOND | needs-symbol w3-1_up_arrow, w3-2_give_way_emblem | red band width / inner white triangle not dimensioned (multi-colour symbol) |
| W3-3-1 | SIGNALS_AHEAD_YELLOW_DIAMOND | needs-symbol w3-3_signals | no position dim on sign; placed with middle lamp on sign centre (matches drawing); hook 25+5 read from inset |
| W3-3-2 | SIGNALS_AHEAD_YELLOWGREEN_DIAMOND | needs-symbol w3-3_signals | as W3-3-1 on fluorescent yellow-green |
| W3-4-1 | SPEED_HUMP_AHEAD_YELLOW_DIAMOND | needs-symbol w3-1_up_arrow (hump drawn as path) | hump fully dimensioned (R250 consistent with 436 chord / 128 rise) |
| W3-4-2 | SPEED_HUMP_AHEAD_DIAGONAL_YELLOW_DIAMOND (L,R) | needs-symbol w3-1_up_arrow (rotated 45°) | 346 (arrow top) vs inset 275/263 disagree by ~8 mm on a 45° arrow; 346 used for y, 263 for x. Generator: hand mirror is applied inside `rotate` (centre/angle not mirrored) → per-hand elements with `mirror:false` used |
| W3-4-3 | SPEED_HUMP_SIDE_ROAD_YELLOW_DIAMOND (L,R) | needs-symbol w3-1_up_arrow (rotated 90°) | same generator rotate/mirror issue handled with per-hand elements |
| W4-1 | NARROW_BRIDGE_YELLOW_DIAMOND | needs-symbol w4-1_narrow_bridge | no position dims (centred as drawn); overall width not dimensioned — 375 taken from the grid (outer corners 10 squares apart) |
| W4-3 | ROAD_NARROWS_YELLOW_DIAMOND | needs-symbol w4-3_road_narrows | fully dimensioned; 294 top |
| W4-4 | DIVIDED_ROAD_YELLOW_DIAMOND | needs-symbol w4-4_divided_road | no position dims (centred as drawn) |
| W4-6 | DIVIDED_ROAD_ENDS_YELLOW_DIAMOND | needs-symbol w4-4_divided_road (flip v) | extra spec from the W4-4 drawing's lower diamond ("W4-6 (W4-4 INVERTED)"); no PNG of its own |
| W4-5 | ISLAND_YELLOW_DIAMOND | spec | 150 D, 669 |
| W4-8 | LOW_CLEARANCE_{clearance}_M_YELLOW_DIAMOND (vary) | spec (runs) | m drawn 34 below numeral top = 194 vs 200 (6 mm inconsistency); common baseline used; clearance values chosen |
| W4-9 | LEFT_LANE_ENDS_YELLOW_DIAMOND | spec | 120 E x3, 413/460/455 |
| W4-10 | THREE_LANE_TWO_WAY_YELLOW_DIAMOND | needs-symbol w4-10_arrow_up (x3, two rotated 180) | 256/206 are measured from the middle arrow axis (23 off centre), confirmed by pixels |
| W4-11 | TWO_WAY_TRAFFIC_YELLOW_DIAMOND | needs-symbol w4-11_arrow_up (x2) | no vertical dim on sign (centred as drawn) |
| W9-1 | ROUTE_TURN_AT_T_YELLOW_DIAMOND (L,R) | needs-symbol w9-1_l | fully dimensioned; 140 / 295 offsets |
| W9-2 | ROUTE_TURN_SIDE_ROAD_YELLOW_DIAMOND (L,R) | needs-symbol w9-2_l | height 465 derived (barb 95 above arm top + 60 + 310) |
| W9-3 | ROUTE_TURN_CROSSROAD_YELLOW_DIAMOND (L,R) | needs-symbol w9-3_l | fully dimensioned 675x570 |
| WM3-2A | GIVE_WAY_AHEAD_YELLOW_SQUARE | needs-symbol w3-1_up_arrow, w3-2_give_way_emblem | arrow width not dimensioned (50 grid); drawn arrow 152x131 matches the W3-1 arrow proportion, reused at 133 tall |

## Flags (summary)

Drawing inconsistencies
1. W2-1, W2-4, W2-8, W2-13: inset vertical chains sum to 710, sign chains to 690 (sign values used, pixel check agrees).
2. W2-8: sign bottom row "200 | 55 | 55" is copied from W2-4; inset/drawn symbol has 150 arms.
3. W2-9, W2-10: inset states arc centre 285 and arrowhead 240; the drawn symbols match R235 / 220 (W1-3 geometry). All W2 curve insets label the arrowhead "240" to the 20 notch line (= 220 to the barb line).
4. W2-11(L) and W2-12(R): angles sum to 77° (37+20+20); W2-11(R)/W2-12(L) sum to 75°. The two hands of W2-11 are not mirror images (arm order differs) — transcribed as drawn.
5. W1-8-5: vertical chain sums to 2960; arrow height 1230 vs 1215 on the symbol sheet; drawn arrow bottom aligned to 2850.
6. W1-8-1: bottom dimension row belongs to W1-8-2..5; numerals drawn ~45 mm off-centre with no dimension.
7. W1-9-x: left-hand 310 | 125 does not reconcile with the right-hand 200 | 190 chain (right chain used).
8. W4-8: "34" + 160 Emod = 194 ≠ 200 D.
9. W3-4-2: 346 (arrow top) vs 275/263 (inset) differ by ~8 mm for a 250x219 arrow at 45°.
10. Missing dimensions (stated in notes): overall extents of every curve-family symbol (W1-3, W1-5, W1-7, W2-9..16, W9-2 height) — derived from inset geometry; symbol positions of W3-3-x, W4-1, W4-4, W4-11 (centred as drawn); W4-1 overall width (grid); WM3-2A arrow width; W3-2 give-way band widths; W3-1 octagon corner radius; W1-10 tram geometry.
11. Border reading for the 1500x3000 and 1400x2400 signs: "20" and "60" taken as 20 yellow edge + 40 black border (pixel check ≈40 black) — confirm.

Generator features needed / issues
1. Symbol `rotate` with hands: the hand mirror (`flip h`) is composed inside the rotation, so the rotation centre and angle are not mirrored — a rotated symbol on a handed spec renders wrongly for the other hand. Worked around with per-hand elements (`hand`, `mirror:false`, opposite angle) on W3-4-2 / W3-4-3; a proper fix would mirror the rotation.
2. `flip:"v"` mirrors about the sign centreline, not the box (fine for W4-6 because the box is centred; documented in notes).
3. Symbol fitting uses min-scale and centres in the box, so a traced symbol's viewBox must be exactly the bbox given here (W2-7 needs the full R312 square as viewBox).
4. Names for handed symbol signs: used `hand_values` (`{dir}`) on W1-1..W1-7 so files read LEFT_/RIGHT_; the rest are hand-neutral (the code suffix carries the hand).

Decisions
* Vary values: advisory speeds 15–95 (W1-8-x, W1-9-x), 10–60 (W1-10), clearances 2.2–4.5 m (W4-8) — not stated on the drawings; adjust as needed.
* W3-1 octagons and W2-3 T drawn as polygons, W3-4-x hump as a path (all fully dimensioned); the W3-1 up arrow (250x219) is reused for W3-2, W3-4-1/2/3 and WM3-2A.
