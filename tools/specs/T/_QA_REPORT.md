# T1–T8 QA report (AS 1743-2023 temporary signs)

Checked every generated sign against its drawing (contact sheets, symbol crops, width checks, lint). One line per spec.
Remaining lint flags (T5-1, T8-2(L), T8-2(R)) are arrow + word layouts placed from the drawing's chain and are correct.

- T1-1 — OK
- T1-2 — OK
- T1-3-1 — OK
- T1-3-2 — OK
- T1-4 — OK
- T1-5 — OK (worker symbol traced clean, box 180/60/550x470 as drawn)
- T1-6 — OK
- T1-10 — OK
- T1-16 — OK (numeral in a 160 slot, line centred; km at cap 160 per its 330 width, drawing's "135 Emod" label does not fit — noted in spec)
- T1-18 — ISSUE: STOP 120 E computes 443 vs drawing 430 (no series/height matches 430; drawing figure inconsistent with AS 1744 spacing). Drawn at 120 E as labelled.
- T1-19 — OK (cattle/sheep symbol traced clean)
- T1-21 — OK
- T1-22 — OK
- T1-23 — OK
- T1-24 — OK (runs, centred for every value)
- T1-25 — OK
- T1-27 — OK
- T1-28 — OK (km at cap 150 per its 309 width; "130 Emod" label does not fit — noted)
- T1-29 — OK (runs, centred for every value)
- T1-30 — OK (traffic-signal symbol traced clean, 332x500)
- T1-31 — OK (WORK drawn in E per its 658 width; labelled "160 D" — noted)
- T1-32 — OK
- T1-33 — OK
- T1-34 — OK (traffic-controller symbol traced clean)
- T1-35 — OK (red letters / black border / white ground as drawn; caption describes another sign — noted)
- T2-4 — OK
- T2-6-1 — OK (bar/stem rects, arrow symbol traced clean)
- T2-6-2 — OK (reuses the T2-6-1 arrow)
- T2-13 — OK
- T2-16 — OK
- T2-17 — OK
- T2-23 — OK
- T2-24 — FIXED (the down arrow reused the up-arrow id with flip "v", so the tracer traced the id twice and the second trace (the down arrow) overwrote the up arrow — both arrows rendered inverted; the down arrow now has its own id `t2-24_arrow_down` traced from its own box)
- T2-25 — OK (truck symbol traced clean)
- T3-3 — OK (slippery-car symbol traced clean)
- T3-6 — OK
- T3-7 — OK
- T3-9 — OK (loose-stones symbol traced clean)
- T3-11 — ISSUE: all five stated widths are 3.5–4 % over AS 1744 spacing at the labelled 150 D / 150 E (they fit a cap height of ~156). Kept at 150 as labelled; drawing inconsistency.
- T3-12 — OK
- T3-13 — OK
- T3-14 — OK
- T3-15 — ISSUE: FIXED the swapped expects (ROUGH 346 / SURFACE 446 — the drawing's outer chain 77|446|77 is SURFACE, inner 127|346|127 is ROUGH); remaining: the bicycle's height is not dimensioned (only its 220 width and 50 bottom margin), taken from the 30 grid as 146 (trace gives 147).
- T3-16-1 — OK
- T3-16-2 — FIXED (50 + km/h converted from two left-aligned elements to one centred run line with the 100 gap; chain 72|239|100|418|71)
- T4-3 — OK
- T4-5 — OK
- T4-6 — ISSUE: drawing specifies a fluorescent yellow ground (drawn paler than standard yellow); the generator palette has no fluorescent yellow, so standard yellow is used.
- T4-7 — ISSUE: FIXED lines 2 and 4 (SWITCH OFF RADIO, & MOBILE PHONES) from left-aligned words at drawn x to centred word groups with per-pair gaps (79/77 and 65/76); remaining: "&" dimensioned 87 wide but the Series C ampersand at 100 is 100 wide (D would be 89) — drawing/font disagreement, kept in C as labelled.
- T5-1 (L,R) — OK (one drawing, both hands; (R) verified as the exact mirror; caption says white ground but the drawing is yellow — drawn as shown, noted)
- T5-1 — ISSUE: horizontal chain 116|687|106|160|121 sums to 1190 on a 1200 sign (drawing inconsistency); placed from the left, leaving 131 right instead of 121.
- T5-4 — OK
- T5-5 — OK
- T5-6 — OK (arrow symbol traced clean)
- T5-7 — ISSUE: drawing gives the height as a range 1140–1200 with 100–130 end bands and no "Illust." size; drawn at 1200 with 130 bands.
- T6-4 — OK
- T6-5 — FIXED (DO NOT OVERTAKE converted from three left-aligned elements to one centred word group with gaps 60/52; size-table "Illust." 1000x350 vs dimensioned 1200x500 and PILOT VEHICLE C-label vs D-widths remain noted)
- T6-6 — OK
- T7-1 — ISSUE: SLOW 135 C computes 382 vs drawing 370 (130 C would give 368); drawing inconsistency, kept at 135 C as labelled.
- T8-1 — OK
- T8-2(L) — OK
- T8-2(R) — FIXED (the spec reused the (L) arrow id with source T8-2(L) and flip "h"; because both codes share the base code T8-2 the tracer re-traced the id from the (L) drawing using the (R) box, producing a 130x105 fragment that overwrote the (L) arrow; now its own id `t8-2_arrow_right` traced from the (R) drawing)
- T8-3 — OK
- T8-4 — OK
- T8-5 — FIXED (TWO - WAY TRAFFIC converted from four hand-positioned elements to one centred run line: gaps 22|21 hyphen|22 inside the 65 zone, 45 before TRAFFIC; 87 margins as drawn)

## Counts
OK 52 · FIXED 5 (T2-24, T3-16-2, T6-5, T8-2(R), T8-5) · ISSUE 8 (T1-18, T3-11, T3-15, T4-6, T4-7, T5-1, T5-7, T7-1)
