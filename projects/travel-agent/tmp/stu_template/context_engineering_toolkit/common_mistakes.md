# Common Student Implementation Mistakes - Travel Agent Project

## Purpose
This catalog documents frequently occurring mistakes in student submissions for the AgentsVille Trip Planner project. Use this as a checklist during evaluation to catch issues before marking PASS.

**Data Sources**: stu_135 (PASS), stu_138 (FAIL on C2), stu_139 (FAIL on C2), stu_141 (FAIL on C4 & C5)

---

## CRITERION 2: Weather Compatibility - Common Mistakes

### Mistake 2.1: Only ONE Example Type (Missing IS_COMPATIBLE or IS_INCOMPATIBLE)
**Frequency**: VERY HIGH 
**Severity**: CRITICAL - Causes FAIL
**Observed**: stu_138, stu_139

**Rubric Requires**:
> "the examples show at least one example of IS_COMPATIBLE and one of IS_INCOMPATIBLE"

**What to Search For**:
```bash
# Must find BOTH types
grep -c "IS_COMPATIBLE" *.ipynb  # Must be >= 1
grep -c "IS_INCOMPATIBLE" *.ipynb # Must be >= 1
```

**Common Patterns**:
 **Only IS_INCOMPATIBLE example** (outdoor activity + rain/storm)
 **Only IS_COMPATIBLE example** (indoor activity + any weather)
 **No examples at all**

**Why This is Critical**:
This is NOT an "enhancement" - it's a **mandatory rubric requirement**. Students MUST demonstrate understanding of BOTH decision outcomes.

**Evidence from stu_138 & stu_139**:
```python
## Examples
Activity: Sunset Groove Hike
...
REASONING: The activity is outdoor. Since no indoor backup plan is mentioned,
a thunderstorm makes this activity incompatible.
FINAL ANSWER: [IS_INCOMPATIBLE]

# MISSING: IS_COMPATIBLE example
```

**Required Fix**:
Add BOTH example types:

```python
Example 1 (IS_COMPATIBLE):
Activity: Museum of Modern Innovation Tour
Description: Indoor climate-controlled facility...
Weather Condition: thunderstorm
REASONING: Indoor activities are not affected by outdoor weather.
FINAL ANSWER: [IS_COMPATIBLE]

Example 2 (IS_INCOMPATIBLE):
Activity: Outdoor Hiking Trail
Description: Mountain trail with no shelter...
Weather Condition: thunderstorm
REASONING: Outdoor activity with no backup plan during severe weather.
FINAL ANSWER: [IS_INCOMPATIBLE]
```

**How to Verify**:
```bash
# Quick check - both should return TRUE
grep -q "IS_COMPATIBLE" *.ipynb && echo " Has COMPATIBLE" || echo " Missing COMPATIBLE"
grep -q "IS_INCOMPATIBLE" *.ipynb && echo " Has INCOMPATIBLE" || echo " Missing INCOMPATIBLE"
```

---

### Mistake 2.2: Not Mentioning Backup Options
**Frequency**: MEDIUM
**Severity**: MODERATE - Reviewer tip requirement

**What to Search For**:
```bash
grep -i "backup\|alternative\|contingency\|indoor.*option" *.ipynb
```

**Why This Matters**:
- Reviewer tip explicitly checks for backup option consideration
- Real-world events often have backup plans for bad weather
- Shows sophisticated reasoning about edge cases

**Good Example from stu_135**:
```python
"If the activity is described as being **indoor**, **covered**, or has a
**backup indoor plan**, mark it as `IS_COMPATIBLE`, even in poor weather."
```

---

## CRITERION 4: ReAct Agent System Prompt - Common Mistakes

### Mistake 4.1: Incomplete Tool Listing in Available Tools Section
**Frequency**: HIGH
**Severity**: CRITICAL - Causes FAIL
**Observed**: stu_141

**What to Check**:
```bash
# Count tools defined in code
grep "ALL_TOOLS = \[" *.ipynb -A 10

# Count tools listed in ITINERARY_REVISION_AGENT_SYSTEM_PROMPT
grep -A 20 "Available Tools" *.ipynb | grep "tool.*→\|tool(.*)"
```

**Common Pattern**:
- Student defines 4 tools in ALL_TOOLS: calculator_tool, get_activities_by_date_tool, run_evals_tool, final_answer_tool
- But only lists 3 in the Available Tools section of the prompt
- **Most frequently missing**: run_evals_tool or calculator_tool

**Why Students Miss This**:
- They list tools they think are "important" rather than ALL tools
- They copy incomplete examples from instructions
- They focus on tools they actively use, forgetting auxiliary tools

**Evidence Pattern in stu_141**:
```
Available Tools section listed:
- get_activities_by_date_tool
- eval_activities_and_weather_are_compatible
- final_answer_tool

Missing: run_evals_tool (even though defined in ALL_TOOLS)
```

**How to Verify**:
1. Count tools in ALL_TOOLS list
2. Count tools in prompt's Available Tools section
3. If counts don't match → FAIL
4. Verify each tool has signature documentation

---

### Mistake 4.2: Vague Language for run_evals_tool Requirement
**Frequency**: HIGH
**Severity**: CRITICAL - Causes FAIL
**Observed**: stu_141

**Rubric Requires**:
> "States that the run_evals_tool must be run before the final_answer_tool"

**What to Search For**:
```bash
# Must find explicit statement with function name
grep -i "run_evals_tool.*before.*final_answer_tool" *.ipynb
grep -i "must.*run_evals_tool" *.ipynb
```

**Common Incorrect Phrasings**:
 "always re-run the evaluation tools"
 "run evaluations before finalizing"
 "make sure to evaluate the plan"
 "validate before submitting"

**Correct Phrasings**:
 "You MUST call run_evals_tool before calling final_answer_tool"
 "Before calling final_answer_tool, you must call run_evals_tool"
 "Call run_evals_tool first, then final_answer_tool only if evaluations pass"

**Why Students Miss This**:
- They describe the concept generically rather than using exact function names
- They assume "evaluation" is understood without being specific
- They focus on the workflow rather than the specific tool sequence

**Evidence Pattern in stu_141**:
```
Student wrote: "always re-run the evaluation tools"
Required: "run_evals_tool must be run before final_answer_tool"
Issue: Generic "evaluation tools" vs. specific "run_evals_tool"
```

**Good Example from stu_135**:
```
"4. Run the evaluation tools again to ensure the revised plan passes all checks."
"5. Once satisfied, return the final revised plan using the `final_answer_tool`."
```
Clear sequencing: step 4 (run_evals_tool) before step 5 (final_answer_tool)

**Red Flags**:
- Generic terms: "evaluation tools," "checks," "validations"
- Missing function names: run_evals_tool, final_answer_tool
- No explicit ordering: "before," "then," "after"

---

### Mistake 4.3: Wrong Tool Listed (eval_activities_and_weather_are_compatible vs run_evals_tool)
**Frequency**: MEDIUM
**Severity**: MODERATE - May cause confusion
**Observed**: stu_141

**What Happens**:
Students list `eval_activities_and_weather_are_compatible` in Available Tools but this is:
- A helper function, not a tool in ALL_TOOLS
- Called by run_evals_tool internally
- Not meant to be called directly by the ReAct agent

**How to Verify**:
```python
# Check ALL_TOOLS definition
ALL_TOOLS = [
  calculator_tool,
  get_activities_by_date_tool,
  run_evals_tool,    # This should be in prompt
  final_answer_tool,
]

# eval_activities_and_weather_are_compatible is NOT in ALL_TOOLS
```

**Why This Happens**:
- Students see the function used in evaluation code
- They confuse internal helper functions with agent-callable tools
- They want to give the agent more granular control

**Evidence Pattern in stu_141**:
Listed in prompt:
- eval_activities_and_weather_are_compatible (not in ALL_TOOLS)

Should have listed:
- run_evals_tool (in ALL_TOOLS)

---

## CRITERION 5: Pydantic Models - Common Mistakes

### Mistake 5.1: Missing TravelPlan Schema in System Prompts
**Frequency**: VERY HIGH
**Severity**: CRITICAL - Causes FAIL
**Observed**: stu_141

**Rubric Requires**:
> "The TravelPlan Pydantic model's schema is included in AT LEAST ONE system prompt"

**What to Search For**:
```bash
# Must find schema method call in prompt
grep "TravelPlan.model_json_schema()" *.ipynb
grep "TravelPlan.schema()" *.ipynb
grep "model_json_schema" *.ipynb
```

**Common Incorrect Approaches**:
 Manually typing JSON structure in prompt
 Showing example JSON output
 Describing the schema in words
 Only having schema in code (not in prompt)

**Correct Approach**:
 Including `{json.dumps(TravelPlan.model_json_schema(), indent=2)}` in prompt
 Or `{TravelPlan.model_json_schema()}` embedded via f-string

**Why Students Miss This**:
- They confuse "showing JSON structure" with "including schema"
- They manually type JSON examples and think that's sufficient
- They don't realize rubric requires **Pydantic-generated schema**, not hand-written JSON

**Evidence Pattern in stu_141**:
```python
# Student had this (WRONG):
FINAL OUTPUT:
  ```json
  {
   "city": "<string>",
   "start_date": "<YYYY-MM-DD>",
   ...
  }
  ```

# Should have this (CORRECT):
## TravelPlan Schema
{json.dumps(TravelPlan.model_json_schema(), indent=2)}
```

**Good Example from stu_135 & stu_138**:
```python
schema_str = json.dumps(TravelPlan.model_json_schema(), indent=2)

ITINERARY_AGENT_SYSTEM_PROMPT = f"""
...
FINAL OUTPUT:
{schema_str}
...
"""
```

**Key Distinction**:
- **Manual JSON**: Human-written structure example
- **Pydantic Schema**: Output of `.model_json_schema()` method

The rubric specifically requires the **Pydantic schema**, not a manual example.

---

### Mistake 5.2: Schema in Only One of Two Prompts
**Frequency**: MEDIUM
**Severity**: MINOR - Technically passes but not ideal

**What Happens**:
There are TWO prompts that output TravelPlan:
1. ITINERARY_AGENT_SYSTEM_PROMPT
2. ITINERARY_REVISION_AGENT_SYSTEM_PROMPT

**Rubric Requirement**: "AT LEAST ONE" must include schema

**Common Pattern**:
- Students add schema to one prompt but not the other
- This technically passes but creates inconsistency

**Best Practice**:
- Include schema in BOTH prompts for consistency
- If choosing only one, prioritize ITINERARY_AGENT_SYSTEM_PROMPT (generates initial plan)

---

## CRITERION 1: Itinerary Agent - Common Mistakes

### Mistake 1.1: Missing Chain-of-Thought Guidance
**Frequency**: LOW
**Severity**: CRITICAL - Causes FAIL if missing

**What to Search For**:
```bash
grep -i "step.*by.*step\|for each day\|ANALYSIS\|reasoning" *.ipynb
```

**Common Missing Elements**:
- No explicit "step-by-step" language
- No ANALYSIS or REASONING section in output format
- No "for each day" iteration guidance
- No examples showing reasoning process

**Good Example from stu_135**:
```python
## Task
Your task is to generate a comprehensive, day-by-day travel itinerary using
Chain-of-Thought (CoT) reasoning.

8-step systematic process:
- Step 1: Parse inputs from VacationInfo
- Step 2: Extract dates & city
- Step 3: Weather-aware activity selection
...
```

**Why Students Miss This**:
- They focus on output format and forget reasoning process
- They assume LLM will reason automatically without prompting

---

## CRITERION 3: Tool Description - Common Mistakes

### Mistake 3.1: Missing Date Format Specification
**Frequency**: MEDIUM
**Severity**: MODERATE - May cause runtime errors

**What to Search For**:
```bash
grep -A 10 "def get_activities_by_date_tool" *.ipynb | grep -i "YYYY-MM-DD\|%Y-%m-%d"
```

**Common Missing Elements**:
- Date parameter documented but format not specified
- Format shown in example but not in Args section
- Inconsistent format documentation

**Good Example from stu_135**:
```python
Args:
  date (str): The date of interest in YYYY-MM-DD format.
  city (str): The name of the city to look up activities in.
```

**Why This Matters**:
- LLM may generate wrong date format (MM-DD-YYYY, DD/MM/YYYY, etc.)
- Causes tool call failures
- Explicit format specification prevents errors

---

## VERIFICATION CHECKLIST FOR REVIEWERS

### Priority #1: Criterion 2 - Examples (MOST COMMON FAILURE)
- [ ] Search for: `grep -c "IS_COMPATIBLE" *.ipynb` (>= 1)
- [ ] Search for: `grep -c "IS_INCOMPATIBLE" *.ipynb` (>= 1)
- [ ] **If BOTH not found → IMMEDIATE FAIL**
- [ ] Search for: `grep -i "backup" *.ipynb`

### Priority #2: Criterion 4 - Tool Listing
- [ ] Count tools in ALL_TOOLS: `grep "ALL_TOOLS = \[" -A 5`
- [ ] Count tools in prompt Available Tools section
- [ ] Verify counts match (usually 4 tools)
- [ ] Search for: `grep "run_evals_tool.*before.*final_answer_tool"`
- [ ] Verify exact function names used (not generic terms)

### Priority #3: Criterion 5 - Schema Inclusion
- [ ] Search for: `grep "model_json_schema()" *.ipynb`
- [ ] Verify schema is IN THE PROMPT (not just in code)
- [ ] Distinguish manual JSON from Pydantic schema
- [ ] Check at least ONE of the two system prompts has it

### Criterion 3 - Tool Description
- [ ] Search for: `grep -A 15 "def get_activities_by_date_tool" *.ipynb`
- [ ] Verify date format specified (YYYY-MM-DD or equivalent)
- [ ] Check both parameters documented: date (str), city (str)

### Criterion 1 - Chain-of-Thought
- [ ] Search for: `grep -i "step.*by.*step\|ANALYSIS\|reasoning" *.ipynb`
- [ ] Verify explicit CoT guidance in prompt

---

## SEARCH PATTERNS FOR QUICK VERIFICATION

### Quick Fail Detection Commands:

```bash
# Criterion 2 - MOST COMMON FAILURE - Check FIRST
echo "=== CRITERION 2 CHECK ==="
grep -q "IS_COMPATIBLE" *.ipynb && echo " Has COMPATIBLE" || echo " FAIL: Missing COMPATIBLE"
grep -q "IS_INCOMPATIBLE" *.ipynb && echo " Has INCOMPATIBLE" || echo " FAIL: Missing INCOMPATIBLE"

# Criterion 4 - Check tool count mismatch
echo "=== CRITERION 4 CHECK ==="
echo "Tools in ALL_TOOLS:"; grep "ALL_TOOLS = \[" -A 10 *.ipynb | grep "_tool" | wc -l
echo "Tools in prompt:"; grep -A 30 "Available Tools" *.ipynb | grep "tool.*→" | wc -l

# Criterion 4 - Check for explicit requirement
grep -q "run_evals_tool.*before.*final_answer_tool" *.ipynb && echo " PASS" || echo " FAIL: Vague language"

# Criterion 5 - Check for schema inclusion
echo "=== CRITERION 5 CHECK ==="
grep -q "model_json_schema()" *.ipynb && echo " Potentially PASS" || echo " FAIL: No schema"
```

---

## PATTERNS THAT INDICATE LIKELY FAILURES

### Red Flag Phrases:
- "evaluation tools" (instead of "run_evals_tool")
- "run checks" (instead of "run_evals_tool")
- "validate" (instead of "run_evals_tool")
- Manual JSON examples (instead of model_json_schema())

### Red Flag Patterns:
- Tool count in prompt < Tool count in ALL_TOOLS
- No "before" or "after" language for tool sequencing
- No grep match for "model_json_schema"
- **Only one type of example (IS_COMPATIBLE or IS_INCOMPATIBLE, not both)** ← MOST COMMON

---

## MOST COMMON FAILURE PATTERNS

### Pattern A: Missing IS_COMPATIBLE Example
**Frequency**: VERY HIGH
**Impact**: Immediate FAIL on Criterion 2
**Fix Time**: 2 minutes

Check: `grep -c "IS_COMPATIBLE" *.ipynb` returns 0 or only shows non-example usage

### Pattern B: Missing Tools + Vague Language
**Frequency**: HIGH
**Impact**: Immediate FAIL on Criterion 4
**Fix Time**: 5 minutes

Combo of:
1. run_evals_tool not in Available Tools
2. "evaluation tools" instead of "run_evals_tool"

### Pattern C: No Schema Inclusion (stu_141)
**Frequency**: HIGH
**Impact**: Immediate FAIL on Criterion 5
**Fix Time**: 2 minutes

Check: `grep "model_json_schema()" *.ipynb` returns no matches in prompt context



## RECOMMENDED REVIEW ORDER

1. **Check Criterion 2 FIRST** (highest failure rate)
  - Quick grep: `grep -c "IS_COMPATIBLE" *.ipynb` AND `grep -c "IS_INCOMPATIBLE" *.ipynb`
  - Both must be >= 1

2. **Check Criterion 5 SECOND** (schema)
  - Quick grep: `grep "model_json_schema()" *.ipynb`
  - Must appear in at least one system prompt

3. **Check Criterion 4 THIRD** (tools)
  - Count ALL_TOOLS vs Available Tools
  - Search for explicit "run_evals_tool...before...final_answer_tool"

4. **Check Criteria 1 & 3** (usually pass)
  - Chain-of-Thought guidance
  - Date format specification

This order maximizes early failure detection and saves review time.
