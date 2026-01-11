#!/bin/bash

# Master Review Script for Building Agents Project
# Usage: ./review_all.sh <student_number>
# Example: ./review_all.sh 51

if [ $# -eq 0 ]; then
    echo "Usage: $0 <student_number>"
    echo "Example: $0 51"
    exit 1
fi

STUDENT_NUM=$1
STUDENT_DIR="stu_${STUDENT_NUM}"

echo "=========================================="
echo "REVIEWING STUDENT: ${STUDENT_DIR}"
echo "=========================================="
echo ""

# Check if student directory exists
if [ ! -d "${STUDENT_DIR}" ]; then
    echo "ERROR: Directory ${STUDENT_DIR} not found!"
    exit 1
fi

# Function to print section headers
print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

# Function to check pass/fail
check_result() {
    if [ $1 -ge $2 ]; then
        echo "✅ PASS (found: $1, required: $2)"
    else
        echo "❌ FAIL (found: $1, required: $2)"
    fi
}

# CRITERIA 1: RAG PIPELINE
print_header "CRITERIA 1: RAG PIPELINE"

echo "📁 Checking for required notebook..."
NOTEBOOK1=$(ls ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null | wc -l)
if [ $NOTEBOOK1 -ge 1 ]; then
    echo "  Found: $(ls ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)"
fi
check_result $NOTEBOOK1 1

echo "📊 Checking for game JSON files..."
GAME_FILES=$(find ${STUDENT_DIR} -name "*.json" -path "*/games/*" 2>/dev/null | wc -l)
check_result $GAME_FILES 1

echo "🗄️ Checking for vector database setup..."
CHROMADB=$(grep -c "chromadb\|ChromaDB\|PersistentClient" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)
check_result $CHROMADB 1

echo "💾 Checking for persistence..."
PERSIST=$(grep -c "persist_directory\|PersistentClient" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)
check_result $PERSIST 1

echo "🔍 Checking for semantic search..."
QUERIES=$(grep -c "query\|search" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)
check_result $QUERIES 1

# CRITERIA 2: AGENT TOOLS
print_header "CRITERIA 2: AGENT TOOLS"

echo "🔧 Checking for tool implementations..."
TOOLS=$(grep -c "@tool\|def.*tool\|class.*Tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
echo "  - Tool definitions found: $TOOLS"

echo "📥 Checking for retrieval tool..."
RETRIEVAL=$(grep -c "retrieve\|retrieval\|query_database" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $RETRIEVAL 1

echo "✅ Checking for evaluation tool..."
EVALUATION=$(grep -c "evaluate\|assess\|quality" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $EVALUATION 1

echo "🌐 Checking for web search tool..."
WEBSEARCH=$(grep -c "tavily\|serper\|web.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $WEBSEARCH 1

echo "🔄 Checking workflow order (internal → evaluate → web)..."
WORKFLOW=$(grep -c "workflow\|StateGraph\|pipeline" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $WORKFLOW 1

# CRITERIA 3: STATEFUL AGENT
print_header "CRITERIA 3: STATEFUL AGENT"

echo "🤖 Checking for agent implementation..."
AGENT_CLASS=$(grep -c "class.*Agent\|def.*agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $AGENT_CLASS 1

echo "💭 Checking for state management..."
STATE=$(grep -c "state\|memory\|history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $STATE 1

echo "🔁 Checking for multi-query support..."
MULTI_QUERY=$(grep -c "multiple\|session\|conversation" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $MULTI_QUERY 1

echo "📝 Checking for citations..."
CITATIONS=$(grep -c "source\|citation\|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $CITATIONS 1

# CRITERIA 4: DEMONSTRATION
print_header "CRITERIA 4: DEMONSTRATION & REPORTING"

echo "📓 Checking for required notebook..."
NOTEBOOK2=$(ls ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null | wc -l)
check_result $NOTEBOOK2 1

echo "❓ Checking for example queries..."
EXAMPLE_QUERIES=$(grep -c "query.*=\|question.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $EXAMPLE_QUERIES 3

echo "🎯 Checking for agent executions..."
EXECUTIONS=$(grep -c "agent.invoke\|agent.run\|agent.query" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $EXECUTIONS 3

echo "📊 Checking for output visibility..."
OUTPUTS=$(grep -c '"output_type":' ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $OUTPUTS 3

echo "📋 Checking for reasoning visibility..."
REASONING=$(grep -c "reasoning\|thought\|Step" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)
check_result $REASONING 1

# SUMMARY
print_header "SUMMARY"

TOTAL_PASS=0
TOTAL_FAIL=0

# Count passes and fails (simplified - you can make this more sophisticated)
[ $NOTEBOOK1 -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $GAME_FILES -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $CHROMADB -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $PERSIST -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $QUERIES -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $RETRIEVAL -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $EVALUATION -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $WEBSEARCH -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $WORKFLOW -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $AGENT_CLASS -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $STATE -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $MULTI_QUERY -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $CITATIONS -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $NOTEBOOK2 -ge 1 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $EXAMPLE_QUERIES -ge 3 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))
[ $EXECUTIONS -ge 3 ] && ((TOTAL_PASS++)) || ((TOTAL_FAIL++))

echo "✅ Passed checks: $TOTAL_PASS"
echo "❌ Failed checks: $TOTAL_FAIL"
echo ""

if [ $TOTAL_FAIL -eq 0 ]; then
    echo "🎉 OVERALL: PASS - All criteria met!"
else
    echo "⚠️ OVERALL: REVIEW NEEDED - Some criteria may not be met"
    echo "Please run detailed checks for each criterion:"
    echo "  - See criteria1.md for RAG pipeline details"
    echo "  - See criteria2.md for agent tools details"
    echo "  - See criteria3.md for stateful agent details"
    echo "  - See criteria4.md for demonstration details"
fi

echo ""
echo "=========================================="
echo "For detailed analysis, run specific commands from criteria*.md files"
echo "=========================================="
