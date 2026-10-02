import csv,json,glob,collections,os,sys
rows=list(csv.DictReader(open("Processing/Australia/NSW/SVGs/MANIFEST.csv")))
specs={}
for s in glob.glob("tools/specs/NSW/*.json"):
    j=json.load(open(s)); specs[j['code'].lower()]=j
    if j.get('drawing'): specs.setdefault(j['drawing'].lower(),j)
def norm(c): return c.lower().replace(' ','')
fam=collections.defaultdict(lambda: collections.defaultdict(list))
for r in rows:
    if not r['file']: continue
    code=r['code']; base=code.split('(')[0]
    j=specs.get(code.lower()) or specs.get(base.lower())
    st='nospec' if j is None else ('skip' if j.get('skip') else 'built')
    fam[r['family']][st].append(code)
for f,d in fam.items():
    print(f,{k:len(v) for k,v in d.items()})
    if f not in('Guide Signs','Freeway Signs'): print('   nospec:',d['nospec'])
