#!/usr/bin/env python3
"""lint_specs.py — flag transcription slips the width check cannot see.
For every spec: text elements placed with align left/right are grouped by `top`; the group's
left and right margins (from the panel edges) are compared. Unequal margins (> 6 mm) on a line
that the drawing centres are the classic 'x typo' (e.g. 374 for 474). Also flags gaps < 15 mm
between neighbouring words and symbol boxes outside the panel."""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import signgen as G
ROOT = G.ROOT
def main(pattern):
    for sp in sorted(glob.glob(pattern, recursive=True)):
        spec = json.load(open(sp))
        if spec.get("skip"): continue
        W, H = spec["size"]; lines = {}
        for el in spec.get("elements", []):
            if el.get("type") == "symbol":
                if el["x"] < 0 or el["y"] < 0 or el["x"] + el["w"] > W + 0.5 or el["y"] + el["h"] > H + 0.5:
                    print(f"{spec['code']}: symbol {el['id']} box outside panel")
            if el.get("type") != "text" or el.get("align", "center") == "center": continue
            text = el.get("text") or " ".join(el.get("words", [])) or " ".join(r["text"] for r in el.get("runs", []))
            try:
                fc = G.face(G.series_for(el, text), el.get("tracking", "plus0")); w = fc.ink_width(text.format(**{k: v for k, v in [("speed", 60), ("km", 2), ("m", 300), ("n", 6), ("t", 5)]}), el["height"])
            except Exception as e:
                w = el.get("expect") or 0
            if isinstance(w, list): w = w[0] or 0
            x0 = el["x"] if el["align"] == "left" else el["x"] - w
            lines.setdefault(el["top"], []).append((x0, x0 + w, text))
        for top, words in lines.items():
            words.sort(); left = words[0][0]; right = W - words[-1][1]
            gaps = [words[i + 1][0] - words[i][1] for i in range(len(words) - 1)]
            flags = []
            if len(words) > 1 and any(g < 15 for g in gaps): flags.append(f"gap {[round(g) for g in gaps]}")
            if abs(left - right) > 6 and not any(k in json.dumps(spec).lower() for k in ("off-centre", "offcentre", "off centre", "left-aligned", "left aligned", "column")):
                flags.append(f"margins L {left:.0f} / R {right:.0f}")
            if flags: print(f"{spec['code']} top {top}: {' | '.join(t for _, _, t in words)} -> {'; '.join(flags)}")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "tools", "specs", "**", "*.json"))
