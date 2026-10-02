# Pack builders (working scripts, kept for reproducibility)

One-off scripts the build agents wrote while producing the state packs, copied out of the session scratchpad so they are
not lost. They are NOT maintained tools: paths are hard-coded to the scratchpad, names are terse, and several overlap.
The specs in `tools/specs/<PACK>/` and symbols in `tools/symbols/` are the source of truth; `tools/signgen.py`
regenerates every sign from them without these scripts.

* `2026-10-02/qld-nsw/` — QLD TC-sheet builder (`auto.py`, `qb.py`, `vec.py`, `fixwind.py`: sheet vectors → spec paths,
  winding fix for even-odd symbols; batch lists `tcw.txt` / `tct.txt`), NSW helpers, overlay/contact-sheet runners.
* `2026-10-02/sa/` — SA artwork-built families (`auto.py`, `board.py`, `contact.py` …): PDF fills rendered without
  dimension line-work, legend words matched to ink and re-set in the FHWA fonts.

Turning the useful parts into proper tools is ticketed (see Tickets/INDEX.md, "pack builders").
