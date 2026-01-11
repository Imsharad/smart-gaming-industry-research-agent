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
grep -c "query.*=|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for numbered queries or test cases
grep -n "query.*1|Query.*1|Example.*1|Test.*1" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "query.*2|Query.*2|Example.*2|Test.*2" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "query.*3|Query.*3|Example.*3|Test.*3" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for different types of queries
grep -i "release.*date|when.*released|launch" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -i "platform|playstation|xbox|nintendo|console" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -i "publisher|developer|company|studio" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -i "genre|type.*game|rpg|racing|action" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify agent execution for each query
grep -n "agent.invoke|agent.run|agent.query|agent.chat" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Count actual execution outputs
grep -c "output_type.*execute_result|output_type.*stream" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 2. The output for each query includes the agent's reasoning, tool usage, and final answer

**Verification Steps:**

```bash
# Check for reasoning/thought process visibility
grep -n "reasoning|thinking|thought|decision" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "Step.*:|stage.*:|phase.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for tool usage logging
grep -n "Using.*tool|Calling.*tool|Executing.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "tool.*called|tool.*selected|invoke.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "retrieve|evaluate|web.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for intermediate results display
grep -n "Retrieved.*:|Found.*:|Results.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "Evaluation.*:|Quality.*:|Relevance.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify final answer formatting
grep -n "Final.*answer|Answer.*:|Response.*:|Result.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "==.*==|---|###.*Answer" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for verbose/debug output settings
grep -n "verbose.*True|debug.*True|show.*reasoning" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for structured output format
grep -n "json.dumps|pprint|format.*output|display" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 3. The report includes at least the response with citation, if any

**Verification Steps:**

```bash
# Check for citations in responses
grep -n "Source.*:|Citation.*:|Reference.*:|\[.*\]" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "According.*to|Based.*on|From.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for web source citations
grep -n "http|www|URL.*:|\[Link.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "tavily|web.*result|online.*source" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for internal source citations
grep -n "database|collection|internal.*source|local.*data" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify report generation or summary
grep -n "report|summary|Report|Summary" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "Performance|Results.*Analysis|Evaluation.*Report" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for markdown report cells
grep -n "## .*Report|# .*Summary|### .*Results" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for response metadata
grep -n "metadata|confidence|source.*type|retrieval.*method" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Additional Verification Commands:

```bash
# Check for complete query-response pairs
grep -B2 -A10 "query.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | grep -E "query|response|answer"

# Verify execution time or performance metrics
grep -n "time|duration|elapsed|took.*seconds" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for error handling in demonstrations
grep -n "could.*not.*find|no.*results|unable.*to" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for comparison between tool outputs
grep -n "internal.*vs|compare|better.*than|more.*accurate" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify diverse query types
grep -n "different.*queries|various.*questions|test.*cases" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Quick Demonstration Check:

```bash
# One-liner to verify demonstration completeness
echo "=== Checking Demonstrations in ${STUDENT_DIR} ===" && \
echo "Test queries found: $(grep -c "query.*=|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Agent executions: $(grep -c "agent.invoke|agent.run" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Tool usage logs: $(grep -c "tool.*called|Using.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Final answers: $(grep -c "Answer.*:|Response.*:|Final" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Citations: $(grep -c "Source.*:|Citation.*:|Reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Output cells: $(grep -c "\"outputs\":" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Query Coverage Verification:

```bash
# Check variety of queries tested
echo "=== Query Type Coverage ===" && \
echo "Release date queries: $(grep -ic "when.*release|release.*date" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Platform queries: $(grep -ic "platform|console|system" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Publisher queries: $(grep -ic "publisher|developer|who.*made" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Genre queries: $(grep -ic "genre|type.*game|category" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Comparison queries: $(grep -ic "compare|difference|similar" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Output Quality Check:

```bash
# Verify output completeness for each query
echo "=== Output Quality Check ===" && \
for i in 1 2 3; do
  echo "Query $i outputs:" && \
  grep -A20 "query.*$i|Query.*$i|Example.*$i" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null | \
  grep -c "tool|answer|source" 2>/dev/null || echo "0"
done
```

## Report Structure Verification:

```bash
# Check for proper report sections
echo "=== Report Structure ===" && \
grep -n "Introduction|Overview|Background" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2 && \
grep -n "Method|Approach|Implementation" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2 && \
grep -n "Results|Findings|Output" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2 && \
grep -n "Conclusion|Summary|Discussion" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -2
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
grep -c "\"outputs\": \[\]" ${STUDENT_DIR}/Udaplay_02_*project.ipynb && \
echo "WARNING: Empty outputs - notebook may not be executed"

# Missing reasoning visibility
grep -c "reasoning|thought|decision" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || \
echo "WARNING: Agent reasoning not visible"

# No citations in responses
grep -c "source|citation|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || \
echo "WARNING: No citations found in responses"

# Tool usage not shown
grep -c "tool.*called|Using.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || \
echo "WARNING: Tool usage not demonstrated"
```

## Acceptable Demonstration Formats:

```bash
# Various valid demonstration approaches
echo "=== Checking for different demonstration styles ===" && \
echo "Interactive demos: $(grep -c "input()|interact|widget" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Batch testing: $(grep -c "for.*query.*in|test_queries.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Individual cells: $(grep -c "query.*=.*\"" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Test framework: $(grep -c "test_|assert|TestCase" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## JSON-based Execution Analysis:

```bash
# Deep analysis of notebook execution outputs using JSON parsing
python3 -c "
import json
import sys

try:
    with open('${STUDENT_DIR}/Udaplay_02_solution_project.ipynb', 'r') as f:
        nb = json.load(f)
    
    print('=== EXECUTION OUTPUT ANALYSIS ===')
    
    # Find agent invocation queries
    query_count = 0
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if cell['source'] else ''
            if 'agent.invoke(' in source:
                query_count += 1
                print(f'Query {query_count} found in cell {i}')
                lines = source.split('\n')
                for line in lines:
                    if 'agent.invoke(' in line:
                        print(f'  {line.strip()}')
    
    print(f'Total agent invocations: {query_count}')
    
    # Analyze execution outputs for demonstration quality
    substantial_outputs = 0
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code' and 'outputs' in cell and cell['outputs']:
            for output in cell['outputs']:
                content = ''
                if 'text' in output:
                    content = ''.join(output['text'])
                elif 'data' in output and 'text/plain' in output['data']:
                    content = ''.join(output['data']['text/plain'])
                
                if len(content) > 100:
                    substantial_outputs += 1
                    break
    
    print(f'Cells with substantial output: {substantial_outputs}')
    
except Exception as e:
    print(f'Error analyzing notebook: {e}')
"
```

```bash
# Analyze actual execution patterns from outputs
python3 -c "
import json

try:
    with open('${STUDENT_DIR}/Udaplay_02_solution_project.ipynb', 'r') as f:
        nb = json.load(f)
    
    # Find the main testing/demonstration cell
    demo_cell = None
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if cell['source'] else ''
            if 'agent.invoke(' in source and len(source) > 500:  # Substantial demo cell
                demo_cell = cell
                print(f'Found demonstration cell {i} with {len(source)} characters')
                break
    
    if demo_cell and 'outputs' in demo_cell and demo_cell['outputs']:
        output_text = ''.join(demo_cell['outputs'][0].get('text', []))
        
        print('\n=== DEMONSTRATION QUALITY METRICS ===')
        print(f'Test queries executed: {output_text.count(\"### TEST\")}')
        print(f'Tool calls made: {output_text.count(\"Tool Called:\")}')
        print(f'Tool responses received: {output_text.count(\"Tool Response from\")}')
        print(f'Citations found: {output_text.count(\"[Source:\")}')
        print(f'Confidence scores: {output_text.count(\"Confidence score:\")}')
        print(f'State machine steps: {output_text.count(\"[StateMachine] Executing step:\")}')
        
        # Check for context retention testing
        if '✅ Context maintained!' in output_text:
            print('✅ Context retention test: PASSED')
        elif '❌ Context lost!' in output_text:
            print('❌ Context retention test: FAILED')
        else:
            print('? Context retention test: NOT FOUND')
    else:
        print('No demonstration outputs found')
        
except Exception as e:
    print(f'Error: {e}')
"
```

```bash
# Extract sample agent responses and verify citation quality
python3 -c "
import json

try:
    with open('${STUDENT_DIR}/Udaplay_02_solution_project.ipynb', 'r') as f:
        nb = json.load(f)
    
    # Find outputs with agent responses
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code' and 'outputs' in cell and cell['outputs']:
            for output in cell['outputs']:
                content = ''
                if 'text' in output:
                    content = ''.join(output['text'])
                
                if 'Answer:' in content and len(content) > 200:
                    print('=== SAMPLE AGENT RESPONSES ===')
                    lines = content.split('\n')
                    
                    response_count = 0
                    for j, line in enumerate(lines):
                        if line.startswith('Answer: '):
                            response_count += 1
                            print(f'\nResponse {response_count}:')
                            print(line[:100] + '...' if len(line) > 100 else line)
                            
                            # Look for citations in next few lines
                            for k in range(1, 8):
                                if j+k < len(lines):
                                    next_line = lines[j+k]
                                    if '[Source:' in next_line or 'Confidence score:' in next_line:
                                        print(f'  {next_line}')
                                    elif next_line.startswith('###') or next_line.startswith('=== '):
                                        break
                            
                            if response_count >= 3:  # Show first 3 responses
                                break
                    break
                    
except Exception as e:
    print(f'Error: {e}')
"
```

## Final Completeness Check:

```bash
# Comprehensive check for all demonstration requirements
echo "=== FINAL DEMONSTRATION COMPLETENESS ===" && \
QUERIES=$(grep -c "query.*=|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
REASONING=$(grep -c "reasoning|thought|Step" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
TOOLS=$(grep -c "tool|retrieve|evaluate|search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
ANSWERS=$(grep -c "Answer|Response|Result" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
CITATIONS=$(grep -c "Source|Citation|Reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
echo "✓ Queries: $QUERIES (min: 3)" && \
echo "✓ Reasoning shown: $REASONING" && \
echo "✓ Tool usage shown: $TOOLS" && \
echo "✓ Answers provided: $ANSWERS" && \
echo "✓ Citations included: $CITATIONS" && \
[ $QUERIES -ge 3 ] && echo "PASS: Meets minimum requirements" || echo "FAIL: Needs at least 3 queries"
```

## Additional Learning Resources:

### Essential Reading - Agent Testing, Evaluation and Demonstration

**LLM Agent Testing and Evaluation:**
- [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/html/2507.21504v1) - Comprehensive academic survey of evaluation methodologies for LLM agents
- [LLM Agent Evaluation: Assessing Tool Use, Task Completion, Agentic Reasoning, and More](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) - Complete guide to component-level and end-to-end agent evaluation
- [10 AI agent benchmarks](https://www.evidentlyai.com/blog/ai-agent-benchmarks) - Overview of standard benchmarking frameworks for AI agents
- [AgentBench: Evaluating LLMs as Agents](https://github.com/THUDM/AgentBench) - First comprehensive benchmark for evaluating LLM-as-Agent across diverse environments

**AI Agent Performance Testing and Validation:**
- [Evaluating AI Agents - DeepLearning.AI](https://www.deeplearning.ai/short-courses/evaluating-ai-agents/) - Structured course on agent evaluation methodologies
- [How to Test AI Agents + Metrics for Evaluation](https://galileo.ai/blog/how-to-test-ai-agents-evaluation) - Practical testing strategies with key performance metrics
- [AI Agent Testing and Validation | Evidently AI](https://www.evidentlyai.com/ai-agent-testing) - Comprehensive testing frameworks and validation approaches
- [Agent Evaluation in 2025: Complete Guide](https://orq.ai/blog/agent-evaluation) - Modern evaluation practices including LLM-as-a-judge and robustness testing

**Agent Workflow Testing and Documentation:**
- [Introducing Agentic Document Workflows — LlamaIndex](https://www.llamaindex.ai/blog/introducing-agentic-document-workflows) - Advanced workflow patterns for agent documentation and reporting
- [How we built our multi-agent research system \\ Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) - Real-world implementation of multi-agent systems with proper documentation
- [Deep Research Workflow in Dify: A Step-by-Step Guide](https://dify.ai/blog/deep-research-workflow-in-dify-a-step-by-step-guide) - Comprehensive workflow design with testing and validation
- [Workflows & agents](https://langchain-ai.github.io/langgraph/tutorials/workflows/) - Official LangGraph tutorials for building testable agent workflows

**Jupyter Notebook Testing and Demonstration Practices:**
- [Jupyter Agents: training LLMs to reason with notebooks](https://huggingface.co/blog/jupyter-agent-2) - Best practices for training and testing agents in Jupyter environments
- [Optimizing Jupyter Notebooks for LLMs](https://www.alexmolas.com/2025/01/15/ipynb-for-llm.html) - Optimization techniques for LLM applications in notebooks
- [LLM Tool-calling — Code Structure and Jupyter Utilities](https://medium.com/@juvvij/llm-tool-calling-1-code-structure-and-jupyter-utilities-26ff52f80a59) - Structured approaches to tool calling demonstration in notebooks
- [From Jupyter to Production: Why Deployment Matters in LLM Projects](https://odsc.medium.com/from-jupyter-to-production-why-deployment-matters-in-llm-projects-39f75c088914) - Transitioning from notebook demonstrations to production systems