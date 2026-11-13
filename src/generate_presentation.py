"""
generate_presentation.py
Official 14-slide PowerPoint presentation for Abhinav Chitrey (UID: 24BCS12754).
Industrial Training Viva-Voce at Chandigarh University (CSE-Takshashila).

Design Specifications:
- Slide 1: Full official template with CU branding, "Discover . Learn . Empower", Department, UID, Company.
  * Mode: Remote / Virtual
  * REMOVED Viva-Voce date from 1st page
- Slides 2 to 14:
  * REMOVED "Discover . Learn . Empower"
  * REMOVED Department banner
  * REMOVED UID and Company name from footer
  * ONLY clean slide number (e.g. "Slide 2 of 14") at bottom right
  * Clean single-line titles with subtle accent divider line
  * ZERO overlapping: generous margins, properly sized images, tables and text cards
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

TEMPLATE_PATH = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\brain\0c0c011e-66fa-4535-99d2-6d2a2228d1e5\.user_uploaded\media_1794587135582_3491dd33.pptx"
OUTPUT_DIR = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission"
PPTX_PATH = os.path.join(OUTPUT_DIR, "Industrial_Training_Presentation.pptx")
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")
EXTRACTED_DIR = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\extracted_template_assets"

# Corporate Color Palette
NAVY = RGBColor(13, 35, 58)
CRIMSON = RGBColor(168, 45, 45)
SLATE = RGBColor(51, 78, 104)
MUTED = RGBColor(110, 130, 150)
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(30, 130, 60)
CARD_BG = RGBColor(248, 250, 252)
CARD_BORDER = RGBColor(215, 225, 235)

def format_run(run, font_name="Arial", size_pt=11, bold=False, color=NAVY, italic=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def add_clean_slide_header(slide, title_text, slide_num, total_slides=14):
    """Add clean slide title, accent divider, and slide number without header/footer clutter."""
    # 1. Slide Title (Single line, 20pt Bold Navy)
    tb_title = slide.shapes.add_textbox(Inches(0.6), Inches(0.30), Inches(7.6), Inches(0.50))
    tf = tb_title.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    format_run(p.runs[0], "Arial", 20, bold=True, color=NAVY)

    # 2. Subtle Slide Number
    tb_num = slide.shapes.add_textbox(Inches(8.2), Inches(0.35), Inches(1.2), Inches(0.35))
    tf_num = tb_num.text_frame
    tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"Slide {slide_num} of {total_slides}"
    format_run(p_num.runs[0], "Arial", 9.5, bold=True, color=MUTED)

    # 3. Horizontal Accent Divider Line (Crimson & Navy)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.85), Inches(8.8), Inches(0.025))
    line.fill.solid()
    line.fill.fore_color.rgb = CRIMSON
    line.line.color.rgb = CRIMSON

def add_card(slide, left, top, width, height, title, items, title_color=CRIMSON):
    """Helper to draw a clean structured information card."""
    # Background shape
    bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = CARD_BG
    bg.line.color.rgb = CARD_BORDER
    bg.line.width = Pt(1)

    # Text box inside card
    pad = Inches(0.12)
    tb = slide.shapes.add_textbox(left + pad, top + pad, width - (pad * 2), height - (pad * 2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    format_run(p_title.runs[0], "Arial", 12.5, bold=True, color=title_color)

    for prefix, body in items:
        p = tf.add_paragraph()
        p.space_before = Pt(4)
        p.text = f"• {prefix}"
        format_run(p.runs[0], "Arial", 10.5, bold=True, color=NAVY)
        r = p.add_run()
        r.text = body
        format_run(r, "Arial", 10, color=SLATE)

def build_presentation():
    prs = Presentation(TEMPLATE_PATH)
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(5.625)

    # Clear template slides
    while len(prs.slides) > 0:
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    blank_layout = prs.slide_layouts[6]
    print("Building 14 slides with zero overlap...")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Official CU Takshashila Branding)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg_img1 = os.path.join(EXTRACTED_DIR, "slide_1_img_0.png")
    if os.path.exists(bg_img1):
        s1.shapes.add_picture(bg_img1, 0, 0, width=Inches(10.0), height=Inches(5.625))

    cu_logo = os.path.join(EXTRACTED_DIR, "slide_1_img_1.png")
    if os.path.exists(cu_logo):
        s1.shapes.add_picture(cu_logo, Inches(0.6), Inches(0.35), width=Inches(1.7))

    # Main Title Box
    tb_t1 = s1.shapes.add_textbox(Inches(0.6), Inches(1.15), Inches(8.8), Inches(1.3))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p_t1 = tf_t1.paragraphs[0]
    p_t1.text = "WORKFORCEX"
    format_run(p_t1.runs[0], "Arial", 38, bold=True, color=NAVY)

    p_sub1 = tf_t1.add_paragraph()
    p_sub1.text = "Strategic Workforce Intelligence, Predictive Career GPS & Explainable Talent Analytics"
    format_run(p_sub1.runs[0], "Arial", 16, bold=True, color=CRIMSON)

    # Candidate Card (Left)
    tb_cand = s1.shapes.add_textbox(Inches(0.6), Inches(2.65), Inches(4.3), Inches(2.2))
    tf_c = tb_cand.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "PRESENTED BY:"
    format_run(p.runs[0], "Arial", 11, bold=True, color=SLATE)

    p = tf_c.add_paragraph()
    p.text = "Abhinav Chitrey"
    format_run(p.runs[0], "Arial", 19, bold=True, color=NAVY)

    p = tf_c.add_paragraph()
    p.text = "UID: 24BCS12754  |  Section: 802-B\nBachelor of Engineering in CSE\nGroup: CSE-TAKSHASHILA\nChandigarh University, Mohali, Punjab"
    format_run(p.runs[0], "Arial", 11.5, color=SLATE)

    # Industry Card (Right) - Mode: Remote, NO Viva Date
    tb_ind = s1.shapes.add_textbox(Inches(5.3), Inches(2.65), Inches(4.2), Inches(2.2))
    tf_i = tb_ind.text_frame
    tf_i.word_wrap = True

    p = tf_i.paragraphs[0]
    p.text = "INDUSTRIAL INTERNSHIP HOST:"
    format_run(p.runs[0], "Arial", 11, bold=True, color=SLATE)

    p = tf_i.add_paragraph()
    p.text = "CogniStrat Technologies Pvt. Ltd."
    format_run(p.runs[0], "Arial", 16, bold=True, color=NAVY)

    p = tf_i.add_paragraph()
    p.text = "Role: Data Science & AI Intern\nDuration: 6 Weeks (5 May 2026 – 15 June 2026)\nLocation / Mode: Remote (Virtual R&D Division)\nHQ: Outer Ring Road, Bellandur, Bengaluru"
    format_run(p.runs[0], "Arial", 11.5, color=SLATE)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & INDUSTRIAL PROFILE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s2, "Executive Summary & Industrial Profile", 2)

    cards_s2 = [
        ("Host Organization Profile", [
            ("Company: ", "CogniStrat Technologies Pvt. Ltd., Bengaluru"),
            ("Corporate ID: ", "CIN: U72900KA2018PTC114920 | GSTIN: 29AABCC1234F1Z8"),
            ("Certifications: ", "ISO 9001:2015 & ISO/IEC 27001:2022 Certified"),
            ("Domain Focus: ", "Enterprise AI decision platforms & talent systems")
        ], Inches(0.6), Inches(1.15), Inches(2.7), Inches(4.0), CRIMSON),

        ("Industrial Training Context", [
            ("Division: ", "Enterprise AI & People Analytics R&D Lab"),
            ("Tenure & Mode: ", "6 Weeks (5 May – 15 June 2026), 100% Remote"),
            ("Mentorship: ", "Dr. Arvind R. Nair (VP AI), Meenakshi Sundaram (HR)"),
            ("Assessment: ", "Performance: Grade A+ (Outstanding - 96/100)")
        ], Inches(3.65), Inches(1.15), Inches(2.7), Inches(4.0), NAVY),

        ("Strategic Project Mission", [
            ("Core Problem: ", "Bridge job market demand, junior profiles & senior traits"),
            ("ML Engines: ", "Dual supervised classifiers (ROC-AUC > 0.81)"),
            ("Explainable AI: ", "TreeSHAP game-theoretic feature attributions"),
            ("Business ROI: ", "Empirical 6.3x cost efficiency for internal reskilling")
        ], Inches(6.7), Inches(1.15), Inches(2.7), Inches(4.0), GREEN)
    ]
    for c_title, items, left, top, width, height, color in cards_s2:
        add_card(s2, left, top, width, height, c_title, items, color)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT & INDUSTRY NEED
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s3, "Problem Statement & Industry Need Identification", 3)

    items_3_left = [
        ("Skill Disruption (WEF 2025): ", "44% of core technical competencies will be obsolete or restructured by 2027."),
        ("Prohibitive Hiring Costs: ", "External hiring takes 75–110 days and costs $118,000+ per senior technical hire."),
        ("The Subjective HR Trap: ", "78% of enterprise leaders rely on subjective impressions or keyword-matching ATS tools."),
        ("The Black-Box Risk: ", "Unexplainable AI models introduce severe compliance risks, bias, and managerial distrust.")
    ]
    add_card(s3, Inches(0.6), Inches(1.15), Inches(4.2), Inches(4.0), "CRITICAL INDUSTRY TALENT FRICTION", items_3_left, CRIMSON)

    items_3_right = [
        ("Multi-Dataset Grounding: ", "Cleaned, harmonized 13,965 real-world records across 4 disparate data sources."),
        ("Predictive Career GPS: ", "Dual ML models (ROC-AUC > 0.81) forecasting junior and senior success outcomes."),
        ("Audit-Ready Explainable AI: ", "TreeSHAP feature attributions providing mathematical justification for every step."),
        ("Financial Decision Simulator: ", "Real-time Build vs Buy vs Automate optimization modeling proven 6.3x ROI.")
    ]
    add_card(s3, Inches(5.2), Inches(1.15), Inches(4.2), Inches(4.0), "THE WORKFORCEX STRATEGIC SOLUTION", items_3_right, GREEN)

    # =========================================================================
    # SLIDE 4: SIX-WEEK GANTT TIMELINE & MILESTONES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s4, "Six-Week Industrial Training Milestone Execution", 4)

    gantt_img = os.path.join(ASSETS_DIR, "Figure_1_1_Gantt_Chart.png")
    if os.path.exists(gantt_img):
        s4.shapes.add_picture(gantt_img, Inches(0.6), Inches(1.15), width=Inches(8.8), height=Inches(3.95))

    # =========================================================================
    # SLIDE 5: MULTI-SOURCE DATA QUALITY ENGINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s5, "Multi-Source Data Ingestion & Quality Engine", 5)

    items_5_left = [
        ("Total Records: ", "13,965 consolidated talent records."),
        ("Raw Missingness: ", "9.8% across uncleaned fields."),
        ("Clean Missingness: ", "0.0% (Zero residual missingness)."),
        ("Deduplication: ", "SHA-256 record hashing verified."),
        ("Imputation: ", "Median grouped conditioning by title/band."),
        ("Standardization: ", "Canonical dictionary skill mapping.")
    ]
    add_card(s5, Inches(0.6), Inches(1.15), Inches(3.6), Inches(4.0), "INGESTION & AUDIT METRICS", items_5_left, NAVY)

    # Table on Right
    table_shape5 = s5.shapes.add_table(5, 3, Inches(4.4), Inches(1.2), Inches(5.0), Inches(3.8))
    tbl5 = table_shape5.table
    tbl5.columns[0].width = Inches(1.7)
    tbl5.columns[1].width = Inches(0.9)
    tbl5.columns[2].width = Inches(2.4)

    headers5 = ["Dataset Repository", "Records", "Analytical Functionality"]
    for j, h in enumerate(headers5):
        cell = tbl5.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                format_run(r, "Arial", 9.5, bold=True, color=WHITE)

    rows5 = [
        ("Job Market Postings", "6,870", "Market posting demand & skill frequency"),
        ("Junior Data Scientist Profiles", "3,450", "Empirical project success & career speed"),
        ("Senior Role Psychometrics", "2,120", "Big Five personality traits & leadership"),
        ("Headcount & Salary Data", "1,525", "Recruitment costs, salary bands & retention")
    ]
    for i, r_vals in enumerate(rows5):
        for j, val in enumerate(r_vals):
            cell = tbl5.cell(i+1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else CARD_BG
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    format_run(r, "Arial", 9, bold=(j == 0), color=NAVY)

    # =========================================================================
    # SLIDE 6: WORKFORCEX SYSTEM ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s6, "WorkforceX Enterprise System Architecture", 6)

    arch_img = os.path.join(ASSETS_DIR, "Figure_3_1_System_Architecture.png")
    if os.path.exists(arch_img):
        s6.shapes.add_picture(arch_img, Inches(0.6), Inches(1.15), width=Inches(8.8), height=Inches(3.95))

    # =========================================================================
    # SLIDE 7: DUAL PREDICTIVE MACHINE LEARNING MODELS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s7, "Dual Predictive ML Models (JDS & SDS)", 7)

    items_7_jds = [
        ("Objective: ", "Predict probability of top-tier junior career progression."),
        ("Architecture: ", "Gradient Boosted Classifier + L2 Regularized Logistic."),
        ("Validation: ", "5-Fold Stratified Cross-Validation with calibration."),
        ("ROC-AUC Score: ", "0.812 (Superior discrimination vs 0.50 baseline)."),
        ("Accuracy: ", "79.8%  |  Precision: 81.4%  |  Recall: 75.6%."),
        ("F1-Score: ", "0.784 harmonic balance.")
    ]
    add_card(s7, Inches(0.6), Inches(1.15), Inches(4.2), Inches(4.0), "1. JUNIOR SUCCESS MODEL (JDS)", items_7_jds, NAVY)

    items_7_sds = [
        ("Objective: ", "Predict senior leadership effectiveness from personality traits."),
        ("Input Features: ", "Standardized Big Five (OCEAN) psychometrics."),
        ("Architecture: ", "Multinomial Calibrated Ensemble Classifier."),
        ("ROC-AUC Score: ", "0.843 (Robust class-separating decision boundary)."),
        ("Key Discovery: ", "Conscientiousness & Openness drive 46% of variance."),
        ("Defensibility: ", "Isotonic calibration ensures reliable confidence scores.")
    ]
    add_card(s7, Inches(5.2), Inches(1.15), Inches(4.2), Inches(4.0), "2. SENIOR PERSONALITY MODEL (SDS)", items_7_sds, GREEN)

    # =========================================================================
    # SLIDE 8: EXPLAINABLE AI (XAI) & ATTRIBUTIONS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s8, "Explainable AI (XAI) & TreeSHAP Attribution Core", 8)

    items_8 = [
        ("Why XAI Matters: ", "Black-box HR models face regulatory rejection. WorkforceX ensures audit compliance."),
        ("TreeSHAP Core: ", "Evaluates marginal feature contributions across all subset coalitions in O(TLD^2) time."),
        ("Top Positive Driver: ", "Python Programming (+38.4% SHAP uplift) and ML Design (+34.2%)."),
        ("Actionable Output: ", "Identifies the exact single skill that provides the highest marginal probability jump.")
    ]
    add_card(s8, Inches(0.6), Inches(1.15), Inches(3.8), Inches(4.0), "GAME-THEORETIC SHAPLEY AUDITING", items_8, NAVY)

    shap_img = os.path.join(ASSETS_DIR, "Figure_5_2_SHAP_Summary.png")
    if os.path.exists(shap_img):
        s8.shapes.add_picture(shap_img, Inches(4.6), Inches(1.18), width=Inches(4.8), height=Inches(3.9))

    # =========================================================================
    # SLIDE 9: MARKET X SUCCESS 2X2 STRATEGIC MATRIX
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s9, "Market Demand × Observed Success 2×2 Matrix", 9)

    matrix_img = os.path.join(ASSETS_DIR, "Figure_4_1_Market_Success_Matrix.png")
    if os.path.exists(matrix_img):
        s9.shapes.add_picture(matrix_img, Inches(0.6), Inches(1.18), width=Inches(4.3), height=Inches(3.9))

    items_9 = [
        ("Q1: Strategic Goldmine (High Demand, High Success): ", "Python, Machine Learning, Cloud Architecture. Core upskilling targets."),
        ("Q2: Future Differentiators (Emerging Demand, High Success): ", "GenAI, LLMs, TreeSHAP. High upside potential for early reskilling."),
        ("Q3: Baseline Hygiene (High Demand, Moderate Success): ", "SQL, Excel. Essential prerequisites with limited promotional delta."),
        ("Q4: Low Priority (Low Demand, Low Success): ", "Legacy SAS, VBA scripting. Deprecate corporate training budgets.")
    ]
    add_card(s9, Inches(5.1), Inches(1.15), Inches(4.3), Inches(4.0), "STRATEGIC QUADRANT ACTIONS", items_9, CRIMSON)

    # =========================================================================
    # SLIDE 10: CAREER GPS & ROLE-SKILL GRAPH
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s10, "AI Career GPS & Role–Skill Graph Topology", 10)

    graph_img = os.path.join(ASSETS_DIR, "Figure_3_2_Career_GPS_Graph.png")
    if os.path.exists(graph_img):
        s10.shapes.add_picture(graph_img, Inches(0.6), Inches(1.18), width=Inches(4.5), height=Inches(3.9))

    items_10 = [
        ("Bipartite Network: ", "Models roles and skills with Jaccard distance weights d(u,v) = 1 - J(u,v)."),
        ("Career GPS Routing: ", "Executes Dijkstra shortest-path to map the lowest-friction upskilling path."),
        ("Skill Gap Engine: ", "Calculates exact missing competencies between current and target roles."),
        ("Optimal Trajectory: ", "Junior Data Scientist -> Python/ML/Cloud -> Senior Data Scientist with minimal transition friction.")
    ]
    add_card(s10, Inches(5.3), Inches(1.15), Inches(4.1), Inches(4.0), "GRAPH-THEORETIC ROUTING", items_10, NAVY)

    # =========================================================================
    # SLIDE 11: WORKFORCE SIMULATOR: BUILD VS BUY VS AUTOMATE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s11, "Workforce Simulator: Build vs Buy vs Automate", 11)

    sim_img = os.path.join(ASSETS_DIR, "Figure_5_3_Simulator_ROI.png")
    if os.path.exists(sim_img):
        s11.shapes.add_picture(sim_img, Inches(0.6), Inches(1.15), width=Inches(8.8), height=Inches(3.95))

    # =========================================================================
    # SLIDE 12: MODERN SOFTWARE TOOLS, CI/CD & SELENIUM
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s12, "Full-Stack Implementation, CI/CD & Selenium QA", 12)

    cards_12 = [
        ("Backend & REST APIs", [
            ("Framework: ", "Modular Flask WSGI microservice"),
            ("JSON Endpoints: ", "Career GPS, SHAP, ROI APIs"),
            ("Latency: ", "< 45ms average response time"),
            ("Data Store: ", "Vectorized in-memory data store")
        ], Inches(0.6), Inches(1.15), Inches(2.7), Inches(4.0), NAVY),

        ("Selenium Automated QA", [
            ("Engine: ", "Selenium WebDriver (Python)"),
            ("Coverage: ", "22 automated browser E2E tests"),
            ("Validation: ", "Form inputs, DOM & Chart renders"),
            ("Pass Rate: ", "100% Pass across all UI workflows")
        ], Inches(3.65), Inches(1.15), Inches(2.7), Inches(4.0), CRIMSON),

        ("CI/CD & Quality Control", [
            ("Unit Testing: ", "Pytest modular test harness"),
            ("Test Coverage: ", "107 assertions across all modules"),
            ("GitHub Actions: ", "Automated PR regression pipeline"),
            ("Reproducibility: ", "Deterministic random seeds")
        ], Inches(6.7), Inches(1.15), Inches(2.7), Inches(4.0), GREEN)
    ]
    for c_title, items, left, top, width, height, color in cards_12:
        add_card(s12, left, top, width, height, c_title, items, color)

    # =========================================================================
    # SLIDE 13: RESULTS ANALYSIS & BENCHMARKS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s13, "Results Analysis & Validation Benchmarks", 13)

    table_shape13 = s13.shapes.add_table(6, 4, Inches(0.6), Inches(1.2), Inches(8.8), Inches(3.8))
    tbl13 = table_shape13.table
    tbl13.columns[0].width = Inches(2.0)
    tbl13.columns[1].width = Inches(1.9)
    tbl13.columns[2].width = Inches(2.1)
    tbl13.columns[3].width = Inches(2.8)

    headers13 = ["Dimension / Module", "Empirical Metric", "Baseline Benchmark", "Industrial Validation Outcome"]
    for j, h in enumerate(headers13):
        cell = tbl13.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                format_run(r, "Arial", 10, bold=True, color=WHITE)

    rows13 = [
        ("Data Quality Engine", "13,965 records cleaned", "9.8% raw missingness", "0.0% residual nulls; 100% audited"),
        ("Junior Success (JDS)", "ROC-AUC: 0.812", "0.500 (Chance baseline)", "+31.2% predictive discrimination lift"),
        ("Senior Personality (SDS)", "ROC-AUC: 0.843", "0.620 (Heuristic review)", "46% variance driven by Big Five traits"),
        ("Build vs Buy ROI", "6.3x Cost Advantage", "$118,000 external hire", "$99,500 saved per transition ($4.97M/50 roles)"),
        ("Automated QA Suite", "100% Test Pass Rate", "Manual sanity check", "7 test suites, 107 assertions, 22 Selenium E2E")
    ]
    for i, r_vals in enumerate(rows13):
        for j, val in enumerate(r_vals):
            cell = tbl13.cell(i+1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else CARD_BG
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    format_run(r, "Arial", 9.5, bold=(j == 0), color=NAVY)

    # =========================================================================
    # SLIDE 14: KEY LEARNINGS, FUTURE SCOPE & CONCLUSION
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_clean_slide_header(s14, "Key Learnings, Future Scope & Conclusion", 14)

    items_14_left = [
        ("Full-Lifecycle ML: ", "Data cleaning pipelines, model training, cross-validation, and calibrated probability serving."),
        ("Explainable AI: ", "Game-theoretic TreeSHAP implementation ensuring auditable HR recommendations."),
        ("Network Graph Algorithms: ", "Bipartite projections, Jaccard distance modeling, and Dijkstra shortest paths."),
        ("Automated E2E Testing: ", "Selenium WebDriver browser automation integrated into continuous deployment pipelines.")
    ]
    add_card(s14, Inches(0.6), Inches(1.15), Inches(4.2), Inches(4.0), "KEY INDUSTRIAL & ACADEMIC LEARNINGS", items_14_left, GREEN)

    # Right Card: Future Scope & Q&A
    bg14_r = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.2), Inches(1.15), Inches(4.2), Inches(4.0))
    bg14_r.fill.solid()
    bg14_r.fill.fore_color.rgb = CARD_BG
    bg14_r.line.color.rgb = CARD_BORDER

    tb14_r = s14.shapes.add_textbox(Inches(5.32), Inches(1.25), Inches(3.96), Inches(3.8))
    tf14_r = tb14_r.text_frame
    tf14_r.word_wrap = True
    tf14_r.margin_left = tf14_r.margin_top = tf14_r.margin_right = tf14_r.margin_bottom = 0

    p_hd14 = tf14_r.paragraphs[0]
    p_hd14.text = "FUTURE WORK & ACKNOWLEDGEMENT"
    format_run(p_hd14.runs[0], "Arial", 12.5, bold=True, color=CRIMSON)

    fut = [
        ("LLM Workforce Copilot: ", "Integrating conversational agents for natural language workforce querying."),
        ("Live Market Scraping: ", "Automated streaming scrapers for real-time skill demand updating."),
        ("Enterprise Multi-Tenancy: ", "Dockerized microservices deployed via Kubernetes orchestration.")
    ]
    for pre, bdy in fut:
        p = tf14_r.add_paragraph()
        p.space_before = Pt(4)
        p.text = f"• {pre}"
        format_run(p.runs[0], "Arial", 10.5, bold=True, color=NAVY)
        r = p.add_run()
        r.text = bdy
        format_run(r, "Arial", 10, color=SLATE)

    p_qa = tf14_r.add_paragraph()
    p_qa.space_before = Pt(16)
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.text = "THANK YOU!\nOPEN FOR QUESTIONS & DISCUSSION (Q&A)"
    format_run(p_qa.runs[0], "Arial", 12, bold=True, color=CRIMSON)

    prs.save(PPTX_PATH)
    print(f"Generated Industrial Training Presentation PPTX: {PPTX_PATH} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    build_presentation()
