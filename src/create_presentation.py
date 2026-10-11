"""
create_presentation.py
======================
Generates a publication-grade widescreen (16:9) PowerPoint research briefing
for the Maternal Mortality Community Research Project (2000–2023).

Designed for visual clarity, large readable typography (14pt–28pt),
structured card/table layouts, zero text overflow, and crystal-clear charts:
- Slide 1: Title & Executive KPI Badges
- Slide 2: Clinical Reality, Three Delays Framework & Methodological Traps Avoided
- Slide 3: Core Research Questions & Pre-Specified Hypotheses
- Slide 4: Data Provenance: WHO/UN MMEIG 2025 & World Bank WDI
- Slide 5: Programmatic Data Quality Audit (Styled Table + Conflict State Note)
- Slide 6: Global Trajectories: The 19-Fold Mean (46-Fold Median) Income Chasm (Figure 1)
- Slide 7: Macroeconomic Capacity: The Preston Curve Decoupled from % GDP (Figure 2)
- Slide 8: Total Fertility Rate (TFR) vs MMR & Clinical Mechanism (Figure 6A)
- Slide 9: Adolescent Fertility Rate (Ages 15–19) vs MMR & Clinical Hazards (Figure 6B)
- Slide 10: Domestic Health Expenditure (% of GDP) Decoupled from GDP (Figure 7 Full-Width)
- Slide 11: Longitudinal Panel Evidence (TWFE) & Doctor's Interview Defense Guide
- Slide 12: Sensitivity Analyses: 80% Uncertainty Bound Invariance (Figure 5)
- Slide 13: Income Tier Heterogeneity & Adolescent Burden Concentration (Figure 4 Full-Width)
- Slide 14: Clinical & Public-Health Synthesis: Bridging Data to Bedside Obstetrics
- Slide 15: Community Implications & Actionable Policy Recommendations (2x2 Grid)

Output: docs/presentation/maternal_mortality_research_briefing.pptx

Author: Dr. Aung Chit Moe (MBBS)
Date: October 2026
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def create_deck(base_dir: str):
    print("=" * 70)
    print("PHASE 4C: POWERPOINT RESEARCH BRIEFING GENERATION (VISUAL POLISH V2)")
    print("=" * 70)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    pres_dir = os.path.join(base_dir, "docs", "presentation")
    images_dir = os.path.join(base_dir, "docs", "images")
    os.makedirs(pres_dir, exist_ok=True)

    # Color Palette
    NAVY = RGBColor(27, 54, 93)         # #1B365D - Primary Header & Brand
    NAVY_DARK = RGBColor(15, 32, 60)    # #0F203C - Deep Title Background
    SLATE = RGBColor(71, 85, 105)       # #475569 - Secondary / Muted Text
    CRIMSON = RGBColor(190, 38, 35)     # #BE2623 - Alert / Accent Red
    TEAL = RGBColor(15, 118, 110)       # #0F766E - Clinical / Protective Accent
    INDIGO = RGBColor(67, 56, 202)      # #4338CA - Defense Guide Accent
    AMBER = RGBColor(180, 83, 9)        # #B45309 - Warning / Highlight
    DARK = RGBColor(30, 41, 59)         # #1E293B - Primary Body Text
    CARD_BG = RGBColor(244, 247, 251)   # #F4F7FB - Crisp Card Fill
    CARD_BORDER = RGBColor(203, 213, 225) # #CBD5E1 - Subtle Card Border
    LIGHT_INDIGO = RGBColor(238, 242, 255)
    LIGHT_TEAL = RGBColor(240, 253, 250)
    LIGHT_RED = RGBColor(254, 242, 242)
    WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]
    TOTAL_SLIDES = 15

    def add_header_and_footer(slide, slide_num, title_text, category_text="PUBLIC-HEALTH RESEARCH BRIEFING"):
        # Top Header Box
        header_box = slide.shapes.add_textbox(Inches(0.75), Inches(0.32), Inches(11.83), Inches(0.95))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CRIMSON

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22.5)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.space_before = Pt(2)

        # Thin horizontal divider line under header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.22), Inches(11.83), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.75), Inches(7.12), Inches(11.83), Inches(0.3))
        tf_f = footer_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        pf = tf_f.paragraphs[0]
        pf.text = f"Maternal Mortality Community Research Project (2000–2023)  •  WHO/UN MMEIG 2025 & World Bank WDI  •  Slide {slide_num} of {TOTAL_SLIDES}"
        pf.font.size = Pt(10)
        pf.font.color.rgb = SLATE

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER,
                 accent_color=NAVY, accent_pos="top", accent_thickness=0.07):
        """Creates a sharp rectangular card with a colored top or left accent strip and returns a top-anchored text_frame."""
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.0)

        if accent_color is not None:
            if accent_pos == "top":
                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(accent_thickness))
            else:
                bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(accent_thickness), Inches(height))
            bar.fill.solid()
            bar.fill.fore_color.rgb = accent_color
            bar.line.fill.background()

        # Dedicated text box inside card for guaranteed top alignment and clean padding
        pad_l = 0.22 if accent_pos != "left" else (accent_thickness + 0.16)
        pad_t = 0.16 if accent_pos != "top" else (accent_thickness + 0.12)
        tb = slide.shapes.add_textbox(
            Inches(left + pad_l),
            Inches(top + pad_t),
            Inches(width - pad_l - 0.18),
            Inches(height - pad_t - 0.12)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        return tf

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    # Left vertical accent stripe
    stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(0.85), Inches(0.14), Inches(4.1))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = CRIMSON
    stripe.line.fill.background()

    tb1 = slide1.shapes.add_textbox(Inches(1.15), Inches(0.85), Inches(11.4), Inches(4.1))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = 0

    p_kicker = tf1.paragraphs[0]
    p_kicker.text = "GLOBAL PUBLIC-HEALTH & EPIDEMIOLOGICAL DATA STUDY"
    p_kicker.font.size = Pt(13)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = RGBColor(248, 113, 113)
    p_kicker.space_after = Pt(10)

    p_main = tf1.add_paragraph()
    p_main.text = "Macroeconomic Financing, Demographic Transition, and Global Maternal Mortality"
    p_main.font.size = Pt(34)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE
    p_main.space_after = Pt(14)

    p_sub = tf1.add_paragraph()
    p_sub.text = "A 24-Year Longitudinal Panel Study Across 195 Countries (177 Balanced Panel, 2000–2023)"
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(26)

    p_auth = tf1.add_paragraph()
    p_auth.text = "Investigator: Dr. Aung Chit Moe (MBBS) • Healthcare Data Analytics & Clinical Research"
    p_auth.font.size = Pt(15.5)
    p_auth.font.bold = True
    p_auth.font.color.rgb = RGBColor(241, 245, 249)
    p_auth.space_after = Pt(6)

    p_prov = tf1.add_paragraph()
    p_prov.text = "Primary Data: WHO/UN MMEIG 2025 Estimation Round (ISBN 978-92-4-010846-2) & World Bank WDI API"
    p_prov.font.size = Pt(13.5)
    p_prov.font.color.rgb = RGBColor(148, 163, 184)

    # 4 Bottom KPI Badges on Slide 1
    badges = [
        ("177 COUNTRIES", "Balanced 24-Year Panel", "4,248 continuous country-years (of 195 sovereign nations)"),
        ("WHO MMEIG 2025", "80% Uncertainty Bounds", "Point estimate (0.5) + 10th & 90th percentile sensitivity"),
        ("-29.0% MMR", "Per Doubling of Real GDP", "Two-Way Fixed Effects panel elasticity (p < 0.001)"),
        ("100% VERIFIED", "Zero Synthetic Data", "No forward-filling, no circular SBA modeling (Rules 3 & 4)")
    ]
    for i, (b_val, b_title, b_desc) in enumerate(badges):
        bx = 0.75 + i * 3.02
        b_card = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(5.35), Inches(2.80), Inches(1.55))
        b_card.fill.solid()
        b_card.fill.fore_color.rgb = RGBColor(27, 54, 93)
        b_card.line.color.rgb = RGBColor(71, 85, 105)
        b_card.line.width = Pt(1.0)

        btf = b_card.text_frame
        btf.word_wrap = True
        btf.vertical_anchor = MSO_ANCHOR.TOP
        btf.margin_left = btf.margin_right = Inches(0.16)
        btf.margin_top = Inches(0.14)

        bp1 = btf.paragraphs[0]
        bp1.text = b_val
        bp1.font.size = Pt(18)
        bp1.font.bold = True
        bp1.font.color.rgb = RGBColor(94, 234, 212)
        bp1.space_after = Pt(3)

        bp2 = btf.add_paragraph()
        bp2.text = b_title
        bp2.font.size = Pt(13)
        bp2.font.bold = True
        bp2.font.color.rgb = WHITE
        bp2.space_after = Pt(4)

        bp3 = btf.add_paragraph()
        bp3.text = b_desc
        bp3.font.size = Pt(11.5)
        bp3.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: BACKGROUND & CLINICAL REALITY
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide2, 2, "The Global Challenge: Clinical Reality & The Three Delays Framework", "CLINICAL & EPIDEMIOLOGICAL CONTEXT")

    # Top Banner Card: Clinical Reality
    tf_top2 = add_card(slide2, 0.75, 1.38, 11.83, 1.25, bg_color=LIGHT_RED, border_color=CRIMSON, accent_color=CRIMSON, accent_pos="left", accent_thickness=0.10)
    p = tf_top2.paragraphs[0]
    p.text = "THE CLINICAL REALITY: >260,000 PREVENTABLE MATERNAL DEATHS IN 2023 (~700 WOMEN EVERY DAY)"
    p.font.size = Pt(14.5); p.font.bold = True; p.font.color.rgb = CRIMSON; p.space_after = Pt(4)
    p = tf_top2.add_paragraph()
    p.text = "Leading direct obstetric causes: Severe Postpartum Hemorrhage (uterine atony), Hypertensive Disorders (preeclampsia/eclampsia), Puerperal Sepsis, and Obstructed Labor. Effective bedside treatments exist (oxytocin, MgSO4, antibiotics, C-section), yet survival depends on systemic infrastructure."
    p.font.size = Pt(13.5); p.font.color.rgb = DARK

    # Middle 3 Cards: Three Delays Framework
    delays = [
        ("DELAY 1: SEEKING CARE", "Household & Sociocultural Barriers",
         "• Lack of female financial autonomy and catastrophic out-of-pocket delivery fees.\n• Low reproductive health literacy and inability to recognize obstetric danger signs.\n• Acute social stigma surrounding adolescent and unmarried pregnancy.", NAVY),
        ("DELAY 2: REACHING CARE", "Geographic & Transport Infrastructure",
         "• Unpaved rural roads, monsoon flooding, and river/mountain barriers.\n• Absence of community ambulances, maternity waiting homes, and telecom networks.\n• Fatal hemorrhage (PPH) can kill a mother within 2 hours without rapid transport.", TEAL),
        ("DELAY 3: RECEIVING QUALITY CARE", "Facility Readiness & Health Financing",
         "• Shortage of 24/7 Comprehensive Emergency Obstetric Care (CEmOC) surgical teams.\n• Unreliable hospital electricity for emergency cesarean sections.\n• Stockouts of tranexamic acid, oxytocin cold-chains, and cross-matched blood.", INDIGO)
    ]
    for i, (d_tag, d_sub, d_body, d_col) in enumerate(delays):
        tf_d = add_card(slide2, 0.75 + i * 4.02, 2.80, 3.79, 2.35, accent_color=d_col, accent_pos="top")
        p = tf_d.paragraphs[0]; p.text = d_tag; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = d_col; p.space_after = Pt(2)
        p = tf_d.add_paragraph(); p.text = d_sub; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(6)
        p = tf_d.add_paragraph(); p.text = d_body; p.font.size = Pt(13); p.font.color.rgb = DARK

    # Bottom 2 Cards: Methodological Traps Avoided
    traps = [
        ("METHODOLOGICAL TRAP 1 AVOIDED: CIRCULAR MODELING",
         "Why we exclude Skilled Birth Attendance (SBA) from regression predictors: WHO/UN MMEIG's Bayesian model (BMat) already uses SBA as a mathematical input to estimate MMR in data-poor countries. Regressing MMR on SBA creates circular endogeneity."),
        ("METHODOLOGICAL TRAP 2 AVOIDED: SURVEY MISSINGNESS BIAS",
         "Why we exclude sporadic survey indicators (e.g., adult female literacy, >80% missing): Listwise deletion on sparse survey variables drops >85% of low-income country-years, biasing studies toward wealthy nations.")
    ]
    for i, (t_head, t_desc) in enumerate(traps):
        tf_t = add_card(slide2, 0.75 + i * 6.02, 5.32, 5.81, 1.62, bg_color=CARD_BG, accent_color=SLATE, accent_pos="left", accent_thickness=0.08)
        p = tf_t.paragraphs[0]; p.text = t_head; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_t.add_paragraph(); p.text = t_desc; p.font.size = Pt(13); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 3: RESEARCH QUESTIONS & HYPOTHESES
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide3, 3, "Core Research Questions & Pre-Specified Hypotheses", "STUDY PROTOCOL & ANALYTICAL DESIGN")

    rqs = [
        ("RESEARCH QUESTION 1: DOMESTIC HEALTH FINANCING PRIORITY (DECOUPLED FROM GDP)",
         "How does national health budget commitment—measured as Current Health Expenditure (% of GDP) decoupled from GDP per capita—correlate with maternal mortality across all income tiers and within resource-constrained Lower-Middle-Income Countries?",
         "Pre-Specified Hypothesis H1: Countries allocating a higher share of GDP to healthcare achieve significantly lower MMR (standalone & within-LMICs), while real GDP per capita acts as the primary longitudinal macro-enabler.",
         NAVY, LIGHT_INDIGO),
        ("RESEARCH QUESTION 2: DEMOGRAPHIC TRANSITION & ADOLESCENT OBSTETRIC HAZARDS",
         "What are the distinct epidemiological and clinical relationships between Total Fertility Rate (TFR), Adolescent Fertility Rate (births per 1,000 girls aged 15–19), and national maternal mortality ratios?",
         "Pre-Specified Hypothesis H2: High TFR elevates MMR via grand multiparity (uterine atony/PPH), while teenage pregnancy independently increases MMR even after controlling for national wealth due to cephalopelvic disproportion and eclampsia.",
         CRIMSON, LIGHT_RED),
        ("RESEARCH QUESTION 3: WITHIN-COUNTRY LONGITUDINAL DYNAMICS VS CROSS-COUNTRY GAPS",
         "Tracking 177 sovereign countries continuously across 24 years (4,248 country-years), which factors drive year-over-year maternal mortality reductions inside a country after controlling for country and year fixed effects?",
         "Pre-Specified Hypothesis H3: Within-country longitudinal declines are propelled by real economic expansion (conquering Delays 2 & 3) and fertility reduction, and remain strictly invariant across MMEIG's 80% uncertainty bounds.",
         TEAL, LIGHT_TEAL)
    ]
    for i, (rq_title, rq_q, rq_hyp, col, bg_c) in enumerate(rqs):
        y_top = 1.40 + i * 1.88
        tf_rq = add_card(slide3, 0.75, y_top, 11.83, 1.72, bg_color=bg_c, border_color=col, accent_color=col, accent_pos="left", accent_thickness=0.12)
        p = tf_rq.paragraphs[0]; p.text = rq_title; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p = tf_rq.add_paragraph(); p.text = rq_q; p.font.size = Pt(14); p.font.color.rgb = DARK; p.space_after = Pt(6)
        p = tf_rq.add_paragraph(); p.text = f"▸ {rq_hyp}"; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 4: DATA SOURCES & PROVENANCE
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide4, 4, "Data Provenance: Authenticated Primary Public-Health Sources", "PHASE 1 SOURCE VERIFICATION")

    # Left Card: WHO/UN MMEIG
    tf_s4_l = add_card(slide4, 0.75, 1.40, 5.75, 5.55, accent_color=CRIMSON, accent_pos="top", accent_thickness=0.09)
    p = tf_s4_l.paragraphs[0]; p.text = "PRIMARY OUTCOME: WHO / UN MMEIG (2025 ROUND)"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = CRIMSON; p.space_after = Pt(8)
    mmeig_items = [
        ("Official Report:", "Trends in Maternal Mortality 2000 to 2023 (Geneva: World Health Organization, published April 7, 2025; ISBN 978-92-4-010846-2)."),
        ("5 UN Agencies:", "WHO, UNICEF, UNFPA, World Bank Group, and UN DESA Population Division."),
        ("Bayesian Model:", "Hierarchical B-spline model (BMis) combining CRVS vital registration, confidential inquiries, censuses, and DHS/MICS surveys."),
        ("Complete 80% UI:", "Extracted Median Point Estimate (0.5), 10th Percentile Lower Bound (0.1), and 90th Percentile Upper Bound (0.9) across 195 countries."),
        ("Verified Case Audit:", "Myanmar MMR declined from 243.2 (2010) to 184.8 (2023); Thailand MMR declined from 41.0 (2010) to 34.1 (2023).")
    ]
    for k, v in mmeig_items:
        p = tf_s4_l.add_paragraph()
        p.text = f"• {k} {v}"
        p.font.size = Pt(13.5); p.font.color.rgb = DARK; p.space_after = Pt(8)

    # Right Card: World Bank WDI
    tf_s4_r = add_card(slide4, 6.83, 1.40, 5.75, 5.55, accent_color=NAVY, accent_pos="top", accent_thickness=0.09)
    p = tf_s4_r.paragraphs[0]; p.text = "EXPLANATORY COVARIATES: WORLD BANK WDI API"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(8)
    wdi_items = [
        ("Real Economic Capacity (NY.GDP.PCAP.PP.KD):", "GDP per capita, PPP in constant 2021 international dollars (eliminates inflation & exchange-rate distortion; 94.7% coverage)."),
        ("Health Financing Priority (SH.XPD.CHEX.GD.ZS):", "Current health expenditure as % of GDP from WHO Global Health Expenditure Database (GHED; 94.8% coverage)."),
        ("Total Fertility Rate (SP.DYN.TFRT.IN):", "Total births per woman from UN DESA World Population Prospects 2024 (100% coverage across 185 WDI countries)."),
        ("Adolescent Fertility (SP.ADO.TFRT):", "Annual births per 1,000 girls aged 15–19 from UN DESA WPP 2024 (100% coverage)."),
        ("Urbanization Proxy (SP.URB.TOTL.IN.ZS):", "Urban population (% of total) capturing geographic proximity to referral hospitals (100% coverage).")
    ]
    for k, v in wdi_items:
        p = tf_s4_r.add_paragraph()
        p.text = f"• {k} {v}"
        p.font.size = Pt(13.5); p.font.color.rgb = DARK; p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: DATA QUALITY & INTEGRITY AUDIT (STYLED TABLE)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide5, 5, "Data Quality & Integrity Audit: 10 Programmatic Rules Verified", "PHASE 3B SQL & PYTHON VALIDATION")

    # Add Styled Table
    rows, cols = 6, 4
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.75), Inches(1.40), Inches(11.83), Inches(4.10))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.70)
    tbl.columns[1].width = Inches(4.53)
    tbl.columns[2].width = Inches(3.20)
    tbl.columns[3].width = Inches(1.40)

    headers5 = ["Validation Domain", "Programmatic Check (SQLite & pytest)", "Observed Audit Result", "Disposition"]
    audit_rows = [
        ("1. Primary Key Uniqueness", "GROUP BY (country_iso3, year) HAVING COUNT(*) > 1", "0 duplicate records across 4,680 cells", "PASS (100%)"),
        ("2. Bayesian UI Ordering", "Verify mmr_low (0.1) <= mmr_pt (0.5) <= mmr_high (0.9)", "4,680 / 4,680 strictly ordered (0 violations)", "PASS (100%)"),
        ("3. Domain Plausibility", "Check MMR > 0, GDP > 0, 0 < Health Exp % < 100, TFR > 0", "Zero negative or out-of-range anomalies", "PASS (100%)"),
        ("4. Strict Zero Imputation", "Verify zero forward-filling, interpolation, or synthetic rows", "100% authentic observed/modeled source values", "PASS (Rule 4)"),
        ("5. Balanced Panel Integrity", "Require 24/24 continuous annual observations (2000–2023)", "177 sovereign countries (4,248 country-years)", "PASS (95.7%)")
    ]

    for c_idx, h_text in enumerate(headers5):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = WHITE

    for r_idx, r_data in enumerate(audit_rows, start=1):
        row_bg = WHITE if r_idx % 2 == 1 else CARD_BG
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_TEAL if c_idx == 3 else row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(13)
            p.font.bold = (c_idx in (0, 3))
            p.font.color.rgb = TEAL if c_idx == 3 else (NAVY if c_idx == 0 else DARK)

    # Bottom Card: Audit Note on Excluded Conflict Nations
    tf_s5_bot = add_card(slide5, 0.75, 5.70, 11.83, 1.25, bg_color=LIGHT_INDIGO, border_color=INDIGO, accent_color=INDIGO, accent_pos="left", accent_thickness=0.10)
    p = tf_s5_bot.paragraphs[0]
    p.text = "TRANSPARENT MISSINGNESS AUDIT: WHY 18 OF 195 COUNTRIES LACK COMPLETE 24-YEAR WDI SERIES"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = INDIGO; p.space_after = Pt(4)
    p = tf_s5_bot.add_paragraph()
    p.text = "4 jurisdictions (Cook Islands, Cuba, Monaco, Puerto Rico) lack full WDI PPP series, 10 conflict/disrupted states (Afghanistan, Eritrea, Iraq, DPRK, Somalia, South Sudan, Syria, Ukraine, Venezuela, Yemen), and 4 early-decade gap states (Djibouti, Montenegro, Timor-Leste, Zimbabwe). Per Rule 4, we never fabricate or interpolate missing data."
    p.font.size = Pt(12.5); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 6: DESCRIPTIVE TRAJECTORIES & FIGURE 1
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide6, 6, "Descriptive Trajectories: The 19-Fold Mean (46-Fold Median) Income Chasm", "EMPIRICAL FINDINGS • GLOBAL EQUITY")

    cards6 = [
        ("GLOBAL PROGRESS (2000–2023)", "-49.7% Decline in Mean MMR",
         "Global mean national MMR dropped from 217.7 (2000) to 109.6 (2023) per 100k live births; global median MMR fell from 67.6 to 42.1.", TEAL),
        ("THE 19-FOLD MEAN (46x MEDIAN) DIVIDE", "370.1 (LIC) vs 19.5 (HIC)",
         "In 2023 (balanced panel, n=177), Low-Income Countries average 370.1 deaths per 100k (median 354.0), compared to 19.5 in High-Income Countries (median 7.7).", CRIMSON),
        ("POST-2015 SDG DECELERATION", "Stagnation & COVID-19 Shock",
         "Mortality reduction slowed after the 2015 MDG-to-SDG transition, with temporary reversals during the 2020–2022 COVID-19 pandemic.", NAVY)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(cards6):
        tf_c = add_card(slide6, 0.75, 1.40 + i * 1.88, 5.10, 1.72, accent_color=c_col, accent_pos="left", accent_thickness=0.09)
        p = tf_c.paragraphs[0]; p.text = c_tag; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(2)
        p = tf_c.add_paragraph(); p.text = c_stat; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(12.8); p.font.color.rgb = DARK

    fig1_file = os.path.join(images_dir, "fig1_mmr_trends_by_income.png")
    if os.path.exists(fig1_file):
        slide6.shapes.add_picture(fig1_file, Inches(6.05), Inches(1.42), width=Inches(6.55))

    # =========================================================================
    # SLIDE 7: THE PRESTON CURVE (DECOUPLED FROM % GDP) & FIGURE 2
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide7, 7, "Macroeconomic Capacity: The Preston Curve of Maternal Survival", "EMPIRICAL FINDINGS • REAL ECONOMIC OUTPUT")

    cards7 = [
        ("MASSIVE PROTECTIVE CORRELATION", "Spearman rho = -0.85 (p < 0.001)",
         "Real GDP per capita (constant 2021 PPP $) exhibits a massive inverse relationship with maternal mortality across all 177 balanced countries (rho = -0.84 across 24 years).", NAVY),
        ("NON-LINEAR DIMINISHING RETURNS", "Steep Drop Below $15,000 PPP",
         "Moving from $1,500 to $15,000 PPP slashes MMR from >500 to <50. Above $20,000 PPP, survival plateaus as basic infrastructure saturates.", TEAL),
        ("REGIONAL CASE CONTRAST (2023)", "Myanmar (185) vs Thailand (34)",
         "Myanmar ($5,364 PPP, MMR 185) vs Thailand ($21,245 PPP, MMR 34) illustrates the 5.4-fold survival gain of upper-middle-income capacity.", CRIMSON)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(cards7):
        tf_c = add_card(slide7, 0.75, 1.40 + i * 1.88, 5.10, 1.72, accent_color=c_col, accent_pos="left", accent_thickness=0.09)
        p = tf_c.paragraphs[0]; p.text = c_tag; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(2)
        p = tf_c.add_paragraph(); p.text = c_stat; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(13); p.font.color.rgb = DARK

    fig2_file = os.path.join(images_dir, "fig2_preston_curve_maternal_mortality.png")
    if os.path.exists(fig2_file):
        slide7.shapes.add_picture(fig2_file, Inches(6.05), Inches(1.42), width=Inches(6.55))

    # =========================================================================
    # SLIDE 8: TOTAL FERTILITY RATE (TFR) VS MMR & CLINICAL MECHANISMS (FIG 6A)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide8, 8, "Demographic Transition: Total Fertility Rate (TFR) vs Maternal Mortality", "DEMOGRAPHIC & CLINICAL MECHANISMS • PART 1")

    cards8 = [
        ("EMPIRICAL CORRELATION & PANEL EFFECT", "rho = +0.82 Panel | -12.3% MMR / Child",
         "TFR strongly tracks MMR across countries (rho = +0.79 in 2023, p < 0.001). Within a country over time, each 1-child drop in TFR reduces MMR by 12.3% (p = 0.032).", CRIMSON),
        ("CLINICAL MECHANISM 1: GRAND MULTIPARITY", "Uterine Atony & Postpartum Hemorrhage",
         "High national TFR means many women undergo >= 5 deliveries. Grand multiparity causes myometrial exhaustion and uterine atony—the #1 cause of fatal PPH and uterine rupture.", NAVY),
        ("CLINICAL MECHANISM 2: MATERNAL DEPLETION", "Short Birth Spacing & Severe Anemia",
         "Closely spaced pregnancies prevent iron and folate recovery, inducing chronic gestational anemia where even moderate delivery blood loss triggers fatal shock.", TEAL)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(cards8):
        tf_c = add_card(slide8, 0.75, 1.40 + i * 1.88, 5.10, 1.72, accent_color=c_col, accent_pos="left", accent_thickness=0.09)
        p = tf_c.paragraphs[0]; p.text = c_tag; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(2)
        p = tf_c.add_paragraph(); p.text = c_stat; p.font.size = Pt(16.5); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(12.8); p.font.color.rgb = DARK

    fig6a_file = os.path.join(images_dir, "fig6a_tfr_vs_mmr.png")
    if os.path.exists(fig6a_file):
        slide8.shapes.add_picture(fig6a_file, Inches(6.05), Inches(1.42), width=Inches(6.55))

    # =========================================================================
    # SLIDE 9: ADOLESCENT FERTILITY RATE VS MMR & OBSTETRIC HAZARDS (FIG 6B)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide9, 9, "Teenage Pregnancy: Adolescent Fertility (Ages 15–19) vs Maternal Mortality", "DEMOGRAPHIC & CLINICAL MECHANISMS • PART 2")

    cards9 = [
        ("INDEPENDENT MULTIVARIABLE PREDICTOR", "rho = +0.86 (2023) | +15.1% MMR / 10 Births",
         "Even after controlling for GDP and adult TFR in 2023 OLS, each +10 adolescent births per 1,000 girls increases national MMR by ~15.1% (beta = +0.0141, p < 0.001).", CRIMSON),
        ("BIOLOGICAL HAZARD: PELVIC IMMATURITY", "Cephalopelvic Disproportion & Eclampsia",
         "Adolescent girls have incompletely ossified pelvic canals, causing cephalopelvic disproportion (CPD), obstructed labor, uterine rupture, fistula, and eclampsia.", NAVY),
        ("SOCIAL HAZARD & REGIONAL CONTRAST", "Delay 1 Stigma • Myanmar vs Thailand",
         "Teenage mothers face acute stigma and financial dependence (Delay 1). Contrast: Myanmar (AdoFert 33.5, MMR 185) vs Thailand (AdoFert 26.1, MMR 34).", TEAL)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(cards9):
        tf_c = add_card(slide9, 0.75, 1.40 + i * 1.88, 5.10, 1.72, accent_color=c_col, accent_pos="left", accent_thickness=0.09)
        p = tf_c.paragraphs[0]; p.text = c_tag; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(2)
        p = tf_c.add_paragraph(); p.text = c_stat; p.font.size = Pt(16.5); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(12.8); p.font.color.rgb = DARK

    fig6b_file = os.path.join(images_dir, "fig6b_adolescent_fert_vs_mmr.png")
    if os.path.exists(fig6b_file):
        slide9.shapes.add_picture(fig6b_file, Inches(6.05), Inches(1.42), width=Inches(6.55))

    # =========================================================================
    # SLIDE 10: HEALTH EXPENDITURE (% OF GDP) DECOUPLED FROM GDP (FIG 7 FULL-WIDTH)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide10, 10, "Domestic Health Financing Priority: Spending (% of GDP) Decoupled from GDP", "HEALTH POLICY COMMITMENT VS ECONOMIC SIZE")

    top_cards10 = [
        ("1. CAPACITY VS COMMITMENT", "rho = -0.40 Panel (-0.39 in 2023)",
         "GDP per capita measures economic capacity; Health Exp (% of GDP) measures political priority for healthcare.", NAVY),
        ("2. 13-FOLD QUARTILE GRADIENT", "Q1: 170.3 vs Q4: 13.4 MMR",
         "Low-priority nations (<4.4% GDP) suffer a median MMR of 170.3 vs 13.4 in high-priority nations (>8.5% GDP).", CRIMSON),
        ("3. PROOF WITHIN LMIC PEERS", "Within-LMIC rho = -0.43 (p = 0.004)",
         "Among 43 Lower-Middle-Income nations with similar GDP, higher health % of GDP significantly lowers MMR.", TEAL)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(top_cards10):
        tf_c = add_card(slide10, 0.75 + i * 4.02, 1.35, 3.79, 1.48, accent_color=c_col, accent_pos="top", accent_thickness=0.06)
        p = tf_c.paragraphs[0]; p.text = f"{c_tag}  •  {c_stat}"; p.font.size = Pt(12.2); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(12.5); p.font.color.rgb = DARK

    fig7_file = os.path.join(images_dir, "fig7_health_exp_vs_mmr.png")
    if os.path.exists(fig7_file):
        slide10.shapes.add_picture(fig7_file, Inches(0.85), Inches(2.92), width=Inches(11.63))

    # =========================================================================
    # SLIDE 11: LONGITUDINAL PANEL EVIDENCE (TWFE) & DOCTOR'S DEFENSE GUIDE
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide11, 11, "Longitudinal Panel Evidence: What Drives Survival Inside a Country Over Time?", "PRIMARY ECONOMETRIC MODEL • TWO-WAY FIXED EFFECTS (N = 4,248)")

    pillars11 = [
        ("PILLAR 1: ECONOMIC CAPACITY", "-29.0% MMR Reduction",
         "Per Doubling of Real GDP per Capita\n(TWFE beta = -0.4959, p < 0.001)",
         "Clinical Translation:\nWhen a country's economy grows over time, it builds the physical enablers that resolve Delays 2 & 3: paved rural roads, ambulance fleets, 24/7 hospital electricity, and regional blood banks.",
         NAVY),
        ("PILLAR 2: FERTILITY TRANSITION", "-12.3% MMR Reduction",
         "Per 1-Child Drop in Total Fertility (TFR)\n(TWFE beta = +0.1308, p = 0.032)",
         "Clinical Translation:\nAs women within a country have fewer total pregnancies over time, high-risk grand multiparity (parities >= 5) drops sharply, preventing uterine atony hemorrhage and maternal anemia.",
         TEAL),
        ("PILLAR 3: PANEL VS CROSS-SECTION", "Structural vs Annual Shifts",
         "Why Do Fixed Effects & OLS Differ?\n(Between-Country vs Within-Country)",
         "Clinical Translation:\nTeenage pregnancy (rho = +0.86) and health budgets (rho = -0.40) are massive structural dividers across countries. Fixed effects absorb baseline gaps and isolate year-to-year changes.",
         CRIMSON)
    ]
    for i, (p_tag, p_stat, p_sub, p_body, p_col) in enumerate(pillars11):
        tf_p = add_card(slide11, 0.75 + i * 4.02, 1.38, 3.79, 3.65, accent_color=p_col, accent_pos="top", accent_thickness=0.08)
        p = tf_p.paragraphs[0]; p.text = p_tag; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = p_col; p.space_after = Pt(4)
        p = tf_p.add_paragraph(); p.text = p_stat; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_p.add_paragraph(); p.text = p_sub; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(10)
        p = tf_p.add_paragraph(); p.text = p_body; p.font.size = Pt(13); p.font.color.rgb = DARK

    # Doctor's Defense Guide Box at Bottom
    tf_def = add_card(slide11, 0.75, 5.22, 11.83, 1.72, bg_color=LIGHT_INDIGO, border_color=INDIGO, accent_color=INDIGO, accent_pos="left", accent_thickness=0.12)
    p = tf_def.paragraphs[0]
    p.text = "DOCTOR'S INTERVIEW & RESEARCH DEFENSE GUIDE (HOW TO EXPLAIN THIS SIMPLY):"
    p.font.size = Pt(13.5); p.font.bold = True; p.font.color.rgb = INDIGO; p.space_after = Pt(4)
    p = tf_def.add_paragraph()
    p.text = "\"Our 24-year panel of 177 countries shows two complementary truths: (1) Within a country over time, maternal deaths are driven down by economic growth (-29% MMR per GDP doubling, which funds roads, power, and surgical centers) and fertility reduction (-12.3% MMR per child drop, which prevents uterine atony). (2) Across countries, teenage pregnancy (rho = +0.86) and health budget priority (rho = -0.40) remain powerful structural determinants of maternal survival.\""
    p.font.size = Pt(13); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 12: SENSITIVITY ANALYSES & FIGURE 5
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide12, 12, "Sensitivity Analyses: Invariance to MMEIG 80% Uncertainty Bounds", "ROBUSTNESS & EXTREME-BOUND TESTING")

    cards12 = [
        ("80% UNCERTAINTY BOUND INVARIANCE", "10th (-0.491) vs 90th (-0.498)",
         "Re-estimating our TWFE panel model on MMEIG's 10th percentile lower bound and 90th percentile upper bound produces virtually identical coefficients.", NAVY),
        ("PRE-PANDEMIC STABILITY (2000–2019)", "Pre-COVID beta = -0.5265 (p < 0.001)",
         "Restricting the panel to the 20 pre-pandemic years (n = 3,540) confirms that findings are not artifacts of COVID-19 mortality spikes.", TEAL),
        ("BALANCED VS UNBALANCED SAMPLE", "4,248 vs 4,406 Country-Years",
         "Including the conflict-affected countries with partial series yields identical directions and significance levels across all covariates.", CRIMSON)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(cards12):
        tf_c = add_card(slide12, 0.75, 1.40 + i * 1.88, 5.10, 1.72, accent_color=c_col, accent_pos="left", accent_thickness=0.09)
        p = tf_c.paragraphs[0]; p.text = c_tag; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(2)
        p = tf_c.add_paragraph(); p.text = c_stat; p.font.size = Pt(16.5); p.font.bold = True; p.font.color.rgb = NAVY; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(13); p.font.color.rgb = DARK

    fig5_file = os.path.join(images_dir, "fig5_uncertainty_forest_plot.png")
    if os.path.exists(fig5_file):
        slide12.shapes.add_picture(fig5_file, Inches(6.05), Inches(1.42), width=Inches(6.55))

    # =========================================================================
    # SLIDE 13: INCOME TIER HETEROGENEITY (FIG 4 FULL-WIDTH)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide13, 13, "Income Tier Heterogeneity: Diminishing Returns & Adolescent Concentration", "STRATIFIED SUBGROUP ANALYSIS (2000–2023)")

    top_cards13 = [
        ("1. STEEPEST GAINS IN LICs & LMICs", "Median MMR: 526.0 (LIC) vs 239.6 (LMIC)",
         "Marginal investments in roads, blood banks, and health budgets yield their largest absolute survival gains in low-resource tiers.", CRIMSON),
        ("2. HIGH-INCOME SYSTEMIC PLATEAU", "Median MMR: 9.8 Deaths / 100k",
         "High-income nations operate on a resilient plateau where baseline emergency obstetric infrastructure is universally guaranteed.", NAVY),
        ("3. 10-FOLD ADOLESCENT BURDEN GAP", "128.9 (LIC) vs 13.1 (HIC) Births / 1k",
         "Panel median adolescent fertility is 10x higher in low-income nations (106.9 vs 6.4 in 2023), concentrating risk among the poorest.", TEAL)
    ]
    for i, (c_tag, c_stat, c_desc, c_col) in enumerate(top_cards13):
        tf_c = add_card(slide13, 0.75 + i * 4.02, 1.35, 3.79, 1.48, accent_color=c_col, accent_pos="top", accent_thickness=0.06)
        p = tf_c.paragraphs[0]; p.text = f"{c_tag}  •  {c_stat}"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = c_col; p.space_after = Pt(4)
        p = tf_c.add_paragraph(); p.text = c_desc; p.font.size = Pt(12.5); p.font.color.rgb = DARK

    fig4_file = os.path.join(images_dir, "fig4_income_heterogeneity_effects.png")
    if os.path.exists(fig4_file):
        slide13.shapes.add_picture(fig4_file, Inches(0.85), Inches(2.92), width=Inches(11.63))

    # =========================================================================
    # SLIDE 14: CLINICAL & PUBLIC-HEALTH DISCUSSION
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide14, 14, "Clinical & Public-Health Synthesis: Bridging Data to Bedside Obstetrics", "INTEGRATED CLINICAL INTERPRETATION")

    disc_cards = [
        ("1. WHY MACROECONOMIC CAPACITY PROTECTS MOTHERS (RESOLVING DELAYS 2 & 3)",
         "In clinical practice, an obstetrician cannot save a mother with a ruptured uterus or placenta previa without blood, anesthesia, and electricity. National economic growth funds rural road paving, telecom coverage to dispatch ambulances, 24/7 surgical theater power, and cold-chain blood banking—turning fatal home emergencies into survivable hospital deliveries.",
         NAVY, LIGHT_INDIGO),
        ("2. THE BIOLOGICAL MECHANISM OF FERTILITY REDUCTION (PREVENTING UTERINE ATONY)",
         "Our fixed-effects finding that falling TFR reduces MMR (-12.3% per child) reflects fundamental obstetric physiology: eliminating grand multiparity (parities >= 5) removes the leading cause of refractory uterine atony and postpartum hemorrhage, while longer birth intervals prevent severe gestational iron-deficiency anemia.",
         TEAL, LIGHT_TEAL),
        ("3. WHY ADOLESCENT PREGNANCY IS AN ACUTE OBSTETRIC EMERGENCY (CPD & ECLAMPSIA)",
         "Across all decades, teenage childbearing (ages 15–19) remains a lethal independent predictor (+15.1% MMR per 10 births/1k). Biologically, pelvic immaturity causes cephalopelvic disproportion (CPD), obstructed labor, and eclampsia; socially, stigma and financial dependence trap teenagers in Delay 1.",
         CRIMSON, LIGHT_RED)
    ]
    for i, (d_head, d_text, d_col, d_bg) in enumerate(disc_cards):
        y_top = 1.40 + i * 1.88
        tf_d = add_card(slide14, 0.75, y_top, 11.83, 1.72, bg_color=d_bg, border_color=d_col, accent_color=d_col, accent_pos="left", accent_thickness=0.12)
        p = tf_d.paragraphs[0]; p.text = d_head; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = d_col; p.space_after = Pt(6)
        p = tf_d.add_paragraph(); p.text = d_text; p.font.size = Pt(13.8); p.font.color.rgb = DARK

    # =========================================================================
    # SLIDE 15: COMMUNITY IMPLICATIONS & ACTIONABLE POLICY RECOMMENDATIONS
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_header_and_footer(slide15, 15, "Community Implications & Actionable Public-Health Recommendations", "EVIDENCE-BASED INTERVENTIONS FOR MATERNAL SURVIVAL")

    recs15 = [
        ("1. EXPAND ADOLESCENT REPRODUCTIVE HEALTHCARE",
         "Target: Delay 1, Obstructed Labor (CPD) & Eclampsia",
         "• Invest in girls' secondary school retention and comprehensive reproductive health education.\n• Provide stigma-free, youth-friendly community clinics and modern contraception to prevent high-risk teenage pregnancies.",
         CRIMSON, 0.75, 1.40),
        ("2. STRENGTHEN RURAL OBSTETRIC REFERRAL NETWORKS",
         "Target: Delay 2 (Geographic & Transport Barriers)",
         "• Establish community maternity waiting homes near CEmOC referral hospitals for high-risk late-trimester mothers in remote villages.\n• Fund local motorcycle, boat, and rural ambulance networks.",
         TEAL, 6.83, 1.40),
        ("3. RING-FENCE HEALTH BUDGETS & REMOVE USER FEES",
         "Target: Delay 1 (Financial) & Delay 3 (Facility Readiness)",
         "• Prioritize domestic health spending (>6.5% of GDP) even in lower-middle-income settings.\n• Abolish out-of-pocket delivery and emergency C-section fees while guaranteeing 24/7 oxytocin, MgSO4, and blood bank stocks.",
         NAVY, 0.75, 4.25),
        ("4. BUILD REAL-TIME CRVS & MATERNAL DEATH AUDITS",
         "Target: Epidemiological Surveillance & Accountability",
         "• Transition from intermittent 5-year household surveys to complete Civil Registration and Vital Statistics (CRVS).\n• Institutionalize facility and community Maternal Death Surveillance and Response (MDSR) to prevent recurring clinical failures.",
         INDIGO, 6.83, 4.25)
    ]
    for r_title, r_sub, r_body, r_col, rx, ry in recs15:
        tf_r = add_card(slide15, rx, ry, 5.75, 2.65, accent_color=r_col, accent_pos="top", accent_thickness=0.08)
        p = tf_r.paragraphs[0]; p.text = r_title; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = r_col; p.space_after = Pt(3)
        p = tf_r.add_paragraph(); p.text = r_sub; p.font.size = Pt(12.5); p.font.bold = True; p.font.color.rgb = SLATE; p.space_after = Pt(8)
        p = tf_r.add_paragraph(); p.text = r_body; p.font.size = Pt(13.5); p.font.color.rgb = DARK

    deck_path = os.path.join(pres_dir, "maternal_mortality_research_briefing.pptx")
    prs.save(deck_path)
    print(f"[SAVED] Visually Polished PowerPoint briefing saved to {deck_path} ({os.path.getsize(deck_path):,} bytes)")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    create_deck(base_dir)
