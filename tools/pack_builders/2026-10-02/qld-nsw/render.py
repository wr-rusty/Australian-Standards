"""render.py CODE... : render TC sheets (all pages) upright at 200 dpi into the QLD Original PNGs folder (TC1234.png, TC1234_p2.png ...)"""
import sys, os, glob, re, pymupdf
ROOT = "/Users/USER/Local/GitHub/Australian-Standards/Processing/Australia/QLD/"
allpdf = [f for f in glob.glob(ROOT + "Original PDFs/TC signs/**/*.pdf", recursive=True) if "/Superseded/" not in f]
def find(code):
    num = code[2:]
    c = [f for f in allpdf if re.fullmatch(r"tc" + num + r"(\D.*)?\.pdf", os.path.basename(f).lower())]
    return sorted(c, key=len)[0] if c else None
if __name__ == "__main__":
    for code in sys.argv[1:]:
        f = find(code)
        if not f: print(code, "NO PDF"); continue
        doc = pymupdf.open(f)
        for i, pg in enumerate(doc):
            out = ROOT + "Original PNGs/" + code + ("" if i == 0 else f"_p{i + 1}") + ".png"
            if not os.path.exists(out): pg.get_pixmap(dpi=200, alpha=False).save(out)
        print(code, len(doc), os.path.relpath(f, ROOT + "Original PDFs/TC signs/TC Signs_June 2026"))
