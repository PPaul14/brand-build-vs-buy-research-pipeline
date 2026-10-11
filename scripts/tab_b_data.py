"""Tab B (Build) rows and AI-claim verifications. Run to regenerate data/tab_b.csv and update data/claims_verification_log.csv.

  python scripts/tab_b_data.py

Same schema as Tab A; consideration_inr_cr, stake_pct, deal_structure and revenue_multiple stay blank for builds.
For builds, `what_was_acquired` records what the parent was trying to BUILD (same vocabulary as Tab A, so the
two routes can be compared like for like); `vocab_rationale` explains it.
status_today: Scaled / Stable / Niche / Withdrawn / Unclear. status_evidence names the proxies used:
  P1 = annual report / investor presentation / earnings call   P2 = annual-report mention tracker (data/ar_mentions.csv)
  P3 = current listing (brand site / marketplaces, date checked) P4 = Wayback Machine snapshots
Annual reports are referenced by their source_id in data/source_log.csv (resolved from the cached file name).
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAB = ROOT / "data" / "tab_b.csv"
CLAIMS = ROOT / "data" / "claims_verification_log.csv"
LOG = ROOT / "data" / "source_log.csv"
ACC = "2026-10-10"
FIELDS = ["route", "row_type", "parent", "brand", "category", "year_start", "consideration_inr_cr", "stake_pct",
          "deal_structure", "revenue_inr_cr", "revenue_fy", "revenue_basis", "revenue_multiple", "what_was_acquired",
          "vocab_rationale", "status_today", "status_evidence", "base_rate_flag", "source_url", "source_ids", "date_accessed",
          "confidence", "notes"]

with LOG.open(encoding="utf-8", newline="") as _f:
    _LOG = list(csv.DictReader(_f))


def ar(code, fy):
    """source_id of a cached annual report, e.g. ar('HUL', 23) -> 'S1xx' (FY23 = FY2022-23)."""
    for r in _LOG:
        if f"ar/{code}_FY{fy}.pdf" in r.get("notes", ""):
            return r["source_id"]
    return f"AR:{code}_FY{fy}"  # placeholder until the download registers it


def url(sid):
    return next((r["url"] for r in _LOG if r["source_id"] == sid), "")


BAJ, ZYD = "Bajaj Consumer Care Ltd", "Zydus Wellness Ltd"
HUL, MAR, HON, GCPL = "Hindustan Unilever Ltd", "Marico Ltd", "Honasa Consumer Ltd", "Godrej Consumer Products Ltd"
DAB, TCPL, NYK, ITC = "Dabur India Ltd", "Tata Consumer Products Ltd", "FSN E-Commerce Ventures Ltd (Nykaa)", "ITC Ltd"
RIL = "Reliance Industries Ltd (via Reliance Consumer Products Ltd)"

ROWS = [
    # ---------------- HUL ----------------
    dict(row_type="calibration", parent=HUL, brand="Lever Ayush", category="Other",
         year_start=2001, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="HUL's own ayurvedic masterbrand: an attempt to build an ayurveda franchise in-house rather than buy one (contrast Indulekha, bought 2016).",
         status_today="Niche",
         status_evidence=(f"P2: in AR FY20 ({ar('HUL',20)} p.13: 'The master brand LEVER Ayush continued its momentum in the focused market - South India') and FY21 ({ar('HUL',21)} p.14: 'LEVER Ayush, the master brand maintained focus on its key market in southern India'); "
                          "0 mentions FY22-FY26. P3: leverayush.com gives no response (SSL error); HUL brand pages are JS-rendered (D8) - current availability UNCONFIRMED (S207)."),
         source_ids=f"{ar('HUL',20)};{ar('HUL',21)};S207", confidence="Low",
         notes=("Launch year conflict: 2001 vs 2002 in secondary write-ups (T4 case studies via search; HUL primary not found) - see conflicts.md. "
                "Relaunch: Dec 2016 with ~20 mass-priced products (Rs 30-130) in TN, Kerala, AP, Telangana, Karnataka, a response to Patanjali (T4 case-study sources via search, not saved as evidence). "
                "Pullback in the 2000s: only T4 reports ('HUL may pull out the brand') - UNCONFIRMED. "
                "Today: regional (South India) brand per HUL's own words in FY20-21; dropped from AR narrative from FY22. Calibration row (pre-2020, named in study scope).")),
    dict(row_type="calibration", parent=HUL, brand="Love Beauty & Planet (Unilever global brand, launched in India by HUL)",
         category="BPC-Haircare", year_start=2019, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Purpose-led 'clean/vegan' masstige brand aimed at a digital, sustainability-minded cohort HUL's mass brands did not reach; built inside the group, not bought.",
         status_today="Stable",
         status_evidence=(f"P1: AR FY24 ({ar('HUL',24)} p.51): 'early success in two of the brands launched by the Premium Beauty Business unit (PBBU) - Simple and Love, Beauty & Planet with their combined ARR scaling Rs 100 crores within 3 years'; "
                          f"AR FY25 ({ar('HUL',25)} p.22): 'Novology, Simple and Love, Beauty & Planet... delivering strong growth'. P2: mentioned FY20-FY25, 0 in FY26. P3: lovebeautyandplanet.in live (HTTP 200, 2026-10-10). P4: Wayback 49 monthly captures 2021-06 to 2026-03 (S124)."),
         revenue_inr_cr="", revenue_fy="FY24", revenue_basis="ARR (company-stated annualised run-rate), combined with Simple; brand-only figure not disclosed",
         source_ids=f"{ar('HUL',20)};{ar('HUL',24)};{ar('HUL',25)};S124", confidence="Medium",
         notes=(f"Launch: AR FY20 ({ar('HUL',20)} p.5): 'During the year, we also launched, a purpose-driven brand from the Unilever stable, Love, Beauty and Planet' -> launched in FY20 (Apr 2019-Mar 2020); month UNCONFIRMED, year_start=2019 is a best estimate, so calibration. "
                "AR FY21 also says HUL 'introduced' it in India; secondary search snippets say 2018 (global launch was 2018) - see conflicts.md. "
                "Caveat: a Unilever global brand localised by HUL, not an Indian ground-up build. revenue_inr_cr blank: only a combined Simple + LB&P ARR of Rs 100 Cr (FY24) is disclosed; Simple is a Unilever-acquired brand, so not attributable. "
                "Not named in FY26 AR (PBBU list there: Minimalist, OZiva, Simple, Nexxus, Liquid I.V.).")),
    dict(parent=HUL, brand="Acne Squad", category="BPC-Skincare", year_start=2022, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Digital-first acne brand for 'hyper-connected' Gen Z consumers, a cohort HUL's mass skincare (Pond's, Glow & Lovely) did not own; built in-house via HUL's Agile Innovation Hub.",
         status_today="Withdrawn",
         status_evidence=(f"P2: AR FY23 only ({ar('HUL',23)} p.13: 'we launched two new brands Acne Squad and Find Your Happy Place'); 0 mentions FY24-FY26, while FY24 AR credits only Simple and LB&P with 'early success'. "
                          "P3: acnesquad.in returns HTTP 404 'Store unavailable... This store is currently unavailable' (Shopify), checked 2026-10-10. P4: Wayback has no live (200) capture; last capture 2025-04-06 = 404 (S124)."),
         source_ids=f"{ar('HUL',23)};{ar('HUL',24)};S124", confidence="Medium",
         notes=(f"Launch FY23 (Apr 2022-Mar 2023); trade press dates the launch to early Oct 2022 (fashionnetwork, 2022-10-04, search snippet only, T3, not saved). AR FY23 ({ar('HUL',23)}): 'a range of 11 skincare products and curated regime kits'; launched 'using the Agile Innovation platform'. "
                "'Withdrawn' is inferred from the dead D2C store + silence in 3 subsequent ARs; HUL has not announced a discontinuation (none found). Marketplace (Nykaa/Amazon) listing status UNCONFIRMED: Nykaa returned 403 to scripted check (not bypassed). revenue: never disclosed.")),
    dict(parent=HUL, brand="Find Your Happy Place", category="BPC-Skincare", year_start=2022, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Premium 'mood-transforming' bath & body brand crafted for digital consumers; a premium self-care cohort HUL's mass bath brands did not serve.",
         status_today="Withdrawn",
         status_evidence=(f"P2: AR FY23 only ({ar('HUL',23)} p.18: 'Find Your Happy Place is a premium brand that provides experiential mood transforming Bath and Body ranges'); 0 mentions FY24-FY26. "
                          "P3: findyourhappyplace.in returns HTTP 402 'Store unavailable... If you would like to reactivate your store contact Shopify support' (2026-10-10). P4: Wayback last live (200) capture 2023-11-13; later captures 403 (S124)."),
         source_ids=f"{ar('HUL',23)};S124", confidence="Medium",
         notes=("Launched FY23 (Apr 2022-Mar 2023); first Wayback capture of the site 2022-11-15 (200), so launch c. H2 2022, year_start=2022 (month UNCONFIRMED). "
                "Withdrawal inferred (store frozen + AR silence); no HUL announcement found. Live for ~1 year on the evidence of Wayback captures.")),
    dict(parent=HUL, brand="Novology", category="BPC-Skincare", year_start=2023, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Masstige derma-therapeutic skincare built in-house to reach the 'actives' cohort that later drove the Minimalist acquisition (2025).",
         status_today="Unclear",
         status_evidence=(f"P1: AR FY25 ({ar('HUL',25)} p.22): 'we expanded our masstige portfolio through Novology, Simple and Love, Beauty & Planet. Each of these brands have a sharp positioning and are delivering strong growth'. "
                          f"P2: AR FY23, FY24, FY25 narrative; FY26 only in an R&D technology table ({ar('HUL',26)} p.58), not in the FY26 premium list. P3/P4: no brand domain found (novology.in DNS fail, no Wayback captures) - UNCONFIRMED."),
         source_ids=f"{ar('HUL',23)};{ar('HUL',24)};{ar('HUL',25)};{ar('HUL',26)};S124", confidence="Low",
         notes=(f"Launch: AR FY23 ({ar('HUL',23)} p.18): 'We have also launched a masstige beauty brand Novology in the growing segment of Derma-therapeutic Care'; AR FY24 p.63: 'Novology Hyper Pigmentation Serum that was launched in 2023' -> year_start 2023 (Jan-Mar 2023). "
                "Technology imported from Unilever under the TCA (AR FY24 p.63). Dropped from FY26 narrative the year after HUL bought Minimalist - a signal worth watching, not proof of withdrawal.")),
    # ---------------- Marico ----------------
    dict(parent=MAR, brand="Saffola Immuniveda (incl. Saffola Arogyam Chyawanamrut)", category="Wellness-Nutrition&Supplements",
         year_start=2020, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Marico's 'first range of Ayurvedic products' (press release): entry into immunity/ayurveda, a category Marico had no presence in, under the Saffola masterbrand.",
         status_today="Withdrawn",
         status_evidence=(f"P2: brand list includes 'Saffola Immuniveda' in AR FY21 ({ar('Marico',21)} p.16), FY22, FY24 ({ar('Marico',24)} p.21); absent from the FY25 ({ar('Marico',25)} p.29) and FY26 ({ar('Marico',26)} p.22) brand lists. 'Saffola Arogyam' appears in FY21 only. "
                          "P1: FY21 AR p.24 groups it with Covid-era 'immunity' launches. P3: saffola.in Immuniveda pages return 403 to scripted check (not bypassed) - UNCONFIRMED; P4: no Wayback captures (S207)."),
         source_ids=f"S118;{ar('Marico',21)};{ar('Marico',24)};{ar('Marico',25)};{ar('Marico',26)};S207", source_url=url("S118"), confidence="Low",
         notes=("Launched 2020-09-16 (S118 p.1: 'Marico Limited, one of India's leading FMCG companies, has strengthened its position in the healthy foods and immunity-boosting segment, with the launch of the Saffola ImmuniVeda range'; Kadha Mix + Golden Turmeric Milk Mix; chyawanprash added 2021). "
                f"AR FY21 ({ar('Marico',21)} p.24): 'introduced Saffola Honey, Saffola Arogyam Chyawanamrut Awaleha, Saffola Oodles, Saffola Mealmaker Soya Chunks and traditional immunity boosters under Saffola Immuniveda'. "
                "Status 'Withdrawn' = dropped from the parent's own brand list (P2) after the Covid immunity spike faded; no discontinuation announcement found, so Low confidence. Revenue never disclosed.")),
    dict(parent=MAR, brand="Veggie Clean", category="Other", year_start=2020, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Fruit-and-vegetable wash: a Covid-era entry into home hygiene, a category Marico had not been in.",
         status_today="Withdrawn",
         status_evidence=(f"P1: AR FY21 ({ar('Marico',21)} p.24) calls the hygiene launches 'tactical plays into hygiene categories'. P2: in AR FY20 ({ar('Marico',20)} p.25: 'Marico has introduced Mediker Hand Sanitizer and Veggie Clean in India') and FY21 product tables; 0 mentions FY22-FY26. P4: Marico's Veggie Clean brand page last captured live 2021-09-18, later 406 (S207)."),
         source_ids=f"{ar('Marico',20)};{ar('Marico',21)};S207", confidence="Low",
         notes=("Launched c. Mar-Apr 2020 (FY20 AR, published Aug 2020, already lists it; exact date UNCONFIRMED). The parent itself framed it as tactical, i.e. never meant to be scaled - a 'planned' exit rather than a failed bet. "
                "Withdrawal inferred from AR silence since FY22.")),
    # ---------------- Honasa (listed 2023-11-07; brand-level ARR disclosed) ----------------
    dict(parent=HON, brand="The Derma Co", category="BPC-Skincare", year_start=2020, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Mamaearth (toxin-free/natural) did not reach the ingredient-aware 'actives' cohort; The Derma Co was built to serve it.",
         status_today="Scaled", revenue_inr_cr=750, revenue_fy="FY26",
         revenue_basis="ARR (company-stated annualised net revenue run-rate, '>INR 750 Cr'); not audited revenue",
         status_evidence=(f"P1: AR FY26 ({ar('Honasa',26)} p.8): 'Derma Co. crossed Rs 750 Cr ARR'; Q2 FY26 press release (S120 p.2): 'crossing INR 750 Cr ARR milestone'; AR FY24 ({ar('Honasa',24)} p.17): 'Rs 500 Cr+ Net ARR of The Derma Co. within 50 Months of Launch'. "
                          "P2: mentioned in every Honasa AR FY24-FY26. P3: thedermaco.com live (S125)."),
         source_ids=f"{ar('Honasa',26)};S120;{ar('Honasa',24)};S121;S125", confidence="High",
         notes=(f"Launch-month conflict: AR FY24 ({ar('Honasa',24)} p.12) 'Since The Derma Co's launch in March 2020' vs AR FY26 ({ar('Honasa',26)} p.13) 'The Derma Co, launched in February 2020' - year 2020 either way; see conflicts.md. "
                "Break-even: 'achieving break-even in all quarters of FY24' (S121 p.2). "
                "LISTING CAVEAT: built while Honasa was unlisted (IPO Nov 2023); valid for Tab B because Honasa is listed now and discloses brand-level ARR, but it was not a listed-company build decision (cf. D13 for Tab A).")),
    dict(parent=HON, brand="Aqualogica", category="BPC-Skincare", year_start=2021, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Hydration-led, fruit-plus-actives skincare for younger, climate-specific needs: a sharper sub-cohort than Mamaearth or The Derma Co served.",
         status_today="Scaled", revenue_inr_cr=200, revenue_fy="FY26",
         revenue_basis="ARR (company-stated, 'crossed Rs 200 Cr ARR'); not audited revenue",
         status_evidence=(f"P1: AR FY26 ({ar('Honasa',26)} p.8): 'Aqualogica and Dr. Sheth's crossed Rs 200 Cr ARR'; AR FY24 ({ar('Honasa',24)} p.17): 'Rs 180 Cr+ Net ARR of Aqualogica within 19 Months of Launch'. P2: in all Honasa ARs FY24-FY26. P3: aqualogica.in live (S125)."),
         source_ids=f"{ar('Honasa',26)};{ar('Honasa',24)};S125", confidence="Medium",
         notes=(f"VERIFICATION 2026-10-10: downgraded High -> Medium. The FY26 figure is a joint, undated timeline bullet ('Aqualogica and Dr. Sheth's crossed Rs 200 Cr ARR'); "
                "read as each brand >Rs 200 Cr (FY24 already had Aqualogica 180+ and Dr. Sheth's 150+ separately, so a combined 200 would be no milestone), but the split is not stated, "
                f"and AR FY25 ({ar('Honasa',25)} p.54) still says '180+Cr Net Annual Revenue Run-Rate of Aqualogica'. Brand-only FY26 ARR UNCONFIRMED. "
                f"Launch: AR FY24 ({ar('Honasa',24)} p.7): 'Aqualogica was launched in 2021'. Growth flattened: ~Rs 180 Cr ARR at 19 months (c. 2022-23) vs ~Rs 200 Cr by FY26, i.e. scaled fast, then plateaued. "
                "LISTING CAVEAT: built pre-IPO (Honasa listed Nov 2023).")),
    dict(parent=HON, brand="Ayuga", category="BPC-Skincare", year_start=2021, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Herbal/ayurvedic skincare ('golden generation of skin rituals') aimed at an ayurveda-leaning millennial cohort.",
         status_today="Withdrawn",
         status_evidence=(f"P2: AR FY24 ({ar('Honasa',24)} p.8: 'Ayuga is a natural skincare brand bringing the golden generation of skin rituals back'), 9 mentions; FY25 only in BRSR/legal notes ({ar('Honasa',25)} p.108); 0 mentions FY26 (FY26 brand list: Mamaearth, The Derma Co, Aqualogica, Dr Sheths, BBlunt, Staze, Lumineve). "
                          "P3: ayuga.in HTTP 402 'Store unavailable' (Shopify), 2026-10-10. P4: Wayback first capture 2021-11-27, last live capture 2025-10-13 (S125)."),
         source_ids=f"{ar('Honasa',24)};{ar('Honasa',25)};{ar('Honasa',26)};S125", confidence="Medium",
         notes=("year_start 2021 from first Wayback capture of ayuga.in (2021-11-27); launch date not stated in the ARs - UNCONFIRMED beyond the year. "
                "Withdrawal inferred (store frozen after Oct 2025 + dropped from the FY26 brand list); no announcement found. Never given an ARR milestone, unlike its siblings. LISTING CAVEAT: launched pre-IPO.")),
    dict(parent=HON, brand="Staze (Staze 9to9)", category="BPC-ColourCosmetics", year_start=2024, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Honasa had no colour-cosmetics brand; Staze is its first ('to capture share of color cosmetics', S122).",
         status_today="Niche",
         status_evidence=(f"P1: AR FY25 ({ar('Honasa',25)} p.30): in lipsticks, 'Led by Staze and Mamaearth within Honasa, we are just getting started and currently hold <1% market share online'; AR FY26 ({ar('Honasa',26)} p.10): 'Staze 9to9 keeps building for the Gen Z consumer'. No ARR disclosed. "
                          "P2: FY24-FY26 ARs. P3: stazebeauty.com live (S125)."),
         source_ids=f"S122;{ar('Honasa',25)};{ar('Honasa',26)};S125", source_url=url("S122"), confidence="Medium",
         notes=("Launched 2024-03-28 (S122 p.2: 'HONASA CONSUMER LAUNCHES STAZE, TO CAPTURE SHARE OF COLOR COSMETICS'); post-IPO build. "
                "Niche = still supported but no ARR milestone and <1% online lipstick share (combined with Mamaearth) after ~1 year; 2.5 years old at the check date, so the verdict is provisional.")),
    # ---------------- Godrej Consumer ----------------
    dict(parent=GCPL, brand="Godrej Fab (liquid detergent)", category="Other", year_start=2024, what_was_acquired="REVENUE_SCALE",
         vocab_rationale="GCPL already sold liquid detergent (Ezee, north/east); Fab is a mass-priced regional build (South India) to add share and scale in a category it knew.",
         status_today="Scaled", revenue_inr_cr=490, revenue_fy="FY26",
         revenue_basis="ARR (company-stated 'annualised revenue run rate of nearly Rs 490 crore'); FY25 'topline' >Rs 150 Cr",
         status_evidence=(f"P1: AR FY26 ({ar('GCPL',26)} p.42): 'In fiscal year 2026, Fab reached an annualised revenue run rate of nearly Rs 490 crore in a category approximately Rs 4,000 crore in size, having moved from loss-making in its early years to near break-even'; "
                          f"AR FY25 ({ar('GCPL',25)} p.39): 'Fab, our new liquid detergent brand, crossed Rs 150 crore topline in its first year'. P2: AR FY24-FY26; one of three 'Speedboats' (FY26 p.43)."),
         source_ids=f"{ar('GCPL',26)};{ar('GCPL',25)};{ar('GCPL',24)}", confidence="High",
         notes=("Launched 2024-01-16 in South India at Rs 99/litre (T3 trade press via search: afaqs/exchange4media, not saved; AR FY24 lists 'Fab Liquid Detergent' among new launches). "
                "Home care, outside the BPC/food taxonomy (category=Other); kept because it is the cleanest recent in-house scale-up by a Tab A parent. Not a new category for GCPL (Ezee) - this is a value-tier regional build.")),
    dict(parent=GCPL, brand="Godrej Ninja (Godrej Pet Care Ltd)", category="Other", year_start=2025, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="GCPL had no pet food business; AR FY25 calls Ninja 'our entry into pet food'.",
         status_today="Niche", revenue_inr_cr=2.22, revenue_fy="FY26", revenue_basis="total_income ('Total Revenue' of subsidiary Godrej Pet Care Ltd, Rs 222.1 lakh)",
         status_evidence=(f"P1: S073 (Reg 30, 2026-07-22): 'Total Revenue of Godrej Pet Care for the Financial Year ended March 31, 2026 was Rs 222.1 Lakh'; FY24 73.11 / FY25 46.33 / FY26 222.1 lakh. AR FY25 ({ar('GCPL',25)} p.39): 'Godrej Ninja, our entry into pet food, is a launch we did in record time'. "
                          "P2: 'Ninja' appears in AR FY25, 0 times in AR FY26 (only 'Pet Care' as a category). P3: godrejninja.com 403 to scripted check (not bypassed); P4: live Wayback captures 2025-09 to 2026-04 (S207)."),
         source_ids=f"S073;{ar('GCPL',25)};{ar('GCPL',26)};S207", source_url=url("S073"), confidence="Medium",
         notes=("Entry disclosed 2024-08-07 (per S073); brand launched in Tamil Nadu 2025-04-08 (T3 press via search; GCPL press release PDF returned 403, S119, not bypassed). "
                "Planned investment Rs 500 Cr over 5 years (press, T3); actual primary infusion Rs 200 Cr (S073). FY26 revenue Rs 2.22 Cr after ~1 year: Niche, provisional given age. "
                "FY24/FY25 revenue predates the brand (entity was Godrej Consumer Care Ltd, renamed 2024-10-28). Low revenue may partly reflect a single-state rollout.")),
    dict(row_type="calibration", parent=GCPL, brand="Godrej Protekt", category="Other", year_start=2018, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Hand and home hygiene beyond soap: Protekt was GCPL's vehicle to enter handwash/sanitiser, where it had no brand.",
         status_today="Withdrawn",
         status_evidence=(f"P2: AR FY19 ({ar('GCPL',19)} p.151: launches 'during the year 2018-19: 1. Protekt-Mr. Magic Hand Wash'), FY20 (7 mentions), FY21 (13), FY22 (1, brand table only); 0 mentions FY23-FY26. "
                          "P1: none - no discontinuation statement found. P3: godrejprotekt.com no response on 2026-10-10; P4: last live Wayback capture 2023-03-13 (S207)."),
         source_ids=f"{ar('GCPL',19)};{ar('GCPL',20)};{ar('GCPL',21)};{ar('GCPL',22)};S207", confidence="Low",
         notes=("Protekt domain has Wayback captures from 2009, so the name may be older than the FY19 Mr. Magic launch - original launch year UNCONFIRMED. Mr. Magic: FY19 launch (Apr 2018-Mar 2019; calendar month UNCONFIRMED; year_start 2018 by the FY rule: an FY-only launch takes the calendar year holding 9 of its 12 months), so calibration. "
                "Covid expansion: Jul 2020, 12 new hygiene SKUs and stated ambition to be a 'Rs 500 crore brand over the next three years' (fashionnetwork/exchange4media, T3, search snippet only). "
                "Disappears from ARs after FY22: the Covid hygiene spike ended and the ambition went unmet. Withdrawal inferred from AR silence (Low).")),
    # ---------------- Dabur ----------------
    dict(parent=DAB, brand="Dabur Vita", category="Wellness-Nutrition&Supplements", year_start=2021, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Dabur's 'foray into the Health Food Drink category' (S117); it had chyawanprash and honey but no HFD brand.",
         status_today="Withdrawn",
         status_evidence=(f"P1: AR FY25 ({ar('Dabur',25)} p.25): 'we have decided to exit categories such as Vedic Tea, Adult & Baby Diapers, and Dabur Vita, where scalability and profitability remain constrained'; AR FY26 ({ar('Dabur',26)} p.85): 'We exited segments such as Vedic Tea, Adult & Baby Diapers, and Dabur Vita'. "
                          "P2: AR FY22 12 mentions -> FY23 7 -> FY24 5 -> FY25/FY26 only as an exit. P3: daburvita.com redirects to a still-live brand page on dabur.com (2026-10-10; residual page, stock UNCONFIRMED). P4: last live Wayback capture of daburvita.com 2024-03-04 (S206)."),
         source_ids=f"S117;{ar('Dabur',22)};{ar('Dabur',25)};{ar('Dabur',26)};S206", source_url=url("S117"), confidence="High",
         notes=("Launched 2021-12-30 (S117: 'Dabur India Ltd. today announced its foray into the Health Food Drink category with the launch of Dabur Vita'; e-commerce launch with Flipkart, 7 SKUs Rs 10-430). "
                "Explicit, parent-stated exit ~3 years after launch: the clearest T1-documented build failure in the set. Revenue never disclosed.")),
    # ---------------- Tata Consumer ----------------
    dict(parent=TCPL, brand="Tata Simply Better", category="Food-Staples&Organic", year_start=2022, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Launched as TCPL's 'entry into protein platform' with plant-based meat, a category it had no presence in; later re-purposed for cold-pressed oils.",
         status_today="Stable",
         status_evidence=(f"P1: AR FY23 ({ar('TCPL',23)} p.21): 'entered the Protein category with plant-based meat under the brand Tata Simply Better'; AR FY24 ({ar('TCPL',24)} p.140): 'launched last year with an innovative portfolio of plant-based meat... complemented by a new range of cold-pressed oils'; "
                          f"AR FY26 ({ar('TCPL',26)} p.25): 'Tata Simply Better expanded its cold-pressed oils portfolio and extended into dry fruit snacking'. P2: in every TCPL AR FY23-FY26. P3: tatasimplybetter.com live ('Buy Cold Pressed Oils Online'), 2026-10-10; P4: Wayback live 2023-03 to 2026-09 (S206)."),
         source_ids=f"{ar('TCPL',23)};{ar('TCPL',24)};{ar('TCPL',25)};{ar('TCPL',26)};S206", confidence="Medium",
         notes=("Launched FY23 (Apr 2022-Mar 2023) as plant-based meat; year_start 2022 (month UNCONFIRMED). The original proposition (plant-based meat) is no longer mentioned after FY24; the brand survives by pivoting to cold-pressed oils (FY24) and dry-fruit snacks (FY26). "
                "'Stable' = alive and extended, but no revenue disclosed and not one of the growth brands TCPL quantifies. Counted as a pivot, not a success, in the base rate.")),
    dict(parent=TCPL, brand="Tata GoFit", category="Wellness-Nutrition&Supplements", year_start=2022, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Plant protein powder: second leg of TCPL's 2022 'protein platform', a category it had not been in.",
         status_today="Niche",
         status_evidence=(f"P2: AR FY23 ({ar('TCPL',23)} p.21: 'plant protein powder under Tata GoFit'), FY24 brand list ({ar('TCPL',24)} p.15), FY25 (brand-name cover collage only); 0 mentions in AR FY26, whose brand list ({ar('TCPL',26)} p.15) omits it. "
                          "P3: tatagofit.com live D2C store ('Tata GoFit Plant Protein | Plant Based Protein Powder for Women'), 2026-10-10. P4: Wayback 31 monthly captures 2023-01 to 2026-03, all live (S206)."),
         source_ids=f"{ar('TCPL',23)};{ar('TCPL',24)};{ar('TCPL',25)};{ar('TCPL',26)};S206", confidence="Low",
         notes=("CORRECTION: first coded Withdrawn from the FY26 AR silence alone; the live D2C store (P3/P4) contradicts that, so Niche: still sold, dropped from the parent's brand list. Lesson: AR silence = de-prioritised, not dead. Launched FY23 alongside Simply Better PBM; year_start 2022 (month UNCONFIRMED). In FY24 AR p.45 TCPL calls it a 'digital brand'. "
                "No exit statement found. Note TCPL bought Organic India (2024), which overlaps the wellness space.")),
    dict(row_type="calibration", parent=TCPL, brand="Tata Sampann (built by Tata Chemicals Ltd; merged into TCPL 2020)",
         category="Food-Staples&Organic", year_start="", what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Group-built pulses/spices staples brand: the Tata group's in-house entry into branded staples beyond salt.",
         status_today="Scaled", revenue_inr_cr=1109, revenue_fy="FY25", revenue_basis="revenue as charted by TCPL ('Tata Sampann Revenue (INR Crores)'); ops vs total income not stated",
         status_evidence=(f"P1: AR FY25 ({ar('TCPL',25)} p.42): '29% Tata Sampann revenue growth', chart 'Tata Sampann Revenue (INR Crores)' with FY25 = 1,109 (FY24 862; 862 x 1.29 = 1,112, consistent). P2: in every TCPL AR FY20-FY26."),
         source_ids=f"{ar('TCPL',20)};{ar('TCPL',25)}", confidence="Medium",
         notes=(f"ORIGIN: not a TCPL build. AR FY20 ({ar('TCPL',20)} p.5): 'Tata Global Beverages was renamed as Tata Consumer Products, following the merger of the Consumer Products business of Tata Chemicals with itself... Tata Salt and Tata Sampann'. Built in-house by Tata Chemicals Ltd (listed). "
                "year_start UNCONFIRMED: recalled as 2017 (C045) but no primary source found; certainly pre-2020. Chart labels in the extracted PDF text are out of order; only FY25=1,109 and FY24=862 are cross-checked via the stated 29% growth.")),
    # ---------------- Nykaa ----------------
    dict(parent=NYK, brand="Nykd by Nykaa", category="Other", year_start=2020, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Lingerie/athleisure: Nykaa's own-brand entry into intimate wear, a category it had only retailed.",
         status_today="Scaled", revenue_inr_cr=150, revenue_fy="FY25", revenue_basis="GMV (gross merchandise value, '>Rs 150 crores (GMV)'); not revenue",
         status_evidence=(f"P1: AR FY25 ({ar('Nykaa',25)} p.20): 'two brands - 20 Dresses and Nykd, already more than Rs 100 crores (GMV) and Rs 150 crores (GMV) brands, respectively in FY2025'; AR FY24 ({ar('Nykaa',24)} p.11): 'Both Kay Beauty and Nykd By Nykaa have an annualised GMV run rate of over Rs 1,500 million (basis Q4FY24)'. "
                          f"P2: AR FY24-FY26. FY26 ({ar('Nykaa',26)} p.87): expanded into sleepwear and activewear."),
         source_ids=f"{ar('Nykaa',24)};{ar('Nykaa',25)};{ar('Nykaa',26)}", confidence="Medium",
         notes=(f"Launch: AR FY24 ({ar('Nykaa',24)} p.67): 'We launched Nykd in 2020'; AR FY26 p.87: 'Introduced in 2020'. GMV, not net revenue: Scaled on GMV only. "
                "LISTING CAVEAT: launched pre-IPO (Nykaa listed Nov 2021). Fashion brands as a group slowed in FY25 ('Growth slowdown in FY2025') and FY26 fashion GMV was Rs 388 Cr across 5 brands.")),
    dict(row_type="calibration", parent=NYK, brand="Kay Beauty (co-created with Katrina Kaif)", category="BPC-ColourCosmetics", year_start=2019,
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Celebrity-led makeup brand: built to borrow a celebrity's cohort, which Nykaa Cosmetics (value makeup) did not have.",
         status_today="Scaled", revenue_inr_cr=240, revenue_fy="FY25", revenue_basis="GMV ('crossed the GMV of Rs 240 crores'); FY26 stated as Rs 250-350 Cr NSV jointly with Nykaa Cosmetics",
         status_evidence=(f"P1: AR FY25 ({ar('Nykaa',25)} p.16): 'Kay Beauty and Nykaa Cosmetics have crossed the GMV of Rs 240 crores and Rs 350 crores, respectively'; AR FY26 ({ar('Nykaa',26)} p.23): 'Nykaa Cosmetics & Kay Beauty have both reached a Rs 250-350 crores NSV'. P2: AR FY22-FY26."),
         source_ids=f"{ar('Nykaa',24)};{ar('Nykaa',25)};{ar('Nykaa',26)}", confidence="Medium",
         notes=(f"Launch: AR FY24 ({ar('Nykaa',24)} p.18): 'Kay Beauty, India's first celebrity beauty brand launched in FY20' -> FY20 = Apr 2019-Mar 2020; year_start 2019 (recalled 2019, C052). Calibration (pre-2020). "
                "Partly a celebrity partnership, so not a pure in-house build. Entered UK via Space NK (FY26).")),
    # ---------------- ITC (calibration) ----------------
    dict(row_type="calibration", parent=ITC, brand="Bingo!", category="Food-Snacks&Bars", year_start=2007, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="ITC's in-house entry into branded salty snacks.",
         status_today="Scaled", revenue_inr_cr=2700, revenue_fy="FY20", revenue_basis="annual consumer spend (retail value, 'nearly Rs 2700 cr'); NOT company revenue",
         status_evidence=(f"P1: AR FY20 ({ar('ITC',20)} p.10): 'Bingo! nearly Rs 2700 cr' annual consumer spend; 'Bingo! is No. 1 in Bridges segment of Snack Foods'. AR FY25 ({ar('ITC',25)} p.75): 'remains the market leader in the Bridges segment across the country'. P2: every ITC AR FY20-FY26."),
         source_ids=f"{ar('ITC',20)};{ar('ITC',25)}", confidence="Medium",
         notes="Launch year 2007 from secondary sources only (search snippets, T4) - ITC primary not checked; year Low confidence. Consumer-spend figures are not repeated after FY20 AR."),
    dict(row_type="calibration", parent=ITC, brand="Sunfeast YiPPee!", category="Food-Snacks&Bars", year_start=2010, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="ITC's in-house entry into instant noodles against an entrenched leader (Maggi).",
         status_today="Scaled", revenue_inr_cr=1300, revenue_fy="FY20", revenue_basis="annual consumer spend (retail value, 'nearly Rs 1300 cr'); NOT company revenue",
         status_evidence=(f"P1: AR FY20 ({ar('ITC',20)} p.10): 'YiPPee! nearly Rs 1300 cr' annual consumer spend; AR FY25 ({ar('ITC',25)} p.75): 'YiPPee! sustained its position as a strong No. 2 brand in the Instant Noodles' segment. P2: every ITC AR FY20-FY26."),
         source_ids=f"{ar('ITC',20)};{ar('ITC',25)}", confidence="Medium",
         notes="Launch year 2010 from secondary sources only (T4); ITC primary not checked."),
    dict(row_type="calibration", parent=ITC, brand="Fabelle", category="Other", year_start=2016, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Luxury chocolates sold through ITC Hotels boutiques: built to reach a luxury cohort ITC's mass foods did not touch.",
         status_today="Niche",
         status_evidence=(f"P1: AR FY20 ({ar('ITC',20)} p.90): 'exclusive boutiques across 8 ITC Hotels and kiosks at 3 Welcomhotels'; AR FY25 ({ar('ITC',25)} p.76): 'opened an exclusive Fabelle store at Bengaluru airport, expanding the availability... beyond the luxury boutiques at ITC Hotels and Quick-Commerce channel'. No scale figure ever disclosed. P2: every ITC AR FY20-FY26 (1-4 mentions/yr)."),
         source_ids=f"{ar('ITC',20)};{ar('ITC',25)}", confidence="Medium",
         notes="Launch April 2016 per secondary sources (T4); ITC primary not checked. Niche by design (luxury, hotel-led); ITC's mass chocolate push came later under 'Sunfeast Fantastik' (FY24)."),
    # ---------------- Bajaj Consumer ----------------
    dict(parent=BAJ, brand="Bajaj Zero Grey", category="BPC-Haircare", year_start=2020, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Premium anti-greying oil sold 'primarily for E-commerce': aimed at an online, premium cohort that mass Almond Drops did not reach.",
         status_today="Withdrawn",
         status_evidence=(f"P2: AR FY20 ({ar('Bajaj',20)} p.27: 'Bajaj Zero Grey Anti Greying Hair Oil was launched on Ecommerce platforms and in select Pharmacy outlets earlier this year'), FY21 ({ar('Bajaj',21)} p.7: 'our digital first brand that has been launched primarily for E-commerce'); FY22-FY23 only in the corporate timeline; 0 mentions FY24-FY26. "
                          "P3: bajajzerogrey.com gives no response (SSL error) on 2026-10-10. P4: Wayback last live capture 2025-07-10 (S206)."),
         source_ids=f"{ar('Bajaj',20)};{ar('Bajaj',21)};{ar('Bajaj',23)};S206", confidence="Low",
         notes=(f"Status Withdrawn (Low): domain dead on the check date and AR silent since FY24, but the site was live as late as 2025-07, so it outlived its AR coverage. Launched early 2020 (AR FY22 {ar('Bajaj',22)} p.5 timeline: '2020 ... Launched Bajaj Zero Grey Hair Oil'). "
                "Not in the FY24 'Digital Brands' list (which names only 100% Pure and Natyv Soul), i.e. dropped within ~3 years; no exit statement found.")),
    dict(parent=BAJ, brand="Natyv Soul", category="BPC-Haircare", year_start=2021, what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Premium imported-oil (argan/marula) hair range: a digital-first premium cohort Bajaj's mass hair oils did not serve.",
         status_today="Niche",
         status_evidence=(f"P2: AR FY22 14 mentions ({ar('Bajaj',22)} p.4: 'the launch of Natyv Soul and Bajaj 100% Pure brands to address the ever-evolving needs of the new-age consumers'), FY23 22, FY24 1 (listed under 'Digital Brands'), FY25 1 (brand tile only), FY26 0. "
                          "P3: natyvsoul.com now redirects to a brand page on the corporate site (bajajconsumercare.com/natyv-soul), 2026-10-10. P4: Wayback last live capture of the standalone store 2023-10-01 (S206)."),
         source_ids=f"{ar('Bajaj',22)};{ar('Bajaj',23)};{ar('Bajaj',24)};{ar('Bajaj',26)};S206", confidence="Low",
         notes=(f"Launched 2021 (AR FY22 {ar('Bajaj',22)} p.5 timeline: '2021 ... Launched two digital first brands: Bajaj 100% Pure and Natyv Soul'). "
                "Mentions collapse from 22 (FY23) to 1 (FY24) and to 0 (FY26); standalone D2C store closed after 2023 but products still shown on the corporate site, so Niche (not Withdrawn). Marketplace availability UNCONFIRMED.")),
    dict(parent=BAJ, brand="Bajaj 100% Pure (coconut oil range)", category="BPC-Haircare", year_start=2021, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Bajaj's entry into pure coconut oil ('we entered the coconut oil category'), a large category it had not been in.",
         status_today="Stable",
         status_evidence=(f"P1: AR FY24 ({ar('Bajaj',24)} p.5): 'We are scaling up Bajaj 100% Pure Coconut Oil across all the channels... the top line for coconut oil witnessed 36% growth in the financial year'; AR FY26 ({ar('Bajaj',26)} p.11): 'Bajaj 100% Pure Coconut Oil delivered a resilient performance this fiscal year'. "
                          "P2: FY22-FY26 every year (15/21/14/14/3)."),
         source_ids=f"{ar('Bajaj',22)};{ar('Bajaj',23)};{ar('Bajaj',24)};{ar('Bajaj',26)}", confidence="Medium",
         notes=("Launched 2021 as a 'digital first' brand, then taken to all channels: the one Bajaj digital launch that survived, by becoming a mainstream coconut-oil range. "
                "No revenue disclosed; '36% growth' is for the coconut oil topline. Stable, not Scaled (no size disclosed; FY26 mentions fall to 3).")),
    # ---------------- Zydus Wellness ----------------
    dict(parent=ZYD, brand="I'mlite", category="Food-Staples&Organic", year_start=2023, what_was_acquired="REVENUE_SCALE",
         vocab_rationale="Sugar blended with stevia: extends Zydus's sugar-substitute franchise (Sugar Free) into the much larger sugar shelf.",
         status_today="Unclear",
         status_evidence=(f"P1: AR FY24 ({ar('Zydus',24)} p.13): 'We also celebrated the launch of a new brand, I'mlite, a unique formulation of sugar blended with stevia to offer consumers 50% fewer calories than regular sugar'. "
                          f"P2: in AR FY24-FY26 brand lists (FY26 {ar('Zydus',26)} p.7). No performance figure disclosed."),
         source_ids=f"{ar('Zydus',24)};{ar('Zydus',25)};{ar('Zydus',26)}", confidence="Low",
         notes="FY24 launch (month UNCONFIRMED; year_start 2023 by the FY rule). Still listed but never quantified; too little evidence to call it Stable or Niche."),
    # ---------------- Reliance (RCPL) ----------------
    dict(parent=RIL, brand="Independence", category="Food-Staples&Organic", year_start=2022, what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="RCPL's own FMCG staples brand: Reliance's in-house entry into branded packaged staples (it previously only retailed them).",
         status_today="Scaled", revenue_inr_cr=2600, revenue_fy="FY26", revenue_basis="'sales' as stated (~Rs 2,600 crore); gross vs net not stated",
         status_evidence=(f"P1: RIL AR FY26 ({ar('RIL',26)} p.47): 'Independence brand achieved ~Rs 2,600 crore sales'; AR FY25 ({ar('RIL',25)} p.34): 'Flagship brands such as Campa and Independence are gaining momentum'. P2: RIL AR FY23-FY26."),
         source_ids=f"S116;{ar('RIL',23)};{ar('RIL',25)};{ar('RIL',26)}", source_url=url("S116"), confidence="Medium",
         notes=("Launched 2022-12-15 in Gujarat (S116 p.1: 'Reliance Consumer Products Ltd., the FMCG arm and a fully owned subsidiary of Reliance Retail Ventures Ltd., today launched its indigenous made-for-India consumer packaged goods brand, INDEPENDENCE in Gujarat'). "
                "Parent per D4: RCPL counted under RIL (listed). CAVEAT: sold heavily through the group's own retail (Reliance Retail/JioMart), a captive channel no other Tab B parent has - scale is not comparable like-for-like. Medium (single T1 figure, basis unstated).")),
    dict(parent=RIL, brand="Campa (HYBRID: dormant name bought 2022, brand rebuilt in-house)", category="Beverages", year_start=2023,
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Reliance had no beverage brand; it bought only a dormant trademark (recall, no revenue or team) and built the business itself - entry by build on a bought name.",
         status_today="Scaled", revenue_inr_cr=4700, revenue_fy="FY26", revenue_basis="gross sales ('Rs 4,700+ crore in gross sales'); not net revenue",
         status_evidence=(f"P1: RIL AR FY26 ({ar('RIL',26)} p.47): 'Campa achieved Rs 4,700+ crore in gross sales in FY 2025-26. In March 2026, it became India's fourth-largest carbonated soft drinks brand'; AR FY25 ({ar('RIL',25)} p.34): '>10% market share in sparkling beverage category in select states'. P2: RIL AR FY23-FY26."),
         source_ids=f"{ar('RIL',23)};{ar('RIL',25)};{ar('RIL',26)};S112", confidence="Medium",
         notes=(f"HYBRID - excluded from the pure-build base rate; discussed in Part 3. Trademark bought from Pure Drinks Group in 2022 (~Rs 22 Cr per PTI citing unnamed sources, S112, T3; also Tab A row). "
                f"Relaunch 2023 (RIL AR FY23 {ar('RIL',23)} p.77: 'The FMCG business launched several products during the year including Independence brand and the iconic beverage brand, Campa'); relaunch month Mar 2023 per recall (C056) - month UNCONFIRMED by primary source. "
                "Beverage investment of up to Rs 8,000 Cr (S113, T4 - not relied on). Same captive-retail caveat as Independence.")),
]


# base_rate_flag: which rows count toward the Part 1 build base rate (data/base_rates.csv). Default 'included'.
BASE_RATE_FLAG = {
    "Godrej Fab": "excluded_out_of_scope",      # home care (liquid detergent)
    "Veggie Clean": "excluded_out_of_scope",    # home hygiene (produce wash); parent called it 'tactical'
    "Godrej Ninja": "excluded_out_of_scope",    # pet food
    "Nykd by Nykaa": "excluded_out_of_scope",   # lingerie/apparel
    "Independence": "excluded_captive_channel", # scale via Reliance Retail/JioMart
    "Campa": "excluded_hybrid",                 # dormant name bought, brand rebuilt in-house
    "Novology": "excluded_unclear",
    "I'mlite": "excluded_unclear",
}


def base_rate_flag(brand):
    return next((v for k, v in BASE_RATE_FLAG.items() if brand.startswith(k)), "included")


def write_tab():
    with TAB.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in ROWS:
            row = {"route": "Build", "row_type": "core", "date_accessed": ACC, **r}
            row.setdefault("base_rate_flag", base_rate_flag(row["brand"]))
            if not row.get("source_url"):
                row["source_url"] = url(row["source_ids"].split(";")[0])
            w.writerow({k: row.get(k, "") for k in FIELDS})
    print(f"{len(ROWS)} rows -> {TAB.relative_to(ROOT)}")


# claim_id -> (value_verified, source_id, match, how_caught)
VERIFY = {
    "C034": ("UNCONFIRMED: secondary sources split 2001 vs 2002; no HUL primary found", "", "Unverified",
             "Search: T4 case studies disagree with each other; logged in conflicts.md"),
    "C035": ("UNCONFIRMED: only T4 reports that HUL 'may pull out the brand'", "", "Unverified",
             "No primary evidence of a formal withdrawal; HUL AR FY20-21 shows it alive as a South-India brand"),
    "C036": ("Relaunch Dec 2016 (~20 products, Rs 30-130, five southern states) per T4 case studies", "", "Partial",
             "Search: relaunch was Dec 2016, not 2017; T4 only"),
    "C037": ("Launched in India during FY20 (Apr 2019-Mar 2020)", "S128", "Y",
             "HUL AR FY20 p.5 'During the year, we also launched... Love, Beauty and Planet'; search snippets saying 2018 conflate the 2018 global launch"),
    "C038": ("April 2016 per secondary sources", "", "Unverified", "Only T4 search snippets; ITC primary not checked"),
    "C039": ("2007 per secondary sources", "", "Unverified", "Only T4 search snippets; ITC primary not checked"),
    "C040": ("2010 per secondary sources", "", "Unverified", "Only T4 search snippets; ITC primary not checked"),
    "C041": ("NOT RESEARCHED: Farmlite dropped from scope (time box)", "", "Not checked", ""),
    "C042": ("Launched 2020-09-16", "S118", "Y", "Marico press release (T1)"),
    "C043": ("Saffola FITTIFY Gourmet already in Marico's FY20 AR brand table and called existing in the Sep 2020 Immuniveda release; launch before Apr 2020, exact date UNCONFIRMED",
             f"{ar('Marico',20)};S118", "N", "AR mention tracker: brand present in the FY20 report, so '2020 launch' is wrong or at best borderline"),
    "C044": ("Present in Marico FY20 AR brand table (pre-2020); launch year not verified", ar('Marico',20), "Unverified", "Not a Tab B row; not researched further"),
    "C045": ("Built by Tata Chemicals Ltd, merged into TCPL in FY20; launch year UNCONFIRMED", ar('TCPL',20), "N",
             "TCPL AR FY20 p.5: Sampann came with the merger of Tata Chemicals' consumer business - not a TCPL build"),
    "C046": ("Launched FY23 (2022-23) as plant-based meat; cold-pressed oils added FY24", f"{ar('TCPL',23)};{ar('TCPL',24)}", "N",
             "TCPL ARs: year wrong (2022 not 2021) and the recall missed that the brand started as plant-based meat and pivoted"),
    "C047": ("Protekt Mr. Magic launched FY19 (2018-19); Protekt in FY20 AR before Covid; domain captured from 2009; 2020 was a Covid range expansion",
             f"{ar('GCPL',19)};{ar('GCPL',20)};S207", "N", "GCPL AR FY19 p.151 + Wayback: the brand predates 2020; recall confused the Jul 2020 expansion with the launch"),
    "C048": ("Launched Feb or Mar 2020 (Honasa ARs disagree on month)", f"{ar('Honasa',24)};{ar('Honasa',26)}", "Y", "Honasa ARs; month conflict logged"),
    "C049": ("Launched 2021", ar('Honasa',24), "Y", "Honasa AR FY24 p.7"),
    "C050": ("Bought: Honasa's '1st Major Acquisitions: BBLUNT + Dr. Sheth's' (2022)", f"{ar('Honasa',24)};{ar('Honasa',26)}", "Y",
             "Honasa AR FY24 p.17 ('Scaling 30x+ in 25 Months Since Acquisition') and FY26 p.8 timeline"),
    "C051": ("In-house; live c.2021-11 to 2025-10; dropped from FY26 AR; store now unavailable", f"{ar('Honasa',24)};{ar('Honasa',26)};S125", "Y",
             "AR mention tracker + Wayback + live check"),
    "C052": ("Launched FY20 (Apr 2019-Mar 2020)", ar('Nykaa',24), "Y", "Nykaa AR FY24 p.18"),
    "C053": ("Launched 2020", f"{ar('Nykaa',24)};{ar('Nykaa',26)}", "Partial", "Nykaa AR FY24 p.67 / FY26 p.87: 2020 (not 2019)"),
    "C054": ("NOT RESEARCHED: Nykaa Cosmetics not a Tab B row", "", "Not checked", ""),
    "C055": ("Launched 2021-12-30; EXITED (announced in FY25 AR)", f"S117;{ar('Dabur',25)}", "Y",
             "Dabur press release; recall had the launch right but did not know Dabur later exited the brand"),
    "C056": ("Relaunched in FY23 (RIL AR FY23 p.77); month UNCONFIRMED by primary source", ar('RIL',23), "Partial", "RIL AR confirms FY23 only"),
    "C057": ("Launched 2022-12-15 in Gujarat", "S116", "Y", "RRVL media release (T1)"),
    "C058": ("Launched 2024-03-28", "S122", "Y", "Honasa Reg 30 press release (T1)"),
    "C059": ("Rs 222.1 lakh = Rs 2.22 Cr total revenue FY26 (FY25 Rs 0.46 Cr, FY24 Rs 0.73 Cr)", "S073", "Y", "GCPL Reg 30 filing"),
}


def update_claims():
    with CLAIMS.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())
    for r in rows:
        if r["claim_id"] in VERIFY:
            r["value_verified"], r["source_id"], r["match"], r["how_caught"] = VERIFY[r["claim_id"]]
    with CLAIMS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    write_tab()
    update_claims()
