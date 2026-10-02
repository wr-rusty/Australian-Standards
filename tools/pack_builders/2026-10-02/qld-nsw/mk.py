"""mk.py — draft a spec from a TraSiCAD plan (live text + vectors). Hand-check afterwards.
usage: mk.py CODE ground NAME [--which n] [--box x0 y0 x1 y1] [--keep-text-from-spec] [--write]"""
import sys, os, re, json, math
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, 'tools')
import tsc, trace_symbol as T
from PIL import Image
from shapely.geometry import Point, Polygon, box as sbox
from shapely.ops import unary_union
NAMES = {'blue': '#3a53a4', 'red': '#ed1c24', 'white': '#ffffff', 'black': '#000000', 'yellow': '#ffe40d', 'green': '#0b804c', 'orange': '#f58020', 'brown': '#754c24'}
def cname(h):
    if h is None: return None
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    if max(r, g, b) < 70: return 'black'
    if min(r, g, b) > 225: return 'white'
    if b > 120 and r < 110 and g < 110: return 'blue'
    if r > 180 and g < 90 and b < 90: return 'red'
    if r > 200 and g > 180 and b < 120: return 'yellow'
    if r > 200 and 90 <= g <= 180 and b < 90: return 'orange'
    if g > 90 and r < 90 and b < 120: return 'green'
    if r > 90 and g < 110 and b < 80: return 'brown'
    return h
def poly_d(g):
    out = []
    for p in ([g] if g.geom_type == 'Polygon' else list(g.geoms)):
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)[:-1]; out.append('M' + 'L'.join('%.2f %.2f' % (x, y) for x, y in c) + 'Z')
    return ''.join(out)
def title(texts):
    val = {}
    for lab in ('Size:', 'Border:', 'Cnr Rad:', 'Patch CR:', 'Scale:'):
        ls = [t for t in texts if t['text'].strip() == lab]
        if not ls: continue
        l = ls[0]; c = [t for t in texts if abs(t['origin'][1] - l['origin'][1]) < 3 and t['origin'][0] > l['origin'][0] + 1 and not t['text'].strip().endswith(':')]
        c.sort(key=lambda t: t['origin'][0])
        if c: val[lab] = c[0]['text'].strip()
    return val
def legend_table(texts):
    rows = []
    for t in texts:
        if t['text'].startswith('FHWA Series'):
            same = sorted([u for u in texts if abs(u['origin'][1] - t['origin'][1]) < 3], key=lambda u: u['origin'][0])
            rows.append((same[0]['text'].strip(), t['text'].strip(), same[-1]['text'].strip()))
    return rows
def draft(code, ground, name, which=0, box=None):
    img = Image.open(f'Processing/Australia/NSW/Original PNGs/{code}.png').convert('RGB')
    page, _ = tsc.load(code)
    sh0 = tsc.Sheet(code, [0, 0, 1, 1], 1); tx0 = tsc.texts(sh0); tb = title(tx0)
    m = re.match(r'(\d+) x (\d+)', tb.get('Size:', ''))
    H, W = (int(m.group(1)), int(m.group(2)))
    if box is None: box = T.find_white_panel(img, which, True) if ground == 'white' else T.find_panel(img, ground, which, True)
    sh = tsc.Sheet(code, box, W); fs = tsc.fills(sh, margin=8); tx = tsc.texts(sh)
    bm = re.match(r'([\d.]+) x ([\d.]+)', tb.get('Border:', '')); e, b = (float(bm.group(1)), float(bm.group(2))) if bm else (0, 0)
    try: R = float(tb.get('Cnr Rad:', '0'))
    except ValueError: R = 0
    info = {'box': [round(v) for v in box], 'H_px_mm': round(sh.H, 1), 'title': tb, 'legend': legend_table(tx)}
    return sh, fs, tx, W, H, e, b, R, info
def circles(fs, colour):
    out = []
    for f in fs:
        x0, y0, x1, y1 = f['bbox']; w, h = x1 - x0, y1 - y0
        if cname(f['fill']) == colour and w > 4 and abs(w - h) < 0.03 * max(w, h) + 0.6 and 'L' not in f['d']: out.append(((x0 + x1) / 2, (y0 + y1) / 2, (w + h) / 4, f))
    return out
def text_elements(sh, tx, legend):
    els = []
    for t in tx:
        if t['font'].startswith('Arial'): continue
        if not (-5 < t['origin'][0] < sh.W + 5 and -5 < t['origin'][1] < sh.H + 5): continue
        ms = re.search(r'Series(Em|[B-F])', t['font']); s = ms.group(1) if ms else None
        txt = t['text'].strip(); h = None
        for lg, font, size in legend:
            if lg == txt or txt in lg.split() or lg in txt:
                if s is None: s = re.search(r'Series (Em|[B-F])', font).group(1)
                try: h = float(size)
                except ValueError: pass
                if lg == txt: break
        s = 'Emod' if s == 'Em' else s
        if h is None: h = round(t['size_mm'] * 0.7246, 0)   # cap height / em of the FHWA 2000EX fonts as embedded (checked against legend tables)
        import signgen as G
        fc = G.face(s); raw = t['text']; words = []; i = 0
        for mw in re.finditer(r'\S+', raw):
            wd = mw.group(0); _, _, l, r_ = fc.layout(wd); left = t['cx'][mw.start()] + l * h / G.CAP; words.append((wd, left, (r_ - l) * h / G.CAP))
        if len(words) == 1:
            el = {'type': 'text', 'text': words[0][0], 'series': s, 'height': h, 'top': round(t['origin'][1] - h, 1), 'cx': round(words[0][1] + words[0][2] / 2, 1)}
        else:
            gaps = [round(words[i + 1][1] - words[i][1] - words[i][2], 1) for i in range(len(words) - 1)]
            el = {'type': 'text', 'words': [w[0] for w in words], 'gap': gaps, 'series': s, 'height': h, 'top': round(t['origin'][1] - h, 1), 'cx': round((words[0][1] + words[-1][1] + words[-1][2]) / 2, 1)}
        el['text_'] = txt
        c = cname(t['col'])
        if c != 'black': el['colour'] = c
        el['_adv'] = t['x']; els.append(el)
    els.sort(key=lambda e: (e['top'], e['cx']))
    return els
if __name__ == '__main__':
    a = sys.argv; code, ground, name = a[1], a[2], a[3]
    which = int(a[a.index('--which') + 1]) if '--which' in a else 0
    box = [float(v) for v in a[a.index('--box') + 1:a.index('--box') + 5]] if '--box' in a else None
    sh, fs, tx, W, H, e, b, R, info = draft(code, ground, name, which, box)
    print(json.dumps(info)); print('e', e, 'b', b, 'R', R, 'size', W, H)
    cs = circles(fs, ground); els = []; rect = '--rect' in a
    bc0 = a[a.index('--border-colour') + 1] if '--border-colour' in a else ('white' if ground in ('blue', 'red', 'green', 'brown', 'black') else 'black')
    hull = unary_union([Point(x, y).buffer(r, 64) for x, y, r, _ in cs]).convex_hull if len(cs) >= 3 else sbox(0, 0, W, H)
    print('circles', [(round(x, 1), round(y, 1), round(r, 1)) for x, y, r, _ in cs], 'hull bounds', [round(v, 1) for v in hull.bounds])
    # snap the hull to the stated size
    hb = hull.bounds
    from shapely import affinity
    hull = affinity.translate(hull, -hb[0], -hb[1]); hull = affinity.scale(hull, W / (hb[2] - hb[0]), H / (hb[3] - hb[1]), origin=(0, 0))
    els.append({'type': 'path', 'd': poly_d(hull), 'colour': ground if not ('--edge-colour' in a) else a[a.index('--edge-colour') + 1]})
    inner = hull
    if b > 0:
        mid = hull.buffer(-e, join_style=2) if e else hull; inner = mid.buffer(-b, join_style=2)
        bc = a[a.index('--border-colour') + 1] if '--border-colour' in a else ('white' if ground in ('blue', 'red', 'green', 'brown', 'black') else 'black')
        els.append({'type': 'path', 'd': poly_d(mid.difference(inner)), 'colour': bc, 'fill_rule': 'evenodd'})
    if rect:
        els = []; inner = sbox(e + b, e + b, W - e - b, H - e - b)
    tol = inner.buffer(0.8)
    for f in fs:
        if f['fill'] is None: continue
        x0, y0, x1, y1 = f['bbox']; c = cname(f['fill'])
        nums = [float(v) for v in re.findall(r'-?[\d.]+', f['d'])]; pts = list(zip(nums[0::2], nums[1::2]))
        if not all(tol.contains(Point(p)) for p in pts): continue
        if c == ground and any(abs((x0 + x1) / 2 - cx) < 1 and abs((y0 + y1) / 2 - cy) < 1 for cx, cy, r, _ in cs): continue
        if c == ground and (x1 - x0) * (y1 - y0) > 0.8 * W * H: continue
        if rect and c in (ground, bc0) and (x1 - x0) > 0.9 * (W - 2 * e - 2 * b) and (y1 - y0) > 0.9 * (H - 2 * e - 2 * b): continue
        el = {'type': 'path', 'd': f['d'], 'colour': c}
        if f['eo'] and f['d'].count('M') > 1: el['fill_rule'] = 'evenodd'
        els.append(el)
    tel = text_elements(sh, tx, info['legend'])
    for t in tel: print('TEXT', t)
    tel = [t for t in tel if t['text_'] != '.']
    nart = len(els) - (0 if rect else 2 if b > 0 else 1)
    tips = [c for c in cs if c[2] < 8]; big = sorted(set(round(c[2]) for c in cs if c[2] >= 8), reverse=True)
    tb = info['title']
    notes = (f"TfNSW plan {tsc.REG[code]['local'].split('/')[-1]} (TraSiCAD sheet {tb.get('Scale:', '')}, live text and vector paths). Size '{tb.get('Size:')}' (H x W), Cnr Rad {tb.get('Cnr Rad:')}, "
             f"Border '{tb.get('Border:')}' = {ground} edge {e:g} + {bc0} border {b:g}. ")
    if tips: notes += f"Pointed sign, so the ground is 'none' and the outline is drawn as paths: the convex hull of the plan's own corner circles (radius {big[0] if big else 0} at the corners and shoulders, tip radius 5 at x {tips[0][0]:.0f}, shoulders at x {sorted(c[0] for c in cs if c[2] >= 8)[0 if tips[0][0] < W / 2 else -1]:.0f}), the border band inset {e:g} to {e + b:g} from it (mitred at the tip); transparent outside. "
    elif len(cs) >= 3: notes += "Outline: the plan's own rounded outline (hull of its corner circles), border band inset from it. "
    notes += "Legend table: " + '; '.join(f"{l}: {f} {z}" for l, f, z in info['legend']) + ". " if info['legend'] else ''
    for t in tel:
        notes += f"{t['text_']} {t['height']:g} {t['series']} top {t['top']} centred {t['cx']} (the plan's live-text position; words start at the plan's character origins" + (f", word gap {t['gap']}" if t.get('gap') else '') + "). "
    if nart: notes += f"Symbols and chevron: {nart} filled paths taken from the sheet's own vector artwork. "
    for t in tel: t.pop('_adv'); els.append(t)
    spec = {'code': code, 'pack': 'NSW', 'name': name, 'legend': ' '.join(t.pop('text_') for t in tel), 'shape': 'rect', 'size': [W, H], 'radius': 0, 'ground': 'none',
            'panel_px': info['box'], 'elements': els, 'notes': notes + (a[a.index('--note') + 1] if '--note' in a else '')}
    print(len(els), 'elements')
    if rect:
        spec.update({'radius': R, 'ground': ground})
        if e > 0: spec['edge'] = {'colour': ground, 'width': e}
        if b > 0: spec['border'] = {'colour': bc0, 'width': b}
        spec = {k: spec[k] for k in ('code', 'pack', 'name', 'legend', 'shape', 'size', 'radius', 'ground', 'edge', 'border', 'panel_px', 'elements', 'notes') if k in spec}
    if '--write' in a:
        json.dump(spec, open(f'tools/specs/NSW/{code}.json', 'w'), indent=1); print('written')

import numpy as _np
_pxcache={}
def px(code, vbox, dpi=600):
    """panel_px (200-dpi px) from an approximate box read off the 1413-wide view (x1.17), snapped to the drawn outline"""
    import meas, h
    box=[v*1653/1413 for v in vbox]
    a=_np.asarray(h.page_img(code,dpi)); f=dpi/200
    (X0,Y0,X1,Y1),oks=meas.refine(a,box,f)
    r=[X0/f,Y0/f,X1/f,Y1/f]
    if not all(oks): print("  px",code,"not snapped:",oks,[round(v) for v in r])
    return r
def gen(codes=None):
    import subprocess
    ps=WRITTEN if codes is None else [f"{ROOT}/tools/specs/SA/{c}.json" for c in codes]
    r=subprocess.run([sys.executable, ROOT+"/tools/signgen.py"]+ps,capture_output=True,text=True,cwd=ROOT); print(r.stdout[-3000:], r.stderr[-2000:])
