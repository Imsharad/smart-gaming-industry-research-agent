#!/usr/bin/env python3
"""
Visual Anti-Patterns Guide Generator

This script processes student feedback files and generates a rich, 
infographic-ready markdown document for LLM slide generation.
"""

import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional

OUTPUT_FILE = "./visual_antipatterns_guide.md"
FAILURES_LIST = "./failures_list.txt"

# Define anti-pattern categories with visual metadata
ANTIPATTERN_CATEGORIES = {
    "string_matching": {
        "title": "🔤 String Matching Pitfalls",
        "icon": "⚠️",
        "color": "red",
        "description": "Logic errors where substring matching causes false positives/negatives",
        "keywords": ["substring", "in ", "contains", "COMPAT", "matching", "parsing logic"]
    },
    "missing_documentation": {
        "title": "📝 Missing Documentation",
        "icon": "📋",
        "color": "orange",
        "description": "Tool docstrings lacking critical information for LLM understanding",
        "keywords": ["docstring", "documentation", "missing", "placeholder", "fill in", "date format", "YYYY-MM-DD"]
    },
    "output_format_mismatch": {
        "title": "📤 Output Format Mismatch",
        "icon": "🔀",
        "color": "yellow",
        "description": "Response formats that don't match downstream parser expectations",
        "keywords": ["format", "output", "IS_COMPATIBLE", "mismatch", "parser", "JSON", "Pydantic", "validation error"]
    },
    "hallucination_triggers": {
        "title": "🌫️ Hallucination Triggers",
        "icon": "👻",
        "color": "purple",
        "description": "Prompt patterns that cause LLMs to generate fictional data",
        "keywords": ["hallucinate", "placeholder", "fictional", "doesn't exist", "made up", "invented", "fake"]
    },
    "incomplete_react_cycle": {
        "title": "🔄 Incomplete ReAct Cycle",
        "icon": "🔁",
        "color": "blue",
        "description": "Missing THINK-ACT-OBSERVE components in agent prompts",
        "keywords": ["ReAct", "THINK", "ACT", "OBSERVE", "cycle", "tool", "parameter", "argument", "schema", "exit"]
    },
    "missing_constraints": {
        "title": "🚧 Missing Constraints",
        "icon": "🛑",
        "color": "gray",
        "description": "Prompts lacking explicit boundaries or validation rules",
        "keywords": ["constraint", "validation", "boundary", "explicit", "requirement", "backup", "alternative", "contingency", "option"]
    },
    "role_definition": {
        "title": "🎭 Role Definition Issues",
        "icon": "🎭",
        "color": "teal",
        "description": "Missing or unclear role instructions for the LLM agent",
        "keywords": ["role", "identity", "persona", "analyst", "expert", "agent"]
    },
    "chain_of_thought": {
        "title": "🧠 Chain-of-Thought Gaps",
        "icon": "🧠",
        "color": "pink",
        "description": "Missing step-by-step reasoning guidance in prompts",
        "keywords": ["chain-of-thought", "reasoning", "step-by-step", "analysis", "think through", "CoT"]
    }
}


@dataclass
class AntiPattern:
    """Represents a single anti-pattern instance"""
    category: str
    title: str
    description: str
    bad_code: Optional[str] = None
    good_code: Optional[str] = None
    why_fails: str = ""
    frequency: int = 0
    students: List[str] = field(default_factory=list)
    criterion: str = ""

def categorize_issue(issue_text: str, full_text: str) -> str:
    """Categorize an issue based on keywords"""
    combined = (issue_text + " " + full_text).lower()
    
    for cat_id, cat_info in ANTIPATTERN_CATEGORIES.items():
        for keyword in cat_info["keywords"]:
            if keyword.lower() in combined:
                return cat_id
    
    return "other"

def extract_code_blocks(text: str) -> List[str]:
    """Extract all code blocks from text"""
    return re.findall(r"```[\w]*\n?(.*?)```", text, re.DOTALL)

def generate_fix_suggestion(category: str, bad_code: str) -> str:
    """Generate a suggested fix based on category"""
    fixes = {
        "string_matching": '''```python
# ✅ CORRECT: Check for negative case first
if "INCOMPAT" in normalized_resp:
    is_compatible = False
elif "COMPAT" in normalized_resp:
    is_compatible = True

# ✅ BETTER: Use exact matching
if normalized_resp == "IS_COMPATIBLE":
    is_compatible = True
elif normalized_resp == "IS_INCOMPATIBLE":
    is_compatible = False
```''',
        "missing_documentation": '''```python
# ✅ CORRECT: Comprehensive docstring with format specification
def get_activities_by_date_tool(date: str, city: str) -> List[Activity]:
    """Retrieves available activities for a specific date and city.
    
    Args:
        date (str): Target date in YYYY-MM-DD format (e.g., "2025-06-12")
        city (str): City name (e.g., "AgentsVille")
    
    Returns:
        List[Activity]: Available activities matching criteria
    
    Example:
        >>> get_activities_by_date_tool("2025-06-12", "AgentsVille")
        [Activity(id="A001", name="Museum Tour", ...)]
    """
```''',
        "output_format_mismatch": '''```yaml
# ✅ CORRECT: Match the exact expected format from rubric
OUTPUT_FORMAT:
  - Use "IS_COMPATIBLE" (not "COMPATIBLE")
  - Use "IS_INCOMPATIBLE" (not "INCOMPATIBLE")
  
EXAMPLES:
  - Input: "Outdoor hiking" + "Heavy Rain"
    Output: "IS_INCOMPATIBLE: Heavy rain makes trails dangerous"
```''',
        "incomplete_react_cycle": '''```python
# ✅ CORRECT: Complete ReAct prompt with all components
ITINERARY_REVISION_AGENT_SYSTEM_PROMPT = """
You are an expert travel planner. Follow the THINK-ACT-OBSERVE cycle:

## Available Tools (with parameter schemas)
- get_activities_by_date_tool(date: str, city: str): Get activities
  - date: Date in YYYY-MM-DD format
  - city: City name string
- run_evals_tool(travel_plan: TravelPlan, info: VacationInfo): Validate plan
- final_answer_tool(answer: str): Submit final answer and EXIT

## Workflow
1. THINK: Analyze what needs to be done
2. ACT: Call a tool with proper JSON: {"tool_name": "...", "arguments": {...}}
3. OBSERVE: Review the result
4. Repeat until ready, then call final_answer_tool to EXIT
"""
```''',
        "missing_constraints": '''```python
# ✅ CORRECT: Include backup options in weather compatibility prompt
WEATHER_COMPATIBILITY_PROMPT = """
## Task
- Report IS_COMPATIBLE if weather allows the activity
- Report IS_INCOMPATIBLE if weather prevents the activity
- Consider backup options: Can the activity move indoors?
- Consider alternatives: Are there covered areas available?

## Decision Criteria
- Indoor activities: Generally IS_COMPATIBLE
- Outdoor with backup: Consider the backup option
- Outdoor-only in bad weather: IS_INCOMPATIBLE
"""
```''',
        "role_definition": '''```python
# ✅ CORRECT: Clear role definition with responsibilities
SYSTEM_PROMPT = """
You are an expert travel planning agent specializing in outdoor activities.

Your responsibilities:
1. Create weather-appropriate itineraries
2. Ensure budget compliance
3. Maximize activity variety
4. Consider traveler preferences

Your expertise includes: activity scheduling, weather analysis, backup planning.
"""
```''',
        "chain_of_thought": '''```python
# ✅ CORRECT: Explicit Chain-of-Thought guidance
PROMPT = """
## Analysis Process (follow these steps)
1. First, review all available activities and their requirements
2. Then, check weather conditions for each date
3. Next, filter activities by weather compatibility
4. Finally, select activities that maximize variety while staying in budget

Show your reasoning at each step before making decisions.
"""
```'''
    }
    return fixes.get(category, "")


def process_failures() -> Dict[str, List[AntiPattern]]:
    """Process all failure files and extract anti-patterns"""
    
    patterns_by_category: Dict[str, List[AntiPattern]] = defaultdict(list)
    issue_tracker: Dict[str, AntiPattern] = {}  # Dedupe by issue text
    
    print("Reading failure list...")
    try:
        with open(FAILURES_LIST, "r") as f:
            file_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("failures_list.txt not found.")
        return {}
    
    print(f"Processing {len(file_list)} files...")
    processed = 0
    
    for fb_path in file_list:
        if "summary.md" in fb_path or "criteria_prompts" in fb_path:
            continue
            
        # Extract metadata from path
        stu_match = re.search(r"(stu_\d+)", fb_path)
        stu_id = stu_match.group(1) if stu_match else "unknown"
        
        filename = os.path.basename(fb_path)
        crit_match = re.search(r"(\d+)", filename)
        crit_id = crit_match.group(1) if crit_match else "unknown"
        
        try:
            with open(fb_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if not re.search(r"Status:.*(?:FAIL|NOT MET)", content, re.IGNORECASE):
                continue
            
            found_issue = False
            code_blocks = extract_code_blocks(content)
            bad_code = code_blocks[0] if code_blocks else ""
                
            # Strategy 1: Action Items with Issue/Why/Fix (stu_333 format)
            action_items = re.findall(
                r"\d+\.\s+\*\*([^*]+)\*\*:.*?\*\*Issue\*\*:\s*(.*?)(?=\*\*(?:Why|Fix)|$)",
                content, re.DOTALL
            )
            
            for title, issue in action_items:
                title = title.strip()
                issue = issue.strip()
                
                why_match = re.search(
                    rf"{re.escape(title)}.*?\*\*Why it (?:fails|matters)\*\*:\s*(.*?)(?=\*\*Fix|$)",
                    content, re.DOTALL
                )
                why = why_match.group(1).strip() if why_match else ""
                
                category = categorize_issue(issue, content)
                issue_key = issue[:100]
                
                if issue_key in issue_tracker:
                    issue_tracker[issue_key].frequency += 1
                    issue_tracker[issue_key].students.append(stu_id)
                else:
                    pattern = AntiPattern(
                        category=category,
                        title=title,
                        description=issue,
                        bad_code=bad_code,
                        why_fails=why,
                        frequency=1,
                        students=[stu_id],
                        criterion=crit_id
                    )
                    issue_tracker[issue_key] = pattern
                found_issue = True
            
            # Strategy 2: "Critical Requirement NOT Met" sections (stu_139 format)
            if not found_issue:
                critical_match = re.search(
                    r"\*\*Critical Requirement NOT Met:\*\*.*?[-•]\s*\*\*([^*]+)\*\*[:\s]*(.*?)(?=\n\n|\*\*Required Fix|$)",
                    content, re.DOTALL
                )
                if critical_match:
                    title = critical_match.group(1).strip()
                    issue = critical_match.group(2).strip()
                    
                    # Get detailed explanation
                    why = ""
                    why_match = re.search(r"The rubric.*?states[:\s]*(.*?)(?=\n\n|$)", content, re.DOTALL)
                    if why_match:
                        why = why_match.group(1).strip()
                    
                    category = categorize_issue(title + " " + issue, content)
                    issue_key = (title + issue)[:100]
                    
                    if issue_key in issue_tracker:
                        issue_tracker[issue_key].frequency += 1
                        issue_tracker[issue_key].students.append(stu_id)
                    else:
                        pattern = AntiPattern(
                            category=category,
                            title=title,
                            description=issue,
                            bad_code=bad_code,
                            why_fails=why,
                            frequency=1,
                            students=[stu_id],
                            criterion=crit_id
                        )
                        issue_tracker[issue_key] = pattern
                    found_issue = True
            
            # Strategy 3: "(PARTIAL)" or "(FAIL)" section headers
            if not found_issue:
                partial_matches = re.findall(
                    r"###\s*\d*\.?\s*([^(]+)\s*\((?:PARTIAL|FAIL)\)(.*?)(?=###|\Z)",
                    content, re.DOTALL
                )
                for title, section in partial_matches:
                    title = title.strip()
                    # Find the issue in this section
                    finding_match = re.search(r"\*\*Finding:\*\*\s*(.*?)(?=\*\*Analysis|$)", section, re.DOTALL)
                    analysis_match = re.search(r"\*\*Analysis:\*\*\s*(.*?)(?=\n\n|$)", section, re.DOTALL)
                    
                    issue = finding_match.group(1).strip() if finding_match else title
                    why = analysis_match.group(1).strip() if analysis_match else ""
                    
                    category = categorize_issue(title + issue, content)
                    issue_key = (title + issue[:50])[:100]
                    
                    if issue_key in issue_tracker:
                        issue_tracker[issue_key].frequency += 1
                        issue_tracker[issue_key].students.append(stu_id)
                    else:
                        pattern = AntiPattern(
                            category=category,
                            title=title,
                            description=issue[:200],
                            bad_code=bad_code,
                            why_fails=why[:300],
                            frequency=1,
                            students=[stu_id],
                            criterion=crit_id
                        )
                        issue_tracker[issue_key] = pattern
                    found_issue = True
            
            # Strategy 4: "Required Fix" section
            if not found_issue:
                fix_match = re.search(
                    r"\*\*Required Fix:\*\*\s*(.*?)(?=```|$)",
                    content, re.DOTALL
                )
                if fix_match:
                    issue = fix_match.group(1).strip()
                    category = categorize_issue(issue, content)
                    issue_key = issue[:100]
                    
                    if issue_key in issue_tracker:
                        issue_tracker[issue_key].frequency += 1
                        issue_tracker[issue_key].students.append(stu_id)
                    else:
                        pattern = AntiPattern(
                            category=category,
                            title="Required Fix",
                            description=issue[:200],
                            bad_code=bad_code,
                            why_fails="",
                            frequency=1,
                            students=[stu_id],
                            criterion=crit_id
                        )
                        issue_tracker[issue_key] = pattern
                    found_issue = True
            
            # Strategy 5: Assessment section with "However" (fallback)
            if not found_issue:
                assessment = re.search(r"## Assessment(.*?)(?=## |\Z)", content, re.DOTALL)
                if assessment:
                    text = assessment.group(1).strip()
                    however_match = re.search(r"However,?\s*(.*?)(?=\n\n|$)", text, re.DOTALL)
                    if however_match:
                        issue = however_match.group(1).strip()
                        category = categorize_issue(issue, text)
                        issue_key = issue[:100]
                        
                        if issue_key in issue_tracker:
                            issue_tracker[issue_key].frequency += 1
                            issue_tracker[issue_key].students.append(stu_id)
                        else:
                            pattern = AntiPattern(
                                category=category,
                                title="Assessment Issue",
                                description=issue,
                                why_fails=text[:500],
                                frequency=1,
                                students=[stu_id],
                                criterion=crit_id
                            )
                            issue_tracker[issue_key] = pattern
                        found_issue = True
            
            # Strategy 6: Generic "Status: FAIL" reason extraction
            if not found_issue:
                # Look for text after "Status: FAIL" header
                fail_reason = re.search(
                    r"##\s*Status:\s*FAIL\s*(.*?)(?=\n##|\Z)",
                    content, re.DOTALL | re.IGNORECASE
                )
                if fail_reason:
                    text = fail_reason.group(1).strip()
                    # First sentence or first 200 chars
                    issue = text.split('.')[0] if '.' in text[:200] else text[:200]
                    category = categorize_issue(issue, text)
                    issue_key = issue[:100]
                    
                    if issue_key in issue_tracker:
                        issue_tracker[issue_key].frequency += 1
                        issue_tracker[issue_key].students.append(stu_id)
                    else:
                        pattern = AntiPattern(
                            category=category,
                            title="Failure Reason",
                            description=issue,
                            bad_code=bad_code,
                            why_fails=text[:300],
                            frequency=1,
                            students=[stu_id],
                            criterion=crit_id
                        )
                        issue_tracker[issue_key] = pattern
                    found_issue = True
            
            if found_issue:
                processed += 1
                            
        except Exception as e:
            print(f"Error: {fb_path}: {e}")
    
    print(f"Extracted issues from {processed} files")
    
    # Organize by category
    for pattern in issue_tracker.values():
        patterns_by_category[pattern.category].append(pattern)
    
    # Sort each category by frequency
    for cat in patterns_by_category:
        patterns_by_category[cat].sort(key=lambda x: x.frequency, reverse=True)
    
    return patterns_by_category


def generate_visual_guide(patterns: Dict[str, List[AntiPattern]]):
    """Generate the visual markdown guide"""
    
    total_failures = sum(p.frequency for cat in patterns.values() for p in cat)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        # Header
        out.write("# 🚫 Agent Anti-Patterns Visual Guide\n\n")
        out.write("> **Purpose**: A visual reference for LLMs to generate educational slides and infographics about common agent development mistakes.\n\n")
        
        # Executive Summary
        out.write("## 📊 Executive Summary\n\n")
        out.write(f"**Total Failures Analyzed**: {total_failures}\n\n")
        
        # Statistics table
        out.write("| Category | Count | Impact Level |\n")
        out.write("|----------|-------|--------------|\n")
        for cat_id, cat_patterns in sorted(patterns.items(), key=lambda x: sum(p.frequency for p in x[1]), reverse=True):
            if cat_id == "other":
                continue
            cat_info = ANTIPATTERN_CATEGORIES.get(cat_id, {"title": cat_id, "icon": "❓"})
            count = sum(p.frequency for p in cat_patterns)
            impact = "🔴 Critical" if count > 100 else "🟡 Moderate" if count > 20 else "🟢 Low"
            out.write(f"| {cat_info['icon']} {cat_info['title']} | {count} | {impact} |\n")
        out.write("\n")
        
        # Visual Overview Diagram
        out.write("## 🗺️ Anti-Pattern Landscape\n\n")
        out.write("```mermaid\nmindmap\n")
        out.write("  root((Agent\\nAnti-Patterns))\n")
        for cat_id, cat_patterns in patterns.items():
            if cat_id == "other" or not cat_patterns:
                continue
            cat_info = ANTIPATTERN_CATEGORIES.get(cat_id, {"title": cat_id})
            safe_title = cat_info['title'].replace('"', "'")
            out.write(f"    {safe_title}\n")
            for p in cat_patterns[:3]:  # Top 3 issues per category
                safe_desc = p.description[:30].replace('"', "'").replace("\n", " ")
                out.write(f"      {safe_desc}...\n")
        out.write("```\n\n")
        
        # Detailed Sections per Category
        for cat_id, cat_patterns in patterns.items():
            if cat_id == "other" or not cat_patterns:
                continue
                
            cat_info = ANTIPATTERN_CATEGORIES.get(cat_id, {"title": cat_id, "icon": "❓", "description": ""})
            
            out.write(f"---\n\n## {cat_info['icon']} {cat_info['title']}\n\n")
            out.write(f"> {cat_info['description']}\n\n")
            
            # Frequency chart (text-based)
            out.write("### 📈 Frequency Distribution\n\n")
            out.write("```\n")
            max_freq = max(p.frequency for p in cat_patterns[:5])
            for p in cat_patterns[:5]:
                bar_len = int((p.frequency / max_freq) * 30) if max_freq > 0 else 0
                bar = "█" * bar_len
                label = p.description[:40].replace("\n", " ")
                out.write(f"{label:<40} {bar} ({p.frequency})\n")
            out.write("```\n\n")
            
            # Top anti-patterns with visual cards
            out.write("### 🃏 Top Anti-Patterns\n\n")
            
            for i, pattern in enumerate(cat_patterns[:3], 1):
                out.write(f"#### {i}. {pattern.title if pattern.title != 'Assessment Issue' else pattern.description[:50]}\n\n")
                
                # Impact badge
                impact_emoji = "🔴" if pattern.frequency > 50 else "🟡" if pattern.frequency > 10 else "🟢"
                out.write(f"**Impact**: {impact_emoji} {pattern.frequency} students affected (Criterion {pattern.criterion})\n\n")
                
                # Description
                if pattern.description:
                    out.write(f"**What went wrong**:\n> {pattern.description}\n\n")
                
                # Why it fails
                if pattern.why_fails:
                    out.write(f"**Why this breaks the agent**:\n> {pattern.why_fails[:300]}{'...' if len(pattern.why_fails) > 300 else ''}\n\n")
                
                # Bad code example
                if pattern.bad_code:
                    out.write("**❌ Anti-Pattern Code**:\n")
                    out.write(f"```python\n{pattern.bad_code}\n```\n\n")
                
                # Good code suggestion
                fix = generate_fix_suggestion(cat_id, pattern.bad_code or "")
                if fix:
                    out.write("**✅ Correct Pattern**:\n")
                    out.write(f"{fix}\n\n")
                
                # Visual metaphor
                out.write("**💡 Visual Metaphor**:\n")
                metaphors = {
                    "string_matching": "Like a bouncer checking IDs who lets in anyone whose name *contains* 'VIP' - including 'NOT_VIP'!",
                    "missing_documentation": "Like giving someone a map with no labels - they'll guess where to go and probably get lost.",
                    "output_format_mismatch": "Like speaking French to a Spanish parser - technically language, but nothing gets through.",
                    "hallucination_triggers": "Like asking 'describe the elephant in the room' when there's no elephant - the LLM will invent one!",
                    "incomplete_react_cycle": "Like a pilot with only 2 of 3 controls - take-off works, but landing is unpredictable.",
                    "missing_constraints": "Like asking a chef to 'make something good' with no ingredient list - they'll improvise with whatever they imagine.",
                    "role_definition": "Like hiring an actor but never telling them what character to play - expect improvised chaos.",
                    "chain_of_thought": "Like asking someone to solve a puzzle blindfolded - they might get lucky, but probably won't."
                }
                out.write(f"> {metaphors.get(cat_id, 'Every small gap compounds into system failure.')}\n\n")
                
                out.write("---\n\n")
        
        # Footer with slide generation hints
        out.write("## 🎨 Slide Generation Hints\n\n")
        out.write("When generating slides from this document:\n\n")
        out.write("1. **Title Slide**: Use the executive summary statistics\n")
        out.write("2. **Category Slides**: One slide per category with the mindmap subsection\n")
        out.write("3. **Deep Dive Slides**: Before/After code comparisons with visual metaphors\n")
        out.write("4. **Impact Slides**: Use frequency bars to show which issues are most common\n")
        out.write("5. **Takeaway Slide**: Summarize the top 3 anti-patterns to avoid\n\n")
        
        out.write("### Color Coding Reference\n\n")
        out.write("| Color | Meaning |\n")
        out.write("|-------|--------|\n")
        out.write("| 🔴 Red | Critical issue (>100 occurrences) |\n")
        out.write("| 🟡 Yellow | Moderate issue (20-100 occurrences) |\n")
        out.write("| 🟢 Green | Low frequency (<20 occurrences) |\n")
    
    print(f"Done. Visual guide written to {OUTPUT_FILE}")

def main():
    patterns = process_failures()
    generate_visual_guide(patterns)
    
if __name__ == "__main__":
    main()
