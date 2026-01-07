---
name: notebook-to-pdf
description: "Convert Jupyter notebooks (.ipynb) to PDF with proper MathJax formula rendering. Use when: (1) User wants to export a notebook to PDF, (2) PDF needs proper math/LaTeX formula display, (3) User needs a Table of Contents, title page, or clickable navigation, (4) User mentions 'convert notebook', 'export to PDF', or 'notebook PDF'."
---

# Notebook to PDF

Convert Jupyter notebooks to professional PDFs with proper MathJax formula rendering using Playwright + Chromium.

## IMPORTANT: Default Behavior

**By default, ALWAYS use the ToC version (`notebook_to_pdf_toc.py`)** which includes:
- Title page with customizable title and subtitle
- Auto-generated clickable Table of Contents
- Professional formatting

**Before running the conversion, you MUST ask the user:**
1. What title should appear on the title page?
2. What subtitle should appear on the title page? (can be empty)

Use the AskUserQuestion tool to gather this information before proceeding.

## Quick Start

### Default Conversion (with ToC) - PREFERRED
```bash
python scripts/notebook_to_pdf_toc.py notebook.ipynb \
  --title "User's Title" \
  --subtitle "User's Subtitle" \
  --color "#41395f"
```

### Basic Conversion (without ToC) - Only if explicitly requested
```bash
python scripts/notebook_to_pdf.py notebook.ipynb
```

## Requirements

Install dependencies before first use:
```bash
pip install nbconvert playwright beautifulsoup4
python -m playwright install chromium
```

## Two Conversion Modes

### 1. Basic PDF (`notebook_to_pdf.py`)

Simple conversion with MathJax rendering.

```bash
python scripts/notebook_to_pdf.py input.ipynb output.pdf
```

**Features:**
- Proper math formula rendering
- Code, outputs, and visualizations preserved
- Clean A4 layout with 1.5cm margins

### 2. PDF with TOC (`notebook_to_pdf_toc.py`)

Professional output with title page and navigation.

```bash
python scripts/notebook_to_pdf_toc.py input.ipynb \
  -o output.pdf \
  -t "Document Title" \
  -s "Subtitle" \
  -c "#41395f"
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output PDF path | `<notebook>.pdf` |
| `-t, --title` | Title page heading | "Document Title" |
| `-s, --subtitle` | Title page subtitle | (empty) |
| `-c, --color` | Header color (hex) | `#41395f` |

**Features:**
- Centered title page with page break
- Auto-generated clickable Table of Contents
- Hierarchical heading structure (H1-H4)
- Custom header colors throughout
- All headings linked from TOC

## How It Works

1. **nbconvert**: Converts `.ipynb` → `.html`
2. **MathJax injection**: Adds MathJax 3 for formula rendering
3. **BeautifulSoup**: Parses HTML, extracts headings, generates TOC
4. **Playwright + Chromium**: Renders MathJax, prints to PDF

## Troubleshooting

**MathJax not rendering**: Check internet connection (CDN required)

**PDF looks broken**: Reinstall Chromium: `python -m playwright install chromium`

**Missing headings in TOC**: Use proper markdown syntax (`#`, `##`, `###`) in notebook cells
