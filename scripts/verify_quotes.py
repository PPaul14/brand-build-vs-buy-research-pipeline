"""Check that every quote and every headline number in tab_a.csv / tab_b.csv appears in the saved source text.

  .venv/Scripts/python scripts/verify_quotes.py

Quotes: any '...' span in status_evidence, notes, vocab_rationale or revenue_basis (3+ words). Each quote is tested
against the source it is attributed to (the last S### cited before it in the same field); if there is none, or it
fails there, against every other source in the row's source_ids. Quotes split on '...' are checked fragment by fragment.
Numbers: consideration_inr_cr, stake_pct, revenue_inr_cr, searched in the row's sources in common print formats.

Match = rapidfuzz partial_ratio >= 90 on normalised text (lower case, unified quotes/dashes, collapsed whitespace).
Result values: PASS | PASS_DERIVED (number = full-rupee amount in Cr, or a difference of two stake %) | PASS_OTHER_SOURCE (found, but not in the source it is attributed to) | FAIL | NO_TEXT (source
has no saved text, e.g. a 403) | SKIPPED_SHORT. page_cited vs page_found compares 'p.N' with the '=== PAGE N ===' marker.
Output: data/verification_report.csv
"""
import csv
import re
from pathlib import Path

from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "sources" / "raw"
OUT = ROOT / "data" / "verification_report.csv"
THRESHOLD = 90
QUOTE_FIELDS = ["status_evidence", "notes", "vocab_rationale", "revenue_basis"]
NUM_FIELDS = ["consideration_inr_cr", "stake_pct", "revenue_inr_cr"]
COLS = ["tab", "row", "brand", "confidence", "check", "field", "source_id", "page_cited", "page_found", "item",
        "score", "result", "best_match", "triage"]

QUOTE_RE = re.compile(r"(?<![\w])'((?:[^']|(?<=\w)'(?=\w))+?)'(?!\w)")
SID_RE = re.compile(r"\bS(\d{3})\b")


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("₹", "rs ").replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip().lower()
    # currency tokens: INR / Rs. / extracted rupee glyph (` or h glued to the number) -> 'rs ' (a labelling artefact, not a value)
    return re.sub(r"(?<![a-z0-9])(?:inr|rs\.?|`|h)\s*(?=\d)", "rs ", s)


def load_sources():
    """source_id -> list of (page_no, normalised page text)."""
    log = list(csv.DictReader((ROOT / "data" / "source_log.csv").open(encoding="utf-8")))
    paths = {}
    for f in RAW.glob("S[0-9][0-9][0-9]_*.txt"):
        paths[f.name[:4]] = f
    for r in log:
        m = re.search(r"text: (sources/raw/\S+\.txt)", r.get("notes", ""))
        if m:
            paths.setdefault(r["source_id"], ROOT / m.group(1))
    out = {}
    for sid, p in paths.items():
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        parts = re.split(r"=== PAGE (\d+) ===", txt)
        pages = [(None, norm(parts[0]))] + [(int(parts[i]), norm(parts[i + 1])) for i in range(1, len(parts) - 1, 2)]
        out[sid] = [(n, t) for n, t in pages if t]
    return out


SRC = load_sources()


def best_in(sid, needle):
    """(score, page, snippet) of the best match of needle in source sid; None if no text."""
    if sid not in SRC:
        return None
    best = (0, None, "")
    for page, text in SRC[sid]:
        if needle in text:
            i = text.index(needle)
            return 100.0, page, text[max(0, i - 20): i + len(needle) + 20]
    for page, text in SRC[sid]:
        a = fuzz.partial_ratio_alignment(needle, text, score_cutoff=best[0])
        if a and a.score > best[0]:
            best = (a.score, page, text[a.dest_start: a.dest_end])
            if a.score == 100:
                break
    return best


def check(item, attributed, others):
    """Try the attributed source(s) first, then the rest. Returns (result, sid, score, page, snippet)."""
    tried, last = [], (0, None, "")
    primary = attributed[0] if attributed else ""
    order = attributed + [s for s in others if s not in attributed]
    for k, sid in enumerate(order):
        r = best_in(sid, item)
        if r is None:
            continue
        tried.append(sid)
        if r[0] >= THRESHOLD:
            res = "PASS" if (k < len(attributed) or not attributed) else "PASS_OTHER_SOURCE"
            return res, sid, r[0], r[1], r[2]
        if r[0] >= last[0]:
            last = r
            last_sid = sid
    if not tried:
        return "NO_TEXT", primary or ";".join(others), "", None, ""
    return "FAIL", primary if primary in tried else last_sid, last[0], last[1], last[2]


def num_variants(v):
    x = float(v)
    vs = {v, f"{x:g}", f"{x:.2f}", f"{x:.1f}", f"{x:,.2f}", f"{x:,g}"}
    if x == int(x):
        vs |= {str(int(x)), f"{int(x):,}"}
    ip, _, fp = f"{x:.2f}".partition(".")  # Indian grouping 1,23,456.78
    if len(ip) > 3:
        head, tail = ip[:-3], ip[-3:]
        head = ",".join(re.findall(r"\d{1,2}(?=(?:\d{2})*$)", head))
        vs |= {f"{head},{tail}.{fp}", f"{head},{tail}"}
    return {s for s in vs if s}


def num_check(v, sids):
    pats = [re.compile(r"(?<![\d.,])" + re.escape(s) + r"(?![\d]|\.\d)") for s in sorted(num_variants(v), key=len, reverse=True)]
    no_text = True
    for sid in sids:
        if sid not in SRC:
            continue
        no_text = False
        for page, text in SRC[sid]:
            for p in pats:
                m = p.search(text)
                if m:
                    return "PASS", sid, 100, page, text[max(0, m.start() - 40): m.end() + 40]
    if no_text:
        return "NO_TEXT", ";".join(sids), "", None, ""
    return derived_check(v, sids)


RUPEE_RE = re.compile(r"(?<![\d,.])\d{1,3}(?:,\d{2,3}){2,}(?![\d,])")  # 78,49,85,170 / 2,706,44,95,728 (full rupees)
PCT_RE = re.compile(r"(\d{1,3}(?:\.\d{1,2})?)\s?%")


def derived_check(v, sids):
    """PASS_DERIVED if v = a full-rupee amount in crore, or the difference of two stake % in one source."""
    x = float(v)
    dec = len(v.partition(".")[2])
    for sid in sids:
        for page, text in SRC.get(sid, []):
            for m in RUPEE_RE.finditer(text):
                cr = int(m.group().replace(",", "")) / 1e7
                if cr >= 1 and round(cr, dec) == x:
                    return "PASS_DERIVED", sid, 100, page, f"{m.group()} rupees = {cr:.4f} Cr"
            pcts = sorted({float(q) for q in PCT_RE.findall(text) if float(q) <= 100})
            for a in pcts:
                if any(abs((b - a) - x) < 0.006 for b in pcts if b > a):
                    b = next(b for b in pcts if b > a and abs((b - a) - x) < 0.006)
                    return "PASS_DERIVED", sid, 100, page, f"{b}% - {a}% = {x}"
    return "FAIL", ";".join(sids), "", None, ""


# Manual triage of the checks the script cannot clear (verification pass 2026-10-10). (tab, brand prefix, item prefix) -> note
TRIAGE = {
    ("tab_a", "Minimalist", "~347 cr turnover"): "NOT A SOURCE QUOTE: label from the D5 instruction; 347 itself PASSES the number check (S007)",
    ("tab_a", "Earth Rhythm", "nykaa acquired 51%"): "NOT A SOURCE QUOTE: the AI recall being refuted (C023)",
    ("tab_a", "Dermicool", "rs 113 crore"): "Search snippet, explicitly UNCONFIRMED in notes and not used as a value",
    ("tab_a", "Dot & Key", "~rs 46.9 cr"): "Search snippet attributed to the RHP; explicitly UNCONFIRMED, consideration left blank",
    ("tab_a", "True Elements", "marico acquires 100%"): "T3 headline not saved; quoted only to show it is wrong; not relied on",
    ("tab_a", "Brillare", "stake would be 66.29%"): "Source filing not saved; notes now mark the quote UNCONFIRMED; not a headline value",
    ("tab_a", "Park Avenue", "100"): "Slump sale of the whole FMCG business: 100% implicit, no % printed",
    ("tab_a", "Dermicool", "100"): "Brand/trademark purchase: 100% implicit, no % printed",
    ("tab_a", "Ching's Secret", "3825"): "DERIVED 75% x EV INR 5,100 Cr (S036); documented in notes; Low",
    ("tab_a", "Sesa", "320"): "DERIVED midpoint of EV range INR 315-325 Cr (S067); documented; Low",
    ("tab_a", "Muuchstac", "449"): "DERIVED 289 + ~160 tranches (S071); documented; Low",
    ("tab_b", "Lever Ayush", "hul may pull out"): "T4 report, explicitly UNCONFIRMED in notes",
    ("tab_b", "Godrej Protekt", "rs 500 crore brand"): "T3 search snippet, flagged as not saved in notes; not used as a value",
}


def triage(tab, brand, item):
    return next((v for (t, b, i), v in TRIAGE.items() if t == tab and brand.startswith(b) and item.startswith(i)), "")


def quotes_with_sid(field_text):
    for m in QUOTE_RE.finditer(field_text):
        before = field_text[: m.start()]
        sids = SID_RE.findall(before)
        attributed = [f"S{sids[-1]}"] if sids else []  # "S007 p.3: '...'" (or the last source named earlier)
        after = SID_RE.search(field_text[m.end(): m.end() + 25])  # "'...' (S015 p.2)"
        if after and f"S{after.group(1)}" not in attributed:
            attributed.append(f"S{after.group(1)}")
        pm = re.findall(r"S\d{3}\s*p\.?\s*(\d+)", before[-60:]) if sids else []
        yield m.group(1), attributed, (pm[-1] if pm else "")


def main():
    rows_out = []
    for tab in ["tab_a", "tab_b"]:
        for i, r in enumerate(csv.DictReader((ROOT / "data" / f"{tab}.csv").open(encoding="utf-8"))):
            sids = [s.strip() for s in r["source_ids"].split(";") if s.strip()]
            base = dict(tab=tab, row=i, brand=r["brand"], confidence=r["confidence"])
            for f in NUM_FIELDS:
                if r.get(f):
                    res, sid, sc, pg, snip = num_check(r[f], sids)
                    rows_out.append(dict(base, check="number", field=f, source_id=sid, page_cited="", page_found=pg or "",
                                         item=r[f], score=sc, result=res, best_match=snip))
            for f in QUOTE_FIELDS:
                for q, attributed, pcited in quotes_with_sid(r.get(f, "")):
                    sid = attributed[0] if attributed else ""
                    for frag in re.split(r"\.\.\.|…", q):
                        frag = norm(frag).strip(" .,;:")
                        if len(frag.split()) < 3:
                            res, s2, sc, pg, snip = "SKIPPED_SHORT", sid, "", None, ""
                        else:
                            res, s2, sc, pg, snip = check(frag, attributed, sids)
                        rows_out.append(dict(base, check="quote", field=f, source_id=s2, page_cited=pcited,
                                             page_found=pg or "", item=frag, score=round(sc, 1) if sc != "" else "",
                                             result=res, best_match=snip))
    for x in rows_out:
        x["triage"] = triage(x["tab"], x["brand"], x["item"]) if x["result"] in ("FAIL", "NO_TEXT") else ""
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows_out)
    from collections import Counter
    print(Counter((x["check"], x["result"]) for x in rows_out))
    print(f"{len(rows_out)} checks -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
