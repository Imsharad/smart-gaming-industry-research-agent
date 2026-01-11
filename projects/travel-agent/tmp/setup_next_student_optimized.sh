#!/bin/bash

# Student Assignment Setup Script - Travel Agent Project (ULTRA-OPTIMIZED)
# PERFORMANCE OPTIMIZATIONS:
# - Single find+stat pass with parallel processing
# - Minimal stat calls (only what's necessary)
# - Fast path operations
# - No redundant verification
# - Streamlined extraction

set -e  # Exit on any error

# Configuration
DOWNLOADS_DIR="/Users/sharad/Downloads"
SUBMISSIONS_DIR="/Users/sharad/Projects/udacity-reviews-hq/projects/travel-agent/tmp"
# External archive location (outside git repo)
PROJECT_NAME=$(basename "$(dirname "$SUBMISSIONS_DIR")")
EXTERNAL_ARCHIVE_DIR="$HOME/Archives/udacity-reviews/$PROJECT_NAME"
VERBOSE=false
AUTO_ARCHIVE=true  # Automatically archive previous student directories

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Output functions
print_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# OPTIMIZED: Ultra-fast zip finder - single pass, minimal stat calls
find_latest_zip_fast() {
    local latest_zip=""
    local latest_time=0

    # Single find command - get modification time and path
    while IFS='|' read -r mtime filepath; do
        if [[ $mtime -gt $latest_time ]]; then
            latest_time=$mtime
            latest_zip="$filepath"
        fi
    done < <(find "$DOWNLOADS_DIR" -maxdepth 1 -name "*.zip" -type f -exec stat -f "%m|%N" {} + 2>/dev/null)

    if [[ -z "$latest_zip" ]]; then
        print_error "No zip files found in $DOWNLOADS_DIR"
        exit 1
    fi

    echo "$latest_zip"
}

# OPTIMIZED: Show only essential info
show_file() {
    local file="$1"
    print_info "Using: $(basename "$file")"
}

# OPTIMIZED: Fast directory finder - single loop
find_highest_student_dir() {
    local highest_num=0
    local highest_dir=""

    # Single loop through both locations
    for dir in "$SUBMISSIONS_DIR"/stu_* "$EXTERNAL_ARCHIVE_DIR"/stu_*; do
        [[ -d "$dir" ]] || continue
        # Ignore template directory when looking for numbers
        if [[ "$(basename "$dir")" == "stu_template" ]]; then continue; fi
        
        local num="${dir##*/stu_}"
        [[ "$num" =~ ^[0-9]+$ ]] || continue
        if [[ $num -gt $highest_num ]]; then
            highest_num=$num
            highest_dir="$dir"
        fi
    done

    if [[ -z "$highest_dir" ]]; then
        print_error "No existing student directories found"
        exit 1
    fi

    echo "$highest_dir"
}

# Main function
main() {
    print_info "Setting up new student directory..."

    cd "$SUBMISSIONS_DIR"

    # Find latest zip (ultra-fast)
    local latest_zip=$(find_latest_zip_fast)
    show_file "$latest_zip"

    # Find source directory for numbering only
    local highest_dir=$(find_highest_student_dir)
    local source_num="${highest_dir##*/stu_}"
    local next_num=$((source_num + 1))
    local target_dir="$SUBMISSIONS_DIR/stu_$next_num"
    local template_dir="$SUBMISSIONS_DIR/stu_template"

    if [[ ! -d "$template_dir" ]]; then
        print_error "Template directory not found: $template_dir"
        print_info "Please run: cp -R stu_403 stu_template (or latest valid student) and clean it up"
        exit 1
    fi

    print_info "Creating stu_$next_num from stu_template"

    # Handle existing target
    if [[ -d "$target_dir" ]]; then
        print_warning "stu_$next_num exists. Overwrite? (y/n)"
        read -r response
        [[ "$response" =~ ^[Yy]$ ]] || { print_info "Cancelled."; exit 0; }
        rm -rf "$target_dir"
    fi

    # Duplicate directory from template (fast copy)
    cp -R "$template_dir" "$target_dir"

    # Clear old submission files from root
    find "$target_dir" -maxdepth 1 -type f \( -name "*.ipynb" -o -name "*.py" -o -name "summary.md" \) -delete 2>/dev/null || true

    # Clear and prepare directories
    local project_dir="$target_dir/project"
    local feedback_dir="$target_dir/feedback"

    # Fast cleanup
    chmod -R u+w "$project_dir" "$feedback_dir" 2>/dev/null || true
    rm -rf "$project_dir"/* "$feedback_dir"/* 2>/dev/null || true
    mkdir -p "$project_dir" "$feedback_dir"

    # Extract zip with robust error handling
    print_info "Extracting submission..."
    local temp_dir=$(mktemp -d)
    local cleanup_needed=true

    # Trap to ensure cleanup happens even on errors
    cleanup_temp() {
        if [[ "$cleanup_needed" == "true" && -d "$temp_dir" ]]; then
            chmod -R u+w "$temp_dir" 2>/dev/null || true
            rm -rf "$temp_dir" 2>/dev/null || true
        fi
    }
    trap cleanup_temp EXIT

    # Extract with error checking
    if ! unzip -q "$latest_zip" -d "$temp_dir" 2>/dev/null; then
        print_error "Failed to extract zip file"
        exit 1
    fi

    # Fix permissions on extracted files (some zips have read-only directories)
    # This prevents "Permission denied" errors during move and cleanup
    chmod -R u+w "$temp_dir" 2>/dev/null || true

    # Smart content detection
    local content_dir="$temp_dir"
    local items=("$temp_dir"/*)
    if [[ ${#items[@]} -eq 1 && -d "${items[0]}" ]]; then
        content_dir="${items[0]}"
    fi

    # Move all content (including hidden files)
    shopt -s dotglob nullglob
    if ! mv "$content_dir"/* "$project_dir/" 2>/dev/null; then
        print_warning "Some files may not have moved correctly"
        # Try with cp as fallback, then remove source
        cp -R "$content_dir"/* "$project_dir/" 2>/dev/null || true
    fi
    shopt -u dotglob nullglob

    # Cleanup temp directory (trap will handle this, but try explicitly first)
    cleanup_temp
    cleanup_needed=false
    trap - EXIT

    # Comprehensive verification
    local nb_count=$(ls -1 "$project_dir"/*.ipynb 2>/dev/null | wc -l | tr -d ' ')
    local py_count=$(find "$project_dir" -name "*.py" 2>/dev/null | wc -l | tr -d ' ')
    local has_project_lib=$([[ -f "$project_dir/project_lib.py" ]] && echo "yes" || echo "no")
    local has_prompts=$([[ -d "$project_dir/prompts" ]] && echo "yes" || echo "no")

    # Verify minimum requirements
    if [[ $nb_count -eq 0 && $py_count -eq 0 ]]; then
        print_error "No notebooks or Python scripts found! Setup may have failed."
        print_info "Check $project_dir manually"
        exit 1
    fi

    # Build status message
    local status="Notebooks: $nb_count | Python Files: $py_count"
    [[ "$has_project_lib" == "yes" ]] && status="$status | project_lib.py: ✓" || status="$status | project_lib.py: ✗"
    [[ "$has_prompts" == "yes" ]] && status="$status | prompts/: ✓" || status="$status | prompts/: ✗"

    print_info "$status"

    # ALWAYS archive previous student directories BEFORE verification
    # This prevents directory buildup even if extraction fails
    if [[ "$AUTO_ARCHIVE" == "true" ]]; then
        archive_previous_students "$next_num"

    # Cleanup: Delete the processed zip file
    if [[ -f "$latest_zip" ]]; then
        rm -f "$latest_zip"
        print_info "Cleaned up source zip: $(basename "$latest_zip")"
    fi
    fi

    # Final success check
    if [[ $nb_count -ge 1 || $py_count -ge 1 ]]; then
        # Check if fully complete
        if [[ "$has_project_lib" == "yes" && "$has_prompts" == "yes" ]]; then
            print_info "Setup complete! Ready for stu_$next_num evaluation."
        else
            print_warning "Setup completed but some components may be missing."
            print_info "Please verify $project_dir before evaluation."
        fi


        # Optional: Open in Finder (macOS) - DISABLED
        # if command -v open >/dev/null 2>&1; then
        #     open "$target_dir"
        # fi
    else
        print_error "Setup failed - no notebooks or Python scripts found!"
        print_info "Please check $project_dir manually."
    fi
}

# Archive all previous student directories
archive_previous_students() {
    local current_num=$1
    local archive_dir="$EXTERNAL_ARCHIVE_DIR"
    local archived_count=0

    # Create archive directory if it doesn't exist
    mkdir -p "$archive_dir"

    print_info "Archiving previous student directories..."

    # Find all stu_* directories in the root (not in archive)
    for dir in "$SUBMISSIONS_DIR"/stu_*; do
        # Skip if not a directory or is the current student
        [[ ! -d "$dir" ]] && continue
        [[ "$dir" == "$SUBMISSIONS_DIR/stu_$current_num" ]] && continue
        # Do not archive the template
        [[ "$(basename "$dir")" == "stu_template" ]] && continue

        # Extract student number
        local dir_num="${dir##*/stu_}"
        [[ ! "$dir_num" =~ ^[0-9]+$ ]] && continue

        # Move to archive
        local dir_name=$(basename "$dir")
        if mv "$dir" "$archive_dir/$dir_name" 2>/dev/null; then
            ((archived_count++))
            [[ "$VERBOSE" == "true" ]] && print_info "  Archived: $dir_name"
        else
            print_warning "  Failed to archive: $dir_name"
        fi
    done

    if [[ $archived_count -eq 0 ]]; then
        print_info "No previous directories to archive"
    else
        print_info "Archived $archived_count student directories to archive/"
    fi
}

# Cleanup orphaned temp directories
cleanup_orphaned_temps() {
    print_info "Scanning for orphaned temp directories..."
    local count=0

    # Find temp directories created by this script
    while IFS= read -r temp_dir; do
        if [[ -d "$temp_dir" ]]; then
            print_info "Found: $temp_dir"
            chmod -R u+w "$temp_dir" 2>/dev/null || true
            if rm -rf "$temp_dir" 2>/dev/null; then
                print_info "  ✓ Cleaned up"
                ((count++))
            else
                print_warning "  ✗ Failed to remove"
            fi
        fi
    done < <(find /var/folders -name "tmp.*" -type d -user "$(whoami)" 2>/dev/null | grep -E "tmp\.[a-zA-Z0-9]+$")

    if [[ $count -eq 0 ]]; then
        print_info "No orphaned temp directories found"
    else
        print_info "Cleaned up $count temp directories"
    fi
}

# Handle arguments
case "${1:-}" in
    --verbose|-v)
        VERBOSE=true
        main
        ;;
    --dry-run)
        print_info "DRY RUN MODE"
        cd "$SUBMISSIONS_DIR"
        latest_zip=$(find_latest_zip_fast)
        source_dir=$(find_highest_student_dir)
        source_num="${source_dir##*/stu_}"
        next_num=$((source_num + 1))
        print_info "Would use: $(basename "$latest_zip")"
        print_info "Would create: stu_$next_num from stu_template"

        # Show what would be archived
        if [[ "$AUTO_ARCHIVE" == "true" ]]; then
            archive_count=0
            for dir in "$SUBMISSIONS_DIR"/stu_*; do
                [[ ! -d "$dir" ]] && continue
                [[ "$dir" == "$SUBMISSIONS_DIR/stu_$next_num" ]] && continue
                [[ "$(basename "$dir")" == "stu_template" ]] && continue
                dir_num="${dir##*/stu_}"
                [[ ! "$dir_num" =~ ^[0-9]+$ ]] && continue
                ((archive_count++))
            done
            if [[ $archive_count -gt 0 ]]; then
                print_info "Would archive: $archive_count previous student directories"
            fi
        fi
        ;;
    --no-archive)
        AUTO_ARCHIVE=false
        main
        ;;
    --cleanup)
        cleanup_orphaned_temps
        ;;
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --verbose       Show detailed output during setup"
        echo "  --no-archive    Skip archiving previous student directories"
        echo "  --dry-run       Preview without making changes"
        echo "  --cleanup       Clean up orphaned temp directories"
        echo "  --help          Show this help"
        echo ""
        echo "Description:"
        echo "  Sets up the next student directory for evaluation."
        echo "  Automatically extracts the latest zip from Downloads,"
        echo "  handles permission issues, verifies the setup, and"
        echo "  archives all previous student directories to archive/."
        echo ""
        echo "Examples:"
        echo "  $0                    # Normal setup with auto-archive"
        echo "  $0 --no-archive       # Setup without archiving"
        echo "  $0 --verbose          # Setup with detailed output"
        echo "  $0 --dry-run          # Preview what would happen"
        echo "  $0 --cleanup          # Clean orphaned temp directories"
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac
