# Track Agentic KPIs Template

**ADW ID:** 18f94bef
**Date:** 2026-01-21
**Specification:** specs/issue-45-adw-18f94bef-sdlc_planner-create-track-agentic-kpis-template.md

## Overview

Created the Jinja2 template for the `/track_agentic_kpis` slash command that enables TAC Bootstrap-generated projects to track and analyze the four core KPIs of Tactical Agentic Coding: SIZE, ATTEMPTS, STREAK, and PRESENCE. This command automates performance measurement for AI Developer Workflows (ADWs).

## What Was Built

- Complete Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2`
- Command structure following TAC Bootstrap template conventions
- Integration with ADW state JSON parsing
- Comprehensive KPI calculation logic using Python
- Dual-table tracking system (Agentic KPIs summary + ADW KPIs detailed)
- Markdown output formatting for `app_docs/agentic_kpis.md`

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/track_agentic_kpis.md.j2`: Created complete template (131 lines)

### Key Changes

- Implemented state_json parsing to extract adw_id, issue_number, issue_class, plan_file, and all_adws list
- Added Python-based calculation commands for all numeric metrics (attempts count, plan size, diff statistics)
- Created instructions for reading and updating existing `app_docs/agentic_kpis.md` file
- Implemented logic for calculating 7 aggregate Agentic KPIs: Current Streak, Longest Streak, Total Plan Size, Largest Plan Size, Total Diff Size, Largest Diff Size, and Average Presence
- Added detailed file structure specification with markdown table formatting
- Emphasized Python calculations to ensure accuracy across all numeric operations

## How to Use

When TAC Bootstrap generates an agentic layer for a project, this template creates the `/track_agentic_kpis` command. To use:

1. Run an ADW workflow (e.g., `/feature`, `/patch`, `/bug`) which generates state JSON
2. Execute `/track_agentic_kpis` with the state JSON as arguments
3. The command will:
   - Parse the ADW execution data
   - Calculate metrics (attempts, plan size, diff statistics)
   - Update or create `app_docs/agentic_kpis.md`
   - Display both summary and detailed KPI tables

Example in a generated project:
```bash
# After running an ADW workflow
/track_agentic_kpis $STATE_JSON
```

## Configuration

The template uses these configuration variables from TACConfig:

- `{{ config.paths.logs_dir }}`: Directory where ADW execution logs are stored (referenced for future log parsing)

The template defines these local variables:

- `state_json: $ARGUMENTS`: Receives ADW state data as JSON
- `attempts_incrementing_adws: [adw_plan_iso, adw_patch_iso]`: List of workflows that increment attempt counters

## Testing

The template itself is validated during TAC Bootstrap CLI tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

To test in a generated project:

1. Generate a new project with `tac-bootstrap init`
2. Run an ADW workflow to generate state
3. Execute `/track_agentic_kpis` with the state JSON
4. Verify `app_docs/agentic_kpis.md` is created/updated correctly
5. Check that calculations match expected values

## Notes

- This is one of the most complex slash command templates in TAC Bootstrap, implementing sophisticated metric tracking
- The template follows the exact structure and logic of the reference implementation in `.claude/commands/track_agentic_kpis.md`
- All calculations use Python commands to ensure cross-platform consistency and numerical accuracy
- The dual-table system provides both high-level summary (Agentic KPIs) and granular detail (ADW KPIs per workflow run)
- This command enables teams to measure and improve their agentic engineering practices systematically
- The four KPIs (SIZE, ATTEMPTS, STREAK, PRESENCE) come directly from Lesson 8 of the TAC course
- Future enhancement consideration: Adding trend visualization with charts or graphs
- The template uses Jinja2 list syntax for arrays, not Python list syntax, to ensure proper rendering
- Emphasis on Python calculations prevents shell-specific inconsistencies and ensures reliable metric tracking
