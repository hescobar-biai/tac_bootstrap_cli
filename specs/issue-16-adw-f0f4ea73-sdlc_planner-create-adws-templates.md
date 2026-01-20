# Chore: Create Templates for adws/ (Modules and Workflows)

## Metadata
issue_number: `16`
adw_id: `f0f4ea73`
issue_json: `{"number":16,"title":"TAREA 3.4: Crear templates para adws/ (modulos y workflows)","body":"# Prompt para Agente\n\n## Contexto\nLos ADWs (AI Developer Workflows) son el corazon de la automatizacion en TAC.\nSon scripts Python que orquestan agentes y comandos deterministicos.\n\nLa estructura de adws/ incluye:\n- adw_modules/ - modulos compartidos (agent, state, git_ops, etc)\n- Workflows individuales (adw_sdlc_iso.py, adw_patch_iso.py, etc)\n- adw_triggers/ - triggers para ejecucion automatica\n\n## Objetivo\nCrear templates Jinja2 para la estructura completa de adws/:\n1. README.md explicativo\n2. Modulos core en adw_modules/\n3. Workflows principales\n4. Triggers basicos\n\n## Directorio Base\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/`"}`

## Chore Description
This chore involves creating Jinja2 templates for the complete ADW (AI Developer Workflows) structure. ADWs are the heart of TAC automation - Python scripts that orchestrate agents and deterministic commands.

The task requires creating 10 template files that will be used to generate the adws/ directory structure in target projects:
1. README.md.j2 - Documentation for the ADW system
2. adw_modules/__init__.py.j2 - Module initialization
3. adw_modules/agent.py.j2 - Claude Code agent wrapper
4. adw_modules/state.py.j2 - Workflow state management
5. adw_modules/git_ops.py.j2 - Git operations wrapper
6. adw_modules/workflow_ops.py.j2 - High-level workflow orchestration
7. adw_sdlc_iso.py.j2 - Full SDLC workflow (Plan → Build → Test → Review → Ship)
8. adw_patch_iso.py.j2 - Quick patch workflow (Build → Test → Ship)
9. adw_triggers/__init__.py.j2 - Triggers initialization
10. adw_triggers/trigger_cron.py.j2 - Basic cron-style trigger for polling tasks

These templates must use Jinja2 variables from the `config` object (TACConfig model) to be parametrizable for different projects.

## Relevant Files
Files needed to complete this chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/` - Template directory (currently only has claude/ subdirectory)
  - Need to create `adws/` subdirectory with all templates
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Contains TACConfig model with all available config variables
  - Provides `config.project.name`, `config.project.package_manager.value`, `config.paths.*`, `config.agentic.model_policy.*`
- `adws/` (repository root) - Reference implementation to base templates on
  - `adws/README.md` - Source for README.md.j2 structure
  - `adws/adw_modules/*.py` - Source modules to convert to templates
  - `adws/adw_sdlc_iso.py` - Source workflow to convert to template
  - `adws/adw_patch_iso.py` - Source workflow to convert to template
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering service (for testing)

### New Files
All files will be created under `tac_bootstrap_cli/tac_bootstrap/templates/adws/`:

1. `README.md.j2`
2. `adw_modules/__init__.py.j2`
3. `adw_modules/agent.py.j2`
4. `adw_modules/state.py.j2`
5. `adw_modules/git_ops.py.j2`
6. `adw_modules/workflow_ops.py.j2`
7. `adw_sdlc_iso.py.j2`
8. `adw_patch_iso.py.j2`
9. `adw_triggers/__init__.py.j2`
10. `adw_triggers/trigger_cron.py.j2`

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create adws template directory structure
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/adws/`
- Create subdirectory `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/`
- Create subdirectory `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/`
- Verify directories are created successfully

### Task 2: Create README.md.j2 template
- Read the issue body for the complete README.md.j2 content provided
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`
- Use Jinja2 variables: `{{ config.project.name }}`, `{{ config.paths.adws_dir }}`, `{{ config.paths.specs_dir }}`, `{{ config.paths.worktrees_dir }}`, `{{ config.project.package_manager.value }}`
- Document the ADW structure, workflows, concepts, and usage

### Task 3: Create adw_modules/__init__.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/__init__.py.j2`
- Use variable: `{{ config.project.name }}`
- Export the main module components: run_claude_command, ADWState, GitOps, WorkflowOps

### Task 4: Create adw_modules/agent.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`
- Implement run_claude_command() function that wraps Claude Code CLI execution
- Use variables: `{{ config.agentic.model_policy.default }}`, `{{ config.agentic.model_policy.heavy }}`
- Include model selection logic based on command complexity (HEAVY_COMMANDS list)
- Handle subprocess execution with timeout and error handling

### Task 5: Create adw_modules/state.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/state.py.j2`
- Implement ADWState dataclass with fields: adw_id, issue_number, issue_class, branch_name, plan_file, worktree_path, backend_port, frontend_port, current_phase, phases_completed, timestamps, error
- Implement save() and load() methods for JSON persistence to agents/{adw_id}/adw_state.json
- Implement mark_phase_complete() and set_error() helper methods

### Task 6: Create adw_modules/git_ops.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/git_ops.py.j2`
- Implement GitOps class with methods: create_branch(), checkout(), add_all(), commit(), push(), create_worktree(), remove_worktree(), get_current_branch()
- All methods should wrap git commands using subprocess and return success boolean
- No Jinja2 variables needed (pure git operations)

### Task 7: Create adw_modules/workflow_ops.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- Implement WorkflowOps class with methods: plan(), build(), test(), review(), ship()
- Each method uses run_claude_command() to execute slash commands
- Use variables: `{{ config.paths.specs_dir }}`
- Integrate with ADWState to mark phases complete

### Task 8: Create adw_sdlc_iso.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_iso.py.j2`
- Implement full SDLC workflow script with argparse (--issue, --description, --adw-id)
- Use variables: `{{ config.paths.worktrees_dir }}`, `{{ config.paths.specs_dir }}`
- Implement 5 phases: Plan → Build → Test → Review → Ship
- Include worktree setup and state management
- Add shebang line and make it executable template

### Task 9: Create adw_patch_iso.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_patch_iso.py.j2`
- Implement quick patch workflow script with argparse (--issue, --fix)
- Use variables: `{{ config.paths.worktrees_dir }}`
- Implement 3 phases: Implement → Test → Ship (skip planning)
- Include worktree setup and state management
- Add shebang line and make it executable template

### Task 10: Create adw_triggers/__init__.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`
- Simple module docstring with project name variable: `{{ config.project.name }}`

### Task 11: Create adw_triggers/trigger_cron.py.j2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`
- Implement polling script with argparse (--once, --interval)
- Use variable: `{{ config.paths.specs_dir }}`
- Implement get_pending_tasks() function that scans specs directory for pending tasks
- Add basic polling loop with configurable interval
- Add shebang line and make it executable template

### Task 12: Validate all templates were created
- Run: `find tac_bootstrap_cli/tac_bootstrap/templates/adws -name "*.j2"` to list all template files
- Verify all 10 template files exist
- Check file count matches expected (10 files)

### Task 13: Test template rendering with sample config
- Create a test script or use Python REPL to test rendering
- Import TemplateRepository and TACConfig models
- Create a sample TACConfig with minimal required fields
- Attempt to render `adws/README.md.j2` template
- Verify rendered output contains replaced variables (no {{ }} remaining)
- Verify no Jinja2 syntax errors

### Task 14: Run validation commands
- Execute all validation commands listed in the Validation Commands section
- Ensure unit tests pass with zero regressions
- Ensure linting passes
- Ensure CLI smoke test works

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && find tac_bootstrap/templates/adws -name "*.j2" | wc -l` - Verify 10 templates created
- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.infrastructure.template_repo import TemplateRepository; from tac_bootstrap.domain.models import *; repo = TemplateRepository(); config = TACConfig(project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV), commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'), claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))); result = repo.render('adws/README.md.j2', {'config': config}); print('OK' if 'test' in result and '{{' not in result else 'FAIL')"` - Test template rendering

## Notes
- All templates must use Jinja2 variables from the `config` object (TACConfig model)
- Follow the exact template content provided in the issue body
- Templates should be parametrizable and work for any project configuration
- The templates are based on the existing adws/ implementation in the repository
- The issue body contains complete code for all 10 templates - use it as the source of truth
- Ensure all file paths use forward slashes for cross-platform compatibility
- Make sure shebang lines are preserved in workflow templates (#!/usr/bin/env python3)
- The templates will be rendered by the TemplateRepository service using Jinja2
