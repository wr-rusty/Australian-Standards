# Sign library

Official traffic-control imagery as SVG, for SitePilot: a plan-markup platform for traffic, civil construction and
planning used by governments and civil contractors. Every sign is taken from its authority's own standard, drawing or
artwork. Nothing is invented, and anything assumed is written down next to the sign.

Status as of 2026-10-02.

## What is here

| Pack | Signs | Source and method | State |
|---|---|---|---|
| Australia national, AS 1743 | 1,068 | generated from the standard's drawings (specs), every family overlaid on its drawing | approved |
| New Zealand national, TCD Manual | 1,437 | NZTA register artwork, plus 149 parking time-plate variants | approved |
| USA federal, MUTCD | 1,451 | FHWA Standard Highway Signs sheets, 2004 / 2012 / 2024 | approved |
| United Kingdom national, TSRGD 2016 | 658 | Department for Transport artwork | built, awaiting inspection |
| France national, IISR | 484 (+46 set aside) | Cerema's official SVGs | built, awaiting inspection |
| Germany national, StVO | 232 of about 1,160 | BASt's free vector set | partial: the rest needs the paid set or generation |
| Australia NSW | 538 | generated from TfNSW design plans | built, awaiting inspection; one sign open |
| Australia QLD | 491 | generated from TMR design sheets | Regulatory, Speed, Parking, Warning built; other families to do |
| Australia SA | 565 | generated from DIT sign sheets | built except one series; awaiting inspection |
| Australia TAS | 15 | generated from State Growth drawings | built, awaiting inspection |
| Australia NT | 8 | generated from DLI standard drawings | built, awaiting inspection |
| Australia VIC, WA, ACT | none usable yet | earlier extractions only (319, 1,189, 5) | rebuild not started |
| Italy national | none | 1992 Gazzetta Ufficiale figures (scan) | sources only |
| Canada, USA states | none usable yet | California and Texas extractions on file | not started |

State and territory packs hold only the signs that jurisdiction adds to the national set. A code that already exists
nationally is a pointer in the manifest, never a second drawing.

## Layout

* `Complete/` holds approved packs, ready to upload: `<country>/<pack>/SVGs/<family>/…` with `SVGs/MANIFEST.csv`.
* `Processing/` holds packs still being built or inspected. Nothing in it is approved.
  * `SVGs (generated)/` is the spec-driven set for a state pack. This is the deliverable once inspected.
  * `SVGs/` in a state pack is the earlier automatic extraction, kept as source material only.
  * `Original PDFs/`, `Original PNGs/`, `Original EPS/` and similar hold the authority's sources.
  * `SOURCES.md` in each pack says where every source came from, its licence, and how the pack was built.
* `tools/` holds the generators and checkers (`tools/README.md`), with one spec per sign in `tools/specs/<pack>/`.
* `Tickets/` is the work tracker: `python3 Tickets/tk.py list`.

A pack moves from `Processing/` to `Complete/` only after inspection.

## How signs are made

Two routes, chosen by what the authority publishes.

* **Official artwork, converted.** Where the authority publishes the sign faces as vector art (UK, France, Germany,
  New Zealand, USA), the artwork is converted as-is to the library's SVG convention. Sizes come from the authority's
  own figures.
* **Drawings, rebuilt from a spec.** Where the authority publishes dimensioned drawings (AS 1743 and the Australian
  states), each sign has a JSON spec holding the numbers read from its drawing. The generator sets legends in the
  AS 1744 letter series and draws the sign from the spec. Each sign is then laid over its drawing to check border
  widths, letter weight and placement.

Every manifest row records the sign's code, file, real size, and notes: what was read, what was decided, and where
the source disagrees with itself.

## SVG convention

* `viewBox` is in points at 1 pt = 1 cm of sign; `width` and `height` are that viewBox in millimetres at 72 pt per
  inch. A 600 mm sign has `viewBox="0 0 60 60"` and `width="21.17mm"`. This is deliberate.
* One `<g transform="scale(0.1)">` wraps paths whose coordinates are tenths of a millimetre.
* Text is outlined. There is no metadata, style block or editor namespace.
* Everything outside the sign's outline is transparent.
* One file per sign at the illustrated size. Variants exist only where the standard defines them, or where a sheet says
  "insert appropriate value" and a small set of values in real use is generated and noted.
* Guide and freeway destination signs are excluded; example and site-specific sheets are skipped with the reason
  recorded.

## Scope

The platform needs the whole traffic-control picture, drawn the way a Traffic Guidance Scheme draws it: plan view.

| Category | Status |
|---|---|
| Traffic signs (regulatory, warning, temporary, service, hazard markers) | the work above |
| Safety signs (AS 1319 and equivalents) | paused: needs the standard's text |
| Pavement markings and line marking | not started: needs AS 1742.2; UK and USA sources on file |
| Worksite devices (cones, bollards, barrier boards, arrow boards) as plan symbols | not started: needs AS 1742.3 |
| Road safety barriers and delineation | not started: needs AS/NZS 3845 |

## Where to look next

* `OPEN-ITEMS.md` lists the paywalled standards, purchases and decisions that work is waiting on.
* `INSPECTION.md` says how a pack is inspected before it moves to `Complete/`. Each pack has an "Inspect: …" ticket
  (SGN-094 to SGN-102).
* `COUNTRIES.md` is the country matrix: what we have, what is being built, what is sourced, and candidates.
* `JURISDICTIONS.md` maps every jurisdiction to its folder and current status.
* `Tickets/INDEX.md` lists all open work; remaining build work is SGN-083 to SGN-093.
* `PLAN.md` is the original AS 1743 plan, kept for the record.

## Licences of the sources

Each pack's `SOURCES.md` has the detail. In short: AS 1743 drawings are the standard's own; NZTA register artwork;
FHWA material is US public domain; DfT artwork is Crown copyright under the Open Government Licence v3; Cerema's SVGs
are under Licence Ouverte 2.0 and need an attribution line; German signs are official works without copyright
protection; TfNSW, TMR and DIT sheets are Creative Commons Attribution; Tasmanian and Northern Territory drawings are
Crown copyright with reuse terms still to be recorded.
