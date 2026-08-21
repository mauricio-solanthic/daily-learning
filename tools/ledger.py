#!/usr/bin/env python3
"""
Daily Learning — the ledger, derived from the archive rather than maintained.

Every earlier ledger bug had the same shape: a hand-written index drifting from
the archive it described. Reports 001 and 005 both covered LP duality, 002 and
003 both covered the simplex family, and report 007's row went missing entirely.
So nothing here is authored. Each report declares in its own front matter what
territory it consumed (`burned:`) and where its track should go next (`next:`),
and this script derives the log, the rotation state and the backlog from the
files on disk. A stale index is not discouraged, it is impossible.

Commands
--------
    ledger.py next            what to write today, as JSON
    ledger.py index           regenerate README.md from src/ and reports/
    ledger.py check "topic"   exit 1 if the topic collides with burned territory
    ledger.py verify          integrity check: pairing, numbering, dates, fields

Run from anywhere; paths resolve against the repo root (the parent of tools/).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
REPORTS = ROOT / "reports"
README = ROOT / "README.md"

# Rotation order. A never-covered category outranks a covered one; ties among
# never-covered categories are broken by this order, which is what makes the
# choice reproducible instead of a judgement call each morning.
CATEGORIES = [
    "Energy",
    "Physics",
    "History of Science",
    "Geopolitics of Resources",
    "Economics",
    "Philosophy",
    "Climate & Sustainability",
    "Operations Research",
    "Quantitative Finance",
    "Cross-Domain Synthesis",
]

# The weekly cross-domain slot. Fixed to a weekday so "roughly weekly" stops
# being a judgement call. 0 = Monday.
CROSS_DOMAIN_WEEKDAY = 4  # Friday

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "to", "for", "with", "as",
    "at", "by", "from", "its", "it", "is", "are", "was", "were", "be", "been",
    "that", "this", "these", "those", "how", "why", "what", "when", "where",
    "problem", "problems", "method", "methods", "theory", "model", "models",
    "and", "into", "about", "any", "all", "its", "their",
}


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #

def load_reports():
    """Every report, newest last, read from src/ front matter."""
    out = []
    for f in sorted(SRC.glob("*.md")):
        try:
            meta, body = frontmatter.parse(f.read_text(encoding="utf-8"))
        except frontmatter.FrontMatterError as e:
            sys.exit(f"ERROR in {f.name}: {e}")
        missing = [k for k in ("seq", "date", "category", "title") if not meta.get(k)]
        if missing:
            sys.exit(f"ERROR in {f.name}: front matter missing {missing}")
        out.append({
            "seq": int(meta["seq"]),
            "date": meta["date"],
            "category": meta["category"].strip(),
            "title": meta["title"],
            "slug": meta.get("slug", ""),
            "burned": meta.get("burned") or [],
            "next": meta.get("next") or [],
            "provenance": meta.get("provenance", ""),
            "src": f,
            "body_words": len(body.split()),
        })
    return sorted(out, key=lambda r: r["seq"])


def pdf_for(rep):
    hits = list(REPORTS.glob(f"{rep['seq']:03d}_*.pdf"))
    return hits[0] if hits else None


# --------------------------------------------------------------------------- #
# rotation
# --------------------------------------------------------------------------- #

def rotation(reports):
    """[{category, last_covered, times_run}] in the order a run should prefer."""
    state = {c: {"category": c, "last_covered": None, "times_run": 0} for c in CATEGORIES}
    for r in reports:
        s = state.get(r["category"])
        if s is None:                       # a category not in CATEGORIES
            s = state.setdefault(r["category"],
                                 {"category": r["category"], "last_covered": None,
                                  "times_run": 0})
        s["times_run"] += 1
        if not s["last_covered"] or r["date"] > s["last_covered"]:
            s["last_covered"] = r["date"]

    order = {c: i for i, c in enumerate(CATEGORIES)}
    return sorted(
        state.values(),
        key=lambda s: (s["last_covered"] or "", order.get(s["category"], 99)),
    )


def next_pick(reports, today=None, weekday=None):
    ranked = rotation(reports)
    last_category = reports[-1]["category"] if reports else None

    if weekday is None and today:
        weekday = datetime.strptime(today, "%Y-%m-%d").date().weekday()

    cross = "Cross-Domain Synthesis"
    cross_state = next((s for s in ranked if s["category"] == cross), None)
    cross_due = False
    if weekday == CROSS_DOMAIN_WEEKDAY and cross_state:
        last = cross_state["last_covered"]
        if not last or (today and
                        datetime.strptime(today, "%Y-%m-%d").date()
                        - datetime.strptime(last, "%Y-%m-%d").date() >= timedelta(days=6)):
            cross_due = True

    if cross_due:
        choice, why = cross, (f"{cross} is the standing slot for weekday "
                              f"{CROSS_DOMAIN_WEEKDAY} and is due")
    else:
        eligible = [s for s in ranked
                    if s["category"] != cross and s["category"] != last_category]
        if not eligible:
            eligible = [s for s in ranked if s["category"] != cross] or ranked
        top = eligible[0]
        choice = top["category"]
        why = ("never covered; first in the rotation order among never-covered "
               "categories" if not top["last_covered"]
               else f"oldest last-covered date ({top['last_covered']})")
        if last_category == choice:
            why += " (no alternative available)"

    return {
        "next_seq": (reports[-1]["seq"] + 1) if reports else 1,
        "category": choice,
        "why": why,
        "avoid_repeating_category": last_category,
        "backlog_for_category": [n for r in reports if r["category"] == choice
                                 for n in r["next"]],
        "burned_for_category": [b for r in reports if r["category"] == choice
                                for b in r["burned"]],
        "burned_all_count": sum(len(r["burned"]) for r in reports),
        "rotation": ranked,
    }


# --------------------------------------------------------------------------- #
# collision check
# --------------------------------------------------------------------------- #

def keywords(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {w for w in words if len(w) > 3 and w not in STOPWORDS}


def check(topic, reports, threshold=2):
    """Report burned entries that share `threshold`+ significant words."""
    want = keywords(topic)
    hits = []
    for r in reports:
        for b in r["burned"]:
            overlap = want & keywords(b)
            if len(overlap) >= threshold:
                hits.append({"seq": r["seq"], "category": r["category"],
                             "burned": b, "shared": sorted(overlap)})
    return hits


# --------------------------------------------------------------------------- #
# README
# --------------------------------------------------------------------------- #

def render_index(reports):
    rot = rotation(reports)
    nxt = next_pick(reports, today=date.today().isoformat())
    L = []
    A = L.append

    A("# Daily Learning")
    A("")
    A("One self-contained, deeply researched ~15-minute read per weekday, rendered to a")
    A("print-quality IEEE-cited PDF in a fixed house format.")
    A("")
    A("<!-- GENERATED FILE — do not edit by hand.")
    A("     Everything below is derived from front matter in src/ and the files in")
    A("     reports/. Regenerate with:  python3 tools/ledger.py index")
    A("     To change what the ledger says, change the report's front matter. -->")
    A("")
    A(f"**{len(reports)} reports.** Next up: **{nxt['category']}** as No. "
      f"{nxt['next_seq']:03d} — {nxt['why']}.")
    A("")

    A("## Log")
    A("")
    A("| # | Date | Category | Title | PDF |")
    A("|---|---|---|---|---|")
    for r in reports:
        pdf = pdf_for(r)
        link = f"[{pdf.name}](reports/{pdf.name})" if pdf else "_missing_"
        flag = " ⚠︎" if r["provenance"] else ""
        A(f"| {r['seq']:03d} | {r['date']} | {r['category']} | {r['title']}{flag} | {link} |")
    A("")

    A("## Rotation state")
    A("")
    A("Ordered as a run should prefer them: never-covered first, then oldest")
    A(f"last-covered. Ties among never-covered are broken by the order in")
    A("`tools/ledger.py`. Cross-Domain Synthesis is a standing weekly slot")
    A(f"(weekday {CROSS_DOMAIN_WEEKDAY}) rather than part of the queue.")
    A("")
    A("| Category | Last covered | Times run |")
    A("|---|---|---|")
    for s in rot:
        A(f"| {s['category']} | {s['last_covered'] or '—'} | {s['times_run']} |")
    A("")

    A("## Burned territory")
    A("")
    A("Spent, in any reframing. A loose collision still counts. Check a candidate with")
    A("`python3 tools/ledger.py check \"your topic\"`.")
    A("")
    for cat in [c for c in CATEGORIES if any(r["category"] == c for r in reports)]:
        rs = [r for r in reports if r["category"] == cat]
        A(f"### {cat}")
        A("")
        for r in rs:
            for b in r["burned"]:
                A(f"- {b} <sub>({r['seq']:03d})</sub>")
        A("")

    A("## Backlog")
    A("")
    A("Where each track should go next, accumulated from the `next:` lists. Advisory,")
    A("not binding — but the Operations Research and Quantitative Finance tracks are")
    A("meant to build rather than restart, so prefer these over starting fresh.")
    A("")
    for cat in [c for c in CATEGORIES if any(r["category"] == c for r in reports)]:
        items = [n for r in reports if r["category"] == cat for n in r["next"]]
        burned_kw = [keywords(b) for r in reports if r["category"] == cat for b in r["burned"]]
        live = [i for i in items
                if not any(len(keywords(i) & bk) >= 2 for bk in burned_kw)]
        if not live:
            continue
        A(f"### {cat}")
        A("")
        for i in live:
            A(f"- {i}")
        A("")

    if any(r["provenance"] for r in reports):
        A("## Provenance notes")
        A("")
        for r in reports:
            if r["provenance"]:
                A(f"- **{r['seq']:03d}** — {r['provenance']}")
        A("")

    return "\n".join(L).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# verify
# --------------------------------------------------------------------------- #

def verify(reports):
    errs, warns = [], []
    if not reports:
        errs.append("no reports found in src/")
        return errs, warns

    seqs = [r["seq"] for r in reports]
    if len(set(seqs)) != len(seqs):
        dupes = sorted({s for s in seqs if seqs.count(s) > 1})
        errs.append(f"duplicate sequence numbers: {dupes}")
    if seqs != list(range(1, len(seqs) + 1)):
        warns.append(f"sequence numbers are not a gapless 1..n run: {seqs}")

    for r in reports:
        if not pdf_for(r):
            errs.append(f"{r['seq']:03d} has a source in src/ but no PDF in reports/")
        if not r["burned"]:
            errs.append(f"{r['seq']:03d} declares no burned: territory — the ledger "
                        f"cannot remember what it consumed")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"]):
            errs.append(f"{r['seq']:03d} has a non-ISO date: {r['date']!r}")
        if r["category"] not in CATEGORIES:
            warns.append(f"{r['seq']:03d} uses category {r['category']!r}, which is "
                         f"not in the rotation list")
        if r["body_words"] < 500:
            warns.append(f"{r['seq']:03d} source body is only {r['body_words']} words "
                         f"— body may not be recovered")

    for pdf in sorted(REPORTS.glob("*.pdf")):
        n = int(pdf.name[:3])
        if n not in seqs:
            errs.append(f"{pdf.name} exists in reports/ but has no source in src/")

    # cross-report burned collisions: the failure this repo exists to prevent
    for i, a in enumerate(reports):
        for b in reports[i + 1:]:
            for ba in a["burned"]:
                for bb in b["burned"]:
                    shared = keywords(ba) & keywords(bb)
                    if len(shared) >= 3:
                        warns.append(
                            f"{a['seq']:03d} and {b['seq']:03d} declare overlapping "
                            f"burned territory ({', '.join(sorted(shared))})")
    return errs, warns


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_next = sub.add_parser("next", help="what to write today, as JSON")
    p_next.add_argument("--date", default=date.today().isoformat())
    sub.add_parser("index", help="regenerate README.md")
    p_chk = sub.add_parser("check", help="does a topic collide with burned territory?")
    p_chk.add_argument("topic")
    p_chk.add_argument("--threshold", type=int, default=2)
    sub.add_parser("verify", help="integrity check")
    a = ap.parse_args()

    reports = load_reports()

    if a.cmd == "next":
        print(json.dumps(next_pick(reports, today=a.date), indent=2))

    elif a.cmd == "index":
        README.write_text(render_index(reports), encoding="utf-8")
        print(f"wrote {README.relative_to(ROOT)} from {len(reports)} report(s)")

    elif a.cmd == "check":
        hits = check(a.topic, reports, a.threshold)
        if not hits:
            print(f"CLEAR — {a.topic!r} does not collide with burned territory.")
            return
        print(f"COLLISION — {a.topic!r} overlaps {len(hits)} burned entr"
              f"{'y' if len(hits) == 1 else 'ies'}:\n")
        for h in hits:
            print(f"  {h['seq']:03d} [{h['category']}] {h['burned']}")
            print(f"      shared: {', '.join(h['shared'])}\n")
        sys.exit(1)

    elif a.cmd == "verify":
        errs, warns = verify(reports)
        for w in warns:
            print(f"  [!] {w}")
        for e in errs:
            print(f"  [x] {e}")
        if errs:
            print(f"\n{len(errs)} error(s). The archive and the ledger disagree.")
            sys.exit(1)
        print(f"OK — {len(reports)} reports, "
              f"{sum(len(r['burned']) for r in reports)} burned entries"
              + (f", {len(warns)} warning(s)" if warns else ""))


if __name__ == "__main__":
    main()
