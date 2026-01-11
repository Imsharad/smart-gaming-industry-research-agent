# CLAUDE.md - Travel Agent Project Review System

This file provides guidance to Claude Code when working with the travel agent project review system. The system uses a sophisticated sub-agent architecture to automate student assignment evaluation.

## Project Overview

This repository contains an automated review system for evaluating student submissions in the Udacity "Travel Agent" project. The system uses Claude sub-agents with an "Orchestrator-Worker" pattern to transform manual review processes into autonomous, scalable evaluation.

## Architecture

### Automated Review System ("Review Factory")
- **Centralized Review Engine**: Shared agents and criteria in `.claude/` and `criteria_prompts/`
- **Sandboxed Execution**: Each review runs in isolated `tmp/stu_*/` environments  
- **Factory Pattern**: Incremental student directories with complete review engine copies

### Sub-Agent Architecture
The system employs specialized agents for different evaluation phases:

1. **workspace-manager**: Downloads, extracts, and organizes student submissions
2. **requirements-interpreter**: Parses rubric criteria into structured evaluation plans
3. **criterion-analyzer**: Evaluates individual criteria using context engineering
4. **context-packager**: Prepares focused context for criterion evaluation
5. **notebook-extractor**: Extracts and processes Jupyter notebook content

### Travel Agent Assignment Structure
Students submit projects containing:
- `project_starter.ipynb` - Main implementation notebook
- `prompts/` directory with YAML prompt files
- Supporting Python modules (`project_lib.py`, etc.)
- Travel planning system implementation with ReAct agents

## Common Evaluation Workflow

### Orchestrated Multi-Step Process

Use the following master prompt to execute the complete evaluation workflow:

```
Execute the following travel agent assignment evaluation workflow:

**Step 1: Setup Workspace**
Use the workspace-manager agent to prepare the student submission. Provide the student number (e.g., 75, 80) and it will:
- Create incremental directory (tmp/stu_75, tmp/stu_75_1, etc.)  
- Extract submission from Downloads
- Copy criteria_prompts/ and .claude/ for isolated evaluation
- Return the workspace path

**Step 2: Context Engineering Pipeline**
Before evaluating criteria, run the context engineering pipeline:
1. Use notebook-extractor to extract all notebook content into structured format
2. Use context-packager to create context/{criterion_number}.md for each criterion
3. Use requirements-interpreter to validate rubric structure (optional)

**Step 3: Execute Sequential Evaluation**
Navigate to the prepared workspace and execute the systematic review process:

FOR criterion_number IN [1, 2, 3, 4, 5]:
1. Use criterion-analyzer with criterion number as parameter
2. Agent reads context/{criterion_number}.md (or extracts directly if missing)
3. Agent creates feedback/{criterion_number}.md with PASS/FAIL assessment
4. Verify file creation before continuing to next criterion

**Step 4: Generate Final Summary**
After all 5 criteria are evaluated, generate summary.md with:
- Overall PASS/FAIL status
- Criterion-by-criterion breakdown
- Priority recommendations for improvement
```

### Five Evaluation Criteria

1. **Criterion 1**: System prompt design for itinerary generation (ITINERARY_AGENT_SYSTEM_PROMPT)
2. **Criterion 2**: Weather compatibility prompt design (ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT)  
3. **Criterion 3**: Tool description quality (get_activities_by_date_tool docstring)
4. **Criterion 4**: ReAct agent reasoning workflow (ITINERARY_REVISION_AGENT_SYSTEM_PROMPT)
5. **Criterion 5**: Pydantic model implementation (VacationInfo and TravelPlan models)

## Key Files and Directories

### Review Engine Components
- `.claude/agents/` - Specialized sub-agent definitions
- `criteria_prompts/` - Detailed evaluation criteria and verification commands
- `criteria_prompts/prompt.md` - Master orchestration instructions

### Student Submissions  
- `tmp/stu_*/` - Individual student submission directories with copied review engines
- Each directory is self-contained with complete evaluation capability

### Generated Outputs
- `tmp/stu_*/feedback/*.md` - Individual criterion evaluations (1.md through 5.md)
- `tmp/stu_*/summary.md` - Final comprehensive assessment report

## Agent Interaction Patterns

When working with this system:

- Use `workspace-manager` for initial submission preparation and workspace setup
- Use `requirements-interpreter` for parsing and structuring rubric criteria  
- Use `criterion-analyzer` for individual criterion evaluation with context engineering
- Use `context-packager` for preparing focused evaluation context
- Use `notebook-extractor` for processing Jupyter notebook submissions

The system maintains complete isolation between evaluations while providing comprehensive, evidence-based assessments of student travel agent implementations.

## Implementation Philosophy

### Context Engineering Approach
- **Isolated Context Windows**: Each criterion evaluation uses fresh 200k token context
- **Pre-Engineered Context**: Filtered, validated, and structured evidence packages
- **Evidence-Based Assessment**: Concrete code quotes and specific technical verification
- **Quality Assurance**: Contamination-free evaluation environment

### Flexible Student Solutions  
- Accept various LLM frameworks (OpenAI, Anthropic, local models)
- Accept different prompt engineering approaches
- Focus on functional requirements over specific implementation choices
- Emphasis on educational outcomes and constructive feedback

The system transforms complex manual evaluation into reliable, scalable, automated assessment while maintaining educational quality and providing actionable student feedback.