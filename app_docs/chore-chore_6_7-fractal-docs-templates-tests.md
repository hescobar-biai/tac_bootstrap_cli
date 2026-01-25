# Fractal Documentation Templates Tests

**ADW ID:** chore_6_7
**Date:** 2026-01-24
**Specification:** specs/issue-183-adw-chore_6_7-sdlc_planner-fractal-docs-templates-tests.md

## Overview

Implemented a comprehensive test suite for fractal documentation templates in TAC Bootstrap CLI. The test suite validates that all fractal documentation templates (Python scripts, Bash scripts, YAML config, slash commands, and conditional docs) render correctly for both Python and TypeScript project configurations, producing valid and parseable output.

## What Was Built

- **Test Suite**: `tac_bootstrap_cli/tests/test_fractal_docs_templates.py` (300 lines)
- **Test Coverage for 6 Template Types**:
  - Python script templates (gen_docstring_jsdocs.py.j2, gen_docs_fractal.py.j2)
  - Bash script template (run_generators.sh.j2)
  - YAML configuration template (canonical_idk.yml.j2)
  - Slash command template (generate_fractal_docs.md.j2)
  - Conditional documentation template (conditional_docs.md.j2)
- **9 Comprehensive Tests**: Covering rendering, syntax validation, and integration
- **Fixtures**: Python and TypeScript project configurations for testing

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_fractal_docs_templates.py`: Comprehensive test suite with 9 test cases organized into 5 test classes

### Key Changes

1. **Test Organization**: Structured tests into logical classes:
   - `TestPythonScriptRendering`: Validates Python script generation
   - `TestBashScriptRendering`: Validates Bash script generation
   - `TestYAMLTemplateRendering`: Validates YAML configuration
   - `TestSlashCommandTemplates`: Validates slash command markdown
   - `TestConditionalDocsTemplate`: Validates conditional documentation
   - `TestScaffoldServiceIntegration`: Validates scaffold service integration

2. **Validation Strategy**: Multi-layer validation approach:
   - Content length checks (> 50 characters for meaningful output)
   - Syntax validation (ast.parse for Python, yaml.safe_load for YAML)
   - Structural checks (shebang for scripts, headers for markdown)
   - Domain-specific keyword checks (backend/frontend domains)

3. **Fixtures**: Created reusable configuration fixtures:
   - `python_config`: Minimal Python project config with UV package manager
   - `typescript_config`: Minimal TypeScript project config with NPM
   - `template_repo`: TemplateRepository instance for rendering

4. **Cross-Language Testing**: All templates tested with both Python and TypeScript configurations to ensure they handle different language contexts correctly

## How to Use

### Running the Tests

Run the complete fractal docs test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py -v
```

Run specific test classes:

```bash
# Test Python script rendering only
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestPythonScriptRendering -v

# Test YAML rendering only
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestYAMLTemplateRendering -v
```

Run individual tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestScaffoldServiceIntegration::test_scaffold_includes_fractal_scripts -v
```

### Test Coverage

The test suite covers:

1. **Python Script Rendering** (3 tests):
   - gen_docstring_jsdocs.py.j2 for Python projects
   - gen_docstring_jsdocs.py.j2 for TypeScript projects
   - gen_docs_fractal.py.j2 main generation script

2. **Bash Script Rendering** (1 test):
   - run_generators.sh.j2 with shebang and structure validation

3. **YAML Configuration** (2 tests):
   - canonical_idk.yml.j2 with Python domain keywords
   - canonical_idk.yml.j2 with TypeScript domain keywords

4. **Slash Commands** (1 test):
   - generate_fractal_docs.md.j2 markdown command

5. **Conditional Documentation** (1 test):
   - conditional_docs.md.j2 with fractal rules

6. **Integration** (1 test):
   - ScaffoldService includes all fractal scripts in build plan

## Configuration

No special configuration needed. Tests use minimal inline configuration fixtures:

- **Python Config**: Uses UV package manager, basic commands
- **TypeScript Config**: Uses NPM package manager, standard npm commands

## Testing

All tests passed with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py -v --tb=short
```

Expected output: 9 tests passed

Validation also includes:
- Full test suite regression check
- Ruff linting
- CLI smoke test

## Notes

- Tests use `ast.parse()` for Python validation without executing code (security best practice)
- Tests use `yaml.safe_load()` for YAML validation (prevents arbitrary code execution)
- Bash scripts validated only for shebang and basic structure (no shellcheck to keep tests fast)
- All tests are unit tests (fast, isolated, no file I/O)
- Templates must render non-empty content or tests fail (prevents silent failures)
- Domain keywords are context-aware (backend/testing for Python, frontend/component for TypeScript)
- Follows established patterns from `test_scaffold_service.py` and `test_template_repo.py`

## Next Steps

Now that fractal docs templates have comprehensive tests, consider:
- Running `/generate_fractal_docs full` to generate documentation for the CLI codebase
- Reviewing generated docs/ for template improvements based on real-world output
- Using fractal docs to onboard new contributors or understand complex modules
