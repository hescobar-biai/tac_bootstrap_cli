# Chore: Create security_logs directory template

## Metadata
issue_number: `351`
adw_id: `chore_Tac_11_task_10_v2`
issue_json: `{"number":351,"title":"Create security_logs directory template","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_10_v2\n\nCreate the template for security_logs directory in generated projects.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/.gitkeep.j2`\n\n**Implementation details:**\n- Create empty .gitkeep.j2 template\n- Ensures security_logs directory is created in generated projects"}`

## Chore Description
Create the security_logs directory template structure for generated projects. This directory will store security-related logs in generated projects. The implementation follows the same pattern as existing agent subdirectories (context_bundles, hook_logs) by creating an empty .gitkeep.j2 template file to ensure the directory is tracked in git.

## Relevant Files
Files relevant to completing this chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2` - Reference template for .gitkeep pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2` - Reference template for .gitkeep pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/` - Parent directory where security_logs will be created

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/.gitkeep.j2` - Empty template to ensure directory creation

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create security_logs directory structure
- Create the directory: `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/`
- This follows the existing pattern for agent subdirectories

### Task 2: Create .gitkeep.j2 template file
- Create empty file: `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/.gitkeep.j2`
- This file should be empty (0 bytes or single newline) to match existing .gitkeep.j2 templates
- The .gitkeep.j2 ensures the directory is tracked in git and created in generated projects

### Task 3: Validation
- Verify the file structure matches existing patterns (context_bundles, hook_logs)
- Run validation commands to ensure no regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/` - Verify directory exists

## Notes
- This is a simple structural chore that creates a new agent subdirectory template
- The security_logs directory will be used in generated projects to store security-related logs
- The pattern follows existing agent subdirectories: context_bundles and hook_logs
- No code changes required, only directory and file creation
