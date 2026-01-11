# Master Failed Context: Agent Anti-Patterns

This document aggregates validated failure traces from student submissions to prevent common agentic design mistakes.

## Criterion 1 Failures

### Unstructured Failure Feedback
**Frequency**: 251 students (stu_333, stu_139, stu_106, stu_302, stu_130, ... (+246 more))

**Why it fails**: See details in full text.

---
### Assessment Feedback
**Frequency**: 21 students (stu_106, stu_163, stu_164, stu_73, stu_89, ... (+16 more))

**Why it fails**: **Role Definition:** Your prompt establishes the agent as "the best itinerary planning agent," which provides clear identity.

**Task Specification:** You've included explicit constraints (avoid outdoor-only activities, handle rain appropriately, stay within budget, ensure 1+ activity per day).

**Chain-of-Thought Guidance:** Your ANALYSIS section requests reasoning steps and data interpretation, though it lacks explicit step-by-step instructions for daily planning that would strengthen the CoT approach.

**Output Format:** The JSON schema is properly structured with clear ANALYSIS and FINAL OUTPUT sections.

**Critical Gap:** The Context section contains placeholder text ("retrieved weather data (json)" and "retrieved activities data (json)") instead of actual data, which causes the agent to hallucinate activity IDs (A1001-A1004 don't exist in the real dataset).

---
## Criterion 2 Failures

### Unstructured Failure Feedback
**Frequency**: 258 students (stu_333, stu_139, stu_106, stu_302, stu_130, ... (+253 more))

**Why it fails**: See details in full text.

---
### Assessment Feedback
**Frequency**: 24 students (stu_139, stu_163, stu_164, stu_131, stu_138, ... (+19 more))

**Why it fails**: Based on the rubric requirements, I evaluated your ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT against the following criteria:

#

---
### The rubric and examples require the output format to use `IS_COMPATIBLE` and `IS_INCOMPATIBLE`. Your prompt uses `COMPATIBLE` and `INCOMPATIBLE`.
**Frequency**: 1 students (stu_333)

**Details**:
**Fix Output Format Mismatch**:
    *   **Issue**: The rubric and examples require the output format to use `IS_COMPATIBLE` and `IS_INCOMPATIBLE`. Your prompt uses `COMPATIBLE` and `INCOMPATIBLE`.
    *   **Why it matters**: In modular AI systems, downstream components (like parsers) often rely on strict string matching. Deviating from the agreed-upon contract breaks the system.
    *   **Fix**: Update your `OUTPUT FORMAT` and `EXAMPLES` sections to use `IS_COMPATIBLE` and `IS_INCOMPATIBLE`.

---
### Your parsing logic contains a severe bug:
**Frequency**: 1 students (stu_333)

**Why it fails**: The string `"INCOMPATIBLE"` (or `"IS_INCOMPATIBLE"`) *contains* the substring `"COMPAT"`. Therefore, your code matches the first `if` statement and returns `True` (Compatible) even when the model says it is incompatible!

**Bad Code Pattern**:
```python
        if "COMPAT" in normalized_resp:
            is_compatible = True
        elif "INCOMPAT" in normalized_resp:
            is_compatible = False
        ```

---
### While you check if an activity moves indoors, the prompt doesn't explicitly mention *considering* backup options or alternatives in a broader sense as per the rubric tip.
**Frequency**: 1 students (stu_333)

**Details**:
**Explicit Backup Options**:
    *   **Issue**: While you check if an activity moves indoors, the prompt doesn't explicitly mention *considering* backup options or alternatives in a broader sense as per the rubric tip.
    *   **Fix**: Add a line to the role or task description like: "Consider if the activity provides a backup option (like moving indoors) before ruling it out."

---
## Criterion 3 Failures

### Unstructured Failure Feedback
**Frequency**: 256 students (stu_333, stu_139, stu_106, stu_302, stu_130, ... (+251 more))

**Why it fails**: See details in full text.

---
### Assessment Feedback
**Frequency**: 22 students (stu_101, stu_139, stu_163, stu_164, stu_165, ... (+17 more))

**Why it fails**: Your tool description effectively guides LLM usage with clear purpose definition and proper parameter documentation. The function signature correctly specifies `date: str` and `city: str` types, and your docstring includes detailed Args documentation. The ReAct agent successfully calls this tool with proper JSON formatting: `{"tool_name": "get_activities_by_date_tool", "arguments": {"date": "2025-06-12", "city": "AgentsVille"}}`.

However, your docstring lacks explicit date format specification (YYYY-MM-DD), which is crucial for reliable LLM tool usage.

---
### The docstring currently reads `"""********** <--- Fill in the docstring for this function.`
**Frequency**: 1 students (stu_333)

**Details**:
**Update the Docstring**:
    *   **Issue**: The docstring currently reads `"""********** <--- Fill in the docstring for this function.`
    *   **Why it matters**: Agents rely heavily on docstrings to understand *how* and *when* to use a tool. Without a clear description and parameter details, the agent is essentially guessing, which leads to hallucinations or incorrect tool usage in production.
    *   **Fix**: Replace the placeholder with a standard Google-style or NumPy-style docstring that includes:
        *   A short summary of what the tool does (e.g., "Retrieves available activities for a specific date and city.").
        *   An `Args:` section defining `date` (str) and `city` (str).
        *   **Crucially**, specify the required date format (e.g., "YYYY-MM-DD").

#

---
## Criterion 4 Failures

### Unstructured Failure Feedback
**Frequency**: 262 students (stu_333, stu_139, stu_106, stu_302, stu_130, ... (+257 more))

**Why it fails**: See details in full text.

---
### Assessment Feedback
**Frequency**: 24 students (stu_139, stu_106, stu_108, stu_163, stu_164, ... (+19 more))

**Why it fails**: Based on the rubric requirements, I evaluated your ITINERARY_REVISION_AGENT_SYSTEM_PROMPT against the following criteria:

#

---
### Your "Available Tools" section lists the *names* and *purposes* of the tools (e.g., "get_activities_by_date_tool: Retrieve valid activities..."), but it does not tell the model what **arguments** (parameters) these tools require.
**Frequency**: 1 students (stu_333)

**Details**:
**Add Tool Parameter Schemas**:
    *   **Issue**: Your "Available Tools" section lists the *names* and *purposes* of the tools (e.g., "get_activities_by_date_tool: Retrieve valid activities..."), but it does not tell the model what **arguments** (parameters) these tools require.
    *   **Why it matters**: Without knowing that `get_activities_by_date_tool` requires `date` and `city` arguments, the model is flying blind. It might guess correctly sometimes, but often it will hallucinate arguments or fail to provide required ones.
    *   **Fix**: Update the "Available Tools" section to include the expected arguments for each tool. You can do this manually or dynamically inject the tool docstrings (if you fix the docstrings from Criterion 3).

#

---
## Criterion 5 Failures

### Unstructured Failure Feedback
**Frequency**: 251 students (stu_333, stu_139, stu_106, stu_302, stu_130, ... (+246 more))

**Why it fails**: See details in full text.

---
### Assessment Feedback
**Frequency**: 17 students (stu_89, stu_191, stu_165, stu_223, stu_277, ... (+12 more))

**Why it fails**: Your implementation meets some of the requirements for this criterion:

*   **`VacationInfo` Model:** The `VacationInfo` model is correctly defined and used to validate the initial vacation details.
*   **`TravelPlan` Schema:** The `TravelPlan.model_json_schema()` is correctly included in the `ITINERARY_AGENT_SYSTEM_PROMPT`.
*   **`TravelPlan` Generation:** The `TravelPlan` object is not successfully generated due to a validation error. The JSON output from the LLM does not match the `TravelPlan` Pydantic model.

---
## Criterion unknown Failures

### Assessment Feedback
**Frequency**: 8 students (stu_139, stu_108, stu_199, stu_109, stu_138, ... (+3 more))

**Why it fails**: Evaluation: **RIGHT**

**Evidence from student code (lines 943-969):**
```python
ITINERARY_AGENT_SYSTEM_PROMPT = f"""
You are an expert travel planner.  # ✅ Clear role

---
### Unstructured Failure Feedback
**Frequency**: 1 students (stu_141)

**Why it fails**: See details in full text.

---
