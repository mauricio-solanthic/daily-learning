"""Figure for report 023 — the two things an outcome tells you, and the gap between them.

Both panels use the same model. An agent has a per-episode probability c of
causing harm. The population mean is fixed at m = 12,429 / 125,000,000 = 9.943e-5,
the ratio of deaths in US alcohol-impaired-driving crashes in 2023 to the CDC's
estimate of annual alcohol-impaired driving episodes. A crash can kill more than
one person, so that ratio is an upper bound on the per-episode probability.

Left panel — harm as evidence. Two types, careless (harm rate p1) and careful
(p0), with likelihood ratio rho = p1 / p0. Bayes gives the posterior probability
that the agent was careless, given that harm did or did not occur, as a function
of the prior. At rho = 100 the harm curve sits far above the diagonal and the
no-harm curve is graphically indistinguishable from it: a rare harm is powerful
evidence, and its absence is almost none.

Right panel — harm as a measurement. Culpability c is lognormal about m with log
standard deviation sigma, and each episode's outcome is Bernoulli(c). By the law
of total variance the correlation between an agent's true c and their observed
harm count over n episodes is sqrt(n Var(c) / (n Var(c) + E[c(1-c)])). Even at a
thirteen-fold spread between the tenth and ninetieth percentile agent, a single
episode correlates 0.013 with how dangerous the agent actually is, and it takes
about 1,950 episodes — sixty-eight years at the observed rate — to reach 0.5.

Palette: the blue/orange/green set already validated for this series (009-022),
all-pairs checked at print contrast. Series are labelled directly; this is print.
Run: python3 figures/023-outcome-as-evidence.py
"""
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

    The repository vendors the faces on purpose, and matplotlib cannot read
    woff2 directly, so decompress them to ttf in a temporary directory and
    register those.
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
    "mathtext.cal": SERIF, "mathtext.sf": SERIF, "mathtext.tt": SERIF,
    "axes.edgecolor": "#c9c9c4", "axes.linewidth": 0.6,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.facecolor": "white", "savefig.facecolor": "white",
})

MEAN = 12429.0 / 125e6         # deaths per episode; an upper bound on P(harm)


# ---------------------------------------------------------------- mechanics
def posterior(prior, p1, p0, harm):
    """P(careless | outcome) under two types with harm rates p1 and p0."""
    lik1 = p1 if harm else 1.0 - p1
    lik0 = p0 if harm else 1.0 - p0
    return prior * lik1 / (prior * lik1 + (1.0 - prior) * lik0)


def moments(sigma, mean=MEAN):
    """Var(c) and E[c(1-c)] for c lognormal with this mean and log sd."""
    second = mean ** 2 * np.exp(sigma ** 2)
    return second - mean ** 2, mean - second


def corr(n, sigma):
    """Correlation of true culpability with the harm count over n episodes."""
    var_c, e_c1c = moments(sigma)
    return np.sqrt(n * var_c / (n * var_c + e_c1c))


P0, RHO = 1e-5, 100.0
P1 = P0 * RHO
assert abs(posterior(0.10, P1, P0, True) - 0.91743) < 1e-4
assert abs(corr(1.0, 1.0) - 0.013073) < 1e-5

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.0, 1.06],
                                                wspace=0.30))

# ---- left: harm as evidence ----------------------------------------------
pri = np.linspace(0.0, 1.0, 601)
axL.plot(pri, pri, color=INK, lw=0.8, ls=(0, (4, 3.2)), zorder=5)
axL.plot(pri, posterior(pri, P1, P0, True), color=ORANGE, lw=1.8, zorder=4)
axL.plot(pri, posterior(pri, P1, P0, False), color=BLUE, lw=1.8, zorder=3)
axL.plot([0.10], [posterior(0.10, P1, P0, True)], "o", ms=3.8, color=ORANGE, zorder=6)
axL.plot([0.10], [posterior(0.10, P1, P0, False)], "o", ms=3.8, color=BLUE, zorder=6)
axL.annotate("harm occurred:\n0.10 becomes 0.92",
             xy=(0.10, posterior(0.10, P1, P0, True)), xytext=(0.245, 0.735),
             fontsize=7.4, color=ORANGE, ha="left", va="top",
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                             shrinkA=3, shrinkB=4))
axL.annotate("no harm:\n0.10 becomes 0.0999",
             xy=(0.10, posterior(0.10, P1, P0, False)), xytext=(0.335, 0.215),
             fontsize=7.4, color=BLUE, ha="left", va="top",
             arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6,
                             shrinkA=3, shrinkB=4))
axL.text(0.745, 0.395, "the no-harm curve lies\non the line of no revision",
         fontsize=7.4, color=MUTED, ha="center", va="bottom")
axL.set_xlim(0, 1)
axL.set_ylim(0, 1)
axL.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_xlabel("prior probability the agent was careless")
axL.set_ylabel("probability after the outcome")
axL.set_title("An outcome as evidence", fontsize=9.0, loc="left", pad=8, color=INK)
axL.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: harm as a measurement ----------------------------------------
n = np.exp(np.linspace(0.0, np.log(3e5), 500))
for sigma, colour, label, lxy in ((2.0, GREEN, "$\\sigma = 2$", (1.35, 0.655)),
                                  (1.0, ORANGE, "$\\sigma = 1$", (4.2e2, 0.595)),
                                  (0.5, BLUE, "$\\sigma = 0.5$", (3.4e4, 0.125))):
    axR.plot(n, corr(n, sigma), color=colour, lw=1.7, zorder=3)
    axR.text(lxy[0], lxy[1], label, color=colour, fontsize=8.2, ha="left", va="bottom")
axR.axhline(0.5, color=INK, lw=0.8, ls=(0, (3, 2.4)), zorder=2)
axR.axvline(28.8, color=MUTED, lw=0.8, ls=(0, (1.4, 2.0)), zorder=2)
axR.text(23.0, 0.955, "one year of\nepisodes (29)", fontsize=7.4, color=MUTED,
         ha="right", va="top")
n_half = moments(1.0)[1] / (3.0 * moments(1.0)[0])
axR.plot([n_half], [0.5], "o", ms=3.8, color=ORANGE, zorder=5)
axR.annotate(f"{n_half:,.0f} episodes\n= 68 years", xy=(n_half, 0.5),
             xytext=(3.0e3, 0.245), fontsize=7.4, color=ORANGE, ha="left", va="top",
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                             shrinkA=3, shrinkB=4))
axR.set_xscale("log")
axR.set_xlim(1, 3e5)
axR.set_ylim(0, 1)
axR.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axR.set_xlabel("episodes observed for one agent")
axR.set_ylabel("correlation with true culpability")
axR.set_title("An outcome as a measurement", fontsize=9.0, loc="left", pad=8, color=INK)
axR.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
print(f"  posterior after harm at prior 0.10: {posterior(0.10, P1, P0, True):.5f}")
print(f"  posterior after no harm:            {posterior(0.10, P1, P0, False):.6f}")
print(f"  corr at n=1, sigma=1:               {corr(1.0, 1.0):.5f}")
print(f"  corr reaches 0.5 at n =             {n_half:,.0f}")
