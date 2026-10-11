"""Story pitch chart: every digital-first build in the base rate, one tile each, by parent type and outcome.
Rows come from data/base_rates.csv rates (c) and (d); statuses from data/tab_b.csv. Output: output/charts/pitch_chart.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984"
FILL = {"Scaled": "#E4003A", "Stable": "#F28AA0", "Niche": "#d9d8d2", "Withdrawn": "#ecebe6"}
GROUPS = [
    ("FMCG giants (HUL, Dabur, Tata Consumer, Bajaj)", "0 of 7 scaled",
     ["Acne Squad", "Find Your Happy Place", "Dabur Vita", "Tata GoFit", "Bajaj Zero Grey", "Natyv Soul", "Bajaj 100% Pure"]),
    ("D2C-native parent (Honasa; built pre-IPO)", "2 of 4 scaled", ["The Derma Co", "Aqualogica", "Ayuga", "Staze"]),
]
PARENT = {"Acne Squad": "HUL", "Find Your Happy Place": "HUL", "Dabur Vita": "Dabur", "Tata GoFit": "Tata",
          "Bajaj Zero Grey": "Bajaj", "Natyv Soul": "Bajaj", "Bajaj 100% Pure": "Bajaj",
          "The Derma Co": "Honasa", "Aqualogica": "Honasa", "Ayuga": "Honasa", "Staze": "Honasa"}
EXTRA = {"The Derma Co": "Rs 750 Cr ARR", "Aqualogica": "Rs 200 Cr ARR"}

b = pd.read_csv(ROOT / "data/tab_b.csv")
status = {r.brand.split(" (")[0]: r.status_today for r in b.itertuples()}
status["Staze"] = status.get("Staze", status.get("Staze 9to9"))

fig, ax = plt.subplots(figsize=(7.2, 3.3), facecolor=SURFACE)
ax.set_facecolor(SURFACE); ax.axis("off"); ax.set_xlim(0, 7.2); ax.set_ylim(0, 3.3)
fig.subplots_adjust(0, 0, 1, 1)
ax.text(0.15, 3.12, "FMCG giants' digital-first brands went 0 for 7", fontsize=12.5, fontweight="bold", color=INK, va="center")
ax.text(0.15, 2.86, "Digital-first brands built in-house since 2020, by parent type and status in October 2026", fontsize=7.5, color=INK2, va="center")
tw, th, gap = 0.93, 0.62, 0.06
y0 = 1.78
for gi, (label, tally, brands) in enumerate(GROUPS):
    y = y0 - gi * 1.08
    ax.text(0.15, y + th + 0.13, label, fontsize=7.6, color=INK, fontweight="bold", va="center")
    ax.text(7.05, y + th + 0.13, tally, fontsize=9, color=INK, fontweight="bold", va="center", ha="right")
    for i, br in enumerate(brands):
        x = 0.15 + i * (tw + gap)
        st = status[br]
        ax.add_patch(plt.Rectangle((x, y), tw, th, facecolor=FILL[st], edgecolor=SURFACE, lw=2))
        dark = st == "Scaled"
        ax.text(x + 0.06, y + th - 0.11, br if len(br) < 15 else br.replace(" ", "\n", 1) if br.count(" ") < 3 else "Find Your\nHappy Place",
                fontsize=6.3, color="white" if dark else INK, fontweight="bold", va="top", linespacing=1.1)
        ax.text(x + 0.06, y + 0.09, f"{PARENT[br]} · {st}" + (f"\n{EXTRA[br]}" if br in EXTRA else ""),
                fontsize=5.5, color="white" if dark else INK2, va="bottom", linespacing=1.15)
ax.text(0.15, 0.12, "Scaled = parent-disclosed revenue/ARR of Rs 100 Cr+. Withdrawn = parent-stated exit, or store shut and dropped from the annual report; "
        "Niche = still sold, no scale.\nSource: Tracker of company annual reports FY20-FY26, brand sites and Wayback captures "
        "(data/tab_b.csv, base_rates.csv). ARR is company-stated.", fontsize=5.3, color=MUTED, va="bottom", linespacing=1.3)
out = ROOT / "output/charts/pitch_chart.png"
fig.savefig(out, dpi=220, facecolor=SURFACE)
print("saved", out, {b: status[b] for g in GROUPS for b in g[2]})
