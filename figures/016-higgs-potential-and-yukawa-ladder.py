"""Figure for report 016 — the mechanism is one potential; the couplings are nine numbers.

Left panel — the Higgs potential, calibrated to measurement rather than sketched.
Writing the tree-level potential for the real part of the neutral component as

    V(phi) = -(1/2) mu^2 phi^2 + (1/4) lambda phi^4,

the two measured quantities fix both parameters completely:

    v      = (sqrt(2) G_F)^(-1/2) = 246.22 GeV        (MuLan G_F)
    lambda = m_H^2 / (2 v^2)      = 0.12928           (m_H = 125.20 GeV)
    mu^2   = lambda v^2           = 7837.5 GeV^2

so the minimum sits at phi = 246.22 GeV and the well is 1.188e8 GeV^4 deep.
Heating the universe adds a positive thermal mass term. Keeping only its leading
piece, m_eff^2(T) = c T^2 - mu^2, and fixing c so the quadratic term vanishes at
the lattice crossover temperature T_c = 159.5 GeV gives c = mu^2 / T_c^2 = 0.308.
The four curves are T/T_c = 0, 0.6, 1 and 1.3. Note the caption's caveat: in the
Standard Model with a 125 GeV Higgs this is a smooth crossover, not the sharp
transition a bare Landau potential would suggest.

Right panel — every Standard Model fermion's coupling to that field, y = sqrt(2) m / v,
on one logarithmic axis. The mechanism does not predict a single one of them; they
span 5.5 decades from y_e = 2.9e-6 to y_t = 0.991, and the top's is one to within
a per cent. Rows separate leptons, up-type and down-type quarks; the three house
colours carry the row identity and every point is directly labelled, which is the
secondary encoding the palette validator's contrast warning requires.

Masses: PDG 2024. Light quarks MS-bar at 2 GeV, charm and bottom MS-bar at their
own scale, top from direct measurements.

Palette: the blue / orange / green trio used in reports 009-015, direct-labelled
rather than legended, as this is print.
Run: python3 figures/016-higgs-potential-and-yukawa-ladder.py
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

# ---- measured inputs -----------------------------------------------------
GF = 1.1663787e-5          # GeV^-2, MuLan
MH = 125.20                # GeV, PDG 2024
TC = 159.5                 # GeV, lattice crossover
V = (np.sqrt(2.0) * GF) ** -0.5
LAM = MH ** 2 / (2.0 * V ** 2)
MU2 = LAM * V ** 2
C_TH = MU2 / TC ** 2

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.0, 1.12],
                                                wspace=0.30))

# ---- left: the potential, warmed up --------------------------------------
phi = np.linspace(0.0, 300.0, 1400)


def potential(p, t):
    return 0.5 * (C_TH * t ** 2 - MU2) * p ** 2 + 0.25 * LAM * p ** 4


CURVES = [(0.0, BLUE, "$T = 0$"),
          (0.6, GREEN, "$0.6\\,T_c$"),
          (1.0, ORANGE, "$T_c$"),
          (1.3, MUTED, "$1.3\\,T_c$")]
for frac, colour, label in CURVES:
    lw = 1.8 if frac in (0.0, 1.0) else 1.4
    axL.plot(phi, potential(phi, frac * TC) / 1e8, color=colour, lw=lw, zorder=3)

vmin = -LAM * V ** 4 / 4.0 / 1e8
axL.plot([V], [vmin], marker="o", ms=3.6, color=BLUE, zorder=5,
         markeredgecolor="white", markeredgewidth=0.7)
axL.plot([V, V], [vmin, 0.02], color=BLUE, lw=0.6, ls=(0, (1.6, 2.0)), zorder=2)
axL.axhline(0.0, color="#9a9a94", lw=0.7, zorder=2)

axL.set_xlim(0, 300)
axL.set_ylim(-1.45, 1.45)
axL.set_xticks([0, 100, 200, 300])
axL.set_yticks([-1, 0, 1])
axL.set_xlabel("Higgs field $\\phi$  (GeV)")
axL.set_ylabel("$V(\\phi)$  ($10^{8}\\,$GeV$^{4}$)")
axL.set_title("A well that opens as the universe cools",
              fontsize=9.0, loc="left", pad=8, color=INK)
axL.text(112, 1.02, "$1.3\\,T_c$", color=MUTED, fontsize=8.0, ha="center")
axL.text(168, 0.62, "$T_c$", color=ORANGE, fontsize=8.0, ha="center")
axL.text(246, 0.16, "$0.6\\,T_c$", color=GREEN, fontsize=8.0, ha="center")
axL.text(105, -0.82, "$T = 0$", color=BLUE, fontsize=8.0, ha="center")
axL.annotate("$v = 246$ GeV", xy=(V, vmin), xytext=(166, -1.30),
             fontsize=7.8, color=MUTED, ha="center", va="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=6, shrinkB=4))
axL.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: the Yukawa ladder --------------------------------------------
ROWS = [
    ("leptons", BLUE, 2, [("$e$", 0.51099895e-3, "up"), ("$\\mu$", 0.1056583755, "up"),
                          ("$\\tau$", 1.77686, "up")]),
    ("up-type", ORANGE, 1, [("$u$", 2.16e-3, "up"), ("$c$", 1.2730, "up"),
                            ("$t$", 172.57, "down")]),
    ("down-type", GREEN, 0, [("$d$", 4.67e-3, "up"), ("$s$", 93.5e-3, "up"),
                             ("$b$", 4.183, "up")]),
]
for name, colour, row, members in ROWS:
    xs = [np.sqrt(2.0) * m / V for _, m, _ in members]
    axR.plot(xs, [row] * len(xs), ls="none", marker="o", ms=5.0, color=colour,
             markeredgecolor="white", markeredgewidth=0.8, zorder=4)
    axR.plot([min(xs), max(xs)], [row, row], color=colour, lw=0.8, alpha=0.45,
             zorder=3)
    axR.text(1.4e-6, row + 0.48, name, color=colour, fontsize=8.0, ha="left")
    for (label, m, side), x in zip(members, xs):
        dy = 0.17 if side == "up" else -0.36
        axR.text(x, row + dy, label, color=INK, fontsize=8.2, ha="center")

axR.axvline(1.0, color="#9a9a94", lw=0.7, ls=(0, (3, 2.5)), zorder=2)
axR.text(0.80, 2.60, "$y = 1$", fontsize=7.8, color=MUTED, ha="right")
axR.set_xscale("log")
axR.set_xlim(1.2e-6, 4.0)
axR.set_ylim(-0.62, 2.85)
axR.set_yticks([])
axR.set_xticks([1e-6, 1e-4, 1e-2, 1.0])
axR.set_xlabel("coupling to the Higgs field,  $y = 2^{1/2}m/v$")
axR.set_title("One mechanism, nine unexplained numbers",
              fontsize=9.0, loc="left", pad=8, color=INK)
axR.grid(axis="x", color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right", "left"):
    axR.spines[sp].set_visible(False)

print(f"v = {V:.4f} GeV   lambda = {LAM:.5f}   mu^2 = {MU2:.1f} GeV^2   c = {C_TH:.5f}")
print(f"depth at T=0: {vmin:.4f} x 1e8 GeV^4")
for name, _, _, members in ROWS:
    for label, m, _ in members:
        print(f"  {name:9s} {label:8s} m = {m:>10.6f} GeV   y = {np.sqrt(2)*m/V:.6e}")

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
