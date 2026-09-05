# International traffic signage — what it would take (NZ, UK, USA)

Reviewed 2026-09-05 against the pipeline built for AS 1743 (`tools/`): a dimensioned drawing or vector
artwork per sign → spec → generated SVG, with fonts outlined and the standard's letter spacing reproduced.
The question for each country is where the authoritative drawings come from, in what form, under what
licence, and with which fonts.

## Summary

| | New Zealand | United Kingdom | United States |
|---|---|---|---|
| Governing document | Land Transport Rule: Traffic Control Devices 2004 (Schedule 1) + Traffic Control Devices Manual (TCD Manual, 16 parts) | Traffic Signs Regulations and General Directions 2016 (TSRGD) + Traffic Signs Manual (Ch. 1–8) | MUTCD 11th Edition (Dec 2023) + Standard Highway Signs (SHS) publication |
| Authoritative sign artwork | NZTA "Sign specifications" register: one spec sheet per sign code, downloadable | DfT "Traffic signs working drawings" per TSRGD schedule (PDF), one drawing per diagram | FHWA SHS: 2004 edition + 2012 supplement (dimensioned PDF) and 2024 edition phased releases with **vector files (EPS/PDF/SVG)** |
| Form of artwork | Spec sheets (formats to confirm; PDF at least) | Vector PDF working drawings with dimensions, x-height based | Vector PDF/EPS (2009 interim set), PDF/EPS/SVG (2024 phases); dimensioned |
| Fonts | FHWA-derived alphabet, the same family as AS 1744 — the repo's FHWA Series fonts apply (confirm in TCD Manual Part 1) | Transport Medium / Transport Heavy, Motorway Permanent / Temporary — Crown copyright | FHWA Series B–F, E Modified — already in the repo |
| Licence | NZTA: files "can be used for commercial and non-commercial purposes without approval" (site statement) | Open Government Licence v3.0 for the working drawings (attribution). Free Transport font downloads are "private non-commercial use" only; commercial fonts sold by URW++ (Transport) and K-Type (Transport New) | US federal work: public domain |
| Sign count (order of magnitude) | ~600 codes in the register | ~1,000 diagrams across 17 schedules (many with sub-variants) | ~700 designs in SHS (R, W, G, S, M, D series) |
| Fit with our pipeline | Good: same alphabet, dimensioned sheets, similar sign families to AS 1743 | Good for artwork (vector, so no tracing); layout is rule-based (x-height tiles) like AS 1319, so the generator needs a tile-layout mode | Best: vector artwork + our fonts + public domain |
| Blocker to resolve first | Confirm spec-sheet file formats and whether they are dimensioned | Commercial font licence for Transport/Motorway | None; download the SHS sets |

## New Zealand

* **Sources.** [Sign specifications register](https://www.nzta.govt.nz/resources/traffic-control-devices-manual/sign-specifications)
  (one entry per sign, e.g. [view/694](https://www.nzta.govt.nz/resources/traffic-control-devices-manual/sign-specifications/view/694)),
  the [TCD Manual](https://www.nzta.govt.nz/resources/traffic-control-devices-manual) and the
  [Signs and markings index](https://nzta.govt.nz/resources/signs-markings-index/signs-markings-index). Legacy MOTSAM codes
  are being retired in favour of the TCD Manual.
* **Codes.** R (regulatory), A (advisory), R6 (parking), IG (information), RP (parking zones), PW (warning) etc.; the
  register lists each sign with its spec sheet.
* **Fonts.** NZ adopted the US/Pacific-Rim system in 1949; sign lettering is the FHWA-derived alphabet also used by
  AS 1744, so the repo's fonts and the AS 1744 spacing check carry over. Motorway signs follow the US model.
* **Licence.** The register states the downloadable files may be used commercially without approval.
* **Unverified (the pages are script-rendered and could not be read here):** the file formats of the spec sheets
  (PDF certain; DXF/EPS unknown) and whether every sheet is fully dimensioned like AS 1743's. Check three or four
  entries by hand before planning.
* **Effort.** If the sheets are dimensioned PDFs, the AS 1743 process applies almost unchanged: transcription agents per
  family, width checks, contact sheets. If vector, symbols can be lifted rather than traced. Estimate: about the same as
  AS 1743 (a few sessions) for ~600 signs, less if vector.

## United Kingdom

* **Sources.** [Working drawings per TSRGD 2016 schedule](https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-3)
  (schedules 2–16 published separately, e.g. [Sch 9](https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-9),
  [Sch 14](https://www.gov.uk/government/publications/traffic-signs-working-drawings-tsrgd-2016-schedule-14)). Each drawing is a
  1–2 page PDF titled by Schedule/Part/Item with a "p-number" (p606, p956x2 …), dimensioned in terms of the x-height.
* **Design system.** UK signs are laid out from tiles scaled by the lettering x-height (Traffic Signs Manual Chapter 7);
  roundels and triangles have prescribed size ranges. That is a rule-driven system like AS 1319, not a fixed drawing per
  size: the generator needs an x-height tile layout mode, after which each sign is a short spec.
* **Artwork.** The PDFs are vector: symbols can be extracted exactly, no tracing.
* **Fonts.** Transport Medium/Heavy and Motorway are Crown copyright. The free TrueType files at
  [roads.org.uk/fonts](https://www.roads.org.uk/fonts/) are for private non-commercial use only and lack professional
  kerning; for a commercial platform license URW++ Transport or K-Type Transport New. The working drawings themselves
  are OGL v3 (attribution required).
* **Effort.** Larger inventory and a new layout engine; realistic estimate two to three times the AS 1743 effort, the
  engine first. Decide the font licence before starting.

## United States

* **Sources.** [MUTCD 11th Edition](https://mutcd.fhwa.dot.gov/index.htm) and the SHS publication
  ([publications page](https://mutcd.fhwa.dot.gov/ser-pubs.htm); [2009-interim vector set](https://mutcd.fhwa.dot.gov/shsm_interim/):
  "full-size, vector-based, undimensioned sign layout in EPS" plus PDF "with dimensions"). The 2024 SHS is being released in
  phases with design details for every 11th-edition sign and supporting vector graphics; as of Feb 2026 the sixth and final
  phase is out (213 guide and 8 regulatory signs in that phase).
* **Codes.** R (regulatory), W (warning), G/D/M (guide), S (school), etc. — the same lineage as AS 1743's families.
* **Fonts.** FHWA Series B–F and E Modified: already in `Fonts/`.
* **Licence.** Works of the US federal government are public domain.
* **Effort.** Lowest per sign: vector artwork means symbols are lifted, not traced; layouts are dimensioned; fonts and
  spacing already handled. A few sessions for the full set, mostly transcription and checking. State supplements
  (California, Minnesota…) are separate and optional.

## Recommended order

1. **USA** first: everything needed is free, public domain and vector, and the fonts are the ones already in use.
2. **New Zealand** second: same alphabet and sign families; confirm the spec-sheet formats first.
3. **UK** last: needs the tile-layout engine and a commercial font licence.

## What to obtain before starting (per country)

* USA: download the SHS 2004 edition, 2012 supplement and the 2024 phased sets (PDF + EPS/SVG) into `International/USA/source/`.
* NZ: download a sample of spec sheets; confirm formats and dimensioning; then the full register into `International/NZ/source/`.
* UK: download the working drawings for all schedules into `International/UK/source/`; obtain a commercial Transport/Motorway
  font licence; decide whether Scotland/Wales bilingual variants are in scope.
