#!/usr/bin/env python3
"""
Daily Learning — announce a merged report as a GitHub release and a Slack post.

Runs in CI after a report PR merges to main. The logic lives here rather than in
the workflow YAML for the same reason the format contract lives in render.py:
things buried in YAML cannot be tested, and this repo's whole premise is that
contracts belong in code.

Commands
--------
    announce.py detect --before SHA --after SHA
        Print, one per line, the seq numbers of reports added between two commits.

    announce.py payload SEQ
        Print a JSON object with everything needed to publish: tag, release
        title, release notes, the Slack upload payload. Prints nothing to
        stdout on failure.

    announce.py post SEQ --release-url URL
        Upload the report's PDF into Slack and share it into #daily-research
        with the `slack:` summary and a link to the release. Reads the bot
        token from $SLACK_BOT_TOKEN. Never logs the token.

Exit codes: 0 success, 1 hard failure, 3 "nothing to do" (not an error).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
REPORTS = ROOT / "reports"

REPO = os.environ.get("GITHUB_REPOSITORY", "mauricio-solanthic/daily-learning")
SLACK_CHANNEL_ID = "C0BTJCQV0D6"  # #daily-research
NOTHING_TO_DO = 3


# --------------------------------------------------------------------------- #

def load(seq: int):
    """Return (meta, src_path, pdf_path) for a sequence number."""
    srcs = sorted(SRC.glob(f"{seq:03d}_*.md"))
    pdfs = sorted(REPORTS.glob(f"{seq:03d}_*.pdf"))
    if not srcs:
        sys.exit(f"ERROR: no source in src/ for report {seq:03d}")
    if not pdfs:
        sys.exit(f"ERROR: no PDF in reports/ for report {seq:03d}")
    meta, _ = frontmatter.parse(srcs[0].read_text(encoding="utf-8"))
    return meta, srcs[0], pdfs[0]


def detect(before: str, after: str):
    """Sequence numbers of reports whose PDF was ADDED between two commits.

    Only additions count. An edit to an existing report is a correction, not a
    new report, and re-announcing it would spam the channel.
    """
    if not before or set(before) == {"0"}:
        # First push, or a force-push with no usable base. Announcing the whole
        # back catalogue would be worse than announcing nothing.
        return []
    try:
        out = subprocess.run(
            ["git", "diff", "--name-status", "--diff-filter=A", before, after,
             "--", "reports/"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"git diff failed: {e.stderr}\n")
        return []
    seqs = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        name = Path(parts[1]).name
        m = re.match(r"^(\d{3})_.*\.pdf$", name)
        if m:
            seqs.append(int(m.group(1)))
    return sorted(set(seqs))


# --------------------------------------------------------------------------- #

def payload(seq: int, release_url: str | None = None):
    meta, src, pdf = load(seq)
    summary = (meta.get("slack") or "").strip()
    if not summary:
        sys.exit(f"ERROR: report {seq:03d} has no `slack:` summary in its front "
                 f"matter. That field is what the channel post is made of.")

    tag = f"report-{seq:03d}"
    title = f"{seq:03d} — {meta['category']}: {meta['title']}"
    url = release_url or f"https://github.com/{REPO}/releases/tag/{tag}"

    notes = "\n".join([
        summary,
        "",
        f"**{meta['category']}** · {meta['date']} · report {seq:03d}",
        "",
        f"The PDF is attached below. Source, figures and references live in "
        f"[the repository](https://github.com/{REPO}).",
    ])

    # Link first, then the summary — the PDF itself is the visual lead once
    # uploaded, this is the text that rides alongside it.
    comment = f"{url}\n\n{summary}"

    return {
        "seq": seq, "tag": tag, "title": title, "notes": notes,
        "pdf": str(pdf.relative_to(ROOT)), "url": url,
        "slack": {
            "channel_id": SLACK_CHANNEL_ID,
            "filename": pdf.name,
            "title": title[:150],
            "initial_comment": comment,
        },
    }


def _slack_call(method: str, token: str, body: dict):
    """POST a normal Slack Web API method. Raises via sys.exit on any failure,
    including a 200-OK response carrying `"ok": false` — Slack's Web API signals
    failure that way, not just through HTTP status."""
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Slack {method} returned HTTP {e.code}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: Slack {method} unreachable: {e.reason}")
    if not resp.get("ok"):
        # Slack's own error string is safe to print; the token and request body
        # never are.
        sys.exit(f"ERROR: Slack {method} failed: {resp.get('error', 'unknown error')}")
    return resp


def post(seq: int, release_url: str):
    """Upload the report's PDF and share it into #daily-research, via Slack's
    external file-upload flow (files.getUploadURLExternal -> raw PUT of the
    bytes -> files.completeUploadExternal, which is what actually shares the
    file into a channel with an accompanying comment)."""
    token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    if not token:
        sys.exit("ERROR: SLACK_BOT_TOKEN is not set. Add it as a repository "
                 "secret; never put it in a file in this repo.")

    p = payload(seq, release_url)
    slack = p["slack"]
    data = (ROOT / p["pdf"]).read_bytes()

    step1 = _slack_call("files.getUploadURLExternal", token,
                        {"filename": slack["filename"], "length": len(data)})
    upload_url, file_id = step1["upload_url"], step1["file_id"]

    up_req = urllib.request.Request(upload_url, data=data, method="POST")
    try:
        with urllib.request.urlopen(up_req, timeout=60) as r:
            if r.status != 200:
                sys.exit(f"ERROR: Slack file upload returned HTTP {r.status}")
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR: Slack file upload failed: HTTP {e.code}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: Slack file upload unreachable: {e.reason}")

    _slack_call("files.completeUploadExternal", token, {
        "files": [{"id": file_id, "title": slack["title"]}],
        "channel_id": slack["channel_id"],
        "initial_comment": slack["initial_comment"],
    })
    print(f"posted {seq:03d} to Slack")


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("detect")
    d.add_argument("--before", required=True)
    d.add_argument("--after", required=True)

    p = sub.add_parser("payload")
    p.add_argument("seq", type=int)
    p.add_argument("--release-url")

    s = sub.add_parser("post")
    s.add_argument("seq", type=int)
    s.add_argument("--release-url", required=True)

    a = ap.parse_args()

    if a.cmd == "detect":
        seqs = detect(a.before, a.after)
        if not seqs:
            sys.exit(NOTHING_TO_DO)
        print("\n".join(str(s) for s in seqs))

    elif a.cmd == "payload":
        print(json.dumps(payload(a.seq, a.release_url), indent=2))

    elif a.cmd == "post":
        post(a.seq, a.release_url)


if __name__ == "__main__":
    main()
