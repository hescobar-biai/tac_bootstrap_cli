# DoctorService - Agentic Layer Health Validation

**ADW ID:** 7f57eb36
**Date:** 2026-01-20
**Specification:** specs/issue-36-adw-7f57eb36-sdlc_planner-doctor-service.md

## Overview

DoctorService is a comprehensive diagnostic and auto-fix system for TAC Bootstrap generated Agentic Layers. It validates project setups by checking directory structures, configuration files, hook permissions, and ADW workflows, then provides detailed reports with actionable suggestions and auto-fix capabilities for common issues.

## What Was Built

- **Severity Classification System**: Enum-based severity levels (ERROR, WARNING, INFO) for categorizing issues by impact
- **Structured Issue Reporting**: Dataclass-based Issue and DiagnosticReport models with auto-fix function support
- **Comprehensive Health Checks**: Six specialized diagnostic methods covering all critical aspects of Agentic Layer setup
- **Auto-Fix Capabilities**: Automated fixes for common issues like missing directories and non-executable hooks
- **FixResult Tracking**: Detailed reporting of fix attempts with success/failure counts and messages

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py`: Complete implementation of DoctorService (422 lines, new file)

### Key Changes

- **Data Models** (Lines 26-89):
  - `Severity` enum with ERROR/WARNING/INFO levels to classify issue impact
  - `Issue` dataclass with severity, message, suggestion, and optional fix_fn callback
  - `DiagnosticReport` dataclass with healthy flag and issue list, auto-updating healthy status on ERROR
  - `FixResult` dataclass tracking fixed_count, failed_count, and result messages

- **Core Service Methods** (Lines 92-156):
  - `diagnose(repo_path)`: Orchestrates all health checks and returns comprehensive DiagnosticReport
  - `fix(repo_path, report)`: Executes auto-fix functions for issues that provide fix_fn callbacks

- **Diagnostic Checks** (Lines 158-376):
  - `_check_directory_structure()`: Validates required (.claude, .claude/commands, .claude/hooks) and optional (adws, specs, scripts) directories
  - `_check_claude_config()`: Validates .claude/settings.json exists, has valid JSON, and contains permissions field
  - `_check_commands()`: Ensures essential commands (prime.md, test.md, commit.md) exist and at least one .md file present
  - `_check_hooks()`: Checks that hook files (pre_tool_use.py, post_tool_use.py) are executable
  - `_check_adws()`: Validates ADW setup with adw_modules/ directory and workflow files
  - `_check_config_yml()`: Validates config.yml exists, has valid YAML, and contains required fields (project, commands)

- **Auto-Fix Functions** (Lines 378-422):
  - `_fix_create_dir()`: Creates missing directories with parents using mkdir
  - `_fix_make_executable()`: Makes hook files executable using chmod with proper permission flags

## How to Use

### Running Diagnostics

```python
from tac_bootstrap.application.doctor_service import DoctorService
from pathlib import Path

# Initialize service
doctor = DoctorService()

# Run diagnostics on a repository
repo_path = Path("/path/to/project")
report = doctor.diagnose(repo_path)

# Check overall health
if not report.healthy:
    print(f"Found {len(report.issues)} issues:")
    for issue in report.issues:
        print(f"[{issue.severity.value}] {issue.message}")
        if issue.suggestion:
            print(f"  Suggestion: {issue.suggestion}")
```

### Auto-Fixing Issues

```python
# After running diagnostics
fix_result = doctor.fix(repo_path, report)

# Review fix results
print(f"Successfully fixed: {fix_result.fixed_count}")
print(f"Failed to fix: {fix_result.failed_count}")

for message in fix_result.messages:
    print(message)
```

### Integration with CLI (Future)

The DoctorService is designed to be integrated with a `tac-bootstrap doctor` command:

```bash
# Diagnose project setup
tac-bootstrap doctor

# Diagnose and auto-fix issues
tac-bootstrap doctor --fix
```

## Configuration

No external configuration required. DoctorService operates entirely on local file system analysis:

- **Required Directories**: `.claude`, `.claude/commands`, `.claude/hooks`
- **Optional Directories**: `adws`, `specs`, `scripts`
- **Config Files**: `.claude/settings.json`, `config.yml`
- **Essential Commands**: `prime.md`, `test.md`, `commit.md`
- **Hook Files**: `pre_tool_use.py`, `post_tool_use.py`

## Testing

### Running Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Inline Test Example

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.application.doctor_service import DoctorService
from pathlib import Path
import tempfile

doctor = DoctorService()
with tempfile.TemporaryDirectory() as tmp:
    report = doctor.diagnose(Path(tmp))
    print(f'Healthy: {report.healthy}')
    print(f'Issues: {len(report.issues)}')
    for issue in report.issues[:5]:
        print(f'  [{issue.severity.value}] {issue.message}')
"
```

Expected output shows detection of multiple missing directories and configuration files, with `healthy=False` due to ERROR-level issues.

## Notes

### Design Decisions

- **Severity Levels**: ERROR for functionality-breaking issues, WARNING for limitations, INFO for optional improvements
- **Idempotent Fixes**: All auto-fix functions can be run multiple times safely without errors
- **Defensive Checks**: All diagnostic methods use try/except to prevent uncaught exceptions
- **No Network Operations**: All checks and fixes are local filesystem operations only
- **User File Safety**: No modification of user files without explicit fix_fn approval

### Limitations

- Does not validate content quality of configuration files beyond syntax
- Cannot fix issues requiring network access (downloading templates, cloning repos)
- Hook executability check uses os.access() which may not reflect actual Claude Code permissions
- Does not validate semantic correctness of commands or workflows

### Future Enhancements

- Integration with `tac-bootstrap doctor` CLI command
- Extended validation of settings.json schema and permission configurations
- Validation of ADW workflow syntax and imports
- Check for common anti-patterns in command files
- Interactive fix mode with user confirmation for each fix
- Export diagnostic reports to JSON/HTML formats
