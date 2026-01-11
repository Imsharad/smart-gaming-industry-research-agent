## Instructions

**IMPORTANT PATH NOTES:**

1. Replace `stu_X` with the actual student number directory found in the tmp/ folder (e.g., stu_39, stu_40, etc.)
2. Replace `/tmp/` with the actual workspace path (e.g., `/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/`)
3. Use `*.ipynb` wildcard for notebook names instead of hardcoding specific filenames
4. Generate feedback immediately after evaluating each criterion for incremental progress

## Initial Setup

 Identify student directory and notebook

```bash
  # List student directories to find the target student number
  List_dir /Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/
  
  # Find the notebook file (usually *.ipynb)
  Glob_file_search --glob_pattern "*.ipynb" --target_directory "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/"
```

 Read evaluation instructions and rubric

```bash
  Read /Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/.claude/rubric.md
```

## Criterion 1 - General Prompt Design (Itinerary Agent System Prompt)

 Check if ITINERARY_AGENT_SYSTEM_PROMPT has clear role instruction as travel planner

```bash
  Grep --pattern "ITINERARY_AGENT_SYSTEM_PROMPT.*=" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 20
```

 Verify detailed daily plans through Chain-of-Thought guidance

```bash
  Grep --pattern "You are an expert travel agent" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 25
```

 Check for Chain-of-Thought prompting or step-by-step planning

```bash
  Grep --pattern "step.*by.*step\|for each day\|daily plan\|Chain.*of.*Thought\|think.*through" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
```

 Confirm JSON output format matches TravelPlan Pydantic model

```bash
  Grep --pattern "FINAL OUTPUT:" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 10
```

 Verify JSON validates against TravelPlan model (check actual validation)

```bash
  Grep --pattern "TravelPlan.*parse\|TravelPlan.*validate\|json\.loads.*TravelPlan\|TravelPlan\(\*\*" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
```

 Check for necessary context (VacationInfo, weather, activities data)

```bash
  Grep --pattern "VacationInfo\|weather.*data\|activities.*data\|vacation_info" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
```

 **Generate feedback/1.md for Criterion 1**

```bash
  Write /Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/feedback/1.md
  # Content: Assessment of Criterion 1 based on findings following PACT guidelines (Personalized, Accurate, Clear, Thorough)
  # Structure: Personal Note, Assessment, Technical Excellence, Next Steps, Further Learning Resources, Status
```

## **FEEDBACK TEMPLATE REQUIREMENTS**

### Structure Format:

1. Personal Note (recognition of specific student implementation choices)
2. Assessment (detailed analysis of each rubric requirement)
3. Technical Excellence (highlighting advanced implementation aspects)
4. Next Steps & Best Practices (actionable improvement suggestions)
5. Further Learning Resources (curated external links)
6. Status: PASS/FAIL

### Required External Learning Resources Section:

Always include this section with these exact links for Criterion 1:

```
## Further Learning Resources

To deepen your expertise in prompt engineering and Chain-of-Thought reasoning, explore these curated resources:

**Essential Guides:**
- **[Chain-of-Thought Prompting | Prompt Engineering Guide](https://www.promptingguide.ai/techniques/cot)** - Comprehensive guide to CoT techniques with practical examples


- **[The Ultimate Guide to Prompt Engineering in 2025 | Lakera](https://www.lakera.ai/blog/prompt-engineering-guide)** - Latest best practices and emerging techniques

**Advanced Techniques:**
- **[Prompt Engineering Principles for 2024 | PromptHub](https://www.prompthub.us/blog/prompt-engineering-principles-for-2024)** - Industry best practices and real-world applications
- **[LLM Reasoning | Prompt Engineering Guide](https://www.promptingguide.ai/research/llm-reasoning)** - Research-backed approaches to reasoning optimization

**Microsoft Azure Resources:**
- **[Prompt Engineering Techniques - Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/prompt-engineering)** - Production-grade implementation patterns



Include these URLs in feedback:

```

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766906556/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766906573/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766906595/image.png)

```

```
