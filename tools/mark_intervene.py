#!/usr/bin/env python3
"""mark_intervene.py — read every tools/specs/*/_QA_REPORT.md, and set "intervene": "<reason>" on each
spec whose line is an ISSUE (or clear it when the line is OK/FIXED). Run before signgen.py so those signs
land in Processed/intervene/."""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
issues = {}; cleared = 0
for rep in glob.glob(os.path.join(ROOT, "tools", "specs", "*", "_QA_REPORT*.md")):
    for line in open(rep):
        m = re.match(r"\s*[-*|]?\s*`?([A-Z][A-Za-z0-9]*(?:-[0-9A-Za-z]+)*(?:\([^)]*\))?)`?\s*[—\-–:|]+\s*(.*)", line)
        if not m: continue
        code, rest = m.group(1), m.group(2).strip()
        up = rest.upper()
        if up.startswith("ISSUE"): issues[code] = re.sub(r"^ISSUE\s*[—\-–:(]*\s*", "", rest).strip(" )")
        elif "ISSUE" in up and (up.startswith("FIXED") or up.startswith("OK")):
            issues[code] = rest[rest.upper().index("ISSUE"):].lstrip("ISSUE").strip(" —-–:()")
for sp in glob.glob(os.path.join(ROOT, "tools", "specs", "**", "*.json"), recursive=True):
    spec = json.load(open(sp)); code = spec.get("code")
    if code in issues:
        spec["intervene"] = issues[code][:300]
    elif "intervene" in spec:
        del spec["intervene"]; cleared += 1
    else: continue
    json.dump(spec, open(sp, "w"), indent=1)
print(f"marked {len(issues)} specs for intervention, cleared {cleared}")
for c, r in sorted(issues.items()): print(f"  {c}: {r[:110]}")
