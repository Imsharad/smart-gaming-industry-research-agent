#!/bin/bash

# Configuration
SETUP_SCRIPT="./setup_next_student_optimized.sh"
NOTES_FILE="notes.txt"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# macOS Notification
notify_macos() {
    local title="$1"
    local message="$2"
    osascript -e "display notification \"$message\" with title \"$title\" sound name \"Submarine\""
}

# Check prerequisites
if [[ ! -f "$SETUP_SCRIPT" ]]; then
    echo -e "${RED}[ERROR]${NC} Setup script not found: $SETUP_SCRIPT"
    exit 1
fi

if [[ ! -f "$NOTES_FILE" ]]; then
    echo -e "${RED}[ERROR]${NC} Notes file not found: $NOTES_FILE"
    exit 1
fi

if ! command -v gemini &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} 'gemini' CLI not found in path."
    exit 1
fi

# Step 1: Run setup script to prepare next student
print_step "Running setup script..."
# Capture the output to find the new directory
OUTPUT=$($SETUP_SCRIPT "$@")
EXIT_CODE=$?

# Print output for user visibility
echo "$OUTPUT"

# Warn if setup failed, but continue anyway to give Gemini a chance
if [[ $EXIT_CODE -ne 0 ]]; then
    echo -e "${YELLOW}[WARNING]${NC} Setup script reported errors, but continuing to run review..."
fi

# Extract the new student directory from the output
# Robustly parse the log message "Creating stu_XXX" to get the exact directory name
# We filter out color codes/prefixes and grab the stu_XXX identifier
NEW_DIR_NAME=$(echo "$OUTPUT" | grep -o "Creating stu_[0-9]*" | head -n 1 | awk '{print $2}')

if [[ -n "$NEW_DIR_NAME" ]]; then
    NEW_DIR="./$NEW_DIR_NAME"
else
    # If we can't detect from output, try to find the latest stu_* directory
    echo -e "${YELLOW}[WARNING]${NC} Could not detect directory from logs, searching for latest..."
    LATEST_STU=$(ls -dt stu_* 2>/dev/null | grep -v "stu_template" | head -1)
    if [[ -n "$LATEST_STU" ]]; then
        NEW_DIR="./$LATEST_STU"
        echo -e "${GREEN}[INFO]${NC} Found: $LATEST_STU"
    else
        echo -e "${RED}[ERROR]${NC} Could not find any student directory to review."
        exit 1
    fi
fi

STUDENT_ID=$(basename "$NEW_DIR")
print_info "Targeting student directory: $STUDENT_ID"

# Step 2: Navigate and Run Automation
print_step "Starting Automated Review for $STUDENT_ID..."

cd "$NEW_DIR" || exit 1

# Start timer
START_TIME=$(date +%s)

# Run Gemini in headless/YOLO mode with notes.txt content
print_info "Invoking Gemini agent..."
# Use cat to pipe the prompt content
cat "../$NOTES_FILE" | gemini --yolo

GEMINI_EXIT=$?
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [[ $GEMINI_EXIT -eq 0 ]]; then
    print_step "Review generation completed in ${DURATION}s."
    
    # Verify outputs
    COUNT=$(ls feedback/criteria_*.md 2>/dev/null | wc -l)
    HAS_SUMMARY=$([[ -f "feedback/summary.md" ]] && echo "yes" || echo "no")
    
    if [[ $COUNT -ge 5 && "$HAS_SUMMARY" == "yes" ]]; then
        print_info "SUCCESS: Generated $COUNT criteria files and summary.md"
        
        # Step 3: Generate JSON for Chrome Extension
        print_step "Generating all_feedback.json for Chrome Extension..."
        if python3 ../generate_feedback_json.py; then
            print_info "JSON feedback generation successful."
            notify_macos "✅ Review Complete" "Feedback for $STUDENT_ID is ready"
        else
            echo -e "${RED}[WARNING]${NC} Failed to generate JSON feedback."
        fi

        # Optional: open the summary
        # open feedback/summary.md
    else
        echo -e "${RED}[WARNING]${NC} Process finished but some files might be missing. Found $COUNT criteria files."
        notify_macos "⚠️ Review Warning" "Some files might be missing for $STUDENT_ID"
    fi
else
    echo -e "${RED}[ERROR]${NC} Gemini agent failed with exit code $GEMINI_EXIT"
    notify_macos "❌ Review Failed" "Gemini agent failed for $STUDENT_ID"
    exit 1
fi
