from qb import *
dark = lambda h: h != "-" and all(int(h[i:i + 2], 16) < 0x60 for i in (1, 3, 5))
vc2 = "W7-Q03_2"
def grab(sid, box):
    it = [f[0] for f in fills(vc2) if dark(f[1]) and f[2][0] >= box[0] and f[2][2] <= box[2] and f[2][1] >= box[1] and f[2][3] <= box[3]]
    b = sym(vc2, sid, [",".join(map(str, it))]); print(sid, len(it), [round(v) for v in b], round((b[2] - b[0]) / (b[3] - b[1]), 3)); return b
grab("qld_w7-q03_symbol_a", (225, 265, 755, 720)); grab("qld_w7-q03_symbol_b", (225, 1105, 760, 1515))
vc, dr, ppx, W, H = "W7-Q03_1", "W7-Q03-1", [298.0, 354.3, 1404.8, 1155.7], 2900, 2100
def U(i, top=1690, r0=300): return f"M{i} {top}H{W - i}V{H - r0}A{r0 - i} {r0 - i} 0 0 1 {W - r0} {H - i}H{r0}A{r0 - i} {r0 - i} 0 0 1 {i} {H - r0}Z"
els = [{"type": "rect", "x": 60, "y": 650, "w": 2780, "h": 1000, "colour": "yellow"}, {"type": "rect", "x": 20, "y": 610, "w": 2860, "h": 40, "colour": "black"}, {"type": "rect", "x": 20, "y": 1650, "w": 2860, "h": 40, "colour": "black"},
       {"type": "path", "d": U(0), "colour": "red"}, {"type": "path", "d": U(20), "colour": "white"}, {"type": "path", "d": U(60), "colour": "red"},
       line(dr, ppx, W, "VEHICLE COMBINATIONS", "D", 160, 120, x0=150, x1=2750),
       {"type": "text", "runs": [{"text": "OVER", "series": "D", "height": 160}, {"text": "12.5", "series": "D", "height": 160}, {"text": "m", "series": "Emod", "height": 160}, {"text": "LENGTH", "series": "D", "height": 160}], "gap": [105, 76, 142], "top": 380, "cx": 1475},
       S("qld_w7-q03_symbol_{sym}", 175, 700, 1190, 900),
       line(dr, ppx, W, "LIMITED", "D", 160, 785, x0=1400, x1=2830), line(dr, ppx, W, "CLEARANCE", "D", 160, 1065, x0=1400, x1=2830), line(dr, ppx, W, "TO RAILS", "D", 160, 1345, x0=1400, x1=2830),
       line(dr, ppx, W, "NO RIGHT TURN", "E", 180, 1780, ink=WHITE, x0=150, x1=2750, colour="white")]
info = clean(els); print(info)
syms = {**symentry("qld_w7-q03_symbol_a", "W7-Q03-2", "Symbol A of page 2: T-intersection, side road and railway with the clearance arrow, 1190 x 900, vector items of the sheet PDF"), **symentry("qld_w7-q03_symbol_b", "W7-Q03-2", "Symbol B of page 2: through road with a side road crossing a railway, with the clearance arrow, 1190 x 900, vector items of the sheet PDF")}
mk("W7-Q03-1", "VEHICLE_COMBINATIONS_OVER_12.5_M_LIMITED_CLEARANCE_TO_RAILS_NO_RIGHT_TURN_SYMBOL_{symU}", "VEHICLE COMBINATIONS OVER 12.5 m LENGTH LIMITED CLEARANCE TO RAILS NO RIGHT TURN (symbol {symU})", [W, H], els,
   f"Q-series sheet W7-Q03_1 railway level crossing warning sign 'LIMITED CLEARANCE TO RAILS' (2023, page 1 of 2), fully dimensioned and drawn to scale, 2900 x 2100, R300. From the sheet's vectors: white edge 20 + black border 40 round the white top panel (to 610) and the yellow panel (650-1650), 40 black bars at 610-650 and 1650-1690; the bottom panel from 1690 is red with a white band (red edge 20, white 40, red ground), white legend. Right chain 120 / 160D / 100 / 160D-120Em / 70 | 40 | 135 / 160D / 120 / 160D / 120 / 160D / 145 | 40 | 90 / 180E / 140 = 2100: cap tops 120, 380, 785, 1065, 1345, 1780. "
   f"Second line 'OVER 12.5 m LENGTH': 160 Series D, 'm' Series E modified lower case ('120Em' = the height of the lower-case m itself: cap height 160), gaps 105 / 76 / 142 and centre x 1475 as drawn; '*insert appropriate distance in metres, e.g. 12.5' with no list: the example only is generated. The sheet's '**' box (1190 x 900 at x 175, y 700: the sheet's '1190' / '900') takes Symbol A or Symbol B of page 2: both generated as variants, each the sheet PDF's own vector artwork. Other lines as the sheet draws them (drawn left / right / gaps / drawn-to-AS 1744 width ratio: {info}); AS 1744 (plus0) spacing at the labelled sizes. Black, red and white on white and retroreflective yellow.",
   panel_px=ppx, drawing=dr, symbols=syms, vary={"keys": ["sym", "symU"], "values": [["a", "A"], ["b", "B"]]}, ground="white", edge={"colour": "white", "width": 20}, border={"colour": "black", "width": 40}, radius=300)
skip("W7-Q03-2", "page 2 of 2 of W7-Q03: Symbol A and Symbol B dimension details (the inserts of W7-Q03-1, generated there as variants), not a sign")
