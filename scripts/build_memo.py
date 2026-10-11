"""Build output/BuyOrBuild_Report.pdf (reportlab; WeasyPrint needs GTK).

Five A4 pages: P1 answer + headline exhibit, P2 model detail, P3 framework, P4 recommendation call,
P5 story pitch + AI usage note + method box. Model numbers are read from data/model_outputs.csv so the memo
cannot drift from the model; text figures come from notes/*.md.

  python scripts/build_memo.py [--sheet https://docs.google.com/spreadsheets/d/...]
"""
import argparse
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "output/charts"
OUT = ROOT / "output/BuyOrBuild_Report.pdf"
PLACEHOLDER = "PASTE_YOUR_LINK_HERE"

ap = argparse.ArgumentParser()
ap.add_argument("--sheet", default=PLACEHOLDER)
SHEET = ap.parse_args().sheet

for name, f in [("Arial", "arial.ttf"), ("Arial-Bold", "arialbd.ttf"), ("Arial-Italic", "ariali.ttf"),
                ("Arial-BoldItalic", "arialbi.ttf")]:
    pdfmetrics.registerFont(TTFont(name, f"C:/Windows/Fonts/{f}"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic",
                              boldItalic="Arial-BoldItalic")

ACCENT = colors.HexColor("#C8102E")
ACCENT_LT = colors.HexColor("#FDEEF1")
INK = colors.HexColor("#111111")
INK2 = colors.HexColor("#52514e")
RULE = colors.HexColor("#d9d8d2")
SHADE = colors.HexColor("#f4f4f1")

PAGE_W, PAGE_H = A4
LM = RM = 18 * mm
TM, BM = 15 * mm, 15 * mm
W = PAGE_W - LM - RM

# ---- model numbers -------------------------------------------------------------------------------------------
m = pd.read_csv(ROOT / "data/model_outputs.csv")
S = {sc: m[(m.section == "summary") & (m.scenario == sc)].set_index("metric").value for sc in ["Bull", "Base", "Bear"]}
MC = m[m.section == "monte_carlo"].set_index("metric").value
GRID = m[m.section == "sensitivity_grid"]
B = S["Base"]
PAID = 2706.45


def cr(v):
    return f"{v:,.0f}"


# ---- styles --------------------------------------------------------------------------------------------------
def st(name, **kw):
    base = dict(fontName="Arial", fontSize=10, leading=13.2, textColor=INK, alignment=TA_LEFT, spaceAfter=5)
    base.update(kw)
    return ParagraphStyle(name, **base)


BODY = st("body", spaceAfter=4)
BODY_S = st("body_s", fontSize=9.2, leading=12)
BUL = st("bul", leftIndent=10, bulletIndent=0, spaceAfter=2.5)
BUL_S = st("bul_s", fontSize=9.2, leading=12, leftIndent=10, bulletIndent=0, spaceAfter=2)
H_TITLE = st("title", fontName="Arial-Bold", fontSize=24, leading=28, spaceAfter=3)
H_DECK = st("deck", fontSize=12, leading=15.5, textColor=INK2, spaceAfter=4)
H_BY = st("by", fontSize=8.5, leading=11, textColor=INK2, spaceAfter=10)
H1 = st("h1", fontName="Arial-Bold", fontSize=15, leading=18, spaceAfter=2, textColor=INK)
KICK = st("kick", fontName="Arial-Bold", fontSize=8, leading=10, textColor=ACCENT, spaceAfter=1)
H2 = st("h2", fontName="Arial-Bold", fontSize=10.5, leading=13, spaceBefore=4, spaceAfter=3)
EXH = st("exh", fontName="Arial-Bold", fontSize=9, leading=11.5, spaceBefore=5, spaceAfter=3)
SRC = st("src", fontSize=7, leading=8.8, textColor=INK2, spaceAfter=6)
CELL = st("cell", fontSize=7.8, leading=9.6, spaceAfter=0)
CELL_B = st("cell_b", fontName="Arial-Bold", fontSize=7.8, leading=9.6, spaceAfter=0)
CELL_H = st("cell_h", fontName="Arial-Bold", fontSize=7.8, leading=9.6, spaceAfter=0, textColor=colors.white)
ANSWER = st("answer", fontSize=10.5, leading=14.2, spaceAfter=0)
TILE_N = st("tile_n", fontName="Arial-Bold", fontSize=17, leading=20, textColor=ACCENT, spaceAfter=1)
TILE_T = st("tile_t", fontSize=7.8, leading=9.6, textColor=INK2, spaceAfter=0)
BOX = st("box", fontSize=8.6, leading=11.2, spaceAfter=2)
BOX_H = st("box_h", fontName="Arial-Bold", fontSize=9, leading=11.5, spaceAfter=3, textColor=ACCENT)


def P(t, s=BODY):
    return Paragraph(t, s)


def bullets(items, s=BUL):
    return [Paragraph(t, s, bulletText="•") for t in items]


def exhibit(n, title):
    return P(f"<font color='#C8102E'>Exhibit {n}.</font> {title}", EXH)


def src(t):
    return P("Source: " + t, SRC)


def img(name, width):
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(str(CH / name)).getSize()
    return Image(str(CH / name), width=width, height=width * ih / iw)


def part_head(kicker, title):
    return [P(kicker.upper(), KICK), P(title, H1),
            Table([[""]], colWidths=[W], rowHeights=[1.2],
                  style=[("LINEABOVE", (0, 0), (-1, 0), 1.2, ACCENT)]), Spacer(1, 4)]


def table(rows, widths, header=True, zebra=True, bold_rows=(), font=CELL, extra=(), right_cols=()):
    def cs(i, j):
        s = CELL_H if (header and i == 0) else (CELL_B if i in bold_rows else font)
        return ParagraphStyle(f"{s.name}_r", parent=s, alignment=2) if j in right_cols else s
    data = [[c if not isinstance(c, str) else Paragraph(c, cs(i, j)) for j, c in enumerate(r)]
            for i, r in enumerate(rows)]
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
             ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
             ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE)]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), ACCENT)]
    if zebra:
        style += [("BACKGROUND", (0, i), (-1, i), SHADE) for i in range(2 if header else 1, len(rows), 2)]
    style += list(extra)
    return Table(data, colWidths=widths, style=style, repeatRows=1 if header else 0)


def box(flowables, bg=ACCENT_LT, border=None):
    t = Table([[flowables]], colWidths=[W])
    s = [("BACKGROUND", (0, 0), (-1, -1), bg), ("LEFTPADDING", (0, 0), (-1, -1), 8),
         ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
         ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if border:
        s.append(("LINEBEFORE", (0, 0), (0, -1), 2.5, border))
    t.setStyle(TableStyle(s))
    return t


story = []

# ================================================= PAGE 1 =====================================================
story += [
    P("CONSUMER BRANDS RESEARCH  ·  BUILD VS BUY", KICK),
    P("Buy or Build", H_TITLE),
    P("HUL paid ₹2,706 Cr for Minimalist. Building it would have cost more, but only just, "
      "and most of the bill would have been time.", H_DECK),
    P("Consumer Brands Research  ·  October 2026  ·  "
      "Evidence: 31 deals, 29 in-house builds and 216 logged sources, 191 of them exchange filings or annual reports", H_BY),
]
answer = (
    f"<b>Buying beat building, but narrowly.</b> Building a digital-first active-skincare brand to Minimalist's "
    f"₹347 Cr would have cost HUL about <b>₹{cr(B.build_equivalent_cost)} Cr</b> risk-adjusted, against "
    f"<b>₹{cr(B.buy_all_in_100pct)} Cr</b> to buy it all-in. The build itself is cheap: peak cash burn is "
    f"₹{cr(B.peak_cumulative_burn)} Cr. But it takes about seven years from the decision, and on the record of "
    f"FMCG parents' own digital brands it succeeds about one time in nine (p = 11%). <b>Time is the main cost:</b> "
    f"profits forgone during the catch-up and market share never recovered come to ₹{cr(B.cost_of_delay)} Cr, "
    f"two-thirds of the build bill. Buying stops making sense above <b>₹{cr(B.breakeven_headline_price)} Cr</b> "
    f"for the 90.5% stake (P10–P90 range ₹{cr(MC.breakeven_P10)}–{cr(MC.breakeven_P90)} Cr). HUL paid "
    f"₹2,706 Cr, below breakeven in {MC.share_breakeven_above_price:.0%} of 10,000 simulated draws. "
    f"The general rule, drawn from the full record: FMCG giants can build brands that win on distribution, "
    f"but they have to buy brands that win on a cohort's trust.")
story.append(box([P(answer, ANSWER)], bg=ACCENT_LT, border=ACCENT))
story.append(Spacer(1, 6))

tiles = [("7 yrs", "decision to ₹347 Cr in the base case (5 bull, 9 bear)"),
         ("11%", "chance an FMCG-built digital brand scales: 0 of 7 did"),
         (f"₹{cr(B.breakeven_headline_price)} Cr", "breakeven headline price for 90.5% (base)"),
         (f"{MC.share_breakeven_above_price:.0%}", "of 10,000 draws where breakeven beats the ₹2,706 Cr paid")]
tw = (W - 3 * 6) / 4
tile_tbl = Table([[[P(n, TILE_N), P(t, TILE_T)] for n, t in tiles]], colWidths=[tw] * 4)
tile_tbl.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, 0), 2, ACCENT), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                              ("TOPPADDING", (0, 0), (-1, -1), 5)]))
story += [tile_tbl, Spacer(1, 2)]

story.append(P("The three Minimalist prices, and what each one measures", H2))
mini = [
    ["Figure", "What it is", "Source"],
    ["₹2,955 Cr", "Pre-money <b>enterprise value of 100%</b>, \"subject to adjustments\". A valuation, not a payment.",
     "Reg 30, 22 Jan 2025 (S007)"],
    ["₹2,670 Cr", "<b>Secondary cash</b> agreed for the sellers' shares (founders, Peak XV, Surge, Twenty Nine) at announcement.",
     "Reg 30, 22 Jan 2025 (S007)"],
    ["<b>₹2,706.45 Cr</b>", "<b>Total paid at completion</b> (21 Apr 2025): secondary after adjustments plus ₹45 Cr primary. "
     "<b>Used here.</b> That is 8.6× FY24 turnover of ₹347 Cr (the filing does not say whether this is revenue from operations or total income).",
     "Completion filing, 21 Apr 2025 (S002)"],
]
story += [table(mini, [60, 325, W - 385]), Spacer(1, 2)]

story.append(exhibit(1, "Building costs about ₹490 Cr more than buying, and two-thirds of the build bill is time"))
story.append(img("p1_headline.png", W))
story.append(src("Build model, base case, 100% basis (scripts/build_model.py → data/model_outputs.csv). Paid: HUL "
                 "completion filing (S002). Last 9.5%: PV of forward rights, HUL AR FY26 Note 43(C) (S134); deal costs "
                 "₹17 Cr + integration ₹50 Cr (UNCONFIRMED) − cash acquired ₹41 Cr (S134)."))

P_ = m[(m.section == "build_pnl") & (m.scenario == "Base")].pivot(index="metric", columns="year", values="value")
T_ = int(B["T"])
first_pos = int(P_.loc["ebitda"][P_.loc["ebitda"] > 0].index.min())
mkt = P_.loc["marketing", 1:T_].sum()
story.append(exhibit(2, f"Even if it works, the build loses money until Y{first_pos}, and the marketing to reach ₹347 Cr "
                        f"adds up to ~₹{mkt:,.0f} Cr"))
YRS = list(range(0, 8)) + [10]
yr = [["₹ Cr, base case"] + [f"Y{y}" + ("*" if y == T_ else "") for y in YRS]]
for lab, k in [("Revenue", "revenue"), ("Gross margin", None), ("A&amp;P (marketing + acquisition)", "marketing"),
               ("R&amp;D (product development)", "rnd"), ("Digital team inside HUL", "org_cost"),
               ("Distribution + overheads", "other_opex"), ("EBITDA", "ebitda"), ("Cumulative cash", "cumulative_cash")]:
    if k is None:
        yr.append([lab] + [("–" if P_.loc["revenue", y] == 0 else f"{P_.loc['gross_profit', y] / P_.loc['revenue', y]:.0%}") for y in YRS])
    else:
        yr.append([lab] + [f"{P_.loc[k, y]:,.0f}" for y in YRS])
yw = (W - 128) / len(YRS)
story += [table(yr, [128] + [yw] * len(YRS), bold_rows=(7, 8), right_cols=tuple(range(1, len(YRS) + 1)),
                extra=[("BACKGROUND", (T_ + 1, 1), (T_ + 1, -1), ACCENT_LT),
                       ("TOPPADDING", (0, 0), (-1, -1), 1.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.4)]),
          src("*Y6 = scale year. data/model_outputs.csv (build_pnl, Base), live in the workbook's Build_Model tab. Y0 = FY26 "
              "setup year; cash-positive from Y7, burn repaid by Y10. Drivers in Exhibit 3.")]
story.append(PageBreak())

# ================================================= PAGE 2 =====================================================
story += part_head("Model", "Price the alternative: what building Minimalist would have cost")
story.append(P(
    "The model builds the brand year by year on Honasa's and Minimalist's cost ratios, divides the burn by the odds "
    "of success, adds the cost of delay and compares the total with the full cost of the deal."))

story.append(exhibit(3, "The build case runs on D2C cost ratios: about seven years and ₹190 Cr of peak burn, if it works"))
assum = [
    ["Driver", "Base (range)", "Evidence"],
    ["Years from launch to ₹347 Cr", "6, plus 1 setup year (4–8)",
     "Bull: Minimalist (founded 2020, ₹347 Cr FY24, S007), The Derma Co (₹500 Cr+ ARR in 50 months, S163). "
     "Bear: Aqualogica's plateau near ₹200 Cr (S165)"],
    ["Gross margin", "60% → 70% at scale", "Honasa 69.8% FY24 (S163), 71.2% FY26 (S165)"],
    ["A&amp;P, % of revenue", "50% → 38% → 30%", "Honasa 34.4% FY24 (S163); Minimalist 34% FY24 (S208), 30% FY25 (S209)"],
    ["Distribution + overheads", "25% (20–32%)", "Minimalist FY25 32% (S209)"],
    ["Digital team inside HUL", "max(₹20 Cr, 7.5% of rev.)",
     "Minimalist 7.1%, Honasa 8.9% (S209, S163); the ₹20 Cr floor is derived (Low)"],
    ["R&amp;D", "₹5 Cr + 2% of revenue", "UNCONFIRMED: neither Honasa nor Minimalist discloses R&amp;D (Low)"],
    ["Discount rate", "11.3% (10.1–13%)", "HUL's own post-tax WACC, impairment test (S134)"],
    ["Category growth", "12% (9–20%)", "BPC ~12% CAGR to 2030; serums 20%+ (Redseer in Honasa AR, S165)"],
    ["P(success)", "11% (5–29%)", "Laplace estimate on 0 of 7 FMCG digital-first builds (see below)"],
]
story += [table(assum, [100, 105, W - 205]), src("data/assumptions.csv (A01–A25), each row with a source ID and a confidence rating.")]

story.append(P(
    "<b>Probability of success: 11%.</b> Since 2020, traditional FMCG parents have launched seven digital-first brands, "
    "and none has scaled. That includes HUL's own Acne Squad and Find Your Happy Place, both withdrawn. HUL's older "
    "naturals build, Lever Ayush, has shrunk to a South India niche and has not appeared in an annual report since FY21. "
    "Seven trials cannot prove impossibility (95% interval 0–35%), so the base uses the Laplace estimate "
    "(0+1)/(7+2) = 11%; the high case, 29%, is the record of all 21 core builds. Honasa's 2 of 4 does not apply: "
    "it comes from a founder-run organisation, the capability HUL lacked and paid for."))

story.append(exhibit(4, "Base case: the build costs ₹490 Cr more than buying; the bull and bear cases bound the range"))
rows = [["₹ Cr", "Bull", "Base", "Bear"]]
for lab, k in [("PV of cash burn to scale", "pv_burn_to_scale"), ("÷ P(success) = risk-adjusted build", "risk_adjusted_build_cost"),
               ("+ Forgone profits, Y1–Y10", "forgone_profits"), ("+ Share never recovered (Y10 gap, capitalised)", "share_loss"),
               ("= Build-equivalent cost", "build_equivalent_cost"), ("Buy all-in (100%)", "buy_all_in_100pct"),
               ("Breakeven headline price for 90.5%", "breakeven_headline_price")]:
    rows.append([lab] + [cr(S[sc][k]) for sc in ["Bull", "Base", "Bear"]])
rows[2][1:] = [f"{cr(S[sc].risk_adjusted_build_cost)} (p {S[sc].p_success:.0%})" for sc in ["Bull", "Base", "Bear"]]
cw = (W - 200) / 3
scen = table(rows, [200, cw, cw, cw], bold_rows=(5, 7), right_cols=(1, 2, 3),
             extra=[("BACKGROUND", (2, 1), (2, -1), ACCENT_LT)])
story += [scen, src("data/model_outputs.csv. Bull and bear stack every driver at one end: bounds, not forecasts. "
                    "Quote the Monte Carlo P10–P90 range, "
                    f"₹{cr(MC.breakeven_P10)}–{cr(MC.breakeven_P90)} Cr (P50 ₹{cr(MC.breakeven_P50)} Cr).")]

story.append(exhibit(5, "Growth and the odds of success move the answer most; at p = 11%, building wins only within 4 years"))
grid_rows = [["P(success)"] + [f"{t} yrs" for t in range(3, 10)]]
grid_style = []
for i, p in enumerate(["0.05", "0.08", "0.11", "0.15", "0.20", "0.29"], start=1):
    g = GRID[GRID.scenario == f"p={p}"].set_index("metric").value
    vals = [g[f"breakeven_T{t}"] for t in range(3, 10)]
    grid_rows.append([f"{float(p):.0%}"] + [cr(v) for v in vals])
    for j, v in enumerate(vals, start=1):
        if v < PAID:
            grid_style.append(("BACKGROUND", (j, i), (j, i), ACCENT))
            grid_style.append(("TEXTCOLOR", (j, i), (j, i), colors.white))
gw = (W * 0.44 - 62) / 7
grid_data = [[Paragraph(c, CELL_H if i == 0 else (CELL_B if (i == 3 and j == 4) else CELL)) if j == 0 or i == 0 else c
              for j, c in enumerate(r)] for i, r in enumerate(grid_rows)]
gt = Table(grid_data, colWidths=[62] + [gw] * 7)
gt.setStyle(TableStyle([("FONT", (1, 1), (-1, -1), "Arial", 7.2), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                        ("FONT", (1, 0), (-1, 0), "Arial-Bold", 7), ("TEXTCOLOR", (1, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.4, RULE), ("BOX", (4, 3), (4, 3), 1.2, INK),
                        ("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                        ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4)] + grid_style))
grid_cap = P("Breakeven headline price, ₹ Cr, by P(success) and years from launch to ₹347 Cr. <font color='#C8102E'><b>Shaded red</b></font> = below the ₹2,706 Cr paid, "
             "so building would have won. Boxed = base case.", SRC)
tor = img("p1_tornado_memo.png", W * 0.55)
pair = Table([[tor, [gt, Spacer(1, 3), grid_cap]]], colWidths=[W * 0.555, W * 0.445])
pair.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                          ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
story += [pair, src("scripts/build_model.py. Left: one driver moved at a time. Right: workbook tab Sensitivity (live formulas).")]
story.append(P(
    f"<b>Checks.</b> Build ÷ buy = {B.build_equivalent_cost / B.buy_all_in_100pct:.2f}: neither route is obviously "
    "cheaper. The headline price was not taken at face value: the last 9.5% is booked at ₹501 Cr, 76% above pro-rata "
    "(₹284 Cr). Costing a failure at ~3 years (Acne Squad) rather than a full ramp cuts the build to "
    f"₹{cr(B.refined_build_cost)} Cr and breakeven to ₹{cr(B.refined_breakeven)} Cr, still above the price paid. "
    f"The model values the bought brand at ₹{cr(B.bought_brand_dcf_100pct)} Cr; HUL's own purchase price allocation "
    "says ₹3,504 Cr (S134). All figures are pre-tax; build losses are deductible and goodwill is not.", BODY_S))
story.append(PageBreak())

# ================================================= PAGE 3 =====================================================
story += part_head("Framework", "The framework: buy the cohort, build the channel")
story.append(P(
    "<b>Buy when a category is won on a cohort's trust and the parent is far from the channel that wins it. "
    "Build when it is won on price and reach the parent already owns.</b> Capability distance gets double weight "
    "because it is the variable that splits the record: FMCG parents' digital-first builds went <b>0 for 7</b>, while "
    "D2C-native parents went <b>2 for 4</b> in the same categories. Price is a gate, set by the model."))
story.append(exhibit(6, "Five variables, one score: S ≥ +2 means buy at up to 10.2× revenue; anything lower means build"))
fw = [
    ["Variable (weight)", "Pushes to BUY (+1)", "Pushes to BUILD (−1)", "Evidence (Tab A / Tab B / model)"],
    ["<b>V1 Demand driver</b> (×1)", "Cohort-led: leaders built online, priced ≥1.5× mass, bought on trust in an ingredient, founder or identity",
     "Distribution-led: mass price point, bought where it is stocked", "Cohort-led builds by parents far from the channel: 0 of 10 scaled. "
     "Distribution-led builds: 7 of 9 survive"],
    ["<b>V2 Capability distance</b> (×2)", "Parent has never taken a brand to ₹100 Cr in the channel that wins",
     "Parent owns that channel (GT reach, captive retail, a D2C engine)",
     "0/7 vs 2/4. GCPL's Godrej Ninja: ₹2.22 Cr in FY26 (S073); the same parent's Fab: ₹150 Cr in year 1 (S161)"],
    ["<b>V3 Time window</b> (×1)", "Independents doubled within 3–4 years", "Mature or mostly unbranded category",
     "Plix 8.1×, Yoga Bar 6.6× growth after their deals. Delay costs ₹2,456 Cr, about 2× the build (model)"],
    ["<b>V4 Price</b> (gate)", "Buy if a credible target is available at ≤10.2× revenue (100% basis)",
     "Buy only at ≤6.1× (cheaper than building)", "10.2× = ₹3,196 Cr ÷ 90.5% ÷ ₹347 Cr; 6.1× = the grid at p 29%, 4 yrs. Tab A median 4.9×; 20 of 22 priced deals at or below 10.2×"],
    ["<b>V5 Founder</b> (×1)", "Credibility sits with a founder who stays (staged deal, earn-out)",
     "Parent is itself founder-run", "Founders still run Minimalist and Dot &amp; Key; Yoga Bar, Plix and Mother Sparsh deals are staged"],
]
story.append(table(fw, [80, 125, 105, W - 310]))
rule = P("<b>Rule:</b> S = V1 + 2·V2 + V3 + V5.  <b>S ≥ +2 → BUY</b> at up to 10.2× revenue.  "
         "<b>S ≤ +1 → BUILD</b>, buying only at up to 6.1×.  During a Covid-type demand spike, do neither: "
         "both spike launches (Saffola Immuniveda and Veggie Clean) were withdrawn.", BOX)
story += [Spacer(1, 3), box([rule]), src("data/framework_scores.csv, scripts/framework.py; Tab A (31 deals) and Tab B (29 builds).")]

story.append(P("Where the line sits", H2))
story += bullets([
    "<b>Buildable: distribution, manufacturing, capital.</b> Godrej Fab reached a ~₹490 Cr run rate in year 2 (S162); "
    "Reliance's Independence ~₹2,600 Cr about three years after launch (S205); Tata Sampann ₹1,109 Cr (S154). "
    "Bought brands compound behind a parent's distribution too: Yoga Bar grew from ₹68 Cr to ₹452 Cr.",
    "<b>Buy-only: cohort credibility and founder judgement.</b> HUL built Acne Squad for Gen Z actives buyers in 2022 "
    "and withdrew it. Three years later it paid ₹2,706 Cr for Minimalist, which serves the same buyers. No FMCG "
    "digital-first build has passed ₹100 Cr. Credibility can sometimes be rented: Nykaa co-created Kay Beauty with a "
    "celebrity and reached ₹240 Cr GMV.",
])
story.append(P("When building wins", H2))
story += bullets([
    "<b>The category is distribution-led and the parent owns the channel:</b> Fab, Independence, Sampann, Bingo!, YiPPee!.",
    "<b>The parent is itself D2C-native and founder-run:</b> The Derma Co (₹750 Cr ARR), Aqualogica, Kay Beauty.",
    "<b>No credible target exists at ≤10.2×,</b> or the category is mature and delay costs little. Build, but budget for p ≈ 11%.",
])
story.append(P(
    "<b>Back-test:</b> the rule calls 39 of 50 scored rows correctly (78%): builds 20 of 27, deals 19 of 23. "
    "<b>Caveat: this is in-sample.</b> The rows were coded after their outcomes were known, so 78% is an upper bound "
    "on accuracy and a test of consistency, not of prediction.", BODY_S))
story.append(P("Two deals it does not explain", H2))
story += bullets([
    "<b>Campa (Reliance).</b> It scores −4, so the rule says build, and Campa reached ₹4,700 Cr+ in gross sales in FY26 "
    "(S205). But Reliance began by paying about ₹22 Cr (T3) for a dormant name with no revenue, team or cohort. "
    "<i>What it reveals:</i> there is a third kind of asset, latent recall, which is cheap to buy and works only with "
    "captive retail and aggressive pricing. The price gate cannot judge it, because a multiple of zero revenue is undefined.",
    "<b>HUL–Wellbeing Nutrition.</b> It scores +4, so the rule says buy, but at 18.2× revenue the gate says don't pay. "
    "HUL paid ₹70 Cr for 19.8%, never took control, and sold the stake for about ₹307 Cr in March 2026. It entered "
    "the category through OZiva instead (51% at 4.2×). <i>What it reveals:</i> the framework prices control, and it "
    "cannot see the option value of a small minority stake bought to learn a category.",
], BUL_S)
story.append(P("<b>Known blind spot:</b> incumbent concentration. Distribution-led builds failed where one brand "
               "already owned the shelf: Dabur Vita in health food drinks, Godrej Protekt in handwash.", BODY_S))
story.append(PageBreak())

# ================================================= PAGE 4 =====================================================
story += part_head("Recommendation", "Make the call: Godrej Consumer Products in pet care")
story.append(box([P("<b>BUY.</b> GCPL should buy the pet-parent channel and cohort, and keep building the food in-house. "
                    "Lead target: Heads Up For Tails, on a staged path to control.", ANSWER)], border=ACCENT))
story.append(Spacer(1, 6))
story.append(P(
    "<b>Why it scores as BUY (S = +4).</b> Demand is cohort-led (+1): ICRA sees a shift \"towards premium, gourmet and "
    "specialised pet food\" (S210). Capability distance is far (+2): GCPL has never sold through pet shops, vets or pet "
    "apps. The window is open (+1): Drools grew at a 49% CAGR to FY24 (S210), and Supertails grew 68% in FY25 (S212)."))
story.append(P(
    "<b>GCPL has already run the test.</b> Godrej Pet Care, which sells the Ninja brand, made <b>₹2.22 Cr in FY26</b>, "
    "about a year after launch, even as GCPL puts another ₹200 Cr into it (S073). The same company's Fab made ₹150 Cr in "
    "its first year (S161). "
    "GCPL's playbook works where it owns the channel, and pet care is not one of those channels."))
story.append(exhibit(7, "Three targets: HUFT is the buy, Supertails is an option, and Drools only shows the ceiling"))
tg = [
    ["Target", "Latest numbers", "Last mark", "Indicative 100%", "Why"],
    ["<b>Heads Up For Tails</b> (lead)", "₹400 Cr ARR (Dec 2025, company-stated, S214); ₹237 Cr FY25 entity revenue (S216); 90+ stores (S215)",
     "$25M Series B; valuation undisclosed (S214)", "<b>₹1,000–2,400 Cr</b> (4–6× on ₹240–400 Cr)",
     "Owns the cohort and the specialist-store channel; near break-even"],
    ["<b>Supertails</b>", "₹108.3 Cr FY25 revenue from operations, +68%; loss ₹52.5 Cr (S212)",
     "$30M (Feb 2026, S213); post-money UNCONFIRMED", "<b>₹650–1,100 Cr</b> (6–10×)",
     "The digital half of the channel. Close to the ceiling, so take a minority stake with a path to control, or wait"],
    ["<b>Drools</b> (price check)", "₹714.9 Cr FY24; ~₹915 Cr FY25 annualised (S211, S210)",
     "$600M (Jun 2023, ≈6.9× FY24); undisclosed Nestlé stake", "<b>₹6,400–9,200 Cr</b> (7–10×)",
     "Scale GCPL can build itself; Nestlé's stake makes it a contested, defensive price"],
]
story += [table(tg, [72, 140, 92, 82, W - 386]),
          src("Company statements, RoC-based press reports and ICRA (S210–S216; T1–T3, none a valuation filing). "
              "Multiples are checked against the Tab A median (4.9×) and the 10.2× ceiling.")]
story.append(P(
    "<b>Structure.</b> A staged deal to control for HUFT: start with 51% (about ₹500–1,200 Cr), with the founders on an "
    "earn-out. That keeps the price inside the Tab A band for cohort deals (Plix 6.0×, Yoga Bar 6.5×, Minimalist 8.6×)."))
story.append(P(
    "<b>The strongest argument against.</b> Pet food is a manufacturing-and-distribution business. Drools has 1,921 "
    "distributors and makes only about a quarter of its sales online (S210). Ninja is barely a year old, and Fab was "
    "loss-making at first and still worked, so GCPL should give its build time."))
story.append(P(
    "<b>My response.</b> On a comparable clock the gap is about 70× (₹2.2 Cr against ₹150 Cr), which is too large to be "
    "a matter of timing. The model shows that what makes building expensive is the delay, not the build cost. In a category "
    "compounding at 25–50% a year, every year of waiting raises the price of each target above. GCPL should keep building "
    "the food, and buy the shelf and the trust."))
story.append(P(
    "<b>Confidence: 65%.</b> It is capped because HUFT's two revenue figures conflict (₹237 Cr entity revenue against "
    "₹400 Cr ARR; see the Conflicts tab) and none of the three valuations comes from a T1 source."))
story.append(box([P("<b>What would change my mind:</b> Godrej Pet Care's FY27 revenue in GCPL's next Reg 30 filing or "
                    "annual report. A run rate above about ₹50 Cr would show that the general-trade route reaches pet "
                    "parents, and I would switch to build.", BOX)]))
story.append(PageBreak())

# ================================================= PAGE 5 =====================================================
story += part_head("Story pitch", "0 for 7: India's FMCG giants keep buying the D2C brands they couldn't build")
story.append(P(
    "<b>Summary.</b> Since 2020, HUL, Dabur, Tata Consumer and Bajaj have launched seven digital-first brands in-house. "
    "None has scaled and four are already gone, yet the same parents have paid up to ₹2,706 Cr for founder-led brands "
    "that serve the same shoppers.", BODY_S))
story.append(exhibit(8, "FMCG giants' digital-first builds went 0 for 7; the D2C-native parent went 2 for 4"))
story.append(img("pitch_chart.png", W))
story.append(src("Tracker of 71 annual reports from 11 parents (FY20–FY26), brand sites and Wayback captures; "
                 "data/tab_b.csv, data/base_rates.csv. ARR is company-stated."))
story.append(P(
    "<b>The data point nobody else has:</b> our annual-report tracker, which records when each brand stops appearing "
    "in its parent's filings and when its online store goes dark. HUL launched Acne Squad for Gen Z actives buyers in "
    "2022. Its Shopify store now returns \"store unavailable\", and three years after the launch HUL bought Minimalist.",
    BODY_S))

# AI usage note (from notes/ai_note.md) and method box, side by side
ai = [P("AI usage note", BOX_H),
      P("<b>Tools.</b> Claude Code (Opus) in VS Code for search, PDF extraction, Python and first drafts. I set the "
        "rules and the scope, and I checked every headline number against its filing.", BOX),
      P("<b>Automations.</b> A BSE API pipeline for Reg 30 filings. An annual-report tracker covering 71 annual reports "
        "from 11 parents, FY20–FY26. A fuzzy-match quote verifier (457 checks, 384 passed, 13 failures triaged by hand). "
        "A 10,000-draw Monte Carlo model.", BOX),
      P("<b>Errors caught.</b> I logged 72 figures the model recalled from memory: 28 right, 15 wrong, 10 partly right, "
        "19 never confirmed.", BOX)]
ai += bullets([
    "<b>Minimalist</b>, recalled as \"₹2,955 Cr for 90.5%\": the filing shows that figure is the pre-money EV. HUL paid ₹2,706 Cr.",
    "<b>Earth Rhythm</b>, recalled as \"Nykaa bought 51%\": the filing says 18.51% for ₹41.65 Cr.",
    "<b>Prasuma</b>, recalled as \"~₹375 Cr\": ITC's filing shows ~₹131 Cr for 43.75%.",
    "<b>My own wrong call:</b> I first coded Tata GoFit as withdrawn because it is missing from TCPL's FY26 annual report. "
    "A live store and Wayback captures show it is still sold.",
], st("bul_box", fontSize=8.6, leading=11.2, leftIndent=8, spaceAfter=1.5))
ai.append(P("<b>Left blank, not estimated:</b> consideration for 6 of 31 deals; revenue for 18 of 29 builds.", BOX))
ai.append(P("<b>Time</b> (Claude run time): setup ~16 min · Tab A 42 · Tab B 18 · verification 12+ · model 10 · "
            "framework and recommendation 12 · workbook 6. My own elapsed time was about 7h40.", BOX))

link = (f"<a href='{SHEET}' color='#C8102E'><u>{SHEET}</u></a>" if SHEET != PLACEHOLDER
        else "<font color='#c0392b'><b>[Google Sheet link to be added]</b></font>")
method = [P("Method", BOX_H),
          P("<b>Source tiers.</b> T1: exchange filings, annual reports, CCI and MCA filings, company releases. "
            "T2: call transcripts, DRHPs, press quoting officials. T3: Inc42, ET, Mint and other trade press. "
            "T4: blogs and model memory, never enough on its own. 191 of 216 sources are T1.", BOX),
          P("<b>Confidence.</b> High = T1 with a verbatim quote. Medium = T2, or two independent T3 sources that agree. "
            "Low = a single T3 source, or a derived value. Tab A: 22 of 31 rows High.", BOX),
          P("<b>Conflicts.</b> Each figure is logged with what it measures (valuation or consideration, stake or 100%, "
            "before or after adjustments), and the most authoritative source wins. Unconfirmed values are left blank "
            "and flagged, never estimated.", BOX),
          P("<b>Scope.</b> The parent had to be listed when the deal completed; core rows run from 2020. Money is in ₹ Cr, "
            "and FY24 = Apr 2023–Mar 2024.", BOX),
          P(f"<b>Workbook</b> (Tab A, Tab B, the live build model, the source log): {link}", BOX)]
cols = Table([[ai, method]], colWidths=[W * 0.55 - 4, W * 0.45 - 4], spaceBefore=4)
cols.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (-1, -1), SHADE),
                          ("BACKGROUND", (1, 0), (1, 0), ACCENT_LT), ("LEFTPADDING", (0, 0), (-1, -1), 7),
                          ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
story.append(cols)


# ---- page template -----------------------------------------------------------------------------------------
def footer(canv, doc):
    canv.saveState()
    canv.setFont("Arial", 7)
    canv.setFillColor(INK2)
    canv.drawString(LM, BM - 8, "Consumer Brands Research  ·  Buy or Build")
    canv.drawRightString(PAGE_W - RM, BM - 8, f"{doc.page} / 5")
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.4)
    canv.line(LM, BM - 2, PAGE_W - RM, BM - 2)
    canv.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
                      title="Buy or Build", author="Priyanshi Paul",
                      subject="Consumer brands research: HUL-Minimalist, buy vs build")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(LM, BM, W, PAGE_H - TM - BM, id="f", leftPadding=0,
                                                         rightPadding=0, topPadding=0, bottomPadding=0)],
                                   onPage=footer)])
doc.build(story)
print("pages:", doc.page, "->", OUT)
if SHEET == PLACEHOLDER:
    print("WARNING: Google Sheet link not set; rerun with --sheet <url>")
