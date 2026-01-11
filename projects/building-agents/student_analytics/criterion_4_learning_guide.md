# Mastering Agent Verification: A Visual Learning Guide
> **Focus**: Overcoming common challenges in Demonstration and Reporting.

Here are the key concepts for proving your agent works, explained with visual metaphors.

## 1. The "Invisible Ink" (Missing Outputs)

### The Common Pitfall
Submitting a notebook where the cells have been reset. The code is there, but the output areas are blank. The reviewer sees `In [ ]: ...` instead of the agent's actual response.

### Visual Metaphor
> **Sending a polaroid photo that hasn't developed yet.**
> You claim the picture is of a sunset, but the reviewer just sees a black square. You must "develop" (execute) the photo before mailing it.

### The Concept: Evidence
Code reviews grade **evidence of execution**, not just syntax.
- **Rule**: If the output isn't preserved in the file, it didn't happen.
- **Action**: "Cell" > "Run All" > "File" > "Save".

---

## 2. The "Movie Trailer" (Insufficient Queries)

### The Common Pitfall
Running usage only once. You ask "What is Mario?", it works, and you submit. The rubric requires **at least three** diverse queries to prove the agent isn't a "hardcoded lucky guess".

### Visual Metaphor
> **A movie trailer that only shows one good scene.**
> The audience suspects the rest of the movie is bad. To prove consistency, you need to show the beginning, middle, and end.

### The Concept: Generalization
One data point is an anecdote. Three is a pattern.
- **Requirement**: Run 3 distinct types of queries (e.g., one simple fact, one comparison, one opinion/evaluation).

---

## 3. The "Black Box" (Hidden Reasoning)

### The Common Pitfall
The agent prints the final answer "Mario was released in 1985" but hides *how* it got there. Did it guess? Did it use the tool? Did it hallucinate?

### Visual Metaphor
> **Showing your work in math class.**
> If you just write "X = 5", the teacher marks it wrong. They need to see the steps: "X + 2 = 7 -> X = 5".

### The Concept: Explainability
Transparency is critical for AI.
- **Requirement**: Configure your agent to print `verbose=True` or log steps: "Using Tool 'Search'...", "Tool Output: '...'", "Final Answer: ...".

---

## 4. The "Plagiarist" (Missing Citations)

### The Common Pitfall
The agent gives a perfect answer but doesn't say where it found the info. Did it come from the vector DB? The web? Training data?

### Visual Metaphor
> **Writing a research paper with no bibliography.**
> It looks professional, but it fails academic standards.

### The Concept: Attribution
Agents must cite sources to be trusted.
- **Fix**: Prompt the agent: "Always include the source URL or document name in your final answer."

---

## Summary Checklist for Verification Success
1.  **Run All**: Ensure every cell has an output number `In [5]:`.
2.  **Rule of Three**: Show 3 distinct examples (Fact, Comparison, Complex).
3.  **Show Work**: Print the tool inputs/outputs (the "thought process").
4.  **Cite Sources**: Ensure final answers say "Source: [Title]".
