---
doc_type: feature
adw_id: chore_Tac_10_task_10
date: 2026-01-27
idk:
  - changelog
  - semantic-versioning
  - release-management
  - configuration
  - version-control
tags:
  - feature
  - chore
  - documentation
related_code:
  - CHANGELOG.md
  - tac_bootstrap_cli/pyproject.toml
---

# Update CHANGELOG and Version to 0.5.1

**ADW ID:** chore_Tac_10_task_10
**Date:** 2026-01-27
**Specification:** specs/issue-323-adw-chore_Tac_10_task_10-sdlc_planner-update-changelog-version.md

## Overview

This chore documents all changes introduced during the TAC-10 iteration by updating the CHANGELOG.md file and incrementing the project version from 0.5.0 to 0.5.1 in pyproject.toml. The update reflects the addition of new advanced command templates, hooks, and scaffold structure changes.

## What Was Built

- Updated CHANGELOG.md with version 0.5.1 entry documenting TAC-10 iteration changes
- Incremented package version in tac_bootstrap_cli/pyproject.toml from 0.5.0 to 0.5.1
- Documented 7 new additions including templates for parallel_subagents, t_metaprompt_workflow, cc_hook_expert_improve, build_w_report, and hook system enhancements
- Recorded 2 key changes to settings.json.j2 and scaffold_service.py

## Technical Implementation

### Files Modified

- `CHANGELOG.md`: Added new [0.5.1] section with 15 lines documenting Added and Changed items from TAC-10 iteration
- `tac_bootstrap_cli/pyproject.toml`: Updated version field from "0.5.0" to "0.5.1" on line 3
- `.mcp.json`: Minor configuration update (2 lines changed)
- `playwright-mcp-config.json`: Minor configuration update (2 lines changed)
- `tac_bootstrap_cli/uv.lock`: Lockfile automatically updated to reflect new version

### Key Changes

- **CHANGELOG.md**: Inserted new version section following Keep a Changelog format, dated 2026-01-26, positioned before the [0.5.0] entry
- **Version Increment**: Applied Semantic Versioning patch increment (0.5.0 → 0.5.1) for backward-compatible additions
- **TAC-10 Documentation**: Captured 7 new templates for advanced agentic patterns (Levels 4, 6, 7) including multi-agent delegation, meta-prompt generation, and self-improvement
- **Hook System Evolution**: Documented addition of 6 new hook types (UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd) with universal logging integration
- **Scaffold Structure**: Recorded new `agents/hook_logs/` and `agents/context_bundles/` directory creation in generated projects

## How to Use

This release documentation is automatically consumed when:

1. Users view the CHANGELOG.md to understand what changed in version 0.5.1
2. Package managers and tools read pyproject.toml to identify the current version
3. Generated projects include these new templates and structure automatically via `tac-bootstrap init`

To verify the changes:

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
cat CHANGELOG.md | grep -A 20 "0.5.1"
```

To check version in pyproject.toml:

```bash
cd tac_bootstrap_cli
grep "^version" pyproject.toml
```

## Configuration

No additional configuration required. The version update affects:
- Package installation: `pip install tac-bootstrap==0.5.1`
- Version reporting: `tac-bootstrap --version`
- Changelog reference for release notes and migration guides

## Testing

Run the complete test suite to verify no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify linting passes:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run smoke test to ensure CLI loads correctly:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is a documentation and versioning chore with no functional code changes
- Version 0.5.1 follows Semantic Versioning as a patch increment
- The CHANGELOG entry is inserted in descending chronological order (most recent first)
- All documented changes correspond to the complete TAC-10 iteration deliverables
- Date format follows ISO 8601 (YYYY-MM-DD) as specified in Keep a Changelog format
- The documented templates enable advanced agentic capabilities: parallel delegation (Level 4), meta-prompt workflows (Level 6), and self-improvement cycles (Level 7) from the TAC framework
