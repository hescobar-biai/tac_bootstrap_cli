# Chore: Update CHANGELOG.md and increment version to 0.6.0

## Metadata
issue_number: `363`
adw_id: `chore_Tac_11_task_20`
issue_json: `{"number":363,"title":"Update CHANGELOG.md and increment version to 0.6.0","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_20\n\nUpdate the changelog with all TAC-11 integration changes and increment version.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`\n\n**Implementation details:**\n- Increment version from 0.5.1 to 0.6.0\n- Add section for v0.6.0 with date\n- Document new features:\n  - Security hook: dangerous_command_blocker.py\n  - New command: /scout (multi-model parallel search)\n  - New command: /question (read-only Q&A)\n  - New trigger: trigger_issue_parallel.py (parallel workflow execution)\n  - New directories: agents/security_logs/, agents/scout_files/\n- Document template additions\n- Reference TAC-11 as source\n- Verify template paths are correct"}`

## Chore Description
Update CHANGELOG.md to document all TAC-11 integration changes and increment project version from 0.5.1 to 0.6.0. This chore consolidates documentation for new security features, commands, triggers, and directory structures introduced in the TAC-11 task series.

## Relevant Files
Files required for completing this chore:

- `CHANGELOG.md` - Main changelog file that needs version 0.6.0 section added with TAC-11 features
- `.claude/commands/scout.md` - Verify /scout command exists and understand its features
- `.claude/commands/question.md` - Verify /question command exists and understand its features
- `.claude/hooks/dangerous_command_blocker.py` - Verify security hook exists
- `adws/adw_triggers/trigger_issue_parallel.py` - Verify parallel trigger exists
- `tac_bootstrap_cli/templates/.claude/commands/scout.md.j2` - Verify template exists
- `tac_bootstrap_cli/templates/.claude/commands/question.md.j2` - Verify template exists
- `tac_bootstrap_cli/templates/.claude/hooks/dangerous_command_blocker.py.j2` - Verify template exists
- `tac_bootstrap_cli/templates/adws/adw_triggers/trigger_issue_parallel.py.j2` - Verify template exists

### New Files
None - only updating existing CHANGELOG.md

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify TAC-11 features exist
- Read `.claude/commands/scout.md` to confirm /scout command implementation
- Read `.claude/commands/question.md` to confirm /question command implementation
- Read `.claude/hooks/dangerous_command_blocker.py` to confirm security hook implementation
- Read `adws/adw_triggers/trigger_issue_parallel.py` to confirm parallel trigger implementation
- Check for existence of `agents/security_logs/` and `agents/scout_files/` directories

### Task 2: Verify template files exist
- Verify `tac_bootstrap_cli/templates/.claude/commands/scout.md.j2` exists
- Verify `tac_bootstrap_cli/templates/.claude/commands/question.md.j2` exists
- Verify `tac_bootstrap_cli/templates/.claude/hooks/dangerous_command_blocker.py.j2` exists
- Verify `tac_bootstrap_cli/templates/adws/adw_triggers/trigger_issue_parallel.py.j2` exists
- Verify scaffold creates `agents/security_logs/` and `agents/scout_files/` directories

### Task 3: Update CHANGELOG.md with v0.6.0 section
- Read current CHANGELOG.md to understand existing format
- Insert new section for v0.6.0 with current date (2026-01-27)
- Document all TAC-11 features in proper Keep a Changelog format:
  - Under "### Added":
    - Security hook: dangerous_command_blocker.py with description
    - New command: /scout (multi-model parallel search) with description
    - New command: /question (read-only Q&A) with description
    - New trigger: trigger_issue_parallel.py (parallel workflow execution) with description
    - New directories: agents/security_logs/, agents/scout_files/ with description
    - Template additions for all above features
- Reference TAC-11 as source of changes
- Follow existing changelog style and formatting

### Task 4: Run validation commands
- Execute all validation commands to ensure no regressions
- Verify CHANGELOG.md follows Keep a Changelog format
- Verify all documented features actually exist in codebase
- Verify all template paths are correct

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cat CHANGELOG.md | head -50` - Verify changelog format

## Notes
- Use Keep a Changelog format: https://keepachangelog.com/en/1.1.0/
- Use Semantic Versioning: https://semver.org/spec/v2.0.0.html
- Version 0.6.0 is a minor version bump (new features, no breaking changes)
- Current version is 0.5.1, next is 0.6.0
- TAC-11 represents a significant feature addition warranting minor version increment
- Ensure date format matches existing entries: [0.6.0] - 2026-01-27
- All new features should be documented under "### Added" section
- Reference TAC-11 for traceability
