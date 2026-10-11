"""Framework: score every Tab A / Tab B row against the buy-vs-build framework and draw the matrix.

Score S = V1 + 2*V2 + V3 + V5 (V3 = 'spike' is a gate: do not enter). V4 (price) is a gate, not a score.
  S >= 2  -> BUY side : buy a target at <= 10.2x revenue (model breakeven, p = 11%)
  S <= 1  -> BUILD side: build; buying is still fine at <= 6.1x (model grid, p = 29%, T = 4 yrs)
Hit rules
  Build rows: BUY side predicts the build fails (Withdrawn/Niche); BUILD side predicts it survives (Scaled/Stable).
              Spike gate predicts failure. Unclear rows are not scored.
  Buy rows:   hit if the multiple is within the price line of the side the row falls on.
              Rows with no multiple are 'untested' (side only). Campa (no revenue bought) is a miss.
Feature codes are analyst judgements; each is explained in notes/part3.md. Outputs:
  data/framework_scores.csv, output/charts/framework.png
"""
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
BUY_LINE, BUILD_LINE = 10.2, 6.1   # 3,196/0.905/347 = 10.18x ; 1,912.5/0.905/347 = 6.09x (model_outputs.csv)

# brand-prefix -> (V1 demand driver C/D, V2 capability distance far/near, V3 window, V5 founder)
# V1: C = cohort-led (+1), D = distribution-led (-1)
# V2: +1 parent has never scaled a brand in the channel that wins this category; -1 it has (weighted x2)
# V3: +1 structural & fast (independents >=2x in 3-4 yrs); -1 mature; 0 unknown; 'spike' = Covid-type demand
# V5: Buy rows: +1 target founders retained (staged deal / founders still run it). Build rows: +1 credibility is
#     founder/heritage-carried and the parent has no such founder; -1 parent itself is founder-run (Honasa, Nykaa)
CODES = {
    # ---- Tab A (Buy)
    "Minimalist": ("C", 1, 1, 1), "OZiva": ("C", 1, 1, 0), "Wellbeing": ("C", 1, 1, 0),
    "Yoga Bar": ("C", 1, 1, 1), "Mother Sparsh": ("C", 1, 1, 1), "24 Mantra": ("C", 1, 0, 0),
    "Prasuma": ("C", 1, 0, 1), "Soulfull": ("C", 1, 1, 0), "Ching": ("D", -1, 0, 0),
    "Organic India": ("C", 1, 1, 0), "Beardo": ("C", 1, 1, 1), "Just Herbs": ("C", 1, 1, 1),
    "True Elements": ("C", 1, 1, 1), "Plix": ("C", 1, 1, 1), "Cosmix": ("C", 1, 1, 1),
    "4700BC": ("C", 1, 1, 1), "Badshah": ("D", -1, -1, 0), "Sesa": ("D", -1, -1, 0),
    "Park Avenue": ("D", -1, -1, 0), "Muuchstac": ("C", 1, 1, 0), "Dot & Key": ("C", -1, 1, 1),
    "Earth Rhythm": ("C", -1, 1, 0), "The Man Company": ("C", 1, 1, 1), "Brillare": ("C", 1, 1, 0),
    "Dermicool": ("D", -1, -1, 0), "Reginald": ("C", -1, 1, 1), "RiteBite": ("C", 1, 1, 0),
    "Banjara": ("D", -1, -1, 0), "Lotus": ("D", -1, -1, 0), "Campa": ("D", -1, -1, 0), "Sosyo": ("D", -1, -1, 0),
    # ---- Tab B (Build)
    "Lever Ayush": ("C", 1, 1, 1), "Love Beauty": ("C", 1, 1, 0), "Acne Squad": ("C", 1, 1, 1),
    "Find Your Happy": ("C", 1, 0, 0), "Novology": ("C", 1, 1, 0), "Saffola Immuniveda": ("C", 1, "spike", 0),
    "Veggie Clean": ("D", -1, "spike", 0), "The Derma Co": ("C", -1, 1, -1), "Aqualogica": ("C", -1, 1, -1),
    "Ayuga": ("C", -1, 1, -1), "Staze": ("C", -1, 0, -1), "Godrej Fab": ("D", -1, 0, 0),
    "Godrej Ninja": ("C", 1, 1, 0), "Godrej Protekt": ("D", -1, 0, 0), "Dabur Vita": ("D", -1, -1, 0),
    "Tata Simply Better": ("C", 1, 0, 0), "Tata GoFit": ("C", 1, 1, 0), "Tata Sampann": ("D", -1, -1, 0),
    "Nykd": ("C", -1, 0, -1), "Kay Beauty": ("C", -1, 1, -1), "Bingo": ("D", -1, 1, 0),
    "Sunfeast YiPPee": ("D", -1, 0, 0), "Fabelle": ("C", -1, 0, 0), "Bajaj Zero Grey": ("C", 1, 0, 0),
    "Natyv Soul": ("C", 1, 0, 0), "Bajaj 100% Pure": ("D", -1, -1, 0), "I'mlite": ("D", -1, -1, 0),
    "Independence": ("D", -1, -1, 0),
}
SUCCESS, FAIL = {"Scaled", "Stable"}, {"Withdrawn", "Niche"}


def code_for(brand):
    for k, v in CODES.items():
        if brand.startswith(k) or k in brand.split(" (")[0]:
            return v
    raise KeyError(brand)


def score(row):
    v1, v2, v3, v5 = code_for(row.brand)
    spike = v3 == "spike"
    s = (1 if v1 == "C" else -1) + 2 * v2 + (0 if spike else v3) + v5
    side = "AVOID (spike)" if spike else ("BUY" if s >= 2 else "BUILD")
    status = str(row.status_today)
    if row.route == "Build":
        if status == "Unclear" or row.base_rate_flag == "excluded_unclear":
            hit = "not scored"
        elif side == "BUILD":
            hit = "hit" if status in SUCCESS else "miss"
        else:
            hit = "hit" if status in FAIL else "miss"
    else:
        m = row.revenue_multiple
        if row.brand.startswith("Campa"):
            hit = "miss"          # bought a name with no revenue, then built: the framework has no box for it
        elif pd.isna(m):
            hit = "untested"
        else:
            hit = "hit" if m <= (BUY_LINE if side == "BUY" else BUILD_LINE) else "miss"
    return pd.Series(dict(v1_demand=v1, v2_distance=v2, v3_window=v3, v5_founder=v5, score=s, side=side, hit=hit))


def main():
    a = pd.read_csv(ROOT / "data/tab_a.csv"); a["table"] = "A"
    b = pd.read_csv(ROOT / "data/tab_b.csv"); b["table"] = "B"
    b["route"] = "Build"
    d = pd.concat([a, b], ignore_index=True)
    d["base_rate_flag"] = d.get("base_rate_flag")
    out = pd.concat([d[["table", "route", "row_type", "parent", "brand", "status_today", "revenue_multiple"]],
                     d.apply(score, axis=1)], axis=1)
    out["brand"] = out.brand.str.split(" \\(").str[0]
    out.to_csv(ROOT / "data/framework_scores.csv", index=False)

    for t in ["A", "B"]:
        x = out[out.table == t]
        n_hit, n_scored = (x.hit == "hit").sum(), x.hit.isin(["hit", "miss"]).sum()
        print(f"Tab {t}: {n_hit}/{n_scored} = {n_hit / n_scored:.0%}; misses: {list(x[x.hit == 'miss'].brand)}; "
              f"untested/not scored: {list(x[~x.hit.isin(['hit', 'miss'])].brand)}")
    s = out[out.hit.isin(["hit", "miss"])]
    print(f"All: {(s.hit == 'hit').sum()}/{len(s)} = {(s.hit == 'hit').mean():.0%}")
    bb = out[(out.table == "B")]
    for lab, mask in [("dist-led builds (non-spike)", (bb.v1_demand == "D") & (bb.v3_window != "spike")),
                      ("cohort-led builds, far parent", (bb.v1_demand == "C") & (bb.v2_distance == 1)),
                      ("cohort-led builds, near parent", (bb.v1_demand == "C") & (bb.v2_distance == -1))]:
        y = bb[mask & (bb.status_today != "Unclear")]
        print(lab, f"{y.status_today.isin(['Scaled']).sum()} scaled, {y.status_today.isin(SUCCESS).sum()} survive / {len(y)}",
              list(zip(y.brand, y.status_today)))
    print(out[["table", "brand", "score", "side", "revenue_multiple", "status_today", "hit"]].to_string())
    ha, hb = [out[(out.table == t) & out.hit.isin(["hit", "miss"])] for t in "AB"]
    draw(f"Back-test: {(s.hit == 'hit').sum()} of {len(s)} scored rows right ({(s.hit == 'hit').mean():.0%}). "
         f"Builds {(hb.hit == 'hit').sum()}/{len(hb)}; deals {(ha.hit == 'hit').sum()}/{len(ha)} with a known multiple. "
         "Misfits: Campa (built on a bought name), HUL-Wellbeing (18x minority, sold).")


def draw(hit_line):
    SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
    BUY, BUILD = "#2a78d6", "#eb6834"
    rows = [
        ("V1 Demand driver", "x1",
         "Cohort-led: leaders built online, priced >=1.5x mass, bought on trust in an ingredient, founder or identity",
         "Distribution-led: mass price point, bought where it is stocked (GT, MT, own retail)",
         "Cohort-led builds by parents far from the channel: 0 of 10 scaled. Distribution-led builds: 7 of 9 survive (Fab Rs 490 Cr run rate; Independence Rs 2,600 Cr; Bingo!, YiPPee!, Sampann)"),
        ("V2 Capability distance", "x2",
         "Parent has never scaled a brand to Rs 100 Cr in the channel that wins the category",
         "Parent already owns that channel (GT reach, captive retail, a D2C engine)",
         "Digital-first builds: FMCG parents 0/7, D2C natives 2/4 (Derma Co, Aqualogica). Godrej Ninja: Rs 2.2 Cr in year 1 vs Fab Rs 150 Cr, same parent"),
        ("V3 Time window", "x1",
         "Structural and fast: independents doubled within 3-4 yrs of purchase",
         "Mature or unbranded-heavy: a late entrant still wins on price. Spike (Covid): do not enter",
         "Plix 8.1x, Yoga Bar 6.6x, Just Herbs 5.6x post-deal. Model: delay = Rs 2,456 Cr, 2x the build; build wins only at scale in <=4 yrs. Spike launches 0/2"),
        ("V4 Price of a credible target", "gate",
         "BUY side: a target exists at <= 10.2x revenue (100% basis)",
         "BUILD side: still buy if <= 6.1x (cheaper than building revenue)",
         "model breakeven Rs 3,196 Cr / 90.5% / Rs 347 Cr = 10.2x (p 11%); grid p 29%, 4 yrs = 6.1x. Tab A median 4.9x; 20 of 22 deals <= 10.2x"),
        ("V5 Founder", "x1",
         "Credibility sits with a founder who stays (staged / earn-out)",
         "Parent is itself founder-run, or credibility sits in price and reach",
         "Founders still run Minimalist, Dot & Key; staged deals: Yoga Bar, Plix, Mother Sparsh, Prasuma. Founder-run Honasa builds 2/4"),
    ]
    W = [1.25, 0.45, 2.15, 2.15, 2.9]
    fig = plt.figure(figsize=(8.3, 4.35), facecolor=SURFACE)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, sum(W)); ax.set_ylim(0, 1); ax.axis("off")
    xs = [sum(W[:i]) for i in range(len(W))]
    top, hdr_h, row_h = 0.865, 0.05, 0.118
    ax.text(0.08, 0.955, "Buy or build? A five-variable test for a conglomerate entering a new category",
            fontsize=10.5, fontweight="bold", color=INK, va="center")
    for x, w, h, c in zip(xs, W, ["Variable", "Weight", "Pushes to BUY when", "Pushes to BUILD when", "Evidence (Tab A / Tab B / model)"],
                          [INK, INK, BUY, BUILD, INK]):
        ax.text(x + 0.08, top + hdr_h / 2, h, fontsize=7.2, fontweight="bold", color=c, va="center")
    ax.plot([0.08, sum(W) - 0.08], [top, top], color=INK2, lw=0.8)
    wraps = [18, 6, 42, 42, 55]
    for i, r in enumerate(rows):
        y = top - (i + 0.5) * row_h
        for j, (x, txt) in enumerate(zip(xs, r)):
            ax.text(x + 0.08, y, textwrap.fill(txt, wraps[j]), fontsize=6.1 if j else 6.8, va="center",
                    color=INK if j in (0, 1) else INK2, fontweight="bold" if j == 0 else "normal", linespacing=1.2)
        ax.plot([0.08, sum(W) - 0.08], [top - (i + 1) * row_h] * 2, color=GRID, lw=0.6)
    yb = top - 5 * row_h - 0.075
    rule = ("Score S = V1 + 2xV2 + V3 + V5 (each +1 toward buy, -1 toward build).   S >= +2: BUY at <= 10.2x revenue.   "
            "\nS <= +1: BUILD, and buy only at <= 6.1x.   Covid-type demand spike: neither.")
    ax.text(0.08, yb, rule, fontsize=6.9, color=INK, fontweight="bold", va="center", linespacing=1.5)
    ax.text(0.08, yb - 0.075, hit_line, fontsize=6.5, color=INK2, va="center")
    ax.text(0.08, 0.025, "Source: Analysis of Tab A (31 deals) and Tab B (29 builds), built from annual reports, Reg 30 filings and "
            "company statements; the build model (data/model_outputs.csv). Scores: data/framework_scores.csv.",
            fontsize=5.6, color=MUTED, va="center")
    out = ROOT / "output/charts/framework.png"
    fig.savefig(out, dpi=220, facecolor=SURFACE)
    print("saved", out)


if __name__ == "__main__":
    main()
