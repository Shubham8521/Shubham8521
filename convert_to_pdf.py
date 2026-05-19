#!/usr/bin/env python3.9
"""Convert all 5 GK/GS markdown files into a single PDF with proper Hindi text shaping using WeasyPrint."""

import markdown2
from weasyprint import HTML, CSS
import os
import re

# Files in order
files = [
    "1000_GK_GS_Part1_Ancient_Medieval_History.md",
    "1000_GK_GS_Part2_Modern_India_Freedom_Struggle.md",
    "1000_GK_GS_Part3_Constitution_Polity.md",
    "1000_GK_GS_Part4_Geography.md",
    "1000_GK_GS_Part5_Science_Economy_Misc.md",
]

base_dir = "/projects/sandbox/Shubham8521"

# Read and convert all markdown files
print("Reading and converting markdown files...")
all_html_parts = []
for f in files:
    path = os.path.join(base_dir, f)
    with open(path, "r", encoding="utf-8") as fp:
        md_content = fp.read()
    print(f"  - {f}: {len(md_content)} chars")
    html_part = markdown2.markdown(
        md_content,
        extras=["fenced-code-blocks", "tables", "break-on-newline"]
    )
    # Wrap each part in a section for page-break control
    all_html_parts.append(f'<section class="part">{html_part}</section>')

# Combine
combined_html = "\n".join(all_html_parts)

# Title page
title_page_html = """
<section class="title-page">
  <div class="title-content">
    <h1 class="main-title">1000 महत्वपूर्ण GK/GS प्रश्न</h1>
    <h2 class="sub-title">Bihar SSC परीक्षा हेतु</h2>
    <p class="tagline">सम्पूर्ण प्रश्नोत्तर संकलन — व्याख्या सहित</p>
    <div class="parts-list">
      <p>भाग 1: प्राचीन एवं मध्यकालीन भारत का इतिहास (1–200)</p>
      <p>भाग 2: आधुनिक भारत एवं स्वतंत्रता संग्राम (201–400)</p>
      <p>भाग 3: भारतीय संविधान एवं राजव्यवस्था (401–600)</p>
      <p>भाग 4: भूगोल — भारत एवं विश्व (531–750)</p>
      <p>भाग 5: विज्ञान, अर्थव्यवस्था, बिहार-विशेष (601–1000)</p>
    </div>
  </div>
</section>
"""

# Full HTML with proper styling and Hindi font
full_html = f"""<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<title>1000 GK/GS प्रश्न — Bihar SSC</title>
<style>
@page {{
    size: A4;
    margin: 1.8cm 1.5cm 2cm 1.5cm;
    @top-center {{
        content: "1000 GK/GS प्रश्न — Bihar SSC";
        font-family: "Noto Sans Devanagari", "DejaVu Sans", sans-serif;
        font-size: 9pt;
        color: #666;
        padding-bottom: 5pt;
        border-bottom: 0.5pt solid #ccc;
    }}
    @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-family: "DejaVu Sans", sans-serif;
        font-size: 9pt;
        color: #666;
    }}
}}

@page :first {{
    margin: 0;
    @top-center {{ content: ""; }}
    @bottom-center {{ content: ""; }}
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: "Noto Sans Devanagari", "Noto Sans", "DejaVu Sans", sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}}

/* Title page */
.title-page {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
    color: white;
    text-align: center;
    padding: 40pt;
}}

.title-content {{
    width: 100%;
}}

.main-title {{
    font-size: 32pt;
    font-weight: 700;
    margin: 0 0 12pt 0;
    color: white;
    border: none;
}}

.sub-title {{
    font-size: 22pt;
    font-weight: 600;
    margin: 0 0 30pt 0;
    color: #ffd54f;
    border: none;
}}

.tagline {{
    font-size: 14pt;
    margin: 0 0 40pt 0;
    color: #e3f2fd;
}}

.parts-list {{
    font-size: 12pt;
    line-height: 2;
    color: #fff;
    margin-top: 30pt;
    padding-top: 20pt;
    border-top: 1pt solid #5c6bc0;
}}

.parts-list p {{
    margin: 4pt 0;
}}

/* Each part starts on new page */
.part {{
    page-break-before: always;
}}

/* Headings */
h1 {{
    font-size: 18pt;
    color: #1a237e;
    border-bottom: 2pt solid #1a237e;
    padding-bottom: 6pt;
    margin: 0 0 16pt 0;
    page-break-after: avoid;
    page-break-inside: avoid;
}}

h2 {{
    font-size: 14pt;
    color: #283593;
    margin: 18pt 0 10pt 0;
    border-bottom: 1pt solid #c5cae9;
    padding-bottom: 4pt;
    page-break-after: avoid;
}}

h3 {{
    font-size: 12pt;
    color: #3949ab;
    margin: 14pt 0 8pt 0;
    page-break-after: avoid;
}}

p {{
    margin: 5pt 0;
    text-align: justify;
    orphans: 2;
    widows: 2;
}}

/* Question/Answer block - keep together */
p strong:first-child {{
    color: #1b5e20;
}}

/* Style for question lines (start with **प्रश्न) */
p {{
    page-break-inside: avoid;
}}

strong {{
    font-weight: 700;
    color: #1b5e20;
}}

hr {{
    border: none;
    border-top: 1pt solid #bdbdbd;
    margin: 16pt 0;
}}

ul, ol {{
    margin: 6pt 0;
    padding-left: 22pt;
}}

li {{
    margin: 3pt 0;
}}

code {{
    font-family: "DejaVu Sans Mono", monospace;
    background: #f5f5f5;
    padding: 1pt 4pt;
    border-radius: 2pt;
    font-size: 9.5pt;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10pt 0;
}}

th, td {{
    border: 0.5pt solid #999;
    padding: 4pt 6pt;
    text-align: left;
}}

th {{
    background: #e8eaf6;
    font-weight: 700;
}}

/* Color the question and answer text */
p:has(strong:first-child) {{
    margin-top: 8pt;
}}
</style>
</head>
<body>
{title_page_html}
{combined_html}
</body>
</html>
"""

# Save HTML for debugging
html_path = os.path.join(base_dir, "/tmp/combined.html")
os.makedirs(os.path.dirname(html_path), exist_ok=True)
with open(html_path, "w", encoding="utf-8") as fp:
    fp.write(full_html)
print(f"HTML saved to {html_path} ({len(full_html)} chars)")

# Generate PDF
output_path = os.path.join(base_dir, "1000_GK_GS_Questions_Bihar_SSC_Complete.pdf")
print(f"\nGenerating PDF (this may take 30-60 seconds)...")
HTML(string=full_html, base_url=base_dir).write_pdf(output_path)

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"\n✅ PDF created successfully!")
print(f"   Path: {output_path}")
print(f"   Size: {size_mb:.2f} MB")
