# Criteria 1: RAG
**Prepare and process a local dataset of video game information for use in a vector database and RAG pipeline**

## Setup
```bash
# Set the student directory variable (replace X with actual student number)
STUDENT_DIR="stu_X"  # e.g., stu_51, stu_52, stu_49, etc.
```

## Requirements to Pass:

### 1. The submission includes the notebook ( Udaplay_01_solution_project.ipynb OR Udaplay_01_starter_project.ipynb OR Udaplay_02_solution_project.ipynb OR Udaplay_02_starter_project.ipynb) that loads, processes, and formats the provided game JSON files.

**Verification Steps:**

```bash
# Check if the required notebook exists
ls -la ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Search for JSON loading code patterns
grep -n "json.load\|pd.read_json\|json.loads" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check for game data directory references
grep -n "games\|data_dir\|game.*json" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Verify game JSON files exist
ls -la ${STUDENT_DIR}/games/*.json 2>/dev/null || ls -la ${STUDENT_DIR}/*/games/*.json 2>/dev/null

# Count number of game files
find ${STUDENT_DIR} -name "*.json" -path "*/games/*" | wc -l

# Check for data processing/formatting code
grep -n "DataFrame\|dict\|format\|process" ${STUDENT_DIR}/Udaplay_01_*project.ipynb | head -20

# Look for evidence of data structure creation
grep -n "metadata\|document\|content\|embedding" ${STUDENT_DIR}/Udaplay_01_*project.ipynb
```

### 2. The processed data is added to a persistent vector database (e.g., ChromaDB) with appropriate embeddings.

**Verification Steps:**

```bash
# Check for ChromaDB or other vector DB imports
grep -n "chromadb\|ChromaDB\|PersistentClient\|weaviate\|pinecone\|qdrant" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Verify persistent storage configuration
grep -n "persist_directory\|storage\|persistent\|PersistentClient" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check for actual ChromaDB database files
find ${STUDENT_DIR} -name "*.sqlite3" -o -name "chroma.sqlite3" 2>/dev/null
ls -la ${STUDENT_DIR}/chroma_db/ 2>/dev/null || ls -la ${STUDENT_DIR}/*/chroma_db/ 2>/dev/null

# Look for collection creation
grep -n "create_collection\|get_or_create_collection\|collection" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check for embedding model configuration
grep -n "embedding\|embed\|SentenceTransformer\|OpenAIEmbeddings\|HuggingFace" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Verify data insertion into vector DB
grep -n "add\|insert\|upsert\|add_documents" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check for document count verification
grep -n "count\|len\|collection.count\|total" ${STUDENT_DIR}/Udaplay_01_*project.ipynb
```

### 3. The notebook or script demonstrates that the vector database can be queried for semantic search.

**Verification Steps:**

```bash
# Check for query/search implementation
grep -n "query\|search\|retrieve\|similarity" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Look for specific query examples
grep -n "collection.query\|similarity_search\|search(" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check for query results handling
grep -n "results\|distances\|documents\|metadatas" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Search for actual game-related queries (examples)
grep -i "racing\|rpg\|playstation\|nintendo\|xbox\|genre\|platform" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Verify output cells have results (non-empty outputs)
grep -A5 '"output_type":' ${STUDENT_DIR}/Udaplay_01_*project.ipynb | grep -v "outputs.*[]"

# Check for query result display/printing
grep -n "print.*result\|display\|pprint\|for.*in.*results" ${STUDENT_DIR}/Udaplay_01_*project.ipynb
```

## Additional Verification Commands:

```bash
# Check overall notebook structure and execution
# Count total code cells
grep -c '"cell_type": "code"' ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Check if notebook has been executed (has outputs)
grep -c '"outputs": \[' ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Verify imports are present
grep -n "^import\|^from" ${STUDENT_DIR}/Udaplay_01_*project.ipynb | head -20

# Check for error outputs that might indicate issues
grep -i "error\|exception\|traceback" ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# Look for documentation/markdown cells explaining the process
grep -c '"cell_type": "markdown"' ${STUDENT_DIR}/Udaplay_01_*project.ipynb
```

## Quick Full Pipeline Check:

```bash
# One-liner to check all key components
echo "=== Checking ${STUDENT_DIR} ===" && \
echo "Notebook exists: $(ls ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null | wc -l)" && \
echo "Game files: $(find ${STUDENT_DIR} -name "*.json" -path "*/games/*" 2>/dev/null | wc -l)" && \
echo "ChromaDB refs: $(grep -c "chromadb\|ChromaDB" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)" && \
echo "Query calls: $(grep -c "query\|search" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)" && \
echo "Persist dir: $(grep -c "persist_directory" ${STUDENT_DIR}/Udaplay_01_*project.ipynb 2>/dev/null)" && \
echo "DB files: $(find ${STUDENT_DIR} -name "*.sqlite3" 2>/dev/null | wc -l)"
```

## Reviewer Tips:

- **Confirm** that the data loading and processing steps are present and correct using the commands above
- **Check** that the vector database is persistently created and populated with the game data
- **Ensure** that at least one semantic search query is demonstrated and returns relevant results
- **IMPORTANT:** Do NOT fail if the student uses a different embedding model or vector DB, as long as the pipeline works

## What to Look For:

- **Evidence of successful data loading:** Check notebook outputs for confirmation messages, data counts, or sample entries
- **Vector database verification:** The vector database collection should show populated documents
- **Semantic search validation:** Queries should return meaningful, relevant results with proper document metadata
- **Data processing:** Look for proper formatting and structuring of the game JSON data before insertion into the vector DB

## Common Issues to Check:

```bash
# Missing game files
[ -d "${STUDENT_DIR}/games" ] || echo "WARNING: games directory not found"

# Empty outputs (notebook not executed)
grep -c '"outputs": \[]' ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# No persistence directory specified
grep -c "persist" ${STUDENT_DIR}/Udaplay_01_*project.ipynb || echo "WARNING: No persistence configuration found"

# Missing collection verification
grep -c "collection.count\|collection.peek" ${STUDENT_DIR}/Udaplay_01_*project.ipynb || echo "WARNING: No collection verification"
```

## Additional Learning Resources:

### Essential Reading - Vector Databases and RAG Pipelines

**ChromaDB and RAG Implementation:**
- [Ultimate Guide to Chroma Vector Database: Everything You Need to Know – Part 1](https://mlexplained.blog/2024/04/09/ultimate-guide-to-chroma-vector-database-everything-you-need-to-know-part-1/) - Comprehensive 2024 guide covering ChromaDB setup, configuration, and best practices
- [Embeddings and Vector Databases With ChromaDB – Real Python](https://realpython.com/chromadb-vector-database/) - Step-by-step tutorial with practical Python examples
- [How to Implement RAG with ChromaDB and Ollama: A Python Guide for Beginners](https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0) - Beginner-friendly implementation guide
- [Learn How to Use Chroma DB: A Step-by-Step Guide | DataCamp](https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide) - Interactive tutorial with hands-on exercises

**Semantic Search and Vector Databases:**
- [Semantic Search with Vector Databases - KDnuggets](https://www.kdnuggets.com/semantic-search-with-vector-databases) - Hands-on Python implementation with practical examples
- [Vector Databases: Building a Semantic Search Engine — A Practical Guide](https://medium.com/@amdj3dax/building-a-semantic-search-engine-with-vector-databases-a-practical-guide-4829fc934e53) - Complete implementation using FastAPI, Pinecone, and Sentence Transformers
- [Implementing Semantic Search with Vector database - GeeksforGeeks](https://www.geeksforgeeks.org/data-science/implementing-semantic-search-with-vector-database/) - Theory and practical applications covered
- [Semantic Search 101 - Qdrant](https://qdrant.tech/documentation/beginner-tutorials/search-beginners/) - 5-minute tutorial for science fiction books search engine

**RAG Implementation with LangChain:**
- [Build a Retrieval Augmented Generation (RAG) App: Part 1 | LangChain](https://python.langchain.com/docs/tutorials/rag/) - Official LangChain RAG tutorial with minimal implementation
- [Retrieval-Augmented Generation (RAG): From Theory to LangChain Implementation](https://www.leoniemonigatti.com/blog/retrieval-augmented-generation-langchain.html) - Theory to implementation guide
- [Retrieval-Augmented Generation (RAG) using LangChain, LlamaIndex, and OpenAI](https://pub.towardsai.net/introduction-to-retrieval-augmented-generation-rag-using-langchain-and-lamaindex-bd0047628e2a) - Multi-framework comparison
- [Building RAG from Scratch (Open-source only!) - LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/low_level/oss_ingestion_retrieval/) - Open-source implementation guide

**Production RAG Systems:**
- [Optimizing RAG: A Guide to Choosing the Right Vector Database](https://medium.com/@mutahar789/optimizing-rag-a-guide-to-choosing-the-right-vector-database-480f71a33139) - Database selection criteria and optimization strategies
- [Building Production-Ready RAG Systems: Best Practices and Latest Tools](https://medium.com/@meeran03/building-production-ready-rag-systems-best-practices-and-latest-tools-581cae9518e7) - Enterprise deployment considerations
- [Architecting for Scale: Evaluating Vector Database Options for Production RAG Systems](https://ragaboutit.com/architecting-for-scale-evaluating-vector-database-options-for-production-rag-systems/) - Scalability and architecture guidance
- [Best Practices for Production-Scale RAG Systems — An Implementation Guide](https://orkes.io/blog/rag-best-practices/) - Production deployment best practices