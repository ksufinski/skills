#!/usr/bin/env python3
"""
Jupyter Notebook to PDF Converter with Table of Contents

Converts Jupyter notebooks to PDF with:
- Title page
- Auto-generated clickable Table of Contents
- Custom header colors
- MathJax formula rendering

Usage:
    python notebook_to_pdf_toc.py <notebook.ipynb> [options]

Options:
    --output, -o      Output PDF file
    --title, -t       Title for title page
    --subtitle, -s    Subtitle for title page
    --color, -c       Header color (hex, default: #41395f)

Requirements:
    pip install playwright nbconvert beautifulsoup4
    python -m playwright install chromium
"""

import asyncio
import argparse
import os
import re
import sys
import subprocess
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install playwright beautifulsoup4 && python -m playwright install chromium")
    sys.exit(1)


def generate_title_page(title: str, subtitle: str, color: str) -> str:
    """Generate HTML for title page."""
    return f'''
    <div id="title-page" style="
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
        text-align: center;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    ">
        <h1 style="
            color: {color};
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 20px;
            line-height: 1.3;
        ">{title}</h1>
        <h2 style="
            color: {color};
            font-size: 1.8em;
            font-weight: normal;
            margin-top: 0;
        ">{subtitle}</h2>
    </div>
    '''


def extract_headings(soup: BeautifulSoup) -> list:
    """Extract all headings from HTML and add anchor IDs."""
    headings = []
    heading_counter = {}

    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        level = int(tag.name[1])
        text = tag.get_text().strip().replace('¶', '').replace('§', '').strip()

        if not text:
            continue

        base_id = re.sub(r'[^\w\s-]', '', text.lower())
        base_id = re.sub(r'[-\s]+', '-', base_id)

        if base_id in heading_counter:
            heading_counter[base_id] += 1
            anchor_id = f"{base_id}-{heading_counter[base_id]}"
        else:
            heading_counter[base_id] = 0
            anchor_id = base_id

        if not tag.get('id'):
            tag['id'] = anchor_id
        else:
            anchor_id = tag['id']

        headings.append({'level': level, 'text': text, 'id': anchor_id})

    return headings


def generate_toc(headings: list, color: str) -> str:
    """Generate HTML for Table of Contents."""
    toc_html = f'''
    <div id="table-of-contents" style="
        page-break-after: always;
        padding: 40px 20px;
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    ">
        <h1 style="
            text-align: center;
            color: {color};
            margin-bottom: 40px;
            font-size: 2em;
            font-weight: normal;
            border-bottom: 2px solid {color};
            padding-bottom: 15px;
        ">Table of Contents</h1>
        <div style="line-height: 2.0;">
    '''

    for heading in headings:
        level = heading['level']
        indent = (level - 1) * 25

        if level == 1:
            font_size, font_weight = '1.1em', 'bold'
        elif level == 2:
            font_size, font_weight = '1.05em', '600'
        elif level == 3:
            font_size, font_weight = '1em', 'normal'
        else:
            font_size, font_weight = '0.95em', 'normal'

        toc_html += f'''
            <div style="margin-left: {indent}px; margin-bottom: 8px;">
                <a href="#{heading['id']}" style="
                    text-decoration: none;
                    color: {color};
                    font-size: {font_size};
                    font-weight: {font_weight};
                ">{heading['text']}</a>
            </div>
        '''

    toc_html += '</div></div>'
    return toc_html


async def convert_to_pdf_with_toc(
    notebook_path: Path,
    pdf_path: Path,
    title: str,
    subtitle: str,
    color: str
):
    """Convert notebook to PDF with TOC."""
    html_path = notebook_path.with_suffix('.html')
    subprocess.run(
        [sys.executable, '-m', 'nbconvert', '--to', 'html', str(notebook_path)],
        check=True
    )

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    headings = extract_headings(soup)
    print(f"Found {len(headings)} headings")

    title_html = generate_title_page(title, subtitle, color)
    toc_html = generate_toc(headings, color)

    body_tag = soup.find('body')
    if body_tag:
        toc_soup = BeautifulSoup(toc_html, 'html.parser')
        title_soup = BeautifulSoup(title_html, 'html.parser')
        body_tag.insert(0, toc_soup)
        body_tag.insert(0, title_soup)

    html_content = str(soup)

    mathjax_and_styles = f'''
    <script>
    MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true
      }},
      options: {{
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
      }}
    }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        html {{ scroll-behavior: smooth; }}
        @media print {{ #table-of-contents {{ page-break-after: always; }} }}
        .anchor-link {{ display: none !important; }}
        h1, h2, h3, h4 {{ color: {color} !important; }}
    </style>
    '''

    html_content = html_content.replace('</head>', mathjax_and_styles + '\n</head>')

    temp_html = html_path.parent / f"{html_path.stem}_toc.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            file_url = f'file://{temp_html.absolute()}'
            await page.goto(file_url, wait_until='networkidle')

            try:
                await page.wait_for_function("typeof MathJax !== 'undefined'", timeout=15000)
                await page.wait_for_timeout(2000)
                await page.evaluate('''async () => {
                    if (MathJax.typesetPromise) {
                        await MathJax.typesetPromise();
                    }
                }''')
                await page.wait_for_timeout(3000)
            except Exception as e:
                print(f"Warning: MathJax loading issue: {e}")
                await page.wait_for_timeout(5000)

            await page.pdf(
                path=str(pdf_path),
                format='A4',
                margin={'top': '1.5cm', 'right': '1.5cm', 'bottom': '1.5cm', 'left': '1.5cm'},
                print_background=True,
                display_header_footer=False
            )
            await browser.close()
    finally:
        if temp_html.exists():
            temp_html.unlink()
        if html_path.exists():
            html_path.unlink()


def main():
    parser = argparse.ArgumentParser(description='Convert Jupyter notebook to PDF with TOC')
    parser.add_argument('notebook', help='Input notebook file (.ipynb)')
    parser.add_argument('-o', '--output', help='Output PDF file')
    parser.add_argument('-t', '--title', default='Document Title', help='Title for title page')
    parser.add_argument('-s', '--subtitle', default='', help='Subtitle for title page')
    parser.add_argument('-c', '--color', default='#41395f', help='Header color (hex)')
    args = parser.parse_args()

    notebook_path = Path(args.notebook)
    if not notebook_path.exists():
        print(f"Error: {notebook_path} not found")
        sys.exit(1)

    pdf_path = Path(args.output) if args.output else notebook_path.with_suffix('.pdf')

    print(f"Converting {notebook_path} to PDF with TOC...")
    asyncio.run(convert_to_pdf_with_toc(
        notebook_path, pdf_path, args.title, args.subtitle, args.color
    ))

    print(f"\n✓ PDF with TOC created: {pdf_path}")
    print(f"  Size: {pdf_path.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
