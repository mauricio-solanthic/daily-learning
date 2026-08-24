"""Figure for report 010 — the two constraints on helium.

Left panel: helium concentration by source, on a log axis in parts per million
by volume. Air sits at 5.4 ppmv (Danabalan et al. 2022); ordinary
natural gas is under about 500 ppmv; the published economic threshold falls
somewhere in 1,000-3,000 ppmv depending on whom you ask, and that band is drawn
rather than a line because the sources genuinely disagree. Everything to the
right of the band is a helium field; everything to the left is not.

Right panel: world helium refinery production in 2024, by country, from USGS
Mineral Commodity Summaries 2025. The United States figure combines the two
lines the USGS reports separately, 68 Mm3 extracted from natural gas and 13 Mm3
withdrawn from the Cliffside field. Qatar is called out because one industrial
city, Ras Laffan, supplies all of it.

Concentrations: Danabalan et al. 2022 (5.4 ppm air, 0.1% threshold, 10.5% Rukwa
seep); Physics World 2016 (0.3% threshold, <=0.05% ordinary gas);
USGS MCS 2025 (production). Palette: dataviz categorical slots 1-3 (light),
validated all-pairs, as used in figure 009.
Run: python3 figures/010-helium-concentration-and-supply.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
    "ytick.color": INK, "figure.facecolor": "white", "savefig.facecolor": "white",
})

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.15),
                               gridspec_kw=dict(width_ratios=[1.12, 1.0],
                                                wspace=0.40))

# ---- left: concentration, log ppmv ----------------------------------------
rows = [("Rukwa seep, Tanzania", 105_000, ORANGE, "10.5%"),
        ("Helium-rich gas field", 19_000, ORANGE, "1.9%"),
        ("Ordinary natural gas", 500, BLUE, "0.05%"),
        ("Dry air", 5.4, BLUE, "5.4 ppm")]
ys = list(range(len(rows)))
axL.axvspan(1_000, 3_000, color=AQUA, alpha=0.16, zorder=1)
for y, (label, ppm, colour, tag) in zip(ys, rows):
    axL.plot([1.0, ppm], [y, y], color=RULE, lw=0.8, zorder=2)
    axL.plot([ppm], [y], "o", ms=6.0, color=colour, zorder=4)
    axL.text(ppm * 1.55, y, tag, va="center", ha="left", fontsize=7.8, color=INK)
axL.text(1_730, 3.70, "economic\nthreshold", fontsize=7.2, color=MUTED,
         ha="center", va="top", linespacing=1.3)
axL.set_yticks(ys, [r[0] for r in rows])
axL.set_xscale("log")
axL.set_xlim(1.0, 1.1e6)
axL.set_xticks([1, 1e2, 1e4, 1e6], ["1", "100", "10,000", "1,000,000"])
axL.set_ylim(-0.75, 4.05)
axL.set_xlabel("helium, parts per million by volume")
axL.set_title("What counts as a helium field", fontsize=9.0, loc="left",
              pad=8, color=INK)
axL.grid(axis="x", color=RULE, lw=0.6, zorder=0)
for s in ("top", "right", "left"):
    axL.spines[s].set_visible(False)

# ---- right: world production 2024 -----------------------------------------
bars = [("Poland", 3, BLUE), ("China", 3, BLUE), ("Canada", 6, BLUE),
        ("Algeria", 11, BLUE), ("Russia", 17, BLUE),
        ("United States", 81, BLUE), ("Qatar", 64, ORANGE)]
ys = list(range(len(bars)))
axR.barh(ys, [b[1] for b in bars], height=0.62,
         color=[b[2] for b in bars], zorder=3)
shares = {"Qatar": "36% of the world", "United States": "45%"}
for y, (name, v, _c) in zip(ys, bars):
    axR.text(v + 2.2, y, f"{v}", va="center", ha="left", fontsize=7.8, color=INK)
    if name in shares:
        axR.text(v + 2.2, y - 0.42, shares[name], va="center", ha="left",
                 fontsize=6.9, color=MUTED)
axR.text(1.8, len(bars) - 1 + 0.52, "one industrial city", fontsize=7.2,
         color=MUTED, ha="left", va="bottom")
axR.set_yticks(ys, [b[0] for b in bars])
axR.set_xlim(0, 108)
axR.set_xticks([0, 20, 40, 60, 80])
axR.set_ylim(-0.7, len(bars) - 0.05)
axR.set_xlabel("million cubic metres, 2024")
axR.set_title("Where the world's helium came from", fontsize=9.0, loc="left",
              pad=8, color=INK)
axR.grid(axis="x", color=RULE, lw=0.6, zorder=0)
for s in ("top", "right", "left"):
    axR.spines[s].set_visible(False)

fig.subplots_adjust(left=0.205, right=0.975, top=0.855, bottom=0.155)
out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300)
print(f"wrote {out}")
print(f"air->threshold(0.1%) = {1_000/5.4:,.0f}x ; air->threshold(0.3%) = {3_000/5.4:,.0f}x")
print(f"Qatar share of 180 Mm3 world total = {64/180*100:.1f}% ; US = {81/180*100:.1f}%")
