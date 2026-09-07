"""Figure for report 019 — the value function, and where the work actually goes.

Left panel — Dirac's value function

    V(x) = (2x - 1) ln(x / (1 - x)),

plotted on a logarithmic assay axis from 0.1 per cent to 99.9 per cent. It is
symmetric about x = 1/2, where it vanishes, and diverges logarithmically at both
ends. The point of drawing it is that the natural-uranium assay of 0.711 per cent
sits far up the left-hand wall, at V = 4.87, while weapons-grade material at 90
per cent sits low on the right at V = 1.76: the value of a kilogram of natural
uranium, on this scale, is nearly three times that of a kilogram of highly
enriched uranium. All of the separative work in enrichment comes from the mass
imbalance, not from the value of the product.

Right panel — the consequence. For one kilogram of 90 per cent product drawn
from natural feed at a tails assay of 0.25 per cent, the total separative work
is 208.03 SWU. Because separative work is additive along a route and independent
of it — verified in the report's checking pass to 1.7e-13 by comparing the direct
cascade against two-stage routes through six intermediate assays — one can ask
how much of that total has been spent by the time the material reaches an assay
x. The answer W(x) rises very steeply and then flattens: 47 per cent of the work
is done by 1 per cent, 78 per cent by 4.5 per cent reactor-fuel assay, and 92 per
cent by the 19.75 per cent HALEU ceiling. The four marked points are the assays
the report discusses.

The curve is computed, not sketched: W(x) is the stage-one separative work of a
two-stage route natural -> x -> 90 per cent, with the second stage's tails dumped
at the natural assay so that they can be recycled as first-stage feed. That
construction is what makes the split well defined.

Palette: the blue / orange trio used in reports 009-018, direct-labelled rather
than legended, as this is print.
Run: python3 figures/019-separative-work-staircase.py
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

XF = 0.00711          # natural uranium, weight fraction U-235
XT = 0.0025           # tails assay
XP = 0.90             # weapons-grade product


def V(x):
    return (2.0 * x - 1.0) * np.log(x / (1.0 - x))


def swu(xp, xf, xt, P=1.0):
    """Separative work, feed and tails masses for one cascade."""
    F = P * (xp - xt) / (xf - xt)
    T = P * (xp - xf) / (xf - xt)
    return F, T, P * V(xp) + T * V(xt) - F * V(xf)


TOTAL = swu(XP, XF, XT)[2]


def work_to(x):
    """SWU spent reaching assay x, per kg of eventual 90 per cent product."""
    Fb = (XP - XF) / (x - XF)                    # kg of x-assay material needed
    return swu(x, XF, XT, Fb)[2]


fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 2.95),
                               gridspec_kw=dict(width_ratios=[1.0, 1.05],
                                                wspace=0.30))

# ---- left: the value function --------------------------------------------
xv = np.logspace(math.log10(0.001), math.log10(0.999), 900)
axL.plot(xv, V(xv), color=BLUE, lw=1.7, zorder=3)

marks = [(XT, "tails\n0.25%", "left", 6, 0),
         (XF, "natural\n0.711%", "right", -6, 0),
         (0.045, "4.5%", "left", 5, 2),
         (XP, "90%", "right", -5, 3)]
for x, lbl, ha, dx, dy in marks:
    axL.plot([x], [V(x)], "o", ms=3.6, color=ORANGE, zorder=5,
             mec="white", mew=0.6)
    axL.annotate(lbl, xy=(x, V(x)), xytext=(dx, dy), textcoords="offset points",
                 color=MUTED, fontsize=7.2, ha=ha, va="center")

axL.set_xscale("log")
axL.set_xlim(0.001, 0.999)
axL.set_ylim(0, 7.4)
axL.set_xticks([0.001, 0.01, 0.1, 1.0])
axL.set_xticklabels(["0.1%", "1%", "10%", "100%"])
axL.set_xlabel("U-235 assay (log scale)")
axL.set_ylabel("value function $V(x)$")
axL.grid(True, axis="y", color=GRID, lw=0.5)
axL.set_axisbelow(True)
for s in ("top", "right"):
    axL.spines[s].set_visible(False)
axL.set_title("the value function measures distance\nfrom a fifty-fifty mixture",
              fontsize=7.8, color=INK, loc="left", pad=6)

# ---- right: where the separative work goes -------------------------------
xw = np.logspace(math.log10(XF * 1.02), math.log10(XP), 700)
share = np.array([100.0 * work_to(x) / TOTAL for x in xw])
axR.fill_between(xw, share, color=ORANGE, alpha=0.12, lw=0)
axR.plot(xw, share, color=ORANGE, lw=1.8, zorder=3)

pts = [(0.01, "1%", 6, -9), (0.045, "4.5%\nreactor fuel", 7, -14),
       (0.1975, "19.75%\nHALEU", 6, -13), (0.90, "90%", -4, 4)]
for x, lbl, dx, dy in pts:
    s = 100.0 * work_to(x) / TOTAL
    axR.plot([x], [s], "o", ms=3.8, color=BLUE, zorder=5, mec="white", mew=0.7)
    axR.annotate(lbl, xy=(x, s), xytext=(dx, dy), textcoords="offset points",
                 color=MUTED, fontsize=7.2,
                 ha="right" if dx < 0 else "left", va="center")

axR.axhline(100.0 * work_to(0.045) / TOTAL, color=MUTED, lw=0.8,
            ls=(0, (3, 3)), zorder=2)
axR.annotate("78", xy=(XF * 1.05, 100.0 * work_to(0.045) / TOTAL),
             xytext=(0, 3), textcoords="offset points", color=MUTED,
             fontsize=7.2, ha="left", va="bottom")

# The curve does not start at zero. Stripping 0.25 per cent tails out of the
# very large feed mass is work that every route must pay, and in the limit as
# the intermediate assay approaches natural it still accounts for 37 per cent
# of the total. Annotated rather than hidden by truncating the axis.
axR.annotate("37% before the assay\nhas moved at all", xy=(XF * 1.03, share[0]),
             xytext=(9, -12), textcoords="offset points", color=MUTED,
             fontsize=7.0, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=1, shrinkB=2))

axR.set_xscale("log")
axR.set_xlim(XF, 1.0)
axR.set_ylim(0, 104)
axR.set_xticks([0.01, 0.1, 1.0])
axR.set_xticklabels(["1%", "10%", "100%"])
axR.set_yticks([0, 25, 50, 75, 100])
axR.set_xlabel("assay reached (log scale)")
axR.set_ylabel("per cent of the 208 SWU spent")
axR.grid(True, axis="y", color=GRID, lw=0.5)
axR.set_axisbelow(True)
for s in ("top", "right"):
    axR.spines[s].set_visible(False)
axR.set_title("the road to weapons-grade, and how far\nreactor fuel already is along it",
              fontsize=7.8, color=INK, loc="left", pad=6)

out = Path(__file__).resolve().parent / "019-separative-work-staircase.png"
fig.savefig(out, dpi=340, bbox_inches="tight", pad_inches=0.02)
print(f"wrote {out}")
print(f"total = {TOTAL:.5f} SWU per kg of 90% product")
for x in (0.01, 0.03, 0.045, 0.05, 0.1975, 0.60):
    print(f"  W({x*100:6.2f}%) = {work_to(x):8.3f} SWU = {100*work_to(x)/TOTAL:6.2f}%")
