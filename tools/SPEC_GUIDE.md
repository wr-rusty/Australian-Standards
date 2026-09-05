# Writing sign specs (tools/specs/<FAMILY>/<CODE>.json)

These are official road signs. Every number in a spec must come from the AS 1743 drawing
(`Australia/National (AS 1743)/Original PNGs/<CODE>.png`). Never estimate a dimension by eye when the
drawing states it; never invent an element the drawing does not show. If something is
unclear, write it in `notes` and keep going.

## One spec per drawing
* `code`: the drawing code exactly as in the PNG filename minus `.png` (e.g. `TM2-4A`, `W1-1(R)(L)` -> use `W1-1` with `hands`).
* `size`: `[width, height]` in mm of the **illustrated** size (the one marked "Illust." when a
  size table exists). Ignore the other sizes in the table.
* `name`: filename stem in Russell's style — UPPERCASE words joined by `_`: legend words, then colour
  (`YELLOW` / `WHITE` / `RED` / `ORANGE` / `GREEN` / `BLUE` / `BROWN`), then shape word:
  `SQUARE` (1:1), `LONG` (2:1), `LONG_SKINNY` (4:1), `WIDE` (3:1), `WIDE_SKINNY` (6:1), `TALL` (portrait),
  `DIAMOND`, `ROUND`. Examples: `ROADWORK_YELLOW_SQUARE`, `ROAD_CLOSED_WHITE_LONG_SKINNY`, `STOP_SIGN`,
  `GIVE_WAY`, `NO_ENTRY`, `FERRY_YELLOW_DIAMOND`, `SLIPPERY_YELLOW_SQUARE`. Keep it under ~45 chars.
  Symbol-only signs: describe the symbol (`LEFT_CURVE_YELLOW_DIAMOND`). The generator appends `_<CODE>`.
* `folder`: usually omit — the generator files each sign by family (Regulatory Signs, Parking Signs, Warning Signs, Temporary
  Signs, Guide Signs, Service Signs, Tourist Signs, Freeway Signs, Hazard Markers). Speed signs set it explicitly:
  `"Speed Signs/Normal Speed Signs"`, `"Speed Signs/Area"`, `"Speed Signs/End"`.
* `legend`: the words on the sign, for the manifest.
* `notes`: anything you had to decide, and any drawing dimension that disagrees with the AS 1744 arithmetic.

## Panel
* `shape`: `rect` | `octagon` | `triangle` (point down, `size` = [sharp width, height]) | `diamond` (`size` = [s*1.41421, s*1.41421] for side s) | `circle`.
* `radius`: outer corner radius (R50 etc.). Inner shapes get `radius - inset` automatically.
* `ground`: colour name (`yellow`, `white`, `red`, `orange`, `green`, `blue`, `brown`, `yellowgreen`, `black`), or `none` for a
  transparent background when the sign's real outline is a polygon (fingerboards, pointed panels, shields): everything
  outside the sign must be transparent for the digital platform; white that is part of the sign is drawn as elements.
* `edge`: `{"colour": "white", "width": 10}` — an outer strip, drawn first (e.g. the 10 white edge on white
  regulatory signs, the 16 white strip on STOP). Only if the drawing shows one.
* `border`: `{"colour": "black", "width": 25}` — the band inside the edge. Several: `"borders": [ ... ]` outer to inner.

## Elements (drawn in order, all coordinates in mm from the panel's top-left)
* Text: `{"type":"text","text":"ROAD","series":"D","height":100,"top":80,"expect":335}`
  - `series`: `B` `C` `D` `E` `Emod` `F` from the drawing's "100 D" style note; `"speed"` = the R4-1 rule
    (2 numerals or 110/115 -> D, other 3 numerals -> C).
  - `height`: capital letter height. `top`: y of the top of the capitals (add the vertical dims down from the
    top edge: e.g. 25 border + 80 gap -> top of first line 80 if the 80 is from the panel edge; read carefully
    which edge the dimension starts from).
  - Centred horizontally by default; `"align":"left","x":123` or `"align":"right","x":...` for guide signs;
    `"cx"` to centre on a different x (e.g. one column of a two-column layout).
  - Words on one line with a stated gap: `{"type":"text","words":["ROAD","CLOSED"],"gap":130,"expect":[553,797], ...}`;
    different gaps between pairs: `"gap":[54,66]` (one per pair, left to right). The group is centred as a whole.
  - Mixed series/heights on one line (e.g. "2 km", "200 m AHEAD"): `"runs":[{"text":"{km}","series":"E","height":100},{"text":"km","series":"Emod","height":85}]`
    with `"gap"` (scalar or list) between runs; all runs share one baseline (= `top` + tallest height); centred as a whole,
    so `vary` works on the numeral. `expect` is then a list, one per run (null to skip a run). A run may carry
    `"slot":160` when the drawing gives the varying numeral a fixed-width box: the run then occupies that width with the numeral centred in it.
  - `expect`: the drawing's dimension across that word (ink width). ALWAYS fill it in when the drawing gives one;
    the generator checks it (±2 %). Lower case: `"series":"Emod"`, height is still the capital height.
  - `colour`: default black. `"tracking":"minus10"` only if the drawing says condensed/medium spacing.
  - Legend that varies (dashed numerals, "Varies"): put `{speed}` in `text` and `name`, and add
    `"vary":{"key":"speed","values":[5,10,20,30,40,50,60,70,80,90,100,110,120,130]}` (use the values that make
    sense for the sign; area limits 10–60; km/h plates as for speeds).
* `{"type":"annulus","cx":300,"cy":400,"r_outer":297,"r_inner":237,"colour":"red"}`
* `{"type":"circle","cx":..,"cy":..,"r":..,"colour":..}`, `{"type":"rect","x":..,"y":..,"w":..,"h":..,"rx":0,"colour":..}`
* `{"type":"panel","x":..,"y":..,"w":..,"h":..,"radius":40,"colour":"white"}` — sub-panel (road-name panel).
* `{"type":"polygon","points":[[x,y],...],"radius":0,"colour":..}` — any straight-edged shape you can dimension
  from the drawing (bars, chevrons, stripes, simple block arrows with stated geometry). Add `"stroke":{"colour":"black","width":2}`
  for an outline when the drawing shows one (e.g. a white pointed fingerboard drawn with its own outline).
* `{"type":"path","d":"M...Z","colour":..}` — hand-entered path in mm when a polygon won't do.
* Symbol from the grid inset (bicycle, worker, curve arrow, car...):
  `{"type":"symbol","id":"tm10-1a_up_arrow","x":250,"y":100,"w":100,"h":400,"colour":"black"}`
  where x/y/w/h is the symbol's bounding box on the sign, from the drawing's dimensions (e.g. TM10-1A: arrow
  between 100 from top and 100 from bottom, centred: y 100, h 400; width from the grid: 2 squares of 50 = 100).
  Also add at spec top level: `"symbols":{"tm10-1a_up_arrow":{"source":"TM10-1A","desc":"upward block arrow","grid_mm":50}}`.
  `"flip":"h"` mirrors the symbol in place within its box (e.g. reuse a left arrow as a right arrow); `"rotate":90` turns it about the box centre.
  The symbol artwork is traced separately; you only place it. Reuse an existing id when the drawing says the
  symbol is the same as another sign's.

## Symbol tracing controls (in the `symbols` entry)
The tracer (`tools/trace_symbol.py --spec ...`) finds the sign's ground in the drawing, maps the symbol's mm box onto it and
traces the dark pixels. Options per symbol entry: `"source":"<CODE>"` (drawing to trace from), `"which":1` (second panel
when the drawing shows two signs, ordered top-to-bottom/left-to-right), `"panel_px":[x0,y0,x1,y1]` (pixel bbox of the
detected region if automatic detection fails), `"colours":["black","red"]` (trace each colour as its own layer with a fixed
fill, for red/black or green/red symbols), `"threshold":110`, `"invert":true` (light symbol on dark ground; automatic for
black grounds), `"nomask":true` (do not blank pixels outside the ground shape; by default the crop is masked to the inner
diamond/circle/rect so border corners are excluded), `"open":9` (remove hairlines such as the drawing's centre lines; 9 = lines thinner than ~1.5 source px). Crops are written to the scratch `crops/` dir with `--show <dir>` for checking.

## Geometric arrows (preferred over traced symbols whenever the drawing states the arrow's dimensions)
```json
{"type":"arrow","width":110,"heading":-90,"x":200.33,"y":305.33,"w":500,"h":485,
 "path":[{"line":340},{"corner":{"turn":"left","angle":90,"r_outer":60,"r_inner":15}},{"line":225}],
 "head":{"length":220,"width":290,"notch":15,"barb_r":20,"tip_r":20}}
```
* `width`: shaft width at the tail. Guide-sign block arrows usually taper: add `"width_head"` (shaft width where it meets the
  head) — only with a single straight `{"line": L}` path — and `"tail_r"` for rounded tail corners. Read the inset carefully:
  on G9-3 the pair 50 / 37 is tail / head shaft width and 13 is the notch (no barb step).
  Example: `{"type":"arrow","width":50,"width_head":37,"heading":180,"path":[{"line":496}],"head":{"length":104,"width":160,"notch":13,"tip_r":8,"barb_r":8}}`.
* `heading`: direction the tail-to-head axis starts in, degrees: 0 right, -90 up, 180 left, 90 down, -45 up-right.
* `path`: the shaft centreline from the tail, in order: `{"line": L}`; `{"arc": {"r_inner": R, "sweep": deg, "turn": "left"|"right"}}`
  (or `"r_outer"`, or `"r"` for the centreline radius); `{"corner": {"turn":..., "angle": 90, "r_outer": Ro, "r_inner": Ri}}` for a
  sharp bend with fillets. Line lengths are measured along the centreline (so a stem "395 tall to the arm top" with a 110 shaft is
  a 340 line to the arm's centreline). A head only, no shaft: omit `path`.
* `head`: `length` (rear extreme of the barbs to the tip) and `width` (barb extreme to barb extreme) are the extremes of the
  finished rounded outline, as the drawings dimension them (`"dims":"vertices"` switches to sharp-vertex dimensions); `notch` (head base meets the shaft this far
  ahead of the barb line; 0 = flat base), `barb_step` (short perpendicular edge at each barb before the base line: the drawings'
  "barb return"/"barb step"), `tip_r`, `barb_r`, `step_r`, `tip_flat` (truncated tip width).
* The finished outline is centred in the box (x, y, w, h) — keep the symbol's box; the generator reports if the computed size
  differs from the box by more than 2 %, which means a dimension was misread. (L)/(R) mirroring works as for symbols.
* When converting a traced symbol: keep the `symbols` entry's desc for the record, delete the `symbol` element, add the `arrow`.

## Handedness
Drawings named `W1-1(R)(L)` or showing (L) and (R): write one spec with `"hands":["L","R"]` and
`"drawn_hand":"L"` (whichever the dimensions are given for). Symbols/polygons/paths mirror automatically for the
other hand; text does not. If (L) and (R) are separate PNGs, write two specs.

## Per-hand words and rotated text
* One drawing that reads LEFT for (L) and RIGHT for (R): `"hands":["L","R"], "hand_values":{"L":{"dir":"LEFT"},"R":{"dir":"RIGHT"}}`
  and use `{dir}` in `name`, `legend` and the text.
* `"rotate": -45` on a text element rotates the line about its own centre (crossbuck arms).

## Not a sign
Figures, forms, symbol grids (S*, TS*, MS*), examples of assemblies: write `{"code":"S1","skip":"symbol source: cross"}`
(or `"skip":"figure"`), so the manifest accounts for every drawing.

## Check your work
Run `.venv/bin/python tools/signgen.py tools/specs/<FAMILY>/*.json` (or the scratch venv) — every width mismatch
must be either fixed (re-read series/height) or explained in `notes`. Then render a few with Inkscape and compare
to the drawing. Write `tools/specs/<FAMILY>/_REPORT.md`: one line per drawing — code, name, status
(spec | needs-symbol <ids> | skipped <why>), flags.

## Worked example — TM2-4A
```json
{"code":"TM2-4A","name":"ROAD_CLOSED_WHITE_SQUARE","legend":"ROAD CLOSED","shape":"rect","size":[600,600],
 "ground":"white","border":{"colour":"black","width":25},
 "elements":[{"type":"text","text":"ROAD","series":"C","height":110,"top":130,"expect":303},
             {"type":"text","text":"CLOSED","series":"C","height":110,"top":360,"expect":450}]}
```
Drawing: 600 square, 25 border, right-hand stack 130 / 110 C / 120 / 110 C / 130 -> tops at 130 and 360;
top dims 180 | 303 | 181 -> ROAD expect 303; bottom 75 | 450 | 75 -> CLOSED expect 450.

## Polygons with different corner radii
`"radius"` on a polygon may be a list, one radius per vertex in order, e.g. the G8-9 route-marker shield:
`{"type":"polygon","points":[[0,0],[360,0],[360,111],[280,360],[80,360],[0,111]],"radius":[100,100,50,50,50,50],"colour":"brown"}`.
Use `"shape":"rect"` with `"ground"` for the drawing's overall bounding box, or draw the whole sign as polygon elements on a
`"ground":"white"` panel if the sign is not rectangular and not one of the built-in shapes.

## Guide signs (G / GE / GM)
* Overall panel: `shape: rect`, `radius`, `edge` (white edge strip) + `border` (e.g. green band) + `ground` — as the drawing dimensions.
* Road-name panels: `{"type":"panel", ...}` white with radius, then its text on top.
* Left-aligned lines: `"align":"left","x":<ink left x>`; route numbers in yellow: `"colour":"yellow"`; lower case destinations: `"series":"Emod"`.
* Arrows: place as a `symbol` element with the bounding box from the drawing; give the id a style hint (`arrow_straight_up`, `arrow_left`, `arrow_diag_up_right`, `arrow_chevron_left`) and copy every stated arrow dimension (radii, shaft width, head width) into the `symbols` entry's `desc` so it can be drawn parametrically.
* Route-marker shields (G8-9 series): polygons with per-vertex radii as above, or a `symbol` if the shape is not dimensioned.
