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

### Report 019: the eighth blocked run — and checks that beat a fetched PDF

Eight in a row (012-019). Two `curl` probes (`arxiv.org`, `www.iaea.org`, both `000`)
and one `WebFetch` (`www.iaea.org`, `EGRESS_BLOCKED`), then stop. **`www.iaea.org` is
worth naming alongside the other institutional hosts**: it carries the *Safeguards
Glossary*, the INFCIRC series and the TECDOC reports, so the entire primary
literature of nuclear safeguards is unreachable. Add `www.nrc.gov` PDFs
(`ML*` accession documents) and `world-nuclear.org` to the same list. Report 019
cited 15 sources without opening one.

The 014-018 rule held again and is now beyond question: **pick a subject whose
load-bearing content is derivable from a closed-form expression.** Everything
quantitative in report 019 came out of Dirac's value function and a two-equation
mass balance — 208.03 SWU, the 78 per cent split, 1,172 cascade stages, the 0.175
per cent optimal tails assay, the whole cost stack. Five checks did the work a
fetched PDF would have done, and three are worth reusing:

- **A three-way reconciliation of numbers from three unrelated pages.** Paducah's
  reported peak demand (3,040 MW), the standard diffusion energy intensity (2,400
  kWh/SWU) and the plant's design rating (11.3 million SWU/yr) are three figures
  from three separate hosts. 3,040 MW for a year is 26.6 TWh, and 26.6 TWh at 2,400
  kWh/SWU is 11.10 million SWU — agreement to two per cent. None of the three could
  be read at source; arithmetic confirmed all three at once.
- **Recovering a published machine rating from an unrelated production quota.**
  Centrus's Piketon cascade has 16 centrifuges and an obligation of at least 900 kg
  of 19.75 per cent HALEU a year. From 4.95 per cent feed that is 5,303 SWU/yr, or
  331 SWU per machine, against a separately published AC100 rating of "exceeds 340".
  Two press releases that were never meant to be compared, cross-checking to 3 per cent.
- **Reproducing a published worked example to the last digit.** WNA quotes 7.9, 4.8
  and 4.3 SWU/kg for three enrichment cases; the value function returns 7.923, 4.811
  and 4.339. That is how you establish that the formula in circulation is the right
  one without reading the paper that defines it.

**One contradiction that a second query inverted, and one that it resolved.** A first
query returned "7.9 SWU at 0.25 per cent tails, requiring only 9.4 kg of natural
uranium feed" — but the mass balance gives 10.30 kg, not 9.4. A differently-worded
query produced the full WNA sentence: 9.4 kg is the feed at **0.20 per cent** tails,
10.4 kg at 0.25. The summariser had dropped the clause that made the number true.
**When a quoted figure contradicts an elementary identity, the identity is right and
the quote is truncated** — re-query for the whole sentence rather than softening it.
Separately, the first author of the vacuum-core paper is **Tronin**, not Bogovalov,
whose name search attaches to it because he is the better-known author on it.

**A near-miss that no cross-check would have caught, because it was a modelling
choice rather than a sourced claim.** The piece's headline — 78 per cent of the
separative work to weapons-grade is spent reaching reactor assay — depends entirely
on where the intermediate stage dumps its tails. Dumping them at the natural assay,
so they recycle as first-stage feed, makes the two-stage total *exactly* equal the
single-pass total (agreement to 1.7e-13 across six intermediate assays) and the split
well defined: 77.8 per cent at 4.5 per cent assay. Fixing the second stage's tails at
0.25 per cent instead answers a different question and gives 69.8 per cent, because
that route discards partially-enriched material and so needs more feed overall. Both
numbers are defensible; only the first is a fraction of a fixed total. **Before
printing a percentage-of-total, check that the total is actually invariant** — two
plausible constructions differed by eight percentage points here.

What search did well again: **bibliography**, with all 15 references confirmed by a
second differently-worded query, including a 1951 National Nuclear Energy Series
volume, a 1984 *Rev. Mod. Phys.* review and a 2021 *Annals of Nuclear Energy* article
number. Also **the provenance of a unit**: that Dirac introduced separative work in an
unpublished 1941 note and that Fuchs and Peierls adopted it in a 1942 classified
report came back consistently across three phrasings. What it did badly: **spot
commodity prices**, which are behind paywalls and reach search only via aggregator
posts. UxC and TradeTech returns agreed closely (spot SWU 215 against 200, U3O8 89.60
against 89.75), so the piece prints long-term contract figures rounded to the nearest
dollar and cites UxC's price-indicator series rather than a number from a social-media
screenshot.

Two smaller notes. The renderer's chat-scaffolding check is `^\s*(Today|Note on today)`
with `re.I` and `re.M`, so an ordinary sentence that happens to wrap with **"today's"
at the start of a line** is rejected outright; the fix is to reword, and `grep -ni
"^\s*today"` finds it in one call. And the stranded-punctuation problem from reports
017 and 018 recurred exactly once, again an inline math span followed by a comma;
`re.match(r'^\s*[,.;:)]', line)` over the extracted text caught it, and rewording so a
word follows the math fixed it.

### The 9-to-8 page fight, part three — one table beat 340 words

Report 019 opened at 9 pages and 3,331 words. Cutting 336 words of prose moved the
page count **not at all**, which is now the third run to confirm it. Trimming every
reference entry (dropping an editor, a subtitle, a series number, `et al.` for a
four-author paper) pulled the reference block onto page 8 and left page 9 holding 37
words — the colophon alone, which is report 014's failure mode exactly. What finally
fixed it was deleting **one table**: a five-row price-ratio-to-optimal-tails table
whose every row could be stated in two lines of prose. The block went, the page went
with it, and the prose replacement cost 60 words.

So the order of operations, settled over three runs:

1. Per-page word profile from `pypdf`. A saturated page here holds about 500 words.
2. If the last page holds only the colophon, trim **reference entries** — cheapest lever.
3. If a body page is light, a **block** forced the break there. Delete the block, and
   prefer the one that recaps prose.
4. Prose cuts are for the word-count warning, not for the page count.

One counter-intuitive note: the word-count warning did **not** fire at 2,975 words even
though the stated target is 2,300-2,700, but it did fire at 3,046. The threshold appears
to scale with block count, so removing a table can clear the warning as well as the page.

### Report 020: the ninth blocked run — and a reported assay used backwards

Nine in a row (012-020). Three `curl` probes (`arxiv.org`, `www.nature.com`,
`www.gracesguide.co.uk`, all `CONNECT tunnel failed, response 403` / `000`) and one
`WebFetch` (`www.gracesguide.co.uk`, `EGRESS_BLOCKED`), then stop. **Two host groups are
worth naming for a history-of-technology piece.** `www.gracesguide.co.uk` is the single
best open index of British nineteenth-century engineering biography — obituaries, works
histories, Iron and Steel Institute proceedings indexes — and it is blocked by the
sandbox, not by the site. And `en.wikisource.org` remains cache-only (recorded below
since report 009), which matters more here than usual: the *Dictionary of National
Biography* and 1911 *Britannica* entries that carry the primary chronology of an
inventor's life live there, and neither can be opened. Report 020 cited 25 sources
without opening one.

The 014-019 rule held again, with a new twist worth reusing. The load-bearing content is
stoichiometry and thermochemistry, so Python supplied every number; but the strongest
check in the piece came from **running a reported assay backwards to recover an operating
practice**:

- **A three-way reconciliation from an assay nobody meant as evidence.** Thomas slag was
  sold as fertiliser, so it was assayed to death: 14-18 per cent P2O5 on 45-50 per cent
  CaO. A tonne of 1.9 per cent phosphorus pig iron yields 43.5 kg of P2O5, and those two
  assay bands then *fix* the slag mass (242-311 kg/t) and the lime charge (11-15 per cent
  of the pig iron) with no further input. The independently reported operating practice is
  12-15 per cent. Three numbers from three unrelated literatures — a metal analysis, a
  fertiliser grade and a shop-floor charging rule — none of them readable at source, all
  confirmed at once by arithmetic. **When a by-product was sold, its assay is better
  attested than the process that made it; work backwards from the product.**
- **A rule of thumb that decodes to a slag basicity.** A patent gives "at least 3 kg of
  lime per 0.1 per cent of silicon per tonne of pig iron". One per cent silicon makes 21.4
  kg of silica, so 30 kg of lime against it is a lime-to-silica ratio of 1.40 — the rule is
  a basicity in disguise. Same trick as report 017's Almgren-Chriss calibration constants.
- **A heat balance that inverts.** Standard enthalpies of formation, divided by atomic
  mass, give 32.4 / 24.1 / 9.2 / 7.0 MJ per kg for Si / P / C / Mn. On a Lorraine iron
  (1.9 per cent P, 0.4 Si) phosphorus supplies 47 per cent of the blow, more than the
  carbon; on a haematite iron (0.05 P, 2.0 Si) silicon supplies 62 per cent. The totals
  differ by seven per cent. That inversion is the whole piece, and it is nine lines of
  Python.

**A secondary claim that the arithmetic corrected.** A popular account says the basic
process was not adopted in America because US ores "didn't have sufficient phosphorus to
make the chemistry go" — i.e. a heat argument. Net of the lime each impurity demands,
silicon is still the better fuel (26.4 against 18.9 MJ/kg), so heat is *not* what excluded
silicon from a basic converter; refractory wear on the dolomite lining is. Phosphorus
becomes the fuel only *because* silicon has already been excluded for another reason.
**A causal chain repeated by secondary sources can be checked for direction, not just
magnitude** — and here the arithmetic reversed it.

**One number that would not firm up, and what replaced it.** Crude steel output for
Germany and Britain in 1913 came back as 19.3 / 17.6 / 14 Mt and 10.4 / 7.7 Mt across
differently-worded queries, because territory definitions and steel-versus-pig-iron
conflate. So the piece prints none of them and uses instead the claim that recurred
identically everywhere — German output passed Britain's in 1893 and was more than double
it by 1914 — plus the British ore-import series (208,000 t in 1870 to 7,442,000 t in
1913), which is one figure from one 1918 *Nature* note and survives because its 8.7 per
cent compound growth is derivable. Same lesson as report 017's intraday index level:
**when a level will not firm up, print the ratio.** Two related figures also stayed out:
Luxembourg's minette tonnage, whose only source was a Springer chapter whose book title
and authors never surfaced, and the share of German steel made by the Thomas process,
which returned nothing for 1900-1913 at all.

**Two invented-authorship traps, both self-inflicted.** Search returns a paper's title,
journal, volume and pages reliably (all 25 references here cross-checked) but often not
its author list. The temptation is to write "G. Branca and others" because a plausible
name appeared nearby. Four of this piece's references were drafted that way and all four
were wrong or unverifiable; the fix is to cite the title with no author, which IEEE style
permits and which is honest. **An unverified author list is a fabrication in exactly the
way report 007's Carr-and-Lee citation was.**

One rendering note, and one repo-mechanics note. The renderer's chat-scaffolding check
also scans the `slack:` field, so an ordinary clause like "modern converter slag" is fine
but "today's converter slag" is rejected outright — the same `^\s*(Today|Note on today)`
pattern recorded under report 019, applied to front matter. And a first section heading
identical to the report's own title renders as a visible stutter under the standfirst;
the validator does not catch it, so read the first page.

### The 8-to-7 page fight — merging two references beat deleting a table

Report 020 rendered at 8 pages with the last page holding 39 words: the colophon alone,
report 014's failure mode exactly. Trimming publisher names and cities from twelve
reference entries moved page 7 from 493 to 440 words and the page count **not at all**.
What fixed it was noticing that references 11 and 12 were two US patents with the *same
title* (3,932,172 and 3,938,790, "Method and Converter for Refining Pig-Iron into
Steel") and merging them into one entry. That removed a numbered item and two rendered
lines, and the colophon came up onto page 7.

So there is a fifth lever, cheaper than deleting a block and cheaper than trimming prose:
**look for two references that are really one.** Same-title patents in a family, a paper
and its preprint, two chapters of one report. Merging costs nothing bibliographically and
frees a whole entry. The order of operations is now:

1. Per-page word profile from `pypdf`. A saturated page here holds about 500 words.
2. If the last page holds only the colophon, look for **two references that can merge**,
   then trim reference entries.
3. If a body page is light, a **block** forced the break there. Delete the block, and
   prefer the one that recaps prose.
4. Prose cuts are for the word-count warning, not for the page count.

Toolchain, unchanged and confirmed again: `pip install Markdown pypdf matplotlib brotli
fontTools` then `pip install --upgrade cffi` for the pypdf / `cryptography` panic (four
runs running), and `npm install playwright@1.56.0` with no `playwright install`. One new
note: `pip install` against `files.pythonhosted.org` timed out twice mid-run on large
wheels and succeeded on a plain retry, so a `ReadTimeoutError` there is not the egress
block — just retry it.

### Report 021: the tenth blocked run — and a unit conversion as a cross-check

Ten in a row (012-021). Three `curl` probes (`arxiv.org`, `pubs.usgs.gov`, `www.nature.com`,
all `000`) and one `WebFetch` (`pubs.usgs.gov`, `EGRESS_BLOCKED`), then stop. **The row for
`pubs.usgs.gov` in the Reliable table below is now wrong for this sandbox and should be read
with the header warning in mind**: the Mineral Commodity Summaries are the single most useful
host for any resource-geopolitics piece — one clean two-page PDF per commodity with production
by country, reserves, unit values and a substitutes paragraph — and they are blocked at the
egress proxy, not by USGS. Reports 009 and 010 read them directly; report 021 could not, and
cited four USGS publications without opening one. Plan a commodity piece around that.

The 014-020 rule held again, with a twist: **when the load-bearing content is an economic
argument rather than a physical law, the derivable core has to be a break-even rather than a
value.** Report 021's central claim — that niobium's monopoly is unexercised because the real
competitor is non-use — rests on the price at which the additive costs as much as the steel it
saves, and that price is Barlow's formula plus one USGS unit value: 26 dollars a kilogram on
0.5 kg per tonne is 13 dollars, over 0.351 tonnes of steel displaced, is 37 dollars a tonne.
No steel price had to be sourced at all, which is the same move as report 020's "print the
ratio when the level will not firm up", applied one level earlier — **choose the quantity that
does not need the unsourceable input**.

Four checks did the work a fetched PDF would have done:

- **An intensity ratio confirming a disputed tonnage.** USGS's world niobium estimate jumps
  from 83,000 t (2023 data year) to 112,000 t (2024) — a third in one year, and search returns
  both confidently. Dividing by worldsteel's crude steel totals gives 43.9 and 59.5 grams of
  niobium per tonne of steel; the intensity independently reported in the trade literature is
  55 to 60 g/t. The ratio adjudicates between two levels neither of which could be read.
  The same check run on the United States (8,400 t apparent consumption over 81.4 Mt of steel
  = 103 g/t against a reported ~100 for advanced economies) confirms it a second way.
- **The same check pointing the other way, and saying so.** The dominant producer's own
  reported 2023 sales, 92,000 t of "ferroniobium equivalent", are 59,800 t of contained
  niobium at 65 per cent — 72 per cent of the 83,000 t world figure but only 53 per cent of
  the 112,000 t one, and only the first is compatible with the 75-80 per cent share the company
  is credited with. **Two arithmetic checks disagreeing is a finding, not a failure**: the piece
  prints both and makes the un-auditability of a single-private-seller market part of the
  argument, rather than picking the level it preferred.
- **A materials constant reported in two unit systems.** The Hall-Petch coefficient for ferrite
  comes back as 17.4 MPa mm^(1/2) (Pickering's form) from one query and 600 MPa um^(1/2) from
  another. Converted, 0.5502 and 0.6000 MPa m^(1/2) — agreement to 9 per cent between two
  figures that look nothing alike. **A quantity quoted in two units is a free cross-check;
  convert before assuming they are different claims.**
- **A pound-to-tonne conversion validating a trade-press figure.** A 2026 Defense Logistics
  Agency solicitation is reported as "1,288,082 lb, or 584.3 t". That converts to 584.27 t,
  agreeing to 0.01 per cent, which is enough to establish that the reporter had the primary
  notice in front of them rather than a rounded secondary. Cheap, and it is the only
  verification available on a live procurement.

**One number deliberately not divided.** The same solicitation carries a ceiling of 160 million
dollars, and 160 m over 584.3 t is 274 dollars a kilogram of ferroniobium — ten times the
commodity grade. That may well be right for vacuum-grade material, or the ceiling may cover
option years the report does not describe. The piece prints both figures as reported and
instead uses the ratio that needs no assumption (160 m is 5.5 per cent of one year of the world
market). **When two reported numbers might not share a denominator, use them separately.**

**Three attribution traps, all caught by a second differently-worded query.**

- **The Smith-Zener relation is Smith's paper, crediting Zener.** One search return cites it as
  "Zener, C. and Smith, C. (1948)"; the paper is C. S. Smith alone, *Trans. AIME* 175, 15-51,
  "Introduction to Grains, Phases, and Interfaces", and the argument is credited in it to Zener
  by private communication. Writing Zener as a co-author would have been report 007's
  Carr-and-Lee error exactly.
- **Irvine, Pickering and Gladman 1967 was dropped rather than guessed.** Search confirms
  *J. Iron Steel Inst.* 205, 161, 1967 but never returns the title, and returns the solubility
  product itself three inconsistent ways — as a product (log[Nb][C] = 2.26 - 6770/T), as a
  quotient, and in a constants table as A = 6770 with B = 1.03 rather than 2.26. So the piece
  cites neither the paper nor the constant and puts the quantitative weight on the Smith-Zener
  limit and the Hall-Petch relation, whose constants do cross-check. **A constant that comes
  back three ways is not a constant yet.**
- **Baker's "Microalloyed steels" review is in *Ironmaking and Steelmaking*, vol. 43, no. 4,
  2016**, not *International Materials Reviews* vol. 61 — the same DOI appears under both on
  different platforms, and the author's own institutional repository labels it "an invited
  review for Ironmaking and Steelmaking". Prefer the author's repository over the aggregator
  when two journals claim one DOI.

What search did well: **corporate-transaction detail**, which cross-checks unexpectedly cleanly.
The two September 2011 tranches (1.95 and 1.8 billion dollars for 15 per cent each), the five
Chinese and six Japanese-Korean buyers by name, the 2.5 per cent each, the Niobec sale (530 m,
of which 500 m cash) and the CMOC-Anglo American deal all came back consistent across
differently-worded queries, and the two implied enterprise values (13.0 and 12.0 billion) agree
to 8 per cent, which is itself a check. What it did badly: **copper reserves**, of all things —
three phrasings returned world copper production (23 Mt) reliably but no reserve figure, so the
piece drops the reserves-to-production comparison and keeps only the mass ratio, which is two
confirmed numbers. And **ferroniobium spot prices** are the report 019 problem again: every
first-page hit is a price-tracker content farm quoting yuan per kilogram of niobium metal, which
is a different product. The USGS *import unit value* is the citable figure and it is stable
(21, 25, 25, 26, 26 dollars per kg of contained niobium, 2021-2025).

One figure-mechanics note. On a log x-axis, `ax.set_xticks([...])` leaves the **minor** tick
labels in place, so hand-chosen major labels ("2.5", "5", "10") render on top of matplotlib's
own "$4\\times10^0$" minor labels. `ax.set_xticks([], minor=True)` clears them in one line;
this cost two renders to spot because the collision is only visible at figure scale.

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
| `www.iaea.org`, `www-pub.iaea.org`, `www.nrc.gov`, `world-nuclear.org` | `EGRESS_BLOCKED` / `000` in every run so far — this is the sandbox, not the agencies | Between them they hold the *IAEA Safeguards Glossary*, the INFCIRC and TECDOC series, the NRC's `ML*` accession PDFs on enrichment processes, and the World Nuclear Association's information papers and fuel reports — so the whole institutional literature of the nuclear fuel cycle is unreadable. Worth knowing that these are the hosts a nuclear piece most wants. Titles, document numbers and worked-example figures cross-check reliably through search; a WNA worked example can be *verified* rather than trusted, because its numbers are reproducible from the value function (see report 019). Report 019 cited 15 sources without opening one. |
| `www.gracesguide.co.uk` | `CONNECT tunnel failed, response 403` / `EGRESS_BLOCKED` — this is the sandbox, not the site | The best open index of British nineteenth-century engineering biography: obituaries, works histories, and the Iron and Steel Institute's own proceedings indexes. Any history-of-technology piece on British industry wants it. Dates, patent years and meeting dates cross-check reliably through search; the quoted council minutes and obituary text do not. Report 020 cited 25 sources without opening one. Pair this with the `en.wikisource.org` row: between them they hold the *Dictionary of National Biography* and 1911 *Britannica* lives that carry an inventor's primary chronology. |
| `pubs.usgs.gov` | `000` / `EGRESS_BLOCKED` on report 021 — this is the sandbox, not USGS, and it contradicts the Reliable row below, which reports 009 and 010 earned | It hosts the *Mineral Commodity Summaries* (one clean two-page PDF per commodity: production by country, reserves, unit values, substitutes) and the *Minerals Yearbook* chapters, so it is the first host any resource-geopolitics piece wants. Country shares, reserve totals and import unit values cross-check reliably through search, and an intensity ratio against a second agency's output series can adjudicate between two conflicting tonnage estimates (see report 021). Report 021 cited four USGS publications without opening one. Probe it before planning; the Reliable row may be true again in another sandbox. |
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

### Report 022: the eleventh blocked run — and a Monte Carlo that beat a fetched PDF

Eleven in a row (012-022). Three `curl` probes (`arxiv.org`, `www.newyorkfed.org`,
`www.federalreserve.gov`, all `CONNECT tunnel failed, response 403` / `000`) and one
`WebFetch` (`www.newyorkfed.org`, `EGRESS_BLOCKED`), then stop. **Two host groups are worth
naming for any macroeconomics or monetary-policy piece.** `www.newyorkfed.org` is the
publisher of the LW and HLW r-star estimates themselves — the staff reports, the real-time
estimates spreadsheet, the suspension and resumption press releases — and it is blocked by the
sandbox, not by the Bank. So is `www.federalreserve.gov`, which the Reliable table below
rightly calls excellent for FEDS working papers; read that row with the header warning. The
regional banks' own research (`clevelandfed.org`, `richmondfed.org`, `frbsf.org`) is where the
comparative r-star work lives and none of it could be opened either. Add
`link.springer.com`, `direct.mit.edu` (*Review of Economics and Statistics*) and
`www.tandfonline.com` for the journal side. Report 022 cited 20 sources without opening one.

The 014-021 rule held, and this run is the cleanest case of it yet: **when a topic's central
object is an estimator, you can run the estimator yourself.** Everything quantitative in
report 022 came out of about eighty lines of numpy on the local level model — the Riccati
fixed point, the steady-state gain, the mean lag, the pile-up frequencies, the revision
statistics. Nothing rests on a summariser. Four checks did the work a fetched PDF would have
done, and the first is the strongest verification this series has managed:

- **Reproducing a 1990 published probability by simulation.** Shephard and Harvey report that
  when the true signal-to-noise ratio is zero, Gaussian ML returns exactly zero with
  probability 0.96 under a fixed initial level and 0.66 under a diffuse prior. Twenty thousand
  diffuse-start samples of 250 quarters returned 65.0 per cent. That is a thirty-five-year-old
  result in a paper that could not be opened, confirmed to one percentage point by arithmetic
  the summariser could not have faked — and it then licensed the *unpublished* numbers the
  piece actually needed (13.6 per cent zeros at HLW's own lambda of 0.040, 21.3 per cent at
  0.030). **Validate your own simulation against the one number the literature does report,
  then use it for the numbers it does not.**
- **A closed form checked against the recursion it summarises.** The steady-state gain
  `K = p/(p+1)` with `p = (q + sqrt(q^2+4q))/2` matched two hundred thousand iterations of the
  Riccati recursion to machine precision at four values of q, and the EWMA mean lag computed by
  summing `j*K(1-K)^j` over four thousand terms matched the analytic `(1-K)/K` exactly.
- **A named constant falling out of the algebra.** At unit signal-to-noise the fixed point is
  `p^2 - p - 1 = 0`, so p is the golden ratio and K is its reciprocal, 0.6180339887 to ten
  digits. A landmark like that in the middle of a numerical check is free confirmation the
  algebra is right.
- **An arithmetic identity inside a set of reported figures.** The Richmond Fed brief's four
  2024 Q2 estimates (0.55, 0.74, 1.22, 2.6) and its stated range "0.55 to 2.6" have to agree,
  and they do — min and max exactly. That is what made it safe to build the policy-stance
  table on them.

**One transient that looked like a broken formula.** The simulated real-time RMS error came
back 0.1244 against a theoretical `sqrt(K)` of 0.1136 at lambda = 0.013 — a 10 per cent gap,
where lambda = 0.040 agreed to three digits. The formula was fine: at that gain the filter's
transient has a half-life of 53 quarters, so trimming 40 observations from each end of a
250-quarter sample does not reach steady state. Re-running with T = 3,000 and discarding the
first 1,000 gave 0.1140 against 0.1136. **Before doubting a steady-state formula, check that
the simulation actually reached the steady state** — the same failure mode as report 017's
unscaled SLSQP, wearing a different hat.

**Three attribution traps, all caught by a second differently-worded query, all of which would
have shipped on one.** Laubach and Williams's "Redux" is *Business Economics* vol. 51,
**pp. 57-67** — a first query returned 257-267, and only the second, which came back with a
substantive abstract attached, settled it. Buncic's critique was drafted from its Riksbank
working-paper title ("Econometric issues *with Laubach and Williams'* estimates…") and is
published as "Econometric issues *in the estimation of* the natural rate of interest",
*Economic Modelling* vol. 132, art. 106641, 2024 — the working-paper title is not the article
title. And Del Negro et al.'s BPEA page range came back as both 235-294 and 235-316; the
official Brookings and RePEc records give **235-316**, which is the BPEA convention of
including the published comments.

**One author list deliberately left off.** The widest uncertainty band the piece quotes — a 95
per cent interval on the two-sided LW estimates running from about +5.5 to -4.5 per cent —
comes from a section of the Hoover volume *The Structural Foundations of Monetary Policy*
(Bordo, Cochrane and Seru, Eds., 2018). Search attaches Cochrane's name to it because the PDF
filename carries it, but he is an editor of the volume and no query confirmed him as the
section's author, so the reference gives the section title and the editors and no author. That
is report 020's lesson applied in advance rather than after the fact. The band is also
attributed in the prose as a survey chapter's *reading* of a figure, not as LW's own reported
standard error, because the latter could not be sourced.

**What search did badly: the FOMC's own longer-run dot.** Four differently-worded queries for
the median longer-run federal funds rate in specific SEP vintages returned nothing consistent
(4.25 per cent for January 2012 and 2.5 for 2019 were never confirmed; June 2026 came back as
both "3.1 per cent" and "around 3 per cent"). The series is on FRED as `FEDTARMDLR` and FRED
is unreachable. So the piece drops the dot-plot series entirely and uses instead the federal
funds *target range*, which is unambiguous and which every source agrees was 5.25-5.50 per cent
from July 2023 to September 2024 — enough to compute the policy stance against four r-star
estimates. **When a level series will not firm up, look for the administered number in the
same sentence**, which is usually better attested than any estimate.

What search did well, again: **bibliography** (all 20 references had journal, volume, issue and
page range confirmed by a second query, including a 1990 *Journal of Time Series Analysis*
paper and a 2024 article number), and **institutional chronology** — the November 2020
suspension of LW and HLW publication after the Q2 2020 release, and the May 2023 resumption
updated through 2022 Q4, came back identically across three phrasings.

One repo-mechanics note and one figure note. `ledger.py verify` flagged a false overlap
between 011 and 022 on *error / noise / standard*, from a burned line reading "real-time
standard error equal to sqrt(K) times the noise scale"; rewording it to "real-time filtered
uncertainty as sqrt(K) times the observation scale" cleared it, the same fix as report 018's
boilerplate collision. And naming a numpy array `GRID` in a figure script shadows the
`GRID` colour constant that all of these scripts define at the top, and the failure surfaces
as matplotlib complaining that a 301-element float array "is not a valid value for color" —
one glance at the traceback's array literal is enough, but only if you know to look for the
shadow rather than for a palette bug.

### Report 023: the twelfth blocked run — and a denominator that nearly shipped wrong

Twelve in a row (012-023). Five `curl` probes this time, all `000`, and they are worth naming
because they are the entire primary literature for a philosophy piece:
`plato.stanford.edu`, `philpapers.org`, `arxiv.org`, `www.jstor.org` and
`academic.oup.com`. The last is where the 1976 *Aristotelian Society Supplementary Volume*
itself lives, so a report on moral luck was written without opening either of the two papers
that created the subject. Add `onlinelibrary.wiley.com`, `compass.onlinelibrary.wiley.com`,
`www.sciencedirect.com`, `link.springer.com`, `www.cambridge.org`, `pubmed.ncbi.nlm.nih.gov`
and `crashstats.nhtsa.dot.gov` — every one of report 023's twenty sources was cited unread.
Probe two or three hosts, then stop; the tables above still describe *site* behaviour, not
reachability.

The 014-022 rule held again, in its philosophy-shaped form: **pick a topic whose load-bearing
content is an argument plus arithmetic on published counts.** Everything quantitative in
report 023 is either three lines of Bayes or a variance decomposition on two published
totals, and both were checked in Python before a word was written. Three checks did the work
a fetched PDF would have done:

- **Three independent internal identities inside the NHTSA release.** 12,429 alcohol-impaired
  deaths out of 40,901 road deaths is 30.39 per cent against a reported "30 per cent";
  525,600 minutes divided by 12,429 is 42.3 against a reported "every 42 minutes"; and the
  7,494 impaired drivers among those deaths is 60.3 per cent against a reported "60%". A
  figure that satisfies three separately-reported relations is not a summariser's invention.
- **An identity that recovers a number the source never states.** The CDC's episode totals
  and its rates per thousand adults are published side by side but never divided. 112e6/0.479
  = 233.8 million and 121e6/0.505 = 239.6 million, which is the US adult population in 2010
  and 2012 to a fraction of a per cent. Two survey years, two independent confirmations, one
  division each. **When a source reports a total and a rate, divide them and see what
  population falls out.**
- **A Monte Carlo against the closed form.** Forty million lognormal agents reproduced
  Var(c) = 1.699e-8 and corr(c, H) = 0.0131 against analytic 1.6988e-8 and 0.01307.

**The mistake that nearly shipped, and how it was caught.** NHTSA's sentence reads "Of the
12,429 people who died in alcohol-impaired-driving traffic crashes in 2023, there were 7,494
drivers (60%) who were alcohol-impaired." A first pass read 7,494 as *impaired drivers
involved in fatal crashes* and built the whole piece's central rate on it. It is not: it is
impaired drivers **killed**, a subset of the 12,429 deaths, and the 60.3 per cent identity is
what makes that unambiguous. The fix was to stop trying to count crashes at all and quote an
exact ratio of two published totals instead — deaths per episode, 12,429/125e6 — flagged in
the prose as an upper bound on the per-episode probability because one crash can kill several
people. **When a reported count could be "involved" or "killed", check it against the
percentage reported alongside it, and if the event you want is not directly counted, publish
the ratio you can defend and say what it bounds.** Every downstream number and the figure had
to be recomputed; doing it before drafting cost twenty minutes rather than a re-render.

Two smaller notes. Search returned **1987** and **1989** for Lewis's "The Punishment That
Leaves Something to Chance" (PhilPapers says 1987); the journal's own volume listing gives
*Philosophy & Public Affairs* vol. 18, no. 1, Winter **1989**, pp. 53-67, and a second query
naming the volume and issue settled it. And the FBI's DUI arrest count comes back almost
entirely through law-firm and statistics-aggregator pages rather than from `cde.ucr.cjis.gov`
— 804,926 for 2024 recurred across differently-worded queries and is used, but a UCR figure
reached only through content farms deserves the caution report 010 recorded for commodity
prices.

One renderer note worth keeping. A draft at 3,133 prose words warned that the target is
2,300-2,700; at 2,975 words, with the same table, figure and two display-math blocks, it
rendered warning-free. The guidance band evidently scales with non-prose blocks, so **trim
until the warning clears rather than to the literal band**. And a full-width figure placed at
the top of a section left the preceding page half empty; moving it two paragraphs later,
after the prose it illustrates rather than before, filled the page without changing the page
count. That is a fourth lever for the page-count fight and the only one that is free.

### Report 024: the thirteenth blocked run — and a summariser that inverted a theorem

Thirteen in a row (012-024). Three `curl` probes (`arxiv.org`, `www.nature.com`,
`www.usgs.gov`, all `000`) and one `WebFetch` (`www.nature.com`,
`EGRESS_BLOCKED`), then stop. **Four host groups are worth naming for anything in
extreme value statistics**, because between them they hold the entire primary
literature of the field and every one is blocked by the sandbox rather than by the
publisher: `projecteuclid.org` (Pickands 1975 in the *Annals of Statistics*,
Balkema and de Haan 1974 in the *Annals of Probability*, Hill 1975), `www.cambridge.org`
(Fisher and Tippett 1928, Cohen 1982, McNeil 1997 and Resnick 1997 in the *ASTIN
Bulletin*), `onlinelibrary.wiley.com` (Jenkinson 1955, de Haan 1990) and
`esd.copernicus.org` (the 2021 Pacific Northwest attribution paper). Add
`www.econometricsociety.org` and `ir.cwi.nl`, which between them host van Dantzig's
1956 *Econometrica* paper in two places. Report 024 cited 21 sources without
opening one.

The 014-023 rule held again and chose the topic: **pick a subject whose load-bearing
content is a closed form plus its consequences.** Everything quantitative here came
out of the generalised extreme value quantile function and three lines of algebra —
the three-curve fan at $\mu$ = 3.00 m and $\sigma$ = 0.30 m, the 23 cm spread at ten
years against 4.46 m at ten thousand, the upper endpoint landing on exactly 5.00 m,
the $\sigma \ln 10$ = 0.691 m increment per decade of rarity, the Weibull size-effect
factors, the penultimate shape. Four checks did the work a fetched PDF would have done:

- **A closed form checked against a library implementation that parameterises it
  differently.** The return-level formula was compared with `scipy.stats.genextreme`,
  whose shape constant `c` is the negative of the conventional $\xi$. Agreement to
  six decimals at three shapes and two return periods — and getting the sign wrong is
  the single easiest error to make in this subject, so the cross-check is worth the
  three lines it costs.
- **An asymptotic formula confirmed by simulation across two orders of magnitude.**
  Fisher and Tippett's penultimate shape $-1/(2\ln n)$ was checked against GEV fits to
  60,000 simulated maxima at each of eight block sizes from 100 to 316,228. Fitted
  shapes ran $-0.095$ to $-0.038$ against a theory running $-0.109$ to $-0.039$;
  agreement is poor below $n \approx 300$, which is what "asymptotic" means, and
  excellent above it. That is also the figure.
- **An arithmetic identity inside a pair of reported tail-index estimates.** McNeil's
  Danish fire result is quoted as $\xi = 0.684$ *or* $\alpha = 1.46$, and a second
  source gives $\xi = 0.6928$ *or* $\alpha = 1.4435$. Both pairs satisfy
  $\alpha = 1/\xi$ to four digits, which is what made two numbers from two summarisers
  safe to print. The Hill-based figure at a lower threshold, $\alpha \approx 2.01$,
  then straddles $\xi = 1/2$ with them — and **two estimates disagreeing is the
  finding**, as in report 021, not a reason to pick one.
- **A high-precision recomputation replacing a floating-point artifact.** The error in
  the Gumbel approximation to normal maxima came back as 0.9994 at $n = 10^{100}$ in
  double precision — obviously wrong, since the sequence runs 0.059, 0.048, 0.031,
  0.020 at $n$ = $10^2$ to $10^{12}$. `mpmath` at 250 digits gives 0.0046. **A "result"
  that breaks a monotone sequence is an underflow, not a discovery**; `scipy.stats.norm.cdf`
  returns values indistinguishable from 1 well before the answer stops mattering.

**One attribution trap where a second query did not merely correct the summariser but
reversed it.** Asked about Fisher and Tippett's penultimate approximation, a first
query returned that for the normal "it is better to avoid the ultimate approximation
(to the Gumbel) and use instead the penultimate approximation (**to the Fréchet**)."
That is backwards: the penultimate shape is $\xi_n \approx -1/(2\ln n) < 0$, which is
Weibull-type and bounded, and a differently-worded query said so explicitly and gave
the formula. The simulation then settled it independently. **When a claim is about a
sign, re-query for the formula rather than the prose** — and if the quantity is
computable, compute it, because that is the one check a summariser cannot fake.

**Two titles deliberately not printed, for the reason report 020 recorded.** Searches
confirm that P. J. Wemelsfelder published the founding Dutch storm-surge frequency
analysis in *De Ingenieur* in 1939, and describe its content consistently across three
phrasings, but no query returned the Dutch title from a primary record. The reference
therefore gives a description of the article rather than a guessed title, and says so
in the entry. The same caution applies to the co-authors of the CPB dike-ring paper:
search attaches two further names to it, none confirmed, so the entry carries
Eijgenraam alone.

**One chronology that a second query untangled, and that would have shipped as a
false causal claim.** A first pass had van Dantzig's cost-benefit optimum (one in
125,000 per year, about 6 m at Hoek van Holland) being overruled by the Dutch
legislature. The sequence is the other way round in part: the *Econometrica* paper is
1956 from a 1954 presentation, the legal standard of one in 10,000 and a 5.00 m design
level was fixed in 1958, and the 6 m figure comes from a 1960 report. The secondary
literature also states plainly that his calculation was "one of the arguments, but not
the most important one" for the 1958 standard. The piece now prints the two pairs as
reported and says the economics was one argument among several. **When two numbers
come from documents of different dates, check the dates before writing a "but".**

**One reconstruction deliberately abandoned.** The two reported height-frequency pairs
(5.00 m at $10^{-4}$, 6.00 m at $8 \times 10^{-6}$) imply a decimation height of
1.00/log₁₀(12.5) = 0.91 m, which is about three times the figure the Dutch literature
gives for Hoek van Holland. Either the pairs come from different frequency curves or
one of them is referenced differently, and neither could be checked. So the piece uses
both pairs only as reported and builds its own worked example on stated parameters
instead. **A derived constant that disagrees threefold with the field's own number is
not a finding, it is a warning that two figures do not share a curve** — report 021's
lesson, arrived at from the other direction.

What search did well again: **bibliography**, with all 21 references confirmed by a
second differently-worded query including a 1928 Cambridge proceedings paper, a 1943
paper in French in the *Annals of Mathematics*, a 1939 Swedish academy monograph and a
1982 *Advances in Applied Probability* article. Issue numbers were the exception and
were dropped rather than guessed for Philip et al. 2022 and Cohen 1982. What it did
badly: **a specific shape-parameter estimate attached to a specific paper**. Four
queries for McNeil's own reported $\xi$ returned 0.5, 0.684 and 0.6928 at three
different thresholds, and only the $\alpha = 1/\xi$ identity made any of them usable.

One figure note and one toolchain note. A double-headed annotation arrow drawn at
$T = 10^4$ passed its vertical stem straight through a series label reading
"$\xi = -0.15$", turning the minus into what reads unmistakably as a plus in the
rendered PDF; neither the renderer nor the contract test catches a sign that is
correct in the source and wrong on the page, so **crop the figure and look at every
label that contains a minus sign**. And `mpmath` is not preinstalled, `pip install
mpmath` works, and the `pypdf` / `cryptography` panic recorded above did not recur on
this container — `pip install numpy scipy matplotlib Markdown pypdf brotli fontTools
pypdfium2` was enough, with `pip install --upgrade cffi` run as a precaution.

### Report 025: the fourteenth blocked run — and a topic chosen for its reversibility

Fourteen in a row (012-025). Four `curl` probes (`arxiv.org`, `www.nature.com`,
`www.iea.org`, `essd.copernicus.org`, all `000`) and one `WebFetch`
(`essd.copernicus.org`, `EGRESS_BLOCKED`), then stop. **`essd.copernicus.org` is
worth naming for any climate or carbon-accounting piece**, because it is the
single most useful host the series has yet been unable to reach: *Earth System
Science Data* publishes the Global Carbon Budget itself and, for this topic,
four of the five cement-carbonation accounts, all open access, all with their
numbers in the abstract. It is blocked by the sandbox, not by Copernicus. Add
`www.ipcc-nggip.iges.or.jp` (the 2006 Guidelines volumes and the EFDB editorial
notes), `www.ipcc.ch`, `www.iea.org`, `pmc.ncbi.nlm.nih.gov` (recorded since
report 013 and still the host that would have served three of this piece's
sources in full) and `www.mdpi.com`. Report 025 cited 19 sources without opening
one.

The 014-024 rule held and did the topic selection: **pick a subject whose
load-bearing content is a reaction equation and its consequences.** Everything
quantitative in report 025 came out of four molar masses, three formation
enthalpies and Fick's law — the 0.785 lime factor, both IPCC clinker emission
factors, the 2.08 GJ/t calcination heat, the twenty orders of magnitude of
atmospheric supersaturation, the carbonation coefficient, the four element
geometries. Five checks did the work a fetched PDF would have done:

- **Two competing published constants reproduced as the same calculation.** The
  clinker emission factor circulates as both 0.5070 and 0.5101 t CO2/t clinker,
  and search returns them from different pages as though they were rival
  estimates. They are 0.646 and 0.650 times 44.009/56.077, and both reproduce to
  four decimal places. **When two reported values differ in the third digit, try
  running the same formula on the two default inputs before treating them as a
  disagreement.**
- **An internal identity inside one paper's three headline numbers.** Huang et
  al. 2023 report 22.9 Gt absorbed, 41.6 Gt emitted and an offset of 55.1 per
  cent. 22.9/41.6 = 55.05. Three numbers from one abstract, none of them
  readable at source, all confirmed at once.
- **A unit conversion confirming two differently-phrased returns.** The Global
  Carbon Budget's cement carbonation sink came back as "0.2 GtC yr-1" from one
  query and "above 700 Mtons/year in 2023" from another. 0.2 times 3.664 is
  0.733. Same lesson as report 021's Hall-Petch coefficient: **a quantity quoted
  in two unit systems is a free cross-check.**
- **A first-principles derivation landing inside the measured band.** The
  carbonation coefficient was derived from Fick's law with an effective
  diffusivity of 5e-8 m2/s, the atmospheric CO2 concentration and a lime binding
  capacity of 3,480 mol/m3, giving 4.0 mm per root year against a field range of
  roughly 2 to 6 for ordinary structural concrete. The derivation is what made
  it safe to use a coefficient whose provenance search would not settle (see
  below).
- **A published theoretical minimum recovered from a heat balance.** Calcination
  alone is 2.08 GJ/t clinker; the alite-forming reaction gives back about 0.30;
  net 1.77 against a published theoretical floor of roughly 1.75. The same
  balance run on pure clinker phases returns 1,848 and 1,343 kJ/kg for alite and
  belite against reported figures of 1,810 and 1,350 — 2.1 and 0.5 per cent.
  Two reported constants confirmed at once by arithmetic on standard formation
  enthalpies.

**One number that would not firm up, and the derivation that replaced it.** The
carbonation coefficient k = 3.75 mm per root year is quoted by several secondary
pages as "the mean for in-service structures up to 79 years old", but no query
attached it to a citable paper — the returns were an ALCONPAT article, a
ResearchGate table and two machine-learning preprints, none of which could be
established as the origin. So the piece cites the *model* (Tuutti 1982, fib
Bulletin 34) rather than the constant, prints the field range instead of the
point value, and derives 4.0 from Fick's law to show the worked example sits in
the right place. Same move as report 021's break-even: **choose the quantity
that does not need the unsourceable input.** The figure still uses 3.75 for the
worked geometries, and says so on its face rather than attributing it.

**One equilibrium temperature deliberately left out.** Search returns 898 C, 850
C and 830 C for the temperature at which calcium carbonate decomposes at one
atmosphere of CO2, and the elementary calculation from standard data gives 844 C
(856 C with a constant-Cp correction). The gap between the calculation and the
most-quoted figure could not be resolved from search, so the piece never states
a decomposition temperature at all — it needs the *enthalpy*, which cross-checks
cleanly, not the temperature. **When a derived number disagrees with the
most-quoted one and the disagreement cannot be explained, check whether the
argument needs the number before trying to fix it.**

**Two shares from two papers, and the ratio printed as a range.** The piece's
central claim — mortar is about a quarter of cement use and about half of the
carbonation sink — rests on uptake shares from Huang et al. 2023 (concrete 30.1
per cent, mortar 58.5) and use shares from Niu et al. 2025 (concrete ~73 per
cent, mortar ~24). Dividing across the two papers gives mortar 5.9 times as much
uptake per tonne of cement; using the 2025 paper's own most-recent-decade mortar
share of 48.0 per cent gives 3.6. Both are defensible and they are not the same
number, so the piece prints "between three and a half and six times" and names
the disagreement. The claim that needs no division — a quarter of the cement,
half of the sink — is directly reported by both papers and is what the headline
rests on.

Bibliography cross-checked cleanly again, which is now the thirteenth run to say
so: all five carbonation accounts had first author, journal, volume and page
range confirmed by a second differently-worded query, including two whose author
lists a first query returned only as "et al." (Huang et al. 2023, ESSD 15,
4947-4958; Niu et al. 2025, ESSD 17, 2231-2247). Three references are cited by
title with no author list, per report 020's rule, because no query established
one: the IOP minimum-energy paper, the SINTEF demolition report and the IVL
report for CEMBUREAU.

One figure note and one repo-mechanics note. The `\sqrt` mathtext warning
recorded under report 016 fired again on an axis annotation; `$x = k\,t^{1/2}$`
renders identically and silently, and is the fix to reach for without
experimenting. And `ledger.py verify` flagged a false overlap between 020 and
025 on *against / heat / released*, from a burned line reading "less 0.30 GJ/t
released by alite formation, against a published theoretical minimum"; rewording
it to "minus the 0.30 GJ/t exotherm of alite formation, reaching a published
theoretical floor" cleared it — the third run to hit this and the third time
rewording the line, not the content, was the fix.

Toolchain, unchanged and confirmed a sixth time on a fresh container: `pip
install numpy scipy matplotlib Markdown pypdf brotli fontTools pypdfium2` then
`pip install --upgrade cffi`, and `npm install playwright@1.56.0` with no
`playwright install`. The pypdf / `cryptography` panic did not recur.

### Report 026: the fifteenth blocked run — and a topic chosen to be computable

Fifteen in a row (012-026). Three `curl` probes (`arxiv.org`, `www.nature.com`,
`www.rand.org`, all `000` with `CONNECT tunnel failed, response 403`) and one
`WebFetch` (`arxiv.org`, `EGRESS_BLOCKED`), then stop. **Five host groups are
worth naming for anything in integer programming or combinatorial optimization**,
because between them they hold essentially the whole primary literature of
Lagrangian relaxation and every one is blocked by the sandbox rather than by the
publisher: `link.springer.com` (*Mathematical Programming* — Held and Karp Part
II 1971, Held/Wolfe/Crowder 1974, Guignard and Kim 1987, Barahona and Anbil
2000, and Geoffrion's 1974 *Mathematical Programming Study 2* paper),
`pubsonline.informs.org` (*Operations Research* — Everett 1963, Held and Karp
Part I 1970, Dantzig/Fulkerson/Johnson 1954; *Management Science* — Fisher 1981;
*Interfaces* — the MISO Edelman paper; *INFORMS Journal on Computing* — Knueven
et al. 2020), `www.sciencedirect.com` (Polyak 1969 in *USSR Comput. Math. Math.
Phys.*), `aclanthology.org` (the 2010 EMNLP dual-decomposition papers) and
`archive.dimacs.rutgers.edu` (the Held-Karp challenge results and the 1996 SODA
paper). Add `www.rand.org`, which holds P-510, the RAND version of the 1954
travelling-salesman paper. Report 026 cited 18 sources without opening one.

The 014-025 rule held and did the topic selection again, in its strongest form
yet: **pick a subject whose load-bearing content you can compute yourself.**
Nothing quantitative in this piece came from a source at all. The entire
numerical spine is one six-order, three-line generalized assignment instance,
constructed here and solved four ways in Python: exact optimum 104 by
enumerating all 729 assignments (183 feasible), LP relaxation 93.2 by
`scipy.optimize.linprog`, and the two Lagrangian duals by linear programming
over enumerated subproblem solutions. Search supplied history, bibliography and
two reported figures, and nothing else. Four checks did the work a fetched PDF
would have done:

- **A theorem verified numerically rather than taken on trust.** Geoffrion's
  1974 result predicts that dualizing the capacity constraints — leaving a
  subproblem whose polytope is a product of simplices, hence integral — gives a
  bound exactly equal to the LP relaxation. Maximizing that dual by
  multi-start Nelder-Mead over 60 starts returns 93.200000 against an LP value
  of 93.200000, agreeing to 1.4e-14. Dualizing the requirement constraints
  instead, leaving three knapsacks, gives 102. **When the claim is a theorem and
  the instance is small, run both sides of the equality;** it is a stronger
  check than a second citation, and it caught nothing only because it was right.
- **An exact dual value obtained two independent ways.** The
  requirements-dualized bound came out of a linear program over all 86 feasible
  job-subsets (29, 28 and 29 per line), and separately as $L(u) = 102$ at the
  integer multiplier vector $(17, 14, 25, 26, 27, 20)$ read off that LP's duals.
  Subgradient ascent from a warm start reaches 101.90 in 200 iterations and
  101.98 in 400 — the tailing-off is real, and printing the exact 102 alongside
  the iterate is what makes the figure honest.
- **A closed-form kink recovered from a grid.** The one-price dual's maximum
  came off a 4,001-point grid as 100.700 at $\mu = 0.37$; the two active affine
  pieces are $97 + 10\mu$ and $107 - 17\mu$, which cross at exactly $\mu = 10/27$
  with value $2719/27 = 100.7037$. **A grid maximum of a piecewise-linear
  function is always an approximation to a rational number** — find the two
  pieces and solve, then print the fraction.
- **An instance searched for rather than taken.** The first instance tried gave
  a three-way separation but eight jobs, which cannot be tabulated inside the
  house four-column limit. Regenerating at three lines by six orders and
  filtering on "LP bound strictly below the Lagrangian bound strictly below the
  integer optimum" produced four candidates in 400 trials. **When a worked
  example has to fit a format constraint, put the constraint in the search, not
  in the write-up.**

**Two attributions deliberately softened.** Search returns Shor's 1962 Kiev work
on gradient methods for network transportation problems and a 1967 *Kibernetika*
paper from a single query and no primary record, so the piece names Shor, Polyak
and Ermoliev in prose and cites Polyak 1969 and the 2023 Bragin survey rather
than inventing a Shor entry — report 020's rule. Likewise the 2010 EMNLP dual
decomposition group: a first draft placed them "at MIT and Columbia", which is
plausible but turns on exactly when Collins moved, and no query settled it, so
the piece says "four researchers" and cites the paper.

**One biographical coincidence that cross-checked cleanly and is the best thing
in the piece.** Everett's 1963 *Operations Research* paper carries the author
affiliation "Weapons Systems Evaluation Division, Institute for Defense
Analyses"; an independently-worded biographical query returns that Hugh Everett
III of the many-worlds interpretation joined WSEG in June 1956, headed its
mathematics division, and stayed until 1964. Two queries, two different kinds of
record, same person and same institution in the same years. **A surprising
claim about a person is safe when the bibliographic record and the biographical
record are fetched by separate queries and agree on institution and dates.**

Bibliography cross-checked cleanly again — the fourteenth run to say so. All 18
references had journal, volume and page range confirmed, including a 1954
*Operations Research* paper, a 1969 Soviet journal translation, a 1974
*Mathematical Programming Study* and a 1997 Wiley book chapter. Two details are
worth recording: Fisher 1981 was reprinted in *Management Science* 50(12), 2004,
in the "Ten Most Influential Titles" issue, which two queries confirm and which
is worth carrying in the entry; and the MISO Edelman paper's own figures (2.1-3.0
billion dollars cumulative 2007-2010, 6.1-8.1 billion more expected through 2020)
are what the widely-quoted "5 billion a year" for the unit-commitment switch is
derived from, so **print the paper's range and not the derived round number.**

One figure note, following report 024's. A rotated mathtext label reading
`slope $-17$` renders correctly at 300 dpi in the PNG and reads unmistakably as
`slope ~17` once the figure is scaled down into the PDF — the minus is too short
and the rotation does the rest. The fix that needs no experimenting is to write
the sign as a word: the labels now read "rising at 10" and "falling at 17".
**Check every minus sign in the rasterized PDF, not in the source PNG.**

One layout note. The renderer will not split a full-width figure across a page,
so a figure that does not fit leaves the rest of the page blank — page 2 lost
about a third of its height on the first render. Trimming 45 words did not
recover it; the fix is to add roughly a dozen lines before the figure, which in
this case meant writing the two paragraphs the piece was missing anyway (the
subproblem's answer being infeasible, and the duality gap never closing).
**A blank half-page is a prompt to add the content you left out, not to cut.**

Toolchain, unchanged and confirmed a seventh time on a fresh container: `pip
install numpy scipy matplotlib Markdown pypdf brotli fontTools pypdfium2` then
`pip install --upgrade cffi`, and `npm install playwright@1.56.0` with no
`playwright install`. One shell trap worth recording: `pkill -f gap3.py` killed
its own shell, because the pattern matches the command line of the bash process
running it, and the heredoc later in the same compound command never ran. **Do
not `pkill -f` on a string that appears in the command you are typing.**

And `ledger.py verify` flagged a false overlap between 011 and 026 on
*cent / example / worked*, from a burned line reading "The generalized
assignment worked example — ... 81.5 per cent of the gap closed"; rewording it
to "The generalized assignment instance behind the figures — ... 0.815 of the LP
gap closed" cleared it. Fourth run to hit this and the fourth time rewording the
line, not the content, was the fix.
