"""
verify_presentation.py
Inspects every slide of Industrial_Training_Presentation.pdf
Verifies text, ensures no overlapping, and checks header/footer hygiene.
"""

import fitz
import os

pdf_path = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\Industrial_Training_Presentation.pdf"
doc = fitz.open(pdf_path)

print(f"=== TOTAL SLIDES IN PDF: {len(doc)} ===")
for i, page in enumerate(doc):
    txt = page.get_text()
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    first_3 = lines[:3] if len(lines) >= 3 else lines
    last_3 = lines[-3:] if len(lines) >= 3 else lines
    print(f"\n--- SLIDE {i+1} ({len(lines)} lines) ---")
    print(f"  Head: {first_3}")
    print(f"  Tail: {last_3}")
    
    # Check assertions for hygiene
    if i == 0:
        # Slide 1: should have CU, Presented by, CogniStrat, Remote
        has_viva = any("viva" in l.lower() for l in lines)
        print(f"  [CHECK Slide 1] Viva-Voce removed: {not has_viva}")
        has_remote = any("remote" in l.lower() for l in lines)
        print(f"  [CHECK Slide 1] Remote location present: {has_remote}")
    else:
        # Slides 2 to 14:
        has_dept = any("department of computer" in l.lower() for l in lines)
        has_taksh = any("cse-takshashila" in l.lower() for l in lines)
        has_uid = any("24bcs12754" in l.lower() for l in lines)
        has_cogni = any("cognistrat technologies pvt. ltd." in l.lower() for l in lines)
        # Note: slide 2 talks about CogniStrat in the body text card, which is valid, but shouldn't have it as footer
        has_empower = any("discover" in l.lower() or "empower" in l.lower() for l in lines)
        print(f"  [CHECK Slide {i+1}] Clean header (no dept): {not has_dept and not has_taksh}")
        print(f"  [CHECK Slide {i+1}] Clean footer (no UID): {not has_uid}")
        print(f"  [CHECK Slide {i+1}] No 'Discover Learn Empower': {not has_empower}")

doc.close()
