"""Figure for report 023 — the shape parameter, and how slowly the limit arrives.

Left panel — the extrapolation fan. Three generalised extreme value laws are
given the same scale (sigma = 1) and their locations are chosen so that all
three agree exactly on the 100-year return level, which is roughly the longest
return period a century of annual maxima can pin down directly. The curves are

    z(T) = mu + (sigma/xi) * [ (-ln(1 - 1/T))^(-xi) - 1 ],   xi != 0
    z(T) = mu - sigma * ln( -ln(1 - 1/T) ),                  xi = 0

plotted against return period on a log axis, which is the standard Gumbel
return-level plot: xi = 0 draws a straight line, xi < 0 bends towards its
finite upper endpoint at mu + sigma/|xi|, xi > 0 curves away without bound.
Past the anchor the three agree on nothing. The 10,000-year level sits 1.20,
4.61 and 19.00 sigma above the 100-year level for xi = -0.2, 0 and +0.2 — a
spread of nearly sixteen to one, on data that cannot distinguish the three.

Right panel — the rate at which the Gumbel limit actually arrives for a
Gaussian parent. Plotted is the supremum distance between the exact law of the
maximum of n standard normals, normalised by the classical constants
b_n = Phi^-1(1 - 1/n) and a_n = 1 / (n phi(b_n)), and two approximations: the
Gumbel limit that Fisher and Tippett's theorem guarantees, and the best-fitting
generalised extreme value law of the same norming with a free shape. The first
decays like 1/ln n — squaring n halves the error, so a trillion observations
are twice as good as a million — while the second, with a shape of only about
-0.04 at n = 10^6, is more than an order of magnitude closer. Fisher and
Tippett noticed this in the founding paper; it is the penultimate
approximation.

Both panels are computed, not drawn by hand; every plotted value is reproduced
in the report's verification pass.

Palette: the blue / orange / green trio used in reports 009-018, direct-labelled
rather than legended, as this is print.
Run: python3 figures/023-shape-parameter-and-convergence.py
"""
import math
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm

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
    tmp = Path(tempfile.mkdtemp(prefix="pagella-"))
    for src in vendored:
        face = TTFont(str(src))
        face.flavor = None                      # woff2 -> ttf
        out = tmp / (src.stem + ".ttf")
        face.save(str(out))
        fm.fontManager.addfont(str(out))
    return SERIF in {f.name for f in fm.fontManager.ttflist}


if not use_vendored_pagella():
    raise SystemExit("vendored Pagella not registered — refusing to draw in a "
                     "substitute face (see docs/source-notes.md)")

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": [SERIF],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9.5,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.linewidth": 0.7,
})


# ---------------------------------------------------------------- left panel
def return_level(T, mu, sigma, xi):
    y = -np.log(1.0 - 1.0 / np.asarray(T, dtype=float))
    if abs(xi) < 1e-12:
        return mu - sigma * np.log(y)
    return mu + (sigma / xi) * (y ** (-xi) - 1.0)


SHAPES = ((-0.20, GREEN, r"$\xi = -0.2$"),
          (0.0, BLUE, r"$\xi = 0$"),
          (0.20, ORANGE, r"$\xi = +0.2$"))

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.4, 3.15))

T = np.logspace(math.log10(1.05), 4.0, 900)
for xi, colour, label in SHAPES:
    mu = -return_level(100.0, 0.0, 1.0, xi)      # anchor: z(100) = 0
    axL.plot(T, return_level(T, mu, 1.0, xi), color=colour, lw=1.5)

axL.axvline(100, color=MUTED, lw=0.6, ls=(0, (4, 3)))
axL.plot([100], [0], "o", ms=3.4, color=INK, zorder=5)
axL.set_xscale("log")
axL.set_xlim(1.05, 3.4e4)
axL.set_ylim(-6.2, 21.5)
axL.set_xlabel("return period (years)")
axL.set_ylabel(r"level, in units of the scale $\sigma$")
axL.grid(True, which="major", color=GRID, lw=0.6)
axL.set_axisbelow(True)

for xi, colour, label in SHAPES:
    mu = -return_level(100.0, 0.0, 1.0, xi)
    y = float(return_level(1.0e4, mu, 1.0, xi))
    axL.annotate(label, xy=(1.05e4, y), xytext=(4, 0),
                 textcoords="offset points", color=colour, fontsize=9,
                 va="center", ha="left")
axL.annotate("fitted here", xy=(100, 0), xytext=(-6, -34),
             textcoords="offset points", color=MUTED, fontsize=8.5, ha="right")
axL.annotate("extrapolated here", xy=(3000, -4.6), color=MUTED, fontsize=8.5,
             ha="center")
axL.set_title("Same data, three answers", fontsize=10, color=INK, pad=7)


# --------------------------------------------------------------- right panel
GRIDX = np.linspace(-4.0, 14.0, 200001)


def norming(n):
    b = norm.isf(1.0 / n)
    return 1.0 / (n * norm.pdf(b)), b


def exact_max_cdf(n):
    a, b = norming(n)
    return np.exp(n * norm.logcdf(a * GRIDX + b))


def sup_err(n, xi):
    exact = exact_max_cdf(n)
    if abs(xi) < 1e-12:
        limit = np.exp(-np.exp(-GRIDX))
    else:
        t = 1.0 + xi * GRIDX
        limit = np.where(t > 0,
                         np.exp(-np.power(np.maximum(t, 1e-300), -1.0 / xi)),
                         0.0)
    return float(np.max(np.abs(exact - limit)))


exps = np.arange(1, 25)
ns = 10.0 ** exps
gumbel_err = np.array([sup_err(n, 0.0) for n in ns])
best_err, best_xi = [], []
for n in ns:
    r = minimize_scalar(lambda x: sup_err(n, x), bounds=(-0.5, 0.0),
                        method="bounded", options={"xatol": 1e-6})
    best_err.append(r.fun)
    best_xi.append(r.x)
best_err = np.array(best_err)

axR.plot(ns, gumbel_err, color=BLUE, lw=1.5)
axR.plot(ns, best_err, color=ORANGE, lw=1.5)
axR.plot(ns, 0.125 / np.log(ns), color=MUTED, lw=0.9, ls=(0, (4, 3)))
axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlim(6, 3e25)
axR.set_ylim(2e-6, 0.25)
axR.set_xlabel("sample size $n$")
axR.set_ylabel("largest error in the approximation")
axR.grid(True, which="major", color=GRID, lw=0.6)
axR.set_axisbelow(True)
axR.set_xticks([1e2, 1e6, 1e12, 1e18, 1e24])
axR.set_xticks([], minor=True)

axR.annotate("the Gumbel limit", xy=(1e14, gumbel_err[13]), xytext=(0, 9),
             textcoords="offset points", color=BLUE, fontsize=9, ha="center")
axR.annotate(r"$0.125 / \ln n$", xy=(1e21, 0.125 / np.log(1e21)),
             xytext=(0, -15), textcoords="offset points", color=MUTED,
             fontsize=8.5, ha="center")
axR.annotate("best shape of its own\n(the penultimate fit)",
             xy=(1e10, best_err[9]), xytext=(0, -30),
             textcoords="offset points", color=ORANGE, fontsize=9, ha="center")
axR.set_title("How slowly the theorem arrives", fontsize=10, color=INK, pad=7)

for ax in (axL, axR):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

fig.tight_layout(pad=0.6, w_pad=2.2)
out = Path(__file__).resolve().parent / "023-shape-parameter-and-convergence.png"
fig.savefig(out, dpi=260, facecolor="white")
print("wrote", out)
print("gaps z(10^4) - z(100):",
      {xi: round(float(return_level(1e4, -return_level(100.0, 0.0, 1.0, xi),
                                    1.0, xi)), 3) for xi, _, _ in SHAPES})
print("n=1e6  gumbel err", round(sup_err(1e6, 0.0), 5),
      " best xi", round(best_xi[5], 4), " err", round(best_err[5], 5))
