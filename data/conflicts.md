# Conflicts log

One section per conflicting figure, all in the same format. Each table row is a figure in circulation: **source (tier)**, then **what it actually measures**. Below each table: the **verdict** and the **value used in tab_a**.
Tiers follow the evidence rules in the README: T1 = exchange filing or company release; T3 = press; T4 = blog or newsletter. Source IDs point to `sources/raw/S###_*.txt`.

---

## 1. HUL – Minimalist: price

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹2,955 Cr | S007 HUL Reg 30, 2025-01-22 (T1); Entrackr and Inc42 headlines (T3) | Pre-money **enterprise value of 100%**, "subject to adjustments". A valuation, not a payment. |
| ₹2,670 Cr | S007 (T1); Storyboard18, Angel One (T3) | **Secondary cash** paid to sellers for the 90.5% stake, at announcement. |
| ₹2,706.45 Cr (₹2,706,44,95,728) | S002 HUL completion letter, 2025-04-21 (T1) | **Total cash paid at completion** for 90.5%: secondary plus the ₹45 Cr primary infusion, after adjustments. |
| ₹2,706.44 Cr | Angel One, Business Standard (T3) | The same completion figure, **truncated** instead of rounded. |

**Verdict:** No real disagreement. These are three different measures (EV, secondary price, total paid), and the press quotes them interchangeably. ₹2,706,44,95,728 = ₹2,706.4495 Cr, which rounds to 2,706.45.
**Used in tab_a:** consideration ₹2,706.45 Cr, stake 90.5%, revenue ₹347 Cr (FY24) → 8.62×. EV cross-check: 2,955 / 347 = 8.5×.

## 2. HUL – OZiva: "the price" depends on the tranche

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹264.28 Cr for 51% | S008, S005 HUL Reg 30 (T1) | First tranche (Jan 2023), primary plus secondary. Implies ~₹518 Cr for 100% (post-money). |
| ₹824 Cr for 49% | S009, S003 HUL Reg 30, Feb 2026 (T1) | Second tranche, priced on "pre-agreed valuation criteria" against FY25 turnover of ₹257.67 Cr. Implies ~₹1,682 Cr for 100%. |

**Verdict:** Both are correct. "HUL bought OZiva for ₹264 Cr" misstates the full cost, which was ₹1,088.28 Cr for 100%.
**Used in tab_a:** consideration ₹264.28 Cr, stake 51%, revenue ₹124.17 Cr (FY22) → 4.17×. The second tranche is in notes and status.

## 3. ITC – Mother Sparsh: FY25 turnover restated

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹99.6 Cr | S021 ITC Reg 30, 2025-05-21 (T1) | FY25 turnover as first reported. |
| ₹80.9 Cr | S032 ITC Reg 30, 2026-05-19 (T1) | FY25 turnover **restated** "on account of reclassification of certain expenses" (some expenses now netted off revenue). |

**Verdict:** The later restated figure is authoritative.
**Used in tab_a:** FY25 not used for the multiple. The row uses FY24 ₹58.7 Cr, which is identical in both filings. ₹80.9 Cr is cited in status.

## 4. ITC – Mother Sparsh: FY21 turnover

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹15.44 Cr | S025 ITC Reg 30, Nov 2021 (T1) | FY21 turnover, filed early in FY22 (likely provisional). |
| ₹15.57 Cr | S028 ITC Reg 30, Oct 2022 (T1) | FY21 turnover, filed a year later (likely audited). |

**Verdict:** Immaterial (0.8%). The later figure is preferred.
**Used in tab_a:** Not used; FY21 is not the revenue year for this row.

## 5. ITC – Prasuma: which revenue base

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹116 Cr (FY24) | S023 ITC Reg 30 (T1) | Ample Foods Pvt Ltd only, consolidated revenue from operations (includes sales to Meat and Spice). |
| ₹131 Cr (FY24) | S023 (T1) | The whole "Target Business": Ample Foods + Meat and Spice + Chao Chao. |

**Verdict:** Use the base that matches the entity in which the stake was bought (Ample Foods). Meat and Spice is bought only in the 2028 tranche.
**Used in tab_a:** ₹131 Cr for 43.75%, revenue ₹116 Cr → 2.58× (2.29× on the ₹131 Cr base). Separately, the memory claim of ~₹375 Cr was wrong (claims_verification_log C007).

## 6. ITC – Yoga Bar: implied valuation by tranche

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹175 Cr for 39.42% | S015 (T1) | First tranche, May 2023, primary plus secondary. Implies ~₹444 Cr for 100%. |
| ~₹225 Cr total for 44.74%; ~₹255 Cr total for ~47.50% | S016, S017 (T1) | **Cumulative** investment after the two primary-only steps (₹50 Cr, then ₹30 Cr) of the ₹80 Cr pre-agreed in the term sheet. All stakes are "on a fully diluted basis". |
| ~₹645 Cr for 52.5% | S031 (T1) | Final secondary purchase, 2026-09-28: "from ~47.50% to 100%". Implies ~₹1,229 Cr for 100%. |

**Verdict:** No disagreement. The value rose roughly 2.8× as turnover went from ₹68 Cr to ₹452 Cr. Control came at about 47.5% via board-nomination rights (S030), so the study's "control taken at sub-50%" is confirmed. Total cost of 100% is about ₹900 Cr.
**Used in tab_a:** consideration ₹175 Cr, stake 39.42%, revenue ₹68 Cr (FY22) → 6.53×.

## 7. Tata Consumer – Capital Foods: headline valuations

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹5,100 Cr | S036 TCPL Reg 30 (T1) | **EV, no cash/no debt, for 100%**. |
| "₹7,000 Cr" | Outlook Business, The Week/PTI (T3) | Capital Foods EV + Organic India EV (5,100 + 1,900) added together. Not a price. |
| "₹5,500 Cr" | Agro & Food Processing (T3) | Valuation reported **during talks**, before signing. |
| "US$616 mn" | Deccan Herald/Reuters headline (T3) | The ₹5,100 Cr EV in dollars (~₹83/$). |

**Verdict:** T1 EV of ₹5,100 Cr. The equity cash actually paid for 75% is not in the filing (UNCONFIRMED).
**Used in tab_a:** consideration ₹3,825 Cr (**derived**: 75% × EV, so Low confidence), stake 75%, revenue ₹705.5 Cr (FY23) → 7.23×.

## 8. Marico – Plix: package size

| Figure | Source (tier) | What it measures |
|---|---|---|
| Up to ₹369.01 Cr for up to 58% | S054 Marico Reg 30, 2023-07-26 (T1) | The contracted package at signing. |
| ₹380.04 Cr for 60% | S056 (T1) | The same package plus 2% bought from founders for ₹11.03 Cr (S055). |

**Verdict:** Both correct; the second includes an add-on.
**Used in tab_a:** consideration ₹369.01 Cr, stake 58%, revenue ₹106.43 Cr (FY23) → 5.98×.

## 9. Marico – True Elements: "100% for ₹138 Cr"

| Figure | Source (tier) | What it measures |
|---|---|---|
| "Marico acquires 100% stake in True Elements for Rs 138 crore" | Storyboard18 headline (T3) | Conflates the final holding (100%) with the stake bought. |
| Up to ₹138 Cr for the balance 46.02% | S052 Marico Reg 30, 2025-09-11 (T1) | Price of the **remaining** stake only. |

**Verdict:** The headline is wrong. The first-tranche price for 53.98% (2022) was never disclosed.
**Used in tab_a:** consideration blank (UNCONFIRMED), stake 53.98%, revenue ₹54.3 Cr (FY22). ₹138 Cr appears only in status.

## 10. Marico – Just Herbs: implied valuation, 2021 vs 2024 (both derived)

| Figure | Source (tier) | What it measures |
|---|---|---|
| 3.48% for ₹9.99 Cr | S048 Marico Reg 30, Nov 2022 (T1) | Tranche "as per the previously agreed pre-money enterprise valuation". Implies ~₹287 Cr for 100% on 2021 terms. |
| Up to ₹70 Cr for 40% | S049 (T1) | Final buyout, Sep 2024. Implies ~₹175 Cr for 100%. |

**Verdict:** Both arithmetic is ours and the share mix differs, so neither is used as the deal price. The pattern (a lower exit valuation even as turnover rose from ₹35 Cr to ₹96 Cr) is a note, not data.
**Used in tab_a:** consideration blank (UNCONFIRMED), stake 52.38%, revenue ₹17.25 Cr (FY21).

## 11. Dabur – Badshah: revenue multiple

| Figure | Source (tier) | What it measures |
|---|---|---|
| "around 4.5x" | S065 Dabur Reg 30 (T1) | 100% EV ₹1,152 Cr ÷ **FY23 estimated** revenue (implies ~₹256 Cr). |
| 6.1× | This workbook (derived from S065) | ₹587.52 Cr equity price for 51% ÷ **FY22 actual** turnover ₹189.1 Cr. |

**Verdict:** Different numerator (EV vs equity price before debt deduction) and different denominator (estimate vs actual). We use actuals for consistency across rows. Dabur's own figure is noted.
**Used in tab_a:** consideration ₹587.52 Cr, stake 51%, revenue ₹189.1 Cr (FY22) → 6.09×.

## 12. GCPL – Muuchstac: FY25 turnover

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹87 Cr | S071 GCPL Reg 30 (T1) | "Audited turnover as per IGAAP" (Indian GAAP), gross. |
| ₹60 Cr | S071 (T1) | "TTM turnover as per IND AS FY 2024-25", net of items Ind AS deducts from revenue (likely trade discounts). |

**Verdict:** Both from the same filing; the gap is accounting basis. The audited IGAAP figure is used, with the Ind AS multiple noted. Zydus–Naturell has the same issue: ₹128.89 Cr IGAAP vs ~₹119 Cr Ind AS (S102).
**Used in tab_a:** consideration ₹449 Cr (derived: ₹289 Cr + ~₹160 Cr tranches, Low), revenue ₹87 Cr → 5.16× (7.5× on Ind AS).

## 13. GCPL – Raymond Consumer Care: price

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹2,825 Cr | S068 GCPL Reg 30 (T1); press (T3) | Cost of acquisition including cash acquired with the business. |
| ₹2,725 Cr | S068 (T1) | The same, "ex cash acquisition from RCCL". |

**Verdict:** Both are T1. The headline figure is the stated cost of acquisition.
**Used in tab_a:** consideration ₹2,825 Cr, 100% (slump sale), sales ₹622 Cr (FY23) → 4.54× (4.38× ex cash).

---

### Not conflicts, but worth knowing (also in claims_verification_log)
- **Study scaffold, "Marico Cosmix 60% · ₹375 Cr val.":** consistent with S059. ₹225.67 Cr for 60% implies ₹376 Cr for 100%, so ₹375 Cr is a **valuation**, not the consideration.
- **Memory errors caught by filings:** Mother Sparsh (16% for ~₹20 Cr in 2021, not 22% for ₹120 Cr in 2023); Prasuma (₹131 Cr, not ₹375 Cr); Earth Rhythm (18.51%, not 51%); Cosmix (2026, not 2025).

---

# Tab B (Build) conflicts

Same format. For builds, conflicts are mostly about **dates** (launch vs relaunch, global vs India) and about **what a "size" figure measures** (ARR vs GMV vs gross sales vs consumer spend vs revenue). Annual reports (AR) are T1 and are listed by source_id in `data/source_log.csv`.

## B1. Honasa – The Derma Co: launch month

| Figure | Source (tier) | What it measures |
|---|---|---|
| March 2020 | S163 Honasa AR FY24 p.12 (T1): "Since The Derma Co's launch in March 2020" | Launch month as stated in FY24 |
| February 2020 | S165 Honasa AR FY26 p.13 (T1): "The Derma Co, launched in February 2020" | Launch month as stated in FY26 |

**Verdict:** The parent contradicts itself by one month. Both are T1, the year is the same, and the row is unaffected.
**Used in tab_b:** year_start 2020; both quotes in notes.

## B2. HUL – Love Beauty & Planet: launch year in India

| Figure | Source (tier) | What it measures |
|---|---|---|
| FY20 (Apr 2019 – Mar 2020) | S128 HUL AR FY20 p.5 (T1): "During the year, we also launched... Love, Beauty and Planet" | India launch inside FY20 |
| "introduced... in India" | S129 HUL AR FY21 p.14 (T1) | Repeats the introduction in the FY21 narrative; not a separate launch date |
| 2018 | Search-result snippets (T4) | Most likely the **2018 global (US) launch**, attributed to India |

**Verdict:** The T1 source wins: the India launch was in FY20. The month is unknown, so year_start = 2019 under the FY rule (an FY maps to the calendar year holding 9 of its 12 months), and the brand is a calibration row.
**Used in tab_b:** 2019, calibration.

## B3. HUL – Lever Ayush: launch year and "withdrawal"

| Figure | Source (tier) | What it measures |
|---|---|---|
| 2001 | Case-study write-ups found via search (T4) | Launch |
| 2002 | Same family of write-ups (T4): "launched in 2002" | Launch |
| Dec 2016 relaunch | Case studies / trade sites (T4) | Mass relaunch in five southern states |
| "momentum in the focused market - South India" | S128/S129 HUL AR FY20–21 (T1) | Alive but regional; then 0 AR mentions FY22–FY26 |

**Verdict:** No primary source for the launch year; 2001 is used and flagged Low. The "2000s pullback" is unsupported beyond T4 and is recorded as UNCONFIRMED.
**Used in tab_b:** 2001 (Low), status Niche.

## B4. Tata Sampann: "a TCPL launch"

| Figure | Source (tier) | What it measures |
|---|---|---|
| Launched by TCPL c.2017 | AI recall (C045) | — |
| Came with "the merger of the Consumer Products business of Tata Chemicals" | S149 TCPL AR FY20 p.5 (T1) | **Built by Tata Chemicals**, transferred to TCPL in FY20 |

**Verdict:** It is not a TCPL in-house build. It is kept as a calibration row (a group build by a listed Tata company), with the launch year UNCONFIRMED.
**Used in tab_b:** calibration; parent field states the origin.

## B5. "Size" figures are not revenue

| Brand | Figure | Source | What it measures |
|---|---|---|---|
| The Derma Co | ₹750 Cr+ | S165, S120 (T1) | **ARR**: annualised net revenue run-rate, company-stated |
| Aqualogica | ₹200 Cr+ | S165 (T1) | ARR |
| Godrej Fab | ~₹490 Cr | GCPL AR FY26 p.42 (T1) | ARR; FY25 "topline" >₹150 Cr |
| Kay Beauty / Nykd | ₹240 Cr / ₹150 Cr+ | S169 Nykaa AR FY25 (T1) | **GMV** (includes taxes and discounts), not revenue; FY26: Kay Beauty "₹250–350 crores **NSV**" |
| Campa | ₹4,700+ Cr | S205 RIL AR FY26 p.47 (T1) | **Gross sales** |
| Independence | ~₹2,600 Cr | S205 (T1) | "sales", basis unstated |
| Bingo! / YiPPee! | ~₹2,700 Cr / ~₹1,300 Cr | S135 ITC AR FY20 p.10 (T1) | **Annual consumer spend** (retail value), not ITC revenue |
| Tata Sampann | ₹1,109 Cr | S154 TCPL AR FY25 p.42 (T1) | Revenue as charted (basis unstated) |
| Godrej Pet Care | ₹2.22 Cr | S073 (T1) | Total revenue of the subsidiary (audited) |

**Verdict:** These cannot be compared directly. tab_b states the basis on every row (`revenue_basis`). Status calls use a threshold ("Scaled" = a disclosed size of ₹100 Cr or more on any of these bases), not cross-brand rankings.

## B6. AR silence vs live listing (method conflict)

| Brand | AR signal | Listing signal | Resolution |
|---|---|---|---|
| Tata GoFit | 0 mentions in TCPL AR FY26; dropped from brand list (S155) | tatagofit.com live; Wayback live to 2026-03 (S206) | **Niche, not Withdrawn**: first coded Withdrawn from AR silence alone, then corrected |
| Natyv Soul | 22 (FY23) → 1 → 1 → 0 mentions | Standalone store redirects to a corporate brand page (S206) | Niche |
| Bajaj Zero Grey | 0 mentions FY24–FY26 | Site live to 2025-07, dead on 2026-10-10 (S206) | Withdrawn (Low): it outlived its AR coverage by ~2 years |
| Dabur Vita | Explicit exit (Dabur AR FY25 p.25, FY26 p.85) | dabur.com brand page still resolves (S206) | Withdrawn: the parent's own exit statement outranks a residual web page |

**Verdict:** Disappearing from an annual report means a brand has been **de-prioritised**, not that it is dead. A Withdrawn call needs either a parent statement (Dabur Vita) or a dead store (Acne Squad, Find Your Happy Place, Ayuga).

---

## Model: Minimalist FY22 revenue

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹103 Cr | S007 HUL Reg 30, 2025-01-22 (T1) | FY22 "turnover of the Business" |
| ₹108 Cr | S208 Entrackr (T3, search snippet of FY23 story) | FY22 "revenue from operations" from RoC filings |

**Verdict:** Small gap, likely basis (turnover vs. revenue from operations, or standalone vs. consolidated). Not a model input; ramp uses FY24 ₹347 Cr (both agree). **Used:** ₹103 Cr (T1).

## Model: cost of the remaining 9.5% of Minimalist

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹284 Cr | Derived: 2,706.45 / 90.5 × 9.5 (S002, T1) | Pro-rata at the completion price; ignores growth |
| ₹501 Cr | S134 HUL AR FY26 Note 43(C) (T1) | PV of the forward rights (symmetric put/call) on the 9.5% NCI at acquisition date, via Other Equity |

**Verdict:** ₹501 Cr is HUL's own accounting estimate; the pro-rata figure understates it. **Used:** base ₹501 Cr, low ₹284 Cr (assumption A20).

## Model: Minimalist pro-forma FY26 revenue in HUL AR

| Figure | Source (tier) | What it measures |
|---|---|---|
| ₹652 Cr | S134 Note 43(I) (T1) | USPL revenue contributed 21 Apr 2025–31 Mar 2026 |
| ₹89 Cr | S134 Note 43(I) (T1) | "If the combination had taken place at the beginning of the year, revenue ... would have been H89 crores" — cannot be full-year revenue; most likely the incremental 1–20 Apr revenue or a drafting error |

**Verdict:** ₹89 Cr not used. **Used:** ₹652 Cr, annualised ₹690 Cr (A18).


## Heads Up For Tails revenue (recommendation)
- Rs 312.8 Cr FY23 revenue from operations (Entrackr, S215).
- Rs 199.1 Cr FY24 / Rs 236.8 Cr FY25 for Earth Paws Pvt Ltd (Inc42 data page, S216) - appears to be a narrower entity scope, so not comparable with S215.
- Rs 400 Cr ARR, company-stated run rate, Dec 2025 (Entrackr, S214) - not audited revenue.
- Resolution: The recommendation prices HUFT on a Rs 240-400 Cr revenue band (FY25 entity figure to stated ARR); Low confidence.

## Drools revenue and valuation (recommendation)
- Rs 714.90 Cr FY24 revenue from operations (Entrackr, S211). Rs 686.4 Cr in 9M FY25 (ICRA, S210), ~Rs 915 Cr annualised. FY25 full year UNCONFIRMED (a search summary said Rs 918 Cr; not found in any page - C071).
- $600M valuation (June 2023, L Catterton, ~10%, S211) vs 'unicorn' (>= $1bn) claimed after Nestle's undisclosed minority stake (May 2025, S211) - a company claim, terms undisclosed.
