# E2E Test Runner

Run end-to-end (E2E) tests using Playwright browser automation (MCP Server).

## When to Use This Command

- When the project has a web UI (frontend)
- When E2E test files exist in `.claude/commands/e2e/`
- NOT for unit tests (use `/test` for those)

## Variables

adw_id: $ARGUMENT if provided, otherwise generate 8-character hex string
agent_name: $ARGUMENT if provided, otherwise use 'test_e2e'
e2e_test_file: $ARGUMENT
application_url: $ARGUMENT if provided, otherwise use default http://localhost:5173

## Instructions

- If `application_url` is not provided, use default http://localhost:5173
- Read the `e2e_test_file`
- Digest the `User Story` to understand what is being validated
- IMPORTANT: Execute the `Test Steps` detailed in `e2e_test_file` using Playwright
- Review `Success Criteria` and if any fails, mark test as failed
- Capture screenshots as specified
- IMPORTANT: Return results in the `Output Format`
- Initialize Playwright browser in headed mode for visibility
- Use the URL determined from `application_url`
- Allow time for async operations and element visibility
- If there's an error, mark test as failed immediately and explain which step failed

## Setup

Read and Execute `.claude/commands/prepare_app.md` to prepare the application.

## Screenshot Directory

<absolute path to codebase>/agents/<adw_id>/<agent_name>/img/<directory name based on test file name>/*.png

Each screenshot should be saved with a descriptive name. The directory structure ensures that:
- Screenshots are organized by ADW ID (workflow run)
- They are stored under the specified agent name
- Each test has its own subdirectory based on the test file name

## Report

- Return exclusively the JSON output specified in the test file
- Capture unexpected errors
- IMPORTANT: Ensure all screenshots are in `Screenshot Directory`

### Output Format

```json
{
  "test_name": "Test Name Here",
  "status": "passed|failed",
  "screenshots": [
    "<absolute path>/agents/<adw_id>/<agent_name>/img/<test name>/01_<descriptive name>.png"
  ],
  "error": null
}
```
