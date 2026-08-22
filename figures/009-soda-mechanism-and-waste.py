"""Figure for report 009 — the ammonia-soda process.

Left panel: solubility of the four salts that share the Solvay liquor, at 25 C.
Sodium bicarbonate is the least soluble by a factor of ~3.5, which is the whole
mechanism: it is the salt that leaves the solution.

Right panel: waste per tonne of soda ash, from stoichiometry (Leblanc:
2 NaCl + H2SO4 -> Na2SO4 + 2 HCl, then Na2SO4 + CaCO3 + 2 C -> Na2CO3 + CaS
+ 2 CO2; ammonia-soda net: 2 NaCl + CaCO3 -> Na2CO3 + CaCl2), cross-checked
against the reported 1.75 t of galligu per tonne of soda.

Solubilities: CRC Handbook of Chemistry and Physics, 95th ed., via PubChem.
Palette: dataviz categorical slots 1-3 (light), validated all-pairs.
Run: python3 figures/009-soda-mechanism-and-waste.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

SERIF = "TeX Gyre Pagella"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED = "#0b0b0b", "#52514e"

plt.rcParams.update({
    "font.family": "serif", "font.serif": [SERIF], "font.size": 8.2,
    "mathtext.fontset": "custom", "mathtext.rm": SERIF,
    "mathtext.it": f"{SERIF}:italic", "mathtext.bf": f"{SERIF}:bold",
    "axes.edgecolor": "#c9c9c4", "axes.linewidth": 0.6,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": INK, "figure.facecolor": "white", "savefig.facecolor": "white",
})

M = dict(Na2CO3=105.988, NaCl=58.443, CaCO3=100.087, CaCl2=110.984,
         CaS=72.143, HCl=36.461)
per_t = lambda sp, n=1: n * M[sp] / M["Na2CO3"]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.0, 1.15],
                                                wspace=0.42))

# ---- left: solubility -----------------------------------------------------
salts = [r"NaHCO$_3$", r"Na$_2$CO$_3$", "NaCl", r"NH$_4$Cl"]
sol = [10.3, 30.7, 36.0, 39.5]
y = range(len(salts))
axL.barh(y, sol, height=0.62, color=BLUE, zorder=3)
for i, v in enumerate(sol):
    axL.text(v + 1.0, i, f"{v:.1f}", va="center", ha="left", fontsize=8.2, color=INK)
axL.set_yticks(list(y), salts)
axL.set_xlim(0, 50)
axL.set_xticks([0, 10, 20, 30, 40])
axL.set_xlabel("grams per 100 g of water, 25 °C")
axL.set_title("What leaves the solution", fontsize=9.0, loc="left", pad=8, color=INK)
axL.text(18.5, 0, "least soluble of the four,\nby a factor of 3.5", fontsize=7.4,
         color=MUTED, ha="left", va="center", linespacing=1.35)
axL.grid(axis="x", color="#e6e6e2", lw=0.6, zorder=0)
for s in ("top", "right", "left"):
    axL.spines[s].set_visible(False)

# ---- right: waste per tonne ----------------------------------------------
hcl, galligu, cacl2 = per_t("HCl", 2), 1.75, per_t("CaCl2")
rows = ["Leblanc\n(1791)", "Ammonia-soda\n(1861)"]
segs = [("Hydrogen chloride evolved", BLUE, [hcl, 0.0]),
        ("Calcium-sulfide waste (galligu)", ORANGE, [galligu, 0.0]),
        ("Calcium chloride to water", AQUA, [0.0, cacl2])]
left = [0.0, 0.0]
for label, colour, vals in segs:
    axR.barh(rows, vals, height=0.66, left=left, color=colour, label=label,
             edgecolor="white", linewidth=1.6, zorder=3)
    for i, v in enumerate(vals):
        if v > 0.25:
            axR.text(left[i] + v / 2, i, f"{v:.2f} t", va="center", ha="center",
                     fontsize=7.8, color="white")
    left = [a + b for a, b in zip(left, vals)]
for i, tot in enumerate(left):
    axR.text(tot + 0.06, i, f"{tot:.2f} t", va="center", ha="left",
             fontsize=8.2, color=INK)
axR.set_xlim(0, 3.0)
axR.set_ylim(1.62, -0.62)
axR.set_xlabel("tonnes of waste per tonne of soda ash")
axR.set_title("What the process throws away", fontsize=9.0, loc="left", pad=8, color=INK)
axR.grid(axis="x", color="#e6e6e2", lw=0.6, zorder=0)
for s in ("top", "right", "left"):
    axR.spines[s].set_visible(False)
axR.legend(loc="upper center", bbox_to_anchor=(0.44, -0.30), frameon=False,
           fontsize=7.4, ncol=1, handlelength=1.1, handleheight=0.9,
           labelcolor=MUTED, borderpad=0)

fig.subplots_adjust(left=0.115, right=0.965, top=0.88, bottom=0.345)
out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300)
print(f"wrote {out}")
print(f"HCl {hcl:.3f} t  galligu {galligu} t  CaCl2 {cacl2:.3f} t"
      f"  | CaS share of galligu {per_t('CaS')/galligu*100:.1f}%")
