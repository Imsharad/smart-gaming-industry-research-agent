# Implementation Plan - Autonomous Udacity Project Review System

# Goal Description
Build a multi-agent system using the `claude-agents-sdk` to automate the Udacity project review workflow. The system will monitor emails, download projects, set up the local environment, and generate feedback using LLM agents. The process explicitly halts for human verification before submission.

## User Review Required
> [!IMPORTANT]
> **Security & Auth**:
> *   **Auth**: Leverages existing Chrome profile cookies. If the session expires, the system **PAUSES** and alerts the user to manually log in.
> *   **Security**: "Bare Metal" execution. Student code runs directly on the host machine.
> *   **Concurrency**: STRICTLY SERIAL (One review at a time).

## Proposed Changes

> [!NOTE]
> The `projects/automation` directory is verified as the clean slate for this implementation.

### Core Architecture
#### [NEW] [orchestrator.py](file:///Users/sharad/Projects/udacity-reviews-hq/projects/automation/orchestrator.py)
*   **Purpose**: The central state machine managing the lifecycle (Watcher -> Fetcher -> Setup -> Review -> Feedback).
*   **Dependencies**: `claude_agent_sdk`, `gmail_agent.py`, `browser_agent.py`, `project_manager.py`.

#### [NEW] [config.py](file:///Users/sharad/Projects/udacity-reviews-hq/projects/automation/config.py)
*   **Purpose**: Configuration for paths (`projects.json`), email filters, and constants.

### Agents & Tools
#### [NEW] [gmail_agent.py](file:///Users/sharad/Projects/udacity-reviews-hq/projects/automation/agents/gmail_agent.py)
*   **Purpose**: Polls `support@udacity.com` for emails with subject "You have been assigned a review".
*   **Tools**: `gmail_api` (or similar access method, strictly read-only for triggers).

#### [NEW] [browser_agent.py](file:///Users/sharad/Projects/udacity-reviews-hq/projects/automation/agents/browser_agent.py)
*   **Purpose**: Headless browser automation (Puppeteer/Playwright) to login, navigate to dashboard, and download projects.
*   **Traits**: Uses persistence (user profile).
*   **Config**: Targeted URL is constant: `https://mentor-dashboard.udacity.com/queue/overview`.
*   **Error Handling**: If navigation fails (redirects to login), trigger `wait_for_manual_login()`:
    1.  Log Error (Console + potential Alert).
    2.  Pause execution.
    3.  Wait for user Input (CLI Keypress) confirming they have logged in.
    4.  Retry navigation.

#### [NEW] [project_manager.py](file:///Users/sharad/Projects/udacity-reviews-hq/projects/automation/agents/project_manager.py)
*   **Purpose**: Handles local file system operations.
*   **Functions**:
    *   `locate_download()`: Finds the zip.
    *   `run_setup(project_name)`: Triggers `setup_next_student.sh` (Must be idempotent).
    *   `read_context(project_name)`: Reads `notes.txt`.

#### [NEW] [reviewer_agent.py](file:///Users/sharad/Projects/udacity-reviews-hq/projects/automation/agents/reviewer_agent.py)
*   **Purpose**: The expert evaluator.
*   **Instructions**: Dynamically loaded from `notes.txt` and `criteria_prompts`.
*   **Capabilities**: Read files, execute analysis commands, write to `feedback/`.

## Verification Plan

### Automated Tests
*   **Unit Tests**: Test the email parser with sample emails.
*   **Integration Test**: Run the `Librarian` phase against a dummy downloaded zip to verify `setup_next_student.sh` triggering.

### Manual Verification
*   **End-to-End Run**:
    1.  Send a self-email mimicking Udacity.
    2.  Verify the agent wakes up.
    3.  Verify it downloads (mocked if no real review available).
    4.  Verify it runs `setup_next_student.sh`.
    5.  Verify it generates feedback in `feedback/`.
    6.  **Stop**: Verify the process halts for human review.
