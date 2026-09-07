# Sign library

Two top-level folders say what a pack is fit for:

* `Complete/` — approved sign packs, ready to upload to SitePilot. Each pack is `<country>/<jurisdiction>/SVGs/<family>/…`
  with a `MANIFEST.csv`. Today: `Complete/Australia/National (AS 1743)` `Complete/New Zealand/National (TCD Manual)` and `Complete/USA/Federal (MUTCD 2023)`.
* `Processing/` — packs still being built or checked: sources, registers, extraction output, review notes. Nothing here
  is approved. Australian states and territories, US states and the United Kingdom sit here until their signs are clean.

A pack moves from `Processing/` to `Complete/` only after review. Tools live in `tools/` (see `tools/README.md`), work
items in `Tickets/`, jurisdiction status in `JURISDICTIONS.md`, the plan in `PLAN.md`.
