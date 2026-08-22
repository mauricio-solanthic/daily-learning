---
name: daily-research-teach
description: Produces the user's daily learning report — one self-contained, deeply researched ~15-minute read on a rotating topic (energy, physics, history of science and invention, geopolitics of resources, economics, philosophy, climate and sustainability, operations research, quantitative finance, cross-domain synthesis), rendered to a print-quality IEEE-cited PDF in a fixed house format and committed to the daily-learning git repository. Use when running the daily learning report, when the daily learning scheduled task fires, or when the user asks for today's report, another installment, or a report on a specific topic in this series.
---

# Daily Learning

Produce one report and commit it. Runs unattended: never ask a question, never
offer a menu of topics, never wait for confirmation. Pick, research, write,
render, commit.

This repository is the whole system: research notes, the ledger, the format
contract, and the archive all live here. If you find yourself writing a
handoff document, something has gone wrong with this skill rather than with
the run.

## Run order

```bash
git clone https://github.com/mauricio-solanthic/daily-learning.git
cd daily-learning
python3 tools/ledger.py next          # 1. what to write, decided for you
                                      # 2. research it (§2)
                                      # 3. write src/NNN_....md (§3, §4)
python3 tools/render.py src/NNN_*.md --outdir reports   # 4. render (§5)
python3 tools/ledger.py index         # 5. regenerate README.md
python3 tests/test_contract.py        # 6. prove nothing broke
git checkout -b report-NNN            # 7. one atomic commit on its own branch (§6)
git add -A && git commit
git push -u origin report-NNN
gh pr create --base main --fill       # 8. open the PR for review (§6)
```

Use absolute paths if you have changed directory. `tools/render.py` resolves its
own assets, but the file you hand it is resolved against your shell's current
directory, which drifts over a long run.

## 1. What to write

`python3 tools/ledger.py next` reads every report's front matter and prints the
next sequence number, the category, and why. **Take what it says.** The category
choice is deliberately not a judgement call — it used to be, and two different
runs picked differently while both following the rules.

It also prints `burned_for_category` and `backlog_for_category`. Choose a
specific sub-topic from the backlog where one fits, then confirm it:

```bash
python3 tools/ledger.py check "your candidate sub-topic in a few words"
```

Exit 0 means clear. Exit 1 lists what it collides with — pick something else. A
loose collision still counts. This check is the whole reason the series stopped
covering linear programming duality three times.

Do not state the rotation in the document. It belongs in the commit message.

## 2. Research

Treat it as a Deep Research task, not a lookup.

- **10–18 searches** for a normal piece, more for a cross-domain synthesis. Fetch
  the actual sources; do not write from search snippets.
- Prioritize peer-reviewed papers, government and institutional data (IEA, EIA,
  ENTSO-E, central banks, national statistics offices), standard textbooks for
  theory, primary documents for history, and original reporting from Reuters, AP,
  FT, the Economist, Nature, Science.
- **Wikipedia is a finding aid, never a citation.** Same for exam-prep and
  study-notes sites, content farms, and unsourced blogs.
- **Cite the paper that actually establishes the claim.** A replication paper
  does not establish a risk premium; a textbook chapter does not establish a
  historical first. Report 007 shipped citing Carr & Lee for the variance risk
  premium, which that paper does not contain.
- Cross-check every load-bearing figure against a second source.
- **Verify arithmetic and attributions in Python.** Recompute every number in a
  worked example and every order-of-magnitude claim. Check who wrote what, in
  which year, and whether they were a co-author or merely a contemporary —
  report 007 shipped crediting Merton as a co-author of the 1973 Black-Scholes
  paper and describing Black's 1976 paper as late-career work.

Read `docs/source-notes.md` before you start and **add to it when you finish.**
It records which hosts are reachable, which redirect, and which decline
automated access. It saves the next run real time, and it is the only part of
this repo that gets more valuable every day.

Some sources decline automated access — `docs.nrel.gov` returns
`ROBOTS_DISALLOWED`, some committee reports return 403. That is the site's
decision and you do not work around it. Find the same document on a host that
permits access (OSTI records and journal versions often do), or cite what is
actually available and record the gap in `docs/source-notes.md`. Note the
pressure this creates: "cite the paper that establishes the claim" plus a
robots-blocked national lab quietly pushes toward whatever happens to be
fetchable. When that has bent a piece, say so in the commit message.

## 3. Audience and voice

An intelligent, technically comfortable general reader who enjoys understanding
how things work across many fields. Nothing more specific.

**The document must be forwardable.** It gets sent to other people.

- Never address the reader's job, employer, industry exposure, or personal
  history. Real industrial cases are excellent — present them as cases, not as
  the reader's own work.
- Generic expository "you" is fine: "suppose you have $m$ supply points."
- No chat scaffolding. No note on the pick, no rotation talk, no "today's read
  will…", no offer to continue, no apology for missing context, no mention of
  skills, schedules, or Claude. The validator rejects several of these outright.

Style: engaging, a little vivid, intellectually serious, never dry — the
register of a very good *Aeon*, *Quanta*, or *Economist* briefing. Precision
matters as much as engagement. Prose paragraphs are the default; headers
organize rather than fragment. No bolded lead-in on every paragraph, no bulleted
study-guide structure, no emoji.

## 4. The source file

One Markdown file in `src/`, named however you like — `tools/render.py` derives
the real filename from the front matter. Line 1 is `---`.

```
---
seq: 9
date: 2026-08-24
category: PLACEHOLDER — take this from `ledger.py next`
title: Title Case Goes Here
slug: ShortCamelCase
deck: One italic sentence of standfirst — the promise of the piece, not a summary.
burned:
  - Each specific sub-topic, anecdote, worked example or framing this piece spends
  - One per line, concrete enough that a later run can collide with it
next:
  - Where this track should go next
---
```

`category` must be exactly one of the ten in `tools/ledger.py`.

**`burned:` is the ledger's memory and the validator rejects a file without it.**
Be concrete. "Grid inertia" is too thin; "Grid inertia, the inertia constant H,
and stored kinetic energy measured in seconds" can actually be collided with.
Include anecdotes and openings you have used up — the Stigler diet problem got
burned only after three separate pieces opened with it.

### Body markup

| What | How |
|---|---|
| Section | `## Title Case Heading` — four to seven |
| Sub-head | `### SHORT LABEL` — sparingly |
| Inline math | `$x \ge 0$` |
| Display math | `$$ ... $$` alone on its lines, blank line either side |
| Table | GFM pipe table, 4 columns max, short cells; numeric columns auto-align |
| Citation | bare `[1]`, `[2]`, `[3], [7]` — no links, no author-year |
| Figure | `![Caption](../figures/NNN-name.svg)` or `.png` |
| Call-out | `:::think Label` … `:::`, one or two, answered in the prose after |

**The reference block.** `## References` must be the last thing in the file, and
the entries must be a Markdown **numbered list**. The stylesheet draws the
brackets.

```
## References

1. F. Black and M. Scholes, "The Pricing of Options and Corporate Liabilities,"
   *Journal of Political Economy*, vol. 81, no. 3, pp. 637-654, 1973.
2. S. L. Heston, "A Closed-Form Solution for Options with Stochastic Volatility,"
   *Review of Financial Studies*, vol. 6, no. 2, pp. 327-343, 1993.
```

Writing `[1] Black and Scholes, …` as a paragraph renders as body text instead of
the IEEE block. That shipped once, in report 007. The validator now rejects it.

Hard bans: no `#` H1, no `---` rule in the body, no footnotes, no HTML. Write
currency as "1,800 dollars" in any paragraph that also contains inline math — a
stray `$` pairs with a math delimiter and swallows the sentence.

### Figures

Put the generating script in `figures/` next to its output, so a figure can be
regenerated and corrected rather than redrawn. Read the `dataviz` skill first,
but only part of it applies to a static figure in a serif PDF:

- **Applies:** choose the chart form before writing code; validate the palette
  with its script; render the figure and actually look at it for label
  collisions and overlaps.
- **Does not apply:** hover layers, tooltips, dark mode, interactive legends,
  and the ≥2-series legend requirement. This is print. Label series directly.

## 5. Render

```bash
python3 tools/render.py /abs/path/src/NNN_....md --outdir /abs/path/reports
```

The filename is derived — `NNN_YYYY.MM.DD_TitleCamel_CategoryCamel.pdf`. Never
type it by hand.

`tools/report.css` **is** the format, and `tools/fonts/` is part of it. The fonts
are vendored on purpose: naming font families in a fallback stack made the output
depend on which machine rendered it, and report 008 came out in a different
typeface than 001–007 for exactly that reason. Do not replace the vendored faces
with family-name lookups, do not restyle a report inline, do not build a bespoke
HTML page, and do not fall back to another PDF tool.

The renderer refuses to produce a PDF on a contract violation, and exits
non-zero **after** writing the PDF if the page count is outside 6–8. Pages are
driven by display math, tables and figures as much as by word count, so the
levers are adding or cutting a table, a figure or a worked example. Fix the
Markdown until it renders clean with no warnings.

Then:

```bash
python3 tests/test_contract.py     # 22 checks, no browser needed
python3 tools/ledger.py verify     # archive and ledger agree
```

## 6. Commit

One commit carries the PDF, the source, any figures, and the regenerated
`README.md`. That atomicity is the point: the old design delivered the PDF first
and updated the ledger afterwards, so an interrupted run left a report that
existed but was never recorded — which is how a category got repeated.

The commit lands on its own branch and goes to Mauricio as a pull request —
never straight to `main`. Nothing is archived until he reviews and merges it,
which he does from his phone.

```bash
python3 tools/ledger.py index
git checkout -b report-NNN
git add -A
git commit -m "008: Energy — grid inertia and RoCoF

Rotation: Energy was the oldest never-covered category.
Sources: 12 searches, 17 fetches; 3 declined automated access (see docs/source-notes.md).
Verified: RoCoF estimate cross-checked against ERCOT's simulation regression."
git push -u origin report-NNN
gh pr create --base main --fill
```

Then **`PushNotification`** with two or three sentences: the topic, why the
rotation landed there, and explicitly whether the PR was opened. A scheduled run
reaches a transcript nobody opens; the notification is the only thing that
actually arrives. Say "opened PR #N" or say what failed.

If the branch push is rejected, rebase and push again. If it fails for any other
reason, say so in the notification and leave the commit local — do not
force-push, and do not start writing a handoff document.

## 7. If the user replies afterwards

Answer what they raise; do not re-summarize the piece. If they flag a repeat, a
factual error, or a topic they want next, put it in the repo — a correction that
only lives in chat is lost. A wrong fact means editing the source, re-rendering,
and committing the fix. A topic they want next goes in the relevant report's
`next:` list, or in `docs/source-notes.md` if it is about access.
