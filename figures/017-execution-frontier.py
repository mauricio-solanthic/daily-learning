"""Figure for report 017 — the trade-off between haste and risk, drawn twice.

Both panels use the worked example of Almgren and Chriss (2001): a one-million
share position in a 50-dollar stock whose average daily volume is five million
shares, liquidated over five trading days in daily slices.

    sigma   = 0.95 $/share/day^(1/2)   (30 per cent a year on a 50-dollar stock)
    epsilon = 1/16 $/share             (half the bid-ask spread)
    gamma   = 2.5e-7 $/share per share (permanent; 10 per cent of ADV = one spread)
    eta     = 2.5e-6 $/share per share (temporary;  1 per cent of ADV = one spread)
    eta_t   = eta - gamma*tau/2 = 2.375e-6

Left panel — the optimal holding trajectory

    x(t) = X * sinh(kappa (T - t)) / sinh(kappa T),

for four risk aversions plus the risk-neutral limit, which is the straight line
(TWAP). kappa comes from the discrete-time relation

    cosh(kappa tau) = 1 + (tau^2/2) * lambda sigma^2 / eta_t,

so kappa = 0.195, 0.433, 0.846 and 1.727 per day for lambda = 1e-7, 5e-7, 2e-6
and 1e-5. Curves are labelled by trading half-life ln2/kappa, which is the one
number a trader actually feels.

Right panel — the same five strategies as points in cost-risk space, on the
frontier traced by sweeping lambda continuously. Expected cost and cost standard
deviation are both expressed in basis points of the 50-million-dollar position:

    E = gamma X^2/2 + epsilon * sum|n_k| + (eta_t/tau) * sum n_k^2
    V = sigma^2 * tau * sum x_k^2      (k = 1..N)

The permanent-impact term gamma X^2 / 2 = 125,000 dollars, 25 bp, is identical
for every point on the curve; it is drawn as the floor the frontier cannot go
below, which is the panel's whole argument.

Palette: the blue / orange / green trio used in reports 009-016, direct-labelled
rather than legended, as this is print.
Run: python3 figures/017-execution-frontier.py
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

# ---- the Almgren-Chriss worked example -----------------------------------
S0, X, T, N = 50.0, 1.0e6, 5.0, 5
TAU = T / N
SIGMA, EPS, GAMMA, ETA = 0.95, 1.0 / 16.0, 2.5e-7, 2.5e-6
ETA_T = ETA - 0.5 * GAMMA * TAU
NOTIONAL = S0 * X
PERM = 0.5 * GAMMA * X ** 2


def kappa_of(lam):
    if lam <= 0.0:
        return 0.0
    return np.arccosh(1.0 + 0.5 * TAU ** 2 * lam * SIGMA ** 2 / ETA_T) / TAU


def holdings(kap, t):
    if kap == 0.0:
        return X * (1.0 - t / T)
    return X * np.sinh(kap * (T - t)) / np.sinh(kap * T)


def cost_and_risk(kap):
    x = holdings(kap, np.arange(N + 1) * TAU)
    n = -np.diff(x)
    exp_cost = PERM + EPS * np.sum(np.abs(n)) + (ETA_T / TAU) * np.sum(n ** 2)
    var = SIGMA ** 2 * TAU * np.sum(x[1:] ** 2)
    return exp_cost / NOTIONAL * 1e4, np.sqrt(var) / NOTIONAL * 1e4


fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.0, 1.1],
                                                wspace=0.29))

# ---- left: trajectories --------------------------------------------------
CASES = [(0.0, MUTED, 0.90, (5, 6), "left", "risk-neutral (TWAP)", 1.4),
         (1e-7, BLUE, 3.05, (6, 7), "left", "half-life 3.56 d", 1.5),
         (5e-7, GREEN, 2.30, (-6, -12), "right", "1.60 d", 1.5),
         (2e-6, ORANGE, 2.60, (6, 4), "left", "0.82 d", 1.8),
         (1e-5, INK, 0.90, (-5, -12), "right", "0.40 d", 1.5)]
grid = np.linspace(0.0, T, 400)
for lam, colour, anchor, off, ha, label, lw in CASES:
    kap = kappa_of(lam)
    axL.plot(grid, holdings(kap, grid) / X, color=colour, lw=lw, zorder=3)
    axL.annotate(label, xy=(anchor, holdings(kap, anchor) / X), xytext=off,
                 textcoords="offset points", color=colour, fontsize=7.4,
                 ha=ha, va="bottom")

axL.set_xlim(0, T)
axL.set_ylim(0, 1.03)
axL.set_xlabel("trading days elapsed")
axL.set_ylabel("fraction of the position still held")
axL.set_xticks([0, 1, 2, 3, 4, 5])
axL.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axL.set_title("Trading half-life sets the whole schedule", fontsize=8.6,
              color=INK, pad=6, loc="left")
for side in ("top", "right"):
    axL.spines[side].set_visible(False)

# ---- right: the efficient frontier ---------------------------------------
lams = np.concatenate([[0.0], np.logspace(-8.4, -3.4, 500)])
pts = np.array([cost_and_risk(kappa_of(l)) for l in lams])
axR.plot(pts[:, 1], pts[:, 0], color=BLUE, lw=1.9, zorder=3)

floor_bp = PERM / NOTIONAL * 1e4
axR.axhline(floor_bp, color=MUTED, lw=1.0, ls=(0, (2.4, 2.2)), zorder=2)
axR.text(214, floor_bp + 5, "permanent impact, 25 bp — the same for every\n"
                            "strategy on the curve, and unavoidable",
         color=MUTED, fontsize=7.3, ha="right", va="bottom", linespacing=1.25)

MARKS = [(0.0, MUTED, "TWAP", (-6, 9), "right"),
         (5e-7, GREEN, "half-life 1.60 d", (-8, -11), "right"),
         (2e-6, ORANGE, "0.82 d", (10, 2), "left"),
         (1e-5, INK, "0.40 d", (11, 0), "left")]
for lam, colour, label, off, ha in MARKS:
    e, s = cost_and_risk(kappa_of(lam))
    axR.plot([s], [e], marker="o", ms=4.2, color=colour, zorder=5,
             markeredgecolor="white", markeredgewidth=0.8)
    axR.annotate(label, xy=(s, e), xytext=off, textcoords="offset points",
                 color=colour, fontsize=7.4, ha=ha, va="center")

axR.set_xlim(0, 225)
axR.set_ylim(0, 400)
axR.set_xlabel("standard deviation of realised cost (bp)")
axR.set_ylabel("expected cost (bp)")
axR.set_title("Every point is optimal for somebody", fontsize=8.6,
              color=INK, pad=6, loc="left")
for side in ("top", "right"):
    axR.spines[side].set_visible(False)
axR.grid(axis="y", color=GRID, lw=0.6, zorder=0)
axR.set_axisbelow(True)

out = Path(__file__).resolve().parent / "017-execution-frontier.png"
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.03)
print(f"wrote {out}")
for lam, *_ in CASES:
    e, s = cost_and_risk(kappa_of(lam))
    print(f"  lambda={lam:9.1e}  kappa={kappa_of(lam):6.3f}  E={e:7.1f} bp  sd={s:7.1f} bp")
