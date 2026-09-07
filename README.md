# Sign library

Two top-level folders say what a pack is fit for:

* `Complete/` — approved sign packs, ready to upload to SitePilot. Each pack is `<country>/<jurisdiction>/SVGs/<family>/…`
  with a `MANIFEST.csv`. Today: `Complete/Australia/National (AS 1743)`.
* `Processing/` — packs still being built or checked: sources, registers, extraction output, review notes. Nothing here
  is approved. Australian states and territories, New Zealand and the USA sit here until their signs are clean.

A pack moves from `Processing/` to `Complete/` only after review. Tools live in `tools/` (see `tools/README.md`), work
items in `Tickets/`, jurisdiction status in `JURISDICTIONS.md`, the plan in `PLAN.md`.
