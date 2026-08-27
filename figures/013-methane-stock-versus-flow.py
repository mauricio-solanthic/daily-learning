"""Figure for report 013 — what a methane source does, and what it is charged.

Both panels follow one hypothetical source emitting 1 Tg (one million tonnes) of
methane a year, held at that rate for long enough before year zero that its
contribution to the atmosphere has reached steady state. Three futures are then
imposed: hold the rate flat, cut it by 0.32 per cent a year, or grow it by 1 per
cent a year.

Left panel — the physics. A one-box atmospheric model,

    dB/dt = E(t) - B / tau,      tau = 11.8 yr (AR6 methane perturbation lifetime)

whose steady state is B = E * tau. Methane's radiative forcing is proportional
to this burden to first order, so the curve is a proxy for the source's warming
contribution. Plotted as an index, 1.0 at year zero.

Right panel — the accounting. Cumulative CO2-equivalent charged to the same
source under two metrics, both using GWP100 = 27 for non-fossil methane:

    GWP100:  E_CO2e(t)  = 27 * E(t)
    GWP*:    E_CO2we(t) = 27 * ( r*H/dt * (E(t) - E(t-20)) + s * E(t) ),
             r = 0.75, s = 0.25, H = 100 yr, dt = 20 yr  (Smith et al. 2021)

so the rate coefficient r*H/dt is exactly 3.75 and the stock coefficient s is
0.25. For t < 20 the source's history is flat, so E(t-20) = E(0).

The point of the pairing: the left panel holds three different climate
outcomes, one of them a source whose contribution to the atmosphere is
shrinking, and every dashed GWP100 line in the right panel ramps upward
regardless.

Palette: the blue / orange / green trio already used in reports 009-012, checked
with the dataviz validator at print contrast (all adjacent pairs pass; the green
carries a contrast WARN against white, met here by direct labels on every line).
Run: python3 figures/013-methane-stock-versus-flow.py
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
    "axes.edgecolor": "#c9c9c4", "axes.linewidth": 0.6,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.facecolor": "white", "savefig.facecolor": "white",
})

TAU = 11.8          # yr, AR6 methane perturbation lifetime
GWP100 = 27.0       # non-fossil methane, AR6
R, S, H, DT = 0.75, 0.25, 100.0, 20.0
K = R * H / DT
assert K == 3.75

YEARS = 80
STEP = 0.02
t = np.arange(0.0, YEARS + STEP, STEP)

SCENARIOS = [
    ("held flat",        0.0,     BLUE),
    ("cut 0.32%/yr",    -0.00322, GREEN),
    ("grown 1%/yr",      0.01,    ORANGE),
]


def emissions(t, g):
    """Tg CH4 per year; before year zero the rate has always been 1."""
    return np.where(t < 0.0, 1.0, (1.0 + g) ** np.maximum(t, 0.0))


def burden(t, g):
    """Integrate dB/dt = E - B/tau from the steady state B(0) = tau."""
    b = np.empty_like(t)
    b[0] = TAU
    for i in range(1, len(t)):
        e = emissions(t[i - 1], g)
        b[i] = b[i - 1] + STEP * (e - b[i - 1] / TAU)
    return b


def annual_charges(t, g):
    """(GWP100, GWP*) annual charge in Mt CO2 equivalent per year."""
    e_now = emissions(t, g)
    e_then = emissions(t - DT, g)
    return GWP100 * e_now, GWP100 * (K * (e_now - e_then) + S * e_now)


fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.15),
                               gridspec_kw=dict(width_ratios=[1.0, 1.12],
                                                wspace=0.30))

# ---- left: what the atmosphere does --------------------------------------
for label, g, colour in SCENARIOS:
    axL.plot(t, burden(t, g) / TAU, color=colour, lw=1.7, zorder=3)
axL.axhline(1.0, color="#9a9a94", lw=0.7, ls=(0, (3, 2.5)), zorder=2)
axL.set_xlim(0, YEARS)
axL.set_ylim(0.55, 2.35)
axL.set_xticks([0, 20, 40, 60, 80])
axL.set_yticks([0.6, 1.0, 1.4, 1.8, 2.2])
axL.set_xlabel("years from now")
axL.set_ylabel("methane in the air from this source, indexed to today")
axL.set_title("What the atmosphere does", fontsize=9.0, loc="left", pad=8,
              color=INK)
axL.text(60, 2.02, "emissions grown 1%/yr", color=ORANGE, fontsize=8.0,
         ha="center")
axL.text(46, 1.07, "held flat", color=BLUE, fontsize=8.0, ha="center")
axL.text(56, 0.70, "cut 0.32%/yr", color=GREEN, fontsize=8.0, ha="center")
axL.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: what the inventory says --------------------------------------
peak = 0.0
for label, g, colour in SCENARIOS:
    gwp, star = annual_charges(t, g)
    cum_gwp = np.cumsum(gwp) * STEP / 1000.0        # Gt CO2e
    cum_star = np.cumsum(star) * STEP / 1000.0
    axR.plot(t, cum_gwp, color=colour, lw=1.2, ls=(0, (3.5, 2.0)), zorder=3)
    axR.plot(t, cum_star, color=colour, lw=1.7, zorder=4)
    peak = max(peak, cum_gwp[-1], cum_star[-1])
axR.set_xlim(0, YEARS)
axR.set_ylim(-0.1, 4.5)
axR.set_xticks([0, 20, 40, 60, 80])
axR.set_yticks([0, 1, 2, 3, 4])
axR.set_xlabel("years from now")
axR.set_ylabel("cumulative charge, Gt carbon dioxide equivalent")
axR.set_title("What the inventory says", fontsize=9.0, loc="left", pad=8,
              color=INK)
axR.annotate("GWP100, all three", xy=(46, 1.30), xytext=(30, 2.75),
             fontsize=7.8, color=MUTED, ha="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6,
                             shrinkA=3, shrinkB=3))
axR.text(2.0, 4.18, "dashed: GWP100    solid: GWP*", fontsize=7.6, color=MUTED,
         ha="left")
axR.text(78, 3.62, "GWP*, grown", color=ORANGE, fontsize=8.0, ha="right")
axR.text(78, 0.72, "GWP*, flat", color=BLUE, fontsize=8.0, ha="right")
axR.text(78, 0.30, "GWP*, cut", color=GREEN, fontsize=8.0, ha="right")
axR.grid(color=GRID, lw=0.6, zorder=0)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

print("peak cumulative charge on the plot: %.2f Gt" % peak)
for label, g, _ in SCENARIOS:
    gwp, star = annual_charges(t, g)
    print("  %-14s  GWP100 %.2f Gt   GWP* %.2f Gt   burden index %.3f"
          % (label, np.cumsum(gwp)[-1] * STEP / 1000.0,
             np.cumsum(star)[-1] * STEP / 1000.0, burden(t, g)[-1] / TAU))

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
