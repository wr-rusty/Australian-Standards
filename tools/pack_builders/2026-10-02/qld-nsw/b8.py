from qb import *
dark = lambda h: h != "-" and all(int(h[i:i + 2], 16) < 0x60 for i in (1, 3, 5))
def within(vc, ppx, W, box, pred=dark, maxw=None):
    k = (ppx[2] - ppx[0]) / W; out = []
    for f in fills(vc):
        m = [(f[2][0] - ppx[0]) / k, (f[2][1] - ppx[1]) / k, (f[2][2] - ppx[0]) / k, (f[2][3] - ppx[1]) / k]
        if pred(f[1]) and m[0] >= box[0] and m[2] <= box[2] and m[1] >= box[1] and m[3] <= box[3] and (maxw is None or m[2] - m[0] < maxw): out.append(f[0])
    return out
def distrun(drawing, ppx, W, top, h, val, x0, x1, mh):
    rr = runs(drawing, ppx, W, top + 0.3 * h, top + 0.7 * h, mingap=0.25 * h, x0=x0, x1=x1, ink=lambda p: not (p[0] > 200 and p[1] > 170))
    a = rr[0][0]; g = rr[-1][0] - rr[-2][1]
    return {"type": "text", "runs": [{"text": val, "series": "D", "height": h}, {"text": "m", "series": "Emod", "height": mh}], "gap": round(g, 1), "top": top, "align": "left", "x": round(a, 1)}, (a, rr[-1][1], g)
WB = dict(ground="white", edge={"colour": "white", "width": 20}, border={"colour": "black", "width": 40}, radius=200)
# ---------------- W7-Q02_1
vc, dr, ppx, W = "W7-Q02_1", "W7-Q02-1", [478.0, 253.8, 1229.1, 1338.8], 1800
s1 = within(vc, ppx, W, (60, 1061, 1740, 2059)); b1 = sym(vc, "qld_w7-q02-1_layout", [",".join(map(str, s1))]); m1 = mm(b1, ppx, W)
b2 = sym(vc, "qld_w7-q02_arrow_left", ["205"]); m2 = mm(b2, ppx, W)
d, dd = distrun(dr, ppx, W, 1400, 140, "12.5", 1185, 1730, 120)
els = [{"type": "rect", "x": 60, "y": 1040, "w": 1680, "h": 1040, "colour": "yellow"}, {"type": "rect", "x": 40, "y": 1020, "w": 1720, "h": 40, "colour": "black"}, {"type": "rect", "x": 40, "y": 2060, "w": 1720, "h": 40, "colour": "black"},
       line(dr, ppx, W, "KEEP TRACKS", "E", 160, 120, x0=70, x1=1730), line(dr, ppx, W, "CLEAR", "E", 160, 360, x0=70, x1=1730), line(dr, ppx, W, "WHEN LIGHTS", "D", 140, 620, x0=70, x1=1730), line(dr, ppx, W, "FLASHING", "D", 140, 830, x0=70, x1=1730),
       S("qld_w7-q02-1_layout", *m1), d, line(dr, ppx, W, "USE EMERGENCY", "D", 140, 2150, x0=100, x1=1700), S("qld_w7-q02_arrow_left", *m2), line(dr, ppx, W, "BAY", "D", 140, 2360, x0=1100, x1=1650, align="right")]
info = clean(els); print(info, m1, m2, dd)
syms = {**symentry("qld_w7-q02-1_layout", dr, "T-intersection, side road and railway with the stacking-distance arrow (the sheet's Symbol A, page 3), vector items of the sheet PDF"), **symentry("qld_w7-q02_arrow_left", dr, "left-pointing arrow 850 x 160 (detailed on page 2: head 143, R8, 45, 15, shaft 60), vector item 205")}
mk("W7-Q02-1", "KEEP_TRACKS_CLEAR_WHEN_LIGHTS_FLASHING_USE_EMERGENCY_BAY_WHITE_TALL", "KEEP TRACKS CLEAR WHEN LIGHTS FLASHING 12.5 m USE EMERGENCY BAY", [1800, 2600], els,
   f"Q-series sheet W7-Q02_1 warning sign 'USE EMERGENCY BAY' (2023, page 1 of 3; used with flashing light panel TC2092), fully dimensioned and drawn to scale, 1800 x 2600, R200, white edge 20 + black border 40 (the sheet's 20 / 60). Yellow band between two 40 black bars (bars at 1020-1060 and 2060-2100). Right chain 120 / 160E / 80 / 160E / 100 / 140D / 70 / 140D / 50 | 380 / 140D-90Em / 560 | 50 / 140D / 70 / 140D / 100 = 2600: cap tops 120 (KEEP TRACKS), 360 (CLEAR), 620 (WHEN LIGHTS), 830 (FLASHING), 1400 (distance), 2150 (USE EMERGENCY), 2360 (BAY). Lines centred as the sheet draws them (BAY ends at the drawn x); word gaps as drawn. The sheet sets its legend tighter than AS 1744 spacing (drawn left / right / gaps / drawn-to-AS 1744 width ratio per line: {info}); generated at the labelled sizes with AS 1744 (plus0) spacing. Layout symbol (Symbol A of page 3) and the left arrow are the sheet PDF's own vector artwork, placed as drawn: symbol {m1[2]} x {m1[3]} at x {m1[0]}, y {m1[1]}; arrow {m2[2]} x {m2[3]} at x {m2[0]}, y {m2[1]}. Distance '12.5 m': numerals 140 Series D, 'm' Series E modified lower case ('90Em' = the height of the lower-case m itself: cap height 120), from x {dd[0]:.0f} with {dd[2]:.0f} between them as drawn; 'insert appropriate distance in metres, e.g. 12.5' with no list: the example only is generated. Black on white and retroreflective yellow.",
   panel_px=ppx, drawing=dr, symbols=syms, **WB)
# ---------------- W7-Q02_2
vc, dr, ppx, W = "W7-Q02_2", "W7-Q02-2", [444.5, 185.4, 1199.0, 1275.2], 1800
s1 = within(vc, ppx, W, (60, 1261, 1740, 2059)); b1 = sym(vc, "qld_w7-q02-2_layout", [",".join(map(str, s1))]); m1 = mm(b1, ppx, W)
b2 = sym(vc, "qld_w7-q02-2_no_right_turn", ["135", "136:#ed1c24"]); m2 = mm(b2, ppx, W)
d, dd = distrun(dr, ppx, W, 1330, 140, "12.5", 400, 1200, 120)
els = [{"type": "rect", "x": 60, "y": 1240, "w": 1680, "h": 840, "colour": "yellow"}, {"type": "rect", "x": 40, "y": 1220, "w": 1720, "h": 40, "colour": "black"}, {"type": "rect", "x": 40, "y": 2060, "w": 1720, "h": 40, "colour": "black"},
       S("qld_w7-q02-2_no_right_turn", *m2), line(dr, ppx, W, "WHEN LIGHTS", "E", 140, 820, x0=70, x1=1730), line(dr, ppx, W, "FLASHING", "E", 140, 1030, x0=70, x1=1730),
       S("qld_w7-q02-2_layout", *m1), d, line(dr, ppx, W, "WAIT IN", "E", 140, 2150, x0=70, x1=1730), line(dr, ppx, W, "TURN LANE", "E", 140, 2360, x0=150, x1=1650)]
info = clean(els); print(info, m1, m2, dd)
syms = {**symentry("qld_w7-q02-2_layout", dr, "through road with a side road crossing a railway and the stacking-distance arrow (the sheet's Symbol B, page 3), vector items of the sheet PDF"), **symentry("qld_w7-q02-2_no_right_turn", dr, "no right turn roundel 600 diameter: black turn arrow under the red annulus and slash, vector items 135 and 136", ("black", "red"))}
mk("W7-Q02-2", "NO_RIGHT_TURN_WHEN_LIGHTS_FLASHING_WAIT_IN_TURN_LANE_WHITE_TALL", "(no right turn symbol) WHEN LIGHTS FLASHING 12.5 m WAIT IN TURN LANE", [1800, 2600], els,
   f"Q-series sheet W7-Q02_2 warning sign 'WAIT IN TURN LANE' (2023, page 2 of 3; used with flashing light panel TC2092), fully dimensioned and drawn to scale, 1800 x 2600, R200, white edge 20 + black border 40 (the sheet's 20 / 60). Yellow band between two 40 black bars (bars at 1220-1260 and 2060-2100). Right chain 120 / 600 (roundel) / 100 / 140E / 70 / 140E / 50 | 110 / 140D-90Em / 630 | 50 / 140E / 70 / 140E / 100 = 2600: roundel top 120 (600 diameter, centred), cap tops 820 (WHEN LIGHTS), 1030 (FLASHING), 1330 (distance), 2150 (WAIT IN), 2360 (TURN LANE). Lines centred as the sheet draws them; word gaps as drawn. The sheet sets its legend tighter than AS 1744 spacing (drawn left / right / gaps / drawn-to-AS 1744 width ratio per line: {info}); generated at the labelled sizes with AS 1744 (plus0) spacing. The no-right-turn roundel (dimensioned on page 3), the layout symbol (Symbol B of page 3) are the sheet PDF's own vector artwork, placed as drawn: roundel {m2[2]} x {m2[3]} at x {m2[0]}, y {m2[1]}; symbol {m1[2]} x {m1[3]} at x {m1[0]}, y {m1[1]}. Distance '12.5 m': numerals 140 Series D, 'm' Series E modified lower case ('90Em' = the height of the lower-case m itself: cap height 120), from x {dd[0]:.0f} with {dd[2]:.0f} between them as drawn; 'insert appropriate distance in metres, e.g. 12.5' with no list: the example only is generated. Black and red on white and retroreflective yellow.",
   panel_px=ppx, drawing=dr, symbols=syms, **WB)
skip("W7-Q02-3", "page 3 of 3 of W7-Q02: dimension details of Symbol A, Symbol B and the no-right-turn roundel used on pages 1 and 2 (built into W7-Q02-1 / W7-Q02-2), not a sign")
