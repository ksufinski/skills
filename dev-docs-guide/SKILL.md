---
name: dev-docs-guide
description: |
  Guide for writing and structuring developer documentation using a systematic four-quadrant framework. Use when:
  (1) Creating new technical documentation (tutorials, guides, API references, conceptual docs)
  (2) Reviewing or improving existing documentation structure
  (3) Deciding what type of documentation to write for a given topic
  (4) Organizing documentation architecture for a project
  (5) User asks about documentation best practices or patterns
  Triggers: "write docs", "documentation structure", "how to document", "API docs", "tutorial", "how-to guide", "reference docs", "explain this feature"
---

# Developer Documentation Framework

Based on the [Diátaxis framework](https://diataxis.fr/).

## The Documentation Compass

All documentation maps to four quadrants based on two axes:

|  | **Action** (doing) | **Cognition** (thinking) |
|---|---|---|
| **Acquisition** (learning) | Tutorial | Explanation |
| **Application** (working) | How-to Guide | Reference |

### Quick Decision

Ask two questions:
1. **Doing or thinking?** → Action / Cognition
2. **Learning or working?** → Acquisition / Application

---

## Four Documentation Types

### 1. Tutorial

**Purpose:** Teach through hands-on practice.

**Pattern:**
```markdown
# Build Your First [Thing]

By the end, you'll have [concrete outcome].

## Step 1: [Action]
[instruction]

You'll see:
> [expected output]

## Step 2: [Action]
...
```

**Rules:**
- Show end result upfront
- One path only — no choices
- Visible output at each step
- Minimize explanation — link to Explanation docs
- Test with real beginners

**Anti-patterns:** Teaching concepts, offering alternatives, allowing failure paths.

---

### 2. How-to Guide

**Purpose:** Solve a specific task for competent users.

**Pattern:**
```markdown
# How to [Accomplish Task]

## Prerequisites
- [requirement]

## Steps
1. [action]
2. [action]
```

**Rules:**
- Title = user's task, not tool feature
- Assume competence
- Only necessary steps
- Allow adaptation

**Anti-patterns:** Teaching basics, explaining theory, covering every edge case.

---

### 3. Reference

**Purpose:** Provide accurate lookup information during work.

**Pattern:**
```markdown
## functionName(params)

Description.

### Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|

### Returns
### Errors
### Example
```

**Rules:**
- Neutral, terse style
- Mirror product structure
- Consistent format across entries
- Include usage examples

**Anti-patterns:** Instructions, opinions, tutorials disguised as examples.

---

### 4. Explanation

**Purpose:** Build understanding through context and connections.

**Pattern:**
```markdown
# About [Concept]

## Why [design decision]
## How [concept] relates to [other concept]
## Trade-offs
## Historical context
```

**Rules:**
- Explain "why", not "how to"
- Connect concepts
- Acknowledge alternatives
- Written for reading away from keyboard

**Anti-patterns:** Step-by-step instructions, API details, implementation specifics.

---

## Quick Reference

| Type | User asks | You provide | Tone |
|------|-----------|-------------|------|
| Tutorial | "Teach me" | Guided lesson | Encouraging |
| How-to | "How do I X?" | Recipe | Direct |
| Reference | "What does Y do?" | Facts | Neutral |
| Explanation | "Why?" | Context | Reflective |

## Review Checklist

Before publishing, verify:
- [ ] Single documentation type per document
- [ ] Title matches the type's pattern
- [ ] No type mixing (tutorials with reference, how-to with explanation)
- [ ] Appropriate assumptions about reader knowledge
