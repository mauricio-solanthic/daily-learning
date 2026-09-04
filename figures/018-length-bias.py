"""Figure for report 018 — length-biased sampling, drawn twice.

Left panel — the two densities. Intervals between arrivals are Erlang-2 with
mean 10 minutes (shape 2, scale 5), so the coefficient of variation is
1/sqrt(2) and c^2 = 1/2. An observer who turns up at an instant chosen without
reference to the timetable lands in an interval drawn not from f but from the
length-biased density

    f*(x) = x f(x) / mu,

which for a gamma is the same family with the shape raised by one: Erlang-3
with the same scale. The two means, 10 and mu(1 + c^2) = 15 minutes, are drawn
as rules so the 50 per cent shift is legible rather than asserted.

Right panel — the expected wait as a function of the coefficient of variation,

    E[R] = (mu/2)(1 + c^2),

for mu = 10 minutes, with the five interval laws of the report's first table
placed on the curve. The dashed rule at 5 minutes is the naive answer (half the
mean headway), which is correct only for a perfectly punctual service. The
curve is drawn to c = 2 and annotated where it leaves the panel: for a Pareto
interval law with tail index at or below 2 the second moment diverges and the
expected wait is infinite even though the mean headway is finite.

Every plotted value is checked against a stationary simulation in the report's
verification pass: probing 2 million instants uniformly over a long realisation
returns 4.9998, 5.4134, 7.4955 and 9.9738 minutes against the theoretical
5.000, 5.417, 7.500 and 10.000.

Palette: the blue / orange / green trio used in reports 009-017, direct-labelled
rather than legended, as this is print.
Run: python3 figures/018-length-bias.py
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from pathlib import Path

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e6e2"


def use_vendored_pagella():
    """Register tools/fonts/texgyrepagella-*.woff2 with matplotlib.

    matplotlib cannot read woff2, so decompress the vendored faces to ttf in a
    temporary directory and register those. Naming the family and hoping the
    host has it installed is what put report 008 in the wrong typeface.
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
    "mathtext.cal": f"{SERIF}:italic", "mathtext.sf": SERIF, "mathtext.tt": SERIF,
    "axes.edgecolor": "#c9c9c4", "axes.linewidth": 0.6,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.facecolor": "white", "savefig.facecolor": "white",
})

MU = 10.0

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 2.95),
                               gridspec_kw=dict(width_ratios=[1.05, 1.0],
                                                wspace=0.27))

# ---- left: the base density and its length-biased twin -------------------
SCALE = 5.0


def gamma_pdf(x, shape, scale):
    """Erlang density for integer shape, written out to avoid a scipy import."""
    return (x ** (shape - 1) * np.exp(-x / scale)
            / (math.factorial(shape - 1) * scale ** shape))


x = np.linspace(0.0, 42.0, 700)
base = gamma_pdf(x, 2, SCALE)
biased = gamma_pdf(x, 3, SCALE)          # x f(x) / mu for Erlang-2 is Erlang-3

axL.fill_between(x, base, color=BLUE, alpha=0.13, lw=0)
axL.fill_between(x, biased, color=ORANGE, alpha=0.13, lw=0)
axL.plot(x, base, color=BLUE, lw=1.7, zorder=3)
axL.plot(x, biased, color=ORANGE, lw=1.7, zorder=3)

top = max(base.max(), biased.max())
axL.vlines(MU, 0, top * 1.02, color=BLUE, lw=0.9, ls=(0, (3, 3)), zorder=2)
axL.vlines(15.0, 0, top * 1.02, color=ORANGE, lw=0.9, ls=(0, (3, 3)), zorder=2)

# Labels sit in the empty upper right, where both curves have decayed to under
# a quarter of the peak; colour identifies them, so no leaders are needed.
axL.text(41.5, top * 1.00, "a passenger's view", color=ORANGE, fontsize=7.6,
         ha="right", va="top")
axL.text(41.5, top * 0.80, "the timetable's view", color=BLUE, fontsize=7.6,
         ha="right", va="top")
axL.annotate("10", xy=(MU, top * 1.02), xytext=(-1, 2), textcoords="offset points",
             color=BLUE, fontsize=7.4, ha="right", va="bottom")
axL.annotate("15 min", xy=(15.0, top * 1.02), xytext=(2, 2), textcoords="offset points",
             color=ORANGE, fontsize=7.4, ha="left", va="bottom")

axL.set_xlim(0, 42)
axL.set_ylim(0, top * 1.16)
axL.set_xlabel("interval between arrivals (minutes)")
axL.set_ylabel("density")
axL.set_yticks([])
axL.set_xticks([0, 10, 20, 30, 40])
for side in ("top", "right", "left"):
    axL.spines[side].set_visible(False)

# ---- right: expected wait against the coefficient of variation -----------
c = np.linspace(0.0, 2.0, 500)
axR.plot(c, MU * (1 + c ** 2) / 2, color=INK, lw=1.7, zorder=3)
axR.axhline(MU / 2, color=MUTED, lw=0.8, ls=(0, (4, 4)), zorder=2)
axR.annotate("half the mean headway", xy=(2.02, MU / 2), xytext=(0, -11),
             textcoords="offset points", color=MUTED, fontsize=7.2,
             ha="right", va="top")

POINTS = [(0.0, "clockface", GREEN, (7, 13), "left"),
          (1 / np.sqrt(12), "uniform 5-15", GREEN, (8, -8), "left"),
          (1 / np.sqrt(2), "Erlang-2", BLUE, (7, -3), "left"),
          (1.0, "Poisson arrivals", ORANGE, (-6, 4), "right"),
          (1.5, "lognormal, CV 1.5", ORANGE, (-6, 2), "right")]
for cv, label, colour, off, ha in POINTS:
    axR.plot([cv], [MU * (1 + cv ** 2) / 2], "o", ms=4.6, color=colour,
             mec="white", mew=0.8, zorder=4)
    axR.annotate(label, xy=(cv, MU * (1 + cv ** 2) / 2), xytext=off,
                 textcoords="offset points", color=colour, fontsize=7.4,
                 ha=ha, va="center")

axR.text(1.74, 25.9, "Pareto, tail index $\\leq 2$:\nsecond moment diverges,\nwait unbounded",
         color=INK, fontsize=7.2, ha="right", va="top", linespacing=1.35)

axR.set_xlim(0, 2.05)
axR.set_ylim(0, 26.5)
axR.set_xlabel("coefficient of variation of the interval, $c$")
axR.set_ylabel("expected wait (minutes)")
axR.set_yticks([0, 5, 10, 15, 20, 25])
axR.grid(axis="y", color=GRID, lw=0.6)
axR.set_axisbelow(True)
for side in ("top", "right"):
    axR.spines[side].set_visible(False)

out = Path(__file__).resolve().parent / "018-length-bias.png"
fig.savefig(out, dpi=320, bbox_inches="tight", pad_inches=0.03)
print("wrote", out)
