# R1–R5 transcription report (AS 1743-2023, 66 drawings)

Status: `spec` = generated and width-checked; `needs-symbol <ids>` = spec written, blocked until the symbol SVG is traced;
`skipped <why>`; `existing` = left untouched. Widths were checked with `signgen.py` (AS 1744 spacing, ±2 %).
Symbol ids and the drawing dims for the tracer are in each spec's `symbols` block.

| Drawing (PNG) | Spec / name | Status | Flags |
|---|---|---|---|
| R1-1 | STOP_SIGN | existing | — |
| R1-2 | GIVE_WAY | existing | — |
| R1-3 | ROUNDABOUT_GIVE_WAY | needs-symbol r1-3_roundabout_arrows | bbox is the 281 square about the symbol centre (88 inner R + 37 band + 15.5 head overhang); the symbol file must use that square as its viewBox. |
| R2-2(L) | R2-2 ONE_WAY_ARROW_WHITE_TALL (hands L,R) | needs-symbol r2-2_arrow_left | Drawing stack 68+120+40+120+44+120+68 = 580 ≠ 600 (the 44 verified by zoom); laid out from the top, bottom gap becomes 88. |
| R2-3(L) (both hands) | R2-3(L) KEEP_LEFT_WHITE_TALL, R2-3(R) KEEP_RIGHT_WHITE_TALL | needs-symbol r2-3_arrow_down_left | Drawing's L/R dims put both text lines 6–7.5 mm right of centre (KEEP 101\|263\|86); transcribed with `cx`. Grid shows the arrow unrotated (406×168); on the sign it is 342×272 at 45°. |
| R2-4 | NO_ENTRY | existing | (pre-existing NO 116 vs 121 mismatch, not touched) |
| R2-5 | NO_U_TURN_WHITE_SQUARE | needs-symbol r2-5_u_turn_arrow | Annulus, red slash (44 @ 45°, clipped to R220) and white halo (grid's "18" read as the gap each side of the slash) are built as paths; only the arrow is a symbol. Arrow vertical position from the grid's 100/37/88 stack. |
| R2-6(L) (both hands) | R2-6 NO_LEFT_TURN_WHITE_SQUARE (hands L,R) | needs-symbol r2-6_left_turn_arrow | As R2-5; halo gap "12". Arrow bbox derived: 27+250 high (the 250 runs from bar top to stem bottom), 243 wide, stem 33+56 right of centre. |
| R2-7 | STRAIGHT_AHEAD_ONLY_WHITE_TALL | needs-symbol r2-7_arrow_up | ONLY dims 49\|359\|42 (centre 3.5 right) – centred. Head 174 = 75+75 + 2×R12. |
| R2-9(L) (both hands) | R2-9(L) LEFT_LANE_MUST_TURN_LEFT_WHITE_TALL, R2-9(R) RIGHT_LANE_MUST_TURN_RIGHT_WHITE_TALL | spec | L/R dims imply line centres 220.5–230 varying line to line – treated as rounding, centred. |
| R2-10 | GIVE_WAY_TO_PEDESTRIANS_WHITE_SQUARE | spec | — |
| R2-11 | TWO_WAY_TRAFFIC_WHITE_TALL | needs-symbol r2-11_arrow_up r2-11_arrow_down | Two ids instead of `flip:"v"` (see generator note 2). |
| R2-14(L) (both hands) | R2-14 LEFT_TURN_ONLY_WHITE_TALL (hands L,R) | needs-symbol r2-14_curve_arrow_left | ONLY 66\|478\|56 (5 right) – centred. |
| R2-15 | U_TURN_PERMITTED_WHITE_TALL | spec | — |
| R2-17 | ONE_WAY_UP_ARROW_WHITE_TALL | needs-symbol r2-17_arrow_up | Grid inset labels the arrow height "800" and head 240 wide vs 315/208 on the sign – inconsistent; sign dims used. |
| R2-19 | LEFT_LANE_MUST_EXIT_WHITE_TALL | spec | — |
| R2-20 | LEFT_TURN_ON_RED_PERMITTED_WHITE_TALL | spec | — |
| R2-21 | RIGHT_TURN_FROM_LEFT_ONLY_WHITE_TALL | needs-symbol r2-21_hook_turn_panel | Whole black symbol panel (upper 715, inside the 15 white edge) is one symbol. Drawing's "25\|750\|25" white-area width contradicts the 15+30 edge/border; text pitches 125 = 80 E + 45. |
| R2-22 | NO_HOOK_TURN_BY_BICYCLES_WHITE_SQUARE | spec | Right-hand dims are baseline-to-baseline (250/150/135/135) – decoded to tops 100/310/445/580 (sums to 750). |
| R3-1 | PEDESTRIAN_CROSSING_YELLOWGREEN_ROUND | needs-symbol r3-1_pedestrian_legs | Only the legs' top (176 above centre) and top corners (100 L / 67 R) are dimensioned; bbox extents 456×332 counted from the 30 grid. |
| R3-2 | SAFETY_ZONE_YELLOWGREEN_ROUND | spec | Rim dims "20" (top) and "10" (bottom): read as 10 yellow-green edge + 20 black ring (alternative reading: ring 10 inside a 10 edge). Text block sits 6 low (SAFETY baseline 6 above centre). |
| R3-3 | CHILDREN_CROSSING_ORANGE_SQUARE | spec | Flag: no corner radius, no border. |
| R3-4 | CHILDREN_CROSSING_{speed}_WHEN_LIGHTS_FLASHING (vary 25/40/60) | spec | Section lines at 400/1200 treated as panel joins (not drawn). Vary values chosen (drawing shows 40 "Varies"). Kept in root folder (not a speed sign). |
| R3-5 (R and L) | R3-5 PEDESTRIAN_TRAFFIC_LIGHT_ARROWS_WHITE (hands L,R, drawn R) | needs-symbol r3-5_arrow_up r3-5_arrow_diag_up_right r3-5_arrow_right r3-5_pedestrian | Edge 1 / border 3 read from the 1 and 3 callouts. One id per arrow orientation (generator note 2). |
| R4-1 | {speed}_SPEED_SIGN | existing | — |
| R4-3 | ROADWORK_WHITE | existing | — |
| R4-4 | {speed}_SHARED_ZONE_WHITE_TALL (vary 10) | needs-symbol r4-4_shared_zone_symbols | Numerals dashed in the drawing → vary; only 10 used. Pedestrian+car placed as one group (individual positions not dimensioned). |
| R4-5 | END_SHARED_ZONE_WHITE_TALL | needs-symbol r4-4_shared_zone_symbols | — |
| R4-8 | SCHOOL_ZONE_WHITE | existing | — |
| R4-9 | END_SCHOOL_ZONE_WHITE_SQUARE | spec | — |
| R4-10 | {speed}_AREA_SPEED_SIGN | existing | — |
| R4-11 | END_{speed}_AREA_SPEED_SIGN (Speed Signs/End) | spec | — |
| R4-12 | END_{speed}_SPEED_SIGN | existing | — |
| R4-13 | END_{speed}_AREA_PLATE_SPEED_SIGN (Speed Signs/End) | spec | The "80 D" (left) is the numerals and "55 D" (right) is END/AREA – the width check confirms (80 D would give 191/272 vs 131/187). Band 15 from the "15" callout / grid. |
| R4-14 | YOU_ARE_WITHIN_A_{speed}_AREA_SPEED_SIGN (Speed Signs/Area) | spec | 80/80 dims are top-to-baseline. Word gaps not given: derived from the line widths (330 − 152 − 147 = 31; 338 − 240 − 51 = 47). |
| R5-10 | DISABLED_PARKING_ONLY_WHITE_LONG | needs-symbol r5-10_wheelchair r5_double_arrow | Symbol file must carry its own blue square + white figure fills. |
| R5-14 | P10_MINUTE_12NOON_MIDNIGHT_GREEN_TALL | needs-symbol r5_double_arrow | Drawing labels "12" 35 E / "MID" 33 C and NOON 12 E / NIGHT 14 E – all four confirmed by the width check. Dash thickness not dimensioned (font hyphen stroke used, see generator note 1). |
| R5-16 | HALF_P_10AM_430PM_MON_SAT_GREEN_TALL | needs-symbol r5_half_fraction r5_arrow_left | ½ fraction: numerals dimensioned but the slash is not → whole fraction is a symbol. PM width not given. |
| R5-17 (R5-17 + R5-40) | 1HALF_P_AMBULANCES_EXCEPTED_LONG | needs-symbol r5_half_fraction r5_arrow_left r5-40_no_parking_140 r5_arrow_right | One spec for the two-panel drawing. 9AM–9PM inset chains to 169 vs the stated 183 (PM right-aligned at the block end). Divider "red or black" (5 wide) drawn red. AMBULANCES/EXCEPTED have only "195 MAX", no ink width. |
| R5-1_R5-35_Example_1 | 1P_9AM_12NOON_SAT_NO_STANDING_LONG | needs-symbol r5_arrow_left r5-35_no_standing_140 r5_arrow_right | Fully dimensioned example → transcribed. |
| R5-1_R5-35_Example_2 | — | skipped: example assembly, not fully dimensioned | 9AM–5.30PM / METER sub-dims absent ("195 MAX"). |
| R5-1_R5-35_Example_3 | — | skipped: example assembly, not fully dimensioned | No horizontal text dims. |
| R5-35 | NO_STANDING_WHITE_TALL | needs-symbol r5-35_no_standing_140 r5_arrow_right | Corner radius not stated on this drawing – R20 taken from R5-36. Roundel (annulus + S 95 E + 65° slash + halo) is a symbol because the halo is undimensioned. |
| R5-36 | NO_STANDING_830_930AM_3_4PM_SCHOOL_DAYS | needs-symbol r5-35_no_standing_140 r5_arrow_right | HORIZONTAL LAYOUT OF THE TIME LINES NOT DIMENSIONED – x positions borrowed from the R5-46_R5-2 "6.30–9.30AM" inset pattern; SCHOOL DAYS width not given. |
| R5-36_R5-23 | NO_STANDING_4_6PM_LOADING_ZONE_9AM_4PM | needs-symbol r5-35_no_standing_140 r5_arrow_left | Fully dimensioned two-panel drawing → transcribed (LOADING ZONE red sub-panel via `panel`). |
| R5-39 | TOW_AWAY_AREA_WHITE_LONG | needs-symbol r5-39_tow_truck | — |
| R5-46_R5-2_Example_1 | — | skipped: example assembly, not fully dimensioned | Time blocks placed only as "195 MAX" while the insets chain to 200; upper MON–FRI position not given. |
| R5-46_R5-2_Example_2 | — | skipped: example assembly, not fully dimensioned | No horizontal text dims. |
| R5-50 | CLEARWAY_WHITE_TALL | needs-symbol r5_clearway_c | Variable 500×320 legend panel left empty; the drawing's fully-dimensioned "AT ALL TIMES" alternative is recorded in `notes`. |
| R5-51 | END_CLEARWAY_WHITE_SQUARE | needs-symbol r5_clearway_c | — |
| R5-58(L-R) | R5-58 EMERGENCY_STOPPING_LANE_ONLY_WHITE_LONG (hands L,R) | needs-symbol r5-58_arrow_down_left | Text right-aligned (L) with `mirror:true` so (R) is left-aligned. |
| R5-60 | — | skipped: variable-name area parking sign | "BRISBANE" / width "Varies"; rotated drawing; name-line dims chained (296+491+115+765+333 = 2000) contradicting the "=" centring marks; time-line sub-dims unreadable. |
| R5-61 | PARKING_AREA_P_TICKET_630AM_7PM_NOV_MAR | spec | Row 65\|184\|21\|64\|20\|181\|65 is EXCEPT AS SIGNED (width check), so NOV–MAR only has 65\|470\|65 and its DASH LENGTH IS NOT DIMENSIONED (drawn 37 like the line above). Positions inside the 162/170 blocks not sub-dimensioned (aligned to block edges). |
| R5-62 | YOU_ARE_WITHIN_A_PARKING_AREA_2P_WHITE_TALL | spec | Time lines have overall widths only (282/182): AM, dashes and 6/12 groups placed by the R5-16 convention – NOT DIMENSIONED. EXCEPT/SIGNED come out 2.6 % over the drawing (124/122 vs 121/119). |
| R5-63 | END_2P_AREA_WHITE_SQUARE | spec | Bottom "543" is the 2P again; AREA has no width dim (at 150 E it is 612). |
| R5-64 | AREA_PARKING_CONTROL_AHEAD_WHITE_SQUARE | spec | — |
| R5-65 | PARK_IN_BAYS_ONLY_WHITE_LONG | spec | — |
| R5-70 | NO_STANDING_AREA_7AM_630PM_MON_FRI_WHITE_LONG | needs-symbol r5-70_no_standing_500 | Fully decoded (the "35" over the top row is a segment: 7 130 + 35 + AM 96). SAT position from the 215\|510\|550\|185\|540 row. PM width not given. |
| R5-71 | NO_STANDING_AREA_9AM_630PM_WHITE_TALL | needs-symbol r5-71_no_standing_360 | AM height not labelled (taken as 25 E like PM); "57" read as the width of the 30. |
| R5-72 | YOU_ARE_WITHIN_A_NO_STANDING_AREA_WHITE_TALL | needs-symbol r5-72_no_standing_290 | AM height taken as 20 E like PM; "46" = width of the 30. |
| R5-73 | END_NO_STANDING_AREA_WHITE_TALL | needs-symbol r5-72_no_standing_290 | Same roundel as R5-72. |
| R5-80 | NO_PARKING_AREA_7AM_630PM_MON_FRI_WHITE_LONG | needs-symbol r5-80_no_parking_500 | Same layout as R5-70. |
| R5-81 | NO_PARKING_AREA_9AM_630PM_WHITE_TALL | needs-symbol r5-81_no_parking_360 | Same layout as R5-71. |
| R5-82 | YOU_ARE_WITHIN_A_NO_PARKING_AREA_WHITE_TALL | needs-symbol r5-82_no_parking_290 | Same layout as R5-72. |
| R5-83 | END_NO_PARKING_AREA_WHITE_TALL | needs-symbol r5-82_no_parking_290 | Same layout as R5-73. |
| R5-85(L-R) | R5-85 EMERGENCY_STOPPING_BAY_WHITE_LONG (hands L,R) | needs-symbol r5-85_arrow_up_right r5-85_telephone | Telephone shown only as a dashed 225 box (no artwork in this drawing). Text left-aligned (L) with `mirror:true`. |

## Counts (66 drawings)
* existing (untouched): 8
* spec (generated, width-checked): 18 drawings / 19 files -> R2-9(L)+(R) (one PNG), R2-10, R2-15, R2-19, R2-20, R2-22, R3-2, R3-3, R3-4, R4-9, R4-11, R4-13, R4-14, R5-61, R5-62, R5-63, R5-64, R5-65
* needs-symbol: 35 drawings / 36 files (R2-3 is two files) -> R1-3, R2-2, R2-3, R2-5, R2-6, R2-7, R2-11, R2-14, R2-17, R2-21, R3-1, R3-5, R4-4, R4-5, R5-10, R5-14, R5-16, R5-17, R5-1_R5-35_Example_1, R5-35, R5-36, R5-36_R5-23, R5-39, R5-50, R5-51, R5-58, R5-70, R5-71, R5-72, R5-73, R5-80, R5-81, R5-82, R5-83, R5-85 -- 35 distinct symbol ids to trace
* skipped: 5 (R5-1_R5-35_Example_2, _Example_3, R5-46_R5-2_Example_1, _Example_2, R5-60)

Width mismatches remaining after re-reading: R5-62 EXCEPT/SIGNED (2.6 % over, explained in notes); R2-4 is pre-existing.

## Generator features needed / quirks found (not worked around by guessing)
1. **Dashes in time legends** ("9AM – 12NOON", "MON – FRI"): the drawings give the dash length and sometimes its thickness/position (R5-61: 45|10|45, R5-71: 36|8|36, R5-72: 27|6|27), but usually only the length. Drawn as `rect`s; where the thickness is not dimensioned it is taken from the FHWA hyphen stroke of the same series/height (E 17.2 %, D 15.6 %, C 14 % of cap height) centred on the cap height – a dedicated `dash` element (length from the drawing, stroke from the font) would make this explicit. The font hyphen itself is 0.5 H wide, never the drawn length.
2. **Symbol `flip`/`rotate`**: `flip:"h"/"v"` mirrors about the panel centre, not the symbol bbox (bbox x becomes W−x−w), and `rotate` is applied after fitting to the bbox, so a rotated arrow needs the unrotated bbox. To avoid both, separate ids were used for each orientation (r2-11_arrow_up/down, r3-5_arrow_up/right/diag); `flip:"h"` was used only where the bbox is symmetric (R2-3(R)).
3. **Multi-word lines with unequal gaps** (R5-61 EXCEPT AS SIGNED 21/20; R5-70/R5-80 inter-word gaps): `gap` is a single value; 20.5 was used for 21/20.
4. **Superscript/stacked small text** (30 C over PM 15 E, 12 over NOON): handled with separate text elements top-/bottom-aligned by the stated heights and gaps – works, but every AM/PM/30 needs its own element and its width is rarely dimensioned (no `expect`).
5. **Symbols with their own colours** (R5-10 blue square + white wheelchair, r5_clearway_c red + white C, the roundels red/black/white, R2-21 black panel + white cut-outs): the symbol SVG must carry explicit fills; the element `colour` only applies to `currentColor` paths.
6. **Sub-panel with border** (R2-21): the black symbol panel merges with the sign border; no element type draws "panel + its own border", so the whole upper area is one symbol.
7. **Variable legend panel** (R5-50): no way to express "optional panel with alternative legends"; base sign generated empty, alternatives recorded in notes.

## Drawing inconsistencies found
R2-2 vertical stack 580 ≠ 600; R2-3 text off-centre by 6–7.5 (consistent on both hands, transcribed); R2-17 grid "800"/240 vs sign 315/208; R2-21 white-area 25|750|25 vs 15+30 border; R3-2 rim 20/10 ambiguous; R4-13 numerals/text heights are swapped between the two columns relative to their positions (resolved by the width check); R5-17 9AM–9PM chain 169 vs 183; R5-35 no corner radius; R5-36 and R5-62 time lines without horizontal dims; R5-61 NOV–MAR dash length missing (and its row of dims actually belongs to EXCEPT AS SIGNED); R5-63 AREA width missing; R5-71/R5-72 AM height not labelled; R5-60 name-line dims chained vs "=" marks.
