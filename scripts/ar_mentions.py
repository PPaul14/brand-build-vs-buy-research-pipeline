"""Annual-report mention tracker for Tab B brands.

  python -I scripts/ar_mentions.py download [--parents HUL ITC ...]   # fetch ARs FY20-FY26 from the BSE API (cached)
  python -I scripts/ar_mentions.py count                              # count brand mentions -> data/ar_mentions.csv

Annual reports come from the BSE AnnualReport_New API (Year N = the FY N report, e.g. 2025 = FY2024-25,
filed mid-2025). PDFs are cached in sources/pdf/ar/, page-marked text in sources/raw/ar/. Each report that
downloads is registered once in data/source_log.csv as a T1 source. Failed downloads are skipped and recorded
as status=failed (nothing is bypassed). FY26 is included because it was available on 2026-10-10.

Counting: a regex per brand (word-bounded; case-sensitive where the brand name is a common word), counted
over all pages. One sample sentence (first hit, preferring a page that is not an index/brand list) is saved.
A brand that stops appearing in its parent's report is a signal, not proof, of de-prioritisation.
"""
import argparse
import csv
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fetch import read_log, next_source_id, append_log, pdf_to_text  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
PDF_DIR = ROOT / "sources" / "pdf" / "ar"
TXT_DIR = ROOT / "sources" / "raw" / "ar"
OUT = ROOT / "data" / "ar_mentions.csv"
API = "https://api.bseindia.com/BseIndiaAPI/api/AnnualReport_New/w"
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bseindia.com/", "Accept": "application/json"}
FYS = range(2020, 2027)

PARENTS = {  # short code: (BSE scrip, legal name)
    "HUL": (500696, "Hindustan Unilever Ltd"),
    "ITC": (500875, "ITC Ltd"),
    "Marico": (531642, "Marico Ltd"),
    "TCPL": (500800, "Tata Consumer Products Ltd"),
    "GCPL": (532424, "Godrej Consumer Products Ltd"),
    "Dabur": (500096, "Dabur India Ltd"),
    "Emami": (531162, "Emami Ltd"),
    "Zydus": (531335, "Zydus Wellness Ltd"),
    "Bajaj": (533229, "Bajaj Consumer Care Ltd"),
    "Nykaa": (543384, "FSN E-Commerce Ventures Ltd (Nykaa)"),
    "Honasa": (544014, "Honasa Consumer Ltd"),
    "RIL": (500325, "Reliance Industries Ltd"),
}

I = re.I
# parent -> {brand label: (pattern, flags)}. flags=0 means case-sensitive.
BRANDS = {
    "HUL": {"Lever Ayush": (r"(?<!Ministry of )\b(?:LEVER |Lever )?Ayush\b", 0),  # case-sensitive: skips 'AYUSH' ministry
            "Love Beauty & Planet": (r"Love,?\s*Beauty\s*(?:&|and)\s*Planet", I),
            "Acne Squad": (r"Acne Squad", I), "Find Your Happy Place": (r"Find Your Happy Place", I),
            "Novology": (r"\bNovology\b", I)},
    "ITC": {"Bingo!": (r"\bBingo\b", I), "Sunfeast YiPPee!": (r"\bYi[pP]{2}[eE]{2}\b", 0),
            "Fabelle": (r"\bFabelle\b", I)},
    "Marico": {"Saffola Immuniveda": (r"Immuniveda", I), "Veggie Clean": (r"Veggie Clean", I)},
    "TCPL": {"Tata Sampann": (r"\bSampann\b", I), "Tata Simply Better": (r"Simply Better", I),
             "Tata GoFit": (r"\bGo\s?Fit\b", I)},
    "GCPL": {"Godrej Ninja / Pet Care": (r"\bpet\s?care\b|\bpet food|\bNinja\b", I), "Godrej Protekt": (r"\bProtekt\b", I),
             "Godrej Fab": (r"\bGodrej Fab\b|\bFab\b(?=[^.]{0,80}(?:liquid|detergent|Liquid|Detergent|launch|South|topline|run rate))", 0)},
    "Dabur": {"Dabur Vita": (r"Dabur Vita\b|\bVita (?:Immune|Health)", 0)},
    "Honasa": {"The Derma Co": (r"\bDerma Co\b", I), "Aqualogica": (r"Aqualogica", I),
               "Staze": (r"\bStaze\b", I), "Ayuga": (r"\bAyuga\b", I)},
    "Nykaa": {"Kay Beauty": (r"Kay Beauty", I), "Nykd": (r"\bNykd\b", I)},
    "Bajaj": {"Bajaj Zero Grey": (r"Zero Grey", I), "Natyv Soul": (r"Natyv\s?Soul", I),
              "Bajaj 100% Pure": (r"100% Pure", I)},
    "Zydus": {"I'mlite": (r"I.?m\s?lite\b", I)},
    "RIL": {"Campa": (r"\bCampa\b", I),
            # case-sensitive + brand context, so auditor/director 'independence' and 'Independence Day' are not counted
            "Independence": (r"(?:‘|'|\")Independence(?:’|'|\")|\bIndependence(?= brand)|(?<=Campa and )Independence|(?<=Campa, )Independence|INDEPENDENCE(?= brand)", 0)},
}


def ar_list(scrip):
    t = requests.get(API, params={"scripcode": scrip}, headers=HDR, timeout=30).json().get("Table", [])
    best = {}
    for x in t:
        y = int(x["Year"])
        if y in FYS and x.get("PDFDownload") and (y not in best or (x.get("Fld_AuthoriseDate") or "") > (best[y].get("Fld_AuthoriseDate") or "")):
            best[y] = x
    return {y: best[y]["PDFDownload"].replace("\\", "") for y in best}


def get_one(code, fy, url):
    pdf, txt = PDF_DIR / f"{code}_FY{fy % 100}.pdf", TXT_DIR / f"{code}_FY{fy % 100}.txt"
    if txt.exists():
        return code, fy, url, "cached"
    try:
        if not pdf.exists():
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.bseindia.com/"}, timeout=300)
            r.raise_for_status()
            if r.content[:5] != b"%PDF-":
                return code, fy, url, "failed: not a PDF"
            pdf.write_bytes(r.content)
        txt.write_text(pdf_to_text(pdf), encoding="utf-8")
        return code, fy, url, "downloaded"
    except Exception as e:  # skip on any failure, per time box
        return code, fy, url, f"failed: {str(e)[:80]}"


def register(code, fy, url):
    rows = read_log()
    for r in rows:
        if r["url"] == url:
            return r["source_id"]
    sid = next_source_id(rows)
    append_log(dict(source_id=sid, url=url, title=f"{PARENTS[code][1]} Annual Report FY{fy - 1}-{fy % 100}",
                    publisher=f"BSE / {PARENTS[code][1]}", tier="T1", date_published="", date_accessed="2026-10-10",
                    notes=f"pdf: sources/pdf/ar/{code}_FY{fy % 100}.pdf; text: sources/raw/ar/{code}_FY{fy % 100}.txt"))
    return sid


def cmd_download(a):
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    TXT_DIR.mkdir(parents=True, exist_ok=True)
    jobs, status = [], []
    for code in a.parents or [p for p in BRANDS]:
        try:
            lst = ar_list(PARENTS[code][0])
        except Exception as e:
            print(code, "list failed", e)
            continue
        jobs += [(code, fy, url) for fy, url in sorted(lst.items())]
    with ThreadPoolExecutor(4) as ex:
        for code, fy, url, st in ex.map(lambda j: get_one(*j), jobs):
            print(code, fy, st, flush=True)
            status.append((code, fy, url, st))
    for code, fy, url, st in status:  # register sequentially (source_log is not thread-safe)
        if not st.startswith("failed"):
            register(code, fy, url)
    (TXT_DIR / "_status.csv").write_text("parent,fy,url,status\n" + "\n".join(
        f"{c},{f},{u},{s}" for c, f, u, s in status), encoding="utf-8")


PAGE_RE = re.compile(r"^=== PAGE (\d+) ===$", re.M)


def sentence(text, m):
    s = max(text.rfind(". ", 0, m.start()), text.rfind("\n\n", 0, m.start())) + 2
    e = text.find(". ", m.end())
    e = len(text) if e == -1 else e + 1
    return re.sub(r"\s+", " ", text[max(s, m.start() - 300):min(e, m.end() + 300)]).strip()


def cmd_count(a):
    log = {r["url"]: r["source_id"] for r in read_log()}
    st = {}
    sp = TXT_DIR / "_status.csv"
    if sp.exists():
        for r in csv.DictReader(sp.open(encoding="utf-8")):
            st[(r["parent"], int(r["fy"]))] = r
    out = []
    for code, brands in BRANDS.items():
        for fy in FYS:
            txt = TXT_DIR / f"{code}_FY{fy % 100}.txt"
            info = st.get((code, fy), {})
            if not txt.exists():
                for b in brands:
                    out.append(dict(parent=PARENTS[code][1], brand=b, fy=f"FY{fy % 100}", mentions="",
                                    pages_with_mentions="", sample_page="", sample_quote="", source_id="",
                                    ar_url=info.get("url", ""),
                                    status=("not available (" + info["status"] + ")") if info else "not available on BSE"))
                continue
            body = txt.read_text(encoding="utf-8", errors="replace")
            parts = PAGE_RE.split(body)
            pages = [(int(parts[i]), re.sub(r"\s+", " ", parts[i + 1])) for i in range(1, len(parts), 2)]  # flatten so multi-word names match across line breaks
            for b, (pat, fl) in brands.items():
                rx = re.compile(pat, fl)
                n, pg, sample = 0, [], None
                for p, t in pages:
                    ms = list(rx.finditer(t))
                    if ms:
                        n += len(ms)
                        pg.append(p)
                        s = sentence(t, ms[0])
                        # prefer a narrative sentence over a bare brand list / index line
                        if sample is None or (len(sample[1]) < 80 and len(s) > len(sample[1])):
                            sample = (p, s)
                out.append(dict(parent=PARENTS[code][1], brand=b, fy=f"FY{fy % 100}", mentions=n,
                                pages_with_mentions=len(pg), sample_page=sample[0] if sample else "",
                                sample_quote=sample[1][:400] if sample else "", source_id=log.get(info.get("url", ""), ""),
                                ar_url=info.get("url", ""), status="counted"))
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} rows -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["download", "count"])
    ap.add_argument("--parents", nargs="*")
    a = ap.parse_args()
    {"download": cmd_download, "count": cmd_count}[a.cmd](a)
