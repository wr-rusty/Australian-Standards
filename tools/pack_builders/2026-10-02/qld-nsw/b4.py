from qb import *
G_ = {"colour": "green"}
def dia(cx, cy, side, e, b, r, ground="yellow", edgec="yellow", borderc="black"):
    out = []; h = side * R2 / 2
    for inset, col, rr in [(0, edgec, r), (e, borderc, r - e), (e + b, ground, r - e - b)]:
        d = h - inset * R2
        out.append({"type": "polygon", "points": [[round(cx, 2), round(cy - d, 2)], [round(cx + d, 2), round(cy, 2)], [round(cx, 2), round(cy + d, 2)], [round(cx - d, 2), round(cy, 2)]], "radius": max(rr, 0), "colour": col})
    return out
# ---- W5-Q19
cx, cy = 2400 - 100 + 20.71 - 530.33, 678.6
px0, py0 = cx - 375, 1200
els = [T("CONSERVATION", "C", 170, 160, align="left", x=135, **G_), TW(["AREA", "FOR"], "C", 170, 490, 96, align="left", x=135, **G_), T("WILDLIFE", "C", 170, 820, align="left", x=135, **G_),
       T("NEXT", "D", 140, 1230, align="left", x=252, **G_),
       {"type": "text", "runs": [{"text": "{km}", "series": "D", "height": 120, "slot": 204}, {"text": "km", "series": "Emod", "height": 105}], "gap": 74, "top": 1480, "align": "left", "x": 223, "colour": "green"}]
els += dia(cx, cy, 750, 10, 20, 50)
els += [S("qld_w5-q18-3_koala", cx - 321.0, cy - 221.6, 591.8, 442.7)]
els += [{"type": "panel", "x": px0, "y": py0, "w": 750, "h": 500, "radius": 50, "colour": "white"}, {"type": "panel", "x": px0 + 10, "y": py0 + 10, "w": 730, "h": 480, "radius": 40, "colour": "green"}, {"type": "panel", "x": px0 + 30, "y": py0 + 30, "w": 690, "h": 440, "radius": 20, "colour": "white"},
        TW(["REPORT", "INJURED"], "C", 70, py0 + 80, 49, cx=cx, **G_), TW(["ANIMALS", "PHONE"], "C", 70, py0 + 215, 42, cx=cx, **G_), TW(["1300", "ANIMAL"], "C", 70, py0 + 350, 37, cx=cx, **G_)]
mk("W5-Q19", "CONSERVATION_AREA_FOR_WILDLIFE_NEXT_{km}_KM_WHITE", "CONSERVATION AREA FOR WILDLIFE NEXT {km} km (W5-47B koala, REPORT INJURED ANIMALS PHONE 1300 ANIMAL)", [2400, 1800], els,
   "Q-series sheet W5-Q19 special warning sign 'CONSERVATION AREA FOR WILDLIFE - NEXT ..km' (2023), fully dimensioned, one size 2400 x 1800, R200, white edge 20 + green border 40 (the sheet's 20 / 60). Left chain 160 / 170C / 160 / 170C / 160 / 170C / 240 / 140D / 110 / 120D-105Em / 200 = 1800: cap tops 160 (CONSERVATION), 490 (AREA FOR), 820 (WILDLIFE), 1230 (NEXT, 140 Series D), 1480 (numeral 120 Series D + km 105 Series E modified lower case, one baseline). The three name lines start 135 from the left edge (the sheet's '135'); NEXT and the distance line are placed as drawn (ink from x 252 and the dashed numeral box from x 223, 204 wide; gap box to km 74; AREA-FOR gap 96 measured). DISAGREEMENT: CONSERVATION is labelled 170C like the other two lines but the sheet draws it in Series B (drawn 1107 wide = Series B at 170; Series C is 1367): the labelled Series C fits (clear of the diamond by about 85) and is generated. "
   "Inset W5-47B koala diamond ('alternative wildlife warning signs ... may be substituted'): size B 750 side (bounding square 1060.66), r 50, yellow edge 10 + black border 20, its rounded right tip 100 from the sign's right edge (the sheet's '100'; sharp corner 20.7 further out), centre height 678.6 as drawn (not dimensioned); koala as drawn on the inset (the W5-Q18 koala artwork, 591.8 x 442.7). Inset W8-Q18B plate REPORT INJURED ANIMALS PHONE 1300 ANIMAL: 750 x 500, r 50, white edge 10 + green border 20, three lines 70 Series C at 80 / 215 / 350 from its top (chain 80 / 70C / 65 / 70C / 65 / 70C / 80), its bottom 100 above the sign's bottom edge (the sheet's '100'), centred under the diamond as drawn; word gaps 49 / 42 / 37 measured. Distance: 'insert appropriate distance' with no example, so 2, 5 and 10 km are generated (Russell: the variants that make sense, not every value). Green legend and border on white, yellow / black inset.",
   panel_px=[374.3, 391.7, 1351.9, 1124.9], radius=200, ground="white", edge={"colour": "white", "width": 20}, border={"colour": "green", "width": 40},
   vary={"key": "km", "values": [2, 5, 10]}, drawn_value=2, symbols=symentry("qld_w5-q18-3_koala", "W5-Q18-3", "koala silhouette as W5-Q18_3 (the sheet's inset W5-47B)"))
# ---- W5-Q21
els = [TW(["CARE", "FOR", "OUR"], "D", 120, 130, [71, 70], **G_), T("ISLAND’S", "D", 180, 360, **G_), T("WILDLIFE", "D", 180, 640, **G_),
       {"type": "panel", "x": 150, "y": 905, "w": 1100, "h": 600, "radius": 75, "colour": "green"}, {"type": "panel", "x": 170, "y": 925, "w": 1060, "h": 560, "radius": 55, "colour": "white"},
       TW(["REPORT", "INJURED"], "C", 100, 985, 54, **G_), TW(["ANIMALS", "PHONE"], "C", 100, 1155, 59, **G_), TW(["1300", "ANIMAL"], "C", 100, 1325, 54, **G_)]
mk("W5-Q21", "CARE_FOR_OUR_ISLANDS_WILDLIFE_REPORT_INJURED_ANIMALS_WHITE_TALL", "CARE FOR OUR ISLAND'S WILDLIFE REPORT INJURED ANIMALS PHONE 1300 ANIMAL", [1400, 1600], els,
   "Q-series sheet W5-Q21 wildlife information sign 'CARE FOR OUR ISLAND'S WILDLIFE / REPORT INJURED ANIMALS PHONE 1300 ANIMAL' (2023), fully dimensioned, one size 1400 x 1600, R200, white edge 20 + green border 40 (the sheet's 20 / 60). Chain 130 / 120D / 110 / 180D / 100 / 180D / 85 / inner panel 600 / 95 = 1600: cap tops 130, 360, 640. Inner panel: green outline 20 wide, R75, 1100 x 600 (x 150-1250 as drawn, 150 each side; the width is not dimensioned), top 905; inside it 80 / 100C / 70 / 100C / 70 / 100C / 80: cap tops 985, 1155, 1325. Word gaps measured on the sheet (71 / 70; 54, 59, 54). Green on white.",
   panel_px=[318.3, 254.3, 1297.7, 1373.6], radius=200, ground="white", edge={"colour": "white", "width": 20}, border={"colour": "green", "width": 40})
# ---- W5-Q22
k = 0.7874; ppx = [516.4 - 15 * k, 399.3 - 15 * k, 1201.4 + 15 * k, 1084.4 + 15 * k]
b = sym("W5-Q22", "qld_w5-q22_fauna_crossing", ["327-339,341-343,345,346,348,349,351-363,365-367,369,370,372,373,375-378"]); m = mm(b, ppx, 900); print("Q22 symbol drawn", m)
mk("W5-Q22", "FAUNA_CROSSING_WHITE_SQUARE", "FAUNA CROSSING (glider on a rope bridge between trees over two cars)", [900, 900],
   [S("qld_w5-q22_fauna_crossing", 75, 90, 750, 360, colour="green"), T("FAUNA", "D", 110, 540, **G_), T("CROSSING", "D", 110, 700, **G_)],
   f"Q-series sheet W5-Q22 wildlife sign 'FAUNA CROSSING' (2023), fully dimensioned, one size 900 x 900, R100, white edge 15 + green border 30 (the sheet's 15 / 45). Chain 90 / 360 (symbol) / 90 / 110D / 50 / 110D / 90 = 900: symbol top 90, cap tops 540, 700. Symbol 750 wide (the sheet's '750') x 360, centred; it is the sheet PDF's own vector artwork (tools/symbols/qld_w5-q22_fauna_crossing.svg: two trees, a rope bridge with a glider, two cars; drawn {m[2]} x {m[3]} on the sheet's sign). Green on white.",
   panel_px=ppx, radius=100, ground="white", edge={"colour": "white", "width": 15}, border={"colour": "green", "width": 30},
   symbols=symentry("qld_w5-q22_fauna_crossing", "W5-Q22", "fauna crossing scene, vector items 327-378 of the sheet PDF", ("green",)))
skip("W5-Q23", "the mahogany glider is a tonal (shaded) illustration embedded as an image on the sheet, not a flat sign-face symbol: it cannot be redrawn accurately as vector artwork from the sheet; the text layout (2400 x 1800, CONSERVATION AREA / FOR MAHOGANY GLIDER / REPORT INJURED ANIMALS PH 1300 ANIMAL) is dimensioned", "CONSERVATION AREA FOR MAHOGANY GLIDER REPORT INJURED ANIMALS PH 1300 ANIMAL")
