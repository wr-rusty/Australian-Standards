import json
def load(code): return json.load(open(f"tools/specs/QLD/{code}.json"))
def save(s, fn=None):
    with open(f"tools/specs/QLD/{fn or s['code']}.json","w") as fh: json.dump(s, fh, indent=1, ensure_ascii=False); fh.write("\n")
