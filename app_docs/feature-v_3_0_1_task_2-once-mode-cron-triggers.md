---
doc_type: feature
adw_id: feature_v_3_0_1_task_2
date: 2026-01-25
idk:
  - cron-trigger
  - single-execution
  - adw-trigger
  - testing-mode
  - scheduler
  - ci-cd
tags:
  - feature
  - testing
  - automation
related_code:
  - adws/adw_triggers/trigger_cron.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2
  - tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py
  - tac_bootstrap_cli/tests/test_value_objects.py
---

# Once-Mode Execution for Cron Triggers

**ADW ID:** feature_v_3_0_1_task_2
**Date:** 2026-01-25
**Specification:** specs/issue-205-adw-feature_v_3_0_1_task_2-sdlc_planner-add-once-mode-triggers.md

## Overview

Added a `--once` flag to the cron trigger system that executes a single check cycle and exits cleanly. This enables testing, debugging, and CI/CD integration without running an infinite loop daemon.

## What Was Built

- `--once` command-line argument for single-execution mode
- Conditional execution logic that bypasses scheduler setup in once-mode
- Updated documentation in module docstrings with usage examples
- Identical implementation in both source file and Jinja2 template
- Minor bugfix in SemanticVersion docstring (0.3.0 > 0.2.0 typo correction)

## Technical Implementation

### Files Modified

- `adws/adw_triggers/trigger_cron.py`: Added `--once` argument to argument parser, implemented single-execution mode logic in `main()`, updated module docstring with usage example
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`: Identical changes to template version to ensure generated projects have once-mode capability
- `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py`: Fixed typo in SemanticVersion docstring (0.3.0 > 0.2.0 instead of 0.3.0 > 0.3.0)
- `tac_bootstrap_cli/tests/test_value_objects.py`: Updated test assertions to match corrected docstring

### Key Changes

1. **Argument Parser Extension**: Added `--once` boolean flag with `action="store_true"` to enable single-execution mode through command-line interface
2. **Early-Return Pattern**: Implemented conditional check in `main()` that executes `check_and_process_issues()` once and returns before scheduler initialization when `--once` is True
3. **Scheduler Bypass**: Single-execution mode skips all `schedule` library setup, making it faster and more deterministic
4. **Consistent Logging**: Added INFO-level messages marking entry ("Running single check cycle") and exit ("Single cycle complete, exiting") for once-mode
5. **Template Synchronization**: Ensured Jinja2 template has identical implementation so all generated projects inherit this capability

## How to Use

### Running Single Check Cycle

Execute the cron trigger in once-mode for testing or one-time runs:

```bash
uv run adws/adw_triggers/trigger_cron.py --once
```

This will:
1. Initialize signal handlers
2. Run `check_and_process_issues()` exactly once
3. Exit cleanly with code 0 (or non-zero on exceptions)

### Normal Continuous Mode

Run without `--once` for the default infinite loop behavior:

```bash
uv run adws/adw_triggers/trigger_cron.py --interval 30
```

### Using in Generated Projects

When using TAC Bootstrap CLI to generate new projects, the trigger template will include the `--once` functionality automatically:

```bash
# In generated project
uv run adws/adw_triggers/trigger_cron.py --once
```

## Configuration

### Command-Line Arguments

- `--once`: Run single check cycle and exit (no value required)
- `--interval N` / `-i N`: Set polling interval in seconds (ignored in once-mode)

### Environment Variables

No new environment variables. Existing trigger configuration (GitHub token, repo settings) applies to both modes.

## Testing

### Verify Help Text Shows New Flag

```bash
uv run adws/adw_triggers/trigger_cron.py --help | grep -A1 "\-\-once"
```

Expected output should show the `--once` argument with description "Run a single check cycle and exit (useful for testing)".

### Test Single Execution Mode Exits Cleanly

```bash
timeout 10 uv run adws/adw_triggers/trigger_cron.py --once && echo "SUCCESS: Exited cleanly"
```

The trigger should complete within the timeout and print "SUCCESS: Exited cleanly".

### Verify Normal Mode Still Works

```bash
timeout 5 uv run adws/adw_triggers/trigger_cron.py --interval 2 || [ $? -eq 124 ] && echo "SUCCESS: Normal mode runs continuously"
```

The command should hit the timeout (exit code 124) proving the infinite loop still works, then print "SUCCESS: Normal mode runs continuously".

### Verify Template Consistency

```bash
diff -u <(grep -A10 "def parse_args" adws/adw_triggers/trigger_cron.py | grep -v "^#") \
        <(grep -A10 "def parse_args" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2 | grep -v "^#" | grep -v "{{" | grep -v "}}") \
        || echo "NOTE: Template may have Jinja2 variables, verify manually"
```

### Run Existing Tests

```bash
uv run pytest tac_bootstrap_cli/tests/test_value_objects.py -v
```

All tests should pass including the updated semantic version comparison test.

## Notes

- The `--once` flag is compatible with `--interval` but the interval is simply ignored in single-execution mode
- Signal handlers (SIGINT/SIGTERM) remain active even in `--once` mode, allowing graceful interruption via Ctrl+C
- Exceptions raised by `check_and_process_issues()` will propagate and cause non-zero exit codes, enabling proper error detection in CI/CD
- The early-return pattern keeps the code simple and avoids conditional logic scattered throughout the scheduler loop
- This feature is particularly useful for CI/CD pipelines that need deterministic execution without managing long-running daemons
- Future enhancements could add timing metrics or dry-run modes specific to single-execution
- The SemanticVersion bugfix (0.3.0 > 0.2.0 correction) was discovered during test validation and fixed as part of this feature work
