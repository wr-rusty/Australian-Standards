#!/usr/bin/env python3
"""shs_run.py — extract every SHS sheet set into MUTCD 2023/SVGs/<set>/ and build review sheets.
  python3 tools/shs_run.py [sheets_dir]"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import shs_extract as X, shs_sheets as SH
P = os.path.join(X.ROOT, "USA", "Federal (MUTCD 2023)", "Original PDFs")
SETS = [("SHS 2004 Edition/Regulatory.pdf", "Regulatory Signs"), ("SHS 2004 Edition/Warning.pdf", "Warning Signs"), ("SHS 2004 Edition/Guide.pdf", "Guide Signs"),
        ("SHS 2004 Edition/School.pdf", "School Signs"), ("SHS 2004 Edition/EM.pdf", "Emergency Management Signs"), ("SHS 2004 Edition/Markers.pdf", "Object Markers"),
        ("SHS 2012 Supplement/shs_2004_2012_sup.pdf", "2012 Supplement"),
        ("SHS 2024 Releases/2024_SHS_Releases_1-4-Regulatory_Warning_TTC_School_Signs.pdf", "2024 Releases 1-4"),
        ("SHS 2024 Releases/2024_SHS_Release_5-Guide_Signs.pdf", "2024 Release 5 Guide"),
        ("SHS 2024 Releases/2024_SHS_Release_6-Regulatory_Signs.pdf", "2024 Release 6 Regulatory"),
        ("SHS 2024 Releases/2024_SHS_Release_6-Guide_Signs.pdf", "2024 Release 6 Guide")]
def run_set(i, sheets=None):
    pdf, fam = SETS[i]; folder = os.path.join(X.OUT, fam)
    if os.path.isdir(folder): shutil.rmtree(folder)
    if os.path.isdir(os.path.join(X.OUT, "intervene", fam)): shutil.rmtree(os.path.join(X.OUT, "intervene", fam))
    X.main(os.path.join(P, pdf), fam)
    if sheets: SH.main(os.path.join(P, pdf), fam, os.path.join(sheets, fam.replace(" ", "_")))
def main(sheets=None, only=None):
    if only is None:
        idir = os.path.join(X.OUT, "intervene")
        if os.path.isdir(idir): shutil.rmtree(idir)
    for i in ([only] if only is not None else range(len(SETS))): run_set(i, sheets)
if __name__ == "__main__":   # shs_run.py [sheets_dir] [set_index]  (set_index: run one set, for parallel runs)
    main(sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else None, int(sys.argv[2]) if len(sys.argv) > 2 else None)
