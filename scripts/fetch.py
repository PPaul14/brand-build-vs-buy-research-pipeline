"""Source capture and search for the buy-or-build project.

Usage (run from project root with the venv python):
  python scripts/fetch.py get URL --title "..." --publisher "..." --tier T1 [--date-published 2025-01-23] [--slug hul_minimalist] [--notes "..."]
  python scripts/fetch.py add --url URL --title "..." --publisher "..." --tier T3 --text-file path.txt [--slug ...]
      (register text captured some other way, e.g. via WebFetch, without re-downloading)
  python scripts/fetch.py find "phrase" [--source S003] [--context 250] [--fuzzy 85]

Raw files are written to sources/raw/S###_slug.txt with a header block. PDF text keeps
"=== PAGE n ===" markers so `find` can report page numbers. HTML is reported as page 1.
Pages that refuse access (401/403/429, captcha, login) are logged as INACCESSIBLE and not bypassed.
"""
import argparse
import csv
import datetime as dt
import html
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "sources" / "raw"
PDF = ROOT / "sources" / "pdf"
LOG = ROOT / "data" / "source_log.csv"
LOG_FIELDS = ["source_id", "url", "title", "publisher", "tier", "date_published", "date_accessed", "notes"]

# A full Chrome UA over Python's TLS stack trips some bot filters (seen: w3.org 403), so on a
# 403 we fall back to simpler UAs. This is header choice only; captchas/logins are never bypassed.
UAS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
       "Mozilla/5.0",
       None]  # None = requests' default UA
BASE_HEADERS = {"Accept": "text/html,application/pdf,application/xhtml+xml,*/*;q=0.8",
                "Accept-Language": "en-IN,en;q=0.9"}
BLOCK_MARKERS = ("captcha", "are you a robot", "access denied", "please log in", "sign in to continue")
PAGE_RE = re.compile(r"^=== PAGE (\d+) ===$", re.M)


# ---------- source log ----------
def read_log():
    if not LOG.exists():
        return []
    with LOG.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def next_source_id(rows):
    nums = [int(r["source_id"][1:]) for r in rows if re.fullmatch(r"S\d{3,}", r.get("source_id", ""))]
    return f"S{(max(nums) + 1) if nums else 1:03d}"


def append_log(row):
    new = not LOG.exists() or LOG.stat().st_size == 0
    with LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in LOG_FIELDS})


def slugify(s, n=50):
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s[:n] or "source"


# ---------- extraction ----------
class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form"}
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "table"}

    def __init__(self):
        super().__init__()
        self.out, self.skip, self.title, self._in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag == "title":
            self._in_title = True
        if tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag == "title":
            self._in_title = False
        if tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self.skip:
            self.out.append(data)


def html_to_text(raw):
    p = _Text()
    p.feed(raw)
    text = html.unescape("".join(p.out))
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return p.title.strip(), "=== PAGE 1 ===\n" + text.strip()


def pdf_to_text(path):
    try:
        import pymupdf as fitz
        with fitz.open(path) as doc:
            pages = [pg.get_text() for pg in doc]
    except Exception as e:  # fall back to pdfplumber
        print(f"pymupdf failed ({e}); trying pdfplumber", file=sys.stderr)
        import pdfplumber
        with pdfplumber.open(path) as doc:
            pages = [(pg.extract_text() or "") for pg in doc.pages]
    if sum(len(p.strip()) for p in pages) < 200:
        print("WARNING: very little text extracted; PDF may be scanned (needs OCR).", file=sys.stderr)
    return "\n".join(f"=== PAGE {i} ===\n{t.strip()}" for i, t in enumerate(pages, 1))


def download(url, retries=3, timeout=45):
    last = None
    for ua in UAS:
        headers = {**BASE_HEADERS, **({"User-Agent": ua} if ua else {})}
        for attempt in range(1, retries + 1):
            try:
                r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
                if r.status_code == 403:
                    last = "HTTP 403"
                    break  # try the next UA
                if r.status_code in (401, 402, 407, 429, 451):
                    return None, f"HTTP {r.status_code}"
                r.raise_for_status()
                return r, None
            except requests.RequestException as e:
                last = str(e)
                time.sleep(2 * attempt)
        else:
            return None, last  # network errors exhausted retries; a different UA won't help
    return None, last


def write_raw(sid, slug, url, title, publisher, tier, accessed, text):
    path = RAW / f"{sid}_{slug}.txt"
    header = (f"SOURCE_ID: {sid}\nURL: {url}\nTITLE: {title}\nPUBLISHER: {publisher}\n"
              f"TIER: {tier}\nDATE_ACCESSED: {accessed}\n{'-' * 70}\n")
    path.write_text(header + text + "\n", encoding="utf-8")
    return path


# ---------- commands ----------
def cmd_get(a):
    rows = read_log()
    for r in rows:
        if r["url"] == a.url and "INACCESSIBLE" not in r.get("notes", ""):
            print(f"Already logged as {r['source_id']}: {r['title']}")
            return r["source_id"]
    sid = next_source_id(rows)
    accessed = dt.date.today().isoformat()
    resp, err = download(a.url)
    base = dict(source_id=sid, url=a.url, publisher=a.publisher, tier=a.tier,
                date_published=a.date_published or "", date_accessed=accessed)

    if resp is None:
        append_log({**base, "title": a.title or "", "notes": f"INACCESSIBLE: {err}. {a.notes or ''}".strip()})
        print(f"{sid} INACCESSIBLE ({err}); logged, not bypassed.")
        return sid

    ctype = resp.headers.get("Content-Type", "").lower()
    is_pdf = "pdf" in ctype or resp.content[:5] == b"%PDF-"
    slug = a.slug or slugify(a.title or a.url.rsplit("/", 1)[-1])

    if is_pdf:
        pdf_path = PDF / f"{sid}_{slug}.pdf"
        pdf_path.write_bytes(resp.content)
        text, title = pdf_to_text(pdf_path), a.title or pdf_path.stem
        note = f"pdf: sources/pdf/{pdf_path.name}"
    else:
        resp.encoding = resp.encoding or resp.apparent_encoding
        page_title, text = html_to_text(resp.text)
        low = text.lower()
        if len(text) < 1500 and any(m in low for m in BLOCK_MARKERS):
            append_log({**base, "title": a.title or page_title,
                        "notes": f"INACCESSIBLE: block/login page. {a.notes or ''}".strip()})
            print(f"{sid} INACCESSIBLE (captcha/login page); logged, not bypassed.")
            return sid
        if len(text) < 800:
            print("WARNING: short text; page may be JS-rendered. Check the raw file.", file=sys.stderr)
        title = a.title or page_title
        note = "html"

    path = write_raw(sid, slug, a.url, title, a.publisher, a.tier, accessed, text)
    append_log({**base, "title": title, "notes": f"{note}. {a.notes or ''}".strip(" .") })
    print(f"{sid} saved -> {path.relative_to(ROOT)} ({len(text):,} chars)")
    return sid


def cmd_add(a):
    rows = read_log()
    sid = next_source_id(rows)
    accessed = dt.date.today().isoformat()
    text = Path(a.text_file).read_text(encoding="utf-8")
    if not PAGE_RE.search(text):
        text = "=== PAGE 1 ===\n" + text
    slug = a.slug or slugify(a.title)
    path = write_raw(sid, slug, a.url, a.title, a.publisher, a.tier, accessed, text)
    append_log(dict(source_id=sid, url=a.url, title=a.title, publisher=a.publisher, tier=a.tier,
                    date_published=a.date_published or "", date_accessed=accessed,
                    notes=f"captured text. {a.notes or ''}".strip(" .")))
    print(f"{sid} registered -> {path.relative_to(ROOT)}")
    return sid


def _norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def find(phrase, source=None, context=250, fuzzy=0):
    """Return [{source_id, file, page, context, score}] for a phrase across saved raw text."""
    hits = []
    files = sorted(RAW.glob(f"{source}_*.txt" if source else "S*.txt"))
    target = _norm(phrase)
    for f in files:
        body = f.read_text(encoding="utf-8", errors="replace")
        parts = PAGE_RE.split(body)  # [preamble, n1, text1, n2, text2, ...]
        for i in range(1, len(parts), 2):
            page, text = int(parts[i]), parts[i + 1]
            flat = re.sub(r"\s+", " ", text)
            low = flat.lower()
            for m in re.finditer(re.escape(target), low):
                s, e = max(0, m.start() - context), min(len(flat), m.end() + context)
                hits.append(dict(source_id=f.name.split("_")[0], file=f.name, page=page,
                                 context=flat[s:e], score=100))
            if fuzzy and not any(h["file"] == f.name and h["page"] == page for h in hits):
                from rapidfuzz import fuzz
                # slide a window the size of the phrase across sentences
                for sent in re.split(r"(?<=[.;:])\s+", flat):
                    sc = fuzz.partial_ratio(target, sent.lower())
                    if sc >= fuzzy:
                        hits.append(dict(source_id=f.name.split("_")[0], file=f.name, page=page,
                                         context=sent[: 2 * context], score=round(sc)))
    return hits


def cmd_find(a):
    hits = find(a.phrase, a.source, a.context, a.fuzzy)
    if not hits:
        print("No matches.")
    for h in hits:
        print(f"[{h['source_id']} p.{h['page']} score={h['score']}] {h['file']}\n  ...{h['context']}...\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("get")
    g.add_argument("url")
    for opt in ("--title", "--slug", "--notes", "--date-published"):
        g.add_argument(opt)
    g.add_argument("--publisher", required=True)
    g.add_argument("--tier", required=True, choices=["T1", "T2", "T3", "T4"])
    g.set_defaults(fn=cmd_get)

    d = sub.add_parser("add")
    d.add_argument("--url", required=True)
    d.add_argument("--title", required=True)
    d.add_argument("--publisher", required=True)
    d.add_argument("--tier", required=True, choices=["T1", "T2", "T3", "T4"])
    d.add_argument("--text-file", required=True)
    for opt in ("--slug", "--notes", "--date-published"):
        d.add_argument(opt)
    d.set_defaults(fn=cmd_add)

    f = sub.add_parser("find")
    f.add_argument("phrase")
    f.add_argument("--source")
    f.add_argument("--context", type=int, default=250)
    f.add_argument("--fuzzy", type=int, default=0, help="rapidfuzz threshold 0-100; 0 = exact only")
    f.set_defaults(fn=cmd_find)

    a = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    PDF.mkdir(parents=True, exist_ok=True)
    a.fn(a)


if __name__ == "__main__":
    main()
