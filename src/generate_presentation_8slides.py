"""
generate_presentation_8slides.py
Builds a high-impact, highly visual 8-slide presentation (90% visuals, 10% plain-language info)
for Abhinav Chitrey (UID: 24BCS12754), Chandigarh University (CSE-Takshashila).

Design Specifications:
- Exactly 8 slides
- 90% visuals (large stat cards, process flow arrows, side-by-side comparison boxes, roadmap badges)
- 10% text in simple, non-technical plain English (no dense AI/ML jargon, ROC-AUC, or math formulas)
- Slide 1: Official CU Takshashila Branding (clean background with gear watermark behind the logo, Section 802-B, Remote mode, no viva date)
- Slides 2-8: Clean, modern executive visual layout
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission"
EXTRACTED_DIR = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\extracted_template_assets"
PPTX_PATH = os.path.join(OUTPUT_DIR, "Industrial_Training_Presentation_8Slides.pptx")
PDF_PATH = os.path.join(OUTPUT_DIR, "Industrial_Training_Presentation_8Slides.pdf")

# Palette
NAVY = RGBColor(13, 35, 58)        # #0D233A - Primary Executive
CRIMSON = RGBColor(176, 32, 32)    # #B02020 - CU Accent / Warning
GREEN = RGBColor(24, 134, 75)      # #18864B - Success / Value
SLATE = RGBColor(71, 85, 105)      # #475569 - Body text
MUTED = RGBColor(148, 163, 184)    # #94A3B8 - Subtitles / Borders
CARD_BG = RGBColor(248, 250, 252)  # #F8FAFC - Clean Card Background
CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0 - Card Borders
WHITE = RGBColor(255, 255, 255)
GOLD = RGBColor(217, 119, 6)       # #D97706 - Milestone Gold
BLUE_ACCENT = RGBColor(2, 132, 199) # #0284C7 - Info Blue
LIGHT_RED_BG = RGBColor(254, 242, 242)
LIGHT_GREEN_BG = RGBColor(240, 253, 244)
LIGHT_BLUE_BG = RGBColor(240, 249, 255)

def format_run(run, font_name="Arial", size_pt=11, bold=False, color=NAVY, italic=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def add_clean_header(slide, title_text, category_text, slide_num, total_slides=8):
    """Add sleek modern slide header with slide category tag and numbering."""
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.6), Inches(0.22), Inches(6.0), Inches(0.25))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = False
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    format_run(p_cat.runs[0], "Arial", 9, bold=True, color=CRIMSON)

    # Title
    tb_title = slide.shapes.add_textbox(Inches(0.6), Inches(0.42), Inches(7.5), Inches(0.45))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = False
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_t = tf_title.paragraphs[0]
    p_t.text = title_text
    format_run(p_t.runs[0], "Arial", 20, bold=True, color=NAVY)

    # Slide Number Badge
    tb_num = slide.shapes.add_textbox(Inches(8.2), Inches(0.35), Inches(1.2), Inches(0.35))
    tf_num = tb_num.text_frame
    tf_num.word_wrap = False
    tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"Slide {slide_num} of {total_slides}"
    format_run(p_num.runs[0], "Arial", 10, bold=True, color=MUTED)

    # Subtle Accent Divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.92), Inches(8.8), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = CARD_BORDER
    line.line.color.rgb = CARD_BORDER

def create_visual_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Draw a smooth rounded card for visual grouping."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)
    return card

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6]

    print("Building 8-slide visual presentation...")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Official CU Takshashila Branding)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg_img1 = os.path.join(EXTRACTED_DIR, "slide_1_bg_final.png")
    if not os.path.exists(bg_img1):
        bg_img1 = os.path.join(EXTRACTED_DIR, "slide_1_img_0.png")
    if os.path.exists(bg_img1):
        s1.shapes.add_picture(bg_img1, 0, 0, width=Inches(10.0), height=Inches(5.625))

    # Main Title Box
    tb_t1 = s1.shapes.add_textbox(Inches(0.6), Inches(1.15), Inches(8.8), Inches(1.3))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    p_t1 = tf_t1.paragraphs[0]
    p_t1.text = "WORKFORCEX"
    format_run(p_t1.runs[0], "Arial", 38, bold=True, color=NAVY)

    p_sub1 = tf_t1.add_paragraph()
    p_sub1.text = "Smart Career GPS & Enterprise Workforce Intelligence Platform"
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
    p.text = "UID: 24BCS12754  |  Section: 802-B\nBachelor of Engineering in CSE\nGroup: CSE-TAKSHASHILA (802-B)\nChandigarh University, Mohali, Punjab"
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
    # SLIDE 2: THE PROBLEM (Visual Side-by-Side Comparison)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_clean_header(s2, "The Real-World Hiring & Talent Crisis", "Industry Need Identification", 2)

    # Left Box: Old Way (Red)
    create_visual_card(s2, Inches(0.6), Inches(1.15), Inches(4.25), Inches(4.1), LIGHT_RED_BG, RGBColor(252, 165, 165))
    tb_old = s2.shapes.add_textbox(Inches(0.8), Inches(1.30), Inches(3.85), Inches(3.8))
    tf_old = tb_old.text_frame
    tf_old.word_wrap = True

    p = tf_old.paragraphs[0]
    p.text = "THE TRADITIONAL WAY"
    format_run(p.runs[0], "Arial", 14, bold=True, color=CRIMSON)

    items_old = [
        ("🐢 75–110 Days Long Hiring Delays", "Companies wait 3+ months just to hire one senior technical expert."),
        ("💸 Prohibitive $118,000+ Cost Per Hire", "Massive agency commissions, sign-on bonuses, and lost productivity."),
        ("🎲 Subjective Guesswork & Keyword Filters", "78% of managers rely on gut feeling or basic resume keyword search."),
        ("🚪 High Employee Turnover", "Valuable employees quit because they cannot see a clear path up.")
    ]
    for title, desc in items_old:
        p_t = tf_old.add_paragraph()
        p_t.space_before = Pt(8)
        p_t.text = title
        format_run(p_t.runs[0], "Arial", 11.5, bold=True, color=NAVY)
        p_d = tf_old.add_paragraph()
        p_d.text = desc
        format_run(p_d.runs[0], "Arial", 10, color=SLATE)

    # Right Box: Smart Way (Green)
    create_visual_card(s2, Inches(5.15), Inches(1.15), Inches(4.25), Inches(4.1), LIGHT_GREEN_BG, RGBColor(187, 247, 208))
    tb_new = s2.shapes.add_textbox(Inches(5.35), Inches(1.30), Inches(3.85), Inches(3.8))
    tf_new = tb_new.text_frame
    tf_new.word_wrap = True

    p = tf_new.paragraphs[0]
    p.text = "THE WORKFORCEX SMART SOLUTION"
    format_run(p.runs[0], "Arial", 14, bold=True, color=GREEN)

    items_new = [
        ("⚡ Fast 6-Week Reskilling Cycles", "Train internal team members directly on targeted competencies."),
        ("💰 6.3× More Cost-Effective", "Massive savings compared to hiring from outside recruitment agencies."),
        ("📊 Objective, Data-Driven Matching", "Clear, mathematical skill matching backed by 13,900+ real records."),
        ("🧭 Crystal-Clear Career GPS", "Every employee sees their step-by-step roadmap to promotions.")
    ]
    for title, desc in items_new:
        p_t = tf_new.add_paragraph()
        p_t.space_before = Pt(8)
        p_t.text = title
        format_run(p_t.runs[0], "Arial", 11.5, bold=True, color=NAVY)
        p_d = tf_new.add_paragraph()
        p_d.text = desc
        format_run(p_d.runs[0], "Arial", 10, color=SLATE)

    # =========================================================================
    # SLIDE 3: PROJECT GOALS & 4 CORE PILLARS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_clean_header(s3, "Four Strategic Pillars of WorkforceX", "Project Vision & Architecture", 3)

    pillars = [
        ("1. Skill Taxonomy", "Reads job postings to identify what skills the tech industry actually demands today.", BLUE_ACCENT, "📊"),
        ("2. Career GPS", "Acts like Google Maps for careers—giving step-by-step directions to reach dream roles.", GREEN, "🧭"),
        ("3. Transparent Logic", "Gives plain, easy-to-understand reasons for every recommendation—zero black boxes.", GOLD, "🔍"),
        ("4. Smart Budgeting", "Calculates instant ROI comparing Training (Build), Hiring (Buy), or Automating tasks.", CRIMSON, "💵")
    ]

    card_w = Inches(2.05)
    card_h = Inches(4.0)
    for i, (p_title, p_desc, col, icon) in enumerate(pillars):
        c_left = Inches(0.6 + i * 2.25)
        create_visual_card(s3, c_left, Inches(1.15), card_w, card_h)

        # Header bar inside card
        hbar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left + Inches(0.02), Inches(1.17), card_w - Inches(0.04), Inches(0.08))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = col
        hbar.line.fill.background()

        tb = s3.shapes.add_textbox(c_left + Inches(0.12), Inches(1.35), card_w - Inches(0.24), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_ico = tf.paragraphs[0]
        p_ico.text = icon
        p_ico.alignment = PP_ALIGN.CENTER
        format_run(p_ico.runs[0], "Arial", 32)

        p_name = tf.add_paragraph()
        p_name.space_before = Pt(8)
        p_name.text = p_title
        p_name.alignment = PP_ALIGN.CENTER
        format_run(p_name.runs[0], "Arial", 12.5, bold=True, color=col)

        p_body = tf.add_paragraph()
        p_body.space_before = Pt(12)
        p_body.text = p_desc
        format_run(p_body.runs[0], "Arial", 10.5, color=SLATE)

    # =========================================================================
    # SLIDE 4: THE 6-WEEK INDUSTRIAL ROADMAP
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_clean_header(s4, "Six-Week Industrial Training Execution Roadmap", "Internship Timeline & Milestones", 4)

    weeks = [
        ("Week 1", "Discovery & Architecture", "Onboarding, corporate setup, audited 4 raw datasets & planned architecture.", NAVY),
        ("Week 2", "Data Cleaning Engine", "Built automated cleaning pipeline, standardized 13,900+ records & 100+ skills.", BLUE_ACCENT),
        ("Week 3", "Smart Predictors", "Trained intelligent readiness models predicting career transition success.", GREEN),
        ("Week 4", "Career GPS Engine", "Built career navigation roadmaps & plain-language explanation system.", GOLD),
        ("Week 5", "Financial Simulator", "Developed Build-vs-Buy ROI calculator & interactive web dashboard.", CRIMSON),
        ("Week 6", "QA & Final Delivery", "Automated browser testing with Selenium & presented final executive review.", NAVY)
    ]

    w_box_w = Inches(1.35)
    w_box_h = Inches(3.9)
    for i, (wk, w_title, w_desc, col) in enumerate(weeks):
        left_pos = Inches(0.6 + i * 1.48)
        create_visual_card(s4, left_pos, Inches(1.2), w_box_w, w_box_h)

        # Top tag badge
        tag = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos + Inches(0.1), Inches(1.32), w_box_w - Inches(0.2), Inches(0.36))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.fill.background()
        tf_tag = tag.text_frame
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = wk
        p_tag.alignment = PP_ALIGN.CENTER
        format_run(p_tag.runs[0], "Arial", 11, bold=True, color=WHITE)

        # Content
        tb = s4.shapes.add_textbox(left_pos + Inches(0.08), Inches(1.78), w_box_w - Inches(0.16), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = w_title
        p_t.alignment = PP_ALIGN.CENTER
        format_run(p_t.runs[0], "Arial", 10.5, bold=True, color=NAVY)

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(8)
        p_d.text = w_desc
        format_run(p_d.runs[0], "Arial", 9.5, color=SLATE)

    # =========================================================================
    # SLIDE 5: HOW THE SYSTEM WORKS (Simple 4-Step Process Flow)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_clean_header(s5, "How WorkforceX Works: Simple 4-Step Flow", "System Methodology & Workflow", 5)

    steps = [
        ("Step 1", "Collect Real Data", "Gathers live job postings, market salaries, and employee skill profiles.", "📥", BLUE_ACCENT),
        ("Step 2", "Clean & Organize", "Standardizes messy text into 100+ verified skills with zero duplicates.", "⚙️", GREEN),
        ("Step 3", "Map Career Roadmaps", "Compares employee skills to dream jobs and computes the best learning path.", "🗺️", GOLD),
        ("Step 4", "Interactive Action", "Displays instant recommendations and cost savings on a web dashboard.", "💻", CRIMSON)
    ]

    s_box_w = Inches(2.05)
    s_box_h = Inches(3.9)
    for i, (st, st_title, st_desc, icon, col) in enumerate(steps):
        left_pos = Inches(0.6 + i * 2.25)
        create_visual_card(s5, left_pos, Inches(1.2), s_box_w, s_box_h)

        # Step badge
        tb_b = s5.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.3), s_box_w - Inches(0.2), Inches(0.35))
        tf_b = tb_b.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = st.upper()
        p_b.alignment = PP_ALIGN.CENTER
        format_run(p_b.runs[0], "Arial", 11, bold=True, color=col)

        # Icon
        tb_i = s5.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.7), s_box_w - Inches(0.2), Inches(0.7))
        tf_i = tb_i.text_frame
        p_i = tf_i.paragraphs[0]
        p_i.text = icon
        p_i.alignment = PP_ALIGN.CENTER
        format_run(p_i.runs[0], "Arial", 32)

        # Text
        tb_t = s5.shapes.add_textbox(left_pos + Inches(0.12), Inches(2.55), s_box_w - Inches(0.24), Inches(2.3))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True

        p_t = tf_t.paragraphs[0]
        p_t.text = st_title
        p_t.alignment = PP_ALIGN.CENTER
        format_run(p_t.runs[0], "Arial", 12.5, bold=True, color=NAVY)

        p_d = tf_t.add_paragraph()
        p_d.space_before = Pt(8)
        p_d.text = st_desc
        format_run(p_d.runs[0], "Arial", 10.5, color=SLATE)

    # =========================================================================
    # SLIDE 6: THE WEB PLATFORM IN ACTION (Core Features)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_clean_header(s6, "Interactive Management Platform Features", "Web Application & Tools", 6)

    features = [
        ("Career GPS Navigator", "Employees choose any target role (e.g. Junior Analyst to AI Lead) and get an immediate step-by-step learning journey.", "🚀", [
            "Shows exact skills required next",
            "Estimates weeks to reach target",
            "Removes confusion from career moves"
        ]),
        ("Visual Skill Gap Meter", "Managers inspect employee readiness at a glance with clear visual bars instead of complicated statistical tables.", "📊", [
            "Identifies strong foundational skills",
            "Highlights top 3 priority gaps",
            "100% fair and transparent criteria"
        ]),
        ("Cost-Benefit Calculator", "Interactive scenario sliders allow executives to see instant dollar savings from training internal staff.", "💰", [
            "Adjust headcount and target timelines",
            "Compares Training vs Hiring costs",
            "Demonstrates clear 6.3× cost savings"
        ])
    ]

    f_box_w = Inches(2.8)
    f_box_h = Inches(4.0)
    for i, (f_title, f_desc, icon, bullets) in enumerate(features):
        left_pos = Inches(0.6 + i * 3.0)
        create_visual_card(s6, left_pos, Inches(1.15), f_box_w, f_box_h)

        tb = s6.shapes.add_textbox(left_pos + Inches(0.15), Inches(1.3), f_box_w - Inches(0.3), f_box_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_i = tf.paragraphs[0]
        p_i.text = f"{icon}  {f_title}"
        format_run(p_i.runs[0], "Arial", 13, bold=True, color=NAVY)

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(8)
        p_d.text = f_desc
        format_run(p_d.runs[0], "Arial", 10, color=SLATE)

        p_sep = tf.add_paragraph()
        p_sep.space_before = Pt(10)
        p_sep.text = "KEY HIGHLIGHTS:"
        format_run(p_sep.runs[0], "Arial", 9.5, bold=True, color=CRIMSON)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(4)
            p_b.text = f"• {b}"
            format_run(p_b.runs[0], "Arial", 9.5, color=NAVY)

    # =========================================================================
    # SLIDE 7: KEY RESULTS & BUSINESS VALUE (Big Stat Cards)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_clean_header(s7, "Tangible Business Results & Impact", "Project Impact & Practical Value", 7)

    stats = [
        ("13,900+", "Records Processed", "Real industry job ads & skills cleaned with 100% data integrity.", GREEN),
        ("6.3× ROI", "Cost Efficiency", "Proven dollar savings for training internal staff over external recruiters.", CRIMSON),
        ("6 Weeks", "Skill Acquisition", "Fast internal learning cycles compared to 90+ days external hiring delay.", BLUE_ACCENT),
        ("100%", "Transparent Logic", "Zero mystery black boxes—every career decision is fully explainable.", GOLD)
    ]

    card_w = Inches(4.25)
    card_h = Inches(1.85)

    positions = [
        (Inches(0.6), Inches(1.2)),
        (Inches(5.15), Inches(1.2)),
        (Inches(0.6), Inches(3.25)),
        (Inches(5.15), Inches(3.25))
    ]

    for i, (big_num, stat_title, stat_desc, col) in enumerate(stats):
        c_left, c_top = positions[i]
        create_visual_card(s7, c_left, c_top, card_w, card_h)

        tb = s7.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.15), card_w - Inches(0.4), card_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = big_num
        format_run(p_num.runs[0], "Arial", 28, bold=True, color=col)

        p_st = tf.add_paragraph()
        p_st.space_before = Pt(2)
        p_st.text = stat_title
        format_run(p_st.runs[0], "Arial", 12.5, bold=True, color=NAVY)

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(4)
        p_d.text = stat_desc
        format_run(p_d.runs[0], "Arial", 10, color=SLATE)

    # =========================================================================
    # SLIDE 8: SUMMARY & KEY LEARNINGS (Conclusion)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_clean_header(s8, "Summary & Key Internship Learnings", "Conclusion & Reflections", 8)

    # 3 Summary Cards
    conclusions = [
        ("Hands-on Industrial Exposure", "Gained real enterprise R&D experience at CogniStrat Technologies, working with real datasets, corporate standards, and executive mentorship.", "🏢"),
        ("Solving Real Corporate Friction", "Addressed the critical industry challenge of high hiring costs ($118k+) and long delays by proving a faster, cheaper internal reskilling model.", "💡"),
        ("Complete End-to-End Delivery", "Successfully completed the entire cycle: from messy raw data to automated cleaning, predictive tools, visual dashboards, and automated test suites.", "🎯")
    ]

    c_box_w = Inches(2.8)
    c_box_h = Inches(2.6)
    for i, (c_title, c_desc, ico) in enumerate(conclusions):
        c_left = Inches(0.6 + i * 3.0)
        create_visual_card(s8, c_left, Inches(1.2), c_box_w, c_box_h)

        tb = s8.shapes.add_textbox(c_left + Inches(0.15), Inches(1.35), c_box_w - Inches(0.3), c_box_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_i = tf.paragraphs[0]
        p_i.text = f"{ico}  {c_title}"
        format_run(p_i.runs[0], "Arial", 12.5, bold=True, color=NAVY)

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(8)
        p_d.text = c_desc
        format_run(p_d.runs[0], "Arial", 10, color=SLATE)

    # Bottom Thank You & Q&A Banner
    thank_card = create_visual_card(s8, Inches(0.6), Inches(4.05), Inches(8.8), Inches(1.2), NAVY, NAVY)
    tb_th = s8.shapes.add_textbox(Inches(0.8), Inches(4.15), Inches(8.4), Inches(1.0))
    tf_th = tb_th.text_frame
    tf_th.word_wrap = True

    p_th = tf_th.paragraphs[0]
    p_th.text = "THANK YOU!"
    p_th.alignment = PP_ALIGN.CENTER
    format_run(p_th.runs[0], "Arial", 20, bold=True, color=GOLD)

    p_qa = tf_th.add_paragraph()
    p_qa.space_before = Pt(2)
    p_qa.text = "Open for Questions & Discussion  |  Abhinav Chitrey (24BCS12754 - 802-B)"
    p_qa.alignment = PP_ALIGN.CENTER
    format_run(p_qa.runs[0], "Arial", 12, bold=True, color=WHITE)

    prs.save(PPTX_PATH)
    print(f"SUCCESS: Saved 8-slide visual presentation to {PPTX_PATH}")

if __name__ == "__main__":
    build_presentation()
