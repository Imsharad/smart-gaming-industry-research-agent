## Criterion 2 - Weather Compatibility System Prompt

 Check ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT role definition

```bash
  Grep --pattern "ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 30
```

 Verify LLM role and task are clearly defined

```bash
  Grep --pattern "You are.*weather\|determine.*compatible\|evaluate.*weather\|assess.*conditions" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
```

 Verify exact output format specification

```bash
  Grep --pattern "IS_COMPATIBLE\|IS_INCOMPATIBLE\|Output.*format\|return.*IS_" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
```

 Confirm examples showing IS_COMPATIBLE and IS_INCOMPATIBLE cases

```bash
  Grep --pattern "Example.*:" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 10
```

 Check if prompt mentions considering backup options for activities

```bash
  Grep --pattern "backup.*option\|alternative.*activit\|contingency\|rain.*plan" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content"
```

 **Generate feedback/2.md for Criterion 2**

```bash
  Write /Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/feedback/2.md
  # Content: Assessment of Criterion 2 based on findings following PACT guidelines (Personalized, Accurate, Clear, Thorough)
  # Structure: Personal Note, Assessment, Technical Excellence, Next Steps, Further Learning Resources, Status
```

## **FEEDBACK TEMPLATE REQUIREMENTS**

### Structure Format:

1. Personal Note (recognition of specific student implementation choices)
2. Assessment (detailed analysis of each rubric requirement)
3. Technical Excellence (highlighting advanced implementation aspects)
4. Enhancement Opportunities (actionable improvement suggestions)
5. Further Learning Resources (curated external links)
6. Status: PASS/FAIL

### Required External Learning Resources Section:

Always include this section with these exact links for Criterion 2:

```
## Further Learning Resources

Enhance your understanding of AI decision systems and conditional logic with these expert resources:

**AI Agent Decision Making:**
- **[What Is Agentic Reasoning? | IBM](https://www.ibm.com/think/topics/agentic-reasoning)** - Comprehensive overview of AI agent decision-making frameworks
- **[AI Agents and Weather Forecasting for Decision-Making](https://techpilot.ai/ai-agents-and-weather-forecasting/)** - Real-time decision systems for weather compatibility

**Advanced Weather AI Systems:**
- **[AI in Weather Forecasting | Climavision](https://climavision.com/resources/ai-weather-forecasting-guide/)** - Industry guide to weather prediction systems
- **[GraphCast: AI Model for Weather Forecasting - Google DeepMind](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/)** - State-of-the-art weather prediction using Graph Neural Networks

**Conditional Logic & Fuzzy Systems:**
- **[Fuzzy Logic Applications in AI - GeeksforGeeks](https://www.geeksforgeeks.org/artificial-intelligence/fuzzy-logic-applications-in-ai/)** - Practical applications of fuzzy logic for uncertainty handling
- **[Explainable Weather Prediction Framework](https://www.sciencedirect.com/science/article/pii/S0950705124001916)** - Research on interpretable weather decision systems
```

Add this image when student fails at incorporating both examples of IS_COMPATIBLE = TRUE and IS_COMPATIBLE = FALSE

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1767075853/image.png)
