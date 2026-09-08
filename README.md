# Sign library

## Scope (widened 2026-09-08)

The platform needs the whole traffic-control and safety picture, not only sign faces. Per jurisdiction the brief covers:

| Category | Australia | New Zealand | USA | UK | Status |
|---|---|---|---|---|---|
| Traffic signs (regulatory, warning, guide, temporary, hazard markers) | AS 1743 + state supplements | TCD Manual / NZTA register | MUTCD / SHS + state supplements | TSRGD 2016 | built (national); states in progress |
| Safety signs (workplace / site) | AS 1319 | AS/NZS 1319 (same) | ANSI Z535 / OSHA | BS EN ISO 7010 | AS 1319 parked (needs the standard text, SGN-064) |
| Pavement markings and line marking (lines, arrows, symbols, letters) | AS 1742.2 | MOTSAM Part 2 / TCD Manual | MUTCD Part 3, SHS "Pavement Markings" chapter (on disk) | TSRGD Schedule 11 (84 drawings on disk) | not started (SGN-069..072) |
| Worksite / temporary traffic control devices (cones, bollards, barrier boards, tapers, arrow boards, VMS, layouts) | AS 1742.3 | CoPTTM | MUTCD Part 6 | Chapter 8 / Safety at Street Works | not started (SGN-073..076) |
| Road safety barriers and delineation (W-beam, wire rope, concrete, terminals, guide posts) | AS/NZS 3845, state drawings (NT CS 3200, TAS) | NZTA M23 | MASH / MUTCD Part 3 delineators | RRRAP / CD 377 | not started (SGN-077) |

Signs came first because they are drawing-by-drawing standards; markings and devices need the same treatment
(one SVG per standard drawing, dimensions from the standard, nothing invented).

Form of the imagery (Russell, 2026-09-08): everything is drawn the way a Traffic Guidance Scheme (TGS) draws it — plan
view. Markings to scale from the standard's plan drawings; signs as their faces; devices (cones, bollards, barrier boards,
arrow boards, barriers, vehicles) as the standard TGS legend symbols of each jurisdiction (AS 1742.3 / AGTTM in Australia,
CoPTTM in NZ, MUTCD Part 6 in the US, Chapter 8 in the UK), at the device's real plan size where the standard gives one.

Two top-level folders say what a pack is fit for:

* `Complete/` — approved sign packs, ready to upload to SitePilot. Each pack is `<country>/<jurisdiction>/SVGs/<family>/…`
  with a `MANIFEST.csv`. Today: `Complete/Australia/National (AS 1743)` `Complete/New Zealand/National (TCD Manual)` and `Complete/USA/Federal (MUTCD 2023)`.
* `Processing/` — packs still being built or checked: sources, registers, extraction output, review notes. Nothing here
  is approved. Australian states and territories, US states and the United Kingdom sit here until their signs are clean.

A pack moves from `Processing/` to `Complete/` only after review. Paywalls, purchases and decisions waiting on Russell are
listed in `NEEDS-RUSSELL.md`. Tools live in `tools/` (see `tools/README.md`), work
items in `Tickets/`, jurisdiction status in `JURISDICTIONS.md`, the plan in `PLAN.md`.
