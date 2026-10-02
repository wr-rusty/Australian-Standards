from qb import *
def symentry(sid, src, desc, colours=("black",)): return {sid: {"source": src, "pack": "QLD", "desc": desc, "colours": list(colours), "vector": "extracted from the sheet PDF (not traced)"}}
green = lambda p: p[1] > p[0] + 25 and p[1] > p[2] + 15 and p[0] < 120
animals = {1: "ducks", 2: "possum", 3: "lizard", 4: "echidna", 5: "small bird", 6: "turtle", 7: "snake", 8: "lyrebird", 9: "tree kangaroo", 10: "northern bettong"}
titles = {1: "DUCKS", 2: "POSSUMS", 3: "LIZARDS", 4: "ECHIDNAS", 5: "SMALL BIRDS", 6: "TURTLES", 7: "SNAKES", 8: "LYREBIRDS", 9: "TREE KANGAROOS", 10: "NORTHERN BETTONG"}
for n in range(1, 11):
    vc = f"W5-Q20_{n}"; drawing = f"W5-Q20-{n}"
    fl = fills(vc); outer = max((f for f in fl if f[3] == 8 and f[2][1] < 1100), key=lambda f: (f[2][2] - f[2][0]))
    ppx_g = outer[2]   # green border outer = inside the white edge 10
    k = (ppx_g[2] - ppx_g[0]) / 730; ppx = [ppx_g[0] - 10 * k, ppx_g[1] - 10 * k, ppx_g[2] + 10 * k, ppx_g[3] + 10 * k]
    items = [f for f in fl if f[1] == outer[1] and f[0] != outer[0] and f[2][0] > ppx_g[0] and f[2][2] < ppx_g[2] and f[2][1] > ppx_g[1] and f[2][3] < ppx_g[3] and (f[2][2] - f[2][0]) > 12]
    rows_ = [r for r in texts(vc) if "SIZE A" in r[0] or r[0].strip() in ("50", "80", "250", "200", "47", "67")]
    tall = any(r[0].strip() == "250" for r in texts(vc, 1300))
    e, f_, g = (50, 250, 47) if tall else (80, 200, 67)
    sid = f"qld_w5-q20-{n}_" + animals[n].replace(" ", "_")
    b = sym(vc, sid, [",".join(str(i[0]) for i in items)]); m = mm(b, ppx, 750)
    sy = 60 + 60 + 43 + 90 + g; w = m[2] * f_ / m[3]
    rr = runs(drawing, ppx, 750, 65, 115, mingap=18, ink=green); gp = [round(v) for v in gaps(rr)]
    print(n, tall, len(items), "drawn mm", m, "tabled top", sy, "h", f_, "w", round(w, 1), "gaps", gp, "inner width ok", w < 690)
    mk(f"W5-Q20-{n}", f"CARE_FOR_OUR_WILDLIFE_{titles[n].replace(' ', '_')}_WHITE", f"CARE FOR OUR WILDLIFE ({animals[n]} symbol)", [750, 600],
       [TW(["CARE", "FOR", "OUR"], "D", 60, 60, gp, colour="green"), T("WILDLIFE", "D", 90, 163, colour="green"), S(sid, (750 - w) / 2, sy, w, f_, colour="green")],
       f"Q-series sheet W5-Q20_{n} wildlife sign 'CARE FOR WILDLIFE - {titles[n]}' (2023, page {n} of 10). Size A 750 x 600 generated (B 900 x 700 also tabled), r 50, c 10 white edge / d 30 (edge 10 + green border 20). "
       f"Chain n 60 / m 60D / k 43 / h 90D / g {g} / f {f_} (symbol) / e {e} = 600: cap tops 60 (CARE FOR OUR) and 163 (WILDLIFE); symbol top {sy}, height f {f_}, width {w:.1f} from the artwork's aspect, centred (drawn {m[2]} x {m[3]} at x {m[0]}, y {m[1]} on the sheet's sign). "
       f"Word gaps {gp} measured on the sheet. The {animals[n]} symbol is the sheet PDF's own vector artwork (tools/symbols/{sid}.svg). Green legend, symbol and border on white.",
       panel_px=ppx, drawing=drawing, radius=50, ground="white", edge={"colour": "white", "width": 10}, border={"colour": "green", "width": 20},
       symbols=symentry(sid, drawing, f"{animals[n]} silhouette, vector item(s) {[i[0] for i in items]} of the sheet PDF", ("green",)))
