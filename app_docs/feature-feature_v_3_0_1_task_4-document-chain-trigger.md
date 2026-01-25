---
doc_type: feature
adw_id: feature_v_3_0_1_task_4
date: 2026-01-25
idk:
  - documentation
  - trigger_issue_chain
  - sequential-processing
  - automation
  - github-issues
  - readme
tags:
  - feature
  - documentation
  - automation
related_code:
  - adws/README.md
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2
  - adws/adw_triggers/trigger_issue_chain.py
---

# Document Chain Trigger in README

**ADW ID:** feature_v_3_0_1_task_4
**Date:** 2026-01-25
**Specification:** specs/issue-207-adw-feature_v_3_0_1_task_4-sdlc_planner-document-chain-trigger.md

## Overview

This feature adds comprehensive documentation for the `trigger_issue_chain.py` automation trigger to the ADWs README files. The chain trigger enables sequential processing of GitHub issues, waiting for each issue to close before starting the next one in the chain.

## What Was Built

- Added complete documentation section for `trigger_issue_chain.py` in `adws/README.md`
- Updated template file `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` to include chain trigger in directory structure
- Documentation includes usage examples, behavior description, use cases, and workflow examples

## Technical Implementation

### Files Modified

- `adws/README.md`: Added new subsection "trigger_issue_chain.py - Sequential Issue Processing" within the "Automation Triggers" section (after `trigger_cron.py`, before `trigger_webhook.py`)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`: Updated directory structure to include `trigger_issue_chain.py` alongside other triggers

### Key Changes

- **Documentation Structure**: New section positioned logically between cron and webhook triggers, following existing format patterns
- **Usage Examples**: Four distinct command examples demonstrating positional arguments, `--issues` flag, `--interval` customization, and `--once` testing mode
- **Behavioral Documentation**: Clear explanation of sequential processing logic (only first open issue processed, waits for closure before next)
- **Use Cases**: Three primary scenarios for chain trigger usage (dependent issues, ordered implementation, batch processing)
- **Workflow Example**: Complete 5-step example showing creation of issues and processing flow

## How to Use

The documentation now provides users with complete information about using the chain trigger:

1. **Basic Usage** (positional arguments):
   ```bash
   uv run adw_triggers/trigger_issue_chain.py 123 456 789
   ```

2. **Using `--issues` flag**:
   ```bash
   uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789
   ```

3. **Custom polling interval**:
   ```bash
   uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --interval 30
   ```

4. **Single check cycle** (for testing):
   ```bash
   uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --once
   ```

## Configuration

No additional configuration required. The documentation is now part of the standard ADWs README that is included in:
- The root `adws/` directory for this repository
- Generated projects created by TAC Bootstrap CLI (via template)

## Testing

Verify the documentation exists and contains required examples:

```bash
# Verify section exists in root README
grep -A5 "trigger_issue_chain.py" adws/README.md
```

```bash
# Verify --issues flag examples
grep "\-\-issues" adws/README.md | head -3
```

```bash
# Check template file includes trigger in directory structure
grep "trigger_issue_chain.py" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2
```

## Notes

- The template `README.md.j2` is intentionally minimal (44 lines) compared to the comprehensive root `adws/README.md`. Only the directory structure was updated in the template, not the full documentation section
- The chain trigger documentation emphasizes sequential processing: only the first open issue in the chain is processed at any given time
- Default polling interval is 20 seconds (configurable via `--interval` flag)
- The trigger supports all ADW workflows (plan, SDLC, patch, etc.) via GitHub issue body keywords
- Documentation format is consistent with existing trigger sections (`trigger_cron.py` and `trigger_webhook.py`)
