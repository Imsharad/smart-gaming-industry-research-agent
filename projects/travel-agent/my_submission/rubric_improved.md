# AgentsVille Trip Planner: Multi-Agent Travel Assistant System
## LLM Reviewer Rubric and Assessment Guide

---

## **REVIEW INSTRUCTIONS FOR LLM ASSESSORS**

### **Overall Assessment Framework**
For each criterion section, provide:
1. **Status**: `PASS` | `FAIL`
2. **What's Awesome**: Highlight specific strengths and correct implementations
3. **Requires Changes** (if applicable): List specific issues that must be addressed
4. **Suggestions**: Provide actionable improvement recommendations

### **Critical Issues Protocol**
- **CRITICAL BUG**: Any issue that prevents code execution or produces incorrect results
- **MISSING REQUIREMENT**: Any rubric requirement not implemented
- **QUALITY ISSUE**: Spelling, grammar, or formatting problems affecting professionalism

---

## **RUBRIC CRITERIA**

### **1. General Prompt Design**

#### **1.1 Design a system prompt that effectively guides the LLM to produce a comprehensive, structured itinerary**
**Location**: `ITINERARY_AGENT_SYSTEM_PROMPT` variable

**Requirements Checklist**:
- [ ] **Role Definition**: Clearly instructs LLM to assume role as travel planner/agent
- [ ] **Chain-of-Thought**: Encourages detailed daily plans through reasoning guidance or examples
- [ ] **Output Format**: Specifies JSON format matching TravelPlan Pydantic model structure
- [ ] **Context Integration**: Includes VacationInfo object, weather data, and activities data
- [ ] **Task Clarity**: Defines comprehensive itinerary generation requirements
- [ ] **JSON Validation**: Output validates against the TravelPlan Pydantic model
- [ ] **Step-by-Step Planning**: Includes examples or cues that elicit day-by-day planning (e.g., "for each day...")

**PASS/FAIL Criteria**:
The system prompt **PASSES** if:
- The system prompt includes clear role instruction, JSON output expectations tied to the Pydantic model, and necessary context, AND
- The JSON output validates against the TravelPlan model, AND
- Review for examples or implicit cues that elicit step-by-step planning (e.g., "for each day…")

**Common Issues to Check**:
- Missing or vague role assignment
- Lack of step-by-step reasoning instructions
- JSON schema mismatch with Pydantic models
- Missing weather/activity context variables
- Unclear task specifications
- JSON output fails validation against TravelPlan model
- Missing day-by-day planning guidance

**Quality Indicators**:
- Specific output format examples
- Clear reasoning structure (e.g., ANALYSIS section)
- Proper context variable inclusion (`{weather_data}`, `{activities_data}`)
- Explicit step-by-step planning instructions
- JSON schema validation compatibility

**Recommendation**: Include the complete TravelPlan Pydantic model schema in the prompt if results are inconsistent with expected structure.

---
#### **1.2 Design a system prompt that determines whether an event should be avoided due to weather conditions**
**Location**: `ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT` variable

**Requirements Checklist**:
- [ ] **Role Definition**: Clearly defines LLM role as weather-compatibility evaluator
- [ ] **Task Specification**: Explains weather suitability evaluation task
- [ ] **Output Format**: Specifies exact format (e.g., IS_COMPATIBLE/IS_INCOMPATIBLE)
- [ ] **Examples**: Includes relevant scenarios illustrating expected evaluations
- [ ] **Decision Logic**: Provides guidance on compatibility assessment
- [ ] **Backup Options**: Mentions considering backup options for activities

**PASS/FAIL Criteria**:
The system prompt **PASSES** if:
- The role, task, and output format are present in the prompt, AND
- The prompt mentions considering backup options for activities, AND
- The examples show at least one example of IS_COMPATIBLE and one of IS_INCOMPATIBLE

**Note**: This prompt is less involved than the others. The emphasis here is on the examples.

**Common Issues to Check**:
- Spelling/grammar errors affecting clarity
- Missing or inadequate examples
- Unclear output format specification
- Lack of evaluation criteria guidance
- Missing backup option considerations

**Quality Indicators**:
- Multiple scenario examples (indoor/outdoor, various weather)
- Clear reasoning structure
- Specific output tokens for parsing
- Examples demonstrating both IS_COMPATIBLE and IS_INCOMPATIBLE outcomes
- Guidance on considering backup plans and indoor alternatives

---

### **2. Agent Reasoning and Tool Use**

#### **2.1 Design a tool description that guides the LLM to call it when needed**
**Location**: `get_activities_by_date_tool` function docstring

**Requirements Checklist**:
- [ ] **Purpose Description**: Sufficient explanation of tool's function and use case
- [ ] **Parameter Definition**: All input parameters with data types specified
- [ ] **Format Specification**: Data formats clearly defined (e.g., "YYYY-MM-DD" for dates)
- [ ] **Example Usage**: Demonstrates proper tool invocation
- [ ] **Return Type**: Describes expected output structure

**Specific Docstring Requirements**:
- [ ] **First Line**: Short description of the tool's purpose
- [ ] **Parameters**: List of parameters including `date (str)` and `city (str)`
- [ ] **Date Format**: Date format specified as "YYYY-MM-DD" or "%Y-%m-%d" or equivalent
- [ ] **ReAct Usage**: Tool used properly by the ReAct agent

**PASS/FAIL Criteria**:
Check that the docstring for `get_activities_by_date_tool` **PASSES** if:
- A short description on the first line
- A list of parameters/arguments including date (str) and city (str)
- The date format is given as YYYY-MM-DD or %Y-%m-%d or something equivalent
- Check that the tool is used properly by the ReAct agent

**Common Issues to Check**:
- Vague or missing purpose description
- Missing parameter type annotations
- Lack of format specifications (especially date formats)
- Incomplete or missing examples
- Grammar/spelling errors in docstring
- LLM not writing date parameter in correct format during ReAct execution

**Quality Indicators**:
- Clear, concise function description
- Complete parameter documentation with types and formats
- Practical usage examples
- Proper date format specification to guide LLM usage

**Recommendation**: If the tool parameter date is not being written properly by the LLM during ReAct execution, recommend adding the date format specification to the tool description to improve LLM compliance.

---
#### **2.2 Design a prompt that guides an LLM to use reasoning and tools in the ReAct cycle**
**Location**: `ITINERARY_REVISION_AGENT_SYSTEM_PROMPT` variable

**Requirements Checklist**:
- [ ] **Role Assignment**: Clearly states LLM role and itinerary revision task
- [ ] **ReAct Cycle**: Explicitly details THINK-ACT-OBSERVE cycle
- [ ] **Tool Listing**: Dynamically lists all available tools with purposes and parameters
- [ ] **Action Format**: Specifies exact JSON format: `{"tool_name": "[tool_name]", "arguments": {"arg1": "value1", ...}}`
- [ ] **Exit Strategy**: Includes explicit final_answer_tool invocation instruction
- [ ] **Evaluation Workflow**: States run_evals_tool must be executed before final_answer_tool
- [ ] **Context Provision**: Includes traveler feedback and itinerary schema information

**PASS/FAIL Criteria**:
The prompt **PASSES** if:
- The prompt guides the LLM step-by-step, clearly delineating the reasoning (THOUGHT) and the tool call (ACTION) portions of the response (e.g. in the output format section), AND
- The tool descriptions and argument schemas are included in the prompt (dynamic insertion is nice but not needed), AND
- The agent calls run_evals_tool at least once, AND
- The agent terminates the loop by calling final_answer_tool

**Common Issues to Check**:
- Missing or incomplete ReAct cycle explanation
- Incorrect tool call JSON format
- Missing evaluation workflow requirement
- Inadequate tool descriptions
- No clear exit strategy
- LLM not requesting tool calls or the right tool calls

**Quality Indicators**:
- Detailed ReAct cycle explanation with examples
- Comprehensive tool documentation
- Clear workflow instructions
- Explicit evaluation requirements

**Recommendation**: If the model is not requesting tool calls or the right tool calls, recommend having the LLM use a step-by-step process within the THOUGHT section to plan, do reasoning, and then to decide on a tool to use.

**Note**: This prompt doesn't need examples to work well.

---
### **3. Structured Output Validation**

#### **3.1 Pydantic models are created and used properly**

**VacationInfo Model Requirements**:
- [ ] **Model Creation**: Properly implements all required fields from JSON structure
- [ ] **Field Types**: Correct data types for all attributes (List[Traveler], str, datetime.date, int)
- [ ] **Usage Correctness**: Model used properly in data retrieval operations
- [ ] **Date Handling**: Start/end dates used correctly in date range operations

**TravelPlan Model Integration**:
- [ ] **Schema Inclusion**: TravelPlan schema included in relevant system prompts
- [ ] **Output Validation**: JSON outputs validate against TravelPlan structure
- [ ] **Field Completeness**: All required TravelPlan fields addressed in prompts

**Critical Usage Checks**:
- [ ] **Date Range Logic**: Verify `date_of_arrival` used as start, `date_of_departure` as end
- [ ] **Data Retrieval**: Weather and activity APIs called with correct date ranges
- [ ] **Model Validation**: Successful parsing and validation of generated outputs

**PASS/FAIL Criteria**:
The Pydantic models **PASS** if:
- The VacationInfo Pydantic object is created and used successfully at the beginning of the notebook, AND
- The TravelPlan Pydantic object is successfully generated and viewed at the end of the notebook

**Common Critical Issues**:
- **SWAPPED DATES**: Using departure date as start and arrival date as end
- **EMPTY DATA**: Invalid date ranges resulting in no weather/activity data
- **SCHEMA MISMATCH**: JSON outputs not matching Pydantic model structure

---

## **ASSESSMENT GUIDELINES**

### **PASS Criteria**:
- All requirements implemented correctly
- No critical bugs or missing functionality
- Minor quality issues acceptable (small typos, formatting)
- Code executes successfully and produces expected results

### **FAIL Criteria**:
- One or more requirements not met
- Critical bugs affecting functionality
- Multiple quality issues impacting professionalism
- Missing explicit requirements from rubric

---

## **COMMON CRITICAL ISSUES TO IDENTIFY**

### **Execution-Breaking Issues**:
1. **Date Range Errors**: Swapped start/end dates causing empty data retrieval
2. **Missing Context**: Weather/activity data not included in prompts
3. **Schema Mismatches**: JSON outputs incompatible with Pydantic models
4. **Tool Call Errors**: Incorrect JSON format for tool invocations

### **Missing Requirements**:
1. **Evaluation Workflow**: Missing run_evals_tool before final_answer_tool requirement
2. **ReAct Details**: Insufficient THINK-ACT-OBSERVE cycle explanation
3. **Format Specifications**: Missing data format requirements in tool descriptions
4. **Examples**: Inadequate or missing prompt examples

### **Quality Issues**:
1. **Spelling/Grammar**: Multiple errors affecting professionalism
2. **Incomplete Documentation**: Missing docstring elements
3. **Unclear Instructions**: Vague or ambiguous prompt guidance

---

## **REVIEW OUTPUT FORMAT**

Structure your review using this template for each criterion: