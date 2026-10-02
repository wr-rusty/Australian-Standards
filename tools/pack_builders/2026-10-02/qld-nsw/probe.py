import sys,glob,json,os
sys.path.insert(0,'tools'); import signgen as G
bad=[]; n=0; fams={}
for sp in sorted(glob.glob('tools/specs/NSW/*.json')):
    spec=json.load(open(sp))
    if spec.get('skip'): continue
    try:
        for values,hand,fname in G.expand(spec):
            svg,checks,flags=G.build(spec,values,hand)
            p=os.path.join(G.out_root(spec),G.folder_for(spec),fname)
            st='same' if os.path.exists(p) and open(p).read()==svg else ('DIFF' if os.path.exists(p) else 'NEW')
            fams.setdefault((G.folder_for(spec),st),[]).append(spec['code'])
    except Exception as ex: bad.append((spec['code'],repr(ex)[:150]))
for k,v in sorted(fams.items()): print(k,len(v), v if k[1]!='same' else '')
print(bad)
