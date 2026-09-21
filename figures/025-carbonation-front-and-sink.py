"""Figure for report 025 — why the geometry of a cement product, not its
chemistry, decides how much carbon dioxide it takes back.

Left panel — the fraction of a cement-bound element that has carbonated, as a
function of its age, under the diffusion-limited square-root law x = k sqrt(t)
with k = 3.75 mm/yr^0.5, a value near the middle of the range reported for
in-service structural concrete and close to the 4.0 the same law returns from
Fick's first law at an effective diffusivity of 5e-8 m2/s. The chemistry is
identical in all four
elements; only the distance the front has to travel differs. A 10 mm mortar bed
joint is finished in seven years and a 20 mm render in twenty-eight; a 200 mm
slab needs seven centuries and a metre-thick raft foundation needs eighteen.

Right panel — the consequence, in the global accounts. Concrete takes about
73 per cent of the world's cement and supplies about 30 per cent of the
carbonation sink; mortar takes about 24 per cent and supplies about 59 per
cent. Use shares are from the 1928-2024 account (Nie et al. 2025); uptake
shares from the 1930-2021 account (Wang et al. 2023), whose remaining 11 per
cent is construction waste and cement kiln dust.

Palette: the blue/orange/green set already validated for this series (009-024),
all-pairs checked at print contrast. Series are labelled directly; this is print.
Run: python3 figures/025-carbonation-front-and-sink.py
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

K = 3.75          # mm per square root of a year


# ---------------------------------------------------------------- mechanics
def depth(t):
    """Carbonation depth in mm after t years, diffusion-limited."""
    return K * np.sqrt(np.asarray(t, dtype=float))


def fraction(t, thickness, faces):
    """Fraction of a section carbonated: one face, two faces, or a square
    section attacked on all four."""
    x = depth(t)
    if faces == 1:
        return np.clip(x / thickness, 0.0, 1.0)
    if faces == 2:
        return np.clip(2.0 * x / thickness, 0.0, 1.0)
    core = np.clip(thickness - 2.0 * x, 0.0, None)
    return 1.0 - (core / thickness) ** 2


def full_at(thickness, faces):
    """Age in years at which the section is wholly carbonated."""
    reach = thickness if faces == 1 else thickness / 2.0
    return (reach / K) ** 2


ELEMENTS = (
    (10.0, 1, ORANGE, "10 mm mortar bed joint"),
    (20.0, 1, "#b8451c", "20 mm render"),
    (200.0, 2, BLUE, "200 mm slab"),
    (1000.0, 2, GREEN, "1 m raft foundation"),
)

assert abs(full_at(10.0, 1) - 7.1111) < 1e-3
assert abs(full_at(20.0, 1) - 28.4444) < 1e-3
assert abs(depth(50.0) - 26.5165) < 1e-3
assert abs(full_at(1000.0, 2) - 17777.7778) < 1e-2

fig, (axL, axR) = plt.subplots(1, 2, figsize=(7.0, 3.15),
                               gridspec_kw=dict(width_ratios=[1.18, 1.0],
                                                wspace=0.34))

# ---- left: the same chemistry, four geometries ---------------------------
t = np.linspace(0.0, 100.0, 900)
for thickness, faces, colour, label in ELEMENTS:
    axL.plot(t, 100.0 * fraction(t, thickness, faces), color=colour, lw=1.8, zorder=4)

axL.text(12.5, 101.5, "10 mm mortar bed joint", color=ORANGE, fontsize=7.6,
         ha="left", va="bottom")
axL.text(33.0, 92.0, "20 mm render", color="#b8451c", fontsize=7.6,
         ha="left", va="top")
axL.text(97.0, 100.0 * fraction(97.0, 200.0, 2) + 3.2, "200 mm slab",
         color=BLUE, fontsize=7.6, ha="right", va="bottom")
axL.text(97.0, 100.0 * fraction(97.0, 1000.0, 2) - 3.2, "1 m raft foundation",
         color=GREEN, fontsize=7.6, ha="right", va="top")
axL.text(46.0, 62.0, "front depth $x = k\\,t^{1/2}$,\n$k = 3.75$ mm per root year",
         fontsize=7.4, color=MUTED, ha="left", va="center")

axL.set_xlim(0.0, 100.0)
axL.set_ylim(0.0, 112.0)
axL.set_yticks([0, 25, 50, 75, 100])
axL.set_xlabel("age of the element, years")
axL.set_ylabel("share of the section carbonated, %")
axL.set_title("Identical chemistry, four geometries", fontsize=9.0, loc="left",
              pad=8, color=INK)
axL.grid(color=GRIDC, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axL.spines[sp].set_visible(False)

# ---- right: where the cement goes against where the carbon goes ----------
ROWS = ((73.0, 30.1, BLUE, "concrete"), (24.0, 58.5, ORANGE, "mortar"))
for use, sink, colour, label in ROWS:
    axR.plot([0, 1], [use, sink], color=colour, lw=1.8, zorder=3)
    axR.plot([0, 1], [use, sink], "o", ms=5.2, color=colour, zorder=4,
             markeredgecolor="white", markeredgewidth=0.6)
    axR.text(-0.045, use, f"{label}  {use:.0f}%", color=colour, fontsize=8.0,
             ha="right", va="center")
    axR.text(1.045, sink, f"{sink:.1f}%", color=colour, fontsize=8.0,
             ha="left", va="center")

axR.text(0.5, 12.0, "waste and kiln dust supply\nthe remaining 11 per cent",
         fontsize=7.4, color=MUTED, ha="center", va="center")
axR.set_xlim(-0.62, 1.34)
axR.set_ylim(0.0, 82.0)
axR.set_xticks([0, 1])
axR.set_xticklabels(["share of cement used", "share of the sink"])
axR.set_yticks([0, 20, 40, 60, 80])
axR.set_ylabel("per cent")
axR.set_title("A quarter of the cement, half of the carbon", fontsize=9.0,
              loc="left", pad=8, color=INK)
axR.grid(axis="y", color=GRIDC, lw=0.6, zorder=1)
for sp in ("top", "right"):
    axR.spines[sp].set_visible(False)
axR.tick_params(axis="x", length=0)

out = Path(__file__).with_suffix(".png")
fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.02)
print("wrote", out)
for thickness, faces, _c, label in ELEMENTS:
    print(f"  {label:24s} full at {full_at(thickness, faces):8.1f} yr; "
          f"{100 * fraction(50.0, thickness, faces):5.1f}% at 50 yr; "
          f"{100 * fraction(10.0, thickness, faces):5.1f}% at 10 yr")
print(f"  depth at 10/50/100 yr: {depth(10):.1f} / {depth(50):.1f} / {depth(100):.1f} mm")
for use, sink, _c, label in ROWS:
    print(f"  {label:9s} uptake per tonne of cement, relative index {sink / use:.3f}")
print(f"  mortar / concrete intensity ratio {(58.5 / 24.0) / (30.1 / 73.0):.2f}")
