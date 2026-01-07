#!/usr/bin/env python3
"""
Jupyter Notebook to PDF Converter with MathJax Support

Converts Jupyter notebooks to PDF with proper math formula rendering using Playwright.

Usage:
    python notebook_to_pdf.py <notebook.ipynb> [output.pdf]

Requirements:
    pip install playwright nbconvert beautifulsoup4
    python -m playwright install chromium
"""

import asyncio
import argparse
import os
import sys
import subprocess
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)


async def convert_html_to_pdf(html_path: Path, pdf_path: Path):
    """Convert HTML file to PDF with MathJax rendering."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    mathjax_config = '''
    <script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true
      },
      options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    '''

    html_content = html_content.replace('</head>', mathjax_config + '\n</head>')

    temp_html = html_path.parent / f"{html_path.stem}_mathjax.html"
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
                print_background=True
            )
            await browser.close()
    finally:
        if temp_html.exists():
            temp_html.unlink()


def convert_notebook_to_html(notebook_path: Path) -> Path:
    """Convert notebook to HTML using nbconvert."""
    html_path = notebook_path.with_suffix('.html')
    subprocess.run(
        [sys.executable, '-m', 'nbconvert', '--to', 'html', str(notebook_path)],
        check=True
    )
    return html_path


def main():
    parser = argparse.ArgumentParser(description='Convert Jupyter notebook to PDF with MathJax support')
    parser.add_argument('notebook', help='Input notebook file (.ipynb)')
    parser.add_argument('output', nargs='?', help='Output PDF file (default: same name as notebook)')
    args = parser.parse_args()

    notebook_path = Path(args.notebook)
    if not notebook_path.exists():
        print(f"Error: {notebook_path} not found")
        sys.exit(1)

    pdf_path = Path(args.output) if args.output else notebook_path.with_suffix('.pdf')

    print(f"Converting {notebook_path} to PDF...")
    print("Step 1: Converting notebook to HTML...")
    html_path = convert_notebook_to_html(notebook_path)

    print("Step 2: Rendering MathJax and generating PDF...")
    asyncio.run(convert_html_to_pdf(html_path, pdf_path))

    html_path.unlink()

    print(f"\n✓ PDF created: {pdf_path}")
    print(f"  Size: {pdf_path.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
