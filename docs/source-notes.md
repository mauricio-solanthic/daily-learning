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

## Redirects and quirks

| Host | Behaviour | What to do |
|---|---|---|
| `entsoe.eu` PDFs | 302 to `eepublicdownloads.entsoe.eu`; `WebFetch` returns cross-host redirects rather than following them | Go straight to `eepublicdownloads.entsoe.eu`. Report 008 spent four fetches on round-trips. |

## Reliable

| Host | Notes |
|---|---|
| `federalreserve.gov` | FEDS working papers fetch cleanly, including PDFs. |
| `federalreservehistory.org` | Good for framing, thin on figures — do not use it as a numeric source. |
| `measuringworth.com` | Authoritative for historical US index levels. Source of the 282.70 → 224.84 S&P figures in report 007. |
| `academic.oup.com` | Abstracts fetch; full text usually does not. Enough to confirm a citation exists and what it claims. |
| `nobelprize.org` | Primary for prize citations and dates. |

## The bias this creates

"Cite the paper that establishes the claim" plus a robots-blocked national lab
pushes each run toward whatever happens to be fetchable, which is not the same as
whatever is best. When that has bent a piece — a second-hand substitution, a
dropped source, a claim you softened because you could not verify a byline — say
so in the commit message rather than letting it disappear.
