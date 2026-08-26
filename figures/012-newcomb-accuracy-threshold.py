"""Figure for report 012 — where the Newcomb payoffs cross.

Both panels are exact arithmetic on the standard payoffs: an opaque box holding
either 1,000,000 or nothing, and a transparent box holding 1,000. Writing p for
the probability that the predictor gets this agent right,

    EV(one box)  = p * B
    EV(two boxes) = p * s + (1 - p) * (B + s) = s + (1 - p) * B

with B = 1,000,000 and s = 1,000. The two are equal at p* = (B + s) / (2B),
which for these numbers is exactly 1001/2000 = 0.5005.

Left panel: the two lines across the whole range of predictor accuracy, with the
gap at high accuracy annotated. Right panel: the same lines within one
percentage point of a coin flip, which is the only place they are close enough
to tell apart — the crossing sits 0.05 points above one half.

Palette: the blue/orange pair already validated for this series (reports 009,
010, 011), all-pairs checked at print contrast.
Run: python3 figures/012-newcomb-accuracy-threshold.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from pathlib import Path

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e6e2"


def use_vendored_pagella():
    """Register tools/fonts/texgyrepagella-*.woff2 with matplotlib.

    The repository vendors the faces on purpose, and matplotlib cannot read
    woff2 directly, so decompress them to ttf in a temporary directory and
    register those. Naming the family and hoping the host has it installed is
    what made report 008 come out in the wrong typeface.
    """
    vendored = sorted((Path(__file__).resolve().parent.parent / "tools" / "fonts")
                      .glob("texgyrepagella-*.woff2"))
    if not vendored:
        return False
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return False
    cache = Path(tempfile.mkdtemp(prefix="pagella-"))
    for src in vendored:
        face = TTFont(str(src))
        face.flavor = None
        dst = cache / (src.stem + ".ttf")
        face.save(str(dst))
        fm.fontManager.addfont(str(dst))
    return SERIF in {f.name for f in fm.fontManager.ttflist}


if not use_vendored_pagella() and SERIF not in {f.name for f in fm.fontManager.ttflist}:
    raise SystemExit("TeX Gyre Pagella unavailable: install fontTools and brotli "
                     "so the vendored woff2 faces in tools/fonts/ can be used.")

plt.rcParams.update({
    "font.family": "serif", "font.serif": [SERIF], "font.size": 8.2,
    "mathtext.fontset": "custom", "mathtext.rm": SERIF,
    "mathtext.it": f"{SERIF}:italic", "mathtext.bf": f"{SERIF}:bold",
    "axes.edgecolor": "#c9c9c4", "axes.linewidth": 0.6,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.facecolor": "white", "savefig.facecolor": "white",
})

B, S = 1_000_000.0, 1_000.0
one = lambda p: p * B
two = lambda p: S + (1.0 - p) * B
P_STAR = (B + S) / (2.0 * B)
assert abs(P_STAR - 0.5005) < 1e-12
assert abs(one(P_STAR) - two(P_STAR)) < 1e-6

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.0),
                               gridspec_kw=dict(width_ratios=[1.15, 1.0],
                                                wspace=0.34))

# ---- left: the whole range ------------------------------------------------
p = np.linspace(0.0, 1.0, 501)
axL.plot(p, one(p) / 1e3, color=BLUE, lw=1.7, zorder=3)
axL.plot(p, two(p) / 1e3, color=ORANGE, lw=1.7, zorder=3)
axL.set_xlim(0, 1)
axL.set_ylim(0, 1060)
axL.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_yticks([0, 250, 500, 750, 1000])
axL.set_xlabel("probability the predictor gets this agent right")
axL.set_ylabel("expected payoff, thousands of dollars")
axL.set_title("Across the whole range", fontsize=9.0, loc="left", pad=8, color=INK)
axL.text(0.72, 885, "take one box", color=BLUE, fontsize=8.2, ha="center")
axL.text(0.28, 885, "take both boxes", color=ORANGE, fontsize=8.2, ha="center")
axL.plot([P_STAR], [one(P_STAR) / 1e3], "o", ms=3.4, color=INK, zorder=4)
axL.annotate("they cross here", xy=(P_STAR, one(P_STAR) / 1e3),
             xytext=(0.5, 120), fontsize=7.4, color=MUTED, ha="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=3, shrinkB=3))
axL.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: within a point of a coin flip --------------------------------
q = np.linspace(0.49, 0.51, 401)
axR.plot(q, one(q) / 1e3, color=BLUE, lw=1.7, zorder=3)
axR.plot(q, two(q) / 1e3, color=ORANGE, lw=1.7, zorder=3)
axR.axvline(0.5, color="#9a9a94", lw=0.8, ls=(0, (3, 2.5)), zorder=2)
axR.plot([P_STAR], [one(P_STAR) / 1e3], "o", ms=3.8, color=INK, zorder=5)
axR.set_xlim(0.49, 0.51)
axR.set_ylim(488, 512)
axR.set_xticks([0.49, 0.495, 0.5, 0.505, 0.51])
axR.set_xticklabels(["0.490", "0.495", "0.500", "0.505", "0.510"])
axR.set_yticks([490, 495, 500, 505, 510])
axR.set_xlabel("probability the predictor gets this agent right")
axR.set_title("Within a point of a coin flip", fontsize=9.0, loc="left",
              pad=8, color=INK)
axR.annotate("0.5005", xy=(P_STAR, one(P_STAR) / 1e3), xytext=(P_STAR, 490.6),
             fontsize=7.8, color=INK, ha="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=3, shrinkB=3))
axR.text(0.5, 509.6, "a fair coin", fontsize=7.4, color=MUTED, ha="center")
axR.text(0.5086, 500.0, "one box", color=BLUE, fontsize=8.2, ha="right",
         va="center")
axR.text(0.4914, 500.0, "both boxes", color=ORANGE, fontsize=8.2, ha="left",
         va="center")
axR.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
