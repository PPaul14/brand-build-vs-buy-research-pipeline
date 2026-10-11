"""Model: price the alternative. What would it cost HUL, risk-adjusted, to build a digital-first
active-skincare brand to Rs 347 Cr revenue, and what is the breakeven acquisition price?

Reads data/assumptions.csv (low/base/high for every driver). Writes data/model_outputs.csv and charts to
output/charts/. All money in Rs Cr, pre-tax, Y0 = decision year (FY26, the year HUL completed the deal).

  python scripts/build_model.py
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
ASSUMPTIONS = ROOT / "data" / "assumptions.csv"
OUT = ROOT / "data" / "model_outputs.csv"
CHARTS = ROOT / "output" / "charts"
YEARS = range(0, 11)
HEADLINE_PRICE = 2706.45   # S002: cash paid at completion for 90.5%
M0 = 0.035                 # S209: Minimalist FY25 EBITDA Rs 18 Cr / Rs 514.8 Cr
POST_SCALE_GROWTH = [0.48, 0.34]  # Minimalist after Rs 347 Cr: FY25 +48% (S209), FY26 +34% annualised (S134)
MARGIN_RAMP_YEARS = 5

# Direction that favours BUILD for each driver ("low" or "high"); used for Bull/Bear and the tornado.
BUILD_FAVOURABLE = {
    "years_to_scale": "low", "y1_revenue": "high", "gross_margin_early": "high", "gross_margin_scale": "high",
    "ap_pct_launch": "low", "ap_pct_growth": "low", "ap_pct_scale": "low", "var_opex_pct": "low",
    "org_cost_floor": "low", "org_cost_pct": "low", "rnd_floor": "low", "rnd_pct": "low", "wc_days": "low",
    "category_growth": "low", "p_success": "high", "steady_ebitda_margin": "low", "acquired_rev_y0": "low",
    "integration_cost": "high", "remaining_stake_cost": "high", "cash_acquired": "low",
    "discount_rate": "base", "transaction_costs": "base", "failed_attempt_years": "base",
    "terminal_growth": "base", "target_revenue": "base",
}
PCT = {"gross_margin_early", "gross_margin_scale", "ap_pct_launch", "ap_pct_growth", "ap_pct_scale",
       "var_opex_pct", "org_cost_pct", "rnd_pct", "discount_rate", "category_growth", "p_success",
       "steady_ebitda_margin", "terminal_growth"}

# Palette: validated default categorical slots (dataviz skill references/palette.md), light surface.
C_BULL, C_BASE, C_BEAR, C_REF = "#1baf7a", "#2a78d6", "#eb6834", "#52514e"
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"


def load_assumptions():
    with ASSUMPTIONS.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    a = {}
    for r in rows:
        vals = [float(r[k]) for k in ("value_low", "value_base", "value_high")]
        if r["parameter"] in PCT:
            vals = [v / 100 for v in vals]
        a[r["parameter"]] = dict(zip(("low", "base", "high"), vals))
    return a


def pick(a, level):
    return {k: v[level] for k, v in a.items()}


def scenario(a, name):
    """Bull = every operating driver at its build-favourable end; Bear = the opposite. Valuation inputs stay base."""
    if name == "Base":
        return pick(a, "base")
    v = {}
    for k, d in a.items():
        fav = BUILD_FAVOURABLE.get(k, "base")
        if fav == "base":
            v[k] = d["base"]
        elif name == "Bull":
            v[k] = d[fav]
        else:
            v[k] = d["high" if fav == "low" else "low"]
    return v


def margin_path(k, m_ss, m_start=M0):
    return m_start + (m_ss - m_start) * min(max(k, 0) / MARGIN_RAMP_YEARS, 1.0)


def build_pnl(v):
    """Y0-Y10 P&L and cash for the in-house build, conditional on success."""
    T = int(round(v["years_to_scale"]))
    target, r1, cg = v["target_revenue"], v["y1_revenue"], v["category_growth"]
    g = (target / r1) ** (1 / (T - 1))
    rows, prev_wc, cum = [], 0.0, 0.0
    for t in YEARS:
        if t == 0:
            rev = 0.0
        elif t <= T:
            rev = r1 * g ** (t - 1)
        else:
            k = t - T
            rev = rows[-1]["revenue"] * (1 + (POST_SCALE_GROWTH[k - 1] if k <= len(POST_SCALE_GROWTH) else cg))
        rnd = v["rnd_floor"] + v["rnd_pct"] * rev
        if t == 0:   # setup year: team half-staffed, formulation work, no sales
            gm = gp = mkt = var = 0.0
            org = 0.5 * v["org_cost_floor"]
            ebitda = -(org + rnd)
        elif t <= T:
            if t <= 2:
                gm, ap = v["gross_margin_early"], v["ap_pct_launch"]
            else:
                w = (t - 2) / max(T - 2, 1)
                gm = v["gross_margin_early"] + w * (v["gross_margin_scale"] - v["gross_margin_early"])
                ap = v["ap_pct_growth"]
            gp, mkt, var = gm * rev, ap * rev, v["var_opex_pct"] * rev
            org = max(v["org_cost_floor"], v["org_cost_pct"] * rev)
            ebitda = gp - mkt - var - org - rnd
        else:        # post-scale: EBITDA follows the same margin path as the bought brand; other opex is the plug
            gm = v["gross_margin_scale"]
            gp, mkt = gm * rev, v["ap_pct_scale"] * rev
            org = max(v["org_cost_floor"], v["org_cost_pct"] * rev)
            m_start = max(M0, rows[T]["ebitda"] / rows[T]["revenue"])  # never below its own margin at scale
            ebitda = margin_path(t - T, v["steady_ebitda_margin"], m_start) * rev
            var = gp - mkt - org - rnd - ebitda
        wc = v["wc_days"] / 365 * rev
        d_wc = wc - prev_wc
        prev_wc = wc
        fcf = ebitda - d_wc
        cum += fcf
        rows.append(dict(year=t, revenue=rev, gross_margin=gm, gross_profit=gp, marketing=mkt, other_opex=var,
                         rnd=rnd, org_cost=org, ebitda=ebitda, wc_investment=d_wc, cash_burn=max(-fcf, 0.0),
                         fcf=fcf, cumulative_cash=cum))
    return rows, T


def bought_path(v):
    rows = []
    for t in YEARS:
        rev = v["acquired_rev_y0"] * (1 + v["category_growth"]) ** t
        rows.append(dict(year=t, revenue=rev, ebitda=margin_path(t, v["steady_ebitda_margin"]) * rev))
    return rows


def evaluate(v):
    r = v["discount_rate"]
    pnl, T = build_pnl(v)
    bought = bought_path(v)
    df = [(1 + r) ** -t for t in YEARS]
    # Gross burn: PV of the cash-negative years up to scale (a cash-positive year does not refund earlier burn).
    pv_burn = sum(pnl[t]["cash_burn"] * df[t] for t in range(0, T + 1))
    peak_burn = -min(row["cumulative_cash"] for row in pnl)
    p = v["p_success"]
    risk_adj_build = pv_burn / p
    forgone = sum((bought[t]["ebitda"] - (pnl[t]["ebitda"] if t > T else 0.0)) * df[t] for t in YEARS if t >= 1)
    gap10 = bought[10]["revenue"] - pnl[10]["revenue"]
    share_loss = gap10 * v["steady_ebitda_margin"] / (r - v["terminal_growth"]) * df[10]
    delay = forgone + share_loss
    build_equiv = risk_adj_build + delay
    other_buy = v["remaining_stake_cost"] + v["transaction_costs"] + v["integration_cost"] - v["cash_acquired"]
    buy_all_in = HEADLINE_PRICE + other_buy
    breakeven = build_equiv - other_buy
    k = int(v["failed_attempt_years"])
    pv_fail = sum(pnl[t]["cash_burn"] * df[t] for t in range(0, k + 1))
    refined_build = pv_burn + (1 / p - 1) * pv_fail
    # Cross-check: what the bought brand is worth on these same drivers (EBITDA proxy, pre-tax, no capex).
    tv = bought[10]["ebitda"] * (1 + v["terminal_growth"]) / (r - v["terminal_growth"])
    bought_dcf = sum(bought[t]["ebitda"] * df[t] for t in YEARS if t >= 1) + tv * df[10]
    return dict(T=T, years_from_decision=T + 1, pv_burn_to_scale=pv_burn, peak_cumulative_burn=peak_burn,
                p_success=p, risk_adjusted_build_cost=risk_adj_build, forgone_profits=forgone,
                share_loss=share_loss, cost_of_delay=delay, build_equivalent_cost=build_equiv,
                other_buy_costs=other_buy, buy_all_in_100pct=buy_all_in, breakeven_headline_price=breakeven,
                headroom_vs_price=breakeven - HEADLINE_PRICE, pv_failed_attempt=pv_fail,
                refined_build_cost=refined_build, refined_breakeven=refined_build + delay - other_buy,
                y10_revenue_gap=gap10, bought_brand_dcf_100pct=bought_dcf), pnl, bought


def style(ax, title, ylabel):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", fontsize=11, color=INK, fontweight="bold")
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)
    ax.tick_params(colors=MUTED, labelsize=8.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def source_line(fig, text):
    fig.text(0.01, 0.01, text, fontsize=7, color=MUTED, ha="left", va="bottom")


def chart_paths(scen, bought):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), facecolor=SURFACE)
    ax = axes[0]
    for name, col in (("Bull", C_BULL), ("Base", C_BASE), ("Bear", C_BEAR)):
        rev = [row["revenue"] for row in scen[name][1]][1:]   # Y0 has no sales; log scale starts at Y1
        ax.plot(list(YEARS)[1:], rev, color=col, linewidth=2, marker="o", markersize=4, label=f"Build: {name}")
    ax.plot(list(YEARS), [row["revenue"] for row in bought], color=C_REF, linewidth=2, linestyle="--",
            label="Bought brand (base)")
    ax.axhline(347, color=MUTED, linewidth=1, linestyle=":")
    ax.text(10, 360, "Rs 347 Cr target", ha="right", fontsize=8, color=MUTED)
    ax.set_yscale("log")
    style(ax, "Revenue, Y0-Y10", "Rs Cr (log scale)")
    ax.set_xlabel("Year (Y0 = FY26)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1]
    for name, col in (("Bull", C_BULL), ("Base", C_BASE), ("Bear", C_BEAR)):
        ax.plot(list(YEARS), [row["cumulative_cash"] for row in scen[name][1]], color=col, linewidth=2,
                marker="o", markersize=4, label=name)
    ax.axhline(0, color=MUTED, linewidth=1)
    style(ax, "Build: cumulative cash (if it succeeds)", "Rs Cr")
    ax.set_xlabel("Year (Y0 = FY26)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    source_line(fig, "Source: scripts/build_model.py; drivers in data/assumptions.csv (Honasa AR FY24/FY26, HUL AR FY26, "
                     "Entrackr on Minimalist RoC filings).")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(CHARTS / "p1_revenue_cash_paths.png", dpi=200)
    plt.close(fig)


def chart_tornado(tornado, base_val):
    top = tornado[:6][::-1]
    fig, ax = plt.subplots(figsize=(8, 3.6), facecolor=SURFACE)
    for i, d in enumerate(top):
        lo, hi = d["at_low"] - base_val, d["at_high"] - base_val
        ax.barh(i, lo, color=C_BASE, height=0.55, left=base_val)
        ax.barh(i, hi, color=C_BEAR, height=0.55, left=base_val)
        ax.text(min(d["at_low"], d["at_high"]) - 60, i, f"{min(d['at_low'], d['at_high']):,.0f}", va="center",
                ha="right", fontsize=8, color=INK)
        ax.text(max(d["at_low"], d["at_high"]) + 60, i, f"{max(d['at_low'], d['at_high']):,.0f}", va="center",
                ha="left", fontsize=8, color=INK)
    ax.set_yticks(range(len(top)), [f"{d['label']}  ({d['range']})" for d in top], fontsize=8.5, color=INK)
    ax.axvline(base_val, color=INK, linewidth=1)
    ax.axvline(HEADLINE_PRICE, color=MUTED, linewidth=1, linestyle="--")
    ax.text(HEADLINE_PRICE, -0.75, "Paid Rs 2,706 Cr ", fontsize=8, color=MUTED, ha="right")
    lo_all = min(min(d["at_low"], d["at_high"]) for d in top)
    hi_all = max(max(d["at_low"], d["at_high"]) for d in top)
    ax.set_xlim(lo_all - 450, hi_all + 450)
    ax.set_ylim(-0.95, len(top) - 0.5)
    style(ax, f"What moves the breakeven price (base Rs {base_val:,.0f} Cr)", "")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Breakeven headline price for 90.5%, Rs Cr   (blue = driver at low value, orange = high)",
                  color=MUTED, fontsize=8.5)
    source_line(fig, "Source: scripts/build_model.py; one driver moved at a time, others at base.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(CHARTS / "p1_tornado.png", dpi=200)
    plt.close(fig)


def chart_grid(grid, ps, Ts):
    fig, ax = plt.subplots(figsize=(7.5, 3.8), facecolor=SURFACE)
    z = np.array(grid)
    im = ax.imshow(z, cmap="Blues", aspect="auto", vmin=0, vmax=np.percentile(z, 95))
    for i in range(len(ps)):
        for j in range(len(Ts)):
            val = z[i, j]
            dark = val > np.percentile(z, 60)
            ax.text(j, i, f"{val:,.0f}" + (" *" if val > HEADLINE_PRICE else ""), ha="center", va="center",
                    fontsize=7.5, color="white" if dark else INK)
    ax.set_xticks(range(len(Ts)), [f"{t} yrs" for t in Ts], fontsize=8.5)
    ax.set_yticks(range(len(ps)), [f"{p:.0%}" for p in ps], fontsize=8.5)
    ax.set_xlabel("Years from launch to Rs 347 Cr (if it succeeds)", color=MUTED, fontsize=9)
    ax.set_ylabel("P(success)", color=MUTED, fontsize=9)
    ax.set_title("Breakeven headline price for 90.5%, Rs Cr  (* = above the Rs 2,706 Cr paid)", loc="left",
                 fontsize=10.5, color=INK, fontweight="bold")
    ax.tick_params(colors=MUTED)
    fig.colorbar(im, ax=ax, fraction=0.03)
    source_line(fig, "Source: scripts/build_model.py; all other drivers at base (data/assumptions.csv).")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(CHARTS / "p1_sensitivity_grid.png", dpi=200)
    plt.close(fig)


def chart_mc(be, pcts):
    fig, ax = plt.subplots(figsize=(8, 3.4), facecolor=SURFACE)
    clipped = np.clip(be, None, np.percentile(be, 99))
    ax.hist(clipped, bins=60, color=C_BASE, edgecolor=SURFACE, linewidth=0.5)
    for lab, val in pcts.items():
        ax.axvline(val, color=INK, linewidth=1)
        ax.text(val, ax.get_ylim()[1] * 0.92, f" {lab} {val:,.0f}", fontsize=8, color=INK,
                ha="right" if lab == "P10" else "left")
    ax.axvline(HEADLINE_PRICE, color=C_BEAR, linewidth=1.5, linestyle="--")
    ax.text(HEADLINE_PRICE, ax.get_ylim()[1] * 0.60, " Paid 2,706", fontsize=8, color=INK)
    share = (be > HEADLINE_PRICE).mean()
    style(ax, f"Monte Carlo, 10,000 draws: breakeven price above the price paid in {share:.0%} of draws",
          "Draws")
    ax.set_xlabel("Breakeven headline price for 90.5%, Rs Cr (top 1% clipped)", color=MUTED, fontsize=9)
    source_line(fig, "Source: scripts/build_model.py; triangular(low, base, high) on every driver, independent draws.")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(CHARTS / "p1_monte_carlo.png", dpi=200)
    plt.close(fig)


def main():
    CHARTS.mkdir(parents=True, exist_ok=True)
    a = load_assumptions()
    out = []

    def rec(section, scen, metric, value, unit="Rs Cr", year=""):
        out.append(dict(section=section, scenario=scen, metric=metric, year=year,
                        value=round(float(value), 4), unit=unit))

    # 1. Scenarios
    scen = {}
    for name in ("Bull", "Base", "Bear"):
        v = scenario(a, name)
        res, pnl, bought = evaluate(v)
        scen[name] = (res, pnl, bought, v)
        for row in pnl:
            for m in ("revenue", "gross_profit", "marketing", "rnd", "org_cost", "other_opex", "ebitda",
                      "wc_investment", "cash_burn", "cumulative_cash"):
                rec("build_pnl", name, m, row[m], year=row["year"])
        for row in bought:
            rec("bought_path", name, "revenue", row["revenue"], year=row["year"])
            rec("bought_path", name, "ebitda", row["ebitda"], year=row["year"])
        for m, val in res.items():
            unit = "years" if m in ("T", "years_from_decision") else ("ratio" if m == "p_success" else "Rs Cr")
            rec("summary", name, m, val, unit)

    # 2. Tornado on breakeven headline price (one driver at a time)
    base_v = pick(a, "base")
    base_be = evaluate(base_v)[0]["breakeven_headline_price"]
    labels = {"years_to_scale": "Years to scale", "p_success": "P(success)", "discount_rate": "Discount rate",
              "category_growth": "Category growth", "steady_ebitda_margin": "Steady EBITDA margin",
              "ap_pct_growth": "A&P % (growth)", "ap_pct_launch": "A&P % (launch)",
              "gross_margin_scale": "Gross margin (scale)", "org_cost_floor": "Org cost floor",
              "var_opex_pct": "Distribution & overheads %", "y1_revenue": "Year-1 revenue",
              "wc_days": "Working capital days", "remaining_stake_cost": "Cost of last 9.5%",
              "integration_cost": "Integration cost", "acquired_rev_y0": "Minimalist FY26 revenue",
              "rnd_floor": "R&D floor", "gross_margin_early": "Gross margin (early)", "ap_pct_scale": "A&P % (scale)",
              "org_cost_pct": "Org cost %", "rnd_pct": "R&D %", "cash_acquired": "Cash acquired"}
    tornado = []
    for k, lab in labels.items():
        lo, hi = dict(base_v), dict(base_v)
        lo[k], hi[k] = a[k]["low"], a[k]["high"]
        at_lo = evaluate(lo)[0]["breakeven_headline_price"]
        at_hi = evaluate(hi)[0]["breakeven_headline_price"]
        fmt = (lambda x: f"{x:.0%}" if x < 1 else f"{x:.1%}") if k in PCT else (lambda x: f"{x:g}")
        tornado.append(dict(key=k, label=lab, at_low=at_lo, at_high=at_hi, swing=abs(at_hi - at_lo),
                            range=f"{fmt(a[k]['low'])} to {fmt(a[k]['high'])}"))
    tornado.sort(key=lambda d: -d["swing"])
    for d in tornado:
        rec("tornado", "Base", f"{d['key']}_at_low", d["at_low"])
        rec("tornado", "Base", f"{d['key']}_at_high", d["at_high"])
        rec("tornado", "Base", f"{d['key']}_swing", d["swing"])

    # 3. Sensitivity grid: p x years-to-scale
    ps = [0.05, 0.08, 0.11, 0.15, 0.20, 0.29]
    Ts = [3, 4, 5, 6, 7, 8, 9]
    grid = []
    for p in ps:
        line = []
        for T in Ts:
            v = dict(base_v, p_success=p, years_to_scale=T)
            be = evaluate(v)[0]["breakeven_headline_price"]
            line.append(be)
            rec("sensitivity_grid", f"p={p:.2f}", f"breakeven_T{T}", be)
        grid.append(line)

    # 4. Monte Carlo
    rng = np.random.default_rng(42)
    N = 10_000
    draws = {k: rng.triangular(d["low"], d["base"], d["high"], N) if d["high"] > d["low"] else np.full(N, d["base"])
             for k, d in a.items()}
    draws["years_to_scale"] = np.rint(draws["years_to_scale"])
    be, ra, delay = np.empty(N), np.empty(N), np.empty(N)
    for i in range(N):
        res = evaluate({k: float(draws[k][i]) for k in a})[0]
        be[i], ra[i], delay[i] = res["breakeven_headline_price"], res["risk_adjusted_build_cost"], res["cost_of_delay"]
    pcts = {f"P{q}": float(np.percentile(be, q)) for q in (10, 50, 90)}
    for lab, val in pcts.items():
        rec("monte_carlo", "MC", f"breakeven_{lab}", val)
    for q in (10, 50, 90):
        rec("monte_carlo", "MC", f"risk_adjusted_build_P{q}", np.percentile(ra, q))
        rec("monte_carlo", "MC", f"cost_of_delay_P{q}", np.percentile(delay, q))
    rec("monte_carlo", "MC", "share_breakeven_above_price", (be > HEADLINE_PRICE).mean(), "ratio")
    rec("monte_carlo", "MC", "n_draws", N, "count")

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["section", "scenario", "metric", "year", "value", "unit"])
        w.writeheader()
        w.writerows(out)

    chart_paths({k: (s[0], s[1]) for k, s in scen.items()}, scen["Base"][2])
    chart_tornado(tornado, base_be)
    chart_grid(grid, ps, Ts)
    chart_mc(be, pcts)

    # 5. Console summary + sanity check required by the study design
    print(f"{'':28}" + "".join(f"{n:>10}" for n in scen))
    for m in ("T", "years_from_decision", "pv_burn_to_scale", "peak_cumulative_burn", "risk_adjusted_build_cost",
              "forgone_profits", "share_loss", "cost_of_delay", "build_equivalent_cost", "other_buy_costs",
              "buy_all_in_100pct", "breakeven_headline_price", "headroom_vs_price", "refined_build_cost",
              "refined_breakeven"):
        print(f"{m:28}" + "".join(f"{scen[n][0][m]:>10,.0f}" for n in scen))
    print("MC breakeven:", {k: round(v) for k, v in pcts.items()}, f"share above price {(be > HEADLINE_PRICE).mean():.0%}")
    print("Top tornado:", [(d["label"], round(d["at_low"]), round(d["at_high"])) for d in tornado[:6]])
    # Rule: build obviously cheaper -> re-check failure and time; buy obviously cheaper -> re-check headline price.
    b = scen["Base"][0]
    ratio = b["build_equivalent_cost"] / b["buy_all_in_100pct"]
    print(f"SANITY: build-equivalent / buy all-in = {ratio:.2f} (base)")
    if ratio < 0.67:
        print("  -> build looks obviously cheaper: re-check p(success) and years-to-scale.")
    elif ratio > 1.5:
        print("  -> buy looks obviously cheaper: re-check the headline price (use all-in, not Rs 2,706 Cr alone).")
    else:
        print("  -> neither obviously cheaper; conclusion rests on the drivers in the tornado.")
    print(f"SANITY: bought-brand DCF on model drivers = {b['bought_brand_dcf_100pct']:,.0f} vs HUL PPA brand "
          f"Rs 2,874 Cr + goodwill Rs 630 Cr (S134 Note 43)")
    rec_ratio = ratio
    return rec_ratio


if __name__ == "__main__":
    main()
