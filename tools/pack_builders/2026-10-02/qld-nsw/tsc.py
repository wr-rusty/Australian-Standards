"""tsc.py — reading aid for TfNSW plan PDFs: vectors and live text of a sign, in sign mm.
usage: tsc.py CODE x0 y0 x1 y1 W_mm [--paths] [--svg out.svg] ; box = sign outline in the 200-dpi PNG px"""
import sys, os, csv, json, math
sys.path.insert(0, 'tools')
import pymupdf, trace_symbol as T
from PIL import Image
NSW = 'Processing/Australia/NSW'
REG = {r['sign_no'].strip().rstrip('-').strip(): r for r in csv.DictReader(open(NSW + '/REGISTER.csv')) if r.get('local')}
def load(code):
    r = REG[code]; page = pymupdf.open(os.path.join(NSW, r['local']))[0]
    png = Image.open(f'{NSW}/Original PNGs/{code}.png'); pw, ph = png.size
    best = None
    for turn in (T.sheet_turn(page), 0, 90, -90):
        M = page.rotation_matrix * pymupdf.Matrix(200 / 72, 200 / 72) * pymupdf.Matrix(turn)
        q = pymupdf.Rect(page.mediabox) ; pts = [pymupdf.Point(x, y) * M for x in (q.x0, q.x1) for y in (q.y0, q.y1)]
        ox = min(p.x for p in pts); oy = min(p.y for p in pts); w = max(p.x for p in pts) - ox; h = max(p.y for p in pts) - oy
        if abs(w - pw) < 3 and abs(h - ph) < 3: best = (M, ox, oy); break
    if not best: raise SystemExit('no turn matches png size')
    return page, best
class Sheet:
    def __init__(self, code, box, W):
        self.page, (self.M, self.ox, self.oy) = load(code); self.box = box; self.k = W / (box[2] - box[0]); self.W = W; self.H = (box[3] - box[1]) * self.k
        # does get_drawings give unrotated coords? derotation_matrix maps rotated->unrotated; drawings are in rotated space in pymupdf
        self.D = pymupdf.Matrix(200 / 72, 200 / 72) * self.extra()
    def extra(self):
        # extra turn applied after page rotation
        R = self.page.rotation_matrix; Rinv = pymupdf.Matrix(R); Rinv.invert()
        return pymupdf.Matrix(72 / 200, 72 / 200) * Rinv * self.M if False else self._turn()
    def _turn(self):
        R = pymupdf.Matrix(self.page.rotation_matrix); R.invert()
        S = pymupdf.Matrix(72 / 200, 72 / 200)
        return S * (R * self.M)
    def _turn_only(self):
        R = pymupdf.Matrix(self.page.rotation_matrix); R.invert()
        T_ = R * self.M * pymupdf.Matrix(72 / 200, 72 / 200)
        return pymupdf.Matrix(T_.a, T_.b, T_.c, T_.d, 0, 0)
    def mm_from_rot(self, p):      # p in rotated-page coords (drawings)
        q = pymupdf.Point(p) * self.D
        return ((q.x - self.ox - self.box[0]) * self.k, (q.y - self.oy - self.box[1]) * self.k)
    def mm_from_unrot(self, p):    # p in unrotated coords (text)
        q = pymupdf.Point(p) * self.M
        return ((q.x - self.ox - self.box[0]) * self.k, (q.y - self.oy - self.box[1]) * self.k)
def hexcol(c):
    return None if c is None else '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in c)
def path_d(sh, items, conv):
    d = []; cur = None; f = lambda p: '%.2f %.2f' % conv(p)
    for it in items:
        if it[0] == 'l':
            if cur is None or abs(it[1].x - cur.x) > 1e-3 or abs(it[1].y - cur.y) > 1e-3: d.append('M' + f(it[1]))
            d.append('L' + f(it[2])); cur = it[2]
        elif it[0] == 'c':
            if cur is None or abs(it[1].x - cur.x) > 1e-3 or abs(it[1].y - cur.y) > 1e-3: d.append('M' + f(it[1]))
            d.append('C' + f(it[2]) + ' ' + f(it[3]) + ' ' + f(it[4])); cur = it[4]
        elif it[0] == 're':
            r = it[1]; d.append('M' + f(r.tl) + 'L' + f(r.tr) + 'L' + f(r.br) + 'L' + f(r.bl) + 'Z'); cur = None
        elif it[0] == 'qu':
            q = it[1]; d.append('M' + f(q.ul) + 'L' + f(q.ur) + 'L' + f(q.lr) + 'L' + f(q.ll) + 'Z'); cur = None
    s = ''.join(d)
    return s if s.endswith('Z') else s + 'Z'
def fills(sh, margin=5):
    out = []
    for dr in sh.page.get_drawings():
        if dr.get('fill') is None and not (dr.get('color') is not None and dr.get('width', 0) and dr['width'] * sh.k * 200 / 72 > 4): continue
        r = dr['rect']; a = sh.mm_from_unrot(r.tl); b = sh.mm_from_unrot(r.br); c = sh.mm_from_unrot(r.tr); e = sh.mm_from_unrot(r.bl)
        xs = [a[0], b[0], c[0], e[0]]; ys = [a[1], b[1], c[1], e[1]]; bb = (min(xs), min(ys), max(xs), max(ys))
        if bb[0] < -margin or bb[1] < -margin or bb[2] > sh.W + margin or bb[3] > sh.H + margin: continue
        out.append({'bbox': [round(v, 1) for v in bb], 'fill': hexcol(dr.get('fill')), 'stroke': hexcol(dr.get('color')) if dr.get('fill') is None else None,
                    'sw': round((dr.get('width') or 0) * sh.k * 200 / 72, 1), 'eo': dr.get('even_odd'), 'd': path_d(sh, dr["items"], sh.mm_from_unrot)})
    return out
def texts(sh, margin=400):
    out = []
    for b in sh.page.get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            for sp in l['spans']:
                sp['text'] = ''.join(c['c'] for c in sp['chars'])
                if not sp['text'].strip(): continue
                o = sh.mm_from_unrot(sp['origin']); r = pymupdf.Rect(sp['bbox']); a = sh.mm_from_unrot(r.tl); c = sh.mm_from_unrot(r.br)
                out.append({'text': sp['text'], 'font': sp['font'], 'size_mm': round(sp['size'] * sh.k * 200 / 72, 1), 'origin': [round(o[0], 1), round(o[1], 1)],
                            'x': sorted([round(a[0], 1), round(c[0], 1)]), 'y': sorted([round(a[1], 1), round(c[1], 1)]), 'col': '#%06x' % sp['color'], 'cx': [round(sh.mm_from_unrot(c['origin'])[0], 1) for c in sp['chars']]})
    return out
if __name__ == '__main__':
    code = sys.argv[1]; box = [float(v) for v in sys.argv[2:6]]; W = float(sys.argv[6]); sh = Sheet(code, box, W)
    print('size mm %.1f x %.1f  k=%.4f mm/px' % (sh.W, sh.H, sh.k))
    fs = fills(sh)
    for t in texts(sh):
        if '--all' not in sys.argv and (t['origin'][0] < -350 or t['origin'][0] > sh.W + 350 or t['origin'][1] < -350 or t['origin'][1] > sh.H + 350): continue
        inside = -20 < t['origin'][0] < sh.W + 20 and -20 < t['origin'][1] < sh.H + 20
        print(('IN  ' if inside else 'out ') + json.dumps(t))
    for i, f in enumerate(fs):
        print(i, f['bbox'], f['fill'], f['stroke'], f['sw'], 'eo' if f['eo'] else '', (f['d'] if '--paths' in sys.argv else f['d'][:60]))
    if '--svg' in sys.argv:
        o = sys.argv[sys.argv.index('--svg') + 1]
        with open(o, 'w') as fh:
            fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sh.W:.1f} {sh.H:.1f}" width="{sh.W:.0f}" height="{sh.H:.0f}">')
            for f in fs:
                if f['fill']: fh.write(f'<path d="{f["d"]}" fill="{f["fill"]}"' + (' fill-rule="evenodd"' if f['eo'] else '') + '/>')
                else: fh.write(f'<path d="{f["d"]}" fill="none" stroke="{f["stroke"]}" stroke-width="{f["sw"]}"/>')
            fh.write('</svg>')
