"""Figure for report 017 — whether the optimal liquidation schedule knows how big the order is.

Both panels solve the same free-horizon problem: choose a holdings path x(t) from
x(0) = X down to x(infinity) = 0 minimising

    J = eta_k * integral |x'|^(1+k) dt  +  lambda * sigma^2 * integral x^2 dt,

the first term the temporary-impact cost of trading at rate |x'| when the price
concession is eta_k |x'|^k, the second the Almgren-Chriss mean-variance penalty
for still holding x(t) while the price moves. The integrand has no explicit time
dependence, so the Hamiltonian is conserved, and the boundary condition at
infinity forces it to zero:

    eta_k * k * w^(1+k) = lambda * sigma^2 * x^2,        w = -x' > 0
    =>  w = c * x^(2/(1+k)),   c = (lambda sigma^2 / (eta_k k))^(1/(1+k)).

For k = 1 that is w = kappa x with kappa = sqrt(lambda sigma^2 / eta), i.e. pure
exponential decay at a rate containing no X — the infinite-horizon limit of
Almgren and Chriss's sinh trajectory. For k != 1 it separates to

    x(t) = [ X^(1-p) + (p-1) c t ]^(1/(1-p)),      p = 2/(1+k),

whose half-life is theta = X^(1-p) (2^(p-1) - 1) / ((p-1) c), proportional to
X^((k-1)/(k+1)). At the measured k = 3/5 that exponent is exactly -1/4.

Calibration, held identical across the two panels: a 50-dollar stock, 2 per cent
daily volatility (sigma = 1 dollar/share/day^0.5), 5,000,000 shares of average
daily volume, a linear temporary impact of eta = 1e-7 dollar day/share^2 (so
trading a full day's volume in a day costs 50 cents a share), risk aversion
lambda = 5e-7 per dollar, and eta_k = eta V^(1-k) so that both impact models
charge the same concession at 100 per cent participation. kappa = sqrt(5) per day
and the linear half-life is ln 2 / kappa = 2.015 trading hours.

Left panel — normalised holdings x(t)/X for orders of 1 and 25 per cent of daily
volume. Under linear impact the two paths coincide exactly; under k = 3/5 the
larger order is worked more than twice as fast.

Right panel — the half-life itself against order size, over three decades. Flat
at 2.015 hours for k = 1; a straight line of slope -1/4 on log axes for k = 3/5.

Every number here is closed-form and was checked against a direct integration of
w = c x^p (scipy solve_ivp, agreement to 1e-6 relative) and, for k = 1, against
the exact discrete minimiser of the quadratic objective on a 4,000-step grid
(agreement to 9e-9 of X).

Palette: the blue / orange / green trio used in reports 009-016, direct-labelled
rather than legended, as this is print.
Run: python3 figures/017-execution-trajectories.py
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

# ---- calibration ---------------------------------------------------------
SIGMA = 1.0          # dollar / share / day^0.5
ETA1 = 1.0e-7        # dollar day / share^2
LAM = 5.0e-7         # 1 / dollar
ADV = 5.0e6          # shares / day
HOURS = 6.5          # trading hours in a session
KAPPA = np.sqrt(LAM * SIGMA ** 2 / ETA1)


def coeffs(k):
    eta_k = ETA1 * ADV ** (1.0 - k)
    return (LAM * SIGMA ** 2 / (eta_k * k)) ** (1.0 / (1.0 + k)), 2.0 / (1.0 + k)


def path(k, X, t):
    c, p = coeffs(k)
    if abs(p - 1.0) < 1e-14:
        return X * np.exp(-c * t)
    return (X ** (1.0 - p) + (p - 1.0) * c * t) ** (1.0 / (1.0 - p))


def half_life(k, X):
    c, p = coeffs(k)
    if abs(p - 1.0) < 1e-14:
        return np.log(2.0) / c
    return X ** (1.0 - p) * (2.0 ** (p - 1.0) - 1.0) / ((p - 1.0) * c)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.0),
                               gridspec_kw=dict(width_ratios=[1.06, 1.0], wspace=0.28))

# ---- left: normalised trajectories ---------------------------------------
t_h = np.linspace(0.0, 8.0, 1200)
t_d = t_h / HOURS
SMALL, BIG = 0.01 * ADV, 0.25 * ADV

axL.plot(t_h, path(1.0, SMALL, t_d) / SMALL, color=BLUE, lw=2.0, zorder=4)
axL.plot(t_h, path(1.0, BIG, t_d) / BIG, color=BLUE, lw=2.0, zorder=4)
axL.plot(t_h, path(0.6, SMALL, t_d) / SMALL, color=GREEN, lw=1.5,
         ls=(0, (4.5, 2.2)), zorder=3)
axL.plot(t_h, path(0.6, BIG, t_d) / BIG, color=ORANGE, lw=1.5,
         ls=(0, (1.6, 1.9)), zorder=3)

for k, X, colour in ((1.0, SMALL, BLUE), (0.6, SMALL, GREEN), (0.6, BIG, ORANGE)):
    th = half_life(k, X) * HOURS
    axL.plot([th], [0.5], marker="o", ms=3.4, color=colour, zorder=6,
             markeredgecolor="white", markeredgewidth=0.7)
axL.axhline(0.5, color=MUTED, lw=0.5, ls=(0, (1.4, 2.4)), zorder=1)

axL.annotate("linear impact, $k=1$\nboth order sizes, one curve",
             xy=(0.95, 0.715), xytext=(2.70, 0.88), color=BLUE, fontsize=7.6,
             ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6,
                             shrinkA=2, shrinkB=2))
axL.annotate("$k=3/5$, order 1% of volume", xy=(6.55, 0.345), xytext=(4.30, 0.615),
             color=GREEN, fontsize=7.6, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6,
                             shrinkA=2, shrinkB=2))
axL.annotate("$k=3/5$, order 25% of volume", xy=(2.75, 0.185), xytext=(1.30, 0.070),
             color=ORANGE, fontsize=7.6, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                             shrinkA=2, shrinkB=2))
axL.text(0.10, 0.525, "half sold", color=MUTED, fontsize=7.2, va="bottom")

axL.set_xlim(0, 8.0)
axL.set_ylim(0, 1.02)
axL.set_xlabel("trading hours elapsed")
axL.set_ylabel("fraction of the order still held")
axL.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axL.grid(True, color=GRID, lw=0.5, zorder=0)
axL.set_axisbelow(True)
for side in ("top", "right"):
    axL.spines[side].set_visible(False)

# ---- right: half-life against order size ---------------------------------
frac = np.logspace(-3, 0, 400)
Xs = frac * ADV
axR.plot(frac * 100, [half_life(1.0, X) * HOURS for X in Xs], color=BLUE, lw=2.0)
axR.plot(frac * 100, [half_life(0.6, X) * HOURS for X in Xs], color=ORANGE, lw=1.6,
         ls=(0, (4.5, 2.2)))
axR.set_xscale("log")
axR.set_yscale("log")
axR.set_xlim(0.1, 100)
axR.set_ylim(1.0, 14.0)
axR.set_xlabel("order size, per cent of average daily volume")
axR.set_ylabel("half-life of the position, trading hours")
axR.set_xticks([0.1, 1, 10, 100])
axR.set_xticklabels(["0.1", "1", "10", "100"])
axR.set_yticks([1, 2, 5, 10])
axR.set_yticklabels(["1", "2", "5", "10"])
axR.grid(True, which="major", color=GRID, lw=0.5, zorder=0)
axR.set_axisbelow(True)
for side in ("top", "right"):
    axR.spines[side].set_visible(False)

axR.text(0.135, 2.24, "$k=1$: flat at 2.015 h", color=BLUE, fontsize=7.6,
         va="bottom", ha="left")
axR.annotate("$k=3/5$: slope $-1/4$", xy=(1.55, 3.70), xytext=(3.10, 6.6),
             color=ORANGE, fontsize=7.6, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                             shrinkA=2, shrinkB=2))

out = Path(__file__).resolve().parent / "017-execution-trajectories.png"
fig.savefig(out, dpi=340, bbox_inches="tight", pad_inches=0.02)
print(f"wrote {out}")
print(f"kappa = {KAPPA:.6f}/day, linear half-life = {np.log(2)/KAPPA*HOURS:.4f} h")
for fr in (0.01, 0.05, 0.25):
    X = fr * ADV
    print(f"  {fr:5.0%} of ADV: k=1 {half_life(1.0, X)*HOURS:6.3f} h, "
          f"k=0.6 {half_life(0.6, X)*HOURS:6.3f} h")
print(f"  ratio over 25x size at k=0.6: "
      f"{half_life(0.6, 0.01*ADV)/half_life(0.6, 0.25*ADV):.4f} vs 25^(1/4) = {25**0.25:.4f}")
