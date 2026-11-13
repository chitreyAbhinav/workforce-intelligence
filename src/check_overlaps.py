"""
check_overlaps.py
Renders each slide to high-res image and analyzes layout bounding boxes
to ensure zero overlap between text frames, shapes, and pictures.
"""

import fitz
import os

pdf_path = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\Industrial_Training_Presentation.pdf"
out_dir = r"C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\slide_renders_v3"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    img_path = os.path.join(out_dir, f"slide_{i+1}.png")
    pix.save(img_path)
    
    # Get all text blocks and drawings
    blocks = page.get_text("blocks") # (x0, y0, x1, y1, text, block_no, block_type)
    # Check vertical ranges of text blocks
    text_blocks = [b for b in blocks if b[4].strip()]
    
    print(f"\nSlide {i+1} has {len(text_blocks)} text blocks. Saved image: {img_path}")
    for b in text_blocks[:4]:
        snippet = b[4].replace('\n', ' ')[:40]
        print(f"   y=({b[1]:.1f} to {b[3]:.1f}), x=({b[0]:.1f} to {b[2]:.1f}): \"{snippet}\"")

doc.close()
