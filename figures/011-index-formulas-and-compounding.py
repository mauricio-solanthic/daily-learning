"""Figure for report 011 — what the formula choice costs.

Left panel: a symmetric two-good CES economy, base prices (1, 1) and equal
expenditure shares, in which one price doubles to (2, 1). Utility is held
constant, so the quantities are compensated (Hicksian) and the Konues true
cost-of-living index is exactly the ratio of unit cost functions,
c(2,1)/c(1,1). Plotted against the elasticity of substitution: the Laspeyres
index (flat at 1.500 by construction — it never moves, because it never lets
the basket move), the Paasche index, the Fisher index as their geometric mean,
and the true index. Laspeyres brackets the truth from above and Paasche from
below for every elasticity; Fisher sits between them and tracks the truth
closely near unit elasticity, where it is exact, and drifts once substitution
gets extreme. That drift is the honest limit of a superlative index: a
second-order approximation, not an identity.

Right panel: why a fraction of a point is worth a congressional commission.
A benefit or a tax bracket indexed to an index that runs b percentage points a
year too fast diverges from the truth as (1+b)^t. Three values of b: 0.25
points, CBO's expected gap between the traditional and the chained CPI; 0.7
points, roughly the residual bias the Boskin members still saw in 1999 after
the geometric-mean change; and 1.1 points, the commission's own 1996 estimate.

Sources for the annotated values: Boskin Commission via GAO/GGD-00-50 (1.10);
CBO, Differences Between the Traditional CPI and the Chained CPI (0.25);
index-number identities computed here. Palette: the same three dataviz
categorical slots used in figures 009 and 010, with ink for the true index so
the reference curve reads as the reference.
Run: python3 figures/011-index-formulas-and-compounding.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, RULE = "#0b0b0b", "#52514e", "#e6e6e2"

plt.rcParams.update({
    "font.family": "serif", "font.serif": [SERIF], "font.size": 8.2,
    "mathtext.fontset": "custom", "mathtext.rm": SERIF,
    "mathtext.it": f"{SERIF}:italic", "mathtext.bf": f"{SERIF}:bold",
    "axes.edgecolor": "#c9c9c4", "axes.linewidth": 0.6,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.facecolor": "white",
    "savefig.facecolor": "white",
})

P0, P1 = (1.0, 1.0), (2.0, 1.0)


def unit_cost(p, sig):
    if abs(sig - 1.0) < 1e-9:
        return (p[0] ** 0.5) * (p[1] ** 0.5)
    return (0.5 * p[0] ** (1 - sig) + 0.5 * p[1] ** (1 - sig)) ** (1 / (1 - sig))


def hicksian(p, sig):
    """Shephard's lemma on the CES unit cost function, at utility one."""
    c = unit_cost(p, sig)
    if abs(sig - 1.0) < 1e-9:
        return [0.5 * c / p[0], 0.5 * c / p[1]]
    return [0.5 * p[i] ** (-sig) * c ** sig for i in (0, 1)]


def indexes(sig):
    q0, q1 = hicksian(P0, sig), hicksian(P1, sig)
    lasp = sum(P1[i] * q0[i] for i in (0, 1)) / sum(P0[i] * q0[i] for i in (0, 1))
    paas = sum(P1[i] * q1[i] for i in (0, 1)) / sum(P0[i] * q1[i] for i in (0, 1))
    return lasp, paas, (lasp * paas) ** 0.5, unit_cost(P1, sig) / unit_cost(P0, sig)


sig = np.linspace(0.0, 5.0, 401)
L, P, F, K = (np.array(v) for v in zip(*(indexes(s) for s in sig)))

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.15),
                               gridspec_kw=dict(width_ratios=[1.06, 1.0],
                                                wspace=0.34))

# ---- left: four answers to one price change -------------------------------
axL.fill_between(sig, P, L, color=AQUA, alpha=0.10, zorder=1)
axL.plot(sig, L, color=ORANGE, lw=1.6, zorder=4)
axL.plot(sig, P, color=BLUE, lw=1.6, zorder=4)
axL.plot(sig, F, color=AQUA, lw=1.6, zorder=5)
axL.plot(sig, K, color=INK, lw=1.3, ls=(0, (3.2, 1.9)), zorder=6)
axL.plot([1.0], [2 ** 0.5], "o", ms=4.6, color=INK, zorder=7)

axL.text(3.55, 1.512, "Laspeyres", color=ORANGE, fontsize=7.8, va="bottom")
axL.text(2.00, 1.090, "Paasche", color=BLUE, fontsize=7.8,
         va="top", ha="left")
axL.text(2.55, 1.325, "Fisher", color=AQUA, fontsize=7.8,
         va="bottom", ha="left")
axL.text(3.90, 1.158, "true index", color=INK, fontsize=7.8,
         va="top", ha="left")
axL.annotate("Fisher is exact here", xy=(1.0, 2 ** 0.5),
             xytext=(1.34, 1.462), fontsize=7.0, color=MUTED,
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=0, shrinkB=3))
axL.set_xlim(0, 5)
axL.set_ylim(1.0, 1.56)
axL.set_xticks([0, 1, 2, 3, 4, 5])
axL.set_yticks([1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
axL.set_xlabel("elasticity of substitution between the two goods")
axL.set_ylabel("index, base period = 1")
axL.set_title("One price doubles: four answers", fontsize=9.0, loc="left",
              pad=8, color=INK)
axL.grid(color=RULE, lw=0.6, zorder=0)
for s in ("top", "right"):
    axL.spines[s].set_visible(False)

# ---- right: a fraction of a point, compounded -----------------------------
yrs = np.arange(0, 31)
tracks = [(0.011, ORANGE, "1.10 points\nBoskin, 1996"),
          (0.007, AQUA, "0.70 points\nresidual, 1999"),
          (0.0025, BLUE, "0.25 points\nchained-CPI gap")]
for b, colour, label in tracks:
    gap = ((1 + b) ** yrs - 1) * 100
    axR.plot(yrs, gap, color=colour, lw=1.6, zorder=4)
    axR.text(30.4, gap[-1], label, color=colour, fontsize=7.4,
             va="center", ha="left", linespacing=1.35)
    axR.plot([30], [gap[-1]], "o", ms=4.0, color=colour, zorder=5)
axR.set_xlim(0, 30)
axR.set_ylim(0, 42)
axR.set_xticks([0, 10, 20, 30])
axR.set_yticks([0, 10, 20, 30, 40], ["0", "10%", "20%", "30%", "40%"])
axR.set_xlabel("years of indexation")
axR.set_title("A fraction of a point, compounded", fontsize=9.0, loc="left",
              pad=8, color=INK)
axR.grid(color=RULE, lw=0.6, zorder=0)
for s in ("top", "right"):
    axR.spines[s].set_visible(False)

fig.subplots_adjust(left=0.083, right=0.845, top=0.855, bottom=0.155)
out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300)
print(f"wrote {out}")

for s in (0.0, 0.5, 1.0, 2.0, 5.0):
    l, p, f, k = indexes(s)
    print(f"sigma={s:4.1f}  L={l:.4f}  P={p:.4f}  Fisher={f:.4f}  true={k:.4f}")
for b in (0.0025, 0.007, 0.011):
    print(f"bias {b*100:.2f} pp/yr -> 10 yr {(1+b)**10-1:.3%}, "
          f"30 yr {(1+b)**30-1:.3%}")
