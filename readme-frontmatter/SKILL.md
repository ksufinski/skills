---
name: readme-frontmatter
description: |
  Generate and validate YAML frontmatter for ReadMe.io documentation pages.
  Use when: (1) Creating new .md files for ReadMe.io docs, (2) Adding/editing frontmatter metadata,
  (3) Setting SEO properties for documentation pages, (4) Configuring page visibility (hidden/deprecated),
  (5) User mentions "ReadMe", "frontmatter", "docs.readme.com", or asks about documentation metadata.
---

# ReadMe.io Frontmatter

Generate YAML frontmatter for ReadMe.io documentation. Place between `---` at file start.

## Required Fields

```yaml
---
title: Page Title
excerpt: Short description under title
---
```

## All Fields Reference

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Page title (required) |
| `excerpt` | string | Description under title |
| `deprecated` | boolean | Mark as deprecated |
| `hidden` | boolean | Hide from navigation |
| `icon` | string | Font Awesome class (e.g., `fad fa-code`) |
| `category` | string | Category organization |

### SEO (`metadata`)

```yaml
metadata:
  title: SEO Title
  description: SEO description
  keywords:
    - keyword1
    - keyword2
  robots: index  # or noindex
  image: https://example.com/og-image.png
```

### Link Pages (`link`)

```yaml
link:
  url: https://external-site.com
  new_tab: true
```

### API Reference (`api`)

```yaml
api:
  file: openapi.json
  operationId: getUser
  webhook: false
```

### Recipes (`recipe`)

```yaml
recipe:
  color: "#4CAF50"
  icon: rocket
```

## Common Patterns

**Standard page:**
```yaml
---
title: Getting Started
excerpt: Learn how to integrate the editor
deprecated: false
hidden: false
metadata:
  robots: index
---
```

**Full SEO:**
```yaml
---
title: API Reference
excerpt: Complete API documentation
metadata:
  title: API Reference | Developer Docs
  description: Comprehensive API reference with examples
  keywords: [api, integration, reference]
  robots: index
  image: https://example.com/api-preview.png
---
```

**Draft/hidden:**
```yaml
---
title: Work in Progress
hidden: true
---
```

**Deprecated:**
```yaml
---
title: Legacy Config
deprecated: true
metadata:
  robots: noindex
---
```

## Project Structure

```
docs/
├── category-folder/
│   ├── _order.yaml    # Page ordering
│   └── page.md
└── reference/
```

`_order.yaml` defines page order:
```yaml
- getting-started
- configuration
- api-reference
```
