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

### Fully Automated Execution ("One-Click Review")

The entire evaluation process is now automated via the `run_auto_review.sh` script, removing the need for human-in-the-loop interaction.

**Command:**
```bash
./run_auto_review.sh
```

**What it does:**
1.  **Preparation**: Calls `setup_next_student_optimized.sh` to extract the latest zip into a new student directory (e.g., `stu_404`).
    *   **Golden Template**: Copies the environment from the immutable `stu_template` directory to prevent configuration drift.
    *   **Flexibility**: Supports both `.ipynb` and `.py` only submissions.
2.  **Execution**: Automatically executes the Gemini agent in "headless" mode (`--yolo`).
    *   **Prompt Injection**: Pipes the content of `notes.txt` directly to the agent.
    *   **Context**: The agent reads the pre-packaged prompt and criteria from the template.
3.  **Verification**: Checks for the generation of 5 criteria feedback files and the final summary.

### Manual / Debug Workflow (Legacy)

If you need to debug a specific student or step:

**Step 1: Setup Workspace**
```bash
./setup_next_student_optimized.sh
```
This creates the directory (e.g., `tmp/stu_75`) using the `stu_template`.

**Step 2: Manual Agent Execution**
Navigate to the directory and run the agent manually:
```bash
cd tmp/stu_75
cat ../notes.txt | gemini --yolo
```

**Step 3: Output Verification**
Check `feedback/` for the generated markdown files.

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
- `tmp/stu_template` - Immutable template for new student directories (prevents configuration drift)

### Generated Outputs
- `tmp/stu_*/feedback/*.md` - Individual criterion evaluations (1.md through 5.md)
- `tmp/stu_*/summary.md` - Final comprehensive assessment report

## Agent Interaction Patterns

When working with this system:

- Use `run_auto_review.sh` for standard end-to-end evaluation
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
