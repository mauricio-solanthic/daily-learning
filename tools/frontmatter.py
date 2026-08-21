"""Front-matter parsing shared by render.py and ledger.py.

Deliberately a small hand-rolled parser rather than PyYAML: the repo should have
no third-party dependency for reading its own ledger, and the front-matter
grammar in use is a fixed, tiny subset of YAML.

Supported grammar
-----------------
    ---
    seq: 8                      # scalar
    title: Some Title           # scalar, quotes optional and stripped
    deck: A long sentence
      continued on the next line
    burned:                     # list
      - first item
      - second item
    ---

Scalars come back as `str`. Lists come back as `list[str]`. A key with neither a
value nor list items comes back as `""`.
"""

from __future__ import annotations

import re

SCALAR_KEYS = ("seq", "date", "category", "title", "slug", "deck", "provenance")
LIST_KEYS = ("burned", "next")


class FrontMatterError(ValueError):
    pass


def split(text: str) -> tuple[str, str]:
    """Return (raw_front_matter, body). Raises if the block is malformed."""
    if not text.startswith("---"):
        raise FrontMatterError("file must start with a YAML front-matter block (---)")
    try:
        end = text.index("\n---", 3)
    except ValueError:
        raise FrontMatterError("front-matter block is never closed with ---") from None
    return text[3:end], text[end + 4:].lstrip("\n")


def parse(text: str) -> tuple[dict, str]:
    """Parse a document into (meta, body)."""
    raw, body = split(text)
    meta: dict = {}
    key: str | None = None
    mode: str | None = None          # "scalar" | "list"

    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key and mode in ("list", None):
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                # key had a scalar value AND list items; treat the scalar as the
                # first item rather than silently dropping either.
                meta[key] = [meta[key]] if meta[key] else []
            meta[key].append(item.group(1).strip().strip("'\""))
            mode = "list"
            continue

        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            key = kv.group(1).strip()
            val = kv.group(2).strip()
            meta[key] = val.strip("'\"") if val else ""
            mode = "scalar" if val else None
            continue

        if key and mode == "scalar" and line.startswith((" ", "\t")):
            meta[key] = f"{meta[key]} {line.strip()}".strip()
            continue

        raise FrontMatterError(f"cannot parse front-matter line: {line!r}")

    for k in LIST_KEYS:
        if k in meta and not isinstance(meta[k], list):
            meta[k] = [meta[k]] if meta[k] else []

    return meta, body


def dump(meta: dict) -> str:
    """Render a meta dict back to a front-matter block, key order preserved."""
    out = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            out.append(f"{k}:")
            out.extend(f"  - {i}" for i in v)
        else:
            out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out) + "\n"
