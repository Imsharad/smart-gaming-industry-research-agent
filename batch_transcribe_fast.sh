#!/bin/bash

# FAST Hybrid Transcription: Use existing SRT files + Whisper tiny model
# This is 10-20x faster than using base model

set -e

WHISPER_ENV="/Users/sharad/Projects/udacity-reviews-hq/whisper_env"
WHISPER_MODEL="tiny"  # Fastest model

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ $# -lt 1 ]; then
    echo "Usage: $0 <course_directory>"
    exit 1
fi

COURSE_DIR="$1"
TRANSCRIPTS_DIR="$COURSE_DIR/transcripts"
MASTER_TRANSCRIPT="$COURSE_DIR/MASTER_TRANSCRIPT_FAST.txt"

mkdir -p "$TRANSCRIPTS_DIR"

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}FAST Hybrid Transcription${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "Using existing SRT + Whisper tiny model"
echo ""

# Step 1: Copy existing SRT files as transcripts
echo -e "${YELLOW}Step 1: Converting existing SRT files...${NC}"
SRT_COUNT=0

find "$COURSE_DIR" -name "*.srt" -path "*/subtitles/*" | while read srt_file; do
    # Get section and filename
    rel_path="${srt_file#$COURSE_DIR/}"
    section=$(echo "$rel_path" | cut -d'/' -f1)
    filename=$(basename "$srt_file" .srt)

    # Create output directory
    section_transcript_dir="$TRANSCRIPTS_DIR/$section"
    mkdir -p "$section_transcript_dir"

    output_txt="$section_transcript_dir/${filename}.txt"

    # Convert SRT to plain text
    awk '
        BEGIN { in_text = 0; text = "" }
        /^[0-9]+$/ { next }
        /^[0-9]{2}:[0-9]{2}:[0-9]{2}/ { next }
        /^$/ {
            if (text != "") {
                print text
                text = ""
            }
            next
        }
        {
            if (text != "") text = text " " $0
            else text = $0
        }
        END { if (text != "") print text }
    ' "$srt_file" > "$output_txt"

    SRT_COUNT=$((SRT_COUNT + 1))
    echo -e "  ${GREEN}✓${NC} $section/$filename"
done

echo -e "${GREEN}Converted $SRT_COUNT SRT files${NC}"
echo ""

# Step 2: Transcribe remaining videos with Whisper tiny
echo -e "${YELLOW}Step 2: Transcribing videos without subtitles (tiny model)...${NC}"

source "$WHISPER_ENV/bin/activate"

MP4_FILES=$(find "$COURSE_DIR" -name "*.mp4" | sort)
TOTAL_MP4=$(echo "$MP4_FILES" | wc -l | tr -d ' ')

COUNT=0
TRANSCRIBED=0
SKIPPED=0

while IFS= read -r video_file; do
    COUNT=$((COUNT + 1))

    rel_path="${video_file#$COURSE_DIR/}"
    section=$(echo "$rel_path" | cut -d'/' -f1)
    filename=$(basename "$video_file" .mp4)

    section_transcript_dir="$TRANSCRIPTS_DIR/$section"
    mkdir -p "$section_transcript_dir"

    output_txt="$section_transcript_dir/${filename}.txt"

    # Skip if already exists
    if [ -f "$output_txt" ]; then
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    echo -e "  [${COUNT}/${TOTAL_MP4}] ${BLUE}Transcribing${NC} $filename"

    # Run Whisper with tiny model
    whisper "$video_file" \
        --model "$WHISPER_MODEL" \
        --language en \
        --output_dir "$section_transcript_dir" \
        --output_format txt \
        --verbose False 2>&1 | grep -v "Downloading" || true

    TRANSCRIBED=$((TRANSCRIBED + 1))
    echo -e "  [${COUNT}/${TOTAL_MP4}] ${GREEN}✓${NC} Done"

done <<< "$MP4_FILES"

echo ""
echo -e "${GREEN}Transcribed $TRANSCRIBED new videos${NC}"
echo -e "${YELLOW}Skipped $SKIPPED (already had transcripts)${NC}"
echo ""

# Step 3: Generate master transcript
echo -e "${YELLOW}Step 3: Generating master transcript...${NC}"

cat > "$MASTER_TRANSCRIPT" << HEADER
================================================================================
MASTER TRANSCRIPT (Fast Hybrid Mode)
Course: $(basename "$(dirname "$COURSE_DIR")")
Method: Existing SRT + Whisper Tiny Model
Generated: $(date '+%Y-%m-%d %H:%M:%S')
Total Videos: $TOTAL_MP4
================================================================================

HEADER

find "$TRANSCRIPTS_DIR" -name "*.txt" | sort | while read transcript; do
    rel_path="${transcript#$TRANSCRIPTS_DIR/}"
    section=$(dirname "$rel_path")
    filename=$(basename "$transcript" .txt)

    cat >> "$MASTER_TRANSCRIPT" << SECTION_HEADER

################################################################################
# Section: $section
# File: $filename
################################################################################

SECTION_HEADER

    cat "$transcript" >> "$MASTER_TRANSCRIPT"
    echo "" >> "$MASTER_TRANSCRIPT"
done

MASTER_SIZE=$(du -h "$MASTER_TRANSCRIPT" | cut -f1)

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}✓ Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo -e "Master transcript: ${BLUE}$MASTER_TRANSCRIPT${NC} ($MASTER_SIZE)"
echo ""
