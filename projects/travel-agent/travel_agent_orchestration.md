# Travel Agent Assignment Evaluation System

## Overview
This system evaluates student submissions for travel agent assignments by analyzing their IPython notebook implementations against the 5-criterion rubric.

## Master Orchestration Prompt

Execute the following context-engineered travel agent assignment evaluation workflow:

### Step 1: Setup Workspace
Use the workspace-manager agent to prepare the student submission from the provided URL. Wait for completion and confirm workspace path.

### Step 2: Extract and Engineer Context (Loop 5x)
Use the notebook-extractor agent to create engineered context packages for each criterion:

For each criterion (1-5):
- Extract all relevant code, outputs, and evidence
- Apply context engineering principles (strategic placement, quality control, compression)
- Write complete context to `context/{criterion_number}.md`
- Ensure isolated, contamination-free context packages

### Step 3: Interpret Rubric Requirements
Use the requirements-interpreter agent to parse the criteria_prompts directory and extract the exact 5 evaluation criteria from the travel agent rubric.

### Step 4: Execute Isolated Evaluation Loop
For each of the 5 criteria from Step 3:

a. Create feedback directory if it doesn't exist

b. Spawn criterion-analyzer agent with:
   - Single criterion definition
   - Pre-engineered context from `context/{n}.md`
   - Complete isolation from other criteria

c. Agent performs evidence-based analysis using engineered context:
   - Reads complete, structured context package
   - Applies rubric requirements exactly
   - Generates PASS/FAIL with specific evidence
   - No grep/find needed - all evidence pre-packaged

d. Generate `feedback/{n}.md` with assessment results

e. **Critical**: Complete context isolation maintained - no memory carries between evaluations

### Step 5: Consolidate Final Report
Combine all feedback files into final_feedback.md with structured evaluation results and overall assessment.

## Context Engineering Benefits Applied

- **Write**: Context externalized to isolated files per criterion
- **Select**: Only relevant information included per criterion  
- **Compress**: Verbose outputs summarized while preserving key details
- **Isolate**: Each criterion evaluation completely independent

This ensures reliable, evidence-based evaluation without context engineering failure modes (Lost in the Middle, context contamination, information overload).

## Agent Roster

| Agent | Purpose | Tools | Output |
|-------|---------|-------|--------|
| workspace-manager | Download/extract submission | bash | Clean workspace |
| notebook-extractor | Parse IPython notebooks for key components | read, grep, find | Extracted implementations |
| requirements-interpreter | Parse 5-criterion rubric | read, glob | Exact evaluation criteria |
| criterion-analyzer | Evaluate single criterion with isolation | read, grep, find, write | Individual PASS/FAIL feedback |

## Key Evaluation Patterns

The system uses specific grep patterns to locate implementations:
- `ITINERARY_AGENT_SYSTEM_PROMPT.*=` for prompt definitions
- `You are.*travel.*planner` for role instructions
- `THINK|THOUGHT|ACT|ACTION` for ReAct patterns
- `def get_activities_by_date_tool` for tool definitions
- `class VacationInfo|class TravelPlan` for Pydantic models
- `IS_COMPATIBLE|IS_INCOMPATIBLE` for weather logic

This ensures precise, evidence-based evaluation against the rubric requirements.

## Specialized Travel Agent Evaluation Criteria

The system will evaluate travel agent assignments against these key areas:

1. **Prompt Design Quality**
   - System prompt effectiveness for itinerary generation
   - Weather compatibility evaluation prompts
   - ReAct cycle implementation for revision agents

2. **Agent Reasoning and Tool Use**
   - Tool description clarity and completeness
   - ReAct methodology implementation
   - Proper tool invocation patterns

3. **Structured Output Validation**
   - Pydantic model implementation
   - JSON schema compliance
   - Data validation and parsing

4. **Multi-Agent Coordination**
   - Agent communication protocols
   - State management between agents
   - Error handling and resilience

5. **Travel Domain Expertise**
   - Weather-activity compatibility logic
   - Budget constraint handling
   - Interest-activity matching algorithms

## Usage Instructions

1. Place this orchestration prompt in the main Claude Code terminal
2. Replace `` with the actual student submission URL
3. Ensure the ./prompts/ directory contains the assignment rubric files
4. Execute the workflow and monitor the real-time to-do checklist
5. Review the final_feedback.md for comprehensive evaluation results

## Key Differences from Building Agents

While following the same architectural pattern, this travel agent system focuses on:
- Travel itinerary generation and optimization
- Weather-activity compatibility evaluation  
- Multi-agent travel planning workflows
- ReAct methodology for iterative improvement
- Travel domain-specific validation criteria

The core sub-agent isolation and orchestration principles remain identical to ensure reliable, repeatable evaluation processes.
