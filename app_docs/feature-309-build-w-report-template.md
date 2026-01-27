---
doc_type: feature
adw_id: feature_Tac_10_task_4
date: 2026-01-26
idk:
  - build-report
  - yaml-report
  - git-diff
  - change-tracking
  - jinja2-template
  - command-template
  - automated-documentation
tags:
  - feature
  - command
  - reporting
  - automation
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2
  - .claude/commands/build_w_report.md
---

# Build with Report Command Template

**ADW ID:** feature_Tac_10_task_4
**Date:** 2026-01-26
**Specification:** specs/issue-309-adw-feature_Tac_10_task_4-sdlc_planner-build-w-report-template.md

## Overview

Created a new command template `build_w_report` that extends standard build functionality by automatically generating detailed YAML reports of all code changes made during implementation. This provides machine-readable documentation for tracking, auditing, and CI/CD integration purposes.

## What Was Built

- **Jinja2 Template**: `build_w_report.md.j2` with configuration variables for project-agnostic generation
- **Rendered Command**: Direct `.md` version for immediate use in TAC Bootstrap project
- **YAML Report Generator**: Automated workflow that captures git diff statistics and change descriptions
- **Structured Output**: Timestamped YAML files with metadata, per-file change details, and summary statistics

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2`: Jinja2 template with config variables for test commands, architecture patterns, and project-specific settings
- `.claude/commands/build_w_report.md`: Rendered version with TAC Bootstrap-specific values (DDD architecture, uv commands)

### Key Changes

- **Frontmatter Configuration**: Uses `allowed-tools: Read, Write, Edit, Bash` to enable file operations and git commands
- **Plan Validation**: Checks plan file existence before proceeding with implementation
- **Git Integration**: Uses `git diff --numstat` for line count statistics and `git diff` with context for change descriptions
- **YAML Structure**: Generates reports with three sections:
  - `metadata`: timestamp, branch name, plan file path
  - `work_changes`: array of per-file changes with lines added/deleted and descriptions
  - `summary`: aggregate statistics (total files, lines added, lines deleted)
- **Edge Case Handling**: Manages no changes detected, binary files, and missing plan files gracefully
- **Timestamped Output**: Files named `build_report_YYYY-MM-DD_HHMMSS.yaml` to prevent overwriting

### Workflow

1. Validate plan file exists
2. Read and analyze the plan
3. Implement changes following plan specifications
4. Run validation commands (tests, linter, type checker)
5. Execute git diff commands to collect change statistics
6. Parse diff output to extract file paths, line counts, and descriptions
7. Generate YAML report with structured data
8. Write report to timestamped file
9. Display summary to user

## How to Use

### Using the Template in TAC Bootstrap

1. Run the command with a plan file path:
```bash
/build_w_report specs/my-feature-spec.md
```

2. The command will:
   - Implement the plan
   - Generate a timestamped YAML report
   - Display a summary of changes

3. Review the generated report:
```bash
cat build_report_2026-01-26_143022.yaml
```

### Generating for New Projects

When using TAC Bootstrap CLI to create a new project, the `build_w_report.md.j2` template will be rendered with project-specific configuration values, automatically adapting to the target project's test commands and architecture patterns.

## Configuration

### Jinja2 Variables Used

- `config.project.architecture.value`: Architecture pattern (e.g., "DDD", "MVC")
- `config.commands.test`: Test command for the project
- `config.commands.lint`: Linter command for the project
- `config.commands.typecheck`: Type checker command for the project

### YAML Report Structure

```yaml
metadata:
  timestamp: "2026-01-26T14:30:22Z"
  branch: "feature-my-feature"
  plan_file: "specs/my-feature-spec.md"

work_changes:
  - file: "src/module/file.py"
    lines_added: 45
    lines_deleted: 12
    description: "Added new function process_data()"
  - file: "tests/test_file.py"
    lines_added: 23
    lines_deleted: 0
    description: "Added test cases for process_data"

summary:
  total_files_changed: 2
  total_lines_added: 68
  total_lines_deleted: 12
```

## Testing

### Verify Template Files Exist

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2
ls -la .claude/commands/build_w_report.md
```

### Test the Command

```bash
# Create a test plan file
echo "# Test Plan\n\nAdd a simple function." > test_plan.md

# Run the build_w_report command
/build_w_report test_plan.md

# Verify YAML report was generated
ls -la build_report_*.yaml

# Validate YAML syntax
python -c "import yaml; print(yaml.safe_load(open('build_report_2026-01-26_143022.yaml')))"
```

### Run Validation Commands

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **Machine-Readable Artifact**: The YAML format enables automated processing in CI/CD pipelines, documentation generation tools, and audit systems
- **Complete Change Tracking**: Even binary files are tracked (with line counts set to 0)
- **History Preservation**: Timestamped filenames maintain full implementation history without overwriting previous reports
- **Git Requirement**: This command requires a git repository to function
- **Future Enhancements**: Could be extended to include commit hashes, author information, or integration with issue tracking systems
- **Description Extraction**: Automatically extracts function/class names from git diff context to provide meaningful change descriptions without manual input
