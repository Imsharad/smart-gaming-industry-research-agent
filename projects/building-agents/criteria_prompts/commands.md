# MASTER TASK LIST FOR UDAPLAY PROJECT EVALUATION
# Tailored for the AgentsVille Trip Planner / Udaplay Game Information Agent Project

## 📋 PHASE 1: INITIAL SETUP & CONTEXT GATHERING
☐ Set student directory variable: `STUDENT_DIR="stu_X"`
☐ Read and understand evaluation context files
  ☐ Read prompt.md for Udaplay project overview
  ☐ Read reviewer_tip.md for grading guidelines
  ☐ Verify student has both required notebooks:
    - `Udaplay_01_*project.ipynb` (RAG implementation)
    - `Udaplay_02_*project.ipynb` (Agent implementation)
  ☐ Check for supporting directories:
    - games/ (should contain 15 JSON files)
    - lib/ (optional, may contain helper modules)
    - newchromadb/ or chroma_db/ (vector database storage)
  ☐ Create feedback directory: `mkdir -p ${STUDENT_DIR}/feedback`

## 🔍 PHASE 2: SYSTEMATIC CRITERION EVALUATION

### ✅ Criterion 1: RAG - Prepare and process video game dataset for vector database
☐ Read criteria1.md file completely
☐ **Subcriteria 1.1: Data Loading & Processing**
  ☐ Check notebook exists: `ls -la ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify JSON loading: `grep -n "json.load\|pd.read_json\|json.loads" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Check game directory refs: `grep -n "games\|data_dir\|game.*json" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify game files exist: `ls -la ${STUDENT_DIR}/games/*.json 2>/dev/null`
  ☐ Count game files (should be 15): `find ${STUDENT_DIR} -name "*.json" -path "*/games/*" | wc -l`
  ☐ Check data formatting: `grep -n "DataFrame\|dict\|format\|process" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify document structure: `grep -n "metadata\|document\|content\|embedding" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`

☐ **Subcriteria 1.2: Vector Database Setup**
  ☐ Check for ChromaDB imports: `grep -n "chromadb\|ChromaDB\|PersistentClient" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify persistence: `grep -n "persist_directory\|storage\|persistent\|PersistentClient" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Check DB files exist: `find ${STUDENT_DIR} -name "*.sqlite3" -o -name "chroma.sqlite3" 2>/dev/null`
  ☐ Verify collection creation: `grep -n "create_collection\|get_or_create_collection" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Check embedding config: `grep -n "embedding\|embed\|OpenAIEmbeddings" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify data insertion: `grep -n "add\|insert\|upsert\|add_documents" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Check document count: `grep -n "count\|len\|collection.count" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`

☐ **Subcriteria 1.3: Semantic Search Demonstration**
  ☐ Check query implementation: `grep -n "query\|search\|retrieve\|similarity" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify query methods: `grep -n "collection.query\|similarity_search" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Check results handling: `grep -n "results\|distances\|documents\|metadatas" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Look for game queries: `grep -i "racing\|rpg\|playstation\|nintendo\|genre" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  ☐ Verify outputs exist: `grep -A5 "output_type": ${STUDENT_DIR}/Udaplay_01_*project.ipynb | grep -v "outputs.*[]"`
  ☐ Check result display: `grep -n "print.*result\|display\|pprint" ${STUDENT_DIR}/Udaplay_01_*project.ipynb`
  
☐ **Quick Pipeline Check:**
  ```bash
  echo "=== Checking ${STUDENT_DIR} ===" && \
  echo "Notebook exists: $(ls ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null | wc -l)" && \
  echo "Game files: $(find ${STUDENT_DIR} -name "*.json" -path "*/games/*" 2>/dev/null | wc -l)" && \
  echo "ChromaDB refs: $(grep -c "chromadb\|ChromaDB" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)" && \
  echo "Query calls: $(grep -c "query\|search" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)"
  ```
☐ Document findings and generate feedback/1.md with PASS/FAIL status

### ⚙️ Criterion 2: Agent Development - Three tools (retrieval, evaluation, web search)
☐ Read criteria2.md file completely
☐ **Subcriteria 2.1: Tool Implementation**
  ☐ Check tool definitions: `grep -n "@tool\|def.*tool\|class.*Tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check lib modules: `grep -n "@tool\|def.*tool" ${STUDENT_DIR}/lib/*.py 2>/dev/null`
  ☐ **Retrieval Tool:**
    - Verify implementation: `grep -n "retrieve\|retrieval\|get_game\|search_game" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
    - Check vector search: `grep -n "collection.query\|similarity_search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ **Evaluation Tool:**
    - Check implementation: `grep -n "evaluate\|eval\|quality\|relevance\|assess" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
    - Verify function: `grep -n "def evaluate\|class.*Evaluat" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ **Web Search Tool:**
    - Check API integration: `grep -n "tavily\|serper\|google\|bing\|web.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
    - Verify API key: `grep -n "TavilyClient\|api_key\|API_KEY" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 2.2: Tool Integration**
  ☐ Check agent integration: `grep -n "tools=\[\|tool_list\|available_tools" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify tool binding: `grep -n "bind_tools\|tool_executor\|execute_tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check workflow: `grep -n "workflow\|StateGraph\|Graph\|pipeline" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify tool execution: `grep -n "tool_calls\|function_call\|invoke.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check return formats: `grep -n "return.*{.*\|return.*dict\|return.*json" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 2.3: Workflow Order (Internal → Evaluate → Web)**
  ☐ Check workflow sequence: `grep -n -A10 "internal.*first\|try.*internal" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify evaluation step: `grep -n -A10 "evaluate.*result\|check.*quality" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check web fallback: `grep -n -A10 "fallback\|web.*search.*if" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify conditional logic: `grep -n "if.*retriev\|if.*evaluat\|if.*quality" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check state transitions: `grep -n "next.*state\|transition\|should_.*" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  
☐ **Quick Tool Check:**
  ```bash
  echo "=== Checking Tools in ${STUDENT_DIR} ===" && \
  echo "Retrieval tool refs: $(grep -c "retrieve\|retrieval" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Evaluation tool refs: $(grep -c "evaluate\|assess\|quality" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Web search tool refs: $(grep -c "tavily\|web.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Tool decorators: $(grep -c "@tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
  ```
☐ Document findings and generate feedback/2.md with PASS/FAIL status

### 🤖 Criterion 3: Stateful Agent - Conversation management & workflow
☐ Read criteria3.md file completely
☐ **Subcriteria 3.1: Agent Class/Function with State**
  ☐ Check agent class: `grep -n "class.*Agent\|class.*Assistant" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify initialization: `grep -n "__init__.*self\|def.*create_agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check state variables: `grep -n "self.state\|self.memory\|self.history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify conversation history: `grep -n "conversation.*history\|message.*history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check memory implementation: `grep -n "memory\|Memory\|ConversationBuffer" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify session handling: `grep -n "session\|Session\|conversation_id" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 3.2: Multi-Query Session Support**
  ☐ Check multiple queries: `grep -n "while\|for.*query\|multiple.*queries" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify context preservation: `grep -n "append.*history\|add.*message\|update.*context" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check conversation continuity: `grep -n "follow.*up\|previous.*answer\|earlier" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify state updates: `grep -n "state\[.*\]_=\|update.*state" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Look for query examples: `grep -B2 -A5 "query.*1\|Query.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check context references: `grep -n "as.*mentioned\|previously\|earlier" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 3.3: State Machine/Workflow Implementation**
  ☐ Check state machine: `grep -n "StateGraph\|state.*machine\|StateMachine" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify workflow structure: `grep -n "LangGraph\|workflow\|WorkflowGraph" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check nodes/edges: `grep -n "add_node\|add_edge\|add_conditional" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify transitions: `grep -n "transition\|next_state\|should_.*" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check compilation: `grep -n "compile\|build.*graph\|create.*workflow" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Look for modular steps: `grep -n "def.*node\|def.*step\|def.*stage" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 3.4: Clear & Cited Answers**
  ☐ Check citations: `grep -n "source\|citation\|cite\|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify formatting: `grep -n "format.*response\|structure.*answer" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check synthesis: `grep -n "combine\|merge\|synthesize" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify web citations: `grep -B5 -A5 "Information is from.*http" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ **CRITICAL**: Manually verify cited URLs match actual search results (not hallucinated)
  
☐ **Quick State Check:**
  ```bash
  echo "=== Checking State Management in ${STUDENT_DIR} ===" && \
  echo "Agent class defs: $(grep -c "class.*Agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "State variables: $(grep -c "self.state\|self.memory" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Workflow refs: $(grep -c "StateGraph\|workflow" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Multiple queries: $(grep -c "query.*\[0-9\]" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
  ```
☐ Document findings and generate feedback/3.md with PASS/FAIL status

### 📊 Criterion 4: Agent Demonstration - At least 3 example queries
☐ Read criteria4.md file completely
☐ **Subcriteria 4.1: Three Example Queries**
  ☐ Check notebook exists: `ls -la ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Count test queries: `grep -c "query.*=\|question.*=\|test.*query" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Find Query 1: `grep -n "query.*1\|Query.*1\|Example.*1" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Find Query 2: `grep -n "query.*2\|Query.*2\|Example.*2" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Find Query 3: `grep -n "query.*3\|Query.*3\|Example.*3" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify diverse query types:
    - Release dates: `grep -i "release.*date\|when.*released" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
    - Platforms: `grep -i "platform\|playstation\|xbox\|nintendo" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
    - Publishers: `grep -i "publisher\|developer\|company" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
    - Genres: `grep -i "genre\|type.*game\|rpg\|racing" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify executions: `grep -n "agent.invoke\|agent.run\|agent.query" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 4.2: Visible Reasoning & Tool Usage**
  ☐ Check reasoning visibility: `grep -n "reasoning\|thinking\|thought\|Step.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify tool usage logs: `grep -n "Using.*tool\|Calling.*tool\|Executing.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check retrieval attempts: `grep -n "Retrieved.*:\|Found.*:\|Results.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify evaluation display: `grep -n "Evaluation.*:\|Quality.*:\|Relevance.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check final answers: `grep -n "Final.*answer\|Answer.*:\|Response.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify verbose output: `grep -n "verbose.*True\|debug.*True" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`

☐ **Subcriteria 4.3: Report with Citations**
  ☐ Check citations present: `grep -n "Source.*:\|Citation.*:\|Reference.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify web sources: `grep -n "http\|www\|URL.*:\|Link.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Check internal sources: `grep -n "database\|collection\|internal.*source" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Look for report sections: `grep -n "report\|summary\|Report\|Summary" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  ☐ Verify metadata: `grep -n "metadata\|confidence\|source.*type" ${STUDENT_DIR}/Udaplay_02_*project.ipynb`
  
☐ **Quick Demo Check:**
  ```bash
  echo "=== Checking Demonstrations in ${STUDENT_DIR} ===" && \
  echo "Test queries found: $(grep -c "query.*=\|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Agent executions: $(grep -c "agent.invoke\|agent.run" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Tool usage logs: $(grep -c "tool.*called\|Using.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
  echo "Citations: $(grep -c "Source.*:\|Citation.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
  ```
  
☐ **Final Completeness Check:**
  ```bash
  echo "=== FINAL DEMONSTRATION COMPLETENESS ===" && \
  QUERIES=$(grep -c "query.*=\|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null) && \
  [ $QUERIES -ge 3 ] && echo "PASS: $QUERIES queries (min: 3)" || echo "FAIL: Only $QUERIES queries (needs 3)"
  ```
☐ Document findings and generate feedback/4.md with PASS/FAIL status

## 📊 PHASE 3: FINAL ASSESSMENT & SUMMARY
☐ Review all four criterion feedback files
☐ Calculate overall PASS/FAIL status
  ☐ All 4 criteria must PASS for overall PASS
  ☐ Note any exceptional implementations
  ☐ Identify areas for improvement
☐ Create comprehensive summary.md with:
  ☐ Overall result (PASS/FAIL)
  ☐ Individual criterion results
    - Criterion 1: RAG - [PASS/FAIL]
    - Criterion 2: Agent Development - [PASS/FAIL]
    - Criterion 3: Stateful Agent - [PASS/FAIL]
    - Criterion 4: Performance Demo - [PASS/FAIL]
  ☐ Key strengths (specific examples)
  ☐ Areas for improvement (constructive feedback)
  ☐ Next steps recommendations
☐ Verify all files are created:
  - feedback/1.md
  - feedback/2.md
  - feedback/3.md
  - feedback/4.md
  - summary.md

## 📝 FEEDBACK TEMPLATE FOR UDAPLAY PROJECT
Each feedback file should follow this format:
```markdown
# Criterion [N]: [NAME] - [PASS/FAIL] [✅/❌]

[Opening statement about performance on this criterion]

• **[Specific Requirement 1]**: [Evidence with file references/line numbers]
• **[Specific Requirement 2]**: [Evidence with file references/line numbers]  
• **[Specific Requirement 3]**: [Evidence with file references/line numbers]
• **[Key Strength]**: [Highlight exceptional work if any]

[Detailed analysis paragraph with specific examples from their code]

**Status: [PASS/FAIL]**
```

## 🎮 PROJECT-SPECIFIC DETAILS TO VERIFY
☐ **Data Requirements:**
  - Exactly 15 game JSON files in games/ directory
  - Each game has: Name, Platform, YearOfRelease, Genre, Publisher, Description
  - Games include titles like Gran Turismo, Mario Kart, Pokémon, etc.

☐ **Technical Stack:**
  - ChromaDB for vector database (or alternative)
  - OpenAI embeddings (or alternative)
  - Tavily API for web search (or alternative)
  - LangChain/LangGraph or custom implementation

☐ **Agent Workflow Must Follow:**
  1. Internal retrieval from vector DB first
  2. Evaluate quality of retrieved results
  3. Web search only if internal results insufficient

☐ **Common Student Variations to Accept:**
  - Different vector DBs (Weaviate, Pinecone, Qdrant)
  - Different embedding models (HuggingFace, Cohere)
  - Different web search APIs (Serper, Google, Bing)
  - Custom implementations vs framework-based

## 🚨 CRITICAL EVALUATION POINTS
☐ **DO NOT FAIL IF:**
  - Student uses different libraries/frameworks as long as requirements met
  - Simple state management as long as it works
  - Agent can't answer every query perfectly if process is demonstrated
  - Different file/folder structure as long as core files present

☐ **MUST FAIL IF:**
  - Missing either required notebook
  - No vector database implementation
  - Missing any of the three required tools
  - No demonstration of at least 3 queries
  - No evidence of stateful conversation
  - Hallucinated web citations (URLs that don't match actual search results)

## 🎯 QUALITY ASSURANCE CHECKLIST
☐ All verification commands executed (no shortcuts taken)
☐ Evidence-based evaluation with specific line numbers
☐ Constructive feedback tone throughout
☐ Clear PASS/FAIL for each criterion
☐ Overall assessment aligns with criteria results
☐ Actionable improvement suggestions provided
☐ Student's unique approach acknowledged

--- 
*This evaluation template is specifically tailored for the Udaplay/AgentsVille Trip Planner Project focusing on video game information retrieval using RAG and agent-based systems.*
