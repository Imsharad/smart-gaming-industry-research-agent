# Criteria 4: Agent Demonstration and Reporting

**Demonstrate and report on the agent's performance with example queries**

## Setup

```bash
# Set the student directory variable (replace X with actual student number)
STUDENT_DIR="stu_X"  # e.g., stu_51, stu_52, stu_49, etc.
```

## Requirements to Pass:

### 1. The submission includes the notebook (Udaplay_02_solution_project.ipynb) that runs the agent on at least three example queries

**Verification Steps:**

```bash
# Check if the required notebook exists
ls -la ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Count number of test queries/examples
grep -c "query.*=\|question.*=\|test.*query\|example.*query" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for numbered queries or test cases
grep -n "query.*1\|Query.*1\|Example.*1\|Test.*1" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "query.*2\|Query.*2\|Example.*2\|Test.*2" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "query.*3\|Query.*3\|Example.*3\|Test.*3" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for different types of queries
grep -i "release.*date\|when.*released\|launch" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -i "platform\|playstation\|xbox\|nintendo\|console" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -i "publisher\|developer\|company\|studio" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -i "genre\|type.*game\|rpg\|racing\|action" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify agent execution for each query
grep -n "agent.invoke\|agent.run\|agent.query\|agent.chat" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Count actual execution outputs
grep -c "output_type.*execute_result\|output_type.*stream" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 2. The output for each query includes the agent's reasoning, tool usage, and final answer

**Verification Steps:**

```bash
# Check for reasoning/thought process visibility
grep -n "reasoning\|thinking\|thought\|decision" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "Step.*:\|stage.*:\|phase.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for tool usage logging
grep -n "Using.*tool\|Calling.*tool\|Executing.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "tool.*called\|tool.*selected\|invoke.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "retrieve\|evaluate\|web.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for intermediate results display
grep -n "Retrieved.*:\|Found.*:\|Results.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "Evaluation.*:\|Quality.*:\|Relevance.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify final answer formatting
grep -n "Final.*answer\|Answer.*:\|Response.*:\|Result.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "==.*==\|---\|###.*Answer" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for verbose/debug output settings
grep -n "verbose.*True\|debug.*True\|show.*reasoning" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for structured output format
grep -n "json.dumps\|pprint\|format.*output\|display" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 3. The report includes at least the response with citation, if any

**Verification Steps:**

```bash
# Check for citations in responses
grep -n "Source.*:\|Citation.*:\|Reference.*:\|\[.*\]" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "According.*to\|Based.*on\|From.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for web source citations
grep -n "http\|www\|URL.*:\|Link.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "tavily\|web.*result\|online.*source" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for internal source citations
grep -n "database\|collection\|internal.*source\|local.*data" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify report generation or summary
grep -n "report\|summary\|Report\|Summary" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "Performance\|Results.*Analysis\|Evaluation.*Report" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for markdown report cells
grep -n "## .*Report\|# .*Summary\|### .*Results" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for response metadata
grep -n "metadata\|confidence\|source.*type\|retrieval.*method" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Additional Verification Commands:

```bash
# Check for complete query-response pairs
grep -B2 -A10 "query.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | grep -E "query|response|answer"

# Verify execution time or performance metrics
grep -n "time\|duration\|elapsed\|took.*seconds" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for error handling in demonstrations
grep -n "could.*not.*find\|no.*results\|unable.*to" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for comparison between tool outputs
grep -n "internal.*vs\|compare\|better.*than\|more.*accurate" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify diverse query types
grep -n "different.*queries\|various.*questions\|test.*cases" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Quick Demonstration Check:

```bash
# One-liner to verify demonstration completeness
echo "=== Checking Demonstrations in ${STUDENT_DIR} ===" && \
echo "Test queries found: $(grep -c "query.*=\|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Agent executions: $(grep -c "agent.invoke\|agent.run" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Tool usage logs: $(grep -c "tool.*called\|Using.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Final answers: $(grep -c "Answer.*:\|Response.*:\|Final" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Citations: $(grep -c "Source.*:\|Citation.*:\|Reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Output cells: $(grep -c '"output_type":' ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Query Coverage Verification:

```bash
# Check variety of queries tested
echo "=== Query Type Coverage ===" && \
echo "Release date queries: $(grep -ic "when.*release\|release.*date" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Platform queries: $(grep -ic "platform\|console\|system" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Publisher queries: $(grep -ic "publisher\|developer\|who.*made" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Genre queries: $(grep -ic "genre\|type.*game\|category" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Comparison queries: $(grep -ic "compare\|difference\|similar" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Output Quality Check:

```bash
# Verify output completeness for each query
echo "=== Output Quality Check ===" && \
for i in 1 2 3; do
  echo "Query $i outputs:" && \
  grep -A20 "query.*$i\|Query.*$i\|Example.*$i" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null | \
  grep -c "tool\|answer\|source" 2>/dev/null || echo "0"
done
```

## Report Structure Verification:

```bash
# Check for proper report sections
echo "=== Report Structure ===" && \
grep -n "Introduction\|Overview\|Background" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2 && \
grep -n "Method\|Approach\|Implementation" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2 && \
grep -n "Results\|Findings\|Output" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2 && \
grep -n "Conclusion\|Summary\|Discussion" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2
```

## Reviewer Tips:

- **Check** that at least three example queries are run and outputs are shown
- **Confirm** that the agent's reasoning and tool usage are visible in the output
- **Ensure** that the report contains the final response and the citation, if from web
- **IMPORTANT:** Do NOT fail if the agent cannot answer every query perfectly, as long as the process is demonstrated

## What to Look For:

- **Complete demonstrations:** Each query shows the full agent workflow
- **Tool selection reasoning:** Clear evidence of why tools were chosen
- **Retrieval attempts:** Shows internal search attempts before web fallback
- **Evaluation results:** Displays quality assessment of retrieved information
- **Final responses:** Clear, well-formatted answers with proper citations
- **Process visibility:** The decision-making process is transparent

## Common Issues to Check:

```bash
# Insufficient number of queries
[ $(grep -c "query.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) -lt 3 ] && \
echo "WARNING: Less than 3 queries demonstrated"

# No execution outputs
grep -c '"outputs": \[\]' ${STUDENT_DIR}/Udaplay_02_*project.ipynb && \
echo "WARNING: Empty outputs - notebook may not be executed"

# Missing reasoning visibility
grep -c "reasoning\|thought\|decision" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || \
echo "WARNING: Agent reasoning not visible"

# No citations in responses
grep -c "source\|citation\|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || \
echo "WARNING: No citations found in responses"

# Tool usage not shown
grep -c "tool.*called\|Using.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || \
echo "WARNING: Tool usage not demonstrated"
```

## Acceptable Demonstration Formats:

```bash
# Various valid demonstration approaches
echo "=== Checking for different demonstration styles ===" && \
echo "Interactive demos: $(grep -c "input()\|interact\|widget" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Batch testing: $(grep -c "for.*query.*in\|test_queries.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Individual cells: $(grep -c "query.*=.*\"" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Test framework: $(grep -c "test_\|assert\|TestCase" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Final Completeness Check:

```bash
# Comprehensive check for all demonstration requirements
echo "=== FINAL DEMONSTRATION COMPLETENESS ===" && \
QUERIES=$(grep -c "query.*=\|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
REASONING=$(grep -c "reasoning\|thought\|Step" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
TOOLS=$(grep -c "tool\|retrieve\|evaluate\|search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
ANSWERS=$(grep -c "Answer\|Response\|Result" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
CITATIONS=$(grep -c "Source\|Citation\|Reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
echo "✓ Queries: $QUERIES (min: 3)" && \
echo "✓ Reasoning shown: $REASONING" && \
echo "✓ Tool usage shown: $TOOLS" && \
echo "✓ Answers provided: $ANSWERS" && \
echo "✓ Citations included: $CITATIONS" && \
[ $QUERIES -ge 3 ] && echo "PASS: Meets minimum requirements" || echo "FAIL: Needs at least 3 queries"
```

## Further Reading

### High-Authority Sources from Leading AI Companies

**OpenAI: Agent Evaluation and Safety**
https://openai.com/research/constitutional-ai
OpenAI's research on evaluating AI agent safety, including methodologies for testing agent behavior, output quality, and alignment with intended objectives.

**Anthropic: Constitutional AI and Agent Evaluation**
https://www.anthropic.com/research/constitutional-ai
Anthropic's groundbreaking research on Constitutional AI, providing frameworks for training and evaluating AI systems to be helpful, harmless, and honest.

**Google: AI Agent Testing Framework**
https://ai.google.dev/docs/agent_testing
Google's comprehensive framework for testing AI agents, including unit testing, integration testing, and performance evaluation methodologies.

**Microsoft: Responsible AI Agent Development**
https://www.microsoft.com/en-us/ai/responsible-ai
Microsoft's guide to responsible AI development including testing frameworks, evaluation metrics, and bias detection for production agent systems.

### Agent Testing & Performance Evaluation

**DeepEval: Comprehensive Agent Testing**
https://docs.confident-ai.com/docs/getting-started
Advanced framework for testing LLM applications and agents, including hallucination detection, factual accuracy, and performance benchmarking.

**LangSmith: Agent Evaluation Platform**
https://docs.smith.langchain.com/evaluation
LangChain's production-grade evaluation platform for testing agent performance, conversation quality, and system reliability at scale.

**Weights & Biases: Agent Performance Monitoring**
https://docs.wandb.ai/guides/prompts
W&B's comprehensive platform for tracking agent experiments, performance metrics, and evaluation results with detailed analytics and visualization.

### Demonstration Best Practices & User Experience

**OpenAI: Prompt Engineering Guide**
https://platform.openai.com/docs/guides/prompt-engineering
OpenAI's official guide to prompt engineering including best practices for creating effective demonstrations and test cases for AI agents.

**Anthropic: Claude Usage Guidelines**
https://docs.anthropic.com/claude/docs/how-to-use-claude
Anthropic's comprehensive guide to effectively demonstrating AI capabilities, including conversation design and interaction patterns.

**Google: Conversational AI Design**
https://developers.google.com/assistant/conversation-design
Google's design principles for conversational AI systems, including user experience patterns and demonstration strategies.

### Performance Analytics & Monitoring

**DataDog: LLM Observability**
https://docs.datadoghq.com/llm_observability/
DataDog's comprehensive platform for monitoring AI applications in production, including conversation tracking, performance analytics, and error detection.

**Azure Application Insights: AI Monitoring**
https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
Microsoft's application monitoring platform adapted for AI systems, including custom metrics, telemetry, and performance dashboards.

**AWS CloudWatch: AI System Monitoring**
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/
AWS's comprehensive monitoring solution for AI applications, including custom metrics, log analytics, and automated alerting.

### Quality Assurance & Reliability Engineering

**Netflix: Chaos Engineering for AI Systems**
https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116
Netflix's approach to testing system reliability through chaos engineering, applicable to building robust AI agent systems.

**Google SRE: Site Reliability for AI**
https://sre.google/sre-book/table-of-contents/
Google's Site Reliability Engineering principles applied to AI systems, including monitoring, incident response, and performance optimization.

### Benchmarking & Standardized Evaluation

**HuggingFace: Agent Evaluation Suite**
https://huggingface.co/docs/evaluate/index
HuggingFace's comprehensive evaluation library for language models and agents, including standardized benchmarks and custom metric creation.

**OpenAI Evals: Agent Testing Framework**
https://github.com/openai/evals
OpenAI's open-source framework for evaluating language models and agents, including standardized test suites and custom evaluation creation.

**Stanford HELM: Holistic Evaluation**
https://crfm.stanford.edu/helm/latest/
Stanford's comprehensive benchmark for evaluating language models across multiple dimensions including accuracy, bias, and robustness.

### Documentation & Reporting Standards

**Mozilla AI: Responsible AI Documentation**
https://foundation.mozilla.org/en/ai/
Mozilla's framework for documenting AI systems including model cards, evaluation reports, and transparency requirements.

**Partnership on AI: Best Practices**
https://partnershiponai.org/
Industry consortium guidelines for AI development including documentation standards, evaluation methodologies, and ethical considerations.

### Enterprise Deployment & Governance

**IBM Watson: AI Governance**
https://www.ibm.com/watson/ai-governance
IBM's comprehensive framework for AI governance including evaluation standards, compliance monitoring, and risk management for enterprise AI systems.

**Salesforce: Trusted AI**
https://www.salesforce.com/news/stories/trusted-ai-principles/
Salesforce's principles for building trusted AI systems including testing frameworks, bias detection, and performance monitoring.

### Research & Advanced Evaluation Methods

**MIT: AI System Evaluation Research**
https://www.csail.mit.edu/research/artificial-intelligence
MIT's cutting-edge research on AI evaluation methodologies including novel testing approaches and evaluation metrics.

**Stanford HAI: Human-AI Interaction**
https://hai.stanford.edu/research
Stanford's research on human-AI interaction including evaluation frameworks for conversational systems and agent usability.

## MANDATORY: External Resources

When generating feedback/4.md, you MUST:

1. Read /criteria_prompts/external_links.md
2. Navigate to "## Criterion 4: Agent Demonstration and Reporting" section
3. Use ONLY links from that section (include all relevant links that support comprehensive learning)
4. Copy URLs exactly - do NOT modify or generate new ones
5. Contextualize each link to the student's specific work with detailed explanations

FORBIDDEN ACTIONS:

- Using links from your training data or knowledge
- Generating URLs based on what "seems" correct
- Using web search to find alternative resources
- Modifying URLs from external_links.md


Paste these EXACT external Image URLs AS IT IS :

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766746155/image.png)
