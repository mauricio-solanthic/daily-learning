"""Figure for report 024 — what the shape parameter decides, and how slowly it settles.

Left panel — return level against return period for three generalised extreme
value distributions that share a location of 3.00 m and a scale of 0.30 m and
differ only in the shape parameter xi. Over the range a century of annual
records actually constrains, the three are nearly indistinguishable: at a
ten-year return period they span 23 cm. Extrapolated a thousandfold, to the
10,000-year level a Dutch dike ring is designed against, they span 4.46 m. The
xi = -0.15 curve is bounded above by mu - sigma/xi = 5.00 m exactly, and no
return period however long can push it past that line.

Right panel — the penultimate problem. Maxima of n independent standard normal
variables were simulated and a GEV fitted to each sample. The fitted shape is
negative at every finite n, tracking the theoretical penultimate value
-1/(2 ln n) (Fisher and Tippett 1928; Cohen 1982), and approaches the true
limiting xi = 0 at the speed of one over the logarithm of the sample size. The
most famously unbounded distribution in statistics looks bounded at every sample
size anyone will ever collect.

Palette: the blue/orange/green set already validated for this series (009-023),
all-pairs checked at print contrast. Series are labelled directly; this is print.
Run: python3 figures/024-shape-parameter.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import math
import tempfile
from pathlib import Path
from scipy import stats

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE, GREEN = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, GRIDC = "#0b0b0b", "#52514e", "#e6e6e2"


def use_vendored_pagella():
    """Register tools/fonts/texgyrepagella-*.woff2 with matplotlib."""
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

MU, SIGMA = 3.00, 0.30


# ---------------------------------------------------------------- mechanics
def return_level(T, xi, mu=MU, sigma=SIGMA):
    """The level exceeded by one annual maximum in T, for a GEV with shape xi."""
    y = -np.log1p(-1.0 / np.asarray(T, dtype=float))
    if xi == 0.0:
        return mu - sigma * np.log(y)
    return mu + (sigma / xi) * (y ** (-xi) - 1.0)


def penultimate_shape(n):
    """Fisher-Tippett's penultimate shape for the maximum of n standard normals."""
    return -1.0 / (2.0 * np.log(n))


def fitted_shape(n, reps, rng):
    """Shape of a GEV fitted to `reps` maxima of n standard normals."""
    out = np.empty(reps)
    chunk = max(1, 8_000_000 // n)
    i = 0
    while i < reps:
        k = min(chunk, reps - i)
        out[i:i + k] = rng.standard_normal((k, n)).max(axis=1)
        i += k
    return -stats.genextreme.fit(out)[0]      # scipy's c is -xi


assert abs(return_level(10_000, -0.15) - 4.497619) < 1e-5
assert abs(return_level(10_000, 0.0) - 5.763087) < 1e-5
assert abs(return_level(10_000, 0.15) - 8.962084) < 1e-5
assert abs((MU - SIGMA / -0.15) - 5.0) < 1e-12

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.06, 1.0],
                                                wspace=0.30))

# ---- left: what the shape parameter decides ------------------------------
T = np.exp(np.linspace(np.log(1.6), np.log(3e4), 700))
axL.axvspan(1.6, 100, color="#f4f3ef", zorder=0)
axL.text(1.80, 9.35, "range a century of\nannual records constrains",
         fontsize=7.2, color=MUTED, ha="left", va="top")

axL.axhline(MU - SIGMA / -0.15, color=GREEN, lw=0.8, ls=(0, (3, 2.4)), zorder=2)
axL.text(1.80, 5.06, "a ceiling at 5.00 m",
         fontsize=7.4, color=GREEN, ha="left", va="bottom")

for xi, colour, label, lxy, va in ((0.15, ORANGE, "$\\xi = +0.15$", (2.2e3, 7.42), "bottom"),
                                   (0.0, BLUE, "$\\xi = 0$", (2.7e4, 5.74), "top"),
                                   (-0.15, GREEN, "$\\xi = -0.15$", (3.8e3, 4.30), "top")):
    axL.plot(T, return_level(T, xi), color=colour, lw=1.8, zorder=4)
    axL.text(lxy[0], lxy[1], label, color=colour, fontsize=8.2, ha="right", va=va)

axL.annotate("", xy=(1.0e4, return_level(1.0e4, 0.15)),
             xytext=(1.0e4, return_level(1.0e4, -0.15)),
             arrowprops=dict(arrowstyle="<->", color=INK, lw=0.7,
                             shrinkA=0, shrinkB=0), zorder=6)
axL.annotate("4.46 m apart at 10,000 years", xy=(1.0e4, 4.44),
             xytext=(1.0e4, 3.62), fontsize=7.4, color=INK,
             ha="center", va="top",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=3, shrinkB=2))
axL.annotate("23 cm apart\nat 10 years", xy=(10.0, 3.69), xytext=(1.80, 4.62),
             fontsize=7.4, color=INK, ha="left", va="top",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=3, shrinkB=4))
axL.set_xscale("log")
axL.set_xlim(1.6, 3e4)
axL.set_ylim(3.0, 9.6)
axL.set_xlabel("return period, years")
axL.set_ylabel("return level, metres")
axL.set_title("One parameter, three futures", fontsize=9.0, loc="left", pad=8, color=INK)
axL.grid(color=GRIDC, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: the penultimate problem --------------------------------------
rng = np.random.default_rng(20260918)
ns = np.array([100, 316, 1000, 3162, 10000, 31623, 100000, 316228])
reps = 60000
fits = np.array([fitted_shape(int(n), reps, rng) for n in ns])
grid = np.exp(np.linspace(np.log(30), np.log(1e12), 500))

axR.axhline(0.0, color=INK, lw=0.8, ls=(0, (3, 2.4)), zorder=2)
axR.text(1.4e11, 0.006, "the true limit,  $\\xi = 0$", fontsize=7.4, color=INK,
         ha="right", va="bottom")
axR.plot(grid, penultimate_shape(grid), color=BLUE, lw=1.7, zorder=3)
axR.text(1.2e7, -0.038, "$-1/(2\\ln n)$", color=BLUE, fontsize=8.2,
         ha="left", va="top")
axR.plot(ns, fits, "o", ms=4.0, color=ORANGE, zorder=5,
         markeredgecolor="white", markeredgewidth=0.5)
axR.text(1.1e2, -0.152, "shape fitted to simulated\nmaxima of $n$ normals",
         color=ORANGE, fontsize=7.4, ha="left", va="top")
axR.text(9e11, -0.105, "still $-0.02$ at a\ntrillion observations",
         fontsize=7.4, color=MUTED, ha="right", va="top")
axR.set_xscale("log")
axR.set_xlim(30, 1e12)
axR.set_ylim(-0.185, 0.045)
axR.set_xlabel("observations per block, $n$")
axR.set_ylabel("effective shape parameter")
axR.set_title("A bounded-looking normal", fontsize=9.0, loc="left", pad=8, color=INK)
axR.grid(color=GRIDC, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
for T_ in (10, 100, 10_000):
    lo, mid, hi = (return_level(T_, x) for x in (-0.15, 0.0, 0.15))
    print(f"  T={T_:6d}: {lo:.4f} / {mid:.4f} / {hi:.4f}   spread {hi - lo:.4f} m")
print(f"  upper endpoint xi=-0.15: {MU - SIGMA / -0.15:.4f} m")
for n, f in zip(ns, fits):
    print(f"  n={int(n):7d}  fitted xi {f:+.5f}   -1/(2 ln n) {penultimate_shape(float(n)):+.5f}")
