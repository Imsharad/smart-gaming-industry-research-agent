# Detailed Agent Logic Implementation Plan

## Goal
Transition from "Scaffolding" (Mocked Agents) to "Production" (Real Logic).

## 1. Gmail Agent (The Watcher)
**Objective**: Reliably detect "Assigned Project" emails.
*   [ ] **Dependency**: Install `google-auth-oauthlib` `google-api-python-client`.
*   [ ] **Auth**: simple `token.json` flow.
    *   *Action*: You will run a "one-time setup script" to authenticate via browser.
    *   **Logic**:
        *   Poll every 60s.
        *   **State Tracking**: Save `last_processed_message_id` or `last_check_timestamp` to a local file (`.gmail_state`).
        *   Query: `from:support@udacity.com subject:"You have been assigned a review" after:TIMESTAMP`.
        *   *Benefit*: Triggers even if you read the email on your phone.

## 2. Browser Agent (The Fetcher)
**Objective**: Login and Download Zip.
*   [ ] **Dependency**: Install `playwright`.
*   [ ] **Browser**: Launch Chrome (Headless) with **User Data Dir** (Profile Persistence).
*   [ ] **Flow**:
    1.  Go to `https://mentor-dashboard.udacity.com/queue/overview`.
    2.  Check for "Login" selector.
        *   If present -> Trigger `wait_for_manual_login`.
    3.  Wait for "Reviews" table.
    4.  Click "Continue Review" or "Start Review".
    5.  Find "Download Zip" button.
    6.  Wait for download to complete.
    7.  Return `zip_path`.

## 3. Project Manager (The Librarian)
**Objective**: Prepare the Workspace.
*   [ ] **Action**: Simply execute `bash setup_next_student.sh` in the project's `tmp` directory.
    *   *Note*: The script handles finding the zip in Downloads, unzipping, creating `stu_N`, and archiving `stu_N-1`.
*   [ ] **Output Parsing**:
    *   Parse stdout to find the new directory path (e.g., "Creating stu_40 from stu_39").
*   [ ] **Validation**: Verify `project/` and `feedback/` directories exist in the new path.

## 4. Reviewer Agent (The Brain)
**Objective**: Think and Write.
*   [ ] **Context Loading**:
    *   Read `notes.txt` (The "System Prompt" for the specific project).
    *   Read `criteria_prompts/*.txt` (The specific rubric items).
*   [ ] **Execution**:
    *   Use `claude-agent-sdk` to analyze the code.
    *   *Constraint*: Read-Only on student files (unless sandboxed).
*   [ ] **Output**:
    *   Write `feedback/summary.md`.
    *   Write `feedback/criteria_X.md`.

## Execution Order
1.  **Gmail** (Unlock the Trigger).
2.  **Browser** (Unlock the Data).
3.  **Project Manager** (Unlock the Environment).
4.  **Reviewer** (Unlock the Value).
