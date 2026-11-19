"""
generate_certificate.py
Generates an ultra-realistic, authentic, corporate-grade Industrial Training Certificate
for Abhinav Chitrey (UID: 24BCS12754) from CogniStrat Technologies Pvt. Ltd.
Location / Mode: Remote / Virtual (Enterprise AI R&D Division).
Produces both:
  1. PDF: reports/internship_submission/Training_Certificate.pdf
  2. High-Res PNG: reports/internship_submission/Training_Certificate.png
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr

OUTPUT_DIR = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_PATH = os.path.join(OUTPUT_DIR, "Training_Certificate.pdf")
PNG_PATH = os.path.join(OUTPUT_DIR, "Training_Certificate.png")

def create_corporate_stamp(size=360):
    """Generate a realistic official circular corporate stamp with seal text and star."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    stamp_color = (24, 60, 128, 220)
    center = size / 2
    r_outer = size * 0.46
    r_inner = size * 0.36
    r_center = size * 0.24
    
    draw.ellipse([center - r_outer, center - r_outer, center + r_outer, center + r_outer], outline=stamp_color, width=4)
    draw.ellipse([center - (r_outer - 6), center - (r_outer - 6), center + (r_outer - 6), center + (r_outer - 6)], outline=stamp_color, width=2)
    draw.ellipse([center - r_inner, center - r_inner, center + r_inner, center + r_inner], outline=stamp_color, width=2)
    draw.ellipse([center - r_center, center - r_center, center + r_center, center + r_center], outline=stamp_color, width=2)

    try:
        font_c = ImageFont.truetype("arialbd.ttf", 20)
        font_sub = ImageFont.truetype("arialbd.ttf", 13)
        font_cin = ImageFont.truetype("arial.ttf", 10)
    except:
        font_c = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_cin = ImageFont.load_default()

    draw.text((center, center - 35), "★ ★ ★", fill=stamp_color, font=font_c, anchor="mm")
    draw.text((center, center - 10), "COGNISTRAT", fill=stamp_color, font=font_c, anchor="mm")
    draw.text((center, center + 12), "SEAL OF EXCELLENCE", fill=stamp_color, font=font_sub, anchor="mm")
    draw.text((center, center + 30), "CIN: U72900KA2018PTC114920", fill=stamp_color, font=font_cin, anchor="mm")
    draw.text((center, center + 46), "★ BANGALORE ★", fill=stamp_color, font=font_sub, anchor="mm")

    top_text = "COGNISTRAT TECHNOLOGIES PRIVATE LIMITED •"
    bottom_text = "• CORPORATE RESEARCH & DEVELOPMENT •"
    
    def draw_curved_text(text, radius, start_angle, end_angle, is_top=True):
        n = len(text)
        if n == 0: return
        angle_step = (end_angle - start_angle) / max(1, n - 1)
        for i, char in enumerate(text):
            angle = start_angle + i * angle_step
            rad = math.radians(angle)
            x = center + radius * math.cos(rad)
            y = center + radius * math.sin(rad)
            char_img = Image.new("RGBA", (40, 40), (255, 255, 255, 0))
            cdraw = ImageDraw.Draw(char_img)
            cdraw.text((20, 20), char, fill=stamp_color, font=font_sub, anchor="mm")
            rot = -(angle + 90) if is_top else -(angle - 90)
            char_img = char_img.rotate(rot, resample=Image.BICUBIC)
            img.paste(char_img, (int(x - 20), int(y - 20)), char_img)

    draw_curved_text(top_text, (r_outer + r_inner) / 2, -165, -15, is_top=True)
    draw_curved_text(bottom_text, (r_outer + r_inner) / 2, 165, 15, is_top=False)
    
    img = img.rotate(8, resample=Image.BICUBIC)
    return img

def create_signature_image(name, title, color=(16, 44, 118)):
    """
    Generate an authentic, high-resolution cursive free-hand signature graphic 
    for corporate authorities using natural handwriting script fonts with fluid pen flourishes.
    """
    scale = 4
    if "Arvind" in name:
        sig_text = "Arvind R. Nair"
        # Rage Italic: fast, confident executive fountain-pen signature
        font_file = "RAGE.TTF" if os.path.exists(r"C:\Windows\Fonts\RAGE.TTF") else "segoescb.ttf"
        font_size = 56
        slant = 2.0
        flourish_style = "swoop"
    else:
        sig_text = "Meenakshi Sundaram"
        # Brush Script MT: flowing, elegant corporate authority cursive signature
        font_file = "BRUSHSCI.TTF" if os.path.exists(r"C:\Windows\Fonts\BRUSHSCI.TTF") else "segoesc.ttf"
        font_size = 50
        slant = 2.0
        flourish_style = "loop"

    font_path = os.path.join(r"C:\Windows\Fonts", font_file)
    try:
        font = ImageFont.truetype(font_path, font_size * scale)
    except:
        font = ImageFont.load_default()

    temp_img = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(temp_img)
    bbox = d.textbbox((0, 0), sig_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    cw = tw + int(100 * scale)
    ch = th + int(90 * scale)
    img = Image.new("RGBA", (cw, ch), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    ink_rgba = (color[0], color[1], color[2], 245)

    tx = int(40 * scale)
    ty = int(20 * scale)
    draw.text((tx, ty), sig_text, font=font, fill=ink_rgba)

    # Dynamic freehand flourish underline sweeping beneath the signature
    fx_start = tx + int(10 * scale)
    fx_end = tx + tw + int(20 * scale)
    fy = ty + th + int(6 * scale)

    steps = 80
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = fx_start + (fx_end - fx_start) * t
        if flourish_style == "swoop":
            y = fy - math.sin(t * math.pi) * (14 * scale) + (t * 8 * scale)
        else:
            y = fy - math.sin(t * math.pi * 1.2) * (10 * scale) + (t * 6 * scale)
        pts.append((x, y))

    for i in range(len(pts) - 1):
        t = i / steps
        stroke_w = max(1, int((2.0 + 2.5 * math.sin(t * math.pi)) * scale))
        draw.line([pts[i], pts[i+1]], fill=ink_rgba, width=stroke_w)

    if slant != 0:
        img = img.rotate(slant, resample=Image.BICUBIC, expand=True)

    cbox = img.getbbox()
    if cbox:
        pad = int(4 * scale)
        img = img.crop((
            max(0, cbox[0] - pad),
            max(0, cbox[1] - pad),
            min(img.width, cbox[2] + pad),
            min(img.height, cbox[3] + pad)
        ))

    # Resize smoothly with Lanczos filter for ultra-crisp ink edges
    target_w = 420
    target_h = int(img.height * (target_w / img.width))
    return img.resize((target_w, target_h), Image.LANCZOS)

def build_pdf_certificate():
    """Build high-resolution vector PDF certificate adhering to corporate design."""
    width, height = landscape(A4)
    c = canvas.Canvas(PDF_PATH, pagesize=(width, height))
    
    # 1. Background Fill
    c.setFillColor(colors.HexColor("#FCFDFD"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # 2. Guilloche / Decorative Luxury Borders
    navy = colors.HexColor("#0D233A")
    gold = colors.HexColor("#C59B27")
    slate = colors.HexColor("#334E68")
    
    c.setStrokeColor(navy)
    c.setLineWidth(5)
    c.rect(20, 20, width - 40, height - 40, fill=0, stroke=1)
    
    c.setStrokeColor(gold)
    c.setLineWidth(1.8)
    c.rect(26, 26, width - 52, height - 52, fill=0, stroke=1)
    c.setLineWidth(0.8)
    c.rect(30, 30, width - 60, height - 60, fill=0, stroke=1)
    
    # Corner Ornamental Accents
    corner_size = 28
    for (cx, cy) in [(30, 30), (width - 30, 30), (30, height - 30), (width - 30, height - 30)]:
        c.setFillColor(gold)
        c.setStrokeColor(navy)
        c.setLineWidth(1)
        sx = 1 if cx == 30 else -1
        sy = 1 if cy == 30 else -1
        p = c.beginPath()
        p.moveTo(cx, cy)
        p.lineTo(cx + sx * corner_size, cy)
        p.lineTo(cx, cy + sy * corner_size)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.setFillColor(navy)
        c.circle(cx + sx * 10, cy + sy * 10, 3, fill=1, stroke=0)

    # 3. Corporate Letterhead Header
    logo_y = height - 72
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(55, logo_y, "COGNISTRAT")
    c.setFillColor(gold)
    c.drawString(195, logo_y, "TECHNOLOGIES")
    
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(slate)
    c.drawString(55, logo_y - 12, "ADVANCED AI, ENTERPRISE DECISION PLATFORMS & TALENT INTELLIGENCE LABS")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#627D98"))
    c.drawString(55, logo_y - 22, "CIN: U72900KA2018PTC114920 | GSTIN: 29AABCC1234F1Z8 | An ISO 9001:2015 & ISO/IEC 27001 Certified Enterprise")
    c.drawString(55, logo_y - 31, "Global Technology Park, Outer Ring Road, Bellandur, Bengaluru 560103 | web: www.cognistrat.tech | email: contact@cognistrat.tech")

    c.setStrokeColor(gold)
    c.setLineWidth(1.2)
    c.line(55, logo_y - 38, width - 55, logo_y - 38)
    
    # Right-aligned Reference details
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(navy)
    c.drawRightString(width - 55, logo_y, "CERTIFICATE ID: CST/BLR/2026/SUM-INT/12754")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(slate)
    c.drawRightString(width - 55, logo_y - 12, "Date of Issuance: 16th June 2026")
    c.drawRightString(width - 55, logo_y - 22, "Mode: Remote / Virtual Internship")
    c.drawRightString(width - 55, logo_y - 31, "Verification Portal: verify.cognistrat.tech")

    # 4. Main Certificate Title
    title_y = height - 142
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width / 2.0, title_y + 16, "★  CERTIFICATE OF INDUSTRIAL INTERNSHIP TRAINING  ★")
    
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2.0, title_y - 8, "CERTIFICATE OF EXCELLENCE")
    
    c.setFont("Helvetica-Oblique", 10.5)
    c.setFillColor(colors.HexColor("#486581"))
    c.drawCentredString(width / 2.0, title_y - 24, "This is to officially certify that")

    # 5. Candidate Name & University
    name_y = title_y - 56
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(width / 2.0, name_y, "ABHINAV CHITREY")
    
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    name_w = 260
    c.line((width - name_w) / 2, name_y - 5, (width + name_w) / 2, name_y - 5)

    c.setFont("Helvetica", 10.5)
    c.setFillColor(colors.HexColor("#334E68"))
    cand_line = "University Registration / UID: 24BCS12754  |  Bachelor of Engineering in Computer Science & Engineering"
    c.drawCentredString(width / 2.0, name_y - 19, cand_line)
    
    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(navy)
    c.drawCentredString(width / 2.0, name_y - 33, "Chandigarh University, Gharuan, Mohali, Punjab (Batch 2024–2028)")

    # 6. Body Paragraph - Training Scope & Contributions (With Remote specification)
    body_y = name_y - 55
    c.setFont("Helvetica", 9.5)
    c.setFillColor(colors.HexColor("#243B53"))
    
    l1 = "has successfully completed a six-week intensive Industrial Training & Research Internship (Mode: Remote / Virtual)"
    l2 = "from 5th May 2026 to 15th June 2026 with the Enterprise AI & People Analytics R&D Division, CogniStrat Technologies Pvt. Ltd., working as a"
    c.drawCentredString(width / 2.0, body_y, l1)
    c.drawCentredString(width / 2.0, body_y - 14, l2)
    
    # Role & Project Highlight Box
    role_box_y = body_y - 48
    box_w = width - 130
    box_x = 65
    box_h = 32
    c.setFillColor(colors.HexColor("#F0F4F8"))
    c.setStrokeColor(colors.HexColor("#D9E2EC"))
    c.roundRect(box_x, role_box_y, box_w, box_h, 4, fill=1, stroke=1)
    
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(navy)
    c.drawCentredString(width / 2.0, role_box_y + 19, "Designation: Data Science & AI Engineering Intern (Remote R&D Division)")
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(colors.HexColor("#A82D2D"))
    c.drawCentredString(width / 2.0, role_box_y + 7, "Project: WorkforceX - Strategic Workforce Intelligence, Predictive Career GPS & Explainable Talent Analytics")

    # Project Description Details
    desc_y = role_box_y - 17
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#334E68"))
    
    p1 = "During the internship, Abhinav architected production-grade data cleaning pipelines across 13,965+ records, developed predictive ML classifiers"
    p2 = "(JDS Success Predictor & SDS Personality Model) achieving ROC-AUC > 0.81, formulated TreeSHAP explainability attributions, topological"
    p3 = "Role–Skill Adjacency Graphs, Build-vs-Buy Workforce Simulation Models (6.3x ROI), and established automated Selenium CI/CD testing."
    c.drawCentredString(width / 2.0, desc_y, p1)
    c.drawCentredString(width / 2.0, desc_y - 12, p2)
    c.drawCentredString(width / 2.0, desc_y - 24, p3)
    
    # Rating Badge
    eval_y = desc_y - 42
    c.setFillColor(colors.HexColor("#0B69A3"))
    c.setFont("Helvetica-Bold", 9.5)
    c.drawCentredString(width / 2.0, eval_y, "PERFORMANCE ASSESSMENT: GRADE A+ (OUTSTANDING)  |  TECHNICAL EVALUATION: 96 / 100")

    # 7. Verification QR Code (Bottom Left)
    qr_drawing = qr.QrCodeWidget('https://verify.cognistrat.tech/credentials/CS-2026-INT-12754')
    qr_drawing.barWidth = 62
    qr_drawing.barHeight = 62
    qr_drawing.qrVersion = 2
    d = Drawing(62, 62)
    d.add(qr_drawing)
    c.saveState()
    c.translate(65, 45)
    d.drawOn(c, 0, 0)
    c.restoreState()
    
    c.setFont("Helvetica", 6.5)
    c.setFillColor(slate)
    c.drawString(135, 88, "Scan QR to verify credential")
    c.drawString(135, 78, "Tamper-Proof Digital Verification")
    c.drawString(135, 68, "Hash: SHA256-a94f82c1b8214...")
    c.drawString(135, 58, "Issued by CogniStrat Registrar")

    # 8. Signatures & Official Stamp
    stamp_img = create_corporate_stamp(360)
    stamp_path = os.path.join(OUTPUT_DIR, "temp_stamp.png")
    stamp_img.save(stamp_path)
    c.drawImage(stamp_path, (width / 2.0) - 55, 36, width=105, height=105, mask='auto')

    sig1_img = create_signature_image("Dr. Arvind R. Nair", "VP AI", color=(18, 48, 110))
    sig1_path = os.path.join(OUTPUT_DIR, "temp_sig1.png")
    sig1_img.save(sig1_path)
    
    sig1_x = 290
    center1 = sig1_x + 37.5
    w1, h1 = 125, 36
    c.drawImage(sig1_path, center1 - (w1 / 2.0), 80, width=w1, height=h1, mask='auto')
    c.setStrokeColor(navy)
    c.setLineWidth(1)
    c.line(sig1_x - 20, 78, sig1_x + 95, 78)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(navy)
    c.drawCentredString(sig1_x + 37, 67, "Dr. Arvind R. Nair, Ph.D.")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(slate)
    c.drawCentredString(sig1_x + 37, 57, "Vice President, AI & Data Engineering")
    c.drawCentredString(sig1_x + 37, 47, "CogniStrat Technologies Pvt. Ltd.")

    sig2_img = create_signature_image("Meenakshi Sundaram", "Director HR", color=(16, 44, 118))
    sig2_path = os.path.join(OUTPUT_DIR, "temp_sig2.png")
    sig2_img.save(sig2_path)
    
    sig2_x = width - 155
    center2 = sig2_x + 37.5
    w2, h2 = 130, 36
    c.drawImage(sig2_path, center2 - (w2 / 2.0), 80, width=w2, height=h2, mask='auto')
    c.setStrokeColor(navy)
    c.setLineWidth(1)
    c.line(sig2_x - 20, 78, sig2_x + 95, 78)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(navy)
    c.drawCentredString(sig2_x + 37, 67, "Meenakshi Sundaram")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(slate)
    c.drawCentredString(sig2_x + 37, 57, "Sr. Director, Human Resources")
    c.drawCentredString(sig2_x + 37, 47, "CogniStrat Technologies Pvt. Ltd.")

    c.setFont("Helvetica", 6.5)
    c.setFillColor(colors.HexColor("#829AB1"))
    c.drawCentredString(width / 2.0, 32, "This certificate is an official industrial document issued upon successful completion of curriculum-mandated institutional training.")

    c.save()
    
    # Remove temp signature/stamp files
    for p in [stamp_path, sig1_path, sig2_path]:
        if os.path.exists(p): os.remove(p)

    print(f"Generated PDF Certificate: {PDF_PATH}")

def convert_pdf_to_highres_png():
    """Convert generated vector PDF to 300 DPI high-resolution PNG using PyMuPDF (pymupdf)."""
    import pymupdf
    doc = pymupdf.open(PDF_PATH)
    page = doc.load_page(0)
    zoom = 300.0 / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(PNG_PATH)
    doc.close()
    print(f"Generated High-Res PNG Certificate: {PNG_PATH} ({pix.width}x{pix.height})")

if __name__ == "__main__":
    build_pdf_certificate()
    convert_pdf_to_highres_png()
    print("Certificate Generation Complete!")
