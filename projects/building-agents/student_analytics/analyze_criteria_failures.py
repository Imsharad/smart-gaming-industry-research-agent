import os
import re
from collections import defaultdict, Counter

FAILURES_LIST = "./failures_list.txt"
OUTPUT_FILE = "./criteria_failures_report.md"

def analyze_failures():
    print("Reading failure list...")
    try:
        with open(FAILURES_LIST, "r") as f:
            file_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("failures_list.txt not found.")
        return

    criteria_stats = defaultdict(list)
    
    # Keywords indicating a failure reason
    FAILURE_KEYWORDS = [
        "missing", "however", "fails to", "not implemented", "incorrect", 
        "required", "error", "unable to", "issue", "problem", "absent",
        "does not", "didn't", "forgot"
    ]

    print(f"Processing {len(file_list)} files...")
    
    for fb_path in file_list:
        if "summary.md" in fb_path:
            continue

        filename = os.path.basename(fb_path)
        crit_match = re.search(r"(\d+)", filename)
        if not crit_match:
            continue
        crit_id = crit_match.group(1)
        
        try:
            with open(fb_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Only process if FAIL
            if not re.search(r"Status:.*(?:FAIL|NOT MET)", content, re.IGNORECASE):
                continue
            
            # Heuristic extraction
            reasons = []
            
            # 1. Look for "However, ..." block
            however_match = re.search(r"However,?\s*(.*?)(?=\n\n|\Z)", content, re.DOTALL)
            if however_match:
                reasons.append(however_match.group(1).strip().replace('\n', ' '))
            
            # 2. Look for lines with failure keywords (bullet points or sentences)
            lines = content.split('\n')
            for line in lines:
                line_lower = line.lower()
                clean_line = line.strip().strip('*').strip('-').strip('•').strip()
                if not clean_line:
                    continue
                
                # Check for keywords
                if any(kw in line_lower for kw in FAILURE_KEYWORDS):
                    # Filter out questions or distinct headers
                    if '?' in line or line.startswith('#'):
                        continue
                    if len(clean_line) > 10 and len(clean_line) < 300:
                         reasons.append(clean_line)

            # 3. Look for explicit "Issue" fields
            action_items = re.findall(r"\*\*Issue\*\*:\s*(.*?)(?=\*\*)", content)
            if action_items:
                 reasons.extend([i.strip() for i in action_items])

            # Dedupe reasoning for this file
            unique_reasons = list(set(reasons))
            
            # If nothing found, try capturing text after Status: FAIL
            if not unique_reasons:
                 fail_match = re.search(r"Status:\s*FAIL\s*(.*?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
                 if fail_match:
                     text = fail_match.group(1).strip()
                     if text:
                        unique_reasons.append(text.split('\n')[0][:200])

            if unique_reasons:
                criteria_stats[crit_id].extend(unique_reasons)

        except Exception as e:
            print(f"Error reading {fb_path}: {e}")

    # Generate Report
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Analysis of Failure Reasons by Criterion\n\n")
        
        sorted_ids = sorted(criteria_stats.keys(), key=lambda x: int(x) if x.isdigit() else 999)
        
        for crit_id in sorted_ids:
            issues = criteria_stats[crit_id]
            out.write(f"## Criterion {crit_id} ({len(issues)} issues extracted)\n\n")
            
            # Simple clustering/normalization
            normalized = []
            for i in issues:
                # Truncate and lower for grouping
                # Removing common prefixes
                clean = i.lower()
                clean = re.sub(r"^(however,?\s*)", "", clean)
                clean = re.sub(r"^(missing\s*)", "missing ", clean)
                
                # Map to categories for Criterion 1 specifically (RAG)
                if crit_id == "1":
                    if "semantic" in clean or "query" in clean:
                        normalized.append("Missing Semantic Search/Query Demo")
                    elif "data" in clean and ("load" in clean or "file" in clean):
                        normalized.append("Data Loading/Processing Issue")
                    elif "chunk" in clean:
                         normalized.append("Chunking Strategy Issue")
                    elif "vector" in clean or "db" in clean or "chroma" in clean:
                         normalized.append("Vector DB Persistence/Setup Issue")
                    elif "notebook" in clean or "cell" in clean:
                         normalized.append("Notebook Execution/Structure Issue")
                    else:
                        normalized.append(i[:100] + "...")
                elif crit_id == "2":
                    if "retrieval" in clean or "evaluate" in clean or "tool" in clean:
                         normalized.append("Missing/Incorrect Tool Implementation")
                    elif "workflow" in clean or "state" in clean:
                         normalized.append("Agentic Workflow/State Issue")
                    elif "fallback" in clean or "web" in clean:
                         normalized.append("Missing Fallback Logic")
                    elif "constraint" in clean or "check" in clean:
                         normalized.append("Missing Validation/Constraints")
                    else:
                         normalized.append(i[:100] + "...")
                elif crit_id == "3":
                    if "state" in clean and ("machine" in clean or "management" in clean or "maintain" in clean):
                        normalized.append("Missing State Management/Machine")
                    elif "history" in clean or "memory" in clean or "context" in clean or "conversation" in clean:
                        normalized.append("Missing Conversation History/Memory")
                    elif "class" in clean or "function" in clean:
                        normalized.append("Improper Agent Structure (Class/Function)")
                    elif "multiple" in clean and "query" in clean:
                        normalized.append("Fails Multiple Query Test")
                    else:
                        normalized.append(i[:100] + "...")
                elif crit_id == "4":
                    if "three" in clean or "3" in clean and ("query" in clean or "example" in clean):
                        normalized.append("Fewer than 3 Queries Demonstrated")
                    elif "reasoning" in clean or "tool" in clean and "visible" in clean:
                        normalized.append("Missing Reasoning/Tool Usage in Output")
                    elif "citation" in clean or "source" in clean:
                        normalized.append("Missing Sources/Citations")
                    elif "notebook" in clean or "output" in clean:
                        normalized.append("Missing Notebook Outputs")
                    else:
                        normalized.append(i[:100] + "...")
                else:
                     normalized.append(i[:100] + "...")
            
            c = Counter(normalized)
            for reason, freq in c.most_common(10):
                out.write(f"- **({freq})** {reason}\n")
            out.write("\n")

    print(f"Done. Report written to {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_failures()
