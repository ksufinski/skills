---
name: claspo-brand-guidelines
description: Apply Claspo's official brand identity system for consistent visual styling to artifacts. Use when creating UI components, HTML pages, presentations, or any visual content that should follow Claspo branding. Triggers include requests for Claspo-styled elements, brand-consistent designs, or any mention of Claspo visual identity.
---

# Claspo Brand Styling Guide

Apply Claspo's official brand identity system for consistent visual styling across all artifacts.

## Core Brand Elements

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--claspo-accent` | `#F3492C` | Primary accent, buttons, links, highlights |
| `--claspo-accent-hover` | `#D93D22` | Hover states for accent elements |
| `--claspo-accent-light` | `rgba(243, 73, 44, 0.1)` | Light backgrounds, focus rings |
| `--claspo-neutral-dark` | `#3D3D3D` | Primary text, headings |
| `--claspo-neutral` | `#5F5F5F` | Secondary text, body content |
| `--claspo-neutral-light` | `#8A8A8A` | Muted text, placeholders |
| `--claspo-white` | `#FFFFFF` | Backgrounds, card surfaces |
| `--claspo-bg` | `#F5F5F5` | Page background |
| `--claspo-border` | `#E0E0E0` | Borders, dividers |

### Typography

- **Font Family**: Montserrat (with system font fallback)
- **Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- **Line Height**: 1.6 for body text

```css
font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

**Heading Sizes**:
- H1: 48px, weight 700
- H2: 36px, weight 600
- H3: 24px, weight 600
- H4: 20px, weight 500

### Icon System

Icon sizes for different UI contexts:
- **16px**: Compact/dense UI
- **20px**: Standard inline usage
- **24px**: Default action icons
- **27px**: Service/browser icons
- **32px**: Featured/prominent placement

## Component Patterns

### Buttons

```css
.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-primary {
  background: #F3492C;
  color: #FFFFFF;
}

.btn-outline {
  background: transparent;
  border: 2px solid #F3492C;
  color: #F3492C;
}
```

**Size Variants**:
- Small: `padding: 8px 16px; font-size: 12px;`
- Default: `padding: 12px 24px; font-size: 14px;`
- Large: `padding: 16px 32px; font-size: 16px;`

### Form Inputs

```css
.form-input {
  padding: 12px 16px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
}

.form-input:focus {
  border-color: #F3492C;
  box-shadow: 0 0 0 3px rgba(243, 73, 44, 0.1);
}
```

### Cards

```css
.card {
  background: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
```

### Badges

```css
.badge {
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}

.badge-primary { background: #F3492C; color: #FFFFFF; }
.badge-light { background: rgba(243, 73, 44, 0.1); color: #F3492C; }
```

## Implementation

### CSS Custom Properties Setup

```css
:root {
  --claspo-accent: #F3492C;
  --claspo-accent-hover: #D93D22;
  --claspo-accent-light: rgba(243, 73, 44, 0.1);
  --claspo-neutral: #5F5F5F;
  --claspo-neutral-light: #8A8A8A;
  --claspo-neutral-dark: #3D3D3D;
  --claspo-white: #FFFFFF;
  --claspo-bg: #F5F5F5;
  --claspo-border: #E0E0E0;
}
```

### Google Fonts Import

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## Demo Page

A complete demo page showing all styled components is available at `assets/claspo-brand-sample.html`. Copy this file as a starting point for new Claspo-branded pages.
