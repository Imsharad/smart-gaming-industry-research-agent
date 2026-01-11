#!/bin/bash

# This script automates the setup of a sandboxed review environment.

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if a student ID was provided as an argument.
if [ -z "$1" ]; then
  echo "Usage: $0 <student_id>"
  echo "Example: $0 stu_1"
  exit 1
fi

STUDENT_ID=$1
STUDENT_SUBMISSION_DIR="tmp/$STUDENT_ID"
TEMP_REVIEW_DIR="tmp/review_$STUDENT_ID"

# 1. Create a fresh, temporary review directory.

echo "[INFO] Creating temporary review directory: $TEMP_REVIEW_DIR"
rm -rf "$TEMP_REVIEW_DIR" # Remove old directory if it exists
mkdir -p "$TEMP_REVIEW_DIR"

# 2. Copy the centralized review engine into the temporary directory.

echo "[INFO] Copying review engine (.claude and criteria_prompts)..."
cp -r .claude "$TEMP_REVIEW_DIR/"
cp -r criteria_prompts "$TEMP_REVIEW_DIR/"

# 3. Copy the student's submission into the temporary directory.

if [ ! -d "$STUDENT_SUBMISSION_DIR" ]; then
    echo "[ERROR] Student submission directory not found: $STUDENT_SUBMISSION_DIR"
    exit 1
fi
echo "[INFO] Copying student submission from $STUDENT_SUBMISSION_DIR..."
cp -r "$STUDENT_SUBMISSION_DIR/"* "$TEMP_REVIEW_DIR/"

# 4. Enter the sandboxed environment and run the review.

echo "[INFO] Entering sandboxed review environment..."
cd "$TEMP_REVIEW_DIR"

echo "[INFO] Current directory: $(pwd)"
echo "[INFO] Files in sandbox:"
ls -l

claude -p "Execute the following multi-step assignment verification workflow:

**Step 1: Initial Setup**
Create a directory named 'feedback' if it doesn't exist.

**Step 2: Execute Evaluation Loop**
You will now iterate from 1 to 4. For each number in the sequence, you must invoke the 'CriterionAgent' with the current number as the 'criterion_number'. Wait for the 'CriterionAgent' to complete its evaluation and write the feedback file before proceeding to the next number.

**Step 3: Synthesize Feedback**
Once the evaluation loop is complete, use the 'FeedbackAgent' to read all the files in the 'feedback/' directory and generate the final 'summary.md' report."

# 5. Return to the original directory.

cd ../..
echo "[INFO] Returned to project root: $(pwd)"

# The cleanup step will be added later.
# echo "[INFO] Cleaning up temporary directory: $TEMP_REVIEW_DIR"
# rm -rf "$TEMP_REVIEW_DIR"

echo "[SUCCESS] Review for $STUDENT_ID is complete."