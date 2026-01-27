# Chore: Create Jinja2 template for /question command

## Metadata
issue_number: `342`
adw_id: `chore_Tac_11_task_10`
issue_json: `{"number":342,"title":"Create scout_files directory structure in base repository","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_10\n\nCreate the Jinja2 template version of the /question command for generated projects.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2`\n\n**Implementation details:**\n- Mirror the implementation from Task 5\n- Use read-only tool restrictions"}`

## Chore Description
Convert the existing `.claude/commands/question.md` file into a Jinja2 template (`question.md.j2`) for generated projects. The /question command provides read-only Q&A functionality to explore project structure and answer questions about the codebase. This template will enable TAC Bootstrap CLI to generate the question command for new projects.

The implementation should:
- Use `.claude/commands/question.md` as the canonical source
- Keep content mostly static with minimal Jinja2 templating
- Preserve read-only tool restrictions
- Add basic template validation tests following existing patterns

## Relevant Files
Files required to complete this chore:

1. **Source file**:
   - `.claude/commands/question.md` - Current implementation to be converted to template

2. **Target template file**:
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2` - New Jinja2 template to be created

3. **Test files**:
   - `tac_bootstrap_cli/tests/test_new_tac10_templates.py` or similar - Add validation tests for the new template

4. **Reference files** (for understanding patterns):
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Example of minimally templated command
   - `tac_bootstrap_cli/tests/test_new_tac10_templates.py` - Test patterns to follow

5. **Domain models** (for test fixtures):
   - `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig, ProjectSpec, etc.

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2` - Jinja2 template version of the question command

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read source file and analyze templating needs
- Read `.claude/commands/question.md` to understand the current implementation
- Identify any project-specific references that need Jinja2 variables
- Determine if the file should remain mostly static or include config variables like `{{ config.project.name }}`
- Review `prime.md.j2` and other minimal templates to understand the templating approach

### Task 2: Create question.md.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2`
- Copy content from `.claude/commands/question.md`
- Add minimal Jinja2 templating only where needed (likely just project name if any)
- Preserve all content including:
  - The 5-step workflow (Analyze, Explore, Read Overview, Read Files, Synthesize)
  - Git command examples for read-only exploration
  - Report format structure
  - Read-only safety notes
  - Tool restrictions

### Task 3: Add template validation tests
- Add a new test class `TestQuestionTemplate` to `tac_bootstrap_cli/tests/test_new_tac10_templates.py`
- Follow existing test patterns from other command templates
- Implement three test methods:
  1. `test_question_renders_valid_markdown` - Verify template renders without errors and has meaningful content (>100 chars)
  2. `test_question_has_expected_sections` - Verify key sections exist: "## Variables", "## Instructions", "## Report"
  3. `test_question_has_read_only_restrictions` - Verify safety notes mention read-only constraints
- Use the existing `python_config` and `template_repo` fixtures
- Use `template_repo.render("claude/commands/question.md.j2", python_config)` to render the template

### Task 4: Validate template rendering
- Run the new tests to verify template renders correctly:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/test_new_tac10_templates.py::TestQuestionTemplate -v
  ```
- Manually verify the rendered output contains expected content
- Check that Jinja2 syntax is valid and variables are resolved

### Task 5: Run full validation suite
- Execute all validation commands to ensure zero regressions:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
  cd tac_bootstrap_cli && uv run ruff check .
  cd tac_bootstrap_cli && uv run tac-bootstrap --help
  ```

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Read-only tool restrictions
The question command is designed for exploration and answering questions without modifying code. The template should preserve these characteristics:
- Allowed tools: Read, Grep, Glob, WebFetch, WebSearch, Task (with Explore subagent), git ls-files
- Disallowed tools: Edit, Write, Bash (except git ls-files), NotebookEdit
- Safety notes emphasize read-only nature

### Minimal templating approach
Based on the auto-resolved clarifications and the simple nature of the question command, keep templating minimal:
- The command is generic and project-agnostic
- Only add Jinja2 variables if the existing question.md references project-specific information
- Example minimal template: `# Question` (no variables needed) or `Answer questions about {{ config.project.name }}` (if project name is referenced)

### Test patterns
Follow the existing test structure in `test_new_tac10_templates.py`:
- Use fixtures: `python_config` and `template_repo`
- Test three aspects: renders without errors, has expected sections, has semantic content
- Keep assertions simple and focused on template integrity

### Git history reference
The question command was implemented in PR #336 (merged into main):
- Branch: `feat-issue-329-adw-feature-tac-11-task-5-question-slash-command`
- Commit: `a8523da` (visible in git log)
- This is the canonical implementation to template
