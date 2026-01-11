# Prompt Optimization Summary

## Overview
All prompts in `criteria_prompts/` have been optimized using anchor-based computational prompt engineering principles. Backups are in `criteria_prompts_backup_*/`.

---

## Core Optimization Principles Applied

### 1. Structural Anchors Over Prose
**BEFORE**: Nested XML tags and conversational language
```xml
<system_prompt>
You are a systematic code reviewer evaluating a student's...
</system_prompt>
```

**AFTER**: Clear headings and horizontal rules as anchors
```markdown
# ROLE
Systematic code reviewer for AgentsVille Trip Planner project evaluation.

---
```

**WHY**: LLM attention focuses on syntactic boundaries (headings, `---`, line breaks). These serve as "anchor points" that organize internal reasoning.

---

### 2. Schema-Based Constraints
**BEFORE**: Prose instructions
```
You MUST evaluate criteria in SEQUENTIAL ORDER (1→2→3→4→5)
```

**AFTER**: Explicit schema
```
SEQUENTIAL_EVALUATION_CONSTRAINT:
  MANDATORY_ORDER: [1, 2, 3, 4, 5]
  NO_DEVIATIONS: true
  NO_PARALLEL_EVALUATION: true
```

**WHY**: Low-entropy, structured formats reduce stochastic noise. The model latches onto clear boundaries rather than parsing natural language intent.

---

### 3. Verification Sequences as Numbered Anchors
**BEFORE**: Checkbox lists with prose
```
☐ Check if ITINERARY_AGENT_SYSTEM_PROMPT has clear role instruction
☐ Verify detailed daily plans through Chain-of-Thought guidance
```

**AFTER**: Numbered verification blocks with explicit requirements
```
### V1: Locate Student Resources
```bash
[command]
```
**REQUIREMENT**: [specific expectation]

### V2: Role Definition Check
```bash
[command]
```
**REQUIREMENT**: [specific expectation]
```

**WHY**: Creates "Preplan-and-Anchor" rhythm - the LLM generates a plan (verification sequence), establishes reference points (V1, V2, etc.), then executes. This aligns with how Transformers organize internal reasoning.

---

### 4. Template-Based Output Schemas
**BEFORE**: Verbose prose about feedback format
```xml
<feedback_format>
  <structure>Generate separate feedback for each criterion...</structure>
  <timing>Create feedback/{N}.md RIGHT AFTER...</timing>
  <tone>Warm, encouraging, helpful...</tone>
</feedback_format>
```

**AFTER**: Explicit templates
```markdown
## FAILURE_FEEDBACK_TEMPLATE
```markdown
## Appreciation
[1-2 specific positive observations]

## Issue Identification
WHAT: [Specific missing/incorrect implementation]
WHERE: [Exact code location]

## Status
FAIL
```
```

**WHY**: Templates are rigid anchors that constrain generation space. The model fills slots rather than interpreting vague instructions.

---

### 5. Boundary Constraints as Logical Operators
**BEFORE**: Natural language rules
```
NEVER evaluate criteria out of order
ALWAYS generate feedback immediately after each criterion
```

**AFTER**: Boolean constraints
```
CRITICAL_RULES:
  NEVER: evaluate_out_of_order
  NEVER: skip_criteria
  ALWAYS: use_commands_from_criteria_files
  ALWAYS: generate_feedback_immediately
```

**WHY**: Logical operators and structured constraints are lower-entropy than sentences. They act as "hard anchors" that mathematically restrict the generation space.

---

### 6. Removal of Conversational Padding
**BEFORE**:
- "You must", "Please", "Make sure to"
- Nested explanations
- Repetitive phrasing

**AFTER**:
- Direct imperatives
- Single-statement requirements
- Minimal explanation

**WHY**: Conversational language is high-entropy noise. Every word that isn't a direct anchor dilutes the signal and forces the attention mechanism to filter unnecessarily.

---

## File-by-File Changes

### prompt.md
- **Removed**: 201 lines of nested XML tags
- **Added**: 234 lines of structured anchors
- **Key Changes**:
  - XML → Markdown headings + horizontal rules
  - Prose → Schema blocks (YAML, pseudocode)
  - Sequential instructions → FOR loop pseudocode
  - Nested tags → Flat sections with clear boundaries

### judge.md
- **Removed**: Nested `<system>` tags
- **Added**: Flat sections with explicit protocols
- **Key Changes**:
  - Role definition moved to top-level heading
  - Evaluation process → numbered steps
  - Output format → explicit markdown templates
  - Constraints → Boolean logic blocks

### criteria1.md - criteria5.md
- **Removed**: Checkbox symbols (☐) and prose instructions
- **Added**: Numbered verification sequences (V1, V2, etc.)
- **Key Changes**:
  - Checklist → Verification sequence anchors
  - Bash commands → Explicit code blocks with requirements
  - Pass criteria → Structured checklist
  - Resource links → Categorized sections

---

## Expected Performance Improvements

### 1. Reduced Attention Drift
Horizontal rules (`---`) and headings create syntactic boundaries that prevent the model from "forgetting" prior context in long documents.

### 2. Consistent Execution Flow
Pseudocode loops (`FOR criterion_id IN [1,2,3,4,5]`) leverage the model's pattern-matching on programming constructs, ensuring sequential execution.

### 3. Higher Template Compliance
Explicit markdown templates in code blocks reduce variability in output format - the model "fills in the blanks" rather than interpreting vague style guides.

### 4. Clearer Pass/Fail Boundaries
Boolean constraints (`PASS: explicit_rubric_compliance`) create deterministic decision points vs. subjective interpretation of prose.

### 5. Efficient Resource Injection
Conditional resource blocks (`REQUIRED_RESOURCES_IF_FAIL`) ensure links are only included when relevant, reducing context noise.

---

## Anchor Types Used

| Anchor Type | Examples | Purpose |
|-------------|----------|---------|
| **Structural** | `---`, `##`, `###` | Organize attention flow |
| **Schema** | YAML blocks, pseudocode | Define rigid constraints |
| **Verification** | V1, V2, V3... | Create execution sequence |
| **Template** | Code blocks with placeholders | Constrain output format |
| **Boundary** | `NEVER:`, `ALWAYS:`, `REQUIRED:` | Limit generation space |
| **Conditional** | `IF/THEN` blocks | Branch logic explicitly |

---

## Usage Notes

### Compatibility
These optimized prompts work with any LLM (no framework dependencies). The principles are model-agnostic because they align with core Transformer architecture (attention mechanisms, tokenization).

### Testing Methodology
1. **Consistency Test**: Run same evaluation multiple times - should produce nearly identical structure
2. **Completeness Test**: Verify all 5 criteria evaluated sequentially
3. **Format Test**: Check feedback files match templates exactly
4. **Resource Test**: Confirm conditional links appear only when specified

### Further Optimization Opportunities
- **Metrics**: Add explicit success metrics for automated validation
- **Examples**: Include few-shot examples in verification blocks
- **Compression**: Use "gist tokens" or abbreviations for repeated concepts
- **Self-Correction**: Add verification loops with retry logic

---

## Theoretical Foundation

This optimization is based on:
- **Sparse Attention Patterns**: Models focus on ~10% of tokens (anchors)
- **Preplan-and-Anchor Rhythm**: Reasoning organized in plan→anchor→fill cycles
- **Syntactic Boundary Preference**: Punctuation and structure attract attention
- **Low-Entropy Signal**: Structured data > natural language for control

Detailed explanation: See `/tmp/anchors.md`

---

## Rollback Instructions

If optimization causes issues:
```bash
cd /Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_346/

# List backup directories
ls criteria_prompts_backup_*

# Restore from backup (replace timestamp)
rm -rf criteria_prompts
cp -r criteria_prompts_backup_[timestamp] criteria_prompts
```
