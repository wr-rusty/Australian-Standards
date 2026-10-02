from qb import *
Y={"ground":"yellow"}
def symentry(sid, src, desc): return {sid: {"source": src, "pack": "QLD", "desc": desc, "colours": ["black"], "vector": "extracted from the sheet PDF (not traced)"}}
# W5-Q18_1..3 : 450 x 600 size A
for n, word, sid, items, h, j, what in [(1, ["BEWARE"], "qld_w5-q18-1_cassowary", "93,94", 30, 265, "cassowary"), (2, ["BEWARE"], "qld_w5-q18-2_emu", "119", 30, 265, "emu"), (3, ["TAKE", "CARE"], "qld_w5-q18-3_koala", "107", 55, 215, "koala")]:
    drawing = f"W5-Q18-{n}"; ppx = {1: [586.3, 214.5, 1117.8, 923.2], 2: [586.3, 214.5, 1117.8, 923.2], 3: [585.5, 186.0, 1117.0, 894.7]}[n]
    b = sym(f"W5-Q18_{n}", sid, [items]); m = mm(b, ppx, 450)
    sy = 45 + 60 + h; w = m[2] * j / m[3]
    if len(word) == 2:
        rr = runs(drawing, ppx, 450, 50, 100, mingap=14); g = gaps(rr)[0]; first = TW(word, "D", 60, 45, round(g)); gnote = f" Word gap TAKE-CARE {round(g)} measured on the sheet."
    else: first = T(word[0], "D", 60, 45); gnote = ""
    mk(f"W5-Q18-{n}", "_".join(word) + f"_{what.upper()}_RECENT_CROSSINGS_YELLOW_TALL", " ".join(word) + f" ({what} symbol) RECENT CROSSINGS", [450, 600],
       [first, S(sid, (450 - w) / 2, sy, w, j), T("RECENT", "D", 50, sy + j + h), T("CROSSINGS", "D", 50, sy + j + h + 75)],
       f"Q-series sheet W5-Q18_{n} wildlife warning sign '{' '.join(word)} / {what} / RECENT CROSSINGS' (Far North District wildlife management, temporary 5-day sign). Size A 450 x 600 generated (B 900 x 1200 also tabled), r 50, c 10 yellow edge / d 30 (edge 10 + black border 20). "
       f"Chain e 45 / k 60D / h {h} / j {j} (symbol) / h {h} / f 50D / g 25 / f 50D / e 45 = 600: cap tops 45, {sy + j + h}, {sy + j + h + 75}; symbol top {sy}, height j {j}, its width {w:.1f} from the artwork's aspect (drawn {m[2]} x {m[3]} at {m[0]}, {m[1]} on the sheet's sign), centred." + gnote +
       f" The {what} is the sheet PDF's own vector artwork (tools/symbols/{sid}.svg). Black on Class 400 retroreflective yellow.",
       panel_px=ppx, drawing=drawing, radius=50, symbols=symentry(sid, drawing, f"{what} silhouette, vector path(s) {items} of the sheet PDF"), **YB(10, 20))
# W5-Q18_4
ppx = [505.9, 441.8, 1214.6, 961.5]
print("WILDLIFE 120D", width("WILDLIFE", "D", 120), "120C", width("WILDLIFE", "C", 120), "drawn", runs("W5-Q18-4", ppx, 750, 85, 195, mingap=40))
