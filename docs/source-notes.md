# Source access notes

Per-host knowledge, accumulated by runs. **Read this before researching; add to it
when you finish.** It is the only file in the repo that gets more valuable every
day, and it exists because report 008 spent four fetches rediscovering a redirect.

Record: hosts that decline automated access, hosts that redirect, reliable
mirrors, and any substitution you were forced into.

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
