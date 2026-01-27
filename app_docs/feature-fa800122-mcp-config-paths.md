---
doc_type: feature
adw_id: fa800122
date: 2026-01-27
idk:
  - configuration
  - mcp
  - playwright
  - relative-paths
  - portability
tags:
  - chore
  - configuration
  - maintenance
related_code:
  - .mcp.json
  - playwright-mcp-config.json
  - tac_bootstrap_cli/tests/test_value_objects.py
---

# MCP Configuration Path Normalization

**ADW ID:** fa800122
**Date:** 2026-01-27
**Specification:** specs/issue-4-adw-fa800122-chore_planner-configure-dependencies.md

## Overview

This chore normalized MCP (Model Context Protocol) configuration files to use relative paths instead of absolute paths. The change makes the configuration portable across different worktrees and machines, eliminating hardcoded paths specific to a single ADW worktree.

## What Was Built

- Converted absolute paths to relative paths in `.mcp.json`
- Converted absolute paths to relative paths in `playwright-mcp-config.json`
- Fixed a test assertion in `test_value_objects.py` for semantic version comparison

## Technical Implementation

### Files Modified

- `.mcp.json`: Updated Playwright MCP server config path from absolute to relative
- `playwright-mcp-config.json`: Updated video recording directory from absolute to relative
- `tac_bootstrap_cli/tests/test_value_objects.py`: Fixed test assertion logic

### Key Changes

1. **MCP Config Portability**: Changed `--config` argument from `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/fa800122/playwright-mcp-config.json` to `./playwright-mcp-config.json`

2. **Video Directory Path**: Changed Playwright video recording directory from `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/fa800122/videos` to `./videos`

3. **Test Fix**: Corrected `test_less_than_with_string()` to properly test less-than comparison:
   - Changed from `assert v1 < "0.6.0"` (comparing 0.6.0 < 0.6.0, which is false)
   - To `assert v1 < "0.7.0"` (comparing 0.6.0 < 0.7.0, which is true)

## How to Use

These configuration changes are transparent to end users. The MCP server will automatically resolve relative paths from the project root directory.

1. The MCP server config at `.mcp.json` now references the Playwright config using a relative path
2. Playwright will record videos to the `./videos` directory relative to the project root
3. This works seamlessly across different worktrees and machines without modification

## Configuration

No additional configuration is required. The changes make the existing MCP and Playwright configurations more flexible:

- **MCP Config**: `.mcp.json` uses relative path `./playwright-mcp-config.json`
- **Video Directory**: Playwright records to `./videos` relative to project root

## Testing

Validate JSON syntax and run existing tests:

```bash
python -m json.tool .mcp.json > /dev/null && echo "✓ .mcp.json is valid JSON"
```

```bash
python -m json.tool playwright-mcp-config.json > /dev/null && echo "✓ playwright-mcp-config.json is valid JSON"
```

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is a maintenance chore focused on portability and configuration normalization
- The test fix in `test_value_objects.py` corrects an invalid assertion that was comparing a version to itself
- Relative paths enable the configuration to work across different ADW worktrees without modification
- No new features or functionality were added, only path normalization for existing configurations
