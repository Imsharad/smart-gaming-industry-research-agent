# Criteria 1: RAG

**Prepare and process a local dataset of video game information for use in a vector database and RAG pipeline**

## Setup

```bash
# Set the student directory variable (replace X with actual student number)
STUDENT_DIR="stu_X"  # e.g., stu_51, stu_52, stu_49, etc.
```

## Requirements to Pass:

### 1. The submission includes the notebook (Udaplay_01_solution_project.ipynb) that loads, processes, and formats the provided game JSON files.

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
grep -A5 '"output_type":' ${STUDENT_DIR}/Udaplay_01_*project.ipynb | grep -v "outputs.*\[\]"

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
grep -c '"outputs": \[\]' ${STUDENT_DIR}/Udaplay_01_*project.ipynb

# No persistence directory specified
grep -c "persist" ${STUDENT_DIR}/Udaplay_01_*project.ipynb || echo "WARNING: No persistence configuration found"

# Missing collection verification
grep -c "collection.count\|collection.peek" ${STUDENT_DIR}/Udaplay_01_*project.ipynb || echo "WARNING: No collection verification"
```

Add these resources at the end while gnerating the feedback/1.md file :
Resources

Core RAG Concepts
https://ai.meta.com/blog/retrieval-augmented-generation-streamlining-the-creation-of-intelligent-natural-language-processing-models/
Retrieval-Augmented Generation (Meta AI) - The original blog post from Meta AI that introduced the RAG framework. This is an essential read for understanding the "why" behind this powerful architecture.

https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/

LlamaIndex Ingestion Pipeline - A comprehensive guide from a leading RAG framework on the entire data ingestion process, including loading, chunking, and embedding text, which are critical first steps in any RAG system.

Vector Databases and Embeddings

https://docs.trychroma.com/docs/overview/introduction

ChromaDB Documentation - The official documentation for ChromaDB, a popular open-source vector database. It provides a practical guide on how to get started with storing and querying embedding data.
Sentence-Transformers Documentation - The official documentation for a foundational Python library used to easily create state-of-the-art text and image embeddings. This is a go-to resource for selecting and using embedding models.

## External Resources

Add these curated resources at the end when generating the feedback/1.md file:

### Core RAG Concepts & Architecture

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Original Paper)**
https://arxiv.org/abs/2005.11401
The foundational research paper that introduced RAG. Essential for understanding the theoretical underpinnings and architectural decisions behind RAG systems.

**Building RAG Systems: The Definitive Guide**
https://docs.llamaindex.ai/en/stable/getting_started/concepts/
LlamaIndex's comprehensive guide covering RAG fundamentals, implementation patterns, and common pitfalls. Excellent practical resource for building production RAG systems.

**Advanced RAG Techniques**
https://python.langchain.com/docs/use_cases/question_answering/
LangChain's deep dive into advanced RAG patterns including multi-query retrieval, contextual compression, and retrieval evaluation techniques.

### Vector Databases & Embeddings

**ChromaDB: Getting Started Guide**
https://docs.trychroma.com/docs/overview/introduction
Official ChromaDB documentation with practical examples for storing and querying embeddings. Perfect for understanding vector database operations.

**Understanding Vector Databases**
https://www.pinecone.io/learn/vector-database/
Comprehensive guide to vector database concepts, indexing algorithms, and similarity search. Great for understanding the "why" behind vector storage decisions.

**Embedding Models Deep Dive**
https://www.sbert.net/docs/pretrained_models.html
Sentence-Transformers model selection guide. Critical for choosing appropriate embedding models for different domains and use cases.

### Data Processing & Chunking Strategies

**Chunking Strategies for RAG**
https://python.langchain.com/docs/guides/evaluation/
LangChain's analysis of different text chunking approaches and their impact on RAG performance. Essential for optimizing retrieval quality.

**Text Preprocessing for Vector Search**
https://weaviate.io/blog/chunking-strategies-langchain
Weaviate's guide to preprocessing techniques that improve embedding quality and retrieval accuracy.

### Performance & Evaluation

**Evaluating RAG Systems**
https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
LlamaIndex's framework for systematically evaluating RAG system performance, including metrics and benchmarking approaches.

**RAG Performance Optimization**
https://python.langchain.com/docs/use_cases/question_answering/how_to/local_retrieval_qa
LangChain's guide to optimizing RAG systems for speed and accuracy, including local deployment strategies.

### Data Processing & Chunking Strategies

**Chunking Strategies for RAG**
https://python.langchain.com/docs/guides/evaluation/
LangChain's analysis of different text chunking approaches and their impact on RAG performance. Essential for optimizing retrieval quality.

**Chunking Strategies for RAG**
https://www.pinecone.io/learn/chunking-strategies/
A comprehensive guide to chunking strategies from Pinecone, a leading vector database provider.

### Performance & Evaluation

**Evaluating RAG Systems**
https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
LlamaIndex's framework for systematically evaluating RAG system performance, including metrics and benchmarking approaches.

**RAG Performance Optimization**

https://python.langchain.com/docs/use_cases/question_answering/how_to/local_retrieval_qa

LangChain's guide to optimizing RAG systems for speed and accuracy, including local deployment strategies.

## Further Reading

### High-Authority Sources from Leading AI Companies

**OpenAI: Retrieval-Augmented Generation Best Practices**
https://platform.openai.com/docs/guides/embeddings
OpenAI's official guide to embeddings and retrieval systems, covering best practices for implementing RAG with their embedding models and APIs. Essential for understanding enterprise-scale RAG implementations.

**Anthropic: Contextual Retrieval Techniques**
https://www.anthropic.com/news/contextual-retrieval
Anthropic's advanced contextual retrieval methodology that improves RAG accuracy by up to 67%. Includes novel techniques for chunk preprocessing and context embedding that significantly enhance retrieval quality.

**Google AI: Vector Search and Embeddings**
https://cloud.google.com/vertex-ai/docs/vector-search/overview
Google's comprehensive guide to vector search architecture, covering scalable embedding storage, similarity search algorithms, and production deployment patterns for enterprise RAG systems.

### Core RAG Concepts & Architecture

**Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Original Paper)**
https://arxiv.org/abs/2005.11401
The foundational research paper from Meta AI that introduced RAG. Essential for understanding the theoretical underpinnings and architectural decisions behind modern retrieval-augmented systems.

**Building Production RAG Systems**
https://docs.llamaindex.ai/en/stable/getting_started/concepts/
LlamaIndex's comprehensive guide covering RAG fundamentals, implementation patterns, and production deployment strategies. Includes advanced topics like hybrid search and multi-modal RAG.

**Advanced RAG Techniques and Patterns**
https://python.langchain.com/docs/use_cases/question_answering/
LangChain's deep dive into advanced RAG patterns including multi-query retrieval, contextual compression, and retrieval evaluation techniques for production systems.

### Vector Databases & Embeddings

**ChromaDB: Production Vector Database Guide**
https://docs.trychroma.com/docs/overview/introduction
Official ChromaDB documentation with practical examples for storing and querying embeddings at scale. Covers performance optimization, persistence, and deployment patterns.

**Pinecone: Vector Database Architecture**
https://www.pinecone.io/learn/vector-database/
Comprehensive guide to vector database concepts, indexing algorithms, and similarity search optimization. Essential for understanding scalable vector storage decisions.

**Sentence-Transformers: Embedding Model Selection**
https://www.sbert.net/docs/pretrained_models.html
Official guide to selecting and fine-tuning embedding models. Critical for choosing appropriate models for different domains and optimizing retrieval performance.

### Data Processing & Chunking Strategies

**LangChain: Document Processing Pipeline**
https://python.langchain.com/docs/how_to/document_loaders/
Comprehensive guide to document loading, chunking strategies, and preprocessing techniques that directly impact RAG system performance.

**Weaviate: Chunking Strategies for Production RAG**
https://weaviate.io/blog/chunking-strategies-langchain
Data science approach to chunking strategies with empirical analysis of different techniques and their impact on retrieval accuracy.

### Performance & Evaluation

**LlamaIndex: RAG Evaluation Framework**
https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
Systematic framework for evaluating RAG systems including faithfulness, answer relevance, and context precision metrics with practical implementation examples.

**Microsoft Research: RAG Evaluation Metrics**
https://www.microsoft.com/en-us/research/blog/rag-evaluation-metrics/
Microsoft's research-backed approach to RAG evaluation including novel metrics and benchmarking methodologies for production systems.

### Enterprise Implementation Guides

**AWS: Building RAG Applications with Amazon Bedrock**
https://aws.amazon.com/blogs/machine-learning/retrieval-augmented-generation-with-amazon-bedrock/
AWS's comprehensive guide to building production RAG applications using managed AI services, including cost optimization and scalability patterns.

**Azure: RAG with Azure AI Search**
https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
Microsoft's guide to implementing RAG within the Azure ecosystem, covering integration patterns with Azure OpenAI Service and cognitive search.

**Google Cloud: Vertex AI Vector Search**
https://cloud.google.com/vertex-ai/docs/matching-engine/overview
Google's guide to building scalable RAG systems with Vertex AI, including vector indexing, approximate nearest neighbor search, and multi-modal retrieval.

### Advanced Research & Techniques

**GraphRAG: Knowledge Graph Enhanced Retrieval**
https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
Microsoft Research's GraphRAG methodology that combines knowledge graphs with traditional RAG for enhanced reasoning over complex, interconnected information.

**Multi-Modal RAG Systems**
https://arxiv.org/abs/2308.07107
Cutting-edge research on RAG systems that handle text, images, and structured data simultaneously, representing the future of retrieval-augmented AI systems.

## MANDATORY: External Resources

When generating feedback/1.md, you MUST:

1. Read /criteria_prompts/external_links.md
2. Navigate to "## Criterion 1: RAG Pipeline" section
3. Use ONLY links from that section (include all relevant links that support comprehensive learning)
4. Copy URLs exactly - do NOT modify or generate new ones
5. Contextualize each link to the student's specific work with detailed explanations

FORBIDDEN ACTIONS:

- Using links from your training data or knowledge
- Generating URLs based on what "seems" correct
- Using web search to find alternative resources
- Modifying URLs from external_links.md




Paste these EXACT external Image URLs AS IT IS :


![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766580720/image.png)
