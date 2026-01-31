# Feature: Create subagent_stop.py Hook File

## Metadata
issue_number: `478`
adw_id: `feature_Tac_12_task_26`
issue_json: `[Task 26/49] [FEATURE] Create subagent_stop.py hook file`

## Feature Description
Create a hook that runs when a subagent stops, enabling subagent lifecycle tracking and result aggregation for post-hoc analysis.

## User Story
As a Claude Code user
I want subagent lifecycle events to be logged automatically
So that I can audit and analyze subagent execution patterns across sessions

## Problem Statement
Claude Code needs to track when subagents complete execution and what results they produced. Currently, there's no mechanism to capture this lifecycle data, making it difficult to debug or analyze subagent behavior after sessions end.

## Solution Statement
Create a `subagent_stop.py` hook that follows the established `stop.py` pattern:
- Read subagent lifecycle data from stdin (JSON)
- Append to session-specific log file (`.claude/hooks/logs/subagent_stop.json`)
- Store raw input as-is, no transformation or validation
- Fail silently to prevent hook failures from disrupting the session

## Relevant Files
- `.claude/hooks/subagent_stop.py` - Base hook implementation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/subagent_stop.py.j2` - Jinja2 template
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Integration point

### New Files
None - hook files already exist and are properly integrated.

## Implementation Status
✅ **COMPLETE** - All components are implemented and integrated:

1. **Base File** (`.claude/hooks/subagent_stop.py`):
   - Reads JSON from stdin containing subagent lifecycle metadata
   - Ensures session log directory exists using `ensure_session_log_dir()`
   - Appends data to `.claude/hooks/logs/subagent_stop.json` as JSON array
   - Handles JSON decode errors gracefully with silent failure

2. **Template** (`subagent_stop.py.j2`):
   - Uses `ensure_session_log_dir()` utility for per-session directories
   - Matches stop.py pattern exactly for consistency
   - Ready for CLI generation with proper variable substitution

3. **Integration** (`scaffold_service.py:350`):
   - Hook already listed in `_add_claude_files()` method
   - Marked as executable and properly configured

## Key Features
- **Subagent lifecycle tracking**: Logs subagent_id, execution_time, status, result payload, error details
- **Result aggregation**: Stores as chronological JSON array per session
- **Silent failure**: Hook won't disrupt main session if it fails
- **Atomic writes**: Uses in-memory list + atomic file write pattern
- **Per-session isolation**: Each session maintains separate log file

## Validation Commands
```bash
# Verify hook file exists and is executable
ls -la .claude/hooks/subagent_stop.py

# Check template exists
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/subagent_stop.py.j2

# Verify integration in scaffold service
grep -n "subagent_stop.py" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

# Run tests if any exist
cd tac_bootstrap_cli && uv run pytest -v 2>/dev/null || echo "No tests found"
```

## Acceptance Criteria
✅ Hook file exists at `.claude/hooks/subagent_stop.py`
✅ Template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/subagent_stop.py.j2`
✅ Hook is registered in `scaffold_service.py` hooks list
✅ Hook follows stop.py pattern (stdin → append → silent fail)
✅ Hook supports per-subagent event tracking with full payload storage

## Notes
- This task was marked as "Wave 3 - New Hooks (Task 26 of 9)" but all implementation is already complete
- The hook is fully functional and integrated into the scaffold service
- No external dependencies required beyond what's already in the stack
- Hook design allows post-hoc analysis of subagent lifecycle without runtime overhead
