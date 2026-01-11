# 📚 Failure Aggregation Playbook

> **Purpose**: Replicable workflow to extract anti-patterns from student feedback and generate visual learning guides.

---

## 🎯 Goal

Transform scattered student feedback files into a consolidated, slide-ready visual guide that documents common mistakes ("anti-patterns") for educational purposes.

---

## 📂 Prerequisites

```
project/
├── tmp/
│   ├── archive/          # Past student submissions
│   │   ├── stu_100/
│   │   │   └── feedback/
│   │   │       ├── 1.md  # Criterion 1 feedback
│   │   │       ├── 2.md
│   │   │       └── ...
│   │   └── stu_N/
│   └── stu_current/      # Current student
└── my_submission/        # Output directory
```

---

## 🔄 Pipeline Steps

### Step 1: Generate Failures List

```bash
cd project/
grep -r -l "Status:.*FAIL\|Status:.*NOT MET" tmp/ > my_submission/failures_list.txt
```

This creates a list of all files containing failure feedback.

---

### Step 2: Run Aggregation Script

```bash
cd my_submission/
python3 aggregate_failures.py
```

**Outputs**:
- `visual_antipatterns_guide.md` - Slide-ready visual guide
- Console: Statistics on files processed

---

### Step 3: Review & Iterate

Open `visual_antipatterns_guide.md` and verify:
- [ ] Executive summary has correct counts
- [ ] Mermaid mindmap renders properly
- [ ] Before/After code examples are accurate
- [ ] Visual metaphors make sense

---

## 🛠️ Script Customization

### Adding New Categories

Edit `ANTIPATTERN_CATEGORIES` in `aggregate_failures.py`:

```python
ANTIPATTERN_CATEGORIES = {
    "your_category": {
        "title": "🏷️ Category Title",
        "icon": "🔴",
        "description": "What this category covers",
        "keywords": ["keyword1", "keyword2"]  # For auto-categorization
    }
}
```

### Adding Fix Suggestions

Add to `generate_fix_suggestion()`:

```python
"your_category": '''```python
# ✅ CORRECT: Example fix
...
```'''
```

### Adding Visual Metaphors

Add to `metaphors` dict in `generate_visual_guide()`:

```python
"your_category": "Like [relatable analogy]..."
```

---

## 📊 Output Structure

```markdown
# 🚫 Agent Anti-Patterns Visual Guide

## 📊 Executive Summary
- Total failures table with impact levels

## 🗺️ Anti-Pattern Landscape
- Mermaid mindmap diagram

## Category Sections
- 📈 Frequency Distribution (bar chart)
- 🃏 Top Anti-Patterns (detailed cards)
  - Impact badge
  - What went wrong
  - Why it fails
  - ❌ Bad code
  - ✅ Correct pattern
  - 💡 Visual metaphor

## 🎨 Slide Generation Hints
- Tips for LLM slide creation
```

---

## 🔁 Replication Checklist

For a new project:

1. [ ] Copy `aggregate_failures.py` to new project's output directory
2. [ ] Update `OUTPUT_FILE` and `FAILURES_LIST` paths in script
3. [ ] Customize `ANTIPATTERN_CATEGORIES` for project-specific issues
4. [ ] Run grep to generate `failures_list.txt`
5. [ ] Run `python3 aggregate_failures.py`
6. [ ] Review and adjust extraction regex if needed

---

## ⚙️ Extraction Strategies (in order)

The script tries multiple patterns to extract failure reasons:

1. **Action Items format**: `1. **Title**: **Issue**: ...`
2. **Critical Requirement NOT Met**: Explicit failure headers
3. **(PARTIAL)/(FAIL) sections**: Section-level status markers
4. **Required Fix sections**: Explicit fix instructions
5. **Assessment + "However"**: Prose with contrasting feedback
6. **Status: FAIL reason**: Generic fallback

If extraction is low, check which format your feedback uses and add a new strategy.

---

## 📈 Metrics

| Metric | This Run |
|--------|----------|
| Files Scanned | 1488 |
| Failures Extracted | 68 |
| Categories Identified | 4 |
| Total Issues | 73 |

---

## 🎓 Use Cases

1. **Student Education**: Generate slides showing common mistakes
2. **Reviewer Training**: Document anti-patterns for consistency
3. **Rubric Improvement**: Identify frequently failed criteria
4. **AI Feedback**: Feed to LLM for generating tailored feedback
