"""Headline chart for the memo: build-equivalent cost vs buy all-in cost (base case, 100% basis, Rs Cr).
Values from data/model_outputs.csv (scripts/build_model.py). Output: output/charts/p1_headline.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984"
ACCENT, ACCENT2, GREY, GREY2 = "#E4003A", "#F28AA0", "#b9b8b2", "#d9d8d2"

m = pd.read_csv(ROOT / "data/model_outputs.csv")
s = m[(m.section == "summary") & (m.scenario == "Base")].set_index("metric").value
build = [("Build cash ÷ P(success)", s.risk_adjusted_build_cost, GREY),
         ("Forgone profits, Y1–Y10", s.forgone_profits, ACCENT2),
         ("Share never recovered", s.share_loss, ACCENT)]
paid = 2706.45  # S002, completion consideration
buy = [("Paid at completion", paid, GREY),
       ("Last 9.5%\n+ costs", s.buy_all_in_100pct - paid, GREY2)]

fig, ax = plt.subplots(figsize=(7.2, 1.95), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
for y, segs, total, label in [(1, build, s.build_equivalent_cost, "Build it"), (0, buy, s.buy_all_in_100pct, "Buy it")]:
    left = 0
    for name, v, c in segs:
        ax.barh(y, v, left=left, color=c, edgecolor=SURFACE, height=0.58)
        tc = "white" if c == ACCENT else INK
        ax.text(left + v / 2, y, f"{name}\n{v:,.0f}", ha="center", va="center", fontsize=6.6, color=tc)
        left += v
    ax.text(left + 50, y, f"₹{total:,.0f} Cr", va="center", fontsize=9, fontweight="bold", color=INK)
ax.set_yticks([0, 1], ["Buy it\n(all-in, 100%)", "Build it\n(risk-adjusted)"], fontsize=8, color=INK)
ax.set_xlim(0, 4400)
ax.tick_params(axis="x", labelsize=7, colors=INK2)
ax.set_xlabel("₹ Cr, base case, present value at HUL's 11.3% WACC", fontsize=7, color=INK2)
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GREY)
ax.tick_params(axis="y", length=0)
ax.annotate("Time (red): ₹2,456 Cr,\n~2x the build itself", xy=(1267 + 1063 + 1393 / 2, 1.32), xytext=(3800, 1.55),
            fontsize=6.8, color=ACCENT, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
ax.set_ylim(-0.45, 1.8)
fig.tight_layout(pad=0.4)
fig.savefig(ROOT / "output/charts/p1_headline.png", dpi=220, facecolor=SURFACE)
print("saved p1_headline.png", round(s.build_equivalent_cost), round(s.buy_all_in_100pct))

# Compact tornado for the memo (top 6 drivers; same values as output/charts/p1_tornado.png)
t = m[m.section == "tornado"].set_index("metric").value
DRIVERS = [("category_growth", "Category growth (9–20%)"), ("p_success", "P(success) (5–29%)"),
           ("steady_ebitda_margin", "Steady EBITDA margin (15–30%)"), ("discount_rate", "Discount rate (10–13%)"),
           ("years_to_scale", "Years to scale (4–8)"), ("org_cost_floor", "Org cost floor (₹12–30 Cr)")]
base_be = s.breakeven_headline_price
fig, ax = plt.subplots(figsize=(4.0, 2.1), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
for i, (k, lab) in enumerate(DRIVERS[::-1]):
    lo, hi = t[f"{k}_at_low"], t[f"{k}_at_high"]
    for v, c in [(lo, ACCENT2), (hi, ACCENT)]:
        ax.barh(i, v - base_be, left=base_be, color=c, height=0.6)
        ax.text(v + (45 if v > base_be else -45), i, f"{v:,.0f}", va="center", ha="left" if v > base_be else "right",
                fontsize=6.8, color=INK)
ax.set_yticks(range(len(DRIVERS)), [d[1] for d in DRIVERS[::-1]], fontsize=7, color=INK)
ax.axvline(base_be, color=INK, lw=0.9)
ax.axvline(paid, color=INK2, lw=0.9, ls="--")
ax.text(paid - 30, 5.55, "Paid ₹2,706", ha="right", va="center", fontsize=6.6, color=INK2)
ax.text(base_be + 30, 5.55, "Base ₹3,196", ha="left", va="center", fontsize=6.6, color=INK)
ax.set_xlim(1700, 6900); ax.set_ylim(-0.6, 5.9)
ax.tick_params(axis="x", labelsize=6.8, colors=INK2); ax.tick_params(axis="y", length=0)
ax.set_xlabel("Breakeven, ₹ Cr (light = driver low, dark = high)", fontsize=6.8, color=INK2)
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GREY)
fig.tight_layout(pad=0.4)
fig.savefig(ROOT / "output/charts/p1_tornado_memo.png", dpi=220, facecolor=SURFACE)
print("saved p1_tornado_memo.png")
