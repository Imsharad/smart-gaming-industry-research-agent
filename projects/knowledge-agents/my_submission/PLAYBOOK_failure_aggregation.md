# 📚 Failure Aggregation Playbook

> **Purpose**: Replicable workflow to extract anti-patterns from student feedback and generate visual learning guides.

---

## 🔄 Pipeline Steps

### Step 1: Generate Failures List

```bash
cd /Users/sharad/Projects/udacity-reviews-hq/projects/knowledge-agents
grep -r -l "Status:.*FAIL\|Status:.*NOT MET" tmp/ > my_submission/failures_list.txt
```

### Step 2: Run Aggregation Script

```bash
cd my_submission/
python3 aggregate_failures.py
```

**Outputs**: `visual_antipatterns_guide.md`

---

## 🛠️ Customization

Edit `ANTIPATTERN_CATEGORIES` in `aggregate_failures.py` to add project-specific categories.

---

## 🎓 Use Cases

1. **Student Education**: Generate slides showing common mistakes
2. **Reviewer Training**: Document anti-patterns for consistency
3. **Rubric Improvement**: Identify frequently failed criteria
