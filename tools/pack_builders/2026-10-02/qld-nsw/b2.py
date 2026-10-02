from qb import *
from b1 import symentry
mk("W5-Q18-4", "WILDLIFE_RECENT_CROSSINGS_YELLOW", "WILDLIFE RECENT CROSSINGS", [750, 550],
   [T("WILDLIFE", "C", 120, 80), T("RECENT", "D", 80, 280), T("CROSSINGS", "D", 80, 400)],
   "Q-series sheet W5-Q18_4 wildlife warning sign 'WILDLIFE RECENT CROSSINGS' (Far North District wildlife management, temporary 5-day sign), one size dimensioned directly: 750 x 550, R50, 10 yellow edge / 30 (edge 10 + black border 20). Chain 80 / 120D / 80 / 80D / 40 / 80D / 70 = 550: cap tops 80, 280, 400. DISAGREEMENT: WILDLIFE is labelled 120D, but at 120 Series D it is 681 wide in the 690 between the borders; the sheet's own live text sets it in Series C (FHWA Series C font, drawn 590 wide; AS 1744 Series C at 120 = 581), so WILDLIFE is generated 120 Series C; RECENT / CROSSINGS 80 Series D as labelled. Black on Class 400 retroreflective yellow.",
   panel_px=[505.9, 441.8, 1214.6, 961.5], radius=50, **YB(10, 20))
B25 = {"border": {"colour": "black", "width": 25}}
panel = "one panel of the modular W5-Q18_5 to _9 wildlife assembly (the sheet's 'example use': a 600 symbol panel beside TAKE CARE over the 1200 x 300 RECENT CROSSINGS panel); square corners, black border 25, no edge strip, as dimensioned. "
mk("W5-Q18-5", "TAKE_CARE_YELLOW_SQUARE", "TAKE CARE", [600, 600], [T("TAKE", "D", 140, 110), T("CARE", "D", 140, 350)],
   "Q-series sheet W5-Q18_5 'TAKE CARE' panel, 600 x 600: " + panel + "Chain 110 / 140D / 100 / 140D / 110 = 600: cap tops 110, 350. Black on Class 400 retroreflective yellow.",
   panel_px=[628.5, 270.2, 1100.9, 742.7], **B25)
mk("W5-Q18-6", "RECENT_CROSSINGS_YELLOW_LONG_SKINNY", "RECENT CROSSINGS", [1200, 300], [TW(["RECENT", "CROSSINGS"], "D", 90, 105, round(gaps(runs("W5-Q18-6", [373.0, 388.5, 1317.9, 624.7], 1200, 110, 190, mingap=30))[0]))],
   "Q-series sheet W5-Q18_6 'RECENT CROSSINGS' panel, 1200 x 300: " + panel + "Chain 105 / 90D / 105 = 300: cap top 105. Word gap measured on the sheet. Black on Class 400 retroreflective yellow.",
   panel_px=[373.0, 388.5, 1317.9, 624.7], **B25)
for n, what, sid, ppx, top, h in [(7, "cassowary", "qld_w5-q18-1_cassowary", [609.0, 270.2, 1081.4, 742.7], 100, 400), (8, "emu", "qld_w5-q18-2_emu", [609.0, 270.2, 1081.4, 742.7], 75, 450), (9, "koala", "qld_w5-q18-3_koala", [608.8, 306.7, 1081.3, 779.2], 125, 350)]:
    mk(f"W5-Q18-{n}", f"{what.upper()}_YELLOW_SQUARE", f"({what} symbol)", [600, 600], [S(sid, 50, top, 500, h)],
       f"Q-series sheet W5-Q18_{n} {what} symbol panel, 600 x 600: " + panel + f"Chain {top} / {h} (symbol) / {top} = 600: symbol top {top}, height {h}, centred, its width from the artwork's aspect. The {what} is the W5-Q18 artwork (tools/symbols/{sid}.svg, the sheet PDF's own vector). Black on Class 400 retroreflective yellow.",
       panel_px=ppx, symbols=symentry(sid, f"W5-Q18-{n}", f"{what} silhouette as W5-Q18_{n - 6}"), **B25)
