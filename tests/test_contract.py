#!/usr/bin/env python3
"""
Contract tests. No pytest, no dependencies — this repo should be able to check
itself on a bare Python.

Every fixture here is a bug that actually shipped, or actually nearly shipped.
Report 007 went out with its reference list written as `[1] ...` paragraphs, so
it rendered as body text instead of the IEEE block. Report 008 rendered in a
different typeface than the container intended, because the font stack named
families instead of vendoring files. Those are the tests below.

    python3 tests/test_contract.py

Exits non-zero on the first failure with a diff-shaped message.
"""

from __future__ import annotations

import io
import re
import sys
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import frontmatter  # noqa: E402
import ledger  # noqa: E402
import render  # noqa: E402

PASSED, FAILED = [], []


def case(name):
    def deco(fn):
        try:
            fn()
        except AssertionError as e:
            FAILED.append((name, str(e)))
        except Exception as e:  # noqa: BLE001
            FAILED.append((name, f"{type(e).__name__}: {e}"))
        else:
            PASSED.append(name)
        return fn
    return deco


GOOD_BODY = """
Lightning hit a transmission circuit north of London and the grid began to slow.
This opening paragraph exists so the validator sees a real body, and it starts
with a capital letter because the first paragraph takes a drop cap.

## A Section That Grounds It

Prose here. A citation looks like this [1], and another like this [2].

$$ E = \\tfrac{1}{2} J \\omega^2 $$

| Region | Floor |
|---|---|
| Ireland | 23 GWs |
| ERCOT | 100 GWs |

:::think Try this before reading on
A real question with no answer inside the box.
:::

The answer follows immediately in prose.

## A Second Section

More prose, enough to look like a report without being one.

## A Third Section

Still more.

## A Fourth Section

And a close with some weight.

## References

1. A. Author, "A Real Paper," *A Real Journal*, vol. 1, pp. 1-2, 2020.
2. B. Author, "Another Real Paper," *Another Journal*, vol. 2, pp. 3-4, 2021.
"""

GOOD_META = {
    "seq": "99", "date": "2026-08-24", "category": "Energy",
    "title": "A Fixture Title", "slug": "Fixture",
    "burned": ["First burned item", "Second burned item"],
    "next": ["Somewhere to go next"],
}


def validate(meta=None, body=None):
    """Run the validator, returning (errors_text, warnings)."""
    m = dict(GOOD_META if meta is None else meta)
    b = GOOD_BODY if body is None else body
    buf = io.StringIO()
    try:
        with redirect_stderr(buf):
            warns = render.validate(m, b)
        return "", warns
    except SystemExit:
        return buf.getvalue(), []


def rejects(fragment, meta=None, body=None):
    errs, _ = validate(meta, body)
    assert errs, "expected the validator to reject this, it passed"
    assert fragment.lower() in errs.lower(), (
        f"rejected, but not for the stated reason.\n"
        f"  expected to see: {fragment!r}\n"
        f"  actually said:   {errs.strip()[:400]!r}")


# --------------------------------------------------------------------------- #
# the baseline must pass, or every negative test below is meaningless
# --------------------------------------------------------------------------- #

@case("a conforming fixture passes with no warnings")
def _():
    errs, warns = validate()
    assert not errs, f"the good fixture was rejected:\n{errs}"
    soft = [w for w in warns if "words of prose" not in w and "references" not in w
            and "sections" not in w]
    assert not soft, f"unexpected warnings on the good fixture: {soft}"


# --------------------------------------------------------------------------- #
# report 007's actual bug
# --------------------------------------------------------------------------- #

@case("bracketed reference paragraphs are rejected (report 007's bug)")
def _():
    body = GOOD_BODY.replace(
        '1. A. Author, "A Real Paper," *A Real Journal*, vol. 1, pp. 1-2, 2020.\n'
        '2. B. Author, "Another Real Paper," *Another Journal*, vol. 2, pp. 3-4, 2021.',
        '[1] A. Author, "A Real Paper," 2020.\n\n[2] B. Author, "Another Paper," 2021.')
    rejects("numbered list", body=body)


@case("references must be last in the file")
def _():
    rejects("must be the last thing", body=GOOD_BODY + "\n## An Afterword\n\nTrailing prose.\n")


@case("a citation with no matching entry is rejected")
def _():
    rejects("cited in text but absent", body=GOOD_BODY.replace("[2]", "[9]", 1))


@case("out-of-order reference numbering is rejected")
def _():
    rejects("not 1..n", body=GOOD_BODY.replace("2. B. Author", "3. B. Author"))


# --------------------------------------------------------------------------- #
# structural bans
# --------------------------------------------------------------------------- #

@case("an H1 in the body is rejected")
def _():
    rejects("h1", body="# A Title\n" + GOOD_BODY)


@case("a horizontal rule in the body is rejected")
def _():
    rejects("horizontal rule", body=GOOD_BODY.replace("## A Second Section",
                                                      "---\n\n## A Second Section"))


@case("chat scaffolding is rejected")
def _():
    rejects("chat scaffolding",
            body="Note on today's pick: picking fresh.\n" + GOOD_BODY)


@case("a forbidden phrase is rejected")
def _():
    rejects("forbidden phrase",
            body=GOOD_BODY.replace("Lightning hit", "I couldn't find prior reports, so lightning hit"))


@case("an unbalanced inline dollar is rejected (currency next to math)")
def _():
    rejects("odd number of `$`",
            body=GOOD_BODY.replace("Prose here.", "It cost $1,800 and $x \\ge 0$ held."))


@case("an unclosed think block is rejected")
def _():
    rejects("closing",
            body=GOOD_BODY.replace("A real question with no answer inside the box.\n:::",
                                   "A real question with no answer inside the box."))


@case("a body opening on a lowercase letter is rejected (drop cap)")
def _():
    rejects("capital letter", body=GOOD_BODY.replace("Lightning hit", "lightning hit"))


# --------------------------------------------------------------------------- #
# the ledger contract: burned: is memory, not metadata
# --------------------------------------------------------------------------- #

@case("missing burned: is rejected — it is the ledger's memory")
def _():
    m = dict(GOOD_META); m["burned"] = []
    rejects("ledger", meta=m)


@case("a non-ISO date is rejected")
def _():
    m = dict(GOOD_META); m["date"] = "21 Aug 2026"
    rejects("iso", meta=m)


# --------------------------------------------------------------------------- #
# report 008's actual bug: fonts resolved per-machine
# --------------------------------------------------------------------------- #

@case("the stylesheet vendors its fonts rather than naming families")
def _():
    css = (ROOT / "tools" / "report.css").read_text(encoding="utf-8")
    assert "@font-face" in css, "report.css declares no @font-face"
    srcs = re.findall(r'url\("fonts/([^"]+)"\)', css)
    assert srcs, ("report.css has no vendored font sources. Naming families in a "
                  "fallback stack is what made report 008 render in a different "
                  "typeface than reports 001-007.")
    for s in set(srcs):
        f = ROOT / "tools" / "fonts" / s
        assert f.exists(), f"report.css references a font file that is not in the repo: {s}"
    body_decl = re.search(r"--body:\s*([^;]+);", css).group(1)
    assert "DL Serif" in body_decl, f"--body should lead with the vendored family, got {body_decl!r}"


@case("inline_fonts refuses a stylesheet with no vendored sources")
def _():
    try:
        render.inline_fonts(":root { --body: Georgia, serif; }")
    except SystemExit as e:
        assert "vendored" in str(e).lower() or "font" in str(e).lower()
    else:
        raise AssertionError("expected inline_fonts to refuse a family-name-only stylesheet")


# --------------------------------------------------------------------------- #
# word counting must not count table syntax as prose
# --------------------------------------------------------------------------- #

@case("table rows and display math do not count as prose words")
def _():
    prose = "One two three four five.\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n$$ x = y $$\n"
    assert render.prose_word_count(prose) == 5, (
        f"expected 5 prose words, got {render.prose_word_count(prose)}")


# --------------------------------------------------------------------------- #
# the ledger derivation
# --------------------------------------------------------------------------- #

@case("the archive and the ledger agree")
def _():
    errs, _ = ledger.verify(ledger.load_reports())
    assert not errs, "ledger verify reported errors:\n  " + "\n  ".join(errs)


@case("every report declares burned territory")
def _():
    bad = [r["seq"] for r in ledger.load_reports() if not r["burned"]]
    assert not bad, f"reports with no burned: list {bad}"


@case("next pick never repeats yesterday's category")
def _():
    reports = ledger.load_reports()
    pick = ledger.next_pick(reports, today="2026-08-24")
    assert pick["category"] != reports[-1]["category"] or len(
        {r["category"] for r in reports}) <= 1, (
        f"next pick {pick['category']!r} repeats the most recent category")


@case("the collision checker catches the duplication that started this")
def _():
    reports = ledger.load_reports()
    assert ledger.check("linear programming duality and shadow prices", reports), (
        "LP duality should collide — reports 001 and 005 both covered it")
    assert not ledger.check("the newsvendor problem and inventory theory", reports), (
        "an unburned topic should come back clear")


@case("front matter round-trips through dump and parse")
def _():
    for f in sorted((ROOT / "src").glob("*.md")):
        meta, body = frontmatter.parse(f.read_text(encoding="utf-8"))
        again, _ = frontmatter.parse(frontmatter.dump(meta) + "\n" + body)
        assert again == meta, f"{f.name} does not round-trip: {meta} != {again}"


# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    for n in PASSED:
        print(f"  ok    {n}")
    for n, why in FAILED:
        print(f"  FAIL  {n}\n          {why}")
    print(f"\n{len(PASSED)} passed, {len(FAILED)} failed")
    sys.exit(1 if FAILED else 0)
