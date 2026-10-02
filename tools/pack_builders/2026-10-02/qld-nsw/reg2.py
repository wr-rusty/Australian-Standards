import sys; sys.path.insert(0,"."); from mk import *
E2="The sheet's two edge figures are the white edge and edge + black border, as the AS 1743 drawings. "
skip("R2-SA62","RIGHT TURN FROM LEFT ONLY / ADELAIDE METRO BUSES ONLY / 7-9 AM 4.30-6.30 PM MON-FRI","composite of three 'modified' signs (R2-21AA, R6-SA67, R9-1-2 modified) at 300 x 1000: the sheet gives only the three panel heights (394 / 295 / 295) and no letter sizes, widths or arrow dimensions for the modified parts — cannot be drawn accurately from the sheet (as R2-SA61)")
spec("R4-SA61A","END_SCHOOL_ZONE_END_{speed}_AREA_WHITE_TALL","END SCHOOL ZONE / END {speed} AREA",(450,1050),"white",
     bordered(0,0,450,300,50,5,10)+[T("END","E",50,45,142),T("SCHOOL","D",50,125,255),T("ZONE","D",50,205,165),
      T("END","D",120,355,287), annulus(225,690,160,135,"black"), T("{speed}","C",150,615,cx=225), T("AREA","D",100,900,340)],
     "R4-SA61A (450 x 1050) illustrated (B 600 x 1400), 2016, 1:10; R50, white ground, no outer border. END SCHOOL ZONE panel across the top as R4-SA59/60: black border 10 inside a 5 white edge (sheet 5 / 15), outer 5..295; END 50 E top 45, SCHOOL 50 D top 125, ZONE 50 D top 205 (baselines 95 / 175 / 255, 40 below); widths END 142 (154/142/154), SCHOOL 255 (97/255/98), ZONE 165 (142/165/143) — the top chains are listed bottom line first. Below the panel: END 120 D baseline 475 (295 + 180; top 355), ink 287 (82/287/82); black ring outer dia 320 (160 + 160; top at 295 + 235 = 530, centre (225, 690)), 25 wide (inner R135); area speed numerals 150 C in the dashed box, 85 above the ring's bottom (baseline 765, top 615), centred; AREA 100 D baseline 1000 (475 + 525; top 900, 50 below), ink 340 (55/340/55); ring bottom to sign bottom 200. The sheet shows no numerals ('End (km/h) Area'): generated at 40 and 50 (the area limits signed in SA with R4-10 / R4-11; R4-SA109 covers END 30 AREA on its own). Approval required.",
     radius=50, panel_px=px("R4-SA61A",(562,572,865,1278)), vary={"key":"speed","values":[40,50]}, folder="Speed Signs/End")
spec("R6-SA66","FISHING_FROM_BRIDGE_PROHIBITED_WHITE_LONG","FISHING FROM BRIDGE PROHIBITED",(900,600),"white",
     [T("FISHING","C",100,85,415),Wd(["FROM","BRIDGE"],75,"C",100,250,[281,383]),T("PROHIBITED","C",100,415,630)],
     E2+"R6-SA66 900 x 600 (2015, 1:10), R50, 7 / 21 (edge 7 + border 14). Three lines 100 C, baselines 185 / 350 / 515 (165 pitch, 85 below): FISHING 415 (242/415/243), FROM 281 + 75 + BRIDGE 383 (80/281/75/383/81), PROHIBITED 630 (135/630/135).",
     radius=50, edge=("white",7), border=("black",14), panel_px=px("R6-SA66",(397,613,1003,1016)))
spec("R6-SA102","FISHING_FROM_CAUSEWAY_PROHIBITED_WHITE_LONG","FISHING FROM CAUSEWAY PROHIBITED",(900,600),"white",
     [Wd(["FISHING","FROM"],70,"C",100,85,[415,281]),T("CAUSEWAY","C",100,250,568),T("PROHIBITED","C",100,415,630)],
     E2+"R6-SA102 900 x 600 (2015, 1:10), R50, 7 / 21 (edge 7 + border 14). Three lines 100 C, baselines 185 / 350 / 515 (85 below): FISHING 415 + 70 + FROM 281 (67/415/70/281/67), CAUSEWAY 568 (166/568/166), PROHIBITED 630 (135/630/135). Sheet note: not regulatory by itself — fishing must be prohibited on the causeway by regulation before the sign is installed.",
     radius=50, edge=("white",7), border=("black",14), panel_px=px("R6-SA102",(397,520,1003,923)))
spec("R6-SA67","ADELAIDE_METRO_BUSES_ONLY_WHITE_SQUARE","ADELAIDE METRO BUSES ONLY",(300,300),"white",
     [T("ADELAIDE","D",40,40,252),T("METRO","E",40,100,192),T("BUSES","E",40,160,189),T("ONLY","E",40,220,160)],
     E2+"R6-SA67 300 x 300 (2016, 1:5), R25, 3 / 9 (edge 3 + border 6). Four lines 40 high, baselines 80 / 140 / 200 / 260 (40 below): ADELAIDE D 252 (24/252/24), METRO E 192 (54/192/54), BUSES E 189 (55/189/56), ONLY E 160 (70/160/70).",
     radius=25, edge=("white",3), border=("black",6), panel_px=px("R6-SA67",(521,725,925,1129)))
spec("R6-SA68","ADELAIDE_METRO_BUSES_EXCEPTED_WHITE_SQUARE","ADELAIDE METRO BUSES EXCEPTED",(300,300),"white",
     [T("ADELAIDE","D",40,40,252),T("METRO","E",40,100,192),T("BUSES","E",40,160,189),T("EXCEPTED","D",40,220,249)],
     E2+"R6-SA68 300 x 300 (2016, 1:5), R25, 3 / 9 (edge 3 + border 6). Four lines 40 high, baselines 80 / 140 / 200 / 260 (40 below): ADELAIDE D (the sheet's chain reads 24 / 222 / 24, which does not add to 300 — 252 as on R6-SA67), METRO E 192 (54/192/54), BUSES E 189 (55/189/56), EXCEPTED D 249 (25/249/26).",
     radius=25, edge=("white",3), border=("black",6), panel_px=px("R6-SA68",(521,636,925,1040)))
spec("R6-SA106A","NEXT_{dist}_m_WHITE_WIDE","NEXT {dist} m",(1200,370),"white",
     [{"type":"text","runs":[{"text":"NEXT","series":"C","height":140},{"text":"{dist}","series":"C","height":140},{"text":"m","series":"C","height":120}],"gap":[105,70],"top":115,"expect":[356,None,101]}],
     E2+"R6-SA106A (1200 x 370) illustrated (B 1440 x 450, C 1800 x 560), 2015, 1:10; R50, 10 / 30 (edge 10 + border 20). One line: NEXT 140 C (ink 356), 105 gap, distance numerals 140 C ('Varies', dashed box), 70 gap, m 120 C lower case (ink 101); baseline 255 (top 115, 115 below). The sheet's chain 149 / 356 / 105 / varies / 70 / 101 / 149 fixes the margins for its dashed box (270 wide); the line is centred as a whole here so that it stays centred for any numeral width. The sheet gives no example distance: generated at 100 to 900 m in hundreds (a sign under R6-22 for lengths short of 1 km; R6-SA105 covers whole km) — not confirmed against SA practice. Mounted below R6-22.",
     radius=50, edge=("white",10), border=("black",20), panel_px=px("R6-SA106A",(297,813,1105,1062)), vary={"key":"dist","values":[100,200,300,400,500,600,700,800,900]})
spec("R6-SA12","CLEARANCE_{clr}_m_WHITE_WIDE_SKINNY","CLEARANCE {clr} m",(2100,450),"white",
     [{"type":"text","runs":[{"text":"CLEARANCE","series":"D","height":160},{"text":"{clr}","series":"D","height":160},{"text":"m","series":"D","height":140}],"gap":[120,80],"top":145,"expect":[1210,None,140]}],
     E2+"R6-SA12 2100 x 450 (undated, 1:15), 10 / 30 (edge 10 + border 20); corner radius not stated on the sheet — R50 used (measured about 50, as the other 10 / 30 plates). One line centred ('=' margins): CLEARANCE 160 D (ink 1210), 120 gap, clearance numerals 160 D ('varies', dashed n.n), 80 gap, m 140 D lower case (ink 140); baseline 305 (top 145, 145 below). The sheet gives no example: generated at 3.0 to 5.0 m in 0.1 m steps (the range of posted low clearances; every tenth is needed because the sign states the structure's own figure).",
     radius=50, edge=("white",10), border=("black",20), panel_px=px("R6-SA12",(246,691,1188,893)), vary={"key":"clr","values":[f"{v/10:.1f}" for v in range(30,51)]})
spec("R7-SA2B","AHEAD_WHITE_LONG_SKINNY","AHEAD",(1800,450),"white",[T("AHEAD","E",240,105,1229)],
     E2+"Sheet R7-SA2 (2015, 1:15): R7-SA2B 1800 x 450 illustrated (A 1650 x 450; the register lists A first, PNG R7-SA2A.png), R100, 10 / 30 (edge 10 + border 20). AHEAD 240 E, baseline 345 (top 105, 105 below), ink 1229 (285/1229/286). Smaller sizes: AS 1743 R7-2.",
     radius=100, edge=("white",10), border=("black",20), drawing="R7-SA2A", panel_px=px("R7-SA2A",(380,827,1188,1029)))
spec("R7-SA4","END_WHITE_LONG_SKINNY","END",(1650,450),"white",[T("END","E",200,125,566)],
     E2+"R7-SA4 1650 x 450 (2015, 1:15), R100, 10 / 30 (edge 10 + border 20). END 200 E, 125 above and below (top 125), ink 566 (542/566/542).",
     radius=100, edge=("white",10), border=("black",20), panel_px=px("R7-SA4",(412,877,1152,1079)))
spec("R7-SA100A","{dist}_m_AHEAD_WHITE_LONG","{dist} m AHEAD",(1200,800),"white",
     [{"type":"text","runs":[{"text":"{dist}","series":"E","height":200},{"text":"m","series":"E","height":170}],"gap":85,"top":150,"expect":[None,175]},T("AHEAD","D",200,450,860)],
     E2+"R7-SA100A (1200 x 800) illustrated (B 1440 x 960, C 1800 x 1200), 2015, 1:15; R150, 15 / 45 (edge 15 + border 30). Line 1 centred ('=' margins): distance numerals 200 E ('varies', dashed box), 85 gap, m 170 E lower case (ink 175), baseline 350 (top 150). AHEAD 200 D baseline 650 (top 450, 150 below), ink 860 (170/860/170). The sheet gives no example distance: generated at 100 to 500 m in hundreds (three numerals, as the sheet's box and title 'XXXm Ahead') — not confirmed against SA practice. For use with R6-22.",
     radius=150, edge=("white",15), border=("black",30), panel_px=px("R7-SA100A",(440,765,979,1124)), vary={"key":"dist","values":[100,200,300,400,500]})
gen()
