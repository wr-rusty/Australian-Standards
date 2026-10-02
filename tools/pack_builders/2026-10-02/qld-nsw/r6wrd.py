import sys; sys.path.insert(0,"."); from mk import *
SYMS={"sa_r6-sa109_skateboard":{"source":"R6-SA109A","pack":"SA","desc":"skateboard side view, 70.2 x 16.1 — the sheet's 10 mm grid inset outline filled (PDF vector strokes of the inset, not a raster trace of the sign, where the slash covers it)"},
      "sa_r6-sa109_skate":{"source":"R6-SA109A","pack":"SA","desc":"in-line skate, 53.7 x 37.8 — from the 10 mm grid inset outline, filled"},
      "sa_r6-sa109_scooter":{"source":"R6-SA109A","pack":"SA","desc":"kick scooter, 49.3 x 50.1 — from the 10 mm grid inset outline, filled between its inner and outer outlines (wheel rings open)"}}
def rings(top1, top2):
    els=[]
    for cx,cy,sid,dx,dy in ((112.5,top1+45,"sa_r6-sa109_skateboard",0,4.25),(60,top2+45,"sa_r6-sa109_skate",1.3,3.3),(165,top2+45,"sa_r6-sa109_scooter",-0.55,-1.45)):
        els+=[symc(sid,cx+dx,cy+dy), annulus(cx,cy,45,37.5), slash(cx,cy,41,7.5)]
    return els
COMMON="Three red prohibition rings 90 dia (ring and slash 7.5 wide, measured — not dimensioned; slash from upper right to lower left over the symbol): skateboard on top (centred, 67.5/90/67.5), in-line skate and scooter below (15 / 90 / 15 / 90 / 15, the sheet's 98 | 98 from the ring edges to the sign's centre line). Pictograms from the sheet's 10 mm grid inset (outlines filled; skateboard 70 x 16, skate 54 x 38, scooter 49 x 50), placed where the sign shows them (measured). The sign draws a hairline white keyline round each pictogram part (CAD outline) — not reproduced. "
spec("R6-SA109AA","END_WHEELED_RECREATIONAL_DEVICES_NOT_PERMITTED_WHITE_TALL","END (no skateboards, no skates, no scooters)",(225,260),"white",
     bordered(0,0,225,51,10,3,3)+[T("END","E",20,15,55)]+rings(58,158),
     "Sheet R6-SA109 (2025, 1:5): R6-SA109AA 225 x 260 illustrated (A 450 x 520; the register lists A first, PNG R6-SA109A.png), R10, white, no outer border. END panel across the top: black border 3 inside a 3 white edge (sheet 3 / 6), outer y 3-48 measured (R7 / R4 from the sign's R10); END 20 high, baseline 35 (the sheet's 35), ink 55 (85/55/86) — series not stated: Series E gives 56.6 (D 47.8). Chain 35 (baseline) / 23 / 90 ring / 10 / 90 ring / 12 = 260. "+COMMON,
     radius=10, drawing="R6-SA109A", panel_px=[521.0, 909.2, 877.5, 1320.8], symbols=SYMS)
spec("R6-SA110AA","WHEELED_RECREATIONAL_DEVICES_NOT_PERMITTED_WHITE_SQUARE","(no skateboards, no skates, no scooters)",(225,210),"white",
     rings(10,110),
     "Sheet R6-SA110 (2025, 1:5): R6-SA110AA illustrated, drawn 225 x 210 (the size table says 225 x 260, the register 225 x 210; A 450 x 450), R10, white, no outer border. The sheet's vertical chain reads 98 / 10 / 90 / 12 (= 210), but the sign is drawn 10 / 90 / 10 / 90 / 10 (rings measured at y 9.9-100.7 and 109.3-200.1): drawn as the drawing, the 98 and 12 taken as typing errors. "+COMMON,
     radius=10, drawing="R6-SA110A", panel_px=[485.2, 938.8, 841.8, 1271.5], symbols=SYMS)
spec("R6-SA111AA","WHEELED_RECREATIONAL_DEVICES_NOT_PERMITTED_ON_FOOTPATH_WHITE_TALL","(no skateboards, no skates, no scooters) ON FOOTPATH",(225,260),"white",
     rings(12,112)+bordered(0,209,225,51,10,3,3)+[Wd(["ON","FOOTPATH"],14.3,"D",20,225,174,expect_total=True)],
     "Sheet R6-SA111 (2026, 1:5): R6-SA111AA 225 x 260 illustrated (A 450 x 520), R10, white, no outer border. Chain 12 / 90 ring / 10 / 90 ring / 23 / 35 = 260 (35 = top of the legend to the bottom edge: 20 D + 15). ON FOOTPATH panel across the bottom: black border 3 inside a 3 white edge (3 / 6), outer y 212-257 measured; ON FOOTPATH 20 D, top 225, overall ink 174 (25/174/26; word gap not stated, set so the pair spans 174: 14.3; measured 15). "+COMMON,
     radius=10, drawing="R6-SA111A", panel_px=[521.0, 909.2, 877.5, 1320.8], symbols=SYMS)
