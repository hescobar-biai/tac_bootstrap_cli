# Feature: Create Jinja2 Template for Dangerous Command Blocker Hook

## Metadata
issue_number: `339`
adw_id: `feature_Tac_11_task_2`
issue_json: `{"number":339,"title":"Create dangerous_command_blocker.py.j2 template","body":"feature\n/adw_sdlc_iso\n/adw_id: feature_Tac_11_task_2\n\nCreate the Jinja2 template version of the dangerous command blocker hook for generated projects.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2`\n\n**Implementation details:**\n- Mirror the implementation from Task 1\n- Use `{{ config.project.package_manager.value }}` where applicable\n- Ensure template renders correctly for uv, pip, and other package managers"}`

## Feature Description
Create a Jinja2 template version of the dangerous command blocker security hook that can be rendered for any Python package manager (uv, pip, poetry, pipenv). This template will be used by the TAC Bootstrap CLI generator to create customized hook files for new projects, replacing hardcoded package manager references with configurable values.

## User Story
As a TAC Bootstrap CLI user
I want the dangerous command blocker hook to adapt to my chosen package manager
So that the security hook uses the correct package manager commands for my project setup

## Problem Statement
The current dangerous_command_blocker.py hook in `.claude/hooks/` uses hardcoded shebang and commands specific to `uv`. When TAC Bootstrap generates new projects with different package managers (pip, poetry, pipenv), the hook needs to use the appropriate package manager syntax. The hook file needs to be templated to support this variability.

## Solution Statement
Convert the existing `.claude/hooks/dangerous_command_blocker.py` file into a Jinja2 template (`.j2` extension) by replacing package manager-specific references with the `{{ config.project.package_manager.value }}` template variable. The template will maintain all security logic, dangerous patterns, and safety checks while allowing the shebang and any package manager commands to adapt to the project's configuration.

## Relevant Files
Files needed for this feature:

- `.claude/hooks/dangerous_command_blocker.py` - Source implementation to convert into template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/*.j2` - Existing hook templates for reference on templating patterns
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Contains PackageManager enum showing all supported package managers
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2` - Example of existing hook template with shebang

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2` - New Jinja2 template file

## Implementation Plan

### Phase 1: Analysis
Analyze the source implementation to identify all package manager-specific references and understand the templating patterns used in existing hook templates.

### Phase 2: Template Creation
Create the Jinja2 template by copying the source file and replacing package manager references with template variables, following established patterns from other hook templates.

### Phase 3: Validation
Manually verify the template syntax is correct and will render properly for different package managers.

## Step by Step Tasks

### Task 1: Read source implementation and analyze template patterns
- Read `.claude/hooks/dangerous_command_blocker.py` to understand full implementation
- Read existing hook templates in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/` to identify templating patterns
- Identify all package manager-specific references in the source (primarily the shebang line)
- Note: The dangerous commands list should remain hardcoded (security best practice)

### Task 2: Create Jinja2 template file
- Create new file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2`
- Copy entire content from `.claude/hooks/dangerous_command_blocker.py`
- Replace shebang line `#!/usr/bin/env -S uv run --script` with templated version:
  - If package_manager is UV: `#!/usr/bin/env -S uv run --script`
  - For other Python package managers (pip, poetry, pipenv): `#!/usr/bin/env python3`
- Keep all dangerous patterns, critical paths, safer alternatives, and security logic unchanged
- Keep all docstrings, comments, and function implementations unchanged
- Maintain file structure, imports, and exit codes exactly as in source

### Task 3: Manual validation
- Review template syntax for Jinja2 correctness
- Verify that no security logic was accidentally removed or modified
- Check that only package manager references were templated
- Mentally simulate rendering with different package_manager values (uv, pip, poetry, pipenv)
- Ensure template follows same patterns as other hook templates in the directory

### Task 4: Run validation commands
- Execute all validation commands to ensure no regressions:
  - `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
  - `cd tac_bootstrap_cli && uv run ruff check .` - Linting
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
  - `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Manual Verification
- Inspect template file for correct Jinja2 syntax
- Verify security patterns remain unchanged
- Confirm only shebang line uses template variables
- Check template follows established patterns from other hooks

### Template Rendering Simulation
Mentally verify template renders correctly for each package manager:
- UV: Should use `#!/usr/bin/env -S uv run --script` (original shebang)
- PIP: Should use `#!/usr/bin/env python3` (standard Python shebang)
- POETRY: Should use `#!/usr/bin/env python3`
- PIPENV: Should use `#!/usr/bin/env python3`

### Edge Cases
- Empty or missing package_manager value (should use default)
- Unknown package manager value (should gracefully handle)
- Template syntax errors (caught by manual inspection)

## Acceptance Criteria
1. ✅ Template file created at: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2`
2. ✅ Template contains complete implementation from `.claude/hooks/dangerous_command_blocker.py`
3. ✅ Shebang line is templated based on package_manager value
4. ✅ All dangerous patterns, critical paths, and security logic remain unchanged
5. ✅ All docstrings, comments, and function signatures preserved exactly
6. ✅ Template follows Jinja2 syntax conventions
7. ✅ Template follows same patterns as other hook templates in the directory
8. ✅ All validation commands pass with zero errors

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes
- **Security First**: The dangerous commands list must remain hardcoded - no configuration allowed
- **Simple Templating**: Only the shebang line needs templating; no complex conditional logic required
- **Package Manager Support**: Template supports Python package managers only (uv, pip, poetry, pipenv)
- **No Tests Required**: Template rendering tests can be added later; manual verification sufficient for initial implementation
- **Consistent Patterns**: Follow the templating approach used in other hook templates like `user_prompt_submit.py.j2`
- **Future Enhancement**: Comprehensive template rendering tests can be added in a future task
