"""Figure for report 024 — how far the carbonation front gets, and how much
carbon that actually returns.

Both panels describe the same cubic metre of structural concrete: 300 kg of
portland cement at a clinker ratio of 0.71 and 65 per cent CaO in the clinker,
so 138.5 kg of calcined lime and 110.8 kg of process CO2 released at the kiln.

Left panel — the front. Carbonation depth follows x = k sqrt(t), the solution
of a steady-state diffusion balance through the already-carbonated layer. Three
carbonation coefficients span the practical range: 1.5 mm/yr^0.5 for a dense
mix rained on, 2.5 for ordinary sheltered exposure, 4.0 for a porous mix in dry
indoor air. Two horizontal lines matter more than the curves: 30 mm, a typical
cover to the reinforcement, at which the steel depassivates and the structure
starts to fail; and 100 mm, the half-thickness of a 200 mm wall, which is what
full carbonation would require.

Right panel — the carbon. Fraction of the element's own process CO2 taken back,
for the same wall carbonating from both faces, and for the same concrete crushed
to 20 mm rubble at demolition in year 60 — same mix, same k, only the geometry
changes. The chemical ceiling is 73.5 per cent:
75 per cent of the calcined lime is carbonatable, and the IPCC's 1.02 kiln-dust
factor put 2 per cent of the emission somewhere the structure never sees. The
cover-depth ceiling is 30.1 per cent of the volume, 22.1 per cent of the carbon,
reached at 144 years — long after the structure is meant to be standing.

Palette: the blue/orange/green set already validated for this series (009-023),
all-pairs checked at print contrast. Series are labelled directly; this is print.
Run: python3 figures/024-carbonation-front-and-cap.py
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

# ------------------------------------------------------------------ chemistry
M_CAO, M_CO2 = 56.0770, 44.009
CEMENT, CLINKER_RATIO, F_CAO, CKD = 300.0, 0.71, 0.65, 1.02
DEGREE = 0.75                      # carbonatable share of the calcined lime

CLINKER = CEMENT * CLINKER_RATIO
PROCESS = CLINKER * F_CAO * (M_CO2 / M_CAO) * CKD      # kg CO2 per m3, 110.8
CAP = DEGREE / CKD                                     # 0.735 of the process CO2

THICK, COVER, PARTICLE = 200.0, 30.0, 20.0             # mm
DEMOLITION = 60.0                                      # years
K_RUBBLE = 2.5                                         # same mix, only the geometry changes


def depth(t, k):
    return k * np.sqrt(t)


def wall_fraction(t, k, thickness=THICK):
    """Volume share of a slab carbonated from both faces."""
    return np.minimum(2.0 * depth(t, k) / thickness, 1.0)


def sphere_fraction(x, radius):
    """Volume share of a sphere carbonated to depth x from the surface."""
    x = np.minimum(x, radius)
    return 1.0 - ((radius - x) / radius) ** 3


# ------------------------------------------------------------------- figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.05))

# ---- left: the front ----
t = np.logspace(0, np.log10(3000), 400)
for k, colour, lab, tlab, off in ((4.0, ORANGE, "$k = 4.0$", 380.0, (-9, 4)),
                                  (2.5, BLUE, "$k = 2.5$", 2300.0, (-10, 3)),
                                  (1.5, GREEN, "$k = 1.5$", 1100.0, (-10, 4))):
    ax1.plot(t, depth(t, k), color=colour, lw=1.5)
    ax1.annotate(lab, xy=(tlab, depth(tlab, k)), xytext=off,
                 textcoords="offset points", ha="right", va="bottom",
                 color=colour, fontsize=7.8)

for y, lab in ((COVER, "30 mm cover to the steel"), (THICK / 2, "100 mm half-wall")):
    ax1.axhline(y, color=MUTED, lw=0.7, ls=(0, (4, 3)))
    ax1.annotate(lab, xy=(1.25, y), xytext=(0, 3), textcoords="offset points",
                 color=MUTED, fontsize=7.4)

for k, colour in ((4.0, ORANGE), (2.5, BLUE), (1.5, GREEN)):
    ax1.plot([(COVER / k) ** 2], [COVER], "o", ms=3.4, color=colour, zorder=5)
ax1.annotate("56 yr", xy=((COVER / 4.0) ** 2, COVER), xytext=(-9, -15),
             textcoords="offset points", ha="right", color=ORANGE, fontsize=7.2)
ax1.annotate("144 yr", xy=((COVER / 2.5) ** 2, COVER), xytext=(11, -13),
             textcoords="offset points", ha="left", color=BLUE, fontsize=7.2)
ax1.annotate("400 yr", xy=((COVER / 1.5) ** 2, COVER), xytext=(9, -13),
             textcoords="offset points", ha="left", color=GREEN, fontsize=7.2)

ax1.set_xscale("log")
ax1.set_xlim(1, 3000)
ax1.set_ylim(0, 130)
ax1.set_xlabel("years of exposure")
ax1.set_ylabel("carbonation depth (mm)")
ax1.set_title("The front advances as the square root of time", fontsize=8.8, color=INK, pad=7)
ax1.grid(True, which="major", color=GRIDC, lw=0.5)
ax1.set_axisbelow(True)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# ---- right: the carbon ----
t2 = np.logspace(0, np.log10(1000), 600)
service = wall_fraction(t2, 2.5) * CAP

crushed = np.where(
    t2 <= DEMOLITION,
    wall_fraction(np.minimum(t2, DEMOLITION), 2.5) * CAP,
    np.maximum(
        wall_fraction(DEMOLITION, 2.5),
        sphere_fraction(depth(np.maximum(t2 - DEMOLITION, 0.0), K_RUBBLE), PARTICLE / 2),
    ) * CAP,
)

ax2.plot(t2, 100 * crushed, color=ORANGE, lw=1.5)
ax2.plot(t2, 100 * service, color=BLUE, lw=1.5)
ax2.axhline(100 * CAP, color=MUTED, lw=0.7, ls=(0, (4, 3)))
ax2.axhline(100 * (2 * COVER / THICK) * CAP, color=MUTED, lw=0.7, ls=(0, (1, 2.5)))

ax2.annotate("73.5%: everything the kiln\ncalcined that can come back",
             xy=(1.25, 100 * CAP), xytext=(0, -20), textcoords="offset points",
             color=MUTED, fontsize=7.4)
ax2.annotate("22.1%: all a reinforced wall may\ngive back before the steel goes",
             xy=(1.25, 100 * (2 * COVER / THICK) * CAP), xytext=(0, 4),
             textcoords="offset points", color=MUTED, fontsize=7.4)
ax2.annotate("crushed at demolition,\nyear 60", xy=(110, 100 * CAP),
             xytext=(8, -26), textcoords="offset points", ha="left",
             color=ORANGE, fontsize=7.8)
ax2.annotate("left standing", xy=(330, 100 * wall_fraction(330, 2.5) * CAP),
             xytext=(-6, 7), textcoords="offset points", ha="right",
             color=BLUE, fontsize=7.8)

ax2.set_xscale("log")
ax2.set_xlim(1, 1000)
ax2.set_ylim(0, 88)
ax2.set_xlabel("years since the concrete was cast")
ax2.set_ylabel("share of the element's process CO$_2$ taken back (%)")
ax2.set_title("What comes back, and when", fontsize=8.8, color=INK, pad=7)
ax2.grid(True, which="major", color=GRIDC, lw=0.5)
ax2.set_axisbelow(True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.tight_layout(pad=0.7)
out = Path(__file__).resolve().parent / "024-carbonation-front-and-cap.png"
fig.savefig(out, dpi=300)
print(f"wrote {out}")
print(f"process CO2 = {PROCESS:.1f} kg/m3 ; chemical cap = {100*CAP:.1f}% ; "
      f"cover cap = {100*(2*COVER/THICK)*CAP:.1f}%")
print(f"service wall at 50/100 yr: {100*wall_fraction(50,2.5)*CAP:.1f}% / "
      f"{100*wall_fraction(100,2.5)*CAP:.1f}%")
