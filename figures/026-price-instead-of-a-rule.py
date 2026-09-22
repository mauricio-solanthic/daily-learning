"""Figure for report 026 — what a Lagrangian dual function looks like, and what
climbing one actually feels like.

Both panels use the same six-job, three-line assignment instance given in the
report. Its exact integer optimum is 104, found by enumerating all 729
assignments; its linear-programming relaxation is 93.2.

Left panel — the dual function obtained by pricing one constraint only: line
A's 28 hours of capacity. Every assignment that respects lines B and C
contributes an affine function of the price mu, with intercept equal to its
cost and slope equal to the hours it puts on line A minus 28. The dual function
is the lower envelope of those 326 lines, which makes it concave and piecewise
linear whatever the problem underneath. Only three pieces are ever active on
[0, 4]. The maximum sits at mu = 10/27 where two pieces cross, slope +10 to the
left and -17 to the right: the best bound is at a corner, and the derivative
there does not exist.

Right panel — 200 iterations of subgradient ascent on the harder dual, the one
that prices the six requirement constraints instead and leaves three knapsacks
behind. The exact value of that dual is 102, computed independently by linear
programming over the 86 feasible job-subsets. Prices start at each job's
cheapest cost, which makes every reduced cost non-negative, empties all three
knapsacks and returns the bound 92. The iterates are not monotone: 60 of the
199 steps lower the bound, which is why the usable answer is the running
maximum and not the last value.

Palette: the blue/orange/green set already validated for this series (009-025),
all-pairs checked at print contrast. Series are labelled directly; this is print.
Run: python3 figures/026-price-instead-of-a-rule.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import itertools
import tempfile
from fractions import Fraction
from pathlib import Path

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

# ------------------------------------------------------------- the instance
HOURS = np.array([[4, 8, 17, 11, 16, 5],
                  [6, 18, 8, 19, 8, 4],
                  [4, 10, 4, 20, 5, 8]], dtype=float)
COST = np.array([[21, 19, 20, 26, 22, 20],
                 [12, 9, 30, 28, 22, 24],
                 [18, 20, 23, 14, 17, 20]], dtype=float)
CAP = np.array([28, 29, 23], dtype=float)
M, N = COST.shape
Z_IP, Z_LP, Z_LD = 104.0, 93.2, 102.0


def enumerate_all():
    """Every assignment, with its cost and its per-line hours."""
    rows = []
    for asg in itertools.product(range(M), repeat=N):
        load = np.zeros(M)
        cost = 0.0
        for j, i in enumerate(asg):
            load[i] += HOURS[i, j]
            cost += COST[i, j]
        rows.append((cost, load.copy(), asg))
    return rows


ALL = enumerate_all()
FEASIBLE = [r for r in ALL if np.all(r[1] <= CAP + 1e-9)]
assert len(ALL) == 729 and len(FEASIBLE) == 183
assert min(r[0] for r in FEASIBLE) == Z_IP

# assignments respecting lines B and C, with line A priced instead
RELAXED = np.array([[cost, load[0]] for cost, load, _ in ALL
                    if load[1] <= CAP[1] + 1e-9 and load[2] <= CAP[2] + 1e-9])
assert len(RELAXED) == 326


def dual_one_price(mu):
    """Lower envelope: min over the relaxed set of cost + mu (hoursA - 28)."""
    mu = np.atleast_1d(np.asarray(mu, dtype=float))
    vals = RELAXED[:, 0][None, :] + mu[:, None] * (RELAXED[:, 1] - CAP[0])[None, :]
    return vals.min(axis=1)


MU_STAR = Fraction(10, 27)
L_STAR = Fraction(2719, 27)
assert abs(dual_one_price(float(MU_STAR))[0] - float(L_STAR)) < 1e-9
assert abs(97 + 10 * float(MU_STAR) - float(L_STAR)) < 1e-9
assert abs(107 - 17 * float(MU_STAR) - float(L_STAR)) < 1e-9

# ------------------------------------------------- subgradient on the other dual
SUBSETS = []
for i in range(M):
    keep = []
    for mask in range(1 << N):
        s = np.array([(mask >> j) & 1 for j in range(N)], dtype=float)
        if s @ HOURS[i] <= CAP[i] + 1e-9:
            keep.append(s)
    SUBSETS.append(keep)
assert [len(s) for s in SUBSETS] == [29, 28, 29]


def dual_requirements(u):
    """Price the six requirement constraints; three knapsacks remain."""
    total = 0.0
    cover = np.zeros(N)
    for i in range(M):
        value, pick = min(((float(s @ (COST[i] - u)), s) for s in SUBSETS[i]),
                          key=lambda t: t[0])
        total += value
        cover += pick
    return total + u.sum(), cover


assert abs(dual_requirements(np.array([17., 14., 25., 26., 27., 20.]))[0] - Z_LD) < 1e-9


def ascend(iterations=200, decay=0.985):
    u = COST.min(axis=0).astype(float)   # each job priced at its cheapest line
    assert abs(dual_requirements(u)[0] - 92.0) < 1e-9
    seen, best_so_far, best = [], [], -np.inf
    for k in range(1, iterations + 1):
        value, cover = dual_requirements(u)
        g = 1.0 - cover
        best = max(best, value)
        seen.append(value)
        best_so_far.append(best)
        norm = float(g @ g)
        if norm < 1e-12:
            break
        u = u + 2.0 * (Z_IP - value) / norm * (decay ** k) * g
    return np.array(seen), np.array(best_so_far)


SEEN, BEST = ascend()
DOWN = int(np.sum(SEEN[1:] < SEEN[:-1] - 1e-9))
assert DOWN == 60 and abs(BEST[-1] - 101.9001) < 1e-3
assert abs(SEEN[0] - 92.0) < 1e-9

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.15),
                               gridspec_kw=dict(width_ratios=[1.0, 1.06],
                                                wspace=0.30))

# ---- left: the dual function is a lower envelope of straight lines --------
grid = np.linspace(0.0, 0.9, 1400)
for cost, hours in RELAXED[::2]:
    axL.plot(grid, cost + grid * (hours - CAP[0]), color="#cfd6dd", lw=0.45,
             zorder=2)
axL.plot(grid, dual_one_price(grid), color=BLUE, lw=2.0, zorder=5)
axL.plot([float(MU_STAR)], [float(L_STAR)], "o", ms=5.6, color=BLUE, zorder=6,
         markeredgecolor="white", markeredgewidth=0.7)
axL.axhline(Z_IP, color=ORANGE, lw=1.1, ls=(0, (4, 2.4)), zorder=4)

axL.text(0.885, Z_IP + 0.35, "true optimum 104", color=ORANGE, fontsize=7.6,
         ha="right", va="bottom")
axL.annotate("best bound $2719/27 = 100.70$\nat $\\mu = 10/27$",
             xy=(float(MU_STAR), float(L_STAR)), xytext=(0.455, 102.6),
             fontsize=7.5, color=INK, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7,
                             shrinkA=0, shrinkB=5))
axL.text(0.045, 98.35, "rising at 10", fontsize=7.3, color=MUTED, ha="left",
         va="bottom", rotation=14)
axL.text(0.585, 97.9, "falling at 17", fontsize=7.3, color=MUTED, ha="left",
         va="bottom", rotation=-24)
axL.text(0.035, 93.3, "each grey line is one assignment's\ncost as the price of an hour rises",
         fontsize=7.3, color=MUTED, ha="left", va="center")

axL.set_xlim(0.0, 0.9)
axL.set_ylim(91.5, 106.0)
axL.set_xlabel("price $\\mu$ charged per hour over line A's 28")
axL.set_xticks([0.0, 0.25, 0.5, 0.75])
axL.set_ylabel("bound on the cheapest schedule")
axL.set_title("The bound sits on a corner", fontsize=9.0, loc="left", pad=8,
              color=INK)
axL.grid(color=GRIDC, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: subgradient ascent, non-monotone -----------------------------
steps = np.arange(1, len(SEEN) + 1)
axR.plot(steps, SEEN, color="#8aa6c6", lw=0.8, zorder=3)
axR.plot(steps, BEST, color=BLUE, lw=1.9, zorder=5)
axR.axhline(Z_LD, color=GREEN, lw=1.1, ls=(0, (4, 2.4)), zorder=4)
axR.axhline(Z_LP, color=MUTED, lw=1.0, ls=(0, (1.6, 2.0)), zorder=4)
axR.axhline(Z_IP, color=ORANGE, lw=1.1, ls=(0, (4, 2.4)), zorder=4)

axR.text(197, Z_IP + 0.5, "true optimum 104", color=ORANGE, fontsize=7.6,
         ha="right", va="bottom")
axR.text(197, Z_LD - 0.7, "exact dual value 102", color=GREEN, fontsize=7.6,
         ha="right", va="top")
axR.text(197, Z_LP - 0.7, "linear-programming bound 93.2", color=MUTED,
         fontsize=7.6, ha="right", va="top")
axR.text(105, 98.4, "best bound so far", color=BLUE, fontsize=7.6, ha="left",
         va="top")
axR.text(88, 86.0, "value at the current prices:\n60 of 199 steps make it worse",
         color="#6f86a4", fontsize=7.3, ha="left", va="center")
axR.annotate("start: every job priced at\nits cheapest line, bound 92",
             xy=(2, 92.0), xytext=(17, 80.4), fontsize=7.3, color=MUTED,
             ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7,
                             shrinkA=0, shrinkB=3))

axR.set_xlim(0, 200)
axR.set_ylim(77.0, 107.0)
axR.set_xlabel("subgradient iteration")
axR.set_ylabel("bound on the cheapest schedule")
axR.set_title("Climbing without a gradient", fontsize=9.0, loc="left", pad=8,
              color=INK)
axR.grid(color=GRIDC, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
print(f"  assignments {len(ALL)}, feasible {len(FEASIBLE)}, relaxed-set points {len(RELAXED)}")
print(f"  z_LP {Z_LP}   z_LD(requirements) {Z_LD}   z_IP {Z_IP}")
print(f"  one-price dual: max {float(L_STAR):.6f} = {L_STAR} at mu = {MU_STAR}")
print(f"  subgradient: best {BEST[-1]:.4f} after {len(SEEN)} iterations, {DOWN} downward steps")
print(f"  LP gap {100*(Z_IP-Z_LP)/Z_IP:.2f}%, dual gap {100*(Z_IP-Z_LD)/Z_IP:.2f}%, "
      f"share of the LP gap closed {100*(Z_LD-Z_LP)/(Z_IP-Z_LP):.2f}%")
