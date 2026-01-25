---
doc_type: feature
adw_id: chore_v_0_4_1_task_8
date: 2026-01-25
idk:
  - trigger-polling
  - api-rate-limiting
  - github-api
  - configuration
  - documentation
  - cron-trigger
  - issue-chain-trigger
tags:
  - feature
  - documentation
  - configuration
related_code:
  - tac_bootstrap_cli/README.md
---

# Trigger Polling Interval Documentation

**ADW ID:** chore_v_0_4_1_task_8
**Date:** 2026-01-25
**Specification:** specs/issue-223-adw-chore_v_0_4_1_task_8-chore_planner-add-polling-interval-docs.md

## Overview

Added comprehensive documentation section to the tac_bootstrap_cli README explaining recommended polling intervals and GitHub API rate limiting considerations for the trigger systems (`trigger_cron.py` and `trigger_issue_chain.py`). This documentation helps users configure their trigger systems appropriately based on their repository's needs and API usage patterns.

## What Was Built

- Polling configuration reference table with default intervals, recommended ranges, and usage notes
- GitHub API rate limiting guidance with practical recommendations
- Documentation placement after "Issue Chain Trigger Setup" section for logical flow

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/README.md`: Added "Trigger Polling Configuration" section with polling interval recommendations and GitHub API rate limiting guidance (lines 637-648)

### Key Changes

- Added configuration table documenting default intervals (20s for both triggers) and recommended ranges (15-60s for cron, 20-120s for issue chain)
- Documented GitHub API rate limits (5,000 requests/hour for authenticated requests)
- Provided practical guidance on API call frequency (1-3 calls per open issue per polling cycle)
- Included monitoring command (`gh api rate_limit`) for users to check their current rate limit status
- Positioned documentation strategically after trigger setup instructions for contextual relevance

## How to Use

1. Navigate to the tac_bootstrap_cli README.md file
2. Locate the "Trigger Polling Configuration" section (after "Issue Chain Trigger Setup")
3. Reference the table to determine appropriate polling intervals for your use case:
   - For repos with few open issues: Use default 20s or lower (15s minimum for cron)
   - For repos with many open issues: Use longer intervals (30s-120s) to avoid rate limits
4. Monitor your API usage with the provided command to ensure you stay within limits

## Configuration

The documentation covers two trigger types with specific interval recommendations:

- **trigger_cron.py**: Default 20s, recommended range 15-60s (lower intervals increase API usage)
- **trigger_issue_chain.py**: Default 20s, recommended range 20-120s (sequential processing, less frequent polling acceptable)

Users should consider:
- Number of open issues in their repository
- GitHub API rate limit of 5,000 authenticated requests/hour
- Each polling cycle makes 1-3 API calls per open issue
- Longer intervals (30s+) recommended for repositories with many open issues

## Testing

Validate the documentation is properly formatted:

```bash
cd tac_bootstrap_cli && cat README.md | grep -A 15 "Trigger Polling Configuration"
```

Run validation commands to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify linting passes:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is a documentation-only change with no code modifications
- The polling intervals are based on existing trigger implementations
- GitHub API rate limit information is current as of January 2025
- Users can monitor their rate limit usage with `gh api rate_limit` to optimize polling intervals
- The documentation provides a starting point; users should adjust based on their specific repository activity and API usage patterns
