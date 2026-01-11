# Building Agents Project Review Guide

This directory contains comprehensive review tools and criteria for evaluating student submissions for the Building Agents project.

## 📁 Files Overview

- **`criteria1.md`** - RAG Pipeline verification commands
- **`criteria2.md`** - Agent Tools verification commands  
- **`criteria3.md`** - Stateful Agent verification commands
- **`criteria4.md`** - Demonstration & Reporting verification commands
- **`review_all.sh`** - Automated review script for all criteria
- **`reviewer_tip.md`** - Original rubric and reviewer tips

## 🚀 Quick Start

### Option 1: Automated Review (Recommended)

Run the master review script for a quick assessment:

```bash
# From the tmp directory
cd stu_53/criteria_prompts/
./review_all.sh 51  # Replace 51 with the student number
```

This will automatically check all four criteria and provide a summary.

### Option 2: Manual Review

For each criterion file, set the student directory and run the commands:

```bash
# Set the student directory
STUDENT_DIR="stu_51"  # Replace with actual student number

# Then copy and run commands from criteria*.md files
```

## 📋 Review Process

### Step 1: Initial Assessment
Run the automated script to get an overview:
```bash
./review_all.sh 51
```

### Step 2: Detailed Review
For any failing criteria, consult the specific criteria file for detailed commands:

1. **Criteria 1 (RAG)**: Check `criteria1.md` for data loading, vector DB, and semantic search
2. **Criteria 2 (Tools)**: Check `criteria2.md` for tool implementations and workflow
3. **Criteria 3 (State)**: Check `criteria3.md` for state management and multi-query support
4. **Criteria 4 (Demo)**: Check `criteria4.md` for example queries and reporting

### Step 3: Verification Commands
Each criteria file contains:
- **Setup section** with parametrized student directory
- **Verification steps** with specific bash/grep commands
- **Quick checks** for rapid assessment
- **Common issues** to watch for

## 🎯 Key Requirements Summary

### Criteria 1: RAG Pipeline
✅ Notebook `Udaplay_01_*project.ipynb` exists  
✅ Loads and processes game JSON files  
✅ Persistent vector database (e.g., ChromaDB)  
✅ Demonstrates semantic search  

### Criteria 2: Agent Tools
✅ Retrieval tool (from vector DB)  
✅ Evaluation tool (quality assessment)  
✅ Web search tool (e.g., Tavily)  
✅ Workflow: internal → evaluate → web  

### Criteria 3: Stateful Agent
✅ Agent maintains conversation state  
✅ Handles multiple queries in session  
✅ State machine or workflow abstraction  
✅ Clear, cited responses  

### Criteria 4: Demonstration
✅ Notebook `Udaplay_02_*project.ipynb` exists  
✅ At least 3 example queries  
✅ Shows reasoning and tool usage  
✅ Includes citations where appropriate  

## 💡 Important Notes

### Flexibility in Implementation
- **DO NOT FAIL** if student uses different tools/libraries as long as functionality works
- Accept various vector DBs (ChromaDB, Pinecone, Weaviate, etc.)
- Accept different web search APIs (Tavily, Serper, Google, etc.)
- Accept different LLM frameworks (LangChain, LlamaIndex, custom, etc.)

### Common Acceptable Variations
- Simple state management is OK if documented and functional
- Different embedding models are acceptable
- Various workflow implementations (state machines, pipelines, etc.)
- Different output formats as long as requirements are met

## 🔍 Detailed Command Examples

### Check Specific Student
```bash
STUDENT_DIR="stu_52"

# Quick check for all notebooks
ls -la ${STUDENT_DIR}/*.ipynb

# Check for game files
find ${STUDENT_DIR} -name "*.json" -path "*/games/*" | wc -l

# Verify vector DB implementation
grep -c "chromadb\|ChromaDB" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check tool implementations
grep -c "@tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify state management
grep -c "state\|memory\|history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### Batch Review Multiple Students
```bash
for num in 49 50 51 52; do
    echo "Reviewing stu_$num..."
    ./review_all.sh $num > review_stu_$num.txt
done
```

## 📊 Output Interpretation

The review script provides:
- ✅ **PASS**: Requirement clearly met
- ❌ **FAIL**: Requirement not found (needs manual verification)
- ⚠️ **REVIEW NEEDED**: Automated check inconclusive

**Important**: Failed automated checks don't necessarily mean the student fails. Always:
1. Manually verify using detailed commands
2. Check for alternative implementations
3. Read the actual code/outputs
4. Consider the spirit of the requirement

## 🛠️ Troubleshooting

### If student uses different notebook names:
```bash
# List all notebooks
ls -la ${STUDENT_DIR}/*.ipynb

# Update search patterns accordingly
grep "pattern" ${STUDENT_DIR}/*project*.ipynb
```

### If tools are in separate files:
```bash
# Check library files
ls -la ${STUDENT_DIR}/lib/*.py
grep "@tool" ${STUDENT_DIR}/lib/*.py
```

### If using different vector DB:
```bash
# Check for other vector DBs
grep -i "pinecone\|weaviate\|qdrant\|faiss" ${STUDENT_DIR}/*.ipynb
```

## 📝 Final Checklist

Before approving/rejecting:
- [ ] Ran automated review script
- [ ] Checked detailed commands for any failures
- [ ] Verified alternative implementations accepted
- [ ] Confirmed notebooks have been executed (non-empty outputs)
- [ ] Checked for proper citations in responses
- [ ] Verified at least 3 example queries demonstrated
- [ ] Confirmed agent workflow order (internal → evaluate → web)
- [ ] Validated state persistence across queries

## 💬 Support

If you encounter issues or need clarification:
1. Check `reviewer_tip.md` for original rubric
2. Run specific commands from criteria files
3. Look for alternative implementations
4. Focus on functionality over specific tools/libraries

---

**Remember**: The goal is to assess whether students understand and can implement RAG pipelines and agentic systems, not whether they use specific tools or follow exact patterns.

