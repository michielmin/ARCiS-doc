#!/usr/bin/env python3
"""
Extract the ARCiS input keywords straight from the Fortran source.

Parses
  * ReadAndSetKey   (Init.f)  -> top-level keywords, aliases, target variable
  * ReadCloud       (Init.f)  -> cloudN:<key> sub-keywords
  * ReadObsSpec     (Init.f)  -> obsN:<key> sub-keywords
  * ReadRetrieval   (Init.f)  -> fitpar:<key> sub-keywords
  * ReadInstrument, ReadPar3D, ReadFixMol (Init.f)
  * SetDefaults + CountStuff (Init.f) -> default values
  * molname list (Modules.f) -> molecules that can be used as keywords

Running it writes  docs/reference/keywords.json  which is used by
gen_reference.py to build the reference pages. Run from the repository root:

    python docs/scripts/extract_keywords.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def strip_comment_lines(lines):
    """Drop fixed-form comment lines (c, C, *, ! in column 1)."""
    out = []
    for ln in lines:
        if ln[:1] in ("c", "C", "*", "!"):
            continue
        out.append(ln)
    return out


def subroutine_body(src, name):
    m = re.search(r"^\s*subroutine\s+%s\b.*?$" % name, src, re.M | re.I)
    if not m:
        raise RuntimeError("subroutine %s not found" % name)
    start = m.end()
    end = re.search(r"^\s*end(\s+subroutine\s+%s)?\s*$" % name, src[start:], re.M | re.I)
    # 'end' alone can also close an if-block in sloppy code; we search for the
    # first bare 'end' or 'end subroutine', which is what ARCiS uses.
    return src[start:start + end.start()]


CASE_RE = re.compile(r"^\s*case\s*\((.*)\)\s*(?:!.*)?$", re.I)
CASEDEFAULT_RE = re.compile(r"^\s*case\s+default\b", re.I)
SELECT_RE = re.compile(r"^\s*select\s+case", re.I)
ENDSELECT_RE = re.compile(r"^\s*end\s*select", re.I)


def parse_cases(body, depth_target=1):
    """
    Return list of (aliases, block_lines) for the cases of the outermost
    select-case statement in *body*.
    """
    lines = strip_comment_lines(body.splitlines())
    depth = 0
    cases = []
    cur = None
    for ln in lines:
        if SELECT_RE.match(ln):
            depth += 1
            if depth > depth_target and cur is not None:
                cur[1].append(ln)
            continue
        if ENDSELECT_RE.match(ln):
            if depth > depth_target and cur is not None:
                cur[1].append(ln)
            depth -= 1
            continue
        if CASEDEFAULT_RE.match(ln) and depth == depth_target:
            cur = (["<default>"], [])
            cases.append(cur)
            continue
        m = CASE_RE.match(ln)
        if m and depth == depth_target:
            raw = m.group(1)
            if raw.strip().lower() == "default":
                cur = (["<default>"], [])
            else:
                names = re.findall(r"[\"']([^\"']*)[\"']", raw)
                cur = (names, [])
            cases.append(cur)
            continue
        if cur is not None and depth >= depth_target:
            cur[1].append(ln)
    return cases


def target_of(block):
    """Best guess at the Fortran variable / handler a case sets."""
    txt = "\n".join(block)
    m = re.search(r"read\s*\(\s*key%value\s*,\s*\*\s*\)\s*([A-Za-z0-9_%()]+)", txt, re.I)
    if m:
        return m.group(1)
    m = re.search(r"^\s*([A-Za-z0-9_%(),]+)\s*=\s*(?:trim\()?key%value", txt, re.M | re.I)
    if m:
        return m.group(1)
    m = re.search(r"call\s+(Read\w+)\s*\(\s*key", txt, re.I)
    if m:
        return "→ " + m.group(1)
    if re.search(r"no longer supported|not in use anymore|already set in CountStuff", txt, re.I):
        if re.search(r"already set in CountStuff", txt, re.I):
            return "(read in CountStuff)"
        return "(deprecated)"
    if re.search(r"select case\(key%key2\)", txt, re.I):
        return "(sub-keywords)"
    return ""


def is_deprecated(block):
    return bool(re.search(r"no longer supported|not in use anymore|depreciated mode", "\n".join(block), re.I))


DEFAULT_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_%()]*)\s*=\s*(.+?)\s*(?:!.*)?$")


def parse_defaults(body, prefix_filter=None):
    defaults = {}
    for ln in strip_comment_lines(body.splitlines()):
        m = DEFAULT_RE.match(ln)
        if not m:
            continue
        var, val = m.group(1), m.group(2).strip()
        if var.lower().startswith(("do ", "if")):
            continue
        key = var.lower()
        key = re.sub(r"\(i\)", "", key)
        if key not in defaults:
            defaults[key] = val
    return defaults


def fortran_value(v):
    """Make a Fortran literal more readable: 1d-4 -> 1e-4, keep strings/logicals."""
    if v is None:
        return None
    v = v.strip()
    v = re.sub(r"(?<=[0-9.])[dD](?=[+-]?[0-9])", "e", v)
    v = re.sub(r"(?<=[0-9])\.?e\+?0*([0-9])", r"e\1", v)
    v = v.replace("trim(homedir) // ", "$HOME")
    return v


def main():
    init = (ROOT / "Init.f").read_text(errors="replace")
    modules = (ROOT / "Modules.f").read_text(errors="replace")

    defaults = parse_defaults(subroutine_body(init, "SetDefaults"))
    # CountStuff sets a handful of defaults (nr, pmin, pmax, ...) before SetDefaults
    count_defaults = parse_defaults(subroutine_body(init, "CountStuff"))
    for k in ("nr", "pmin", "pmax", "rp_range", "nrsurf", "freept_fitt", "freept_fitp"):
        if k in count_defaults:
            defaults.setdefault(k, count_defaults[k])
    # do_cia is switched on in Init before CountStuff
    defaults.setdefault("do_cia", ".true.")

    def dflt(var):
        if not var or var.startswith(("→", "(")):
            return None
        base = re.sub(r"\(.*\)", "", var).lower()
        for k in (var.lower(), base, base + "0"):
            if k in defaults:
                return fortran_value(defaults[k])
        return None

    def cloud_dflt(var):
        base = re.sub(r"\(.*\)", "", var).lower()  # cloud(j)%xyz
        m = re.match(r"cloud%(\w+)", base.replace("cloud(j)", "cloud"))
        if not m:
            return None
        k = "cloud%" + m.group(1)
        return fortran_value(defaults.get(k))

    def section(name, default_fn, prefix):
        body = subroutine_body(init, name)
        # the sub-key select is the first (outermost) select case in these routines
        out = []
        for names, block in parse_cases(body):
            if names == ["<default>"]:
                continue
            var = target_of(block)
            v = re.sub(r"\(.*?\)", "", var)
            out.append({
                "key": names[0],
                "aliases": names[1:],
                "variable": var,
                "default": default_fn(var.replace("(j)", "").replace("(i)", "")) if var else None,
                "deprecated": is_deprecated(block),
            })
        return out

    # ---- top-level keywords -------------------------------------------------
    top = []
    body = subroutine_body(init, "ReadAndSetKey")
    for names, block in parse_cases(body):
        if names == ["<default>"]:
            continue
        var = target_of(block)
        top.append({
            "key": names[0],
            "aliases": names[1:],
            "variable": var,
            "default": dflt(var),
            "deprecated": is_deprecated(block),
        })

    def obj_dflt(prefix):
        def f(var):
            m = re.match(r"\w+(?:\(\w+\))?%(\w+)", var)
            if not m:
                return None
            return fortran_value(defaults.get(prefix + "%" + m.group(1).lower()))
        return f

    cloud = section("ReadCloud", obj_dflt("cloud"), "cloud")
    obs = section("ReadObsSpec", obj_dflt("obsspec"), "obs")
    fitpar = section("ReadRetrieval", obj_dflt("retpar"), "fitpar")
    instrument = section("ReadInstrument", lambda v: None, "instrument")
    par3d = section("ReadPar3D", obj_dflt("par3d"), "par3d")
    fixmol = section("ReadFixMol", lambda v: None, "fixmol")

    # orbit:<x> is a nested select inside ReadAndSetKey
    orbit = []
    for names, block in parse_cases(body):
        if names and names[0] == "orbit":
            for n2, b2 in parse_cases("\n".join(block)):
                var = target_of(b2)
                orbit.append({"key": n2[0], "aliases": n2[1:], "variable": var,
                              "default": dflt(var), "deprecated": False})

    # ---- molecules --------------------------------------------------------------
    m = re.search(r"parameter\(molname\s*=\s*\(/(.*?)/\)\)", modules, re.S)
    molecules = [x.strip() for x in re.findall(r"'([^']*)'", m.group(1))]
    m = re.search(r"parameter\(Mmol\s*=\s*\(/(.*?)/\)\)", modules, re.S)
    masses = [float(x) for x in re.findall(r"[0-9]+\.[0-9]+", m.group(1))]

    data = {
        "top": top,
        "cloud": cloud,
        "obs": obs,
        "fitpar": fitpar,
        "instrument": instrument,
        "par3d": par3d,
        "fixmol": fixmol,
        "orbit": orbit,
        "molecules": [{"name": n, "mass": masses[i] if i < len(masses) else None}
                      for i, n in enumerate(molecules)],
    }
    out = ROOT / "docs" / "reference" / "keywords.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1))
    print("top-level keywords: %d" % len(top))
    print("cloud keywords:     %d" % len(cloud))
    print("obs keywords:       %d" % len(obs))
    print("fitpar keywords:    %d" % len(fitpar))
    print("molecules:          %d" % len(molecules))
    print("written to", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
