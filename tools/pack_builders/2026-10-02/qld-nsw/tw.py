import sys, json; sys.path.insert(0,'tools'); import signgen as G
def widths(spec):
    for el in spec['elements']:
        if el['type'] != 'text': continue
        runs = el.get('runs') or [{'text': w} for w in el.get('words', [el.get('text')])]
        ws = [G.face(G.series_for({'series': r.get('series', el.get('series'))}, r['text'])).ink_width(r['text'], r.get('height', el.get('height'))) for r in runs]
        gap = el.get('gap', 0); gaps = gap if isinstance(gap, list) else [gap] * (len(runs) - 1)
        tot = sum(ws) + sum(gaps); cx = el.get('cx', spec['size'][0] / 2)
        left = cx - tot / 2 if el.get('align', 'center') == 'center' else el['x']
        print(' '.join(r['text'] for r in runs), 'top', el['top'], 'w', [round(w, 1) for w in ws], 'total', round(tot, 1), 'left', round(left, 1), 'right', round(left + tot, 1))
for c in sys.argv[1:]:
    print(c); widths(json.load(open(f'tools/specs/NSW/{c}.json')))
