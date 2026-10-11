"""Build base rates from data/tab_b.csv -> data/base_rates.csv.

  python scripts/base_rates.py

Success = status_today 'Scaled'. 'Stable' (alive, no size disclosed, often a pivot) is NOT a success; the
'rate_if_stable_counts' column shows the more generous reading. Only core rows (year_start >= 2020) are used.
Wilson 95% interval given because every denominator is small.
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "base_rates.csv"
AS_OF = 2026  # 2026-10-10
D2C_NATIVE = ("Honasa", "FSN E-Commerce")

# Digital-first = the parent itself called the launch digital-first / e-commerce-first (evidence in tab_b notes/status_evidence).
DIGITAL_FIRST = {
    "Acne Squad": "'Digital-first acne brand' (HUL AR FY23, Agile Innovation Hub; D2C Shopify store)",
    "Find Your Happy Place": "'crafted for digital consumers' (HUL AR FY23; D2C Shopify store)",
    "Tata GoFit": "TCPL AR FY24 p.45 calls it a 'digital brand'; D2C store",
    "Bajaj Zero Grey": "sold 'primarily for E-commerce' (Bajaj AR)",
    "Natyv Soul": "'Launched two digital first brands: Bajaj 100% Pure and Natyv Soul' (Bajaj AR FY22 p.5)",
    "Bajaj 100% Pure": "same AR FY22 line; later taken to all channels",
    "Dabur Vita": "BORDERLINE: launched on e-commerce with Flipkart (S117); not called 'digital-first' by Dabur",
}
# Launched in calendar 2023 but on/before 2026-10-10 minus 3 years only if the month is known
AGE_OK_2023 = {"Novology": "launched Jan-Mar 2023 (AR FY23)", "Campa": "relaunched in FY23, i.e. by Mar 2023 (RIL AR FY23)"}


def wilson(k, n, z=1.96):
    if n == 0:
        return ""
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return f"{max(0, (c - h) / d):.0%}-{min(1, (c + h) / d):.0%}"


def short(b):
    return b.split(" (")[0]


def main():
    rows = [r for r in csv.DictReader((ROOT / "data" / "tab_b.csv").open(encoding="utf-8")) if r["row_type"] == "core"]
    old_enough = lambda r: int(r["year_start"]) <= AS_OF - 4 or any(r["brand"].startswith(k) for k in AGE_OK_2023)
    trad = lambda r: not r["parent"].startswith(D2C_NATIVE)
    digital = lambda r: any(r["brand"].startswith(k) for k in DIGITAL_FIRST)
    defs = [
        ("a) all core builds (year_start >= 2020), no exclusions", lambda r: True,
         "Raw rate. Includes out-of-scope (Fab, Veggie Clean, Ninja, Nykd), captive (Independence), hybrid (Campa) and Unclear rows; Unclear counted as not scaled."),
        ("b) core builds at least 3 years old (launched on/before 2023-10-10)", old_enough,
         "year_start <= 2022, plus 2023 launches whose month is known to be early: " + "; ".join(f"{k}: {v}" for k, v in AGE_OK_2023.items())
         + ". Dropped as too young or undatable: Staze (2024), Godrej Fab (2024), Godrej Ninja (2025), I'mlite (FY24, month UNCONFIRMED). No other exclusions."),
        ("c) traditional FMCG parents, base_rate_flag = included, digital-first builds only",
         lambda r: trad(r) and r["base_rate_flag"] == "included" and digital(r),
         "Traditional = all parents except Honasa and Nykaa. Excludes out-of-scope, captive-channel, hybrid and unclear rows. Digital-first evidence: "
         + "; ".join(f"{k}: {v}" for k, v in DIGITAL_FIRST.items())
         + ". Excluding borderline Dabur Vita: 0/6. All 9 included traditional core builds (adding Immuniveda, Simply Better): 0/9."),
        ("d) D2C-native parents (Honasa, Nykaa), base_rate_flag = included",
         lambda r: not trad(r) and r["base_rate_flag"] == "included",
         "Nykd (apparel, out of scope; Scaled on GMV) excluded; with it: 3/5. CAVEATS: The Derma Co and Aqualogica were built pre-IPO (unlisted parent); "
         "both 'Scaled' figures are company-stated ARR, not audited revenue (Aqualogica's ARR is a joint figure with Dr. Sheth's, Medium); Staze is only ~2.5 years old."),
    ]
    out = []
    for name, pred, note in defs:
        sel = [r for r in rows if pred(r)]
        k = sum(r["status_today"] == "Scaled" for r in sel)
        ks = sum(r["status_today"] in ("Scaled", "Stable") for r in sel)
        n = len(sel)
        out.append(dict(definition=name, numerator=k, denominator=n, rate=f"{k / n:.0%}" if n else "",
                        wilson_95=wilson(k, n), rate_if_stable_counts=f"{ks}/{n} = {ks / n:.0%}" if n else "",
                        rows_included="; ".join(f"{short(r['brand'])} [{r['status_today']}]" for r in sel),
                        notes="Success = status_today Scaled. " + note))
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for o in out:
        print(f"{o['definition'][:70]:70} {o['numerator']}/{o['denominator']} = {o['rate']} (95% {o['wilson_95']}); +Stable {o['rate_if_stable_counts']}")
        print("   ", o["rows_included"])


if __name__ == "__main__":
    main()
