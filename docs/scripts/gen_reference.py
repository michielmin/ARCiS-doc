#!/usr/bin/env python3
"""
Build the keyword reference pages from

  docs/reference/keywords.json            (extracted from Init.f, see extract_keywords.py)
  docs/reference/keyword_descriptions.yml (hand-written descriptions)

Writes
  docs/reference/keywords.md
  docs/reference/molecules.md

Run from the repository root (after extract_keywords.py):

    python docs/scripts/extract_keywords.py
    python docs/scripts/gen_reference.py

Keywords present in the code but missing a description are collected in a
"Not yet described" section; descriptions for keywords that no longer exist
in the code are reported as warnings.
"""
import glob
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "docs" / "reference"

REVIEW = ' <span class="review" title="Inferred from the code, to be checked">✎</span>'
UNUSED = ' <span class="unused" title="Parsed by Init.f but not used anywhere else in the code">no effect</span>'


def tidy_default(v):
    if v is None:
        return "—"
    v = v.strip()
    if v in ("' '", "'  '", '" "'):
        return "*(empty)*"
    if v.startswith("$HOME"):
        v = "$HOME" + v[5:].strip("'\"")
    m = re.fullmatch(r"([0-9.]+)e0/([0-9.]+)e0", v)
    if m:
        v = "%g" % (float(m.group(1)) / float(m.group(2)))
    m = re.fullmatch(r"([0-9.]+)e0", v)
    if m:
        v = "%g" % float(m.group(1))
    if v in (".true.", ".false."):
        return "`%s`" % v
    try:
        f = float(v)
        if 1e-3 <= abs(f) < 1e5 or f == 0:
            return "%g" % f
        return "%.3g" % f
    except ValueError:
        pass
    return "`%s`" % v.strip("'\"")


def used_elsewhere(variable, sources):
    """Is the variable used outside the routines that only read/set defaults?"""
    if not variable or variable.startswith(("→", "(")):
        return True
    base = re.sub(r"\(.*", "", variable).split("%")[0]
    if base.lower() in ("photoreacts", "obsspec", "mixrat", "cloud", "retpar"):
        return True
    pat = re.compile(r"\b%s\b" % re.escape(base), re.I)
    return any(pat.search(s) for s in sources)


def load_sources():
    sources = []
    for f in glob.glob(str(ROOT / "*.f")) + glob.glob(str(ROOT / "*.f90")) + \
            glob.glob(str(ROOT / "*.F")) + glob.glob(str(ROOT / "ggchem" / "*.f")):
        name = Path(f).name
        if name == "Modules.f":
            continue
        s = Path(f).read_text(errors="replace")
        if name == "Init.f":
            for sub in ("ReadAndSetKey", "SetDefaults"):
                m = re.search(r"^\s*subroutine\s+%s\b" % sub, s, re.M | re.I)
                e = re.search(r"^\s*end\s*$", s[m.end():], re.M | re.I)
                s = s[:m.start()] + s[m.end() + e.end():]
        sources.append(s)
    return sources


def key_cell(k, prefix=""):
    names = ["`%s%s`" % (prefix, k["key"])]
    names += ["`%s%s`" % (prefix, a) for a in k["aliases"]]
    return names[0] + ("<br><small>" + ", ".join(names[1:]) + "</small>" if len(names) > 1 else "")


def desc_cell(d, unused=False):
    if d is None:
        return "*not yet described*"
    txt = d.get("desc", "").replace("|", "\\|").replace("\n", " ")
    if d.get("unit"):
        txt += " <small>[%s]</small>" % d["unit"]
    if d.get("review"):
        txt += REVIEW
    if unused:
        txt += UNUSED
    return txt


def table(rows):
    out = ["| Keyword | Default | Description |", "|---|---|---|"]
    out += ["| %s | %s | %s |" % r for r in rows]
    return "\n".join(out)


def main():
    data = json.loads((REF / "keywords.json").read_text())
    desc = yaml.safe_load((REF / "keyword_descriptions.yml").read_text())
    sources = load_sources()

    top = {k["key"]: k for k in data["top"]}
    warnings = []
    described = set()

    md = []
    md.append("# Keyword reference\n")
    md.append(
        "This page is **generated from the source code** (`Init.f`) by "
        "`docs/scripts/gen_reference.py`: the keywords, aliases and default values "
        "are always those of the current code. Descriptions come from "
        "`docs/reference/keyword_descriptions.yml`.\n\n"
        "* Keywords are **case-insensitive**, molecule names are **case-sensitive**.\n"
        "* A trailing number is an index: `phase2`, `tauVpoint3`.\n"
        "* Keywords with sub-keywords use a colon: `cloud1:tau=10`, `obs2:file=…`.\n"
        "* Values use Fortran list-directed input: `1d-4`, `.true.`, `'TEXT'`.\n\n"
        "Markers: ✎ description inferred from the code and still to be verified; "
        "<span class=\"unused\">no effect</span> keyword is read but its value is not "
        "used anywhere in the current code.\n")

    for sec in desc["sections"]:
        rows = []
        for key, d in sec["keys"].items():
            if key == "<molecule>":
                rows.append(("`<molecule>`<br><small>e.g. `H2O`, `CO2`</small>", "0", desc_cell(d)))
                continue
            if key not in top:
                warnings.append("described keyword '%s' not found in the code" % key)
                continue
            k = top[key]
            described.add(key)
            rows.append((key_cell(k), tidy_default(k["default"]),
                         desc_cell(d, not used_elsewhere(k["variable"], sources))))
        md.append("## %s\n" % sec["title"])
        md.append(table(rows) + "\n")

    missing = [k for k in data["top"] if k["key"] not in described]
    if missing:
        md.append("## Not yet described\n")
        md.append("These keywords exist in the code but have no description yet. "
                  "The *Variable* column gives the Fortran variable that is set.\n")
        md.append("| Keyword | Default | Variable |\n|---|---|---|")
        for k in missing:
            md.append("| %s | %s | `%s` |" % (key_cell(k), tidy_default(k["default"]), k["variable"] or "?"))
        md.append("")

    def sub_section(name, prefix, anchor_title, intro):
        md.append("## %s\n" % anchor_title)
        md.append(intro + "\n")
        rows = []
        dsec = desc.get(name, {})
        seen = set()
        for k in data[name]:
            d = dsec.get(k["key"])
            seen.add(k["key"])
            rows.append((key_cell(k, prefix), tidy_default(k["default"]), desc_cell(d)))
        for k in dsec:
            if k not in seen:
                warnings.append("described %s sub-keyword '%s' not found in the code" % (name, k))
        md.append(table(rows) + "\n")

    sub_section("cloud", "cloudN:", "cloudN: sub-keywords",
                "Cloud layers are numbered: `cloud1:`, `cloud2:`, … `cloud0:` applies a "
                "setting to **all** cloud layers (`cloud:` without a number means `cloud1:`). Per-material keywords take "
                "a second index, e.g. `cloud1:abun02=0.3`. A molecule name as sub-keyword "
                "(e.g. `cloud1:H2O=…`) sets the condensation ratio of that species.")
    sub_section("obs", "obsN:", "obsN: sub-keywords", "Observations are numbered `obs1:`, `obs2:`, …")
    sub_section("fitpar", "fitpar:", "fitpar: sub-keywords",
                "Retrieval parameters are not numbered: every `fitpar:keyword=` starts a new "
                "parameter and the following `fitpar:` lines apply to that parameter.")
    sub_section("instrument", "instrumentN:", "instrumentN: sub-keywords", "")
    sub_section("par3d", "par3dN:", "par3dN: sub-keywords", "")
    sub_section("fixmol", "fixmolN:", "fixmolN: sub-keywords", "")
    sub_section("orbit", "orbit:", "orbit: sub-keywords", "")

    (REF / "keywords.md").write_text("\n".join(md))

    # molecules -----------------------------------------------------------------
    mol = ["# Molecules\n",
           "All species ARCiS knows by name (from `molname` in `Modules.f`). Any of these "
           "can be used as an input keyword to set a constant volume mixing ratio, e.g. "
           "`CO2=1d-4`. Names are **case sensitive**. Opacity data for the species must "
           "be present in `opacitydir`.\n",
           "| # | Name | Mass [amu] | | # | Name | Mass [amu] |", "|---|---|---|---|---|---|---|"]
    mols = data["molecules"]
    half = (len(mols) + 1) // 2
    for i in range(half):
        a = mols[i]
        row = "| %d | `%s` | %.3f | |" % (i + 1, a["name"], a["mass"])
        if i + half < len(mols):
            b = mols[i + half]
            row += " %d | `%s` | %.3f |" % (i + half + 1, b["name"], b["mass"])
        else:
            row += " | | |"
        mol.append(row)
    (REF / "molecules.md").write_text("\n".join(mol) + "\n")

    nrev = sum(1 for s in desc["sections"] for d in s["keys"].values() if d.get("review"))
    print("wrote keywords.md (%d keywords, %d described, %d marked for review, %d undescribed)"
          % (len(top), len(described), nrev, len(missing)))
    print("wrote molecules.md (%d species)" % len(mols))
    for w in warnings:
        print("WARNING:", w, file=sys.stderr)


if __name__ == "__main__":
    main()
