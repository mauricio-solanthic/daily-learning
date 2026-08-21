#!/usr/bin/env python3
"""
Daily Learning — canonical report renderer.

Markdown (+ YAML front matter)  ->  styled HTML  ->  print-quality PDF.

Usage
-----
    python3 render.py INPUT.md [--outdir DIR] [--keep-html]

Front matter (all fields except `deck` are required):

    ---
    seq: 7                     # sequence number; rendered as 007
    date: 2026-08-20           # ISO date of the report
    category: Physics          # one of the backlog categories, Title Case
    title: Noether's Theorem and the Origin of Conservation Laws
    slug: NoethersTheorem      # optional; auto-derived from title if omitted
    deck: One italic sentence…  # optional standfirst line
    ---

Output filename is derived, never hand-typed:

    00{seq}_{YYYY.MM.DD}_{TitleCamel}_{CategoryCamel}.pdf

Markdown extras supported
-------------------------
  $inline$ and $$display$$ math      -> MathJax SVG (vendored, no network)
  :::think ... :::                   -> the "pause and think" call-out box
  Standard GFM tables                -> ruled academic tables
  ## References + numbered list      -> IEEE reference block (auto-detected)
  ![caption](file.svg)               -> centred figure with caption

Requires: markdown, playwright (chromium), assets/report.css, assets/tex-svg.js
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date as _date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402

ASSETS = Path(__file__).resolve().parent
CSS = ASSETS / "report.css"
MATHJAX = ASSETS / "tex-svg.js"

CATEGORIES_SHORT = {
    "Operations Research": "OperationsResearch",
    "Math & Operations Research": "OperationsResearch",
    "Quantitative Finance": "QuantitativeFinance",
    "History of Science": "HistoryOfScience",
    "Geopolitics of Resources": "GeopoliticsOfResources",
    "Climate & Sustainability": "ClimateAndSustainability",
    "Cross-Domain Synthesis": "CrossDomain",
}


# --------------------------------------------------------------------------- #
# front matter
# --------------------------------------------------------------------------- #

def parse_front_matter(text):
    try:
        return frontmatter.parse(text)
    except frontmatter.FrontMatterError as e:
        sys.exit(f"ERROR: {e}")


def camel(s):
    s = re.sub(r"[‘’“”'\"]", "", s)
    s = re.sub(r"[^A-Za-z0-9]+", " ", s)
    parts = [p for p in s.split() if p]
    return "".join(p[:1].upper() + p[1:] for p in parts)


def out_stem(meta):
    d = meta["date"]
    y, m, dd = d.split("-")
    seq = f"{int(meta['seq']):03d}"
    title_c = camel(meta.get("slug") or meta["title"])
    cat = meta["category"].strip()
    cat_c = CATEGORIES_SHORT.get(cat, camel(cat))
    return f"{seq}_{y}.{m}.{dd}_{title_c}_{cat_c}"


def pretty_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    suffix = "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")
    wd = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
          "Saturday", "Sunday"][_date(y, m, d).weekday()]
    return f"{wd}, {months[m - 1]} {d}{suffix}, {y}"


# --------------------------------------------------------------------------- #
# markdown -> html
# --------------------------------------------------------------------------- #

MATH_STORE = []


def protect_math(md):
    """Pull $$…$$ and $…$ out of the markdown so it can't mangle them."""
    def stash(m):
        MATH_STORE.append(m.group(0))
        return f"\x00MATH{len(MATH_STORE) - 1}\x00"

    md = re.sub(r"(?<!\\)\$\$.+?\$\$", stash, md, flags=re.S)
    md = re.sub(r"(?<!\\)\$(?!\s)(?:\\.|[^$\\\n])+?(?<!\s)\$", stash, md)
    return md


def restore_math(html):
    def unstash(m):
        return MATH_STORE[int(m.group(1))]
    return re.sub(r"\x00MATH(\d+)\x00", unstash, html)


def convert_think_blocks(md):
    """:::think … :::  ->  raw HTML call-out."""
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        if lines[i].strip().startswith(":::think"):
            label = lines[i].strip()[len(":::think"):].strip() or "Pause and work this out"
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip() == ":::":
                buf.append(lines[i])
                i += 1
            i += 1
            _md = _ensure("markdown", "Markdown")
            inner = _md.Markdown(extensions=["extra", "sane_lists"]).convert("\n".join(buf))
            out.append(f'<div class="think"><span class="label">{label}</span>\n{inner}\n</div>')
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def wrap_references(html):
    """Turn a trailing `<h2>References</h2><ol>…` into the IEEE block."""
    m = re.search(r"<h2[^>]*>\s*References\s*</h2>(.*)$", html, flags=re.S | re.I)
    if not m:
        return html, ""
    body = html[: m.start()]
    refs = m.group(1).strip()
    return body, f'<section class="references"><h2>References</h2>{refs}</section>'


def tag_tables(html):
    """Right-align whole columns that are numeric, headers included."""
    def fix_table(tm):
        tbl = tm.group(0)
        rows = re.findall(r"<tr>(.*?)</tr>", tbl, flags=re.S)
        if not rows:
            return tbl
        body_rows = [r for r in rows if "<td" in r]
        if not body_rows:
            return tbl
        cols = [re.findall(r"<td[^>]*>(.*?)</td>", r, flags=re.S) for r in body_rows]
        ncol = max((len(c) for c in cols), default=0)
        numeric = []
        for j in range(ncol):
            vals = [re.sub(r"<[^>]+>", "", c[j]).strip() for c in cols if len(c) > j]
            vals = [v for v in vals if v not in ("", "—", "-", "n/a")]
            numeric.append(bool(vals) and all(
                re.fullmatch(r"[-+\u2212]?[$\u20ac\u00a3]?[\d,.]+\s*%?"
                             r"(\s*[-\u2013\u2014]\s*[-+\u2212]?[$\u20ac\u00a3]?[\d,.]+\s*%?)?", v)
                for v in vals))

        def retag(rm):
            row = rm.group(1)
            idx = [0]

            def cell(cm):
                tag, attrs, inner = cm.group(1), cm.group(2), cm.group(3)
                j = idx[0]
                idx[0] += 1
                if j < len(numeric) and numeric[j] and "class=" not in attrs:
                    return f'<{tag} class="num"{attrs}>{inner}</{tag}>'
                return cm.group(0)

            return "<tr>" + re.sub(r"<(t[dh])([^>]*)>(.*?)</\1>", cell, row, flags=re.S) + "</tr>"

        return re.sub(r"<tr>(.*?)</tr>", retag, tbl, flags=re.S)

    return re.sub(r"<table>.*?</table>", fix_table, html, flags=re.S)


def _ensure(mod, pkg=None):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                        "--break-system-packages", pkg or mod], check=False)
        return __import__(mod)


def md_to_html(body):
    markdown = _ensure("markdown", "Markdown")

    MATH_STORE.clear()
    body = protect_math(body)
    body = convert_think_blocks(body)
    html = markdown.Markdown(
        extensions=["extra", "sane_lists", "smarty", "attr_list", "md_in_html"],
        extension_configs={"smarty": {"smart_dashes": True, "smart_quotes": True}},
    ).convert(body)
    html = restore_math(html)
    html = tag_tables(html)
    return html


def inline_images(html, base):
    """Embed local images/SVGs so the PDF and the HTML are self-contained."""
    def repl(m):
        pre, src, post = m.group(1), m.group(2), m.group(3)
        if src.startswith(("data:", "http://", "https://")):
            return m.group(0)
        p = (base / src)
        if not p.exists():
            return m.group(0)
        if p.suffix.lower() == ".svg":
            return p.read_text(encoding="utf-8")
        mime = mimetypes.guess_type(p.name)[0] or "image/png"
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f'{pre}data:{mime};base64,{b64}{post}'
    return re.sub(r'(<img[^>]*src=")([^"]+)("[^>]*>)', repl, html)


def wrap_figures(html):
    """A lone <img> in its own paragraph becomes a captioned figure."""
    def repl(m):
        img, alt = m.group(0), m.group(1)
        src_only = re.sub(r"</?p>", "", img)
        cap = f'<figcaption><span class="lbl">Figure</span> {alt}</figcaption>' if alt else ""
        return f'<figure class="figure">{src_only}{cap}</figure>'
    return re.sub(r'<p>\s*<img[^>]*alt="([^"]*)"[^>]*>\s*</p>', repl, html)


# --------------------------------------------------------------------------- #
# page assembly
# --------------------------------------------------------------------------- #

def inline_fonts(css):
    """Replace url("fonts/x.woff2") with a data URI so the page is machine-independent."""
    def repl(m):
        f = ASSETS / "fonts" / m.group(1)
        if not f.exists():
            sys.exit(f"ERROR: vendored font missing: {f}\n"
                     f"The house format depends on these files; do not fall back to "
                     f"system font names.")
        b64 = base64.b64encode(f.read_bytes()).decode()
        return f'url("data:font/woff2;base64,{b64}") format("woff2")'
    css, n = re.subn(r'url\("fonts/([^"]+)"\)\s*format\("woff2"\)', repl, css)
    if n == 0:
        sys.exit("ERROR: report.css declares no vendored @font-face sources. "
                 "Rendering would depend on whatever fonts this machine happens "
                 "to have, which is how reports drift apart.")
    return css


PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{fname}</title>
<style>{css}</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']],
 processEscapes:true,tags:'none'}},svg:{{fontCache:'global',scale:0.98}},
 options:{{enableMenu:false}},
 startup:{{typeset:true,pageReady(){{return MathJax.startup.defaultPageReady()
   .then(()=>{{window.__mjDone=true;}})
   .catch(e=>{{window.__mjErr=String(e);window.__mjDone=true;}});}}}}}};</script>
<script src="{mathjax}"></script>
</head><body>
<header class="masthead">
  <div class="topline"><span class="series">Daily Learning</span><span class="issue">No. {seq}</span></div>
  <p class="dateline">{datestr}</p>
  <p class="kicker">{category}</p>
  <h1 class="title">{title}</h1>
  {deck}
  <p class="meta">{words} words · {minutes}-minute read{extrameta}</p>
</header>
<main>
{body}
</main>
{refs}
<footer class="colophon">Daily Learning No. {seq} · {category} · {datestr} · Sources are listed above; every load-bearing figure traces to a numbered reference.</footer>
</body></html>
"""


def build_html(meta, body_html, refs_html, fname):
    words = len(re.sub(r"<[^>]+>", " ", body_html).split())
    deck = f'<p class="deck">{meta["deck"]}</p>' if meta.get("deck") else ""
    return PAGE.format(
        css=inline_fonts(CSS.read_text(encoding="utf-8")),
        mathjax=MATHJAX.resolve().as_uri(),
        seq=f"{int(meta['seq']):03d}",
        datestr=pretty_date(meta["date"]),
        category=meta["category"],
        title=meta["title"],
        deck=deck,
        words=f"{words:,}",
        minutes=max(1, round(words / 190)),
        extrameta=f" · {meta['extrameta']}" if meta.get("extrameta") else "",
        body=body_html,
        refs=refs_html,
        fname=fname,
    )


PDF_JS = r"""
const {chromium} = require('playwright');
(async () => {
  const [src, dst, running] = process.argv.slice(2);
  const browser = await chromium.launch({args: ['--font-render-hinting=none',
                                                '--disable-lcd-text',
                                                '--allow-file-access-from-files']});
  const page = await browser.newPage();
  await page.goto('file://' + src, {waitUntil: 'load', timeout: 120000});
  await page.waitForFunction(() => window.__mjDone === true, null, {timeout: 60000})
    .catch(() => console.error('WARN: MathJax did not signal completion'));
  const mjErr = await page.evaluate(() => window.__mjErr || null);
  if (mjErr) console.error('WARN: MathJax error: ' + mjErr);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(700);
  await page.pdf({
    path: dst,
    format: 'Letter',
    printBackground: true,
    margin: {top: '20mm', bottom: '17mm', left: '20mm', right: '20mm'},
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      `<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7pt;` +
      `color:#6b7280;padding:0 20mm;display:flex;justify-content:space-between;` +
      `letter-spacing:.04em;">` +
      `<span>${running.replace(/[<>&]/g, '')}</span>` +
      `<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>` +
      `</div>`,
  });
  await browser.close();
})();
"""


def pdf_page_count(path):
    """Page count without a third-party dependency, falling back to pypdf."""
    try:
        data = Path(path).read_bytes()
        counts = [int(m.group(1)) for m in re.finditer(rb"/Type\s*/Pages[^>]*?/Count\s+(\d+)", data, re.S)]
        if counts:
            return max(counts)
    except Exception:
        pass
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except Exception:
        return None


def to_pdf(html_path, pdf_path, running):
    js = Path(tempfile.mkdtemp()) / "topdf.js"
    js.write_text(PDF_JS, encoding="utf-8")
    env = dict(os.environ)
    env.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    node_path = env.get("NODE_PATH", "")
    globals_ = subprocess.run(["npm", "root", "-g"], capture_output=True,
                              text=True).stdout.strip()
    parts = [p for p in (globals_, node_path) if p]
    env["NODE_PATH"] = ":".join(parts)
    if not shutil.which("node"):
        sys.exit("ERROR: node is not on PATH; the PDF step needs node + playwright.")
    r = subprocess.run(["node", str(js), str(html_path), str(pdf_path), running],
                       capture_output=True, text=True, env=env)
    if r.returncode != 0 or not Path(pdf_path).exists():
        sys.exit(f"ERROR rendering PDF:\n{r.stdout}\n{r.stderr}")


# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# validation — the format contract lives here, not only in the prose spec
# --------------------------------------------------------------------------- #

def prose_word_count(text):
    """Words a reader actually reads: no display math, tables, figures or fences."""
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)      # display math
    text = re.sub(r"^\s*\|.*$", " ", text, flags=re.M)         # table rows
    text = re.sub(r"^\s*!\[.*$", " ", text, flags=re.M)        # figures
    text = re.sub(r"^\s*:::.*$", " ", text, flags=re.M)        # callout fences
    text = re.sub(r"^\s*#+\s.*$", " ", text, flags=re.M)       # headings
    text = re.sub(r"\$[^$\n]*\$", " x ", text)                 # inline math -> 1 word
    return len(text.split())


PAGE_MIN, PAGE_MAX = 6, 8

KNOWN_CATEGORIES = {
    "Energy", "Physics", "History of Science", "Geopolitics of Resources",
    "Economics", "Philosophy", "Climate & Sustainability",
    "Operations Research", "Quantitative Finance", "Cross-Domain Synthesis",
}


def validate(meta, body):
    """Refuse to render anything that would not match reports 001-007.

    Returns a list of warnings; raises SystemExit on a hard violation.
    """
    errs, warns = [], []

    # ---- front matter ----
    for k in ("seq", "date", "category", "title"):
        if not meta.get(k):
            errs.append(f"front matter is missing `{k}`")
    if meta.get("category") and meta["category"] not in KNOWN_CATEGORIES:
        warns.append(f"category {meta['category']!r} is not one of the ten rotation "
                     f"categories; the filename suffix will be auto-camelised")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("date", "")):
        errs.append("`date` must be ISO yyyy-mm-dd")
    if meta.get("title", "").startswith(("#", '"', "'")):
        errs.append("`title` must not start with punctuation")
    burned = meta.get("burned") or []
    if not burned:
        errs.append("front matter has no `burned:` list. That list IS the ledger's "
                    "memory of what this report consumed — without it a later run "
                    "can repeat this topic. Name the specific sub-topics, anecdotes "
                    "and worked examples this piece spends.")
    elif len(burned) < 2:
        warns.append("only one `burned:` entry; most reports consume several "
                     "sub-topics, anecdotes or examples")
    if not (meta.get("next") or []):
        warns.append("no `next:` list; naming where this track should go next is how "
                     "the series builds instead of restarting")

    # ---- structural bans ----
    if re.search(r"^#\s+\S", body, re.M):
        errs.append("body contains an H1 (`# ...`); the title comes from front matter")
    if re.search(r"^---\s*$", body, re.M):
        errs.append("body contains a horizontal rule (`---`); not allowed")
    if re.search(r"^\s*(Today|Note on today)", body, re.M | re.I):
        errs.append("body opens a line with chat scaffolding (`Today:` / `Note on today`)")
    for phrase in ("couldn't find", "could not find", "your rotation", "prior reports",
                   "Solanthic", "as an AI"):
        if phrase.lower() in body.lower():
            errs.append(f"body contains forbidden phrase {phrase!r}")

    # ---- opening paragraph gets a drop cap ----
    first = next((l for l in body.splitlines() if l.strip() and not l.startswith(("#", "|", "$"))), "")
    if first and not re.match(r"[A-Z]", first.strip()):
        errs.append("first body paragraph must begin with a capital letter (it gets a drop cap)")

    # ---- math and call-out balance ----
    stripped = re.sub(r"\$\$.*?\$\$", "", body, flags=re.S)
    if stripped.count("$") % 2:
        errs.append("odd number of `$` delimiters outside display math — an unbalanced "
                    "inline equation (a bare currency `$` is the usual cause)")
    if body.count("$$") % 2:
        errs.append("odd number of `$$` display-math fences")
    opens = len(re.findall(r"^\s*:::think", body, re.M))
    closes = len(re.findall(r"^\s*:::\s*$", body, re.M))
    if opens != closes:
        errs.append(f"{opens} `:::think` opener(s) but {closes} closing `:::`")
    if opens == 0:
        warns.append("no `:::think` call-out box; the house format expects one or two")
    elif opens > 2:
        warns.append(f"{opens} call-out boxes; the house format expects one or two")

    # ---- references: the contract that broke on report 007 ----
    parts = re.split(r"^##\s+References\s*$", body, flags=re.M)
    if len(parts) != 2:
        errs.append("body must contain exactly one `## References` heading, spelled "
                    "exactly that way")
        return _report(errs, warns)
    prose, refs = parts
    trailing = re.findall(r"^##+\s+(.*)$", refs, flags=re.M)
    if trailing:
        errs.append(f"`## References` must be the last thing in the file, but "
                    f"{len(trailing)} heading(s) follow it: "
                    f"{', '.join(repr(h.strip()) for h in trailing[:3])}")
    if prose.count("## ") < 3:
        warns.append("fewer than four `##` sections; the house shape expects four to seven")

    ref_lines = [l for l in refs.splitlines() if l.strip()]
    numbered = [l for l in ref_lines if re.match(r"^\d+\.\s+\S", l)]
    bracketed = [l for l in ref_lines if re.match(r"^\[\d+\]\s+\S", l)]
    if bracketed:
        errs.append(f"{len(bracketed)} reference entr{'y' if len(bracketed)==1 else 'ies'} "
                    f"written as `[n] ...` paragraphs. The IEEE block only renders from a "
                    f"Markdown numbered list — use `1. `, `2. `, ... and let the stylesheet "
                    f"draw the brackets. (First offender: {bracketed[0][:60]!r})")
    if not numbered and not bracketed:
        errs.append("`## References` is not followed by a numbered list")
    if numbered:
        nums = [int(re.match(r"^(\d+)\.", l).group(1)) for l in numbered]
        if nums != list(range(1, len(nums) + 1)):
            errs.append(f"reference numbers are not 1..n in order: {nums}")
        cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", prose)})
        missing = [c for c in cited if c > len(nums)]
        unused = [n for n in nums if n not in cited]
        if missing:
            errs.append(f"cited in text but absent from the reference list: {missing}")
        if unused:
            warns.append(f"listed but never cited in text: {unused}")
        if len(nums) < 6:
            warns.append(f"only {len(nums)} references; a properly researched piece has more")

    # ---- length ----
    words = prose_word_count(prose)
    if not 2000 <= words <= 3000:
        warns.append(f"body is ~{words} words of prose; the target is 2,300-2,700 "
                     f"(page count is the enforced contract, this is guidance)")

    return _report(errs, warns)


def _report(errs, warns):
    if errs:
        sys.stderr.write("\nFORMAT CONTRACT VIOLATIONS — nothing was rendered:\n")
        for e in errs:
            sys.stderr.write(f"  [x] {e}\n")
        for w in warns:
            sys.stderr.write(f"  [!] {w}\n")
        sys.stderr.write("\nFix the Markdown and run again. Do not work around the "
                         "renderer or hand-build an HTML page.\n\n")
        sys.exit(1)
    return warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--keep-html", action="store_true")
    a = ap.parse_args()

    src = Path(a.input).resolve()
    outdir = Path(a.outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    meta, body = parse_front_matter(src.read_text(encoding="utf-8"))
    warnings = validate(meta, body)
    for w in warnings:
        sys.stderr.write(f"  [!] {w}\n")

    stem = out_stem(meta)
    html = md_to_html(body)
    html, refs = wrap_references(html)
    html = wrap_figures(inline_images(html, src.parent))
    page = build_html(meta, html, refs, stem)

    html_path = outdir / f"{stem}.html"
    html_path.write_text(page, encoding="utf-8")
    pdf_path = outdir / f"{stem}.pdf"
    running = f"Daily Learning · {meta['category']} — {meta['title']}"
    if len(running) > 118:
        running = running[:117].rsplit(" ", 1)[0] + "\u2009…"
    to_pdf(html_path, pdf_path, running)
    if not a.keep_html:
        html_path.unlink()

    pages = pdf_page_count(pdf_path)
    words = prose_word_count(body.split("## References")[0])
    result = {"pdf": str(pdf_path), "stem": stem, "prose_words": words,
              "pages": pages, "warnings": warnings}
    print(json.dumps(result, indent=2))

    if pages is None:
        sys.stderr.write("  [!] could not read the page count; check it by hand\n")
    elif not PAGE_MIN <= pages <= PAGE_MAX:
        sys.stderr.write(
            f"\nPAGE COUNT OUT OF CONTRACT: {pages} pages, must be "
            f"{PAGE_MIN}-{PAGE_MAX}.\nThe PDF was written so you can look at it, but it "
            f"is not shippable as is.\nPages are driven by display math, tables and "
            f"figures at least as much as by\nword count, so the levers are: add or cut a "
            f"table, a figure or a worked\nexample; or move a section boundary. Re-render "
            f"and check again.\n\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
