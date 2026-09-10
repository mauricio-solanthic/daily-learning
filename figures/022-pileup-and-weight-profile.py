"""Figure for report 022 — the two arithmetic facts behind a filtered r-star.

Both panels are computed from the canonical signal-extraction problem, a random
walk observed with additive noise:

    x_t = x_{t-1} + eta_t,   var(eta) = q * s2 ;   y_t = x_t + eps_t, var(eps) = s2

with q the signal-to-noise ratio. HLW's reported lambda_z = 0.040 is a ratio of
standard deviations, so q = lambda^2 = 0.0016; Buncic's corrected estimate of
0.013 gives q = 0.000169.

Left panel: the pile-up problem. 20,000 samples of 250 quarters are simulated at
the true value lambda = 0.040 (HLW's own estimate, on roughly HLW's own sample
length) and the signal-to-noise ratio is re-estimated by maximum likelihood on
each. A seventh of the samples return exactly zero — no time variation at all —
and the median estimate sits below the truth. The bar at zero is drawn detached
because it is an atom of probability, not a bin.

Right panel: the weight profile. In steady state the real-time estimate is an
exponentially weighted moving average of past observations with smoothing
parameter equal to the Kalman gain K, so the weight on the observation j
quarters back is K(1-K)^j. The mean lag is (1-K)/K exactly: 24.5 quarters at
lambda = 0.040 and 76.4 at 0.013. Those centres of mass are marked.

Palette: the blue/orange pair already validated for this series (reports 009-021),
all-pairs checked at print contrast.
Run: python3 figures/022-pileup-and-weight-profile.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import tempfile
from math import log, sqrt
from pathlib import Path

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE = "#2a78d6", "#eb6834"
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


# ---------------------------------------------------------------- mechanics
def steady_gain(q):
    """Steady-state Kalman gain: p^2 - q p - q = 0, K = p / (p + 1)."""
    p = (q + sqrt(q * q + 4.0 * q)) / 2.0
    return p / (p + 1.0)


def kf_sequences(q, T):
    """Deterministic F and K sequences, diffuse start at y_1, var(eps) = 1."""
    F = np.empty(T - 1)
    K = np.empty(T - 1)
    P = 1.0 + q
    for t in range(T - 1):
        f = P + 1.0
        F[t] = f
        k = P / f
        K[t] = k
        P = P * (1.0 - k) + q
    return F, K


def concentrated_loglik(Y, q, cache={}):
    """Concentrated log-likelihood of every row of Y at this q."""
    R, T = Y.shape
    if (q, T) not in cache:
        cache[(q, T)] = kf_sequences(q, T)
    F, K = cache[(q, T)]
    a = Y[:, 0].copy()
    ssq = np.zeros(R)
    for t in range(1, T):
        v = Y[:, t] - a
        ssq += v * v / F[t - 1]
        a = a + K[t - 1] * v
    n = T - 1
    return -0.5 * n * np.log(ssq / n) - 0.5 * np.sum(np.log(F))


T, LAM_TRUE, REPS = 250, 0.040, 20000
Q_TRUE = LAM_TRUE ** 2
Q_GRID = np.concatenate(([0.0], np.exp(np.linspace(log(1e-6), log(5.0), 300))))

rng = np.random.default_rng(20260910)
X = np.cumsum(rng.normal(0.0, sqrt(Q_TRUE), (REPS, T)), axis=1)
Y = X + rng.normal(0.0, 1.0, (REPS, T))
LL = np.empty((len(Q_GRID), REPS))
for i, q in enumerate(Q_GRID):
    LL[i] = concentrated_loglik(Y, q)
qhat = Q_GRID[np.argmax(LL, axis=0)]
lamhat = np.sqrt(qhat)

frac_zero = float(np.mean(qhat == 0.0))
lam_median = float(np.median(lamhat))
assert 0.10 < frac_zero < 0.18, frac_zero
assert lam_median < LAM_TRUE

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.06, 1.0],
                                                wspace=0.30))

# ---- left: the pile-up ----------------------------------------------------
TOP = 0.13
positive = lamhat[qhat > 0.0]
bins = np.linspace(0.0, TOP, 40)
axL.hist(np.clip(positive, 0.0, TOP - 1e-6), bins=bins,
         weights=np.full(positive.size, 100.0 / REPS),
         color=BLUE, alpha=0.80, zorder=3)
axL.bar([-0.0075], [frac_zero * 100.0], width=0.0095, color=ORANGE,
        zorder=4, align="center")
axL.axvline(LAM_TRUE, color=INK, lw=0.9, ls=(0, (3, 2.2)), zorder=5)
axL.set_xlim(-0.0155, TOP)
axL.set_ylim(0, max(15.5, frac_zero * 100.0 + 2.0))
axL.set_xticks([0.0, 0.04, 0.08, 0.12])
axL.set_xlabel("re-estimated signal-to-noise ratio  $\\hat{\\lambda}$")
axL.set_ylabel("per cent of samples")
axL.set_title("Estimating how much a trend moves", fontsize=9.0, loc="left",
              pad=8, color=INK)
axL.annotate(f"exactly zero\nin {frac_zero * 100:.0f} per cent\nof samples",
             xy=(-0.0075, frac_zero * 100.0), xytext=(0.0555, 12.5),
             fontsize=7.4, color=ORANGE, ha="left", va="top",
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                             shrinkA=3, shrinkB=5))
axL.text(0.0425, max(15.5, frac_zero * 100.0 + 2.0) - 0.9,
         "true value 0.040", fontsize=7.4, color=INK, ha="left", va="top")
axL.grid(color=GRID, lw=0.6, axis="y", zorder=0)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: the weight profile ------------------------------------------
j = np.arange(0, 121)
for lam, colour, label, lxy in ((0.040, BLUE, "$\\lambda = 0.040$", (4.0, 4.06)),
                                (0.013, ORANGE, "$\\lambda = 0.013$", (7.0, 0.50))):
    K = steady_gain(lam ** 2)
    w = K * (1.0 - K) ** j * 100.0
    lag = (1.0 - K) / K
    axR.plot(j, w, color=colour, lw=1.7, zorder=3)
    axR.plot([lag], [K * (1.0 - K) ** lag * 100.0], "o", ms=3.6,
             color=colour, zorder=4)
    axR.annotate(f"mean lag {lag:.1f} quarters", xy=(lag, K * (1.0 - K) ** lag * 100.0),
                 xytext=(lag + 9.5, K * (1.0 - K) ** lag * 100.0 + 1.06),
                 fontsize=7.4, color=colour, ha="left",
                 arrowprops=dict(arrowstyle="-", color=colour, lw=0.6,
                                 shrinkA=3, shrinkB=3))
    axR.text(lxy[0], lxy[1], label, color=colour, fontsize=8.2,
             ha="left", va="bottom")
axR.set_xlim(0, 120)
axR.set_ylim(0, 4.6)
axR.set_xticks([0, 30, 60, 90, 120])
axR.set_xlabel("quarters before the estimate's own date")
axR.set_ylabel("weight on that quarter, per cent")
axR.set_title("What a real-time estimate is averaging", fontsize=9.0,
              loc="left", pad=8, color=INK)
axR.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
print(f"  P(lambda_hat == 0) = {frac_zero * 100:.2f}%   median lambda_hat = {lam_median:.4f}")
for lam in (0.040, 0.013):
    K = steady_gain(lam ** 2)
    print(f"  lambda={lam:.3f}: K={K:.5f}, mean lag={(1 - K) / K:.2f} q, "
          f"half-life={log(0.5) / log(1 - K):.2f} q")
