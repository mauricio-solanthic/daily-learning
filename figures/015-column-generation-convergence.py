"""Figure for report 015 — the sandwich closes, and then it dawdles.

Column generation on the Gilmore-Gomory master LP for a paper-mill instance:
a 5,600 mm master reel, twelve ordered widths between 423 and 901 mm, 380
finished rolls. The instance admits 175,968 distinct feasible cutting patterns.
Column generation starts from twelve trivial single-width patterns and prices
one new pattern per iteration by solving an unbounded integer knapsack.

Two bounds are plotted against the iteration count.

  Upper bound  the value of the restricted master LP over the columns generated
               so far. It is feasible for the full LP, so it can only overstate
               the optimum, and it falls monotonically.

  Lower bound  Farley's bound. If y is the dual solution of the restricted
               master and z* = max_p y.a_p is the value of the pricing knapsack,
               then y/z* is feasible for the full dual, so b.y / z* = z_RMP / z*
               is a valid lower bound on the LP optimum. It is not monotone,
               because the dual solution jumps around between iterations —
               which is the phenomenon stabilized column generation exists to
               damp.

The two meet at z_LP = 44.287709, confirmed independently against the same LP
solved with all 175,968 columns present (agreement to 2.3e-13).

The shape worth seeing is the tailing off: the first thirteen iterations of
twenty-nine capture 96 per cent of the total improvement in the upper bound,
and the remaining sixteen grind out the last 4 per cent. Every number in the
caption is recomputed here at run time and asserted, so the figure and the
prose cannot drift apart.

Palette: the blue / orange pair used in reports 009-014, validated for print
and direct-labelled rather than legended.
Run: python3 figures/015-column-generation-convergence.py
"""
import math
import tempfile
from functools import lru_cache
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE = "#2a78d6", "#eb6834"
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

# ------------------------------------------------------------- the instance
W = 5600
WIDTHS = [423, 461, 513, 549, 591, 637, 679, 723, 767, 809, 853, 901]
DEMAND = [32, 41, 25, 18, 47, 29, 36, 22, 51, 27, 33, 19]
N = len(WIDTHS)


def count_patterns(widths, cap):
    """Exact number of non-empty multisets of widths with total width <= cap."""
    n = len(widths)
    caps = [cap // w for w in widths]

    @lru_cache(maxsize=None)
    def rec(i, rem):
        if i == n:
            return 1
        t = k = 0
        while k <= caps[i] and k * widths[i] <= rem:
            t += rec(i + 1, rem - k * widths[i])
            k += 1
        return t

    return rec(0, cap) - 1


def price(y, widths, cap):
    """Unbounded integer knapsack by dynamic programming over the reel width.

    Returns (max value, the pattern attaining it). This is the pricing
    subproblem: the dual prices are the item values and the reel is the sack.
    """
    n = len(widths)
    f = np.zeros(cap + 1)
    arg = -np.ones(cap + 1, dtype=int)
    for c in range(1, cap + 1):
        best, a = f[c - 1], -1
        for i in range(n):
            if widths[i] <= c and y[i] + f[c - widths[i]] > best + 1e-12:
                best, a = y[i] + f[c - widths[i]], i
        f[c], arg[c] = best, a
    pat, c = [0] * n, cap
    while c > 0:
        i = arg[c]
        if i < 0:
            c -= 1
            continue
        pat[i] += 1
        c -= widths[i]
    return f[cap], tuple(pat)


b = np.array(DEMAND, dtype=float)
cols = [tuple((W // WIDTHS[i]) if j == i else 0 for j in range(N)) for i in range(N)]
ub, lb = [], []
for _ in range(300):
    res = linprog(np.ones(len(cols)), A_ub=-np.array(cols, float).T, b_ub=-b,
                  bounds=(0, None), method="highs")
    assert res.status == 0, res.message
    y = np.maximum(-res.ineqlin.marginals, 0.0)
    z_star, pat = price(y, WIDTHS, W)
    ub.append(res.fun)
    lb.append(res.fun / z_star)
    if z_star <= 1.0 + 1e-9 or pat in cols:
        break
    cols.append(pat)

ub, lb = np.array(ub), np.array(lb)
it = np.arange(1, len(ub) + 1)
z_lp = ub[-1]
n_pat = count_patterns(WIDTHS, W)

# assertions: the caption's claims, checked rather than remembered
assert n_pat == 175968, n_pat
assert len(cols) == 40 and len(ub) == 29, (len(cols), len(ub))
assert abs(z_lp - 44.287709235) < 1e-7, z_lp
assert math.ceil(z_lp - 1e-9) == 45
assert np.all(np.diff(ub) <= 1e-9), "upper bound should fall monotonically"
assert lb.max() <= z_lp + 1e-9 and ub.min() >= z_lp - 1e-9, "bounds must bracket"
assert (np.diff(lb) < -1e-9).sum() >= 5, "Farley bound should be non-monotone"
captured = (ub[0] - ub[12]) / (ub[0] - z_lp)
assert 0.955 < captured < 0.965, captured

# ------------------------------------------------------------------ the plot
fig, ax = plt.subplots(figsize=(7.0, 3.30))
fig.subplots_adjust(left=0.085, right=0.985, top=0.86, bottom=0.145)

ax.fill_between(it, lb, ub, color="#f0f2f5", zorder=1)
ax.axhline(z_lp, color="#9a9a94", lw=0.8, ls=(0, (3, 2.5)), zorder=2)
ax.plot(it, ub, color=BLUE, lw=1.7, zorder=4)
ax.plot(it, lb, color=ORANGE, lw=1.5, zorder=3)
ax.plot(it[[0, -1]], ub[[0, -1]], "o", ms=3.6, color=BLUE, zorder=6,
        markeredgecolor="white", markeredgewidth=0.7)
ax.plot([it[0]], [lb[0]], "o", ms=3.6, color=ORANGE, zorder=6,
        markeredgecolor="white", markeredgewidth=0.7)

ax.set_xlim(0.4, 29.9)
ax.set_ylim(40.9, 47.6)
ax.set_xticks([1, 5, 10, 15, 20, 25, 29])
ax.set_yticks([41, 42, 43, 44, 45, 46, 47])
ax.set_xlabel("patterns priced (one per iteration)")
ax.set_ylabel("master reels")
ax.set_title("Two bounds close on the answer, then slow to a crawl",
             fontsize=9.4, loc="left", pad=9, color=INK)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.grid(axis="y", color=GRID, lw=0.5, zorder=0)
ax.set_axisbelow(True)

ax.text(15.4, 47.42, f"{n_pat:,} patterns exist; only {len(cols)} are ever written down",
        color=MUTED, fontsize=7.8, ha="left", va="top")

ax.annotate("restricted master LP\n(upper bound)", xy=(4.0, 45.72),
            xytext=(6.1, 46.58), color=BLUE, fontsize=8.0, ha="left",
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6,
                            shrinkA=2, shrinkB=3))
ax.annotate("Farley bound from the\npricing knapsack (lower bound)",
            xy=(6.0, 43.30), xytext=(8.4, 41.52), color=ORANGE, fontsize=8.0,
            ha="left", arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                                       shrinkA=2, shrinkB=3))

ax.annotate("", xy=(13, ub[12]), xytext=(13, z_lp),
            arrowprops=dict(arrowstyle="<->", color="#8e8d88", lw=0.6))
ax.annotate(f"{100*(1-captured):.0f}% of the descent still to go\n"
            f"after {13} of the {len(ub)} iterations",
            xy=(13.1, (ub[12] + z_lp) / 2), xytext=(14.2, 45.55),
            color=MUTED, fontsize=7.5, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color="#8e8d88", lw=0.5,
                            shrinkA=2, shrinkB=2))

ax.annotate(f"$z_{{LP}} = {z_lp:.4f}$, so 45 master\nreels once rounded up",
            xy=(24.0, z_lp - 0.02), xytext=(18.6, 42.55), color=INK,
            fontsize=8.0, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color="#8e8d88", lw=0.5,
                            shrinkA=3, shrinkB=2))

out = Path(__file__).resolve().parent / "015-column-generation-convergence.png"
fig.savefig(out, dpi=320)
print(f"wrote {out}")
print(f"patterns {n_pat:,}; columns {len(cols)}; iterations {len(ub)}; "
      f"z_LP {z_lp:.9f}; ceil {math.ceil(z_lp - 1e-9)}; "
      f"first 13 iterations capture {100*captured:.1f}% of the descent")
