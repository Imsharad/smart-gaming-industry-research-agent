#!/usr/bin/env python3
"""
generate_feedback_json.py
Generates `all_feedback.json` from `criteria_*.md` files.
Starts a local HTTP server to serve the feedback to the Chrome Extension.

Usage:
    python generate_feedback_json.py ./feedback
"""

import json
import sys
import re
import subprocess
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Any, Optional

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

PORT = 8543
FEEDBACK_DATA = {}
SERVER_SHUTDOWN_REQUESTED = False

class FeedbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global SERVER_SHUTDOWN_REQUESTED
        
        if self.path == '/feedback':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Allow Chrome Extension
            self.end_headers()
            
            response = json.dumps(FEEDBACK_DATA).encode('utf-8')
            self.wfile.write(response)
            
            # Signal to shutdown after successful fetch
            # We wait a moment to ensure response is sent
            SERVER_SHUTDOWN_REQUESTED = True
            
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        pass # Silence server logs

def print_info(msg): print(f"{GREEN}[INFO]{NC} {msg}")
def print_step(msg): print(f"{BLUE}[STEP]{NC} {msg}")
def print_warning(msg): print(f"{YELLOW}[WARNING]{NC} {msg}")
def print_error(msg): print(f"{RED}[ERROR]{NC} {msg}")

def find_summary_file(feedback_dir: Path) -> Optional[str]:
    """Look for summary.md in feedback dir or its parent."""
    # Check feedback/summary.md
    s1 = feedback_dir / "summary.md"
    if s1.exists():
        return s1.read_text(encoding='utf-8').strip()
    
    # Check ../summary.md (root/parent of feedback)
    s2 = feedback_dir.parent / "summary.md"
    if s2.exists():
        return s2.read_text(encoding='utf-8').strip()
        
    return None

def combine_criteria_files(feedback_dir: Path) -> Dict[str, Any]:
    """Combine criteria_*.md files into JSON object."""
    result = {}
    
    # Robustly find files matching criteria_N.md
    files = list(feedback_dir.glob("criteria_*.md"))
    
    criteria_files = []
    for f in files:
        match = re.search(r'criteria_(\d+)\.md', f.name)
        if match:
            criteria_files.append((int(match.group(1)), f))
        else:
            print_warning(f"Skipping file with unexpected name format: {f.name}")
            
    criteria_files.sort(key=lambda x: x[0])
    
    if not criteria_files:
        raise FileNotFoundError(f"No valid criteria_*.md files found in {feedback_dir}")

    for num, file in criteria_files:
        try:
            content = file.read_text(encoding='utf-8').strip()
        except Exception as e:
            print_error(f"Failed to read {file}: {e}")
            continue
            
        # Parse Status
        lines = content.split('\n')
        status = 'pass'
        text_start_idx = 0
        
        for i, line in enumerate(lines):
            if line.strip():
                if line.upper().startswith('STATUS:'):
                    status_part = line.split(':', 1)[1].strip().lower()
                    if status_part in ['pass', 'fail']:
                        status = status_part
                    text_start_idx = i + 1
                    break
                else:
                    # Missing status line, treat whole file as text
                    break
        
        text = '\n'.join(lines[text_start_idx:]).strip()
        
        result[str(num)] = {
            "text": text,
            "status": status
        }
        
    # Process Summary
    summary_text = find_summary_file(feedback_dir)
    if summary_text:
        result["summary"] = summary_text
        print_info("Found and included summary.md")
    else:
        print_warning("No summary.md found (checked feedback/ and parent dir)")
    
    return result

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard using pbcopy (macOS)."""
    if sys.platform != 'darwin':
        return False
        
    try:
        subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def start_server_and_wait():
    """Start HTTP server and wait for extension to fetch data."""
    server = HTTPServer(('localhost', PORT), FeedbackHandler)
    server.timeout = 1.0
    print_step(f"Waiting for Chrome Extension to fetch feedback on port {PORT}...")
    print_info("Keep this window open. It will close automatically when feedback is transferred.")
    
    # Wait for up to 60 seconds
    start_time = time.time()
    while not SERVER_SHUTDOWN_REQUESTED and (time.time() - start_time < 60):
        server.handle_request()
        
    if SERVER_SHUTDOWN_REQUESTED:
        print_info("Feedback successfully transferred to Chrome!")
    else:
        print_warning("Timeout: Chrome Extension did not fetch the feedback.")

def main():
    if len(sys.argv) < 2:
        print_error("Usage: python generate_feedback_json.py <feedback_directory>")
        sys.exit(1)
    
    feedback_dir = Path(sys.argv[1])
    
    if not feedback_dir.exists() or not feedback_dir.is_dir():
        print_error(f"Feedback directory not found: {feedback_dir}")
        sys.exit(1)
        
    print_info(f"Processing feedback from: {feedback_dir}")
    
    try:
        global FEEDBACK_DATA
        FEEDBACK_DATA = combine_criteria_files(feedback_dir)
        
        # Output File
        output_file = feedback_dir / "all_feedback.json"
        json_output = json.dumps(FEEDBACK_DATA, indent=2, ensure_ascii=False)
        output_file.write_text(json_output, encoding='utf-8')
        
        # Clipboard (still useful as backup)
        if copy_to_clipboard(json_output):
            print_info("JSON copied to clipboard (Backup)")
            
        # Start Server for Direct Integration
        start_server_and_wait()
            
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
