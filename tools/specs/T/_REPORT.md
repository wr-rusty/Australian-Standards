# T1–T8 spec report (AS 1743-2023, temporary/roadwork signs)

65 drawings. Specs written for all; 5 (T1-1, T1-6, T1-10, T1-18, T2-4) pre-existed and were left as found.
Generator: `signgen.py tools/specs/T/*.json` -> 64 files written; remaining width mismatches are all explained in the spec notes (listed under Flags). "BLOCKED: symbol ... missing" is expected for the needs-symbol rows.

Status key: spec = generates clean; needs-symbol <ids> = spec complete, waiting on traced symbol artwork in tools/symbols/; skipped = not a sign.

| Code | Name | Status | Flags |
|---|---|---|---|
| T1-1 | ROADWORK_AHEAD_YELLOW_WIDE | spec (pre-existing) | |
| T1-2 | BRIDGEWORK_AHEAD_YELLOW_WIDE | spec | |
| T1-3-1 | ROAD_PLANT_AHEAD_YELLOW_LONG | spec | |
| T1-3-2 | ROAD_PLANT_AHEAD_YELLOW_WIDE | spec | |
| T1-4 | GRADER_AHEAD_YELLOW_LONG | spec | |
| T1-5 | WORKER_ORANGE_LONG | needs-symbol t1-5_worker | |
| T1-6 | DETOUR_AHEAD_YELLOW_LONG | spec (pre-existing) | |
| T1-10 | TRAFFIC_HAZARD_YELLOW_LONG | spec (pre-existing) | |
| T1-16 | ROADWORK_{km}_KM_AHEAD_YELLOW_WIDE | spec | Numeral varies ({km} 1-5). Drawing labels "km" as "135 Emod" but its stated width 330 matches Emod at capital height 160 (135 would give 280); drawn at 160. Second line has per-word series and unequal gaps (80/129) — generator cannot centre such a line as a whole, so words are placed at fixed x from the drawn "1"; other numerals are not re-centred. |
| T1-18 | PREPARE_TO_STOP | spec (pre-existing) | Pre-existing note: STOP 120 E computes 443 vs drawing 430. |
| T1-19 | STOCK_AHEAD_YELLOW_LONG | needs-symbol t1-19_cattle_sheep | |
| T1-21 | NEW_ROUNDABOUT_YELLOW_WIDE | spec | |
| T1-22 | CHANGED_SIGNALS_YELLOW_LONG | spec | |
| T1-23 | CHANGED_TRAFFIC_CONDITIONS_YELLOW_LONG | spec | |
| T1-24 | ROADWORK_NEXT_{km}_KM_YELLOW_WIDE | spec | Numeral varies ({km} 1-5). "km" is Emod at capital height 135 (width 279 matches). Mixed-series line with unequal gaps: positions fixed for the drawn "2"; not re-centred for other numerals (generator feature missing: one centred line with per-word series/height and per-gap values). |
| T1-25 | ROADWORK_ON_SIDE_ROAD_YELLOW_WIDE | spec | |
| T1-27 | ROAD_PLANT_ON_SIDE_ROAD_YELLOW_WIDE | spec | |
| T1-28 | NEXT_{km}_KM_YELLOW_SQUARE | spec | Numeral varies ({km} 1-5). "km" labelled "130 Emod" but width 309 matches Emod at capital height 150; drawn at 150. Same fixed-position limitation as T1-24. |
| T1-29 | BRIDGEWORK_{km}_KM_AHEAD_YELLOW_WIDE | spec | Numeral varies ({km} 1-5). "km" Emod at 135 (279 matches). Same fixed-position limitation as T1-24. |
| T1-30 | TRAFFIC_SIGNALS_YELLOW_LONG | needs-symbol t1-30_traffic_signals | Symbol is fully dimensioned in the inset (could be traced exactly). No horizontal position on the sign; centred. |
| T1-31 | ROAD_WORK_AHEAD_YELLOW_TALL | spec | Drawing labels WORK "160 D" but its width 658 is Series E (D = 560); drawn in E. |
| T1-32 | SIDE_ROAD_CLOSED_YELLOW_WIDE | spec | |
| T1-33 | CHANGED_INTERSECTION_YELLOW_WIDE | spec | |
| T1-34 | TRAFFIC_CONTROLLER_ORANGE_LONG | needs-symbol t1-34_traffic_controller | |
| T1-35 | STOP_HERE_WHEN_DIRECTED_WHITE_LONG | spec | Drawing caption ("Black symbol and border on retroreflective fluorescent orange ground") is a copy-paste error; drawing shows red letters, black border, white ground — drawn as shown. STOP HERE only dimensioned as a whole (756): gap 62.5 derived. |
| T2-4 | ROAD_CLOSED_WHITE_WIDE_SKINNY | spec (pre-existing) | |
| T2-6-1 | LANE_STATUS_1_CLOSED_1_OPEN_YELLOW_LONG | needs-symbol t2-6_up_arrow | Bar and stem are rects. Arrow head barb geometry (64/12 with R23) not unambiguous for a polygon. |
| T2-6-2 | LANE_STATUS_1_CLOSED_2_OPEN_YELLOW_LONG | needs-symbol t2-6_up_arrow | Reuses T2-6-1 arrow (inset grid here is 90). |
| T2-13 | WATER_OVER_ROAD_YELLOW_LONG | spec | |
| T2-16 | END_ROADWORK_YELLOW_WIDE | spec | |
| T2-17 | END_ROAD_WORK_YELLOW_TALL | spec | |
| T2-23 | END_DETOUR_YELLOW_LONG | spec | |
| T2-24 | TWO_WAY_ARROWS_YELLOW_LONG | needs-symbol t2-24_arrow | Down arrow is the same symbol with flip "v". Shaft tapered 50/66 so not a polygon. |
| T2-25 | TRUCK_YELLOW_LONG | needs-symbol t2-25_truck | Fully dimensioned inset. |
| T3-3 | SLIPPERY_YELLOW_LONG | needs-symbol t3-3_slippery_car | |
| T3-6 | SOFT_EDGES_YELLOW_LONG | spec | |
| T3-7 | ROUGH_SURFACE_YELLOW_LONG | spec | |
| T3-9 | LOOSE_STONES_YELLOW_LONG | needs-symbol t3-9_loose_stones | |
| T3-11 | NEW_WORK_NO_LINES_MARKED_YELLOW_LONG | spec | All five stated widths are 3.5-4 % wider than AS 1744 spacing at the stated 150 height (they all match a height of ~156). Kept at 150; generator reports the mismatch. |
| T3-12 | NO_LINES_DO_NOT_OVERTAKE_UNLESS_SAFE_YELLOW_LONG | spec | |
| T3-13 | GRAVEL_ROAD_YELLOW_LONG | spec | |
| T3-14 | LOOSE_SURFACE_YELLOW_LONG | spec | |
| T3-15 | ROUGH_SURFACE_BICYCLE_YELLOW_LONG | needs-symbol t3-15_bicycle | Bicycle height not stated; measured from the 30 grid (~146). |
| T3-16-1 | 50_KMH_YELLOW_SQUARE | spec | Numerals drawn solid (not dashed), so fixed at 50. |
| T3-16-2 | 50_KMH_YELLOW_LONG | spec | As above; numerals 150 D and km/h 100 Emod placed at drawn x. |
| T4-3 | END_BLASTING_AREA_RED_WIDE | spec | T4-3AA illustrated; no border. |
| T4-5 | POWER_LINE_WORKS_IN_PROGRESS_YELLOW_LONG | spec | |
| T4-6 | SMOKE_HAZARD_YELLOW_LONG | spec | Fluorescent yellow ground drawn with standard yellow. |
| T4-7 | BLASTING_AREA_SWITCH_OFF_RADIO_RED_LONG | spec | Lines 2 and 4 have unequal gaps; words placed at drawn x. "&" dimensioned 87 wide, Series C font ampersand at 100 is 100 wide (mismatch reported). |
| T5-1 (L,R) | DETOUR_ARROW_YELLOW_LONG_SKINNY | needs-symbol t5-1_arrow_left | File `T5-1(L,R).json`, code T5-1, hands L/R, drawn_hand L (text uses mirror:true). Drawn yellow as shown; caption says "white retroreflective ground" — contradiction. Same code as T5-1.png (straight-ahead) — two specs share code "T5-1" (outputs differ by (L)/(R) suffix). |
| T5-1 | DETOUR_ARROW_UP_YELLOW_LONG_SKINNY | needs-symbol t5-1_arrow_up | Horizontal chain 116+687+106+160+121 = 1190, not 1200 (drawing inconsistency); arrow placed from the left chain, leaving 131 on the right. Arrow is the T5-1(L,R) arrow rotated. |
| T5-4 | CHEVRON_ALIGNMENT_3_YELLOW_WIDE | spec | Three black 45-degree bands as polygons; geometry confirmed against the drawing's pixels. Single hand drawn (points right). |
| T5-5 | CHEVRON_ALIGNMENT_1_YELLOW_SQUARE | spec | One black band as a polygon. |
| T5-6 | LEFT_ARROW_YELLOW_SQUARE | needs-symbol t5-6_arrow_left | |
| T5-7 | CHEVRON_MARKER_YELLOW_TALL | spec | Height given as 1140-1200 (end bands 100-130) with no "Illust." size; drawn at 1200 with 130 bands. Chevron band geometry (dims 100/50/100) resolved against the drawing's pixels. No border. |
| T6-4 | SCHOOL_BUS_YELLOW_WIDE_SKINNY | spec | "Variable size" note; drawn at 1200x230 as dimensioned. No border. |
| T6-5 | PILOT_VEHICLE_DO_NOT_OVERTAKE_YELLOW_WHITE_LONG | spec | Drawing dimensioned 1200x500 (= T6-5B) but table marks T6-5A 1000x350 "Illust." — drawn at 1200x500. PILOT VEHICLE labelled "100 C" but widths 344/526 are Series D (drawn in D). Two-colour ground: yellow upper half is a hand `path` with R20 inner corners (no generator feature for split grounds). Unequal gaps on the lower line; words placed at drawn x. |
| T6-6 | PILOT_VEHICLE_IN_USE_YELLOW_LONG | spec | |
| T7-1 | SLOW_YELLOW_ROUND | spec | Circle 450 dia, 12 border. SLOW 135 C computes 382 vs drawing 370 (3 %) — drawing figure inconsistent with AS 1744 spacing. |
| T8-1 | PEDESTRIANS_WATCH_YOUR_STEP_YELLOW_LONG | spec | |
| T8-2(L) | PEDESTRIANS_ARROW_LEFT_YELLOW_LONG_SKINNY | needs-symbol t8-2_arrow_left | Separate PNG per hand -> separate spec. |
| T8-2(R) | PEDESTRIANS_ARROW_RIGHT_YELLOW_LONG_SKINNY | needs-symbol t8-2_arrow_left | Uses the (L) arrow with flip "h". |
| T8-3 | USE_OTHER_FOOTPATH_YELLOW_LONG | spec | |
| T8-4 | FOOTPATH_CLOSED_WHITE_LONG | spec | |
| T8-5 | LOOK_BOTH_WAYS_TWO_WAY_TRAFFIC_YELLOW_LONG | needs-symbol t2-24_arrow | Arrows are "T2-24 @70%" (reused id, rotated +/-90 with an unrotated bbox). Drawing gives 265 for the arrow length vs 263 (70 % of 376). "TWO-WAY": font spacing would give 406 vs the drawn 373 (145 | 65 hyphen zone | 163), so TWO, "-", WAY, TRAFFIC are placed at drawn x. |

## Counts
* spec: 48 (incl. 5 pre-existing)
* needs-symbol: 17 (T1-5, T1-19, T1-30, T1-34, T2-6-1, T2-6-2, T2-24, T2-25, T3-3, T3-9, T3-15, T5-1(L,R), T5-1, T5-6, T8-2(L), T8-2(R), T8-5)
  — 17 spec files / 18 generator outputs (T5-1 L+R); symbol ids needed: t1-5_worker, t1-19_cattle_sheep, t1-30_traffic_signals, t1-34_traffic_controller, t2-6_up_arrow, t2-24_arrow, t2-25_truck, t3-3_slippery_car, t3-9_loose_stones, t3-15_bicycle, t5-1_arrow_left, t5-1_arrow_up, t5-6_arrow_left, t8-2_arrow_left (14 ids).
* skipped: 0

## Flags
Drawing inconsistencies
* T1-16 / T1-28: "km" height annotation (135 Emod / 130 Emod) does not match the stated ink width, which fits Emod at the line's capital height (160 / 150). T1-24 / T1-29 label 135 Emod and their widths do fit 135.
* T1-31: WORK labelled 160 D, width is 160 E.
* T1-35: caption describes a different sign (orange symbol sign).
* T3-11: all widths ~4 % over AS 1744 at 150 (fit ~156).
* T4-7: "&" 87 vs font 100.
* T5-1: horizontal chain sums to 1190 on a 1200 sign.
* T5-1(L,R): caption says white ground, drawing is yellow.
* T6-5: dimensioned at 1200x500 but table says 1000x350 is illustrated; PILOT VEHICLE labelled C, widths are D.
* T7-1: SLOW 370 vs 382 computed.
* T8-5: arrow length 265 vs 263 (70 % of T2-24).
* T5-7: no illustrated size (1140-1200 range).

Generator features needed (not worked around by guessing)
* One centred line containing words of different series/height and different inter-word gaps (T1-16, T1-24, T1-28, T1-29 "NEXT [n] km" style lines, T8-5 "TWO-WAY TRAFFIC", T4-7, T6-5). Worked around with left/cx-positioned elements at the drawn x, which is exact for the drawn numeral but leaves varying-numeral lines un-centred for other values.
* Split (two-colour) ground panels (T6-5): done with a hand `path`.
* Symbol placement bottom-aligned when only width and bottom margin are given (T3-15): height taken from the grid instead.

Other
* Two specs share code "T5-1" (T5-1.json straight-ahead; T5-1(L,R).json with hands) because both PNGs carry that code; manifest rows are T5-1, T5-1(L), T5-1(R).
* Not touched by this work but visible in `git status`: `.gitignore` has an uncommitted `.venv/` line and `tools/` / `PLAN.md` are untracked.
