"""Figure for report 024 — the carbonation front, and why thin sections are the sink.

Both panels are the same one-parameter law. Carbonation advances into concrete as
a diffusion front, so its depth goes as the square root of time,

    x(t) = k sqrt(t),

with k in mm per sqrt(year). Field surveys of real structures put k between about
0 and 14 mm/sqrt(yr) with a median near 1.4; laboratory and exposed-deck values of
3 to 8 are common in poorer or more exposed concrete.

Left panel — the corrosion clock. Depth against time for four values of k, with
the Eurocode nominal cover band (25-50 mm) shaded. Where a curve crosses the band
is when the front reaches the reinforcement, the pore solution has lost its
alkalinity, and the steel's passive film is gone. At k = 1.4 a 30 mm cover lasts
459 years; at k = 8 it lasts 14.

Right panel — where the sink actually lives. For a member of thickness d exposed
on both faces, the carbonated fraction of the section is min(1, 2 k sqrt(t) / d).
A 10 mm mortar render at k = 3 is fully carbonated in under three years; a 300 mm
column has done 14 per cent of its section in fifty. The sink is overwhelmingly a
thin-section phenomenon, which is why mortar and crushed demolition waste
dominate the published uptake accounts and structural concrete does not.

Palette: the blue/orange/green set already validated for this series (009-023),
all-pairs checked at print contrast. Series are labelled directly; this is print.
Run: python3 figures/024-carbonation-front.py
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
def depth(t, k):
    """Carbonation depth in mm after t years."""
    return k * np.sqrt(t)


def years_to(x_mm, k):
    """Years for the front to reach depth x_mm."""
    return (x_mm / k) ** 2


def fraction(t, k, d_mm):
    """Carbonated fraction of a section of thickness d, exposed on both faces."""
    return np.minimum(1.0, 2.0 * k * np.sqrt(t) / d_mm)


assert abs(years_to(30, 1.4) - 459.18) < 0.05
assert abs(years_to(30, 8.0) - 14.0625) < 1e-6
assert abs(fraction(50.0, 3.0, 300.0) - 0.14142) < 1e-5

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.05),
                               gridspec_kw=dict(width_ratios=[1.0, 1.02],
                                                wspace=0.30))

# ---- left: the corrosion clock -------------------------------------------
t = np.linspace(0.0, 300.0, 1200)
axL.axhspan(25, 50, color=GRID, zorder=0)
axL.text(296, 37.5, "Eurocode nominal\ncover, 25–50 mm", fontsize=7.4, color=MUTED,
         ha="right", va="center")
for k, colour, lxy in ((8.0, ORANGE, (26, 62)),
                       (5.0, GREEN, (92, 61)),
                       (3.0, BLUE, (110, 38.0)),
                       (1.4, INK, (232, 23.0))):
    axL.plot(t, depth(t, k), color=colour, lw=1.7, zorder=3)
    axL.text(lxy[0], lxy[1], f"$k = {k}$", color=colour, fontsize=8.2,
             ha="left", va="bottom")
axL.text(296, 12.0,
         "30 mm of cover: the front arrives\n"
         "after 14 years at $k = 8$, 459 at $k = 1.4$",
         fontsize=7.4, color=MUTED, ha="right", va="top")
axL.set_xlim(0, 300)
axL.set_ylim(0, 70)
axL.set_xticks([0, 50, 100, 150, 200, 250, 300])
axL.set_xlabel("years of exposure")
axL.set_ylabel("carbonation depth (mm)")
axL.set_title("The front reaches the steel", fontsize=9.0, loc="left", pad=8,
              color=INK)
axL.grid(color=GRID, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: where the sink lives -----------------------------------------
t2 = np.linspace(0.0, 100.0, 1200)
for d_mm, colour, label, lxy in (
        (10, ORANGE, "10 mm mortar render", (30.0, 0.915)),
        (150, GREEN, "150 mm slab", (46.0, 0.425)),
        (300, BLUE, "300 mm column — 14% of its\nsection after half a century",
         (38.0, 0.115))):
    axR.plot(t2, fraction(t2, 3.0, d_mm), color=colour, lw=1.7, zorder=3)
    axR.text(lxy[0], lxy[1], label, color=colour, fontsize=7.8, ha="left",
             va="top")
t_full = (10.0 / (2 * 3.0)) ** 2
axR.plot([t_full], [1.0], "o", ms=3.8, color=ORANGE, zorder=6)
axR.annotate(f"fully carbonated\nat {t_full:.1f} years", xy=(t_full, 1.0),
             xytext=(12.0, 0.80), fontsize=7.4, color=ORANGE, ha="left", va="top",
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6,
                             shrinkA=3, shrinkB=4))
axR.plot([50.0], [fraction(50.0, 3.0, 300.0)], "o", ms=3.8, color=BLUE, zorder=6)
axR.set_xlim(0, 100)
axR.set_ylim(0, 1.05)
axR.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axR.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
axR.set_xlabel("years of exposure   ($k = 3$ mm yr$^{-1/2}$)")
axR.set_ylabel("share of the section carbonated")
axR.set_title("Where the sink actually lives", fontsize=9.0, loc="left", pad=8,
              color=INK)
axR.grid(color=GRID, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
for k in (1.4, 3.0, 5.0, 8.0):
    print(f"  k={k:4.1f}: 25 mm in {years_to(25, k):7.1f} yr, "
          f"30 mm in {years_to(30, k):7.1f} yr, 50 mm in {years_to(50, k):7.1f} yr")
print(f"  10 mm render fully carbonated at k=3 in {t_full:.2f} yr")
print(f"  300 mm column at 50 yr: {fraction(50.0, 3.0, 300.0):.4f} of section")
