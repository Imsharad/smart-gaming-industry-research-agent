Hello José,

You are spot on with your suspicion! The issue is indeed related to the `voc-` key.

**The Explanation:**
Keys starting with `voc-` are specific to the Udacity/Vocareum classroom environment. Unlike standard OpenAI keys (`sk-`) that connect directly to `api.openai.com`, these `voc-` keys require a specific **proxy URL** (API Base) to function. By default, the `OpenAIEmbeddingFunction` tries to connect to the main OpenAI servers, which reject your classroom key.

**The Fix:**
You need to explicitly tell the embedding function to use the Udacity proxy. This URL is usually stored in the `OPENAI_API_BASE` environment variable in your classroom.

Update your code in the notebook to include the `api_base` parameter:

```python
embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_API_BASE") # This directs the request to the correct proxy
)
```

**Heads Up for Part 2:**
I noticed the `llm.py` file you might be using for the second part of the project (the Agent) also creates an `OpenAI` client. You might run into the same issue there. If you do, make sure to update the `LLM` class in `lib/llm.py` to also use the `base_url`:

```python
# In lib/llm.py
import os 

# ... inside __init__ ...
base_url = os.getenv("OPENAI_API_BASE")
self.client = OpenAI(api_key=api_key, base_url=base_url) if api_key else OpenAI(base_url=base_url)
```

Good luck with the project!

Best regards,
Gemini CLI Agent