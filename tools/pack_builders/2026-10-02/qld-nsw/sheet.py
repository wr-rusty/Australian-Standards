"""sheet.py CODE [ymax_px] — live text (px bbox at 200 dpi, size) and filled vectors of a sheet page, title block left out."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vec, pymupdf
K = vec.K
def dump(code, ymax=1880, minv=14):
    page = vec.page_for(code); M = page.rotation_matrix
    print("page px", round(page.rect.width * K), round(page.rect.height * K), "rot", page.rotation)
    lines = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = " ".join(sp["text"].strip() for sp in l["spans"] if sp["text"].strip())
            if not t: continue
            r = pymupdf.Rect(l["bbox"]) * M; r.normalize()
            if r.y0 * K > ymax: continue
            lines.append((round(r.y0 * K), round(r.x0 * K), round(r.x1 * K), round(r.y1 * K), round(l["spans"][0]["size"] * K, 1), l["spans"][0]["font"][:14], t, l["dir"]))
    lines.sort()
    # merge same-row short tokens (tables) into rows
    rows = []
    for ln in lines:
        if rows and abs(rows[-1][0][0] - ln[0]) <= 6 and len(ln[6]) < 40: rows[-1].append(ln)
        else: rows.append([ln])
    for r in rows:
        r.sort(key=lambda l: l[1])
        if len(r) == 1 and (r[0][5].startswith("Arial") and len(r[0][6]) > 28 or r[0][6] in ("Notes:", "Colour Legend", "Note:")): continue
        if len(r) == 1:
            y0, x0, x1, y1, sz, font, t, d = r[0]; print(f"T [{x0} {y0} {x1} {y1}] s{sz} {font}{'' if abs(d[0]) > 0.9 else ' dir' + str(tuple(round(v, 2) for v in d))}: {t}")
        else: print(f"R y{r[0][0]} x{r[0][1]} s{r[0][4]}: " + " | ".join(l[6] for l in r))
    for i, d in enumerate(page.get_drawings()):
        r = d["rect"] * M; r.normalize()
        if "f" not in d["type"] or max(r.width, r.height) * K < minv or r.y0 * K > ymax or min(r.width, r.height) * K < 7.5: continue
        fc = vec.hexc(d.get("fill"))
        if d["type"] == "f" and len(d["items"]) == 3 and max(r.width, r.height) * K < 16: continue   # arrowheads
        print(f"V{i} {d['type']} {fc} [{r.x0 * K:.1f} {r.y0 * K:.1f} {r.x1 * K:.1f} {r.y1 * K:.1f}] n{len(d['items'])}{' eo' if d.get('even_odd') else ''}")
if __name__ == "__main__": dump(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 1880)
