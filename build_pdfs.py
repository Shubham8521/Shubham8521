#!/usr/bin/env python3
"""
Build readable PDFs from Hindi (Devanagari) markdown files using Noto fonts.

Why this exists: The previous PDFs rendered Hindi as boxes/jumbled glyphs because
the embedded font did not support the Devanagari script. This script uses
WeasyPrint with locally-bundled Noto Sans + Noto Sans Devanagari fonts so the
output is fully readable and offline-renderable.
"""

from __future__ import annotations

import os
from pathlib import Path

import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

ROOT = Path(__file__).resolve().parent
FONT_DIR = ROOT / "fonts"
PDF_DIR = ROOT / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# Files that should be rendered to PDF.
FILES = [
    "1000_GK_GS_Part1_Ancient_Medieval_History.md",
    "1000_GK_GS_Part2_Modern_India_Freedom_Struggle.md",
    "1000_GK_GS_Part3_Constitution_Polity.md",
    "1000_GK_GS_Part4_Geography.md",
    "1000_GK_GS_Part5_Science_Economy_Misc.md",
    "Bihar_GK_Hot_100_Fact_Sheet_Hindi.md",
    "Bihar_SSC_GS_GK_60_Day_Roadmap.md",
    "Bihar_SSC_GS_GK_60_Din_Roadmap_Hindi.md",
    "Current_Affairs_Capsule_Last_6_Months_Hindi.md",
]

# Use file:// URIs for the embedded fonts so WeasyPrint can resolve them.
DEVA_FONT_URI = (FONT_DIR / "NotoSansDevanagari-Regular.ttf").as_uri()
LATIN_FONT_URI = (FONT_DIR / "NotoSans-Regular.ttf").as_uri()

CSS_TEMPLATE = f"""
@font-face {{
    font-family: 'NotoLatin';
    src: url('{LATIN_FONT_URI}') format('truetype');
    font-weight: 100 900;
    font-style: normal;
}}
@font-face {{
    font-family: 'NotoDeva';
    src: url('{DEVA_FONT_URI}') format('truetype');
    font-weight: 100 900;
    font-style: normal;
}}

@page {{
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
    @bottom-center {{
        content: counter(page) " / " counter(pages);
        font-family: 'NotoLatin', 'NotoDeva', sans-serif;
        font-size: 9pt;
        color: #555;
    }}
}}

html, body {{
    /* Devanagari listed first so Hindi glyphs always pick the right font;
       Latin font covers ASCII fallback (digits, English words). */
    font-family: 'NotoDeva', 'NotoLatin', sans-serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1a1a1a;
}}

h1, h2, h3, h4 {{
    font-family: 'NotoDeva', 'NotoLatin', sans-serif;
    color: #0b3d91;
    page-break-after: avoid;
}}
h1 {{ font-size: 20pt; border-bottom: 2px solid #0b3d91; padding-bottom: 6px; margin-top: 0; }}
h2 {{ font-size: 15pt; margin-top: 18px; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; }}
h3 {{ font-size: 13pt; margin-top: 14px; color: #b8410f; }}
h4 {{ font-size: 11.5pt; margin-top: 10px; }}

p {{ margin: 4px 0 8px 0; }}
strong {{ color: #111; }}

hr {{ border: none; border-top: 1px dashed #94a3b8; margin: 12px 0; }}

ul, ol {{ margin: 4px 0 8px 18px; }}
li {{ margin-bottom: 3px; }}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0 12px 0;
    font-size: 10pt;
}}
th, td {{
    border: 1px solid #94a3b8;
    padding: 5px 7px;
    vertical-align: top;
}}
th {{ background: #e2e8f0; }}

code {{
    font-family: 'NotoLatin', monospace;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 10pt;
}}
pre {{
    background: #f1f5f9;
    padding: 8px;
    border-radius: 4px;
    overflow-x: auto;
}}

blockquote {{
    border-left: 4px solid #0b3d91;
    margin: 8px 0;
    padding: 4px 12px;
    background: #f8fafc;
    color: #334155;
}}

/* Question/answer block readability tweaks. The source uses bold "प्रश्न N." and
   "उत्तर:" / "व्याख्या:" prefixes; nothing special needed beyond strong styling. */
.qa-block {{ page-break-inside: avoid; }}
"""


def md_to_html(md_text: str, title: str) -> str:
    body_html = markdown.markdown(
        md_text,
        extensions=[
            "extra",         # tables, fenced_code, footnotes, etc.
            "sane_lists",
            "toc",
            "nl2br",
        ],
        output_format="html5",
    )
    return f"""<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8" />
<title>{title}</title>
</head>
<body>
{body_html}
</body>
</html>
"""


def build_one(md_path: Path) -> Path:
    out_pdf = PDF_DIR / (md_path.stem + ".pdf")
    md_text = md_path.read_text(encoding="utf-8")
    html_str = md_to_html(md_text, md_path.stem)

    font_config = FontConfiguration()
    css = CSS(string=CSS_TEMPLATE, font_config=font_config)

    HTML(string=html_str, base_url=str(ROOT)).write_pdf(
        str(out_pdf),
        stylesheets=[css],
        font_config=font_config,
        optimize_images=True,
    )
    return out_pdf


def main() -> None:
    for name in FILES:
        src = ROOT / name
        if not src.exists():
            print(f"SKIP missing: {name}")
            continue
        print(f"Building PDF for: {name}")
        out = build_one(src)
        size_kb = out.stat().st_size / 1024
        print(f"  -> {out.relative_to(ROOT)}  ({size_kb:,.1f} KB)")
    print("Done.")


if __name__ == "__main__":
    main()
