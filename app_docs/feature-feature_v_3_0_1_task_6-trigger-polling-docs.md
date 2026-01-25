---
doc_type: feature
adw_id: feature_v_3_0_1_task_6
date: 2026-01-25
idk:
  - trigger-polling
  - github-api
  - rate-limiting
  - configuration
  - cli-flags
  - documentation
tags:
  - feature
  - documentation
  - triggers
related_code:
  - adws/README.md
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2
---

# Trigger Polling Configuration Documentation

**ADW ID:** feature_v_3_0_1_task_6
**Date:** 2026-01-25
**Specification:** specs/issue-209-adw-feature_v_3_0_1_task_6-sdlc_planner-trigger-polling-docs.md

## Overview

Added comprehensive documentation about ADW trigger polling configuration to help users understand default polling intervals, customize them via CLI flags, and avoid GitHub API rate limiting. The documentation includes recommended intervals for different use cases (development, production, CI/CD) with rationale and API limit calculations.

## What Was Built

Documentation additions covering:
- Default polling interval specification (20 seconds)
- CLI flag usage examples (`--interval` and `-i`)
- Recommended intervals table organized by use case
- GitHub API rate limiting calculations and guidance
- Added to both root README and Jinja2 template for consistency

## Technical Implementation

### Files Modified

- `adws/README.md` (lines 647-680): Added new "Trigger Polling Configuration" subsection within the Configuration section, positioned after "ADW Tracking" and before "Target Branch"
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`: Replicated identical documentation in the template with appropriate Jinja2 variables for package manager commands

### Key Changes

- Created structured documentation explaining the 20-second default polling interval that was previously only discoverable in source code
- Documented CLI override flags (`--interval` / `-i`) with practical examples showing different interval values
- Built comprehensive table mapping 4 use cases to recommended intervals: Development/Testing (10-20s), Production light (30-60s), Production heavy (60-120s), and CI/CD (--once flag)
- Included GitHub API rate limiting calculations showing ~180-540 calls/hour at default 20s interval against 5,000/hour limit
- Maintained consistency by updating both the working README and the Jinja2 template used for generating new projects

## How to Use

### For End Users

When running ADW triggers, users can now refer to the README for guidance on:

1. Understanding the default behavior (20-second polling)
2. Customizing intervals based on their use case
3. Avoiding API rate limits

Example from documentation:
```bash
# Poll every 30 seconds
uv run adw_triggers/trigger_cron.py --interval 30

# Poll every 60 seconds
uv run adw_triggers/trigger_issue_chain.py --issues 1,2,3 -i 60
```

### For Developers

The template ensures generated projects include this documentation:
- Users running `tac-bootstrap init` will get the updated README.md.j2 template
- Generated projects automatically include polling configuration guidance
- Jinja2 variables adapt commands to the project's package manager

## Configuration

No configuration changes were required. This is documentation-only, clarifying existing CLI flag behavior:
- `--interval N` or `-i N`: Sets polling interval to N seconds
- `--once`: Single execution without polling (for CI/CD)

## Testing

Verify the documentation was added correctly:

```bash
# Verify section exists in root README
grep -A3 "Trigger Polling Configuration" adws/README.md
```

```bash
# Verify default interval documented
grep "20 seconds" adws/README.md
```

```bash
# Verify table exists (should be >= 2 matches)
grep -c "Interval" adws/README.md
```

```bash
# Verify template updated
grep "Trigger Polling Configuration" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2
```

```bash
# Visual inspection of formatting
grep -A10 "### Trigger Polling Configuration" adws/README.md
```

```bash
# Visual inspection of template formatting
grep -A10 "### Trigger Polling Configuration" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2
```

## Notes

- This is a documentation-only change with zero code impact
- The 20-second default is hardcoded in trigger implementations, not yet configurable via `config.yml`
- Future enhancement could add `config.yml` support for project-wide default intervals
- Documentation helps users make informed decisions about polling frequency based on their GitHub API usage patterns
- The table format provides quick reference for common scenarios without requiring users to do rate limit math themselves
