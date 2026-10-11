"""Logic checks on tab_a.csv / tab_b.csv. Writes data/logic_checks.csv (tab, row, brand, check, severity, detail).

  python scripts/logic_checks.py

ERROR = breaks an evidence rule; WARN = allowed but worth a second look; the memo should not rely on an ERROR row.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "logic_checks.csv"
VOCAB = {}
for v in csv.DictReader((ROOT / "data" / "vocabulary.csv").open(encoding="utf-8")):
    VOCAB.setdefault(v["field"], set()).add(v["value"])
STATUS = {"Scaled", "Stable", "Niche", "Withdrawn", "Unclear"}
YEAR_MIN, YEAR_MAX = 1990, 2026
MULT_HI, MULT_LO = 25, 0.5


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def checks(tab, r):
    buy = r["route"] == "Buy"
    out = []
    add = lambda c, s, d: out.append((c, s, d))
    # vocabulary / taxonomy
    if r["category"] not in VOCAB["category"]:
        add("category", "ERROR", f"'{r['category']}' not in taxonomy")
    if r["what_was_acquired"] not in VOCAB["what_was_acquired"]:
        add("what_was_acquired", "ERROR", f"'{r['what_was_acquired']}' not in vocabulary")
    if not r["vocab_rationale"].strip():
        add("vocab_rationale", "ERROR", "missing")
    if r["row_type"] not in VOCAB["row_type"]:
        add("row_type", "ERROR", f"'{r['row_type']}'")
    if r["confidence"] not in {"High", "Medium", "Low"}:
        add("confidence", "ERROR", f"'{r['confidence']}'")
    # years
    y = f(r["year_start"])
    if y is None:
        add("year_start", "ERROR" if r["row_type"] == "core" else "WARN", "missing")
    else:
        if not YEAR_MIN <= y <= YEAR_MAX:
            add("year_start", "ERROR", f"{y:.0f} outside {YEAR_MIN}-{YEAR_MAX}")
        if r["row_type"] == "core" and y < 2020:
            add("year_start", "ERROR", f"core row with year_start {y:.0f} < 2020 (D2)")
        if r["row_type"] == "calibration" and y >= 2020:
            add("year_start", "WARN", f"calibration row with year_start {y:.0f} >= 2020")
    if r["revenue_inr_cr"] and not r["revenue_fy"]:
        add("revenue_fy", "ERROR", "revenue without FY")
    if r["revenue_inr_cr"] and not r["revenue_basis"]:
        add("revenue_basis", "ERROR", "revenue without basis (D5)")
    if buy:
        stake, cons, rev, mult = f(r["stake_pct"]), f(r["consideration_inr_cr"]), f(r["revenue_inr_cr"]), f(r["revenue_multiple"])
        if r["deal_structure"] not in VOCAB["deal_structure"]:
            add("deal_structure", "ERROR", f"'{r['deal_structure']}' not in vocabulary")
        if stake is None:
            add("stake_pct", "WARN", "missing (multiple cannot be computed)")
        elif not 0 < stake <= 100:
            add("stake_pct", "ERROR", f"{stake} outside (0, 100]")
        if stake is not None and r["deal_structure"] == "full_100" and stake < 100:
            add("deal_structure", "WARN", f"full_100 but stake_pct {stake} (row records the tranche that took the parent to 100%; prior stake held earlier)")
        if stake is not None and r["deal_structure"] in ("minority_no_path", "minority_with_path") and stake > 50:
            add("deal_structure", "ERROR", f"minority structure but stake_pct {stake}")
        if stake is not None and r["deal_structure"] == "outright_majority" and stake <= 50:
            if "incremental" in r["notes"]:  # control step: stake_pct is the increment, the holding after it is >50%
                add("deal_structure", "WARN", f"outright_majority with incremental stake_pct {stake}; check the post-step holding in notes")
            else:
                add("deal_structure", "ERROR", f"outright_majority but stake_pct {stake}")
        if stake is not None and r["deal_structure"] == "staged_to_control" and stake > 50:
            add("deal_structure", "WARN", f"staged_to_control but stake_pct {stake}: stake_pct sums all tranches, not the first one")
        if cons and stake and rev:
            calc = cons / (stake / 100) / rev
            if mult is None or abs(calc - mult) > 0.01:
                add("revenue_multiple", "ERROR", f"stored {r['revenue_multiple']} vs computed {calc:.2f}")
            if calc > MULT_HI or calc < MULT_LO:
                add("revenue_multiple", "WARN", f"{calc:.2f}x outside {MULT_LO}-{MULT_HI}x")
        elif mult is not None:
            add("revenue_multiple", "ERROR", "multiple present but an input is missing")
    else:
        for c in ("consideration_inr_cr", "stake_pct", "deal_structure", "revenue_multiple"):
            if r.get(c):
                add(c, "ERROR", "must be blank for Build rows")
        if r["status_today"] not in STATUS:
            add("status_today", "ERROR", f"'{r['status_today']}'")
        if r.get("base_rate_flag") not in VOCAB["base_rate_flag"]:
            add("base_rate_flag", "ERROR", f"'{r.get('base_rate_flag')}'")
        basis = r["revenue_basis"].lower()
        if r["status_today"] == "Scaled" and any(k in basis for k in ("gmv", "consumer spend", "gross sales")):
            add("status_today", "WARN", f"Scaled on a non-revenue measure ({r['revenue_basis'][:40]})")
    return out


def main():
    rows = []
    for tab in ("tab_a", "tab_b"):
        for i, r in enumerate(csv.DictReader((ROOT / "data" / f"{tab}.csv").open(encoding="utf-8"))):
            for c, s, d in checks(tab, r):
                rows.append(dict(tab=tab, row=i, brand=r["brand"], check=c, severity=s, detail=d))
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["tab", "row", "brand", "check", "severity", "detail"])
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['severity']:5} {r['tab']} {r['row']:>2} {r['brand'][:34]:34} {r['check']:18} {r['detail']}")
    print(f"{len(rows)} findings -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
