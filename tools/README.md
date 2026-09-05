# tools

Pipeline that turns the AS 1743-2023 drawings into SVGs under `AS 1743-2023/Processed/`.

```bash
python3 -m venv .venv && .venv/bin/pip install fonttools pillow   # once; potrace via `brew install potrace`
.venv/bin/python tools/trace_symbol.py --spec 'tools/specs/*/*.json'   # symbols from the drawings -> tools/symbols/
.venv/bin/python tools/mark_intervene.py                                # QA reports -> "intervene" fields on specs
.venv/bin/python tools/signgen.py                                       # all specs -> Processed/ (+ MANIFEST.csv)
.venv/bin/python tools/contact_sheets.py 'tools/specs/TM/*.json' /tmp/sheets   # review sheets: drawing | generated
.venv/bin/python tools/lint_specs.py 'tools/specs/[TRW]*/*.json'        # margin/gap sanity check on hand-placed text
```

| File | Role |
|---|---|
| `SPEC_GUIDE.md` | The spec format and the rules for transcribing a drawing. Read before writing or editing specs. |
| `specs/<FAMILY>/<CODE>.json` | One spec per drawing (TM, T, R, W, G, GE, MISC). `_REPORT_*.md` = transcription notes, `_QA_REPORT.md` = review results. |
| `signgen.py` | Generator. Outlines text from the FHWA fonts with AS 1744 spacing (hyphen re-spaced per the table), builds shapes, places symbols, checks stated widths (±2 %), writes `MANIFEST.csv`. |
| `trace_symbol.py` | Traces a symbol from a drawing: finds the sign's ground by colour (or the black ring on white signs), maps the spec's mm box, masks to the ground shape, upsamples, potrace, per-colour layers if asked. Options per symbol entry are listed in the guide. |
| `symbols/<id>.svg` | Traced symbol artwork in mm (viewBox = ink extent). Fill `currentColor` unless the symbol carries its own colours. |
| `contact_sheets.py` | Renders each sign beside its drawing for visual review. |
| `lint_specs.py` | Flags left-aligned lines with unequal margins or tiny gaps (catches x typos the width check cannot). |
| `mark_intervene.py` | Reads the QA reports; every `CODE — ISSUE (...)` line sets `"intervene"` on that spec. |

## Output layout (`AS 1743-2023/Processed/`)

Family folders: Regulatory Signs, Parking Signs (R5), Speed Signs/…, Warning Signs, Temporary Signs, Guide Signs,
Service Signs (G7), Tourist Signs (G11, TRA/TRB), Freeway Signs (GE), Hazard Markers (D4). Filenames are
`<NAME>_<CODE>[(L|R)].svg` in the style of the older `SVGs/` folder.

`intervene/<family>/` holds every sign that needs a human decision: a QA ISSUE, or a stated width the fonts
cannot reproduce. The reason is in `MANIFEST.csv` (`intervene` column) and in the spec's `notes`.

SVG header matches the Illustrator speed-sign exports (`width`/`height` in mm at 72 pt/in, viewBox in points,
1 pt = 1 cm of drawn sign). No comments or metadata are written into the SVGs.

## Conventions
* One file per drawing at the illustrated size; variants only for values the drawing marks as varying (speeds,
  distances, channels) and for (L)/(R). No size-table variants.
* Nothing not on the drawing is added. Drawing dimensions that contradict AS 1744 spacing are kept as `expect`,
  flagged by the width check, explained in `notes`, and routed to `intervene`.
* Templates in `Design Templates/` supply the base geometry; their hairline keyline and `minus10` numeral tracking
  are off by default (`"keyline": true`, `"tracking": "minus10"` to enable).
