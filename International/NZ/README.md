# New Zealand — TCD Manual sign specifications

Status 2026-09-05: **blocked on access**. Every nzta.govt.nz URL (the sign-specifications register, each `view/<id>` entry
and the `/assets/...` PDFs) sits behind Imperva/Incapsula bot protection, which answers curl and the in-app browser with a
"security check" checkbox page. That check is not something the extractor may complete on its own; it has to be passed
once by a person in the browser the tools use (the in-app Browser pane, or Chrome with the Claude extension connected),
after which the register and files load normally.

## Sources (once reachable)

* Register: https://www.nzta.govt.nz/resources/traffic-control-devices-manual/sign-specifications
  (filters `?category=<id>&term=<code>`, entries `.../sign-specifications/view/<id>`).
* TCD Manual Part 1, General requirements for traffic signs (fonts, sizes, colours):
  https://www.nzta.govt.nz/assets/resources/traffic-control-devices-manual/docs/part-1-general-requirements.pdf
* Colours: NZTA M28:2023; performance spec for permanent signs: NZTA P24:2020.
* Licence: NZTA states the downloadable files can be used commercially without approval (Wikimedia Commons carries the
  same statement in its NZTA-Sign-Spec licence tag).

## Plan

1. Pass the security check, then crawl the register: one row per sign (code, name, category, entry URL, file URLs).
2. Download every spec file into `Original PDFs/` (PDF certain; DXF/EPS if offered — DXF/EPS means exact artwork like MUTCD).
3. Confirm the lettering standard in Part 1 (expected: the FHWA-derived alphabet, so the repo's Series fonts apply).
4. Vector files → the MUTCD extractor route (`tools/shs_extract.py` adapted to the NZ sheet layout);
   dimensioned raster/PDF drawings only → the AS 1743 spec route (`tools/signgen.py`).
5. Output to `SVGs/` in family folders with a manifest, same header/transparency/no-metadata rules as the other sets.
