"""Figure for report 021 — what half a kilogram of niobium buys, and how
concentrated the supply of it is.

Left panel — the grain-boundary strengthening available from refining ferrite,
against the grain size a given niobium addition can actually hold. The curve is
the Hall-Petch increment k*d^(-1/2) with k = 0.550 MPa m^(1/2), which is
Pickering's 17.4 MPa mm^(1/2) converted; the independently quoted 600 MPa
um^(1/2) gives 0.600 and is drawn as the upper edge of the band, so the band is
the disagreement between two reported forms of the same constant.

The vertical markers are the Smith-Zener limiting grain size D = 4r/3f for
carbide particles of radius 2.5 nm, evaluated at three niobium additions. The
volume fraction f is computed, not assumed: 0.05 weight per cent niobium taken
entirely to NbC is 0.0565 weight per cent carbide, which at 7.82 against
7.87 g/cm3 is 5.68 parts in ten thousand by volume. So f scales linearly with
the addition and D scales inversely — 0.01 per cent niobium holds 29 um, 0.05
per cent holds 5.9 um, and the strengthening that buys is about 105 MPa.

Right panel — leading-producer share of world mine production for four
commodities whose concentration is routinely called a strategic problem, plus
niobium, which is more concentrated than any of them. The inner segment on the
niobium bar is the share attributed to a single company; the whisker spans the
75-80 per cent range reported for it.

Chart form chosen before coding: the left panel is one continuous function of a
continuous variable with three discrete cases marked on it, which is a line
with rules, not bars; the right panel is a ranked part-of-whole comparison
across named categories, which is a horizontal bar. Print figure — direct
labels, no legend, no interaction, no dark mode.

Palette: the blue / orange / green trio used in reports 009-020.
Run: python3 figures/021-leverage-and-concentration.py
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

# --- the arithmetic --------------------------------------------------------
M_NB, M_C, M_FE = 92.90637, 12.011, 55.845
RHO_NBC, RHO_FE = 7.82, 7.87
K_LO = 17.4 * (1e-3) ** 0.5          # MPa mm^1/2  -> MPa m^1/2   (0.5502)
K_HI = 600.0 * (1e-6) ** 0.5         # MPa um^1/2  -> MPa m^1/2   (0.6000)
R_PART = 2.5e-9                      # strain-induced carbide radius, m


def carbide_volume_fraction(nb_wt_pct):
    """Volume fraction of NbC if all the niobium precipitates as carbide."""
    w_nb = nb_wt_pct / 100.0
    w_nbc = w_nb * (M_NB + M_C) / M_NB
    return (w_nbc / RHO_NBC) / ((w_nbc / RHO_NBC) + ((1.0 - w_nbc) / RHO_FE))


def zener_limit_um(nb_wt_pct, r=R_PART):
    """Smith-Zener limiting grain size, micrometres."""
    return 4.0 * r / (3.0 * carbide_volume_fraction(nb_wt_pct)) * 1e6


fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.1, 3.4),
                             gridspec_kw={"width_ratios": [1.24, 1.0]})

# --- left: what the grain refinement is worth ------------------------------
d = np.logspace(np.log10(2.2), np.log10(60.0), 400)          # micrometres
ax.fill_between(d, K_LO / np.sqrt(d * 1e-6), K_HI / np.sqrt(d * 1e-6),
                color=BLUE, alpha=0.16, linewidth=0, zorder=2)
ax.plot(d, K_LO / np.sqrt(d * 1e-6), color=BLUE, lw=1.7, zorder=4)

CASES = [(0.01, "0.01 %", (33.5, 168)), (0.03, "0.03 %", (10.9, 200)),
         (0.05, "0.05 %", (6.7, 252))]
for nb, lab, (tx, ty) in CASES:
    dl = zener_limit_um(nb)
    s = K_LO / np.sqrt(dl * 1e-6)
    ax.plot([dl, dl], [0, s], color=ORANGE, lw=0.9, ls=(0, (3, 2)), zorder=3)
    ax.plot([dl], [s], "o", ms=4.0, color=ORANGE, mec="white", mew=0.7, zorder=6)
    ax.annotate(f"{lab} Nb\n{dl:.1f} $\\mu$m, {s:.0f} MPa",
                xy=(dl, s), xytext=(tx, ty),
                fontsize=7.0, color=INK, linespacing=1.35, zorder=7,
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.5,
                                shrinkA=1.0, shrinkB=3.0))

d_plain = 20.0
s_plain = K_LO / np.sqrt(d_plain * 1e-6)
ax.plot([d_plain], [s_plain], "s", ms=4.2, color=MUTED, mec="white", mew=0.7,
        zorder=6)
ax.annotate("no microalloying\n20 $\\mu$m, 123 MPa",
            xy=(d_plain, s_plain), xytext=(5.6, 66),
            fontsize=7.0, color=MUTED, ha="left", va="top", linespacing=1.35,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5), zorder=7)

ax.set_xscale("log")
ax.set_xlim(2.2, 62)
ax.set_ylim(0, 420)
ax.set_xticks([2.5, 5, 10, 20, 40])
ax.set_xticklabels(["2.5", "5", "10", "20", "40"])
ax.set_xticks([], minor=True)
ax.set_xlabel("ferrite grain size $d$, micrometres")
ax.set_ylabel("grain-boundary strengthening $k\\,d^{-1/2}$, MPa")
ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_title("Half a kilogram, and where it goes", fontsize=9.0, color=INK,
             loc="left", pad=7)

# --- right: leading-producer share -----------------------------------------
ROWS = [("Niobium\nBrazil", 4.35, 92.9, 0.50, BLUE, 1.00),
        ("of which one\nprivate company", 3.62, 77.5, 0.30, ORANGE, 1.00),
        ("Cobalt\nDR Congo", 2.45, 73.0, 0.50, MUTED, 0.42),
        ("Platinum\nSouth Africa", 1.35, 70.0, 0.50, MUTED, 0.42),
        ("Rare earths\nChina", 0.25, 69.2, 0.50, MUTED, 0.42)]

for lab, y, share, h, col, a in ROWS:
    bx.barh(y, share, height=h, color=col, alpha=a, edgecolor="white",
            linewidth=0.7, zorder=3)
    txt = f"{share:.0f} %" if col is not ORANGE else "75 to 80 %"
    bx.text(share + 1.8 if col is not ORANGE else 81.5, y, txt,
            ha="left", va="center", fontsize=8.4 if col is not ORANGE else 7.4,
            color=INK if col is not ORANGE else ORANGE, zorder=5)

# the reported range for the single company, drawn on its own bar
bx.plot([75.0, 80.0], [ROWS[1][1]] * 2, color=ORANGE, lw=1.0, zorder=5)
for x in (75.0, 80.0):
    bx.plot([x, x], [ROWS[1][1] - 0.11, ROWS[1][1] + 0.11], color=ORANGE,
            lw=1.0, zorder=5)

bx.set_yticks([r[1] for r in ROWS])
bx.set_yticklabels([r[0] for r in ROWS], fontsize=7.6, linespacing=1.4)
for tick, (_, _, _, _, col, _) in zip(bx.get_yticklabels(), ROWS):
    if col is ORANGE:
        tick.set_color(ORANGE)
        tick.set_fontsize(7.0)
bx.set_ylim(-0.45, 4.95)
bx.set_xlim(0, 104)
bx.set_xticks([0, 25, 50, 75, 100])
bx.set_xlabel("share of world mine output, per cent")
bx.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
bx.set_axisbelow(True)
for s in ("top", "right", "left"):
    bx.spines[s].set_visible(False)
bx.tick_params(axis="y", length=0)
bx.set_title("The concentration nobody legislates about", fontsize=9.0,
             color=INK, loc="left", pad=7)

fig.tight_layout(pad=0.9)
out = Path(__file__).resolve().parent / "021-leverage-and-concentration.png"
fig.savefig(out, dpi=300)
print(f"wrote {out}")
print(f"  k: {K_LO:.4f} and {K_HI:.4f} MPa m^1/2 "
      f"(differ by {100 * (K_HI - K_LO) / K_LO:.1f}%)")
print(f"  f(0.05 wt% Nb as NbC) = {carbide_volume_fraction(0.05):.4e}")
for nb, _, _ in CASES:
    dl = zener_limit_um(nb)
    print(f"  Nb {nb:.2f} wt%: f = {carbide_volume_fraction(nb):.3e}, "
          f"D_lim = {dl:5.1f} um, k d^-1/2 = {K_LO / (dl * 1e-6) ** 0.5:5.0f} MPa")
print(f"  plain 20 um: {s_plain:.0f} MPa; gain to 0.05% case "
      f"{K_LO / (zener_limit_um(0.05) * 1e-6) ** 0.5 - s_plain:.0f} MPa")
