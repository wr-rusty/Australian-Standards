from qb import *
INFO = {1: ("KEEP TRACK CLEAR", "T_INTERSECTION", "T-intersection beyond the crossing", 20, "55 / 590 / 25 / 55 / 90D / 85 = 900"),
        2: ("KEEP TRACK CLEAR", "CROSS_ROAD", "cross road beyond the crossing", 20, "75 / 770 / 25 / 55 / 90D / 85 = 1100"),
        3: ("KEEP INTERSECTION CLEAR", "CROSS_ROAD", "crossing beyond a cross road", 20, "75 / 770 / 25 / 45 / 90D / 45 / 90D / 60 = 1200"),
        4: ("KEEP TRACK CLEAR", "ROUNDABOUT", "roundabout beyond the crossing", 40, "75 / 1070 / 25 / 55 / 90D / 85 = 1400"),
        5: ("KEEP ROUNDABOUT CLEAR", "ROUNDABOUT_CROSSING_AHEAD", "crossing beyond a roundabout, straight ahead", 40, "75 / 1070 / 25 / 45 / 90D / 45 / 90D / 60 = 1500"),
        6: ("KEEP ROUNDABOUT CLEAR", "ROUNDABOUT_CROSSING_RIGHT", "crossing on the right-hand leg of a roundabout", 40, "95 / 900 / 75 / 45 / 90D / 45 / 90D / 60 = 1400"),
        7: ("KEEP ROUNDABOUT CLEAR", "ROUNDABOUT_CROSSING_LEFT", "crossing on the left-hand leg of a roundabout", 40, "95 / 900 / 75 / 45 / 90DN / 45 / 90DN / 60 = 1400")}
notyel = lambda p: not (p[0] > 200 and p[1] > 170 and p[2] < 120) and not (p[0] > 200 and p[1] < 110)
black = lambda p: p[0] < 110 and p[1] < 110 and p[2] < 110
white = lambda p: p[0] > 200 and p[1] > 200 and p[2] > 200
for n, (legend, kind, what, ex, chain) in INFO.items():
    vc = f"W7-Q01_{n}"; drawing = f"W7-Q01-{n}"; fl = fills(vc)
    yel = [f for f in fl if f[1] == "#fad716" and f[2][2] - f[2][0] > 500][0]; red = [f for f in fl if f[1] == "#ed3237" and f[2][2] - f[2][0] > 500][0]
    ppx = [yel[2][0], yel[2][1], yel[2][2], red[2][3]]; k = (ppx[2] - ppx[0]) / 1200
    H = round((ppx[3] - ppx[1]) / k / 10) * 10; rt = round((red[2][1] - ppx[1]) / k / 5) * 5
    lines = legend.split(" "); two = H - rt > 300
    tl = [" ".join(lines[:-1]), lines[-1]] if two else [legend]
    tops = [rt + 45, rt + 180] if two else [rt + 55]
    # symbol: dark fills inside the yellow part
    reg = (ppx[0] + 15 * k, ppx[1] + 15 * k, ppx[2] - 15 * k, red[2][1] + 1)
    dark = lambda h: h != "-" and all(int(h[i:i + 2], 16) < 0x60 for i in (1, 3, 5))
    items = [f for f in fl if dark(f[1]) and f[2][0] >= reg[0] and f[2][2] <= reg[2] and f[2][1] >= reg[1] and f[2][3] <= reg[3] and (f[2][2] - f[2][0]) < 0.9 * (ppx[2] - ppx[0])]
    sid = f"qld_w7-q01-{n}_layout"; bx = sym(vc, sid, [",".join(str(f[0]) for f in items)]); m = mm(bx, ppx, 1200)
    # distance text "NN m" as drawn
    t = [t for t in texts(vc, 1200) if "FHWA" in t[1] and t[0].endswith(" m")][0]
    tb = [(t[3][0] - ppx[0]) / k, (t[3][1] - ppx[1]) / k, (t[3][2] - ppx[0]) / k, (t[3][3] - ppx[1]) / k]
    midy = (tb[1] + tb[3]) / 2
    rr = runs(drawing, ppx, 1200, midy - 25, midy + 25, mingap=25, x0=tb[0] - 15, x1=tb[2] + 4, ink=notyel)
    mrun = rr[-1]; nrun = (rr[0][0], rr[-2][1])
    ry = rows(drawing, ppx, 1200, mrun[0] + 2, mrun[1] - 2, tb[1] + 10, tb[3] + 5, mingap=3, ink=black)
    ry = [r for r in ry if r[1] - r[0] > 40]; base = ry[0][1]; gap = mrun[0] - nrun[1]; slot = nrun[1] - nrun[0]
    dist = {"type": "text", "runs": [{"text": "{d}", "series": "D", "height": 100, "slot": round(slot, 1)}, {"text": "m", "series": "Emod", "height": 86.67}], "gap": round(gap, 1), "top": round(base - 100, 1), "align": "left", "x": round(nrun[0], 1)}
    # red panel
    r0 = 100
    def U(i): return f"M{i} {rt}H{1200 - i}V{H - r0}A{r0 - i} {r0 - i} 0 0 1 {1200 - r0} {H - i}H{r0}A{r0 - i} {r0 - i} 0 0 1 {i} {H - r0}Z"
    els = [{"type": "path", "d": U(0), "colour": "red"}, {"type": "path", "d": U(10), "colour": "white"}, {"type": "path", "d": U(20), "colour": "red"}, S(sid, *m), dist]
    gnote = []
    for txt, top in zip(tl, tops):
        ws = txt.split(" ")
        if len(ws) > 1:
            rw = runs(drawing, ppx, 1200, top + 10, top + 80, mingap=28, ink=white, x0=30, x1=1170); g = [round(v) for v in gaps(rw)]
            if len(g) != len(ws) - 1: print("  !! gaps", n, txt, rw)
            els.append(TW(ws, "D", 90, top, g, colour="white")); gnote.append(str(g))
        else: els.append(T(txt, "D", 90, top, colour="white"))
    print(n, H, rt, "symbol", m, "dist", dist["x"], dist["top"], slot, gap, "m run", mrun, "tops", tops, gnote)
    mk(f"W7-Q01-{n}", legend.replace(" ", "_") + "_{d}_M_" + kind + "_YELLOW_TALL", legend + " {d} m (" + what + ")", [1200, H], els,
       f"Q-series sheet W7-Q01_{n} railway level crossing short-stacking warning sign '{legend}' ({what}; 2023, page {n} of 7), fully dimensioned and drawn to scale, 1200 x {H}, R100. Upper part: yellow ground, yellow edge 10 + black border 10 (the sheet's 10 / 20); lower part from {rt} down: red with a white band 10 wide 10 in from the edge along the sides and bottom (the sheet's vectors), white legend 90 Series D. Right chain {chain}: legend cap top(s) {tops}; word gaps {', '.join(gnote) or 'n/a'} measured. "
       + ("DISAGREEMENT: the sheet labels the overall height 900 but its chain and drawing give 1100; 1100 generated. " if n == 2 else "") + ("'90DN' read as Series D. " if n == 7 else "") +
       f"Layout symbol (road, track, stacking arrows): the sheet PDF's own vector artwork (tools/symbols/{sid}.svg), placed as drawn: {m[2]} x {m[3]} at x {m[0]}, y {m[1]} (the sheet's chain dimensions describe this artwork). Distance: numeral 100 Series D in the dashed box ({slot:.0f} wide at x {nrun[0]:.0f}) and 'm' Series E modified lower case {gap:.0f} after it ('65Em' is the height of the lower-case m itself, drawn 64.8: cap height 86.67), baseline {base:.0f}, as drawn ('insert appropriate distance in metres e.g. {ex}'): {ex} and 10 / 20 / 30 / 40 generated (the owner: the variants that make sense, not every value). Black, red and white on retroreflective yellow.",
       panel_px=ppx, drawing=drawing, radius=100, vary={"key": "d", "values": [10, 20, 30, 40]}, drawn_value=ex, symbols=symentry(sid, drawing, f"road / railway layout with stacking-distance arrows ({what}), vector items of the sheet PDF"), **YB(10, 10))
