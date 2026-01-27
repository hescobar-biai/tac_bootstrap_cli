# Feature: Build with Report Template

## Metadata
issue_number: `309`
adw_id: `feature_Tac_10_task_4`
issue_json: `{"number":309,"title":"Crear template build_w_report.md.j2 con reporte YAML estructurado","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_10_task_4\n\n- **Descripción**: Variante del comando build que genera un reporte YAML detallado de los cambios realizados (files, lines_changed, description).\n- **Archivos**:\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/build_w_report.md`\n- **Contenido**:\n  - Frontmatter con allowed-tools (Read, Write, Edit, Bash, MultiEdit)\n  - Variables: PATH_TO_PLAN ($ARGUMENTS)\n  - Workflow: Read plan, implement, run git diff\n  - Report format YAML: work_changes array\n- **Nota**: El template .j2 usa variables Jinja2, el archivo .md es la versión renderizada para uso directo\n\n"}`

## Feature Description
Create a new command template `build_w_report` that extends the standard build command functionality by generating a detailed YAML report of all code changes made during implementation. This command reads a plan file, implements the changes, and then automatically generates a timestamped YAML report containing file-level change details including lines added/deleted and descriptions extracted from git diff context.

The template will be created in two forms:
1. A Jinja2 template (`.j2`) that uses configuration variables for generalization
2. A direct rendered version (`.md`) for immediate use in the TAC Bootstrap project

## User Story
As a developer using TAC Bootstrap
I want to run a build command that automatically documents my changes in a structured format
So that I have a detailed, machine-readable record of implementation work for tracking, auditing, and reporting purposes

## Problem Statement
Currently, the standard build command executes implementation but provides no structured documentation of the changes made. Developers must manually run git commands and create reports if they want to track what files were modified and the scope of changes. This lack of automation makes it difficult to:
- Track implementation progress across multiple build sessions
- Generate reports for stakeholders
- Audit what changes were made during automated builds
- Maintain structured records for compliance or documentation purposes

## Solution Statement
Create a `build_w_report` command template that combines implementation workflow with automated change tracking. The command will:
1. Validate that the plan file exists before proceeding
2. Read and implement the plan (similar to standard build/implement commands)
3. Use `git diff --numstat` to extract line count statistics (additions/deletions per file)
4. Use `git diff` with context to extract descriptive information about changes
5. Generate a YAML report with metadata (timestamp, branch) and detailed change information
6. Handle edge cases (no changes, binary files, missing plans)
7. Write the report to a timestamped file in the project root

The YAML format will be simple, readable, and machine-parseable, making it suitable for both human review and automated processing.

## Relevant Files
Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Existing build template to use as reference for structure and workflow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/implement.md.j2` - Reference for plan reading and implementation workflow patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` - Directory where the new template will be created

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2` - Jinja2 template with config variables
- `.claude/commands/build_w_report.md` - Rendered version for direct use in TAC Bootstrap

## Implementation Plan

### Phase 1: Foundation
Review existing build and implement templates to understand:
- Frontmatter structure and allowed-tools configuration
- Variable usage patterns (especially $ARGUMENTS)
- Validation command integration
- Report format conventions

### Phase 2: Core Implementation
Create the build_w_report template with:
- Frontmatter with appropriate allowed-tools (Read, Write, Edit, Bash)
- Variables section defining PATH_TO_PLAN from $ARGUMENTS
- Instructions workflow: validate plan exists, read plan, implement changes
- Git diff analysis: parse --numstat for line counts, extract descriptions from context
- YAML report generation with proper structure and formatting
- Error handling for edge cases (no changes, missing plan, binary files)

### Phase 3: Integration
- Render the Jinja2 template for direct use in `.claude/commands/`
- Test template with real plan files
- Validate YAML output structure
- Ensure integration with existing validation commands

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read and analyze reference templates
- Read `build.md.j2` to understand basic build command structure
- Read `implement.md.j2` to understand plan reading workflow
- Identify patterns for frontmatter, variables, and instructions sections
- Note how validation commands are integrated

### Task 2: Create build_w_report.md.j2 template
- Create frontmatter with:
  - allowed-tools: Read, Write, Edit, Bash
  - Command description
- Define Variables section:
  - PATH_TO_PLAN: $ARGUMENTS (path to plan file)
- Write Instructions section:
  1. Validate plan file exists (exit early if not)
  2. Read and analyze the plan
  3. Implement the changes following the plan
  4. Run validation commands if specified in plan
  5. Generate change report
- Write Git Diff Analysis section:
  - Run `git diff --numstat` to get line statistics
  - Run `git diff` with context for descriptions
  - Parse output to extract file-level information
- Write Report Generation section:
  - Create YAML structure with metadata (timestamp, branch)
  - Populate work_changes array with per-file details:
    - file: relative path to file
    - lines_added: integer from --numstat
    - lines_deleted: integer from --numstat
    - description: extracted from git diff context (function/class names)
  - Handle binary files (lines_added/deleted = 0, description = "Binary file changed")
  - Handle no changes case (empty work_changes array, note "No changes detected")
  - Write to file: `build_report_YYYY-MM-DD_HHMMSS.yaml`
- Write Report Output section:
  - Inform user of report file location
  - Summarize key metrics (files changed, total lines added/deleted)

### Task 3: Create rendered version for TAC Bootstrap
- Render the Jinja2 template with TAC Bootstrap config values
- Write rendered version to `.claude/commands/build_w_report.md`
- Ensure all Jinja2 variables are properly substituted

### Task 4: Test template functionality
- Create a test plan file
- Run the build_w_report command (manually test the workflow)
- Verify YAML report is generated with correct structure
- Validate YAML syntax with `python -c "import yaml; yaml.safe_load(open('build_report_*.yaml'))"`
- Test edge cases:
  - Missing plan file (should error early)
  - No changes detected (should create report with empty work_changes)
  - Binary file changes (should handle gracefully)

### Task 5: Run validation commands
- Execute all validation commands to ensure zero regressions
- Verify template integrates properly with CLI

## Testing Strategy

### Unit Tests
No unit tests required for template files, but manual testing workflow:
1. Test with valid plan file containing multiple tasks
2. Test with missing plan file (should fail gracefully)
3. Test with plan that results in no changes
4. Test with changes including binary files

### Edge Cases
- **Missing plan file**: Command should check file exists first and exit with clear error message
- **No changes detected**: Report should include empty work_changes array with note "No changes detected"
- **Binary files**: Include in report with lines_added/deleted = 0, description = "Binary file changed"
- **Empty diff**: Handle gracefully with appropriate messaging
- **Invalid git repository**: Bash commands will naturally error; include note in instructions about git requirement

## Acceptance Criteria
- [ ] Template file `build_w_report.md.j2` exists at correct path with Jinja2 variables
- [ ] Rendered file `build_w_report.md` exists at `.claude/commands/` with all variables substituted
- [ ] Frontmatter includes correct allowed-tools (Read, Write, Edit, Bash)
- [ ] Template validates plan file exists before proceeding
- [ ] Template reads plan file and implements changes
- [ ] Git diff commands are used correctly (--numstat for counts, regular diff for descriptions)
- [ ] YAML report structure includes:
  - Metadata: timestamp, branch
  - work_changes array with: file, lines_added, lines_deleted, description
- [ ] Report file naming follows format: `build_report_YYYY-MM-DD_HHMMSS.yaml`
- [ ] Edge cases are handled (no changes, missing plan, binary files)
- [ ] YAML output is valid and parseable
- [ ] All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2` - Verify template exists
- `ls -la .claude/commands/build_w_report.md` - Verify rendered version exists
- `python -c "import yaml; yaml.safe_load(open('build_report_*.yaml'))"` - Validate YAML syntax (after test run)

## Notes
- This template creates a machine-readable artifact of implementation work, useful for CI/CD pipelines, documentation generation, and audit trails
- The YAML format is intentionally simple to allow easy extension in the future (e.g., adding commit hashes, author info)
- Binary file handling ensures complete change tracking even for non-text files
- The timestamp in filename prevents overwriting previous reports, maintaining full history
- Future enhancements could include: aggregating multiple reports, comparing reports across builds, or integration with issue tracking systems
- The template uses Bash tool for git commands, which is appropriate since git operations require shell execution
- Description extraction from git diff context provides meaningful change summaries without requiring manual input
