"""Figure for report 014 — the threshold is set by the mean, the outcome is not.

A Galton-Watson process starts from one individual whose number of offspring is
drawn from a law with probability generating function f(s) = sum_j p_j s^j. The
extinction probability q is the smallest root in [0, 1] of

    q = f(q),

and f'(1) is the mean offspring number m. Every law with m > 1 has q < 1, and
every law with m <= 1 has q = 1: that is the whole of the criticality theorem.

Three laws are plotted, all with the same mean m = 2, so all three have the same
slope where they meet the diagonal at s = 1, and all three cross the threshold at
exactly the same place:

    Poisson(2)              f(s) = exp(-2(1-s))                  variance 2
    geometric, NB k = 1     f(s) = 1 / (1 + 2(1-s))              variance 6
    negative binomial       f(s) = (1 + 20(1-s))^(-0.1)           variance 42
      with k = 0.1, the order of magnitude Endo et al. estimated for
      SARS-CoV-2 transmission

Left panel — the fixed-point construction at m = 2. The three curves have the
same tangent at the top right corner and wildly different first crossings:
q = 0.203, 0.500 and 0.890.

Right panel — the survival probability 1 - q as the mean is swept from 0.5 to 3.
All three curves lift off the axis at m = 1 and nowhere else, which is the point
of the pairing: the threshold is a property of the mean alone, and everything
above the threshold is a property of the whole distribution.

Palette: the blue / orange / green trio used in reports 009-013, direct-labelled
rather than legended, as this is print.
Run: python3 figures/014-branching-fixed-point.py
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


def pgf_poisson(s, m):
    return np.exp(-m * (1.0 - s))


def pgf_nb(s, m, k):
    return (1.0 + (m / k) * (1.0 - s)) ** (-k)


LAWS = [
    ("Poisson", BLUE, lambda s, m: pgf_poisson(s, m)),
    ("geometric", ORANGE, lambda s, m: pgf_nb(s, m, 1.0)),
    ("k = 0.1", GREEN, lambda s, m: pgf_nb(s, m, 0.1)),
]


def extinction(f, m, iters=400000):
    """Smallest fixed point of f in [0, 1], reached by iterating from zero."""
    q = 0.0
    for _ in range(iters):
        nxt = f(np.array([q]), m)[0]
        if abs(nxt - q) < 1e-14:
            return nxt
        q = nxt
    return q


fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.15),
                               gridspec_kw=dict(width_ratios=[1.0, 1.06],
                                                wspace=0.30))

# ---- left: the fixed-point construction at m = 2 -------------------------
M = 2.0
s = np.linspace(0.0, 1.0, 1200)
axL.plot(s, s, color="#9a9a94", lw=0.8, ls=(0, (3, 2.5)), zorder=2)
for label, colour, f in LAWS:
    axL.plot(s, f(s, M), color=colour, lw=1.7, zorder=3)
    q = extinction(f, M)
    axL.plot([q], [q], marker="o", ms=3.4, color=colour, zorder=5,
             markeredgecolor="white", markeredgewidth=0.7)
    axL.plot([q, q], [0.0, q], color=colour, lw=0.6, ls=(0, (1.6, 2.0)),
             zorder=2)
axL.set_xlim(0, 1)
axL.set_ylim(0, 1)
axL.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_xlabel("$s$")
axL.set_ylabel("$f(s)$, all three with mean 2")
axL.set_title("Where the generating function meets the diagonal",
              fontsize=9.0, loc="left", pad=8, color=INK)
axL.text(0.30, 0.815, "$k = 0.1$", color=GREEN, fontsize=8.0, ha="center")
axL.text(0.145, 0.465, "geometric", color=ORANGE, fontsize=8.0, ha="center")
axL.text(0.615, 0.165, "Poisson", color=BLUE, fontsize=8.0, ha="center")
axL.text(0.262, 0.030, "0.203", color=BLUE, fontsize=7.4, ha="center")
axL.text(0.565, 0.030, "0.500", color=ORANGE, fontsize=7.4, ha="center")
axL.text(0.822, 0.030, "0.890", color=GREEN, fontsize=7.4, ha="center")
axL.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: survival probability as the mean is swept --------------------
means = np.linspace(0.5, 3.0, 251)
for label, colour, f in LAWS:
    surv = np.array([max(0.0, 1.0 - extinction(f, float(m), iters=60000))
                     for m in means])
    axR.plot(means, surv, color=colour, lw=1.7, zorder=3)
axR.axvline(1.0, color="#9a9a94", lw=0.7, ls=(0, (3, 2.5)), zorder=2)
axR.set_xlim(0.5, 3.0)
axR.set_ylim(0, 1.0)
axR.set_xticks([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
axR.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axR.set_xlabel("mean offspring number $m$")
axR.set_ylabel("probability one ancestor is never extinct")
axR.set_title("The threshold sits at one for every law",
              fontsize=9.0, loc="left", pad=8, color=INK)
axR.text(2.45, 0.90, "Poisson", color=BLUE, fontsize=8.0, ha="center")
axR.text(2.55, 0.60, "geometric", color=ORANGE, fontsize=8.0, ha="center")
axR.text(2.55, 0.155, "$k = 0.1$", color=GREEN, fontsize=8.0, ha="center")
axR.annotate("$m = 1$", xy=(1.0, 0.72), xytext=(1.34, 0.80),
             fontsize=7.8, color=MUTED, ha="left",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=3, shrinkB=3))
axR.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

for label, colour, f in LAWS:
    print("%-10s  m=2: q=%.4f    m=1.001: q=%.6f    m=0.999: q=%.6f"
          % (label, extinction(f, 2.0), extinction(f, 1.001, iters=2000000),
             extinction(f, 0.999, iters=2000000)))

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
