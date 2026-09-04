# Source access notes

Per-host knowledge, accumulated by runs. **Read this before researching; add to it
when you finish.** It is the only file in the repo that gets more valuable every
day, and it exists because report 008 spent four fetches rediscovering a redirect.

Record: hosts that decline automated access, hosts that redirect, reliable
mirrors, and any substitution you were forced into.

## First: check whether the run has any web access at all

Report 012 was written in a container whose network policy blocked **all**
outbound HTTPS except the Anthropic API, the package registries in `no_proxy`
(pypi, npm, crates, proxy.golang.org) and git-over-HTTPS to GitHub. Every
`WebFetch` returned `EGRESS_BLOCKED`; `curl` returned `CONNECT tunnel failed,
response 403`. Hosts confirmed dead in that session included
`plato.stanford.edu`, `arxiv.org`, `philarchive.org`, `consc.net`,
`journals.publishing.umich.edu`, `survey2020.philpeople.org`,
`link.springer.com` and `www.bls.gov` — the last of which the table below calls
excellent. So a refusal is not always the site's decision, and the tables in
this file describe *site* behaviour, not reachability.

Spend one probe before planning the research, not fifteen:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" --max-time 20 https://arxiv.org/
curl -sS "$HTTPS_PROXY/__agentproxy/status"      # says nothing about the allowlist
```

`000` or a 403 CONNECT on two unrelated hosts means the whole open web is gone
for that run. What still works in that state: `WebSearch` (it goes out through
the API, not through the sandbox), the GitHub MCP tools, `git`, and `pip`/`npm`.

Research is still possible, but it changes shape, and it is worth saying plainly
what is lost: no primary PDFs, so no reading the paper that establishes the
claim. What survives:

- **Pick a topic whose load-bearing content is derivable rather than reported.**
  Report 012 went to Newcomb's problem partly because its central numbers are
  arithmetic on stipulated payoffs — the 0.5005 accuracy threshold is a
  three-line derivation checked in Python, not a figure taken on trust.
- **Search the same fact two or three ways with different phrasings** and keep
  only what comes back consistent. Search backends do read the pages, so a
  figure that recurs across differently-worded queries is better attested than
  one that appears once.
- **Lean harder on arithmetic identities**, which is the one check a summariser
  cannot fake. The 2009 PhilPapers Newcomb split came back as raw counts from
  one query (292 two-boxers, 198 one-boxers) and as percentages from another
  (31.4 and 21.3 per cent); 292/931 and 198/931 reproduce both to two decimals,
  which is what made them safe to print.
- **Bibliographic detail is the one thing search does well.** Titles, journals,
  volumes, page ranges and years cross-check cleanly. Content does not.
- **Say in the commit message which sources you could not read.** Report 012
  never opened Nozick 1969, Gibbard and Harper 1978, either Bourget–Chalmers
  survey paper, or Quattrone and Tversky 1984; the last is cited for its design
  and the direction of its result, not for its numbers, because the reported
  tolerance figures could not be cross-hosted.

### Report 013: the second fully-blocked run, and what it cost

The same total egress block as report 012, confirmed in three calls rather than
fifteen: `curl` returned `000` for `arxiv.org`, `ipcc.ch` and `iea.org`, and
`WebFetch` returned `EGRESS_BLOCKED` for `www.ipcc.ch`, `pmc.ncbi.nlm.nih.gov`
and `ora.ox.ac.uk`. `pmc.ncbi.nlm.nih.gov` is worth naming because it is the
open-access host that would otherwise have served four of this piece's sources
in full; it is blocked by the sandbox, not by NIH. Probe two unrelated hosts and
one `WebFetch`, then stop probing and plan around it.

What made a search-only run survivable was picking a topic whose load-bearing
numbers are arithmetic on published coefficients. Everything that carried weight
in report 013 — the 15/16 zero-warming condition, the 3.75 rate coefficient, the
16-to-1 new-versus-established asymmetry — is three lines of algebra on r = 0.75,
s = 0.25, H = 100 and dt = 20, each of which came back identically from two
differently-worded searches. Two further identities did the verification work
that a fetched PDF would normally do:

- **Burden over emissions must equal the lifetime.** 1,921.79 ppb (NOAA 2024)
  times 2.75 Tg/ppb over 575 Tg/yr (Global Carbon Project, 2010s) gives 9.19
  years against an assessed atmospheric lifetime of 9.1. Three numbers from
  three separate sources, none of which could be read directly, all confirmed at
  once.
- **A modelled ratio against a tabulated one.** Integrating the Joos et al. 2013
  carbon dioxide impulse response and a single methane exponential gives
  GWP20/GWP100 = 3.06; the assessed values give about 3.0. Close enough to
  confirm the shape, far enough to be honest that indirect chemistry is missing.

One caution learned here. Search returns AR6's methane GWP values inconsistently
— 27.0, 27.2, 27.9 and 29.8 all came back for GWP100, and 79.7, 80.8 and 82.5
for GWP20, because fossil and non-fossil rows get conflated. **Do not print an
AR6 metric value to a decimal place from search alone.** Report 013 wrote
"roughly 80 and 27", which is robust to every variant that came back, and the
derived ratio of 3.0 is identical under all of them.

Bibliographic detail again cross-checked cleanly: article numbers, volumes and
author lists for all eight journal references were confirmed by a second,
differently-phrased query. Nothing in the piece is cited for content that could
not be established from at least two independent search returns.

### Report 014: the third fully-blocked run — treat the block as the default

Three runs in a row now (012, 013, 014) have had **all** outbound HTTPS blocked
except the Anthropic API, the package registries and git-over-HTTPS. Assume it.
Report 014 spent exactly three calls confirming it — `curl` returned `CONNECT
tunnel failed, response 403` for `arxiv.org`, `www.nature.com` and
`www.bls.gov`, and one `WebFetch` of an arXiv abstract returned
`EGRESS_BLOCKED` — and then stopped probing and planned around it. Do the same:
two `curl` probes on unrelated hosts plus one `WebFetch`, then move on. The
tables below still describe *site* behaviour, not reachability.

**Pick the topic to survive the block, not in spite of it.** Report 014 went to
branching processes because the entire load-bearing content of the piece is a
fixed-point equation and its consequences. Twenty-five searches supplied history
and bibliography; Python supplied every number. Nothing in the piece rests on a
figure that had to be taken on trust from a summariser. Three kinds of check did
the work a fetched PDF would normally do:

- **An internal consistency identity in the reported facts themselves.** The
  Chicago Pile-1 accounts say the reaction ran 28 minutes at a two-minute
  doubling time and rose by "a factor of around 16,000". Those are two
  independently reported numbers, and 28/2 = 14 doublings with $2^{14} =
  16{,}384$. Both figures confirmed at once, by arithmetic that a summariser
  could not have faked.
- **Deriving a quantity rather than sourcing it.** The pile's multiplication
  factor is not quoted in any source that could be read, so it was recovered:
  period = 120/ln 2 = 173 s, effective generation time 0.081 s from
  β = 0.0065 and a 12.5 s mean precursor lifetime, giving k − 1 = 4.7e−4. A
  derived number with its inputs stated is safer than a fetched one.
- **An asymptotic formula checked against exact fixed points.** S ≈ 2(m−1)/σ²
  was verified against numerically exact extinction probabilities for three
  different offspring laws at three values of m — nine agreements. That is also
  how Haldane's 2s rule was confirmed before being attributed to him.

Two things search does reliably, confirmed again: **bibliography** (every one of
this piece's 22 references had its journal, volume and page range confirmed by a
second differently-worded query, including a 1930 paper in Danish and a 1933 one
in French), and **who got what wrong**, which turns out to be well documented in
the history-of-mathematics literature and to cross-check cleanly.

One thing it does badly, worth naming: **narrow experimental moments**. Two
queries for the prompt-neutron multiplicity moments of thermal U-235 fission
returned 2.41, 4.63 and 6.86 from an unattributable secondary path. They are
almost certainly right — they reproduce Diven's published factor of about 0.80
to three digits — but neither the primary measurement nor a citable evaluation
could be reached, so the piece dropped the sub-Poisson-variance argument
entirely and made the reactor/epidemic contrast on sample size instead (half a
watt is 1.6e10 fissions a second, so the law of large numbers, not the offspring
law, is what makes a reactor predictable). That substitution improved the piece.
**When a number cannot be attributed, look for the argument that does not need
it** rather than softening the sentence around it.

Two smaller notes for the next run. The `pypdf` / distro-`cryptography` panic
recorded below is *not* self-healing — it failed identically on two consecutive
invocations, and `pip install --upgrade cryptography` cannot fix it either
("Cannot uninstall cryptography 41.0.7, RECORD file not found. Hint: The package
was installed by debian"). What did work: `pip install --upgrade cffi`, after
which `from pypdf import PdfReader` imports and page-by-page text extraction
works — the fastest way to find out *which* page a 9-page draft is spilling
onto. And matplotlib's `mathtext.fontset: custom` needs `mathtext.cal`,
`mathtext.sf` and `mathtext.tt` set as well as `rm`/`it`/`bf`, or the figure
script emits a `findfont: Font family ['cursive'] not found` warning; the figure
is fine, but the render is supposed to be warning-free.

### Report 015: the fourth blocked run — and what a second query is actually for

Four in a row (012-015). The block is the default; stop treating it as news. Report
015 spent three `curl` probes (`arxiv.org`, `www.nature.com`, `pubsonline.informs.org`,
all `000`) and one `WebFetch` (`EGRESS_BLOCKED`) and then planned around it.
**`pubsonline.informs.org` is worth naming**, because it is the primary host for
essentially the entire operations-research literature — *Operations Research*,
*Management Science*, *INFORMS Journal on Computing* — and it is blocked by the
sandbox, not by INFORMS. Any OR piece will therefore be written without reading
its own primary sources. Plan for it.

The topic was chosen to survive that, and the rule from 014 held: **pick a subject
whose load-bearing content is computable rather than reported.** Every number in
report 015 — 175,968 patterns, 40 columns, 29 iterations, `z_LP` = 44.287709, 45
reels, the 0.0000/0.0070/1.8247/20.6121 bound table — was computed locally, and
the central claim was checked two independent ways: column generation against the
same LP with all 175,968 columns enumerated (agreeing to 2e-13), and the integer
optimum against the rounded-up relaxation. Nothing quantitative rests on a
summariser. `scipy` is **not** preinstalled and `pip install scipy` works fine;
HiGHS via `scipy.optimize.linprog` and `milp` is enough for real LP and MILP work
inside the sandbox.

Three attribution traps, all caught by a second differently-worded query, all of
which would have shipped as errors on one query:

- **Search stated as fact that Kantorovich's 1939 monograph already contains the
  Gilmore-Gomory pattern formulation.** A second query surfaced Uchoa and Sadykov's
  2026 *Mathematical Programming* paper describing exactly that as a widespread
  misconception — and arguing the real precursor is Kantorovich and Zalgaller's
  1951 book. The cross-check did not confirm the claim; it inverted it, and
  improved the piece.
- **The 1963 Lanchester Prize was for Part II (1963), not the famous 1961 paper.**
  A one-query answer conflates them.
- **Search implied the 1961 paper carried computational results.** It did not;
  Part II does. Asking specifically for the computational details is what
  established the absence.

One numeric contradiction of the AR6-GWP kind. Asked for the largest known
integrality gap in one-dimensional cutting stock, one query returned "raised to
6/5, and no instance known with a gap greater than 7/6" — internally inconsistent,
since 6/5 > 7/6. A second query pinned it to Rietz and Dempe 2008: gaps of 13/11
and 6/5, from 18 and 28 distinct widths. **When a single answer contradicts
itself, it is not a source; re-query rather than picking the half you prefer.**

Bibliography again cross-checked cleanly — all 24 references had journal, volume,
issue and page range confirmed by a second query, including a 2026 paper and a
1958 *Management Science* note. Two smaller notes: the `pypdf` / `cryptography`
panic recorded below is still live and `pip install --upgrade cffi` still fixes it;
and `pdftoppm` is **not** installed, so to actually look at a rendered page use
`pip install pypdfium2` and `PdfDocument(path)[i].render(scale=1.6).to_pil()`.
Eyeballing the PDF is worth the two minutes — it is what confirmed the figure,
the pipe tables and the numeric column alignment survived the render.

### Report 016: the fifth blocked run — and search as a bibliography engine

Five in a row (012-016). Three `curl` probes (`arxiv.org`, `www.nature.com`,
`pdg.lbl.gov`, all `000`) and one `WebFetch` (`journals.aps.org`,
`EGRESS_BLOCKED`), then stop. **`journals.aps.org` and `link.aps.org` are worth
naming for the same reason `pubsonline.informs.org` was**: between them they host
essentially the entire foundational literature of twentieth-century particle
physics — *Physical Review*, *Physical Review Letters*, *Physical Review D* — and
they are blocked by the sandbox, not by APS. Report 016 cited 29 papers, 20 of
them APS, without opening one.

The 014/015 rule held again and is now the settled way to pick a topic under a
block: **choose a subject whose load-bearing numbers are derivable from two or
three measured constants.** Everything quantitative in report 016 came out of
twelve lines of Python on the Fermi constant, three boson masses and nine fermion
masses — the vacuum expectation value 246.22 GeV, the quartic coupling 0.1293,
the gauge coupling 0.6528, the Yukawa ladder from 2.9e-6 to 0.991, the 30 MeV
Higgsless W mass, the 9.2 ps electroweak crossover time. Three checks did the
work a fetched PDF would normally do:

- **A three-way identity between independently measured quantities.**
  $\sin^2\theta_W = 1 - (m_W/m_Z)^2$ gives 0.22321 from the two boson masses
  against a directly determined on-shell 0.22342. Three measurements confirming
  each other to one part in a thousand, from arithmetic a summariser cannot fake.
- **A residual that is itself a known physical quantity.** Pushing the same tree
  relation one step further predicts $\alpha = 1/132.1$ where the measured value
  is $1/137.036$ — and that 3.6 per cent gap is $\Delta r$, whose two dominant
  pieces (5.9 per cent from the running of $\alpha$, minus 3.2 per cent from the
  top loop, recomputed from $\Delta\rho = 3G_F m_t^2/8\sqrt2\pi^2$) reproduce it
  to about a percentage point. A failed check that lands on the right named
  discrepancy is stronger evidence than a passed one.
- **A conservation law in the bookkeeping.** 4 scalars + 6 + 2 vector
  polarisations before breaking = 1 + 9 + 2 after. The table in the piece exists
  because that sum has to come out equal.

Two attribution notes. Search returned "Fritz Meissner" for the 1933
Meissner-Ochsenfeld paper (a rare-book listing); the physicist is **Walther**
Meissner, and a second query said so plainly. And a first query on Anderson 1963
described it as "Anderson's 1962 paper" — the manuscript was received in November
1962 and *Phys. Rev.* 130, 439 appeared 1 April 1963. Both are the ordinary
failure mode: search reports what a page says, including when the page is a
bookseller.

One thing search did better than expected. The single best detail in the piece —
that Nambu was the referee of the *Physical Review Letters* paper he had
effectively caused, and that the sentence predicting the Higgs boson exists only
because *Physics Letters* rejected the earlier version — came back consistently
across three differently-worded queries, from CERN's Higgs10 series, Edinburgh's
own history page and the Ellis-Gaillard-Nanopoulos historical profile. **Named
anecdotes with a documented provenance cross-check as reliably as bibliography
does.** What did *not* firm up was the quoted referee verdict ("of no obvious
relevance to physics"), which every source attributes to "an editor" without
naming one; it was left out rather than hedged.

Two smaller notes. `matplotlib`'s `mathtext.fontset: custom` emits
`No TeX to Unicode mapping for '\__radicalbig__'` for a `\sqrt` in an axis
label — the figure still draws, but write $2^{1/2}$ instead if the run is
supposed to be warning-free. And an inline `$^\pm$` inside a GFM table cell
renders as a stacked glyph in the PDF; spell it out in words.

### Report 017: the sixth blocked run — and a check that beats a fetched PDF

Six in a row (012-017). Three `curl` probes (`arxiv.org`, `www.nature.com`,
`www.sec.gov`, all `CONNECT tunnel failed, response 403` / `000`) and one
`WebFetch` (`arxiv.org`, `EGRESS_BLOCKED`), then stop. **`www.sec.gov` is worth
naming alongside `pubsonline.informs.org` and `journals.aps.org`**: it hosts the
joint CFTC-SEC report on the 2010 flash crash, every SEC concept release, and
the rule filings that document US market structure, and it is blocked by the
sandbox, not by the SEC. `papers.ssrn.com` and `onlinelibrary.wiley.com` were
never reachable either, which between them closes off most of the quantitative
finance literature. Report 017 cited 17 sources without opening one.

The topic was picked to survive that, and the 014/015/016 rule held again.
Everything quantitative in the piece is a derivation, not a report: Kyle's
$\beta$, $\lambda$ and half-revelation result; the Almgren-Chriss trajectory,
half-life and efficient frontier; the capacity ratio. Four checks did the work a
fetched PDF would have done, and one of them is stronger than anything a PDF
could have supplied:

- **A closed form checked against a general-purpose optimiser.** The
  Almgren-Chriss sinh trajectory was compared with SLSQP minimising the same
  $E + \lambda V$ over unconstrained trade lists at four risk aversions. Agreement
  to 0.0 shares at all four, once the variables were scaled to fractions of the
  position — unscaled, SLSQP stopped about 1,500 shares short and made the closed
  form look wrong. **Scale the decision variables before concluding a formula
  disagrees with an optimiser.**
- **Calibration constants that decode.** Almgren and Chriss's $\gamma = 2.5\times10^{-7}$
  and $\eta = 2.5\times10^{-6}$ look arbitrary until you multiply them by 10 per
  cent and 1 per cent of the stated 5-million-share daily volume: both give
  0.125 dollars, the stated bid-ask spread of an eighth. Their $\sigma = 0.95$ and
  $\alpha = 0.02$ likewise reproduce the stated 30 per cent annual volatility and
  10 per cent annual drift on a 50-dollar stock to four digits. Four numbers
  taken on trust from search, all confirmed at once by arithmetic.
- **Monte Carlo against an analytic equilibrium.** Four million paths of the
  single-auction Kyle model returned 499,407 dollars of insider profit against an
  analytic 500,000, noise-trader losses of 499,589, and a posterior variance of
  12.4874 against the predicted 12.5.
- **A ratio that is independent of its inputs.** The two-thirds capacity result
  was derived symbolically and then confirmed numerically on a grid, where the
  cost-to-gross ratio came back 0.666665 for arbitrary $a$ and $b$.

Two attribution traps, both caught by a second differently-worded query. Search
returned **Econometrica volume 74** for Huberman and Stanzl 2004 from two
separate hosts, including Columbia Business School's own faculty page; the paper
is in **volume 72**, issue 4, pages 1247-1275, confirmed by the Econometric
Society's issue index and RePEc. And a first query for Kyle 1985 gave pages
1315-**1336**; RePEc and two other returns give 1315-**1335**. Both are the
ordinary failure mode — search reports what a page says, including when the page
is wrong — and both would have shipped on one query.

What search did well again: **bibliography**, with all 17 references confirmed by
a second query including a 1997 BARRA internal handbook and a 2007 *Journal of
Trading* article whose volume number never firmed up (cited as "Spring 2007,
pp. 59-66" rather than guessed). What it did badly: **index levels on a specific
intraday date**. Three differently-worded queries for where the S&P 500 stood at
2:32 p.m. on 6 May 2010 returned nothing consistent, so the piece dropped the
"well below the opening level" comparison and kept only the derived 1,093-point
average execution, which is arithmetic on two figures the joint report itself
states. **When a comparison cannot be sourced, print the derivation and drop the
comparison** rather than hedging the sentence.

One rendering note. Inline math immediately followed by a comma will strand that
comma at the start of the next line when the math falls near the right margin —
it happened twice in the first render of this piece. The fix is to reword so a
*word* follows the math, not punctuation; a comma removed or a "then" inserted
costs nothing and the problem disappears.

### Report 018: the seventh blocked run — and what actually moves a page count

Seven in a row (012-018). Two `curl` probes (`arxiv.org`, `www.nature.com`, both
`CONNECT tunnel failed, response 403` / `000`) and one `WebFetch`
(`projecteuclid.org`, `EGRESS_BLOCKED`), then stop. **`projecteuclid.org` is worth
naming alongside the other publisher hosts**: it carries *Probability Surveys*, the
*Annals of Probability* and the *Annals of Statistics*, so probability and statistics
join operations research, physics and finance as fields whose primary literature is
unreachable from this sandbox. Report 018 cited 22 sources without opening one.

The topic was picked to survive that, and the 014-017 rule held again: the entire
load-bearing content is one reweighting identity and its consequences, so Python
supplied every number and search supplied only history and bibliography. Four checks
did the work a fetched PDF would have done, and the first is a trick worth reusing:

- **Reconstructing a second moment from a reported mean and a reported size-biased
  mean, to confirm both at once.** Hemenway's 1982 class-size figures — 111 courses,
  mean 14.5, student-experienced "over 78" — are only mutually consistent at a
  coefficient of variation of 2.09, because $14.5 \times (1 + 2.09^2) = 78.1$. The
  three courses he names (105, 171, 229) then account for 31 per cent of enrolments
  and 74 per cent of the second moment. Two numbers taken on trust from a summariser,
  both confirmed by arithmetic that could not have been faked, plus a new fact.
- **Stationary simulation against the closed form.** Probing two million instants
  along long realisations returned mean waits of 4.9998, 5.4134, 7.4955 and 9.9738
  minutes against theoretical 5.000, 5.417, 7.500 and 10.000 for four interval laws.
  The harmonic identity $\mathbb{E}[1/X^*] = 1/\mathbb{E}[X]$ reproduced the base
  mean to four digits on gamma, lognormal and uniform laws.
- **A reported correction checked against the mechanism's own prediction.** Wolfson
  et al. 2001 report dementia survival falling from 6.60 to 3.30 years once length
  bias is removed — a factor of 2.00. Pure length bias on exponential durations
  inflates the median by 2.4213 (the gamma-2 median 1.678 over the exponential's
  0.693) and the mean by exactly 2. The observed factor sits just inside what the
  mechanism predicts, which is how you establish that a reported correction is the
  right size without reading the paper.
- **An implied total from two agencies.** 62.3 million small-firm workers at 45.9 per
  cent of private-sector employment implies 135.7 million private-sector workers,
  which is the right order — so two figures from two separate federal sources confirm
  each other.

Four attribution traps, all caught by a second differently-worded query:

- **Fisher 1934 is "The *Effect* of Methods of Ascertainment upon the Estimation of
  Frequencies"** — singular. The plural "Effects" is what most citing papers write,
  and what a first query returns.
- **Pollaczek 1930 is titled "Über eine Aufgabe der Wahrscheinlichkeitstheorie. I"**;
  Springer's own record carries the numeral, and the Wikipedia-derived citation chain
  drops it.
- **"Variation in Class Size, the Class Size Paradox…" is Feld and Grofman 1977**
  (*Research in Higher Education*, vol. 6, pp. 215-222), not Hemenway 1982. A first
  query merged the two papers into one.
- **Masuda and Porter's "The Waiting-Time Paradox" is 2021, in *Frontiers for Young
  Minds*** 9:582433 — a children's journal, not the physics venue the title suggests.
  Worth knowing before citing it for anything load-bearing.

One near-miss that no cross-check would have caught, because it was a mathematical
claim rather than a sourced one. The draft asserted that the exponential is the only
law whose expected wait equals the whole mean headway. It is not: *any* law with a
coefficient of variation of one does that, a lognormal at CV 1 included, since the
wait is $\mu(1+c^2)/2$. The exponential is unique in that the entire residual-wait
*distribution* equals the interval distribution. **A uniqueness claim about a mean is
almost never a uniqueness claim** — recompute the condition before writing "the only".

What search did badly, again: **tabulated figures that live on one host.** Terada's
own 1922 tram numbers, the Ugander et al. Facebook degree table, TfL's excess-wait-time
table in *Travel in London 2024*, and the Census household-size distribution all
refused to firm up across differently-worded queries. So the piece cites Terada for
the argument and not his figures, and drops the Facebook, London-bus and household
examples entirely rather than hedging them. The firm-size pair survived only because
the two numbers cross-check arithmetically.

### The 9-to-8 page fight, part two — blocks quantise, prose reflows

Recorded because report 018 spent five renders on it and the lesson generalises past
the note under report 014. Cutting roughly 250 words of prose **and** dropping two
whole references moved the page count from 9 to 9. What moved it to 8 was deleting one
table. Prose reflows within the pages it already occupies; tables, figures, display
maths and call-outs cannot be split, so they force breaks and leave light pages behind.

The procedure that works:

1. Get the per-page word profile from `pypdf` (`len(page.extract_text().split())`).
   A saturated body page in this format holds about 500 words.
2. Any page well under that is light because a **block** forced a break there. That is
   the page to attack, and the fix is removing a block from it, not words from it.
3. Report 018's page 7 held 370 words, a heading, two display equations and a
   summary table whose every row was already stated in the prose. Deleting the table
   pulled the whole reference block up one page.

Prefer deleting the block that is a **recap** — a table that restates the prose is the
cheapest thing in the piece — over shortening the argument.

Two smaller notes. The stranded-punctuation problem recorded under report 017 recurred
twice here and is now cheap to *detect* rather than eyeball: extract the text and scan
for lines matching `^\s*[,.;:)]`. Both hits were inline math immediately followed by a
comma or a full stop, and inserting a word after the math fixed both. And
`ledger.py verify` reports a false overlap when two reports both close their `burned:`
list with the boilerplate "Openings now spent - … figure" line, since
*openings / spent / figure* is enough shared vocabulary to trip the checker; reword the
line rather than shipping a warning that means nothing.

Toolchain, for a fresh container: `pip install --upgrade cffi` still fixes the
pypdf / `cryptography` panic, three runs running. `matplotlib` 3.11 with `numpy` 2.4
no longer exposes `np.math`, so a figure script that reached for `np.math.factorial`
needs a plain `import math`.

### Getting a 9-page draft down to 8

Recorded because report 014 lost real time to it. Ninety words of prose cuts
moved the page count not at all: prose reflows within pages 1-7 and the last
page stays saturated. The renderer's own advice (add or cut a table, a figure or
a worked example) is right, but there is a fourth lever it does not mention.
**Find out what is actually on the last page first** — with `pypdf` per the note
above. In report 014 the ninth page held 44 words: the colophon alone, with the
whole reference block fitting on page 8. Nothing in the prose was the problem.
What fixed it was shortening reference *entries* so that four of them dropped
from two rendered lines to one — trimming a series title, a journal's "of Great
Britain and Ireland", redundant issue numbers, `et al.` for a seven-author paper
— plus dropping one reference outright. The one dropped was a textbook cited for
a theorem, repointed at the two papers that actually established it, so the fix
also improved the citations. Reference entries are the cheapest page-count lever
in the format and the easiest to overlook.

## Declines automated access — do not attempt to work around

| Host | Behaviour | What to do instead |
|---|---|---|
| `docs.nrel.gov` | `ROBOTS_DISALLOWED` | The site is declining automated access. Look for the same report on `osti.gov`, or a journal version. If neither exists, cite what is available and record the gap here. Cost so far: three intended primary sources on report 008 (Iberian blackout analysis, NREL/TP-6A20-73856 on inertia, the UNIFI grid-forming specification). |
| Spanish committee report on the April 2025 Iberian blackout | HTTP 403 | Report 008 substituted Transpower New Zealand's system-operator white paper — institutional and citable, but second-hand. Flag the substitution in the piece if the claim is load-bearing. |
| `pubs.acs.org` | HTTP 403 on `/doi/...` | ACS full text is closed to fetches. Look for the same data in a BREF, a USGS commodity summary, or PubChem's HSDB record, which cites CRC and Ullmann's directly. |
| `sciencedirect.com` | `ROBOTS_DISALLOWED` | Elsevier declines automated access on both `/abs/` and `/pii/` paths. Search for a preprint, an institutional PDF, or a Springer/EU equivalent. |
| `tandfonline.com` | `/doi/full/...` returns 403 | The `/doi/abs/...` form sometimes returns title and metadata. Enough to confirm a citation exists — never enough to cite for content. |
| `hansard.parliament.uk` (modern site) | HTTP 403 | Use `api.parliament.uk/historic-hansard/...` instead; same debates, fetches cleanly (see Reliable). |
| `en.wikisource.org` | "This domain is cache-only and cannot be fetched" | Applies to both `Page:` and article namespaces. Report 009 lost Hou Te-Pang's *Manufacture of Soda* and the 1911 Britannica alkali article this way. Find the underlying monograph elsewhere. |
| `journals.uchicago.edu` | `/doi/abs/` gives citation only, no abstract text | Confirms a citation's existence. Do not cite the paper for a claim you could not read — report 009 dropped Gillispie's 1957 *Isis* paper on the Leblanc process for exactly this reason and used two other sources for the prize date. |
| `royalsocietypublishing.org` | HTTP 403 on both `/doi/pdf/...` and `/doi/...` | Applies to papers old enough to be out of copyright. Report 010 lost Glueckauf's 1946 determination of atmospheric helium (5.24 ppm) this way and used Danabalan et al. 2022's 5.4 ppm instead, which is readable and peer-reviewed. Find the value restated in a modern paper rather than citing the original unread. |
| `lyellcollection.org` | HTTP 403 on `/doi/full/...` | The Geological Society's own host declines. Oxford's `ora.ox.ac.uk` carries the accepted manuscript of the same papers in full — that is where report 010 read *The principles of helium exploration*. |
| `repository.arizona.edu` | HTTP 403 on `/bitstream/handle/...` PDFs | Cost report 010 a 1964 thesis on the 1938 helium controversy. Primary diplomatic papers on `history.state.gov` covered the same ground better. |
| `cen.acs.org` | HTTP 406 on article URLs, both `/articles/...` and `/business/...` forms | *Chemical & Engineering News* declines automated access. Other trade coverage of the same story is usually available. |
| `gasworld.com` | Returns the opening paragraphs, then a subscription wall | Applies to `/story/` and `/open-access/` alike. Enough for a single fact with attribution; never enough for a figure table. |
| `interfax.com/newsroom/...` | HTTP 404 on story URLs returned by search | The wire's permalinks rot fast. Look for the same wire copy republished elsewhere. |
| `pubs.aeaweb.org` | HTTP 403 on `/doi/pdf/...` | The AEA's own host declines, so JEP and AER full text is closed. Authors' institutional copies are usually open — `economics.mit.edu/sites/default/files/...` and `hbs.edu/ris/Publication%20Files/...` both served AEA papers in full on report 011. |
| `elischolar.library.yale.edu` | HTTP 403 on `/cgi/viewcontent.cgi?article=...` | Yale's repository declines PDF fetches, which costs the Cowles discussion-paper versions. Nordhaus's history-of-lighting paper is readable as the NBER chapter instead (see Redirects). |
| `hbs.edu/ris/download.aspx?name=...` | Returns an empty document, not an error | Silently useless: the fetch succeeds and the summariser reports it has no content. The `/ris/Publication%20Files/<name>_<hash>.pdf` form of the same paper returns the full text. |
| `pubsonline.informs.org` | Blocked at the egress proxy in every run so far — this is the sandbox, not INFORMS | It hosts *Operations Research*, *Management Science* and *INFORMS Journal on Computing*, so an OR piece cannot read its own primary literature. Bibliographic detail (volume, issue, pages) cross-checks reliably through search; content does not. Report 015 cited 24 papers without opening one of them, and said so. |
| `journals.aps.org`, `link.aps.org` | `EGRESS_BLOCKED` / `000` in every run so far — this is the sandbox, not APS | Between them they host *Physical Review*, *Physical Review Letters* and *Physical Review D*, so any physics piece is written without reading its own primary sources. Volume, issue, page range and received/published dates cross-check reliably through search; content does not. Report 016 cited 20 APS papers without opening one, and said so. `osti.gov/biblio/...` records and `semanticscholar.org` confirm the bibliographic shell of the older ones. |
| `www.sec.gov`, `papers.ssrn.com`, `onlinelibrary.wiley.com` | `CONNECT tunnel failed, response 403` / `EGRESS_BLOCKED` in every run so far — this is the sandbox, not the publishers | Between them they hold the joint CFTC-SEC flash-crash report, most quantitative-finance working papers, and *Econometrica*, *Journal of Finance* and *Journal of Financial Economics*, so a quant piece is written without reading its own primary sources. Volume, issue and page range cross-check reliably through search — with the two exceptions recorded under report 017 — but content does not. Report 017 cited 17 sources without opening one. `ideas.repec.org` and `www.econometricsociety.org` issue indexes are the best second host for the bibliographic shell. |
| `projecteuclid.org` | `EGRESS_BLOCKED` in every run so far — this is the sandbox, not the publisher | It carries *Probability Surveys*, the *Annals of Probability* and the *Annals of Statistics*, so the probability and statistics literature is unreadable too. `arxiv.org` listings and `semanticscholar.org` confirm the bibliographic shell; `ideas.repec.org` does not cover these journals. Report 018 cited 22 sources without opening one. |
| `api.bls.gov` | `CONNECT tunnel failed, response 403` from the agent proxy | Not the site's decision — this session's egress policy does not allow it, so the BLS public data API is unavailable and there is no point retrying. Index levels and rates have to come from BLS's own HTML and PDF pages via `WebFetch`, which work well (see Reliable). |

## Redirects and quirks

| Host | Behaviour | What to do |
|---|---|---|
| `entsoe.eu` PDFs | 302 to `eepublicdownloads.entsoe.eu`; `WebFetch` returns cross-host redirects rather than following them | Go straight to `eepublicdownloads.entsoe.eu`. Report 008 spent four fetches on round-trips. |
| `legislation.gov.uk` | First attempt returned `PROVENANCE_REQUIRED` (permission timeout), not a refusal | Retry, and prefer the `?view=plain+extent` form of the enacted text — that is what returned the 1906 Alkali Act sections verbatim on report 009. |
| `pubchem.ncbi.nlm.nih.gov` compound pages | HTML page renders via JavaScript, so a fetch returns nothing usable | Use the REST view instead: `/rest/pug_view/data/compound/<CID>/JSON?heading=Solubility`. It returns the HSDB record with each value's original citation (CRC, Ullmann's, Merck), which is what you actually want to cite. |
| Large scanned books on `archive.org` | The PDF fetches, but extraction only reaches the front matter and opening chapters | Do not plan a load-bearing figure around a deep page of a scanned monograph. Report 009 lost Kingzett (1877) this way. |
| `geosci.uchicago.edu/~kite/doc/` | 302 to `sseh.uchicago.edu/doc/` | Go straight to the `sseh` path. |
| `history.state.gov` FRUS subchapter index pages | Return document headers and dates only, no telegram text | Fetch the individual `/historicaldocuments/<volume>/dNNN` document pages. The index is still useful for getting the document numbers and dates in one call. |
| `pubs.usgs.gov/periodicals/mcs2026/` | The 2026 edition merges helium into a combined "Helium and Rare Gases" chapter; a broad prompt comes back with the helium and argon rows conflated | Prefer `mcs2025-helium.pdf`, which is a clean standalone chapter and returned its production table verbatim. If you need 2026 numbers, ask for one table row at a time and sanity-check the magnitudes. |
| `link.springer.com/content/pdf/...` for book chapters | Returns metadata, abstract and reference list, not the chapter text | Do not cite a Springer chapter for a value you only saw in its abstract. |
| `nber.org/system/files/chapters/...` | First attempt returned `PROVENANCE_REQUIRED` (a permission timeout), succeeded unchanged on retry | Same pattern as `legislation.gov.uk`. Retry once before concluding anything. These chapter PDFs then return full tables — report 011 got Nordhaus's lighting efficiencies and labour prices out of one call. |
| `nber.org/books-and-chapters/<volume>` | `PROVENANCE_REQUIRED` twice; never returned | Volume landing pages are not worth a third attempt. For editors, series volume and page ranges use `ideas.repec.org/h/nbr/nberch/NNNN.html`, which returns the full bibliographic record and often the chapter's headline result too. |
| `ssa.gov/history/reports/boskinrpt.html` | Serves the whole Boskin report, but a request for a verbatim quotation is refused outright, and a broad request for its bias table came back with **fabricated** component values (0.40 and 0.35) that do not reconcile with the report's own total | The summariser will invent a table rather than say the table was not in the part of the document it saw. Cross-host every table: `gao.gov/assets/ggd-00-50.pdf` and the `govinfo.gov` HTML of the same GAO report both give the real decomposition (0.15 / 0.25 / 0.60 / 0.10 = 1.10). |
| `federalreserve.gov/boarddocs/testimony/...` | Fetches cleanly — but the search result's attribution may be wrong | Always ask the fetch who the byline is. The 29 April 1998 congressional testimony on the CPI is Governor Edward Gramlich's, not Greenspan's, and search results say otherwise. |

## Reliable

| Host | Notes |
|---|---|
| `federalreserve.gov` | FEDS working papers fetch cleanly, including PDFs. |
| `federalreservehistory.org` | Good for framing, thin on figures — do not use it as a numeric source. |
| `measuringworth.com` | Authoritative for historical US index levels. Source of the 282.70 → 224.84 S&P figures in report 007. |
| `academic.oup.com` | Abstracts fetch; full text usually does not. Enough to confirm a citation exists and what it claims. |
| `nobelprize.org` | Primary for prize citations and dates. |
| `api.parliament.uk/historic-hansard` | Outstanding. Returns nineteenth-century debates in full and will quote verbatim on request — report 009's opening figures (5,762 tons of salt a week, 98.72 per cent condensation, 64 works) came straight from the Lords debate of 22 May 1865. Use this, not the modern Hansard site. |
| `legislation.gov.uk` | Statute text, including pre-1900 consolidating Acts. Numerical limits in old law are quotable from the primary source rather than from a secondary summary. |
| `eur-lex.europa.eu` | `legal-content/EN/TXT/HTML/?uri=CELEX%3A...` returns full Implementing Decisions including BAT-AEL tables. Ideal for a modern regulatory number to set against a historical one. |
| `bureau-industrial-transformation.jrc.ec.europa.eu` | Hosts the EU BREF PDFs (the eippcb.jrc.ec.europa.eu path is flakier). Good for per-tonne consumption and emission ranges; ask for specific BAT numbers, since a broad prompt comes back thin on a 700-page document. |
| `pubs.usgs.gov/periodicals/mcs20XX/` | Mineral Commodity Summaries fetch cleanly, one two-page PDF per commodity, with production by country *and* unit price. The natural cross-check for any global tonnage claim. |
| `comptes-rendus.academie-sciences.fr` | Full text of Académie des sciences journals, open access. Peer-reviewed history-of-chemistry articles live here. |
| `nature.com` | Old front-matter articles (1940s) fetch in full — useful for scientific biography and obituaries. |
| `envchemgroup.com` | RSC Environmental Chemistry Group bulletins. Peter Reed's articles on the Leblanc trade and the Alkali Inspectorate are scholarly, cite their parliamentary papers, and carry real numbers. |
| `nber.org/system/files/working_papers/` | Working-paper PDFs fetch in full. |
| `lse.ac.uk` Economic History working papers | Fetch in full; good for industrial price and trade series. |
| `ora.ox.ac.uk` | Oxford's institutional repository. Serves accepted manuscripts in full and will quote sentences verbatim on request — the reliable way around Lyell Collection and several other publisher 403s. |
| `nature.com/articles/...` | Recent papers return the full citation and the key quantitative claims. Enough to cite properly; not a substitute for the PDF if you need a figure. |
| `website.whoi.edu` | Hosts course-reading PDFs of *Nature* papers in full text. Worth trying when the publisher declines. |
| `gazprom.com/projects/` | Design capacities, train counts and commissioning dates for named plants, stated as the operator's own figures. |
| `qatarenergylng.qa` | Per-unit capacities in MMscf/yr with start dates and offtaker shares. Report 010 cross-checked Ras Laffan Helium 2's 1.3 Bscf/yr against Air Liquide's 38 Mm3/yr rating and they agree to 3 per cent. |
| `blm.gov/press-release/` and `doi.gov/ocl/hearings/` | Federal programme history, statutory mechanics and volumes, from the agency that ran the programme. The 2013 Interior testimony is the best single source on the Federal Helium Reserve. |
| `gao.gov/products/` | Report highlights fetch cleanly, with the debt and volume figures that congressional testimony tends to skip. |
| `usitc.gov/publications/332/executive_briefings/` | Two-page trade briefs with sourced figures and named authors. Good for the history of a commodity's supply disruptions. |
| `agbi.com` | Gulf business reporting that names its analysts and their firms, so a figure can be attributed to a person rather than to "industry sources". |
| `bls.gov` | Excellent across the whole site, and the single best host the series has found for statistical methodology. `opub/hom/cpi/*` (Handbook of Methods), `opub/mlr/*` (Monthly Labor Review, with named authors), `opub/btn/*` (Beyond the Numbers), `cpi/quality-adjustment/*`, `cpi/factsheets/*` and the `cpi/additional-resources/*.pdf` files all fetch in full. One caveat: ask one page one narrow question. A broad prompt against `hom/cpi/design.htm` returned the strata-by-area arithmetic and the population coverage; the same prompt asked for formula details it does not contain and simply said so, which is the behaviour you want. |
| `gao.gov/assets/<report>.pdf` | Not just the highlights page — the full report PDF fetches, tables included. The reliable cross-check on any figure that originated in a congressional commission. |
| `govinfo.gov/content/pkg/.../html/...` | HTML renderings of GAO and other federal reports. Fetches cleanly and is the easiest second host for a table you do not want to trust from one read. |
| `finance.senate.gov/imo/media/doc/...` | Senate Finance Committee hearing prints, including the one carrying the Boskin Commission's final report. Good for membership lists and for who said what. |
| `cbo.gov/publication/NNNNN` | Short CBO explainers fetch in full. Source of the 0.25-point expected gap between the traditional and chained CPI in report 011. |
| `federalregister.gov/documents/...` | Full notices, including agency methodology changes that never get a press release. BLS's move to annual single-year CPI weights, and its own estimate of the effect, is only stated properly here. |
| `ilo.org/sites/default/files/wcmsp5/...` | Hosts the ILO/IMF *Consumer Price Index Manual* PDF in full. The authoritative statement of index-number theory when a journal declines — and it names the establishing papers, which lets you cite Diewert or Konues honestly rather than from memory. |
| `econometricsociety.org/publications/econometrica/...` | Exact bibliographic details (volume, issue, page range, month) for old *Econometrica* papers. Use it rather than guessing page numbers. |
| `ssa.gov/news/en/press/releases/...` | Primary for COLA percentages, beneficiary counts and the taxable maximum. The `cola/factsheets/` pages are thinner — the press release carries the counts. |
| `taxpolicycenter.org/taxvox/...` | Named-author posts with the Joint Committee on Taxation scores attached. Not a primary source, but it names its own. |

## Known permanent gaps

Reports whose committed PDF cannot be exactly reproduced from the current
source, and why. `tests/test_contract.py`'s CI render job skips the exact
page-match check for these by name (`KNOWN_GAPS` in `.github/workflows/ci.yml`)
rather than failing on them forever.

- **008** (`GridInertia_Energy`) — Only the prose and equations were recovered
  from the Notion attachment after the original scheduled run shipped with no
  device bridge; the figure (initial RoCoF vs. stored kinetic energy, log
  scale) and its generator script were not found alongside the source. The
  committed PDF is the real, 6-page report with that figure; re-rendering the
  recovered source today produces a reproducible but figure-less 7-page PDF.
  If the generator script ever surfaces, restore it to `figures/`, add the
  figure back into the source, and remove the `KNOWN_GAPS` entry.

## The bias this creates

"Cite the paper that establishes the claim" plus a robots-blocked national lab
pushes each run toward whatever happens to be fetchable, which is not the same as
whatever is best. When that has bent a piece — a second-hand substitution, a
dropped source, a claim you softened because you could not verify a byline — say
so in the commit message rather than letting it disappear.

There is a third version, which report 011 walked into twice. The fetch tool
summarises with a small model, and when a long HTML document's table is not in
the slice it actually saw, it will sometimes *produce a table anyway* rather than
report the absence. Asked for the Boskin Commission's bias decomposition, the
Social Security Administration's copy of the report returned four plausible
numbers, of which two were wrong; they were caught only because the components
have to sum to the total the same fetch had quoted. Two rules follow. Any table
that carries load gets read from a second host before it is written down. And
any number that belongs to an arithmetic identity — components and a total,
shares and a hundred per cent, a rate and its compounded factor — gets checked
against that identity in Python, because the identity is the only part of the
answer the summariser cannot fake. Bylines deserve the same suspicion: search
results attributed the April 1998 congressional testimony on the CPI to
Greenspan, and the document itself says Gramlich.

There is a second version of this problem for anything still unfolding. Report
010 covered a March 2026 supply shock for which no institutional post-mortem
exists yet — the USGS commodity summaries stop at a data year that predates it —
so the load-bearing event figures came from trade and news reporting rather than
from a statistical agency. Search results for a live commodity story are also
dominated by price-tracker content farms, which look authoritative and cite
nothing; of roughly forty hits on the 2026 helium shortage the citable ones were
AGBI, *Foreign Policy*, *The National*, CNBC and C&EN. When sources for a live
event disagree, quote the spread and explain the denominators rather than picking
one — report 010's three competing shock figures (11 per cent, 14 per cent, 5.2
million cubic metres a month) all turned out to be right about different things.


## Toolchain notes for a fresh container

A container cloned from this repo has none of the renderer's dependencies. What
report 012 needed, in order, all of it reachable even when the open web is not:

```bash
pip install Markdown pypdf matplotlib brotli
npm install playwright@1.56.0        # chromium is already at /opt/pw-browsers
```

Do **not** run `playwright install`. `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`
already holds `chromium-1194`, which playwright 1.56.0 accepts, so
`tools/render.py` finds a browser without a download. That also matters for the
CI page-for-page check: the re-render matches only if the local chromium is the
revision CI's pinned playwright would have fetched.

**matplotlib cannot read the vendored fonts, and fails silently.**
`tools/fonts/` holds woff2, which matplotlib's font manager ignores, so
`font.serif: ["TeX Gyre Pagella"]` falls straight through to DejaVu Sans with a
`findfont` warning buried in a wall of repeats. That is report 008's failure
mode wearing a different hat: the figure comes out in the wrong typeface and
nothing errors. The fix, now in `figures/012-newcomb-accuracy-threshold.py` and
worth copying forward, is to decompress the vendored faces at run time and
register those:

```python
from fontTools.ttLib import TTFont          # needs brotli for woff2
face = TTFont("tools/fonts/texgyrepagella-regular.woff2")
face.flavor = None                          # woff2 -> ttf
face.save(tmp / "texgyrepagella-regular.ttf")
matplotlib.font_manager.fontManager.addfont(str(tmp / "..."))
```

The script then asserts the family is actually registered and exits rather than
drawing in a substitute face. Figure scripts for 009-011 name the family and
assume the host has it installed, which is true only on the machine they were
first drawn on.

One smaller quirk: `from pypdf import PdfReader` panicked once against the
distro-installed `cryptography` (`_cffi_backend` missing, then a pyo3
`PanicException`) and imported fine on the next invocation. `tools/render.py`
prints the page count either way, so use its JSON rather than reaching for
pypdf yourself.

## Reaching this repository from a Claude session

Worth writing down because a session lost time to it, and then compounded the
mistake by reading stale numbers rather than saying access had failed.

| Method | Works? | Notes |
|---|---|---|
| `git clone https://github.com/mauricio-solanthic/daily-learning.git` | yes | The repo is public. This is the reliable way to read the real state. |
| `raw.githubusercontent.com/.../main/<path>` | yes | HTTP 200. Good for reading one file without cloning. |
| `WebFetch` on the github.com repo page | yes | Renders the README, including the generated log table. |
| `api.github.com/repos/...` | **no** | The sandbox proxy gates it: *"GitHub access to this repository is not enabled for this session."* Returns the same refusal with or without a token. |
| `github.com/...` HTML pages via `curl` | **no** | 403 at the egress proxy. Not evidence that a link is broken — it will open fine in a browser. |
| `slack.com`, `files.slack.com`, `hooks.slack.com` | **no** | 403 at the egress proxy. This is why announcing to Slack is a GitHub Actions job and not something the daily run does. |

The rule that matters more than the table: **if a lookup fails, say so in the
reply.** A failed call followed by a confident answer from memory is worse than
no answer, because it looks identical to a real one.
