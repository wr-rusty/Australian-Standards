from qb import *
import vec as _vec, json
p = page("W5-040-Q01_6"); ds = p.get_drawings(); K = 200 / 72
dias = sorted([(i, d["rect"]) for i, d in enumerate(ds) if d["type"] == "fs" and len(d["items"]) == 8], key=lambda t: (round(t[1].y0), t[1].x0))
KINDS = {1: "side impact", 2: "side impact", 3: "side impact", 4: "side impact", 5: "head on impact", 6: "rear end impact"}
symbols = {}
for n, (i0, r0) in enumerate(dias, 1):
    items = [i for i, d in enumerate(ds) if d["type"] == "f" and _vec.hexc(d.get("fill")) == "#373435" and d["rect"].x0 >= r0.x0 - 1 and d["rect"].x1 <= r0.x1 + 1 and d["rect"].y0 >= r0.y0 - 1 and d["rect"].y1 <= r0.y1 + 1]
    big = max(items, key=lambda i: ds[i]["rect"].width); items.remove(big)
    sym("W5-040-Q01_6", f"qld_w5-040-q01_crash_{n}", [",".join(map(str, items)), f"--vb={r0.x0 * K},{r0.y0 * K},{r0.x1 * K},{r0.y1 * K}"])
    symbols.update(symentry(f"qld_w5-040-q01_crash_{n}", "W5-040-Q01-6", f"crash scene option {n} ({KINDS[n]}) of page 6 of the sheet (vector items {items}); the symbol's viewBox is the whole drawn diamond so every option sits in the same box"))
W_ = {"colour": "white"}
RED = dict(ground="red", edge={"colour": "red", "width": 30}, border={"colour": "white", "width": 30}, radius=130)
def inset(cx, cy, side):
    e, b, r = (15, 30, 60) if side == 900 else (10, 20, 50)
    half = side * R2 / 2 - r * (R2 - 1)     # the drawn (rounded) diamond's half extent
    return dia(cx, cy, side, e, b, r) + [S("qld_w5-040-q01_crash_{opt}", cx - half, cy - half, 2 * half, 2 * half)]
def vary(km):
    if km: return {"keys": ["opt", "km"], "values": [[o, k] for o in range(1, 7) for k in (2, 5, 10)]}
    return {"key": "opt", "values": [1, 2, 3, 4, 5, 6]}
COMMON = ("Red sign: red edge 30 + white border 30 (the sheet's 30 / 60), r 130, white legend on Class 400 retroreflective red. The '*' diamond is the sheet's 'insert appropriate warning sign option - refer page 6': the six crash-scene options of page 6 (1-4 side impact, 5 head on, 6 rear end) are generated as variants, each scene the sheet PDF's own vector artwork placed in the diamond as page 6 draws it; "
          "the inset diamond is {side} side (note 2), yellow edge {e} + black border {b}, r {r} (the QLD W-series values at that size; not dimensioned on this sheet), and the sheet's dimensions run to its rounded tips. ")
KM = "Distance '**' = 'insert appropriate distance' with no example: 2, 5 and 10 km generated (Russell: the variants that make sense, not every value). "
def com(side): return COMMON.format(side=side, e=15 if side == 900 else 10, b=30 if side == 900 else 20, r=60 if side == 900 else 50)
c9 = 100 - 24.85 + 636.4
# page 1
mk("W5-040-Q01-1", "TAKE_CARE_HIGH_CRASH_SITE_OPTION_{opt}_RED_LONG", "TAKE CARE HIGH CRASH SITE (crash symbol option {opt})", [3000, 1800],
   inset(c9, 900, 900) + [TW(["TAKE", "CARE"], "E", 200, 200, 140, align="right", x=2720, **W_), T("HIGH", "D", 200, 660, cx=1935, **W_), T("CRASH", "D", 200, 980, cx=1935, **W_), T("SITE", "D", 200, 1300, cx=1935, **W_)],
   "Q-series sheet W5-040-Q01_1 'TAKE CARE HIGH CRASH SITE' (2025, page 1 of 6), fully dimensioned, 3000 x 1800. " + com(900) +
   "Chain 200 / 200E / 260 / 200D / 120 / 200D / 120 / 200D / 300 = 1800: cap tops 200 (TAKE CARE, Series E), 660, 980, 1300 (HIGH / CRASH / SITE, Series D). Diamond: left tip 100 from the left edge (the sheet's '100'), centred vertically (as drawn). TAKE CARE ends 280 from the right edge (the sheet's '280'), word gap 140 measured; HIGH / CRASH / SITE centred on x 1935 as drawn (measured 1936 / 1935 / 1930; not dimensioned).",
   panel_px=[331.7, 465.8, 1276.6, 1032.7], vary=vary(False), symbols=symbols, **RED)
c7 = 900
mk("W5-040-Q01-2", "TAKE_CARE_HIGH_CRASH_SITE_OPTION_{opt}_RED_SQUARE", "TAKE CARE HIGH CRASH SITE (crash symbol option {opt})", [1800, 1800],
   [TW(["TAKE", "CARE"], "E", 160, 150, 110, **W_), TW(["HIGH", "CRASH", "SITE"], "D", 140, 460, [92, 84], **W_)] + inset(900, 1700 + 20.71 - 530.33, 750),
   "Q-series sheet W5-040-Q01_2 'TAKE CARE HIGH CRASH SITE' (2025, page 2 of 6), fully dimensioned, 1800 x 1800. " + com(750) +
   "Chain 150 / 160E / 150 / 140D / 1100 / 100 = 1800: cap tops 150 (TAKE CARE 160 Series E) and 460 (HIGH CRASH SITE 140 Series D); the diamond's bottom tip is 100 above the bottom edge (centre height 1190.4), centred horizontally as drawn. Both lines centred on the sign (drawn centres 894 / 911); word gaps 110 and 92 / 84 measured. The sheet's bottom dimensions 120 (left) and 160 (right) do not correspond to any legend edge on the drawing (the legend's margins are drawn 157 / 134) and are not used.",
   panel_px=[434.7, 324.4, 1139.3, 1029.1], vary=vary(False), symbols=symbols, **RED)
def nextline(top, hN, hk, slot, g1, g2, **kw):
    return {"type": "text", "runs": [{"text": "NEXT", "series": "E", "height": hN}, {"text": "{km}", "series": "E", "height": hN, "slot": slot}, {"text": "km", "series": "Emod", "height": hk}], "gap": [g1, g2], "top": top, "colour": "white", **kw}
mk("W5-040-Q01-3", "TAKE_CARE_HIGH_CRASH_ZONE_NEXT_{km}_KM_OPTION_{opt}_RED_LONG", "TAKE CARE HIGH CRASH ZONE NEXT {km} km (crash symbol option {opt})", [3300, 1800],
   inset(c9, 900, 900) + [TW(["TAKE", "CARE"], "E", 200, 200, 137, align="right", x=3080, **W_), TW(["HIGH", "CRASH"], "E", 180, 640, 133, cx=2254, **W_), T("ZONE", "E", 180, 1000, cx=2254, **W_), nextline(1420, 180, 155, 187, 206, 140, cx=2254)],
   "Q-series sheet W5-040-Q01_3 'TAKE CARE HIGH CRASH ZONE NEXT ... km' (2025, page 3 of 6), fully dimensioned, 3300 x 1800. " + com(900) + KM +
   "Chain 200 / 200E / 240 / 180E / 180 / 180E / 240 / 180E-155Em / 200 = 1800: cap tops 200, 640, 1000, 1420 (NEXT and numeral 180 Series E, km 155 Series E modified lower case, one baseline). Diamond: left tip 100 from the left edge, centred vertically. TAKE CARE ends 220 from the right edge (the sheet's '220'); the other lines centred on x 2254 as drawn (measured 2255 / 2251 / 2257). Word gaps measured: 137, 133; NEXT to the dashed numeral box 206, box 187 wide, box to km 140.",
   panel_px=[300.1, 432.0, 1339.5, 999.0], vary=vary(True), symbols=symbols, **RED)
cx4 = 160 - 20.71 + 530.33; cy4 = 620 - 20.71 + 530.33
mk("W5-040-Q01-4", "TAKE_CARE_HIGH_CRASH_ZONE_NEXT_{km}_KM_OPTION_{opt}_RED_SQUARE", "TAKE CARE HIGH CRASH ZONE NEXT {km} km (crash symbol option {opt})", [1800, 1800],
   [TW(["TAKE", "CARE"], "E", 160, 150, 111, **W_), TW(["HIGH", "CRASH", "ZONE"], "D", 120, 390, [78, 73], **W_)] + inset(cx4, cy4, 750) +
   [T("NEXT", "E", 120, 1320, cx=1404.5, **W_), {"type": "text", "runs": [{"text": "{km}", "series": "E", "height": 120, "slot": 270}, {"text": "km", "series": "Emod", "height": 105}], "gap": 48, "top": 1530, "align": "right", "x": 1670, "colour": "white"}],
   "Q-series sheet W5-040-Q01_4 'TAKE CARE HIGH CRASH ZONE NEXT ... km' (2025, page 4 of 6), fully dimensioned, 1800 x 1800. " + com(750) + KM +
   "Chain 150 / 160E / 80 / 120D / 110 / 700 / 120E / 90 / 120E-105Em / 150 = 1800: cap tops 150 (TAKE CARE 160 Series E), 390 (HIGH CRASH ZONE 120 Series D), 1320 (NEXT 120 Series E), 1530 (numeral 120 Series E + km 105 Series E modified lower case). Diamond: top tip at 620 (the start of the 700 span), left tip 160 from the left edge (the sheet's '160'). The distance line ends 130 from the right edge (the sheet's '130'): dashed numeral box 270 wide, 48 to km (read from the drawing); NEXT centred over that line (x 1404.5). The two top lines centred on the sign (drawn centres 893 / 907); word gaps 111 and 78 / 73 measured.",
   panel_px=[362.7, 279.0, 1076.7, 993.1], vary=vary(True), symbols=symbols, **RED)
mk("W5-040-Q01-5", "WATCH_FOR_TURNING_TRAFFIC_NEXT_{km}_KM_OPTION_{opt}_RED_LONG", "WATCH FOR TURNING TRAFFIC NEXT {km} km (crash symbol option {opt})", [3300, 1800],
   inset(c9, 900, 900) + [TW(["WATCH", "FOR"], "E", 200, 200, 152, align="right", x=3080, **W_), T("TURNING", "E", 200, 590, cx=2226, **W_), T("TRAFFIC", "E", 200, 980, cx=2226, **W_), nextline(1420, 180, 155, 187, 200, 127, cx=2213)],
   "Q-series sheet W5-040-Q01_5 'WATCH FOR TURNING TRAFFIC NEXT ... km' (2025, page 5 of 6), fully dimensioned, 3300 x 1800. " + com(900) + KM +
   "Chain 200 / 200E / 190 / 200E / 190 / 200E / 240 / 180E-155Em / 200 = 1800: cap tops 200, 590, 980, 1420. Diamond: left tip 100 from the left edge, centred vertically. WATCH FOR ends 220 from the right edge (the sheet's '220'), word gap 152 measured; TURNING / TRAFFIC centred on x 2226 and the NEXT line on x 2213, as drawn (not dimensioned); NEXT to the dashed numeral box 200, box 187 wide, box to km 127.",
   panel_px=[300.1, 422.4, 1339.5, 989.4], vary=vary(True), symbols=symbols, **RED)
skip("W5-040-Q01-6", "page 6 of 6 of W5-040-Q01: the six crash-scene warning plate options (insets of the signs on pages 1-5, generated there as variants), not a sign on its own")
