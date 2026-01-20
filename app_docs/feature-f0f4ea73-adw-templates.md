# ADW Templates for TAC Bootstrap CLI

**ADW ID:** f0f4ea73
**Date:** 2026-01-20
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/f0f4ea73/specs/issue-16-adw-f0f4ea73-sdlc_planner-create-adws-templates.md

## Overview

Created a complete set of Jinja2 templates for generating AI Developer Workflows (ADWs) in target projects. These templates enable the TAC Bootstrap CLI to automatically generate workflow automation scripts that orchestrate Claude Code agents for full SDLC processes.

## What Was Built

The implementation added 10 Jinja2 template files organized in the following structure:

- **README.md.j2** - Documentation for generated ADW systems
- **adw_modules/** - Core shared modules
  - **__init__.py.j2** - Module exports
  - **agent.py.j2** - Claude Code CLI wrapper with model selection
  - **state.py.j2** - Persistent workflow state management
  - **git_ops.py.j2** - Git operations wrapper
  - **workflow_ops.py.j2** - High-level workflow orchestration
- **adw_sdlc_iso.py.j2** - Full SDLC workflow (Plan → Build → Test → Review → Ship)
- **adw_patch_iso.py.j2** - Quick patch workflow (Build → Test → Ship)
- **adw_triggers/** - Automated workflow triggers
  - **__init__.py.j2** - Module initialization
  - **trigger_cron.py.j2** - Polling-based task trigger

## Technical Implementation

### Files Modified

All files created under `tac_bootstrap_cli/tac_bootstrap/templates/adws/`:

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`: Documentation template explaining ADW structure, workflows, and usage for generated projects
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/__init__.py.j2`: Module initialization exporting core components
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`: Claude Code agent wrapper with `run_claude_command()` function and model selection logic
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/state.py.j2`: ADWState dataclass for JSON-based state persistence
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/git_ops.py.j2`: GitOps class wrapping git commands
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`: WorkflowOps class implementing plan(), build(), test(), review(), ship() methods
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_iso.py.j2`: Full SDLC workflow script with 5 phases
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_patch_iso.py.j2`: Quick patch workflow script with 3 phases
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`: Triggers module initialization
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`: Polling script for automated task detection

### Key Changes

- **Parameterized templates**: All templates use Jinja2 variables from the TACConfig model (config.project.name, config.paths.*, config.agentic.model_policy.*, config.project.package_manager.value)
- **Isolated workflow pattern**: Templates implement worktree-based isolation where each workflow runs in its own git worktree to avoid conflicts
- **State management**: ADWState dataclass provides JSON persistence to agents/{adw_id}/adw_state.json for workflow resumability
- **Model selection logic**: HEAVY_COMMANDS list determines when to use heavy vs default models (implement, feature, bug, review, document use heavy model)
- **Phase-based execution**: Both SDLC and patch workflows implement phase tracking with mark_phase_complete() to enable resuming workflows

## How to Use

### For CLI Developers

Templates are automatically rendered by the TemplateRepository when running the `tac-bootstrap init` or `tac-bootstrap generate` commands. The templates will be populated with values from the project's TACConfig.

### Template Rendering Example

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig, ProjectSpec, Language, PackageManager

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(
        name='my-project',
        language=Language.PYTHON,
        package_manager=PackageManager.UV
    ),
    # ... other config
)

# Render a template
result = repo.render('adws/README.md.j2', {'config': config})
```

### Generated ADW Usage (in target projects)

Once templates are rendered in a target project:

```bash
# Run full SDLC workflow
uv run python adws/adw_sdlc_iso.py --issue 123 --description "Add user auth"

# Run quick patch workflow
uv run python adws/adw_patch_iso.py --issue 456 --fix "Fix login bug"

# Resume existing workflow
uv run python adws/adw_sdlc_iso.py --adw-id abc123ef

# Run automated trigger
uv run python adws/adw_triggers/trigger_cron.py --interval 300
```

## Configuration

### TACConfig Variables Used

The templates rely on the following configuration variables:

- **config.project.name** - Project name (used in documentation)
- **config.project.package_manager.value** - Package manager (uv, npm, poetry, etc.)
- **config.paths.adws_dir** - ADWs directory path (default: "adws")
- **config.paths.specs_dir** - Specifications directory path (default: "specs")
- **config.paths.worktrees_dir** - Worktrees directory path (default: "trees")
- **config.agentic.model_policy.default** - Default AI model (e.g., "sonnet")
- **config.agentic.model_policy.heavy** - Heavy model for complex tasks (e.g., "opus")

### Workflow Isolation

Each workflow creates its own git worktree in `trees/{adw_id}` to prevent conflicts. State is persisted to `agents/{adw_id}/adw_state.json` for resumability.

## Testing

### Verify Templates Were Created

```bash
cd tac_bootstrap_cli && find tac_bootstrap/templates/adws -name "*.j2" | wc -l
# Expected output: 10
```

### Test Template Rendering

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(
        name='test',
        language=Language.PYTHON,
        package_manager=PackageManager.UV
    ),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

result = repo.render('adws/README.md.j2', {'config': config})
print('OK' if 'test' in result and '{{' not in result else 'FAIL')
"
```

### Run Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Notes

- Templates are based on the reference implementation in `adws/` at the repository root
- All templates use forward slashes for cross-platform compatibility
- Shebang lines (`#!/usr/bin/env python3`) are preserved in executable workflow scripts
- The agent.py.j2:74 implements HEAVY_COMMANDS list for intelligent model selection
- State management in state.py.j2:32-40 enables workflow resumability across agent sessions
- Workflow isolation prevents conflicts when multiple ADWs run concurrently
- Templates will be rendered during `tac-bootstrap init` or `tac-bootstrap generate` commands
