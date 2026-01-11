# Action Items for Next Submission

All criteria require attention. Please address the following prioritized checklist to ensure your next submission passes.

### Must Fix (Priority Order):

- [ ] **Criterion 1 (Critical Implementation)**: Fix the `InternalError` in `Udaplay_01_starter_project.ipynb` by changing `create_collection` to `get_or_create_collection`. Ensure the `collection` variable is defined so data loading can proceed. Add a cell to demonstrate a simple query.
- [ ] **Criterion 2 (Tool Logic)**: Implement the actual logic for `evaluate_retrieval` in `Udaplay_02_starter_project.ipynb`. It currently contains placeholder code that calls another tool. It must use an LLM to judge the quality of retrieved docs.
- [ ] **Criterion 4 (Demonstration)**: Run the agent on at least **three different queries** in `Udaplay_02_starter_project.ipynb`. The current submission only shows one.
- [ ] **Criterion 3 (Verification)**: Ensure your multiple queries (from the step above) demonstrate that the agent remembers context (e.g., ask a follow-up question like "Who made it?").

### Quick Reference:

| Criterion | Status | File/Location                              | Key Issue |
| --------- | ------ | ------------------------------------------ | --------- |
| 1         | FAIL   | `Udaplay_01_starter_project.ipynb` | `create_collection` crash & missing query |
| 2         | FAIL   | `Udaplay_02_starter_project.ipynb` | `evaluate_retrieval` tool is a placeholder |
| 3         | FAIL   | `Udaplay_02_starter_project.ipynb` | Only 1 query run; no state proof |
| 4         | FAIL   | `Udaplay_02_starter_project.ipynb` | Less than 3 example queries |

### Estimated Effort: ~2-3 hours of focused work
- **1 hour** to fix the Notebook 1 pipeline and database persistence.
- **1 hour** to properly implement the Evaluation tool logic.
- **30 mins** to run the final demonstrations and verify outputs.
