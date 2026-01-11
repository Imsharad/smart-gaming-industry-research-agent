# Common Mistakes and Best Practices

This document outlines common software development mistakes and best practices for avoiding them, based on a review of various code snippets.

### 1. Configuration and Data Consistency

*   **Mistake:** Mismatches between configuration references and their definitions. For example, a mapping that points to a template name that doesn't exist.
*   **Best Practice:** Implement tests to ensure that all references in your configuration are valid. The `test_template_file_mapping_consistency` function is a good example of this, ensuring that every key in `TEMPLATE_FILE_MAPPING` corresponds to a real template in `DOCUMENT_TEMPLATES`.

### 2. Data Handling and Validation

*   **Mistake:** Assuming input data is always well-formed. This can lead to crashes when data is missing fields or has unexpected structures.
*   **Best Practice:** Design data processing functions to be resilient to malformed input. The `test_convert_handles_missing_content_or_parts` test shows how to gracefully skip events that are missing `content` or `parts`, preventing the system from crashing and ensuring that valid data is still processed.

### 3. Database Query Optimization

*   **Mistake:** Failing to utilize database indexes, leading to slow queries. This can happen when query conditions don't match the index definition, for instance, due to differences in quoting or casing.
*   **Best Practice:** Write specific tests to verify that your query analysis logic correctly identifies when an index can be used. The tests `test_check_secondary_index_usage_with_quotes` and `test_check_secondary_index_usage_no_indexes` demonstrate checking for index usage, even with edge cases like quoted identifiers, and correctly identifying when no suitable index exists.

### 4. API and Callback Signatures

*   **Mistake:** Mismatched function signatures between API definitions, handlers, or callbacks. This can lead to runtime errors that are hard to debug.
*   **Best Practice:** Use static analysis and runtime checks to enforce correct function signatures. The `test_wrong_params_on_input_causes_error` test shows how to raise a `UserError` when a handoff function is registered with the wrong number of parameters, catching the error early.

### 5. Text and Data Parsing

*   **Mistake:** Brittle parsing logic that breaks with small variations in the input format.
*   **Best Practice:** Create robust parsing functions and test them against representative data. The `test_extract_props_markdown` function is an example of testing the extraction of structured data from a markdown file, ensuring the parser correctly identifies the required sections and content.

### 6. Algorithm and Logic Correctness

*   **Mistake:** Subtle bugs in algorithms, such as case-sensitivity issues in string comparisons.
*   **Best Practice:** Isolate algorithmic logic into pure functions and test them thoroughly. The `_find_common_terms` function, for example, correctly converts terms to lowercase before comparison to ensure a case-insensitive intersection.

### 7. CLI and Service Configuration

*   **Mistake:** Hardcoding configuration values like host, port, or logging levels, making services inflexible.
*   **Best Practice:** Expose configuration options through command-line arguments with sensible defaults. The `fast_api_common_options` decorator is a great example of how to provide a standard set of options for running a FastAPI service, making it easy to configure for different environments.

### 8. Reporting and Output Generation

*   **Mistake:** Generating reports that are difficult to consume or integrate with other tools.
*   **Best Practice:** Support multiple output formats (like Markdown, JSON, etc.) for generated reports. The `test_generate_markdown_report` test shows how to generate a report in a specific format (`markdown`), ensuring the output is structured and correct.
