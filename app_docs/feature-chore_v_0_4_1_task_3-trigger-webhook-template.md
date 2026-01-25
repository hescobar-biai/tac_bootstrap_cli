---
doc_type: feature
adw_id: chore_v_0_4_1_task_3
date: 2026-01-25
idk:
  - webhook
  - fastapi
  - github-events
  - adw-trigger
  - template
  - user-assignment
  - background-workflow
tags:
  - feature
  - template
  - adw-trigger
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2
---

# Trigger Webhook Template

**ADW ID:** chore_v_0_4_1_task_3
**Date:** 2026-01-25
**Specification:** specs/issue-219-adw-chore_v_0_4_1_task_3-sdlc_planner-create-trigger-webhook-template.md

## Overview

Created the missing `trigger_webhook.py.j2` template by copying the complete, tested implementation from the root directory. This template enables generated TAC Bootstrap projects to receive GitHub webhook events and automatically trigger AI Developer Workflows (ADW) in response to issue creation or comments.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2` (360 lines)
- Complete FastAPI webhook server implementation
- GitHub user assignment validation before workflow execution
- Background workflow launching to meet GitHub's 10-second timeout
- Support for both standard and isolated ADW workflows

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2`: Created new template by copying from root `adws/adw_triggers/trigger_webhook.py`

### Key Changes

- **Complete webhook server**: FastAPI app with `/gh-webhook` POST endpoint that processes GitHub issue events (opened, comment created)
- **User assignment validation**: Checks if issue is assigned to current GitHub user before triggering workflows, prevents unauthorized workflow execution
- **Background workflow execution**: Launches ADW workflows as background processes to respond to GitHub within timeout
- **Workflow parsing**: Extracts workflow directives from issue body or comments (e.g., `/adw_sdlc_iso`, `/adw_patch_iso`)
- **Dependent workflow protection**: Blocks direct triggering of dependent workflows (build, test, review, document, ship) that require existing worktrees
- **Health check endpoint**: `/health` endpoint for monitoring and service verification

## How to Use

When you generate a new TAC Bootstrap project using the CLI, the `trigger_webhook.py` file will be created in the `adws/adw_triggers/` directory.

1. **Generate a project** with TAC Bootstrap CLI
2. **Configure environment** variables in generated project:
   - `PORT`: Server port (default: 8001)
   - `GITHUB_PAT`: GitHub Personal Access Token
   - `ANTHROPIC_API_KEY`: For AI workflows
3. **Start the webhook server**:
   ```bash
   cd <generated-project>
   uv run adws/adw_triggers/trigger_webhook.py
   ```
4. **Configure GitHub webhook** pointing to your server at `/gh-webhook`
5. **Create or comment on issues** with workflow directives like:
   - `/adw_sdlc_iso` - Full SDLC workflow
   - `/adw_patch_iso` - Quick patch workflow

## Configuration

The webhook server can be configured via environment variables:

- **PORT**: Port to run the webhook server (default: 8001)
- **GITHUB_PAT**: Required for GitHub API operations
- **ANTHROPIC_API_KEY**: Required for AI workflows

Workflow directives in issue body or comments:
- Must include workflow name (e.g., `/adw_sdlc_iso`)
- Optional: `/adw_id: <custom_id>` to specify custom workflow ID
- Optional: `/model_set: <model_config>` to specify AI model configuration

## Testing

Test template file was created correctly:

```bash
cd tac_bootstrap_cli
ls -la tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2
```

Verify template line count matches source (360 lines):

```bash
wc -l tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2
```

Run unit tests to ensure no regressions:

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

Verify linting passes:

```bash
cd tac_bootstrap_cli
uv run ruff check .
```

Test CLI smoke test:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap --help
```

## Notes

- This template is a direct copy from the root implementation with no Jinja2 variable substitution needed
- The source file at `adws/adw_triggers/trigger_webhook.py` is the canonical reference (361 lines including newline)
- Template preserves critical user assignment validation logic that prevents workflows from running unless issue is assigned to current GitHub user
- Startup message displays current GitHub user for verification
- Background process execution ensures webhook responds within GitHub's 10-second timeout requirement
- Template complements existing trigger templates: `trigger_cron.py.j2`, `trigger_issue_chain.py.j2`, `trigger_polling.py.j2`
