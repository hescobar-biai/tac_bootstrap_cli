# Feature: Create load_bundle.md Command File

## Metadata
issue_number: `463`
adw_id: `feature_Tac_12_task_11`
issue_json: `{"number":463,"title":"[Task 11/49] [FEATURE] Create load_bundle.md command file","body":"## Description\n\nCreate a command that loads context bundles (pre-packaged file sets).\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_bundle.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`\n\n## Key Features\n- Pre-packaged context loading\n- Bundle definitions\n- allowed-tools: Read, Glob\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md`\n\n## Wave 1 - New Commands (Task 11 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_11"}`

## Feature Description

The `/load_bundle` command enables context recovery by loading session bundles automatically created by the `context_bundle_builder` hook. These bundles are JSONL files that track file operations (read, write, edit, notebookedit) during Claude Code sessions, allowing agents to restore context from previous work.

This feature addresses the need to resume interrupted sessions, debug agent behavior, and efficiently recover project context without manually re-reading files. Bundles contain file operation metadata (not content), making them lightweight and focused on tracking what files were accessed and how.

The command provides flexible loading options: by explicit path, by session ID, or auto-discovery of the most recent bundle. It handles missing files gracefully and provides detailed reporting on what was restored.

## User Story

As a TAC Bootstrap user generating agentic layers
I want to include the `/load_bundle` command in scaffolded projects
So that end users can recover context from previous Claude Code sessions efficiently

## Problem Statement

Projects using TAC Bootstrap need a standardized way to:
1. Resume work after session failures, timeouts, or interruptions
2. Understand what files were accessed in previous agent sessions
3. Debug agent behavior by reviewing file operation history
4. Recover context efficiently without manually identifying relevant files

Currently, the `load_bundle.md` command exists in the base repository but lacks:
- A Jinja2 template version for CLI generation
- Integration in `scaffold_service.py`'s command list
- Verification that both base and template implementations are functionally identical

## Solution Statement

Create both base and template versions of the `load_bundle.md` command that:
1. Accept optional `bundle_path` or `session_id` arguments
2. Default to loading the most recent bundle when no arguments provided
3. Parse JSONL bundle files tracking file operations
4. Re-read files to restore context, handling missing files gracefully
5. Report detailed statistics on what was loaded/missing

The implementation uses minimal Jinja2 templating (only `{{ config.paths.logs_dir }}` for configurable paths) since the command logic is project-agnostic. Integration into `scaffold_service.py` ensures the command is included in all generated projects.

## Relevant Files

### Existing Files (to verify/update)
- `.claude/commands/load_bundle.md` - Base command implementation (already exists)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` - Template version (already exists)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:279-324` - Commands list to update

### Reference Files
- `.claude/commands/load_ai_docs.md` - Similar command pattern for loading documentation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` - Template example with minimal Jinja2

### New Files
None - both files already exist per issue clarifications. This is a verification task.

## Implementation Plan

### Phase 1: Verification
Verify that both base and template implementations exist and are functionally identical.

### Phase 2: Template Refinement
Ensure the Jinja2 template uses `{{ config.paths.logs_dir }}` appropriately for configurable paths.

### Phase 3: Integration
Update `scaffold_service.py` to include `load_bundle` in the commands list (already present at line 318).

## Step by Step Tasks

### Task 1: Verify Base Implementation
- Read `.claude/commands/load_bundle.md`
- Confirm it contains:
  - Variables section with `bundle_path` and `session_id` arguments
  - Instructions explaining JSONL format and bundle location
  - Run section with 5 steps for locating, verifying, parsing, re-reading, and reporting
  - Examples showing different usage patterns
  - Report section with structured output format
- Verify allowed-tools are Read and Glob only

### Task 2: Verify Template Implementation
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`
- Confirm it matches base implementation exactly
- Verify it uses `{{ config.paths.logs_dir }}` instead of hardcoded "logs" path
- Check that no other Jinja2 variables are needed (command is project-agnostic)

### Task 3: Compare Base and Template
- Identify any differences between base and template
- If differences exist:
  - Determine which version is correct based on reference implementation
  - Update the incorrect version to match
- Ensure both use consistent JSONL schema and reporting format

### Task 4: Verify scaffold_service.py Integration
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:279-324`
- Confirm `load_bundle` is present in the commands list
- Verify it's in the correct category comment (TAC-9/10: Context and agent delegation commands)
- Check that template path is correctly referenced: `claude/commands/load_bundle.md.j2`

### Task 5: Validate Bundle Path Configuration
- Check if `config.paths.logs_dir` is defined in domain models
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py` to confirm PathsConfig includes logs_dir
- Verify default value is "logs" to match expected bundle location

### Task 6: Run Validation Commands
Execute all validation commands to ensure no regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests required - this is verification and integration work.

Existing tests should cover:
- Template rendering in `test_template_repo.py`
- Scaffold plan building in `test_scaffold_service.py`
- Command list completeness checks

### Edge Cases
The command itself handles these edge cases (no testing needed for this task):
- Missing bundle files (graceful error reporting)
- Invalid JSONL format (skip unparseable lines)
- Missing referenced files (track and report, continue loading)
- No bundles available (clear error message)

## Acceptance Criteria

1. **Base Implementation Exists**: `.claude/commands/load_bundle.md` is present and complete
2. **Template Implementation Exists**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` is present and complete
3. **Functional Equivalence**: Base and template are identical except for Jinja2 path variable
4. **Path Configuration**: Template uses `{{ config.paths.logs_dir }}` for logs directory reference
5. **Integration Complete**: `load_bundle` is included in scaffold_service.py commands list at line 318
6. **Bundle Location**: Default bundle path is `logs/context_bundles/session_{session_id}.jsonl`
7. **JSONL Schema**: Bundle entries include timestamp, operation, file_path, status, session_id, tool_input
8. **Graceful Handling**: Command handles missing files, invalid entries, and missing bundles gracefully
9. **Detailed Reporting**: Report includes bundle info, restored files, missing files, operation summary
10. **All Tests Pass**: Validation commands complete without errors

## Validation Commands

Execute in order to validate with zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

**Important Discovery**: Both base file (`.claude/commands/load_bundle.md`) and template file (`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`) already exist and are functionally identical. This task is primarily **verification** rather than creation.

**Key Implementation Details**:
- Bundle format: JSONL (JSON Lines) for append-only logging and line-by-line parsing
- Bundle location: `logs/context_bundles/session_{session_id}.jsonl`
- Bundle creation: Automated by `context_bundle_builder` hook (not manual)
- Bundle content: File operation metadata only, not file content snapshots
- Context restoration: Re-reads current files to restore context, not historical snapshots
- Naming: Session ID provides unique identification, no conflicts or versioning needed

**Template Pattern**: Follows the pattern from `load_ai_docs.md.j2` which uses minimal Jinja2 since command logic is primarily instructional content. Only path references need templating for configurability.

**Integration Status**: The command is already listed in `scaffold_service.py:318` in the "TAC-9/10: Context and agent delegation commands" section, confirming integration is complete.

**No New Dependencies**: Command uses only Read and Glob tools, no additional libraries needed.
