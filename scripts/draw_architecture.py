"""Draw the pipeline architecture diagram -> docs/architecture.png (matplotlib boxes and arrows).

  python scripts/draw_architecture.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "docs" / "architecture.png"
RED, INK, GREY, FILL = "#C8102E", "#222222", "#6B6B6B", "#FFF5F7"

# (title, body lines, x-centre, y-centre)
STAGES = [
    ("1. Sources", ["BSE/NSE disclosures API", "Annual reports FY20-FY26", "Brand sites / Wayback"], 1.1, 3.0),
    ("2. Collection", ["bse_ann.py · fetch.py", "ar_mentions.py · reg30_fields.py"], 3.3, 3.0),
    ("3. Tables", ["tab_a_data.py → acquisitions", "tab_b_data.py → in-house builds", "source_log.csv"], 5.5, 3.0),
    ("4. Verification", ["verify_quotes.py (quote matcher)", "logic_checks.py", "conflicts.md · claims log"], 7.7, 3.0),
    ("5. Base rates", ["base_rates.py", "Wilson interval · Laplace p"], 7.7, 0.9),
    ("6. Build-vs-buy model", ["build_model.py: assumptions →", "Y0-Y10 P&L → risk-adj. cost →", "breakeven → sensitivity,", "tornado, Monte Carlo"], 5.5, 0.9),
    ("7. Framework scoring", ["framework.py"], 3.3, 0.9),
    ("8. Outputs", ["build_workbook.py", "polish_workbook.py", "build_memo.py (report)", "chart_*.py (charts)"], 1.1, 0.9),
]
W, H = 1.95, 1.45


def box(ax, title, lines, x, y):
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=FILL, ec=RED, lw=1.4))
    ax.text(x, y + H / 2 - 0.2, title, ha="center", va="center", fontsize=9.5, weight="bold", color=RED)
    for i, s in enumerate(lines):
        ax.text(x, y + H / 2 - 0.48 - i * 0.24, s, ha="center", va="center", fontsize=7.6, color=INK)


def arrow(ax, a, b):
    (x1, y1), (x2, y2) = a, b
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.3))


def main():
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.set_xlim(0, 8.8)
    ax.set_ylim(-0.1, 3.9)
    ax.axis("off")
    for s in STAGES:
        box(ax, *s)
    top = [s for s in STAGES if s[3] == 3.0]
    bot = [s for s in STAGES if s[3] == 0.9]
    for a, b in zip(top, top[1:]):
        arrow(ax, (a[2] + W / 2, 3.0), (b[2] - W / 2, 3.0))
    arrow(ax, (7.7, 3.0 - H / 2), (7.7, 0.9 + H / 2))
    for a, b in zip(bot, bot[1:]):
        arrow(ax, (a[2] - W / 2, 0.9), (b[2] + W / 2, 0.9))
    ax.text(4.4, 3.82, "Research pipeline: build vs buy for Indian consumer brands", ha="center", fontsize=12,
            weight="bold", color=INK)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
    print(OUT)


if __name__ == "__main__":
    main()
