# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains an automated review system for evaluating student submissions in the Udacity "Building Agents" nanodegree project. The system uses a sophisticated "Orchestrator-Worker" pattern with three specialized Claude sub-agents to transform manual review processes into autonomous, scalable evaluation.

## Architecture

### Automated Review System ("Review Factory")
- **Centralized Review Engine**: Shared agents and rubrics in `.claude/` and `criteria_prompts/`
- **Sandboxed Execution**: Each review runs in isolated `tmp/review_stu_*/` environments
- **Factory Script**: `review.sh` orchestrates the entire automated workflow

### Three-Agent Architecture
1. **RubricAgent**: Reads and understands evaluation criteria
2. **CriterionAgent**: Evaluates student code against individual rubric criteria
3. **FeedbackAgent**: Synthesizes individual evaluations into coherent final reports

### Student Project Structure
Students submit projects containing:
- `Udaplay_01_*project.ipynb` - RAG pipeline implementation notebook
- `Udaplay_02_*project.ipynb` - Stateful agent implementation notebook  
- `games/` directory with JSON game data files
- `lib/` directory for supporting Python modules
- Vector database implementation (ChromaDB, Pinecone, etc.)

## Common Commands

### Running Automated Reviews
```bash
# Review a single student submission
./review.sh stu_75

# The script automatically:
# 1. Creates sandboxed environment in tmp/review_stu_75/
# 2. Copies review engine and student files
# 3. Executes multi-step evaluation workflow
# 4. Generates feedback files and final summary
```

### Manual Review Process
```bash
# Set student directory for manual evaluation
STUDENT_DIR="stu_75"

# Check specific criteria manually
cd criteria_prompts/
# Follow commands from criteria1.md through criteria4.md
```

### Environment Setup
```bash
# Install required dependencies
pip install -r requirements.txt
# Includes: chromadb, openai, pydantic, python-dotenv, tavily-python
```

## Evaluation Workflow

### Automated Multi-Step Process
1. **Setup**: Creates `feedback/` directory in sandbox
2. **Evaluation Loop**: Iterates through criteria 1-4, invoking CriterionAgent for each
3. **Synthesis**: FeedbackAgent generates final `summary.md` report

### Four Evaluation Criteria
1. **RAG Pipeline**: Vector database, semantic search, data processing
2. **Agent Tools**: Retrieval, evaluation, and web search tools with proper workflow
3. **Stateful Agent**: Conversation state management and multi-query support  
4. **Demonstration**: Example queries with reasoning and tool usage

## Key Files and Directories

### Review Engine Components
- `.claude/agents/` - Three specialized agent definitions
- `criteria_prompts/` - Detailed rubric criteria and verification commands
- `review.sh` - Factory script for automated review orchestration

### Student Submissions
- `tmp/stu_*/` - Individual student submission directories
- `tmp/review_stu_*/` - Sandboxed review environments (temporary)

### Generated Outputs
- `tmp/review_stu_*/feedback/*.md` - Individual criterion evaluations
- `tmp/review_stu_*/summary.md` - Final synthesized review report

## Implementation Philosophy

### Flexibility in Student Solutions
- Accept various vector databases (ChromaDB, Pinecone, Weaviate, FAISS)
- Accept different web search APIs (Tavily, Serper, Google)
- Accept different LLM frameworks (LangChain, LlamaIndex, custom implementations)
- Focus on functionality and requirements over specific technology choices

### Review Quality Assurance
- Automated checks provide initial assessment
- Manual verification recommended for borderline cases
- Emphasis on constructive feedback and learning opportunities
- Balance between thoroughness and efficiency

## Agent Interaction Patterns

When working with this system:
- Use `criterion-agent` for evaluating against specific rubric criteria
- Use `feedback-agent` for providing constructive code reviews
- Use `rubric-evaluator` for systematic project assessment against structured criteria

The system maintains objectivity while providing actionable feedback to help students improve their implementations.