"""Tab A (Buy) rows and AI-claim verifications. Run to regenerate data/tab_a.csv and update data/claims_verification_log.csv.

  python scripts/tab_a_data.py

Each row is a dict in the tab_a schema; revenue_multiple is computed here
(consideration / (stake_pct/100) / revenue) and becomes a live formula in the xlsx.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAB = ROOT / "data" / "tab_a.csv"
CLAIMS = ROOT / "data" / "claims_verification_log.csv"
ACC = "2026-10-10"
FIELDS = ["route", "row_type", "parent", "brand", "category", "year_start", "consideration_inr_cr", "stake_pct",
          "deal_structure", "revenue_inr_cr", "revenue_fy", "revenue_basis", "revenue_multiple", "what_was_acquired",
          "vocab_rationale", "status_today", "status_evidence", "source_url", "source_ids", "date_accessed",
          "confidence", "notes"]

ROWS = [
    dict(parent="Hindustan Unilever Ltd", brand="Minimalist (Uprising Science Pvt Ltd)", category="BPC-Skincare",
         year_start=2025, consideration_inr_cr=2706.45, stake_pct=90.5, deal_structure="outright_majority",
         revenue_inr_cr=347, revenue_fy="FY24",
         revenue_basis="turnover as stated in Reg 30 annexure (\"turnover of the Business\"); not labelled ops vs total income",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="HUL already sold skincare (Pond's, Lakme, Glow & Lovely); Minimalist brought the actives-led, digital-first premium cohort HUL lacked ('higher growth demand spaces').",
         status_today="Subsidiary since 2025-04-21; founders Mohit & Rahul Yadav continue to run it; balance 9.5% to be acquired",
         status_evidence="S002: 'Uprising and its subsidiaries have become subsidiaries of the Company'; S006: 'The current Minimalist team led by Mohit and Rahul will continue to operate the business'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/7ecb9005-13d6-4ea3-8cad-7fe05bffd54e.pdf",
         source_ids="S007;S002;S006", confidence="High",
         notes=("Announced 2025-01-22 (S007 p.1: 'secondary buyout for a cash consideration of INR 2670 crores at a pre-money Enterprise Valuation of INR 2955 crores (subject to adjustments as set out in the SPSA) and a primary infusion of INR 45 crores'); "
                "CCI approval 2025-03-17; completed 2025-04-21 for total cash consideration 'INR 2,706,44,95,728' incl. primary (S002 p.1) = INR 2,706.45 Cr (press rounds down to 2,706.44). consideration_inr_cr uses the completion figure. "
                "Turnover S007 p.3: 'FY 2021-22: INR 103 Crores / FY 2022-23: INR 184 Crores / FY 2023-24: INR 347 Crores'; ARR >INR 500 Cr (Dec-24 quarter, unaudited). "
                "Revenue-basis check: '~347 Cr turnover' CONFIRMED against the filing; filing calls it 'turnover', Entrackr calls it 'revenue' (same number). "
                "Remaining 9.5% 'with eventual acquisition'; press release: 'path to acquire the balance stake in two years'. Multiple on EV basis = 2955/347 = 8.5x. See conflicts.md (2,670 vs 2,706.44 vs 2,955).")),
    dict(parent="Hindustan Unilever Ltd", brand="OZiva (Zywie Ventures Pvt Ltd)", category="Wellness-Nutrition&Supplements",
         year_start=2023, consideration_inr_cr=264.28, stake_pct=51, deal_structure="outright_majority",
         revenue_inr_cr=124.17, revenue_fy="FY22", revenue_basis="revenue_from_operations ('turnover from operations')",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing calls it entry into Health & Wellbeing (VMS/plant protein), a category where HUL had no supplements business (Horlicks/Boost are health food drinks).",
         status_today="Wholly owned since 2026-02-13; balance 49% bought for INR 824 Cr; FY25 turnover INR 257.67 Cr (2.1x FY22)",
         status_evidence="S003: 'completed the acquisition' of 'the balance stake of 49%... for a total consideration of INR 824 Crores'; S009: 'turnover from operations of INR 257.67 Crores for the financial year 2024-2025'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/a9bee337-d3ac-428e-b3eb-9fe3bf141942.pdf",
         source_ids="S008;S005;S009;S003;S001", confidence="High",
         notes=("Announced 2022-12-08 (S008): agreement to acquire 100% in 2 tranches; 'Total consideration for acquisition of the first tranche: INR 264.28 Crores'; 51% first tranche, 'Balance 49.00%... after the expiry of a period of 3 years'. "
                "Completed first tranche 2023-01-11 (S005), so year_start=2023 (announced 2022). Turnover S008 p.2: 'turnover from operations of INR 124.17 Crores for the financial year 2021-2022'. "
                "Second tranche approved 2026-02-12 (S009) and completed 2026-02-13 (S003) at INR 824 Cr for 49%: implied 100% value ~INR 1,682 Cr vs ~INR 518 Cr at first tranche (264.28/0.51, post-money incl. primary). "
                "deal_structure = outright_majority (51% at first completion; contracted top-up noted, not reclassified per the what-vs-how rule).")),
    dict(parent="Hindustan Unilever Ltd", brand="Wellbeing Nutrition (Nutritionalab Pvt Ltd)", category="Wellness-Nutrition&Supplements",
         year_start=2023, consideration_inr_cr=70.00, stake_pct=19.8, deal_structure="minority_no_path",
         revenue_inr_cr=19.40, revenue_fy="FY22", revenue_basis="turnover as stated in Reg 30 annexure; not labelled ops vs total income",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Same filing language as OZiva: 'Strategic investment to enter the Health & Wellbeing category'.",
         status_today="EXITED: HUL sold entire 19.8% to USV Pvt Ltd for ~INR 307 Cr (completed 2026-03-04); FY25 revenue from ops INR 118.48 Cr",
         status_evidence="S011: 'completed the sale of its entire shareholding in Nutritionalab, for a total consideration of approx. INR 307 Crores'; S009 Annexure 2: 'revenue from operations of Nutritionalab... for the financial year 2024-25 is INR 118.48 crores'",
         source_url="https://bseindia.com/xml-data/corpfiling/AttachHis/52af87d5-25a4-45c8-aad3-78626bd1a474.pdf",
         source_ids="S001;S012;S009;S011", confidence="High",
         notes=("Announced 2022-12-08 (S001 p.3: 'INR 70.00 Crores for the acquisition of proposed stake'; 'agreed to acquire 19.8% shareholding'); completed 2023-01-04 (S012). "
                "Turnover S001 p.3: FY22 19.40 / FY21 5.33 / FY20 2.14 (INR Cr). Accounted as a joint venture under the equity method (S009). "
                "deal_structure = minority_no_path (non-controlling stake rule): a 19.8% stake with no disclosed option or schedule to increase; minority_with_path needs rights to increase, and none were found. "
                "Arguably an investment, not an acquisition; kept as a core row because it shows the exit route (bought 70, sold ~307 = ~4.4x in ~3 years).")),
    # ---------------- ITC ----------------
    dict(parent="ITC Ltd", brand="Yoga Bar (Sproutlife Foods Pvt Ltd)", category="Food-Snacks&Bars",
         year_start=2023, consideration_inr_cr=175, stake_pct=39.42, deal_structure="staged_to_control",
         revenue_inr_cr=68, revenue_fy="FY22", revenue_basis="turnover as stated in Reg 30 enclosure; not labelled ops vs total income",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="ITC already sold packaged snacks/biscuits; filing says the deal adds 'innovative food products for health conscious consumers' via a digital-first brand, a cohort ITC lacked.",
         status_today="Wholly owned since 2026-09-28; subsidiary (board control) from 2026-04-01; turnover FY26 INR 452 Cr (6.6x FY22)",
         status_evidence="S031: 'the Company now holds 100% of the entire share capital of Sproutlife'; 'Cost of acquisition... ~ ₹ 645 crores'; 'turnover (based on audited accounts) 2025-26 INR 452 crores 2024-25 INR 200 crores 2023-24 INR 108 crores'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/2919b815-f54c-41e2-894d-65994e51f770.pdf",
         source_ids="S013;S014;S015;S016;S017;S030;S031", confidence="High",
         notes=("Term sheet 2023-01-17 (S013); SSPA executed 2023-04-19 (S014); first tranche completed 2023-05-04: 'aggregate consideration of Rs. 175 crores... aggregates 39.42%' (S015). "
                "Plan (S013 Annexure): 175 Cr for 39.4% + 80 Cr primary by Mar-2025 to reach 47.5%, balance to 100% on pre-agreed valuation criteria. "
                "Path - all stakes are stated 'on a fully diluted basis'; no undiluted figure is disclosed. 44.74% and 47.50% are NOT separate deals: they are the two primary-infusion steps of the ~Rs 80 Cr agreed up-front in the term sheet (S013 Annexure: 'Acquisition of 47.5%... Initial Investment of Rs 175 crores... for acquisition of 39.4%... Further infusion of Rs 80 crores will be made through primary subscription, in one or more tranches, by 31st March, 2025... based on pre-agreed pre-money valuation'). Step 1, 2024-03-11 (S016): 2,356 CCPS for '~ Rs. 50 crores' -> 'aggregates 44.74%... (on a fully diluted basis) at a total investment of ~ Rs. 225 crores'. Step 2, 2024-09-25 (S017): 1,413 CCPS for '~ Rs. 30 crores' -> 'aggregates ~ 47.50%... at a total investment of ~ Rs. 255 crores'. CONTROL AT SUB-50% (the study's note): on 2026-04-01, still at ~47.50%, ITC 'acquired the right to nominate majority of the Directors on the Board of Sproutlife' under the 2023 SHA, so Sproutlife became a subsidiary under Section 2(87)(i) (S030). The 52.5% = 100% - 47.50%: bought 2026-09-28 from the remaining holders by secondary purchase for '~ ₹ 645 crores', taking ITC 'from ~ 47.50% to 100%' (S031). "
                "Total cost of 100% ~INR 900 Cr. Implied 100% value at first tranche ~444 Cr (post-money) vs ~1,358 Cr at the final tranche (645/0.525). "
                "Turnover S013 p.4: '2021-22 Rs 68 crores 2020-21 Rs 39 crores 2019-20 Rs 32 crores'.")),
    dict(parent="ITC Ltd", brand="Mother Sparsh (Mother Sparsh Baby Care Pvt Ltd)", category="BPC-Baby&Mother",
         year_start=2025, consideration_inr_cr=50.6, stake_pct=12.97, deal_structure="staged_to_control",
         revenue_inr_cr=58.7, revenue_fy="FY24", revenue_basis="turnover as stated in Reg 30 enclosure; not labelled ops vs total income",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filings frame it as access to baby care / D2C ayurvedic personal care; no ITC baby-care brand is named in any filing (INFERRED: ITC's personal care brands are adult soaps, fragrances, skincare).",
         status_today="Associate at 49.32% (2026-05-19); FY26 turnover INR 138.5 Cr; balance to 100% by Q1 FY2027-28 (extendable to Q1 FY2028-29)",
         status_evidence="S032: 'shareholding in Mother Sparsh has increased from 39.47% to 49.32%'; 'turnover 2025-26 INR 138.5 crores 2024-25 INR 80.9 crores *'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/eb24ba27-a9eb-42ca-b4dd-29312337bdcf.pdf",
         source_ids="S020;S021;S032;S025;S026;S027;S028;S029;S018;S019", confidence="High",
         notes=("Row = the CONTROL deal: SSPA executed 2025-04-17 to acquire the balance 73.5% (S020); first tranche completed 2025-05-21: 'aggregate consideration of approx. Rs 50.6 crores', stake 26.50% -> 39.47% (S021), so stake_pct = 12.97 incremental. "
                "Plan (S020 p.16): ~Rs 81 Cr in two tranches to reach up to 49.3% (total investment ~Rs 126 Cr), then balance to 100% by Q1 FY2027-28 on pre-agreed criteria. Second tranche ~Rs 30 Cr -> 49.32% on 2026-05-19 (S032). "
                "PRIOR MINORITY ENTRY (not counted in this row): 16% agreed 2021-11-26 for '~ Rs 20 crores' (S025), completed in two tranches 2021-12 (8.70%, S026) and 2022-03-15 (16%, S027); to 22% for ~Rs 13.50 Cr (2022-10-27, S028/S029); to 26.50% for ~Rs 11.54 Cr (2023-06-27, S018/S019). "
                "Multiple caveat: 50.6 Cr includes primary subscription, so implied value is post-money. Turnover restated: FY25 Rs 99.6 Cr (S021) vs Rs 80.9 Cr restated (S032). See conflicts.md.")),
    dict(parent="ITC Ltd", brand="24 Mantra Organic (Sresta Natural Bioproducts Pvt Ltd)", category="Food-Staples&Organic",
         year_start=2025, consideration_inr_cr=472.5, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr=306.1, revenue_fy="FY24", revenue_basis="consolidated turnover as stated in Reg 30 annexure; not labelled ops vs total income",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="ITC was already in staples (filing: deal will 'fortify ITC's presence'); 24 Mantra brought the organic shopper and US Indian-diaspora franchise (~50% revenue international). Tie-break over CAPABILITY (27,500-farmer organic sourcing base).",
         status_today="Wholly owned from 2025-06-13; amalgamated into ITC Ltd (NCLT-sanctioned, appointed date 2025-06-13), so no longer a separate entity",
         status_evidence="S022: 'SNBPL has become a wholly owned subsidiary of the Company'; S033: 'Scheme of Amalgamation of Sresta Natural Bioproducts Private Limited... with the Company... has been sanctioned'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/eb24ba27-a9eb-42ca-b4dd-29312337bdcf.pdf",
         source_ids="S020;S022;S033", confidence="High",
         notes=("Announced 2025-04-17 (S020): 'Consideration of up to Rs 472.50 crores on a cash-free debt-free basis... comprising Rs 400 crores payable upfront at Closing and up to Rs 72.50 crores payable in the next 24 months'. Presentation: 'Additional Founders Consideration of up to Rs. 72.5 cr... basis pre-agreed criteria'; founder Raj Seelam stays 2 years. "
                "Completed 2025-06-13 (S022). consideration_inr_cr = the maximum 472.5 (upfront 400 + earn-out); upfront-only multiple = 400/306.1 = 1.31x. "
                "Turnover S020 p.4 (consolidated): '2023-24 Rs 306.1 crores 2022-23 Rs 327.3 crores 2021-22 Rs 326.7 crores' - flat-to-declining before the deal. Earn-out not counted as FOUNDER_TEAM: price is 1.5x revenue, so people are not the primary asset (what-vs-how rule).")),
    dict(parent="ITC Ltd", brand="Prasuma (Ample Foods Pvt Ltd)", category="Food-Frozen&ReadyToCook",
         year_start=2025, consideration_inr_cr=131, stake_pct=43.75, deal_structure="staged_to_control",
         revenue_inr_cr=116, revenue_fy="FY24", revenue_basis="revenue_from_operations (AFPL consolidated, sales to third parties incl. sales to MSPL)",
         what_was_acquired="CAPABILITY",
         vocab_rationale="ITC already had frozen foods (Master Chef, 2019); release cites 'Prasuma's strength in manufacturing and innovation' and first-to-market products (momos, baos) to build a 'full stack' portfolio. Judgement call vs REVENUE_SCALE.",
         status_today="Associate at 43.75%; next secondary (~Rs 56 Cr to 62.5%) due by Apr 2027; 100% by 2028-06-30",
         status_evidence="S024: 'shareholding in AFPL aggregates 43.75% of its share capital'; no later Reg 30 update found on BSE to 2026-10-10",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/a8097585-aeec-49ae-9525-cebf604d1aaf.pdf",
         source_ids="S023;S024", confidence="High",
         notes=("Announced 2025-02-06 (S023); first tranche completed 2025-04-04: 'aggregate consideration of approx. Rs 131 crores... aggregates 43.75%' (S024). "
                "Plan (S023 Annexure): ~Rs 131 Cr for 43.8%; ~Rs 56 Cr secondary to 62.5% by Apr-2027; balance 37.5% of AFPL plus 100% of Meat and Spice Pvt Ltd (MSPL, owns ~43% of AFPL) by 2028-06-30 on pre-agreed criteria. "
                "Revenue: AFPL FY24 Rs 116 Cr used (stake is in AFPL); 'Target Business' (AFPL+MSPL+Chao Chao) FY24 Rs 131 Cr -> multiple 2.29x on that basis. ARR ~Rs 200 Cr (trailing 3 months, Feb-2025 release). "
                "Category 'Food-Frozen&ReadyToCook' added to the taxonomy: no existing bucket fits frozen/chilled meats and momos.")),
    # ---------------- Tata Consumer Products ----------------
    dict(parent="Tata Consumer Products Ltd", brand="Soulfull (Kottaram Agro Foods Pvt Ltd)", category="Food-Snacks&Bars",
         year_start=2021, consideration_inr_cr=155.8, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr=39.38, revenue_fy="FY20", revenue_basis="turnover as stated in Reg 30 annexure; not labelled ops vs total income",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing: deal is in line with TCPL's 'strategic intent of entering into new adjacent categories'; TCPL had no breakfast cereals or millet snacks.",
         status_today="Renamed Tata Consumer Soulfull, then amalgamated into Tata Consumer Products Ltd (scheme effective 2024-09-01); brand continues as Tata Soulfull",
         status_evidence="S044: 'has now been re-named to Tata Consumer Soulfull'; S042 headline: 'Scheme Of Amalgamation Of Nourishco Beverages Limited (NCBL), Tata Smartfoodz Limited (TSFL) And Tata Consumer Soulfull...'; 'the Effective Date of the Scheme is September 1, 2024'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/6b5c78ca-543a-4181-8f13-c0b10991f345.pdf",
         source_ids="S034;S035;S042;S044", confidence="High",
         notes=("Announced 2021-02-02 (S034): 'Consideration of INR 155.8 cr. In addition, the promoters are entitled to a contingent consideration, which is payable upon the business achieving certain operational and financial milestones over a period of 5 years.' Completed 2021-02-20 (S035). "
                "Turnover S034 p.3: 2019-20 INR 39.38 Cr; 2018-19 INR 21.58 Cr (OCR reads '2L58'); 2017-18 INR 11.08 Cr; net worth 31-Mar-2020 INR -6.26 Cr. "
                "Contingent consideration amount UNCONFIRMED: not disclosed. Post-deal Soulfull revenue UNCONFIRMED: not separately disclosed after amalgamation.")),
    dict(parent="Tata Consumer Products Ltd", brand="Ching's Secret / Smith & Jones (Capital Foods Pvt Ltd)", category="Food-Ethnic&Condiments",
         year_start=2024, consideration_inr_cr=3825, stake_pct=75, deal_structure="outright_majority",
         revenue_inr_cr=705.5, revenue_fy="FY23", revenue_basis="revenue_from_operations",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing: 'entering into new adjacent high growth/ attractive margin categories'; TCPL (tea, coffee, salt, pulses) had no sauces, chutneys or Desi-Chinese condiments.",
         status_today="Subsidiary; stake 80% after buying 5% from Wildflower Private Trust on 2026-09-01; 20% still to be acquired (3-year window from 2024-02-01)",
         status_evidence="S038: 'the Company now holds 27,95,533 equity shares... (representing 80% of the paid-up equity share capital of Capital Foods)'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/4c77fffc-daff-4dad-8633-13be1e459dfe.pdf",
         source_ids="S036;S037;S038;S043", confidence="Low",
         notes=("Announced 2024-01-12 (S036): 'Enterprise value on no cash/no debt basis for 100% of the Target Company is INR 5,100 crores'; 75% upfront, balance 25% within 3 years. Completed 75% on 2024-02-01 (S037). "
                "consideration_inr_cr 3,825 is DERIVED (75% x INR 5,100 Cr EV): the equity cash paid for 75% is not in the Reg 30 filing, hence Low confidence under the rules; EV, stake and revenue are all T1. Multiple = EV/FY23 revenue = 7.2x. "
                "Revenue S036 p.4: 'Revenue from operations: FY 2022-23 Rs. 705.5 crores FY 2021-22 Rs. 574.2 crores FY 2020-21 Rs. 666.7 crores'; FY24 estimated 'approximately Rs. 750 to 770 crores' (S036 p.2). "
                "UNCONFIRMED: equity consideration paid for 75% (try TCPL FY24 annual report business-combination note); price of the 2026 5% top-up (BW Retail World S043: 'did not disclose the value').")),
    dict(parent="Tata Consumer Products Ltd", brand="Organic India (Organic India Pvt Ltd)", category="Wellness-Nutrition&Supplements",
         year_start=2024, consideration_inr_cr=1900, stake_pct=99.99, deal_structure="full_100",
         revenue_inr_cr=324.4, revenue_fy="FY23", revenue_basis="revenue_from_operations (consolidated)",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing: 'entering into new adjacent... categories' and 'will enable creation of health and wellness platform'; TCPL sold tea but not herbal supplements. Herbal infusions overlap TCPL tea, so COHORT_EQUITY is the runner-up.",
         status_today="Wholly owned subsidiary since 2024-12-13 (99.99% from 2024-04-16)",
         status_evidence="S041: 'completed the acquisition of the remaining 8,750 equity shares... thereby making Organic India a wholly owned subsidiary of the Company'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/28441e71-335d-47a6-a86e-2bff25286d57.pdf",
         source_ids="S039;S040;S041", confidence="High",
         notes=("Announced 2024-01-12 (S039): 'Enterprise value on no cash/no debt basis for 100% of the Target Company is Rs. 1,900 crores along with an additional earnout for the shareholders linked to FY2025-26 audited financials'. Seller: Fabindia Ltd. "
                "Completed 99.99% on 2024-04-16 (S040); remaining 8,750 shares 2024-12-13 (S041). consideration_inr_cr = disclosed EV (equity value not disclosed); earn-out amount UNCONFIRMED. "
                "Revenue S039 p.4: 'Revenue from operations (consolidated) FY22-23 Rs. 324.4 crores FY21-22 Rs. 361.8 crores FY20-21 Rs. 394.8 crores' - declining before the deal; FY24 estimated 'approximately Rs. 360 to 370 crores'. "
                "deal_structure full_100: 99.99% at first completion.")),
    # ---------------- Marico ----------------
    dict(parent="Marico Ltd", brand="Beardo (Zed Lifestyle Pvt Ltd)", category="BPC-MensGrooming",
         year_start=2020, consideration_inr_cr="", stake_pct=55, deal_structure="full_100",
         revenue_inr_cr=78.50, revenue_fy="FY20", revenue_basis="turnover as stated in Reg 30 annexure (INR 78,49,85,170); not labelled ops vs total income",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Marico already sold men's styling (Set Wet, Parachute Advansed Men - INFERRED, not in filing); Beardo brought the young, online beard-grooming cohort. The 2020 step-up itself is about 'complete control'.",
         status_today="Wholly owned since 2020-06-30; FY25 turnover INR 214.17 Cr (2.7x FY20); business being moved into Marico Ltd via voluntary liquidation of Zed Lifestyle (announced 2026-01-27)",
         status_evidence="S064: 'Zed's financial details... Turnover 214.17 1.98%' (contribution to consolidated); 'Distribution of business undertaking of Zed on a going concern basis'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/9bdee60f-06e1-4486-a933-6c890b79602a.pdf",
         source_ids="S045;S064;S063", confidence="High",
         notes=("Row = the 2020 control step: 'The Company has now acquired the balance equity stake of 55%' on 2020-06-30, holding 45% since March 2017 (S045). The 2017 entry is pre-2020; it could be a calibration row in Tab A. "
                "consideration_inr_cr UNCONFIRMED: 'pre-money enterprise valuation has not been disclosed herein due to reasons of confidentiality' (S045); press also reports 'undisclosed sum'. "
                "Turnover S045 p.3: FY20 INR 78.50 Cr; FY19 INR 48.24 Cr; FY18 INR 22.66 Cr. deal_structure full_100 because holding reached 100% at this completion (55% bought on top of 45%).")),
    dict(parent="Marico Ltd", brand="Just Herbs (Apcos Naturals Pvt Ltd)", category="BPC-Skincare",
         year_start=2021, consideration_inr_cr="", stake_pct=52.38, deal_structure="outright_majority",
         revenue_inr_cr=17.25, revenue_fy="FY21", revenue_basis="turnover as stated in later Reg 30 annexure (FY21 INR 17.25 Cr; 'approx. revenue' INR 17.5 Cr unaudited at signing)",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Marico had personal care; filing says the deal lets it participate 'in the premium, natural and ayurvedic beauty segment' and the D2C channel, a cohort its mass brands lacked.",
         status_today="Wholly owned since 2024-09-17 (balance 40% for up to INR 70 Cr); FY24 turnover INR 96.03 Cr (5.6x FY21)",
         status_evidence="S049: 'Aggregate consideration of upto Rs. 70 Crores towards acquisition of balance 40% equity stake'; 'FY 2023 - 24 96.03'; S050: 'the transaction has been completed today'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/b14ca7a2-bf6b-4ee2-be75-9db8bae2c8f4.pdf",
         source_ids="S046;S047;S048;S049;S050", confidence="High",
         notes=("Signed 2021-07-14 (S046): 60% via equity + CCPS; 52.4% by 2021-07-31 (subsidiary), balance 7.6% by 2023-03-31. Path: 52.38% -> 56.52% (2022-07-04, S047) -> 60% (2022-11-11, 'Rs. 9.99 crores for... additional equity stake of 3.48%', S048) -> 100% (2024-09-17, up to Rs 70 Cr for 40%, S049/S050). "
                "consideration_inr_cr UNCONFIRMED: first-tranche price not disclosed ('pre-money enterprise valuation has not been disclosed herein due to reasons of confidentiality'). "
                "DERIVED, not used: 9.99/0.0348 implies ~INR 287 Cr for 100% at the 2021 agreed pre-money valuation (~16x FY21 turnover) - treat with caution, tranche may include a different primary/secondary mix. "
                "Final 40% at up to 70 Cr implies ~175 Cr for 100% in 2024 (1.8x FY24 turnover) - lower than the 2021-agreed valuation. year_start=2021 (first completion by 2021-07-31).")),
    dict(parent="Marico Ltd", brand="True Elements (HW Wellness Solutions Pvt Ltd)", category="Food-Snacks&Bars",
         year_start=2022, consideration_inr_cr="", stake_pct=53.98, deal_structure="outright_majority",
         revenue_inr_cr=54.3, revenue_fy="FY22", revenue_basis="turnover as stated in Reg 30 annexure (unaudited at the time)",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Marico already sold breakfast (Saffola Oats - INFERRED, not in filing); filing says the deal expands its 'presence in the healthy foods segment' with a digital-first brand, i.e. the online health-food cohort.",
         status_today="Wholly owned since 2025-10-17 (balance 46.02% for up to INR 138 Cr); FY25 turnover INR 164.38 Cr (3.0x FY22)",
         status_evidence="S052: 'Aggregate consideration of upto Rs. 138 Crores towards acquisition of balance 46.02%'; 'FY 2024 - 25 164.38'; S053: 'completed the aforesaid acquisition on October 17, 2025... True Elements has become a wholly owned subsidiary'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/27472172-f501-43b4-bfea-2d22eda5b637.pdf",
         source_ids="S051;S052;S053", confidence="High",
         notes=("Completed 2022-05-23 (S051): 'acquired 53.98% of the paid-up share capital of HW Wellness and it has accordingly become a subsidiary'. "
                "consideration_inr_cr UNCONFIRMED: 'mutually agreed pre-money enterprise valuation... has not been disclosed herein due to reasons of confidentiality'. "
                "Turnover S051: FY22 54.3 (unaudited), FY21 36.3, FY20 16.5 (INR Cr). Balance 46.02% at up to 138 Cr implies ~300 Cr for 100% in 2025 (1.8x FY25 turnover). "
                "Storyboard18 headline 'Marico acquires 100% stake in True Elements for Rs 138 crore' (T3, seen via search, NOT saved; not relied on) misstates it: 138 Cr bought the remaining 46.02%, not 100%.")),
    dict(parent="Marico Ltd", brand="Plix (Satiya Nutraceuticals Pvt Ltd)", category="Wellness-Nutrition&Supplements",
         year_start=2023, consideration_inr_cr=369.01, stake_pct=58, deal_structure="staged_to_control",
         revenue_inr_cr=106.43, revenue_fy="FY23", revenue_basis="turnover as stated in Reg 30 annexure; later filings call it consolidated turnover",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing: deal expands 'presence in the rapidly growing Health & Wellness category' (plant-based supplements/ACV gummies), where Marico had no material revenue (INFERRED: Saffola's wellness extensions were small).",
         status_today="Subsidiary at 84.09% (2026-10-05, INR 1,012.03 Cr for 24.09%); FY26 consolidated turnover INR 864.31 Cr (8.1x FY23); last 14.09% due July 2027",
         status_evidence="S058: 'Consideration of INR 1,012.03 Crores towards current tranche of acquisition of 24.09% stake'; 'FY 2025 - 26 864.31'; 'aggregate consideration for acquisition of 84.09% stake... stands at INR 1,392.07 Crores'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/32224d77-4090-4b97-9c64-a9b3319a3b5e.pdf",
         source_ids="S054;S055;S056;S057;S058", confidence="High",
         notes=("Signed and first tranche completed 2023-07-26 (S054): 32.75% 'and requisite majority control over the Board composition/total voting rights', i.e. subsidiary from day one; 'Aggregate Consideration of upto Rs. 369.01 Crores towards acquisition of 58%'. "
                "consideration/stake = the contracted 58% package (first-tranche price alone not disclosed). Path: 51.20% (2023-11-30; +2% from founders for Rs 11.03 Cr, package now 60% for Rs 380.04 Cr, S055/S056); 60% (2025-05-31, S056); agreement amended 2025-12-17 to change timing of the 40% (S057); 84.09% (2026-10-05, S058); remaining 14.09% 'will be acquired in July 2027' for 'up to INR 592 Crores and additional consideration subject to milestones' (S058). "
                "Implied 100% value: ~636 Cr (2023) vs ~4,201 Cr (2026 tranche, 1012.03/0.2409). Turnover: FY21 10.92, FY22 41.58, FY23 106.43, FY24 155.32, FY25 432.84, FY26 864.31 (INR Cr). "
                "deal_structure staged_to_control: first tranche 32.75% (<=50%) with contracted tranches to majority, even though board control came at once.")),
    dict(parent="Marico Ltd", brand="Cosmix (Cosmix Wellness Pvt Ltd)", category="Wellness-Nutrition&Supplements",
         year_start=2026, consideration_inr_cr=225.67, stake_pct=60, deal_structure="outright_majority",
         revenue_inr_cr=50.93, revenue_fy="FY25", revenue_basis="turnover 'Calculated as per Indian GAAP' (Reg 30 annexure)",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Marico was already in wellness via Plix; filing cites 'a digital-first functional wellness brand with a distinct and compelling proposition', i.e. another consumer cohort, not a new category.",
         status_today="Subsidiary at 60% since 2026-02-05; Marico has a right to buy the rest after FY29",
         status_evidence="S060: 'transaction has been completed on February 5, 2026 and consequently Cosmix Wellness has become a subsidiary'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/01fbc9b3-3e17-4de2-8d46-4228c8de2550.pdf",
         source_ids="S059;S060", confidence="High",
         notes=("Signed 2026-02-04 (S059): 'Aggregate consideration of Rs. 225.67 crores towards acquisition of 60%' via secondary buy-out from founders; 'right to acquire the remaining stake in Cosmix Wellness after completion of FY29'. Completed 2026-02-05 (S060). "
                "Turnover: FY25 50.93, FY24 24.32, FY23 5.39 (INR Cr, Indian GAAP); 'Last 6 months ARR as per IndAS (Aug 2025 to Jan 2026): ~Rs. 100 crores'. "
                "Memory said 2025 completion (C014): actual is 2026. Remaining-stake right is an option, not a committed schedule; noted, not reclassified.")),
    dict(parent="Marico Ltd", brand="4700BC (Zea Maize Pvt Ltd)", category="Food-Snacks&Bars",
         year_start=2026, consideration_inr_cr=226.83, stake_pct=93.27, deal_structure="outright_majority",
         revenue_inr_cr=98.66, revenue_fy="FY25", revenue_basis="turnover as stated in Reg 30 annexure; not labelled ops vs total income",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Marico already sold healthy snacks (True Elements); filing cites 'a gourmet snacking brand with a differentiated premium positioning', i.e. the premium/gourmet snacking cohort.",
         status_today="Subsidiary at 93.27% since 2026-01-29; founder retains a stake; Marico can buy it after 3 years",
         status_evidence="S062: 'the aforesaid transaction has been completed on January 29, 2026 and consequently Zea Maize has become a subsidiary'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/1e497d48-0c27-4c5b-811c-7658d2bfbf12.pdf",
         source_ids="S061;S062;S063", confidence="High",
         notes=("NEW (not in the lead list). Signed 2026-01-26 (S061): 'Aggregate consideration of up to Rs. 226.83 Crores towards acquisition of 93.27%' bought from PVR INOX Ltd, the listed former parent, so this is listed-to-listed and the brand was itself a corporate buy-and-build. Completed 2026-01-29 (S062). "
                "Turnover: FY25 98.66, FY24 75.29, FY23 48.47 (INR Cr); 'Last 3 months ARR (Oct to Dec 2025): ~Rs. 140 crores'. Seller-side view: PVR INOX's exit is a data point for the cinema-snacks-to-retail brand route.")),
    # ---------------- Dabur ----------------
    dict(parent="Dabur India Ltd", brand="Badshah Masala (Badshah Masala Pvt Ltd)", category="Food-Ethnic&Condiments",
         year_start=2023, consideration_inr_cr=587.52, stake_pct=51, deal_structure="outright_majority",
         revenue_inr_cr=189.1, revenue_fy="FY22", revenue_basis="turnover as stated in Reg 30 annexure; not labelled ops vs total income",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Dabur had no branded spices business; Badshah (ground and blended spices) gave it entry into the masala category (INFERRED: filing gives no rationale beyond the business description).",
         status_today="Subsidiary at 51% since 2023-01-02; balance 49% due after 5 years (~2028); Badshah portfolio +12% in Q4 FY26",
         status_evidence="S066: 'Badshah Masala Private Limited has become a subsidiary of Dabur India Limited w.e.f. today i.e. 2nd January 2023'; S076 (T3): 'The Badshah portfolio increased 12% during the quarter' (Q4 FY26)",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/479e8327-282f-4bb6-9a41-a7d3ffb13143.pdf",
         source_ids="S065;S066;S076", confidence="High",
         notes=("Announced 2022-10-26 (S065): 'Cost of Acquisition of 51% equity shareholding has been agreed at INR 587.52 crore less proportionate debt as on the closing date (100% enterprise valuation being INR 1152 crore which translates to Revenue multiple of around 4.5x and EBIDTA multiple of around 19.6x of FY2022-23 estimated financials)'; balance 49% 'after a period of five years'. "
                "Completed 2023-01-02 (S066), so year_start=2023 (announced 2022). Turnover: 'Turnover for FY 21-22 - INR 189.1 crore'. "
                "Multiple here = 6.1x on FY22 actuals vs Dabur's own '4.5x' on FY23 estimates (see conflicts.md). The 587.52 is before deducting proportionate debt, so the actual cash paid may be lower: UNCONFIRMED.")),
    dict(parent="Dabur India Ltd", brand="Sesa (Sesa Care Pvt Ltd)", category="BPC-Haircare",
         year_start=2026, consideration_inr_cr=320, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr=133.3, revenue_fy="FY24", revenue_basis="consolidated turnover as stated in Reg 30 annexure",
         what_was_acquired="REVENUE_SCALE",
         vocab_rationale="Dabur is 'a market leader in the hair oils category' (its own release); Sesa is #3 in ayurvedic hair oil, so the deal mainly adds share in a category and cohort Dabur already owns.",
         status_today="Merger into Dabur sanctioned by NCLT on 2026-09-24; Sesa Care to be dissolved; Dabur shares issued to Sesa shareholders (True North)",
         status_evidence="S075/S074: NCLT 'pronounced the order sanctioning the Scheme of Amalgamation between Sesa Care Private Limited... and Dabur India Limited' (2026-09-24); 'There is no cash consideration involved in the Scheme'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/cadeef7a-138a-4e88-abf5-2285a34d9383.pdf",
         source_ids="S067;S074;S075", confidence="Low",
         notes=("NEW (not in the lead list). Implementation agreement 2024-10-30 (S067): Dabur buys 51% of Sesa's cumulative redeemable preference shares for Rs 12.59 Cr at face value and guarantees Rs 289 Cr of Sesa debt; equity and remaining CRPS then swapped into Dabur shares on merger. "
                "'Enterprise value of the Target Company (including debt of INR 289 crs.) is estimated to be in the range of INR 315-325 crs'; presentation: 'EV/ Sales: 2.4x and EV/ EBITDA: 19-20x'. "
                "consideration_inr_cr 320 = DERIVED midpoint of the disclosed EV range (hence Low); it is EV, mostly assumed debt, not cash. Share-swap ratios set 2025-05-26 (S074). "
                "year_start=2026: equity changes hands only when the merger becomes effective (NCLT sanction 2026-09-24; effective date UNCONFIRMED). Turnover: FY24 133.3, FY23 130.3, FY22 111.9 (INR Cr), i.e. near-flat. Seller: True North (PE), which bought the business from Ban Labs in 2018.")),
    # ---------------- Godrej Consumer Products ----------------
    dict(parent="Godrej Consumer Products Ltd", brand="Park Avenue (FMCG) & KamaSutra (Raymond Consumer Care FMCG business)", category="BPC-MensGrooming",
         year_start=2023, consideration_inr_cr=2825, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr=622, revenue_fy="FY23", revenue_basis="'historical reported sales' as stated in Reg 30 annexure",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="GCPL calls deodorants and sexual wellness 'under-penetrated categories' that 'complement our business portfolio'; it had no sexual-wellness brand and only a small deo presence (INFERRED: Cinthol deo).",
         status_today="Integrated into GCPL (slump sale, completed 2023-05-08); post-deal brand sales not separately disclosed",
         status_evidence="S069: 'the Company has now completed this acquisition'. Post-deal performance UNCONFIRMED.",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/09aaabc3-d276-44a4-b240-f217c79c7333.pdf",
         source_ids="S068;S069", confidence="Medium",
         notes=("VERIFICATION 2026-10-10: stake_pct 100 is inferred from the deal type (slump sale of the whole business); the Reg 30 field 'Percentage of shareholding / control acquired' reads 'NA' (S068), so the row is downgraded from High to Medium. Consideration and revenue are verbatim T1. "
                "Announced 2023-04-27 (S068): 'Cost of acquisition Rs. 2825 Crore / Rs. 2725 Crore (ex cash acquisition from RCCL)'; slump sale of the FMCG business with the Park Avenue (FMCG category), KS, KamaSutra and Premium trademarks. Completed 2023-05-08 (S069). "
                "Sales: 'FY21- Rs. 411 crore FY22- Rs. 522 crore FY23- Rs. 622 crore'. Multiple 4.5x (4.4x ex cash). Seller Raymond Ltd is itself listed, so this is a listed-to-listed carve-out. "
                "Category judgement: Park Avenue deodorants are the bigger part; if GCPL's Cinthol deo is judged 'meaningful', the label becomes REVENUE_SCALE (deos) + CATEGORY_ENTRY (sexual wellness).")),
    dict(parent="Godrej Consumer Products Ltd", brand="Muuchstac (Triology Solutions Pvt Ltd FMCG business)", category="BPC-MensGrooming",
         year_start=2025, consideration_inr_cr=449, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr=87, revenue_fy="FY25", revenue_basis="'Audited turnover as per IGAAP' (Ind AS TTM FY25 = INR 60 Cr; see notes)",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="GCPL already sold men's grooming (Park Avenue, Cinthol); Muuchstac brought the young, online men's face-wash cohort.",
         status_today="Integrated into GCPL (slump sale completed 2025-11-10); second-tranche payment (~INR 160 Cr) due ~12 months after signing, i.e. late 2026",
         status_evidence="S072: 'the said acquisition has been completed today' (2025-11-10)",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/d84288eb-224d-4315-8ca8-0327ab543ee2.pdf",
         source_ids="S071;S072", confidence="Low",
         notes=("NEW (not in the lead list). Signed 2025-10-31 (S071): '100% of Business acquired via slump sale. Tranche 1 cash payment (signing date): Rs 289 crore (EV @ ~Rs 380 Crore); Tranche 2 cash payment (post 12 months): Approx. Rs 160 crore (EV @ ~Rs 400-500 Crore)'. Completed 2025-11-10 (S072). "
                "consideration_inr_cr 449 = 289 + ~160 (approximate, valuation-linked second tranche), hence Low; tranche-1-only multiple = 3.3x on 87. "
                "Turnover: 'Audited turnover as per IGAAP FY 2022-23 19 Crore FY 2023-24 12 Crore FY 2024-25 87 Crore'; 'TTM turnover as per IND AS FY 2024-25 60 Crore; TTM September 2025 80 Crore'. IGAAP vs Ind AS gap (87 vs 60) logged in conflicts.md; on Ind AS the multiple is 7.5x.")),
    # ---------------- Nykaa (FSN E-Commerce Ventures) ----------------
    dict(parent="FSN E-Commerce Ventures Ltd (Nykaa)", brand="Dot & Key (Dot and Key Wellness Pvt Ltd)", category="BPC-Skincare",
         year_start=2021, consideration_inr_cr="", stake_pct=51, deal_structure="outright_majority",
         revenue_inr_cr="", revenue_fy="FY21", revenue_basis="",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Nykaa was a retailer with small private labels; Dot & Key was its 'first direct to customer (D2C) beauty brand acquired' (S088), giving it an owned skincare brand. Entry into owning a scaled brand, not into selling skincare (judgement call vs COHORT_EQUITY).",
         status_today="Subsidiary at 90% since 2024-09-20 (39% bought for up to INR 265.3 Cr); FY24 revenue INR 198.3 Cr (7.2x FY22); founders still run it",
         status_evidence="S080: 'the Company holds 90% equity shares of Dot & Key Wellness Private Limited effective September 20'; S079: 'Revenue (in INR Crores) FY 2023-24 198.3 FY 2022-23 57.7 FY 2021-22 27.5'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/07eae3e3-fc2e-44b3-9709-da47560b4f0a.pdf",
         source_ids="S079;S080;S087;S088", confidence="Low",
         notes=("FLAG: Nykaa was NOT yet listed at the first completion (51% on 2021-09-28 per search snippet; IPO opened 2021-10-28 (S088), listed Nov 2021), so no Reg 30 filing exists for the 2021 tranche. Included because Nykaa is listed today and the 2024 step-up is a T1 Reg 30 deal. "
                "consideration_inr_cr UNCONFIRMED: Business Today (S088) says Nykaa 'did not disclose the amount'; a search snippet attributes '~Rs 46.9 Cr secondary + ~Rs 50 Cr primary' to the RHP - lead only, not verified (check Nykaa RHP, 'Recent developments'). "
                "revenue FY21 UNCONFIRMED (first disclosed year is FY22 = 27.5 Cr, S079). 2024 step: 'Acquisition of the shares of Dot & Key will be done at a consideration of up to INR 265.3 crores' for 39% (S079) -> implies ~680 Cr for 100% (3.4x FY24 revenue).")),
    dict(parent="FSN E-Commerce Ventures Ltd (Nykaa)", brand="Earth Rhythm (Earth Rhythm Pvt Ltd)", category="BPC-Skincare",
         year_start=2024, consideration_inr_cr=44.5, stake_pct="", deal_structure="outright_majority",
         revenue_inr_cr=30.7, revenue_fy="FY24", revenue_basis="revenue as stated in Reg 30 annexure",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Filing: 'will further strengthen Company's product portfolio into sustainable beauty segment' - the clean/sustainable beauty cohort, inside a category (skincare) Nykaa already owned via Dot & Key.",
         status_today="Subsidiary at ~75.83% (converted basis) after second tranche on 2025-06-09; FY24 revenue INR 30.7 Cr (FY22 18.5)",
         status_evidence="S082: 'Following this investment, Nykaa now holds approximately 75.83% in ERPL, on a converted basis'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/07eae3e3-fc2e-44b3-9709-da47560b4f0a.pdf",
         source_ids="S077;S079;S081;S082", confidence="Low",
         notes=("Row = the CONTROL step (approved 2024-08-13, S079): further investment 'at a consideration of up to INR 44.5 crores' through primary and secondary, in tranches, making ERPL a subsidiary; first tranche executed Nov 2024 (S081), second tranche (Rs 5 Cr) 2025-06-09 (S082). "
                "stake_pct LEFT BLANK: the incremental stake bought for the 44.5 Cr is not stated (pre-deal 18.51% -> ~75.83% after both tranches, partly via primary OCRPS), so no multiple is computed. "
                "PRIOR MINORITY ENTRY (2022): Board approved on 2022-04-22 'upto 18.51%' for 'a consideration of Rs 41.65 crores' (S077); FY22 revenue Rs 18.56 Cr (unaudited) -> ~12x implied. "
                "deal_structure outright_majority: the first 2024 tranche made ERPL a subsidiary (S081); the 2022 entry would be minority_with_path. Memory said 'Nykaa acquired 51% of Earth Rhythm in 2022' (C023): WRONG, it was 18.51%.")),
    # ---------------- Emami ----------------
    dict(parent="Emami Ltd", brand="The Man Company (Helios Lifestyle Pvt Ltd)", category="BPC-MensGrooming",
         year_start=2024, consideration_inr_cr=177.63, stake_pct=49.6, deal_structure="full_100",
         revenue_inr_cr=183, revenue_fy="FY24", revenue_basis="turnover as stated in Reg 30 annexure",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Emami already sold men's products (Fair and Handsome - INFERRED); TMC 'caters to premium segment' with a head-to-toe online men's range, a premium cohort Emami lacked.",
         status_today="Wholly owned since 2024-11-21; FY24 turnover INR 183 Cr (4.3x FY21)",
         status_evidence="S092: 'in the last tranche of this transaction, 4585 equity shares of Helios have been acquired by the Company today, i.e., 21st November, 2024'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/2c0eecbf-b80b-4bb9-bdab-7ee327518b7d.pdf",
         source_ids="S089;S090;S091;S092", confidence="High",
         notes=("Row = the 2024 buyout of the balance: 'The total purchase consideration to be paid for the acquisition of 1,33,572 equity shares (i.e., 49.60% stake) will be Rs. 177.63 Cr' (S091, approved 2024-08-30); Emami already held 50.40%. Completed in tranches to 2024-11-21 (S092). "
                "Earlier path (prices undisclosed, 'not been disclosed due to reasons of confidentiality'): entry pre-2020 (UNCONFIRMED date, likely 2017); 33.09% -> 45.96% (2021-06-28, S089); 45.96% -> 48.49% (2021-08-05, S090); crossed 50% at an UNCONFIRMED date before 2024-08. "
                "Turnover: FY24 183, FY23 115, FY22 74 (S091); FY21 42.89, FY20 39.34 (S089) (INR Cr). Implied 100% value in 2024 ~358 Cr = 1.95x FY24. deal_structure full_100 because the holding reached 100% in this transaction (same convention as Beardo).")),
    dict(parent="Emami Ltd", brand="Brillare (Brillare Science Pvt Ltd)", category="BPC-Haircare",
         year_start=2021, consideration_inr_cr="", stake_pct=22.66, deal_structure="outright_majority",
         revenue_inr_cr=9.76, revenue_fy="FY21", revenue_basis="turnover as stated in Reg 30 annexure",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Emami had mass hair oils (Navratna, Kesh King); Brillare is a 'professional beauty care brand for salon', i.e. the salon/professional cohort.",
         status_today="Wholly owned since 2024-03-27; FY23 turnover INR 19.71 Cr (2x FY21) - still small",
         status_evidence="S095: 'Emami's Shareholding in Brillare has increased from 95.36% to 100% and it has become a wholly owned subsidiary'; 'Turnover... 2022-23 19.71'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/3a8cdf98-78aa-4e2b-ad29-5d1a3158e89b.pdf",
         source_ids="S093;S094;S095", confidence="High",
         notes=("Row = the control step: CCPS 'aggregating to Rs 1.50' Cr (subscribed 2020-12-31 and 2021-03-24, S093) converted into equity on 2021-10-01, taking Emami 'from 34.70% to 57.36%' - 'Brillare Science has become Subsidiary Company' (S094). stake_pct = 22.66 incremental. "
                "consideration_inr_cr UNCONFIRMED: 'Cost of conversion from CCPS to Equity Shares has not been disclosed'; the Rs 1.5 Cr CCPS outlay is too small to be the economic price of 22.66% (conversion likely ratcheted on performance), so not entered. Confidence High on the T1 facts; price blank. "
                "Entry pre-2020 (letters dated 2018-02-05 and 2019-04-26). Later: CCPS 'upon conversion... stake would be 66.29% subject to achievement of agreed future performance' (2021-11-02; that filing is NOT saved in sources/raw - quote UNCONFIRMED, verification 2026-10-10); 100% on 2024-03-27, price undisclosed (S095). Turnover FY21 9.76 / FY20 4.49 / FY19 9.32 (INR Cr).")),
    dict(parent="Emami Ltd", brand="Dermicool (brand acquired from Reckitt Benckiser Healthcare India)", category="BPC-Skincare",
         year_start=2022, consideration_inr_cr=432, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr="", revenue_fy="", revenue_basis="",
         what_was_acquired="REVENUE_SCALE",
         vocab_rationale="Emami already led cool talc with Navratna; release says 'Combined with Emami's Navratna Cool Talc, Emami will become leader in this niche category' - share, not a new category or cohort.",
         status_today="Owned brand within Emami (brand/trademark purchase, not a company); post-deal sales UNCONFIRMED",
         status_evidence="S096: 'the Company has acquired \"Dermicool\"... from Reckitt Benckiser Healthcare (India) Private Limited' (2022-03-25)",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/4bbf5be6-b8d6-4c4b-93e0-d9e5ed244f03.pdf",
         source_ids="S096;S098;S099", confidence="Medium",
         notes=("VERIFICATION 2026-10-10: stake_pct 100 is inferred from the deal type (outright brand purchase, S096: 'acquired \"Dermicool\"'); no % is printed, so the row is downgraded from High to Medium. Consideration is verbatim T1. "
                "NEW (not in the lead list). S096 press release: 'total consideration of Rs 432 crores excluding taxes & duties'; Dermicool 'commands ~20% market share' in prickly heat powder. "
                "A brand (asset) purchase from a multinational's Indian subsidiary, not a startup; kept because the parent is listed and the brand is Indian-market. Category bucket 'BPC-Skincare' is the nearest fit (talc/prickly heat). "
                "revenue UNCONFIRMED: a search snippet says 'Rs 113 crore in 2021, EBITDA margin 35%' but neither saved T3 article (S098, S099) contains it - lead only. If 113 holds, multiple = 3.8x.")),
    # ---------------- Other listed consumer companies (found by BSE scan) ----------------
    dict(parent="Honasa Consumer Ltd", brand="Reginald Men (BTM Ventures Pvt Ltd)", category="BPC-MensGrooming",
         year_start=2026, consideration_inr_cr=197.96, stake_pct=95, deal_structure="outright_majority",
         revenue_inr_cr=20.15, revenue_fy="FY25", revenue_basis="revenue as stated in Reg 30 annexure",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing: 'Expansion in a sizeable and fast-growing category (male personal care)'; Honasa had no dedicated men's brand (INFERRED from its portfolio of Mamaearth, The Derma Co, Aqualogica, BBlunt, Dr. Sheth's).",
         status_today="Subsidiary at 95% since 2026-01-06; remaining 5% after 12 months; TTM revenue to Oct-2025 INR 74 Cr",
         status_evidence="S101: 'completed the acquisition of 95% of the issued and paid-up equity share capital of BTM Ventures Private Limited'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/fc202c10-6ea5-4442-b480-7785e67736e9.pdf",
         source_ids="S100;S101", confidence="High",
         notes=("NEW (not in the lead list). Approved 2025-12-11 (S100): '95% equity stake via secondary purchase at a Rs 195 Crores enterprise value on a no-cash no-debt basis'; remaining 5% in tranche 2 after 12 months. Completed 2026-01-06 (S101) 'for an equity value of INR 197.96 Crores, which includes cash and cash equivalents of INR 12.71 Crores'. "
                "Revenue: FY23 ~Rs 0.7 thousand, FY24 ~Rs 43 thousand, FY25 Rs 20.15 Cr, TTM Oct-2025 Rs 74 Cr. Multiple 10.3x on FY25 but 2.8x on TTM - a young, fast-ramping brand (incorporated 2022-08-25), so FY25 understates scale. "
                "Honasa was listed (Nov 2023) at signing. Its 2022 deals (Dr. Sheth's, BBlunt) predate listing and are excluded; see claims_verification_log C020/C021.")),
    dict(parent="Zydus Wellness Ltd", brand="RiteBite Max Protein (Naturell (India) Pvt Ltd)", category="Food-Snacks&Bars",
         year_start=2024, consideration_inr_cr=390, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr=128.89, revenue_fy="FY24", revenue_basis="revenue_from_operations (IGAAP; ~119 Cr under Ind AS)",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Filing: 'expanding its footprint in the consumer wellness industry by foraying into the rapidly growing healthy snacking' segment; Zydus Wellness (Complan, Glucon-D, Sugar Free, Nycil) had no snack bars.",
         status_today="Subsidiary at 98.14% from 2024-11-29; balance 1.86% 'expected to be completed shortly' (completion of the last 1.86% UNCONFIRMED)",
         status_evidence="S103: 'on November 29, 2024, the Company has acquired 98.14% equity share capital from the Sellers of the Target'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/9eec263b-6a51-4a93-bb9c-4d767c184732.pdf",
         source_ids="S102;S103", confidence="High",
         notes=("NEW (not in the lead list). SPA approved 2024-10-30 (S102) for 100%: 'Rs 369 crores... will be paid as upfront consideration (subject to customary adjustments). Over and above this amount of upfront consideration, earnout amount of Rs 21 crores'; total 'consideration of Rs 390 crores'. "
                "Revenue: 'Revenue from Operations as per IGAAP... March 31, 2024: Rs 128.89 crores; March 31, 2023: Rs 102.06 crores; March 31, 2022: Rs 59.07 crores'; '(approx. Rs 119 crores as per IND-AS)'. Multiple 3.0x (IGAAP) / 3.3x (Ind AS). "
                "deal_structure full_100: 98.14% at first completion with the rest a formality (same convention as Organic India 99.99%).")),
    dict(parent="Bajaj Consumer Care Ltd", brand="Banjara's (Vishal Personal Care Pvt Ltd)", category="BPC-Haircare",
         year_start=2025, consideration_inr_cr=120, stake_pct=100, deal_structure="staged_to_control",
         revenue_inr_cr=51.53, revenue_fy="FY24", revenue_basis="revenue_from_operations",
         what_was_acquired="COHORT_EQUITY",
         vocab_rationale="Bajaj already sold herbal hair care (Almond Drops); filing cites 'size, geography, growth, profitability, and portfolio' - Banjara's (Hyderabad, ayurvedic henna/hair/skin) adds a southern consumer base (INFERRED: Bajaj's north/west skew).",
         status_today="Wholly owned since 2025-05-16 (tranche 2: 51% for INR 61.18 Cr)",
         status_evidence="S106: 'completed the acquisition of tranche 2 shares today, i.e., 51%... for a consideration of INR 61,18,23,600. Pursuant to this, the Target Company has now become 100% subsidiary'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/595c2660-0101-4f9b-a8a0-06bfaa5e1f77.pdf",
         source_ids="S104;S105;S109;S106", confidence="High",
         notes=("NEW (not in the lead list). Approved 2025-02-14 (S104; S105 is a duplicate filing): 'Estimated cash consideration of approx. INR 120 crore at an Enterprise value of INR 108.3 crore' for 100% in two tranches (49% then 51%); seller incl. Peepul Capital Fund III. "
                "Tranche 1 (49%) completed 2025-03-10 (S109); tranche 2 (51%) 2025-05-16 for INR 61.18 Cr (S106), so tranche 1 cost ~INR 59 Cr (DERIVED). consideration/stake recorded as the contracted 100% package. "
                "Revenue from operations: FY24 INR 51.53 Cr; FY23 45.36; FY22 39.43. deal_structure staged_to_control: first tranche 49% (<=50%) with a contracted second tranche to 100%. Category bucket inferred: Banjara's sells henna/hair and skin products.")),
    # ---------------- Reliance Consumer Products (SPECIAL CASE) ----------------
    dict(parent="Reliance Industries Ltd (via Reliance Consumer Products Ltd)", brand="Lotus Chocolate (Lotus Chocolate Company Ltd)", category="Other",
         year_start=2023, consideration_inr_cr=74.00, stake_pct=51, deal_structure="outright_majority",
         revenue_inr_cr=86.97, revenue_fy="FY22", revenue_basis="'Income from Operations' as stated in the letter of offer (audited)",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="RCPL had no chocolate/cocoa business; Lotus (cocoa products and chocolates, with a factory) gave entry into confectionery. CAPABILITY (manufacturing) is the runner-up.",
         status_today="Listed subsidiary of RCPL (51% via SPA plus open offer for up to 26% at INR 115.50/share, offer in Mar 2023); later performance UNCONFIRMED",
         status_evidence="S110: 'Shares / voting rights acquired... 65,48,935 51.00% 74,00,29,655 Cash'; open offer 'at a price of INR 115.50 per Offer Share'",
         source_url="https://www.bseindia.com/xml-data/corpfiling/AttachHis/fea041df-8810-409c-94b9-e89ad604024e.pdf",
         source_ids="S110;S111", confidence="High",
         notes=("SPECIAL CASE: acquirer is Reliance Consumer Products Ltd (RCPL), a wholly owned subsidiary of Reliance Retail Ventures, counted under listed parent Reliance Industries Ltd (listed-parent rule). RIL itself filed no Reg 30 for this size of deal; T1 evidence is the TARGET's SEBI SAST filings (Lotus is BSE-listed). "
                "SPA 2022-12-29: 51% from the promoters 'at a price of INR 113.00 per Sale Share, for a total consideration of INR 74,00,29,655' (S110); plus preferential issue of redeemable preference shares to RCPL (S111). Completion of the SPA ~May 2023 (Reg 29 disclosures 2023-05-27); exact date UNCONFIRMED. "
                "Revenue S111: 'Income from Operations' INR Cr - 9M FY23 37.11 (unaudited), FY22 86.97, FY21 47.87, FY20 69.89. Category 'Other' = confectionery (no bucket in the taxonomy).")),
    dict(parent="Reliance Industries Ltd (via Reliance Consumer Products Ltd)", brand="Campa (brand bought from Pure Drinks Group)", category="Beverages",
         year_start=2022, consideration_inr_cr=22, stake_pct=100, deal_structure="full_100",
         revenue_inr_cr="", revenue_fy="", revenue_basis="",
         what_was_acquired="CATEGORY_ENTRY",
         vocab_rationale="Reliance had no soft-drink brand; Campa was a dormant heritage cola trademark bought to enter carbonated drinks.",
         status_today="Relaunched 2023 and now Reliance's flagship beverage brand; Reliance plans up to INR 8,000 Cr of beverage investment (T4)",
         status_evidence="S113 (T4): 'Much of its INR 8,000 crore investment will be devoted to Campa-Cola's expansion'; 'It bought the Campa Cola brand for a measly INR 22 crore'",
         source_url="https://www.dtnext.in/amp/story/news/business/reliance-acquires-soft-drink-brand-campa-as-part-of-expansion",
         source_ids="S112;S113", confidence="Low",
         notes=("SPECIAL CASE (RCPL under RIL, see Lotus row). A trademark purchase of a dormant brand - really a BUILD on a bought name; flag for Tab B discussion. "
                "consideration 22 from S112 (PTI via DT Next): 'The deal is estimated to be around Rs 22 crore... said sources close to the development' - unnamed sources, T3 only; S113 repeats it (T4). No company disclosure found. Date 2022 (Aug-2022 per press; exact date UNCONFIRMED). "
                "revenue LEFT BLANK: brand was dormant at purchase; no turnover attributable. Multiple not meaningful.")),
    dict(parent="Reliance Industries Ltd (via Reliance Consumer Products Ltd)", brand="Sosyo (Sosyo Hajoori Beverages Pvt Ltd)", category="Beverages",
         year_start=2023, consideration_inr_cr="", stake_pct=50, deal_structure="minority_no_path",
         revenue_inr_cr="", revenue_fy="", revenue_basis="",
         what_was_acquired="CAPABILITY",
         vocab_rationale="Release: 'Sosyo's expertise in formulations can be leveraged to develop unique value proposition' for Reliance's beverage portfolio, which already had Campa - the formulation know-how is the stated asset.",
         status_today="50:50 joint venture with the Hajoori family, who keep running the business; later status UNCONFIRMED",
         status_evidence="S114: 'The existing promoters, Hajoori family, will continue to own the remaining stake in SHBPL'",
         source_url="https://www.afaqs.com/news/brands/reliance-consumer-to-acquire-50-stake-in-sasyo-hajoori-beverages",
         source_ids="S114;S115", confidence="Medium",
         notes=("SPECIAL CASE (RCPL under RIL). Announced Jan 2023 (S114, S115, both carrying RCPL's release): 'will acquire 50% equity stake in Gujarat-headquartered Sosyo Hajoori Beverages Private Limited'. "
                "JOINT VENTURE: a 50:50 JV, confirmed by both sources - S114: 'Speaking on the joint venture with RCPL'; 'The existing promoters, Hajoori family, will continue to own the remaining stake in SHBPL'. ""deal_structure = minority_no_path (the minority_no_path rule covers non-controlling stakes of 50% or less, including 50:50 JVs): no disclosed route for RCPL to take control. ""consideration UNCONFIRMED (not disclosed); revenue UNCONFIRMED. "
                "Medium = two T3 sources that agree (both rely on the same company release). Completion date UNCONFIRMED.")),
]


def multiple(r):
    try:
        return round(float(r["consideration_inr_cr"]) / (float(r["stake_pct"]) / 100) / float(r["revenue_inr_cr"]), 2)
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return ""


def write_tab():
    with TAB.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in ROWS:
            row = {"route": "Buy", "row_type": "core", "date_accessed": ACC, **r}
            row["revenue_multiple"] = multiple(row)
            w.writerow({k: row.get(k, "") for k in FIELDS})
    print(f"{len(ROWS)} rows -> {TAB.relative_to(ROOT)}")


# claim_id -> (value_verified, source_id, match, how_caught)
VERIFY = {
    "C001": ("90.5% for INR 2,670 Cr secondary at pre-money EV INR 2,955 Cr + INR 45 Cr primary; completion total INR 2,706.45 Cr (INR 2,706,44,95,728; 2025-04-21); FY24 turnover INR 347 Cr",
             "S007;S002", "Partial",
             "Reg 30 filing: recalled 'Rs 2,955 Cr' is the pre-money EV, not the price paid; stake and FY24 turnover correct"),
    "C002": ("51% for INR 264.28 Cr (first tranche, completed 2023-01-11)", "S008;S005", "Y",
             "Reg 30 filing; recall omitted the contracted 49% second tranche (bought 2026 for INR 824 Cr)"),
    "C003": ("19.8% for INR 70.00 Cr (completed 2023-01-04)", "S001;S012", "Y",
             "Reg 30 filing; recall missed that HUL SOLD the stake for ~INR 307 Cr in Mar 2026"),
    "C004": ("39.42% for Rs 175 Cr (2023-05-04); path to 100% completed 2026-09-28 (further ~Rs 645 Cr)", "S015;S031", "Y",
             "Reg 30 filings; stake and price correct"),
    "C005": ("First entry 16% for ~Rs 20 Cr (2021-11); 22% reached 2022-10 (~Rs 13.5 Cr more); 26.5% 2023-06; control deal 2025-04; total ~Rs 126 Cr for 49.3%", "S025;S028;S020", "N",
             "Reg 30 filings: recall had wrong year (2023 vs 2021), wrong stake (22% vs 16%) and wrong amount (Rs 120 Cr vs ~Rs 20 Cr); 120 Cr is close to the cumulative ~126 Cr investment up to 49.3%"),
    "C006": ("100% for up to Rs 472.50 Cr (Rs 400 Cr upfront + up to Rs 72.50 Cr in 24 months), completed 2025-06-13", "S020;S022", "Y",
             "Reg 30 filing; recall omitted the upfront/deferred split"),
    "C007": ("43.75% of Ample Foods for ~Rs 131 Cr (2025-04-04)", "S023;S024", "N",
             "Reg 30 filing: recall said ~Rs 375 Cr; actual first tranche ~Rs 131 Cr. Stake roughly right (43.8%)"),
    "C008": ("100% for INR 155.8 Cr + contingent consideration over 5 years; completed 2021-02-20", "S034;S035", "Y",
             "Reg 30 filing; recall omitted the contingent earn-out"),
    "C009": ("EV INR 5,100 Cr for 100%; 75% acquired 2024-02-01; now 80% (2026-09-01), 20% outstanding", "S036;S037;S038", "Y",
             "Reg 30 filing; recall's '75% upfront' right; did not know the 2026 top-up"),
    "C010": ("EV INR 1,900 Cr for 100% + earn-out linked to FY26; 99.99% on 2024-04-16; 100% on 2024-12-13", "S039;S040;S041", "Y",
             "Reg 30 filing; recall omitted the earn-out"),
    "C011": ("52.38% in Jul 2021 (consideration undisclosed); 60% by Nov 2022; 100% Sep 2024", "S046;S048;S050", "N",
             "Reg 30 filing: year wrong (2021 not 2022); recalled '~Rs 32 Cr' has no source; price was never disclosed"),
    "C012": ("53.98% on 2022-05-23 (consideration undisclosed); 100% on 2025-10-17", "S051;S053", "Y",
             "Reg 30 filing; recall's '54%' and 2022 correct"),
    "C013": ("Agreement 2023-07-26 for up to 58% at up to Rs 369.01 Cr; first tranche 32.75%; 84.09% by 2026-10-05", "S054;S058", "Partial",
             "Reg 30 filing: '58% for ~Rs 370 Cr' right as the package; first tranche was 32.75%, so 'acquired 58%' in 2023 is wrong"),
    "C014": ("60% for Rs 225.67 Cr, completed 2026-02-05", "S059;S060", "Partial",
             "Reg 30 filing: amount and stake right; year wrong (2026, not 2025)"),
    "C015": ("Balance 55% acquired 2020-06-30 taking Marico to 100% (from 45% held since 2017); price undisclosed", "S045", "Y",
             "Reg 30 filing; recall said 'around 2020-21', confirmed 2020-06-30"),
    "C016": ("51% on 2023-01-02 for INR 587.52 Cr less proportionate debt; 100% EV INR 1,152 Cr; balance 49% after 5 years", "S065;S066", "Partial",
             "Reg 30 filing: amounts right; year wrong (completed 2023, announced 2022)"),
    "C017": ("Balance 49.60% of Helios for Rs 177.63 Cr; 100% on 2024-11-21", "S091;S092", "Y",
             "Reg 30 filing; recall's '100% in 2024' right"),
    "C018": ("Control 2021-10-01 (34.70% -> 57.36% via CCPS conversion); 100% 2024-03-27; prices undisclosed", "S094;S095", "Partial",
             "Reg 30 filing: recall said 2022 and 'a stake'; control came in Oct 2021"),
    "C019": ("FMCG business (Park Avenue, KamaSutra) by slump sale for Rs 2,825 Cr (Rs 2,725 Cr ex cash), completed 2023-05-08", "S068;S069", "Y",
             "Reg 30 filing"),
    "C022": ("51% on ~2021-09-28 (pre-IPO; price undisclosed in press); 90% on 2024-09-20 for up to Rs 265.3 Cr", "S079;S080;S087;S088", "Partial",
             "Reg 30 2024 filing + press: '51% (2021)' right; '~Rs 100 Cr' unverified (only a search snippet citing the RHP)"),
    "C023": ("18.51% for Rs 41.65 Cr (2022); subsidiary ~75.83% only after 2024-25 tranches", "S077;S082", "N",
             "Reg 30 filing: recall said 51% in 2022; actual first stake 18.51%"),
    "C020": ("NOT VERIFIED - excluded: Honasa listed only in Nov 2023, so its 2022 Dr. Sheth's deal was by an unlisted company", "", "Rejected",
             "Scope rule (listed parent at deal time); BSE scan of Honasa from listing found BTM Ventures (Reginald Men) 2025-26 instead, added as a row"),
    "C021": ("NOT VERIFIED - excluded: Honasa unlisted at the 2022 BBlunt deal", "", "Rejected",
             "Scope rule; not researched further"),
    "C024": ("Campa: ~Rs 22 Cr per unnamed sources (2022); Sosyo: 50% (Jan 2023, price undisclosed); Lotus Chocolate: 51% for Rs 74.00 Cr + 26% open offer at Rs 115.50 (SPA 2022-12-29); Velvette: not researched",
             "S110;S112;S114", "Partial",
             "Lotus via target's SAST filings (T1); Campa only via press citing 'sources'; Sosyo stake confirmed, price undisclosed; Velvette dropped (time box)"),
}


def update_claims():
    with CLAIMS.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys()) if rows else ["claim_id", "item", "value_recalled", "value_verified", "source_id", "match", "how_caught"]
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
