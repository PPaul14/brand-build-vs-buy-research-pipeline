"""Small multiples of annual-report mentions per FY for each Tab B brand -> output/charts/ar_mentions.png

  python scripts/chart_ar_mentions.py

One panel per brand, one series per panel (single hue, no legend), panels grouped by status_today from
data/tab_b.csv. Each panel has its own y-scale: the chart is about presence/absence over time, not about
comparing counts across parents (report length differs a lot). FYs with no report on BSE are marked 'n/a'.
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "charts" / "ar_mentions.png"
SURFACE, INK, INK2, MUTED, GRID, BAR = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#2a78d6"
ORDER = ["Scaled", "Stable", "Unclear", "Niche", "Withdrawn"]
FYS = [f"FY{y}" for y in range(20, 27)]

mentions = {}
for r in csv.DictReader((ROOT / "data" / "ar_mentions.csv").open(encoding="utf-8")):
    mentions.setdefault(r["brand"], {})[r["fy"]] = int(r["mentions"]) if r["status"] == "counted" else None

status, rowtype = {}, {}
for r in csv.DictReader((ROOT / "data" / "tab_b.csv").open(encoding="utf-8")):
    status[r["brand"]], rowtype[r["brand"]] = r["status_today"], r["row_type"]


def tab_b_key(label):
    """Match a tracker label ('Nykd') to its tab_b brand ('Nykd by Nykaa')."""
    hits = [b for b in status if b.lower().startswith(label.lower().split(" /")[0]) or label.lower().split(" /")[0] in b.lower()]
    return hits[0] if hits else None


panels = []
for label, series in mentions.items():
    k = tab_b_key(label)
    if k:
        panels.append((ORDER.index(status[k]), label, status[k], rowtype[k], series))
panels.sort(key=lambda p: (p[0], p[1]))

cols = 6
rows = -(-len(panels) // cols)
fig, axes = plt.subplots(rows, cols, figsize=(cols * 2.35, rows * 1.75 + 0.9), facecolor=SURFACE)
plt.rcParams["font.family"] = "DejaVu Sans"
for ax in axes.flat:
    ax.set_visible(False)
for ax, (_, label, st, rt, series) in zip(axes.flat, panels):
    ax.set_visible(True)
    ax.set_facecolor(SURFACE)
    vals = [series.get(fy) for fy in FYS]
    top = max([v for v in vals if v] + [1])
    for i, v in enumerate(vals):
        if v is None:
            ax.text(i, top * 0.04, "n/a", ha="center", va="bottom", fontsize=5.5, color=MUTED)
        elif v == 0:
            ax.plot([i - 0.3, i + 0.3], [0, 0], color=MUTED, lw=1.2, solid_capstyle="round")  # explicit zero
        else:
            ax.bar(i, v, width=0.7, color=BAR, edgecolor=SURFACE, linewidth=1)
    ax.set_ylim(0, top * 1.18)
    ax.set_xlim(-0.6, len(FYS) - 0.4)
    ax.set_xticks(range(len(FYS)), [f[2:] for f in FYS], fontsize=6, color=INK2)
    ax.tick_params(axis="y", labelsize=6, colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(2, integer=True))
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    tag = " (calib.)" if rt == "calibration" else ""
    ax.set_title(f"{label}{tag}\n{st}", fontsize=7, color=INK, loc="left", pad=3, linespacing=1.15)

fig.suptitle("Tab B brands: mentions in the parent's annual report, FY20-FY26", x=0.01, ha="left",
             fontsize=11, color=INK, fontweight="bold", y=0.995)
fig.text(0.01, 0.958, "Count of brand-name matches per report (own y-scale per panel). Grey dash = 0 mentions; n/a = no report "
         "(parent not yet listed). Second title line = status_today in tab_b. Panels grouped by status.",
         fontsize=7, color=INK2, ha="left")
fig.text(0.01, 0.004, "Source: annual reports FY20-FY26 from the BSE AnnualReport API (T1), counted by scripts/ar_mentions.py; "
         "data/ar_mentions.csv. Accessed 2026-10-10.", fontsize=6.5, color=MUTED, ha="left")
fig.tight_layout(rect=(0, 0.015, 1, 0.945), h_pad=1.2, w_pad=0.6)
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=200, facecolor=SURFACE)
print(f"{len(panels)} panels -> {OUT.relative_to(ROOT)}")
