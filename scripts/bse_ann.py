"""List BSE corporate announcements for a scrip and date range (public JSON API used by bseindia.com).

  python scripts/bse_ann.py 500696 20250121 20250124 [--grep minimalist]
Prints date, headline and the attachment PDF URL (AttachLive/AttachHis) for each announcement.
"""
import argparse
import datetime as dt
import sys
import requests

sys.stdout.reconfigure(encoding="utf-8")

API = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"
HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bseindia.com/", "Accept": "application/json"}

ap = argparse.ArgumentParser()
ap.add_argument("scrip"); ap.add_argument("start"); ap.add_argument("end"); ap.add_argument("--grep", default="")
a = ap.parse_args()


def fetch(start, end):
    out, page = [], 1
    while True:
        p = dict(pageno=page, strCat=-1, strPrevDate=start, strScrip=a.scrip, strSearch="P", strToDate=end, strType="C", subcategory=-1)
        r = requests.get(API, params=p, headers=HDR, timeout=30)
        r.raise_for_status()
        t = r.json().get("Table", [])
        out += t
        if len(t) < 50:
            return out
        page += 1


# The API silently returns nothing for long ranges, so query in 90-day windows.
rows, d0, d1 = [], dt.datetime.strptime(a.start, "%Y%m%d"), dt.datetime.strptime(a.end, "%Y%m%d")
while d0 <= d1:
    e = min(d0 + dt.timedelta(days=89), d1)
    rows += fetch(d0.strftime("%Y%m%d"), e.strftime("%Y%m%d"))
    d0 = e + dt.timedelta(days=1)
for x in rows:
    text = f"{x.get('HEADLINE','')} {x.get('NEWSSUB','')}"
    if a.grep.lower() not in text.lower():
        continue
    att = x.get("ATTACHMENTNAME") or ""
    url = f"https://www.bseindia.com/xml-data/corpfiling/AttachHis/{att}" if att else ""
    print(x.get("NEWS_DT", "")[:10], "|", x.get("NEWSSUB", "")[:120], "|", url)
