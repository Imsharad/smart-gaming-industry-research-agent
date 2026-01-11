
## Criterion 2 - Weather Compatibility System Prompt
☐ Check ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT role definition
   ```bash
   Grep --pattern "ACTIVITY_AND_WEATHER_ARE_COMPATIBLE_SYSTEM_PROMPT" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 30
   ```
☐ Verify LLM role and task are clearly defined
   ```bash
   Grep --pattern "You are.*weather\|determine.*compatible\|evaluate.*weather\|assess.*conditions" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
   ```
☐ Verify exact output format specification
   ```bash
   Grep --pattern "IS_COMPATIBLE\|IS_INCOMPATIBLE\|Output.*format\|return.*IS_" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 5
   ```
☐ Confirm examples showing IS_COMPATIBLE and IS_INCOMPATIBLE cases
   ```bash
   Grep --pattern "Example.*:" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content" -A 10
   ```
☐ Check if prompt mentions considering backup options for activities
   ```bash
   Grep --pattern "backup.*option\|alternative.*activit\|contingency\|rain.*plan" --path "/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/*.ipynb" --output_mode "content"
   ```
☐ **Generate feedback/2.md for Criterion 2**
   ```bash
   Write /Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp/stu_X/feedback/2.md
   # Content: Assessment of Criterion 2 based on findings
   ```