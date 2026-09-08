"""Figure for report 020 — the two fuels of the Bessemer blow.

Left panel — where the heat in a converter comes from, per tonne of pig iron,
for the two chemistries the nineteenth century actually ran. The bars are
computed from standard enthalpies of formation at 298 K (SiO2 -910.7, MnO
-385.2, CO -110.53 kJ/mol; P4O10 -2984.0 kJ/mol, taken per mole of phosphorus)
divided by the atomic mass of the element oxidised, which gives 32.43, 7.01,
9.20 and 24.08 MJ per kilogram for silicon, manganese, carbon and phosphorus.
Carbon is taken to CO rather than CO2, because the second oxidation happens in
the flame above the bath and its heat leaves up the stack.

The acid bar is a Cumberland or Bilbao hematite iron: 2.0 per cent silicon,
3.4 carbon, 1.0 manganese, 0.05 phosphorus. The basic bar is a Lorraine minette
iron: 0.4 per cent silicon, 3.4 carbon, 1.0 manganese, 1.9 phosphorus. The
totals are within seven per cent of each other — 1,044 and 970 MJ — but the
composition inverts. Silicon supplies 62 per cent of the acid blow; phosphorus
supplies 47 per cent of the basic one, more than carbon does. Each process is
forbidden the other's principal fuel: phosphorus by the chemistry of a silica
lining, silicon by the wear it inflicts on a dolomite one.

The hatched deduction on the basic bar is the heat absorbed in raising 128 kg of
lime — the quantity the phosphorus itself demands — from ambient to 1,600 C at a
mean solid heat capacity of 0.90 kJ/(kg K): 181 MJ, or 19 per cent of the blow.

Right panel — the flux bill, per kilogram of impurity, against the heat that
impurity releases. Silicon at a lime-to-silica ratio of two demands 4.28 kg of
lime per kilogram; phosphorus slagged as tetracalcium phosphate demands 3.62.
Both remain net fuels after paying it, which is the point: the constraint that
excluded silicon from the basic converter was refractory wear, not arithmetic.

Chart form chosen before coding: a part-to-whole comparison across two named
cases is a stacked bar, and with four components and two bars the segments are
large enough to label in place, so no legend. Print figure — direct labels, no
interaction, no dark mode.

Palette: the blue / orange / green trio used in reports 009-019.
Run: python3 figures/020-two-fuels-of-the-blow.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
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

# --- thermochemistry -------------------------------------------------------
MASS = {"Si": 28.085, "Mn": 54.938, "C": 12.011, "P": 30.973762,
        "Ca": 40.078, "O": 15.999}
DHF = {"SiO2": -910.7, "MnO": -385.2, "CO": -110.53, "P4O10": -2984.0}

Q = {"Si": -DHF["SiO2"] / MASS["Si"],
     "Mn": -DHF["MnO"] / MASS["Mn"],
     "C": -DHF["CO"] / MASS["C"],
     "P": -(DHF["P4O10"] / 4.0) / MASS["P"]}          # MJ per kg

CAO = MASS["Ca"] + MASS["O"]
SIO2 = MASS["Si"] + 2 * MASS["O"]
LIME = {"Si": 2.0 * SIO2 / MASS["Si"],                # basicity CaO/SiO2 = 2
        "P": 4.0 * CAO / (2.0 * MASS["P"])}           # slagged as 4CaO.P2O5

CP_LIME, T_TAP = 0.90, 1600 - 25                      # kJ/(kg K), K

CASES = {
    "Acid lining\nhematite iron": {"Si": 0.0200, "C": 0.0340,
                                   "Mn": 0.0100, "P": 0.0005},
    "Basic lining\nminette iron": {"Si": 0.0040, "C": 0.0340,
                                   "Mn": 0.0100, "P": 0.0190},
}
ORDER = ["Si", "C", "Mn", "P"]
COLOUR = {"Si": BLUE, "C": MUTED, "Mn": GRID, "P": ORANGE}
LABEL = {"Si": "silicon", "C": "carbon", "Mn": "manganese", "P": "phosphorus"}

fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.1, 3.35),
                             gridspec_kw={"width_ratios": [1.32, 1.0]})

# --- left: the blow --------------------------------------------------------
X_ACID, X_BASIC, W = 0.0, 1.62, 0.70
lime_kg = 128.0
sink = lime_kg * CP_LIME * T_TAP / 1000.0

tops = {}
for x, (name, comp) in zip((X_ACID, X_BASIC), CASES.items()):
    bottom, total = 0.0, sum(comp[e] * 1000.0 * Q[e] for e in ORDER)
    tops[name] = total
    struck = total - sink if x == X_BASIC else total   # top of the un-struck part
    for e in ORDER:
        h = comp[e] * 1000.0 * Q[e]
        ax.bar(x, h, bottom=bottom, width=W, color=COLOUR[e],
               edgecolor="white", linewidth=0.7, zorder=3)
        # centre the caption in the part of the segment still visible
        lo, hi = bottom, min(bottom + h, struck)
        mid = (lo + hi) / 2.0
        room = hi - lo
        ink = "white" if e in ("Si", "P", "C") else INK
        if room >= 220.0:                    # room for three lines inside
            ax.text(x, mid, f"{LABEL[e]}\n{h:.0f} MJ\n{100 * h / total:.0f} %",
                    ha="center", va="center", fontsize=7.0, zorder=4,
                    linespacing=1.35, color=ink)
        elif room >= 40.0:                   # one line, and the name outside
            ax.text(x, mid, f"{h:.0f} MJ", ha="center", va="center",
                    fontsize=6.9, zorder=4, color=ink)
            ax.annotate(f"{LABEL[e]}, {100 * h / total:.0f} %",
                        xy=(x + W / 2 + 0.02, mid), xytext=(x + W / 2 + 0.14, mid),
                        ha="left", va="center", fontsize=6.9, color=MUTED,
                        zorder=4,
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))
        bottom += h
    ax.text(x, total + 30, f"{total:.0f} MJ", ha="center", va="bottom",
            fontsize=8.6, color=INK)

# the acid bar's phosphorus is a sliver worth naming
acid_total = tops["Acid lining\nhematite iron"]
ax.annotate("phosphorus, 12 MJ", xy=(W / 2 + 0.02, acid_total - 6),
            xytext=(W / 2 + 0.16, 1120), fontsize=6.9, color=MUTED,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))

# the lime the phosphorus demands, struck off the top of the basic bar
basic_total = tops["Basic lining\nminette iron"]
ax.bar(X_BASIC, sink, bottom=basic_total - sink, width=W, color="white",
       alpha=0.74, edgecolor="none", zorder=5)
ax.bar(X_BASIC, sink, bottom=basic_total - sink, width=W, color="none",
       edgecolor=INK, linewidth=0.9, hatch="xxx", zorder=6)
ax.plot([X_BASIC - W / 2, X_BASIC + W / 2], [basic_total - sink] * 2,
        color=INK, lw=1.0, zorder=7)
ax.annotate(f"less the {sink:.0f} MJ absorbed in\nheating {lime_kg:.0f} kg of lime to\n"
            f"tapping temperature, which\nleaves {basic_total - sink:.0f} MJ",
            xy=(X_BASIC + W / 2 + 0.02, basic_total - sink / 2.0),
            xytext=(X_BASIC + 0.50, 690),
            fontsize=7.1, color=INK, ha="left", va="center", zorder=8,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))

xs = [X_ACID, X_BASIC]
ax.set_xlim(-0.66, 3.44)
ax.set_ylim(0, 1230)
ax.set_xticks(xs)
ax.set_xticklabels(list(CASES), fontsize=8.0)
ax.set_ylabel("heat released in the bath, MJ per tonne of pig iron")
ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_title("Two ways to heat the same tonne", fontsize=9.0, color=INK,
             loc="left", pad=7)

# --- right: gross heat against flux bill -----------------------------------
els = ["Si", "P"]
pos = [0.0, 1.0]
for x, e in zip(pos, els):
    cost = LIME[e] * CP_LIME * T_TAP / 1000.0
    bx.bar(x, Q[e], width=0.44, color=COLOUR[e], edgecolor="white",
           linewidth=0.7, zorder=3)
    bx.bar(x, cost, width=0.44, color="none", edgecolor=INK, linewidth=0.8,
           hatch="////", zorder=4)
    bx.text(x, Q[e] + 0.8, f"{Q[e]:.1f} MJ", ha="center", va="bottom",
            fontsize=8.4, color=INK)
    bx.text(x, cost + (Q[e] - cost) / 2.0, f"net\n{Q[e] - cost:.1f} MJ",
            ha="center", va="center", fontsize=7.6, color="white",
            linespacing=1.35)
    bx.text(x, cost + 0.9, f"flux {cost:.1f} MJ", ha="center", va="bottom",
            fontsize=7.0, color="white")
    bx.text(x, -1.1, f"{LABEL[e]}\n{LIME[e]:.2f} kg lime per kg",
            ha="center", va="top", fontsize=7.2, color=MUTED,
            linespacing=1.4)

bx.set_xlim(-0.62, 1.62)
bx.set_ylim(0, 38)
bx.set_xticks([])
bx.set_ylabel("MJ per kg of impurity oxidised")
bx.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
bx.set_axisbelow(True)
for s in ("top", "right"):
    bx.spines[s].set_visible(False)
bx.set_title("Each fuel pays for its own flux", fontsize=9.0, color=INK,
             loc="left", pad=7)

fig.tight_layout(pad=0.9)
fig.subplots_adjust(bottom=0.185)
out = Path(__file__).resolve().parent / "020-two-fuels-of-the-blow.png"
fig.savefig(out, dpi=300)
print(f"wrote {out}")
for e in ORDER:
    print(f"  q[{e}] = {Q[e]:.2f} MJ/kg")
for name, comp in CASES.items():
    tot = sum(comp[e] * 1000.0 * Q[e] for e in ORDER)
    shares = ", ".join(f"{e} {100 * comp[e] * 1000.0 * Q[e] / tot:.1f}%" for e in ORDER)
    print(f"  {name.replace(chr(10), ' ')}: {tot:.0f} MJ/t — {shares}")
print(f"  lime sink {sink:.0f} MJ = {100 * sink / basic_total:.0f}% of the basic blow")
