# Interactive Wizard with Rich UI

**ADW ID:** ede93862
**Date:** 2026-01-20
**Specification:** specs/issue-25-adw-ede93862-sdlc_planner-implement-wizard-interactivo.md

## Overview

Implemented a complete interactive wizard using the Rich library that guides users through TAC Bootstrap project configuration with numbered options, contextual defaults, visual progress feedback, and confirmation steps. This transforms the CLI experience from flag-based commands to a conversational guided flow.

## What Was Built

- Interactive wizard module with Rich UI components
- CLI integration for `init` and `add-agentic` commands in interactive mode
- Enum selection helper with filtered options and visual defaults
- Configuration summary tables with color-coded output
- Contextual command defaults based on language and package manager selections

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Integrated wizard with CLI commands, replacing placeholders with actual wizard invocations for `--interactive` mode

### Key Changes

1. **CLI Integration (`cli.py:124-168`)**: Replaced "Interactive wizard not yet implemented" placeholder in `init()` command with call to `run_init_wizard()`. The wizard is invoked when `--interactive=True`, receiving pre-selected values from CLI flags (language, framework, package_manager, architecture) and only prompting for unspecified options.

2. **Non-Interactive Path Preserved (`cli.py:133-153`)**: Moved existing non-interactive configuration logic into `else` block to maintain backward compatibility. Users can still use CLI flags without the wizard.

3. **Dry Run Preview Enhancement (`cli.py:174-181`)**: Updated dry run preview to use values from `config` object instead of local variables, ensuring consistency between interactive and non-interactive modes.

4. **Add-Agentic Integration (`cli.py:292-294`)**: Integrated `run_add_agentic_wizard()` for existing projects, replacing placeholder with wizard invocation that receives `repo_path` and `detected` settings.

5. **Conditional Logic Refactoring**: Both `init()` and `add_agentic()` now follow pattern:
   ```python
   if interactive:
       config = run_wizard(...)
   else:
       config = build_config_from_flags(...)
   ```

## How to Use

### Interactive Mode for New Projects

```bash
cd tac_bootstrap_cli

# Launch wizard for new project (prompts for all settings)
uv run tac-bootstrap init my-project --interactive

# Launch wizard with pre-selected language (only prompts for remaining options)
uv run tac-bootstrap init my-project --language python --interactive

# The wizard will guide you through:
# 1. Language selection (if not specified)
# 2. Framework selection (filtered by language)
# 3. Package manager selection (filtered by language)
# 4. Architecture pattern selection
# 5. Commands configuration (with smart defaults)
# 6. Worktrees preference
# 7. Configuration summary and confirmation
```

### Interactive Mode for Existing Projects

```bash
cd tac_bootstrap_cli

# Add agentic layer to existing repo with wizard
uv run tac-bootstrap add-agentic /path/to/repo --interactive

# The wizard will:
# 1. Show auto-detected settings as defaults
# 2. Allow overriding detected language/framework/package-manager
# 3. Prompt for commands configuration (critical for existing projects)
# 4. Show summary and request confirmation
```

### Non-Interactive Mode (Original Behavior)

```bash
# Non-interactive mode with all flags specified
uv run tac-bootstrap init my-project \
  --language python \
  --framework fastapi \
  --package-manager uv \
  --architecture ddd \
  --no-interactive

# Dry run to preview what would be created
uv run tac-bootstrap init my-project --interactive --dry-run
```

## Configuration

No additional configuration required. The wizard uses:
- Rich library (already in dependencies: `rich>=13.7.0`)
- Existing helper functions from `domain/models.py`:
  - `get_frameworks_for_language()`
  - `get_package_managers_for_language()`
  - `get_default_commands()`

## Testing

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "test_wizard"
```

### Manual Testing

```bash
# Test wizard import
cd tac_bootstrap_cli
uv run python -c "
from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard
from tac_bootstrap.domain.models import Language
print('✓ Wizard module loaded successfully')
"

# Test interactive init (manual - requires user input)
uv run tac-bootstrap init test-wizard-project --interactive

# Test interactive add-agentic (requires DetectService implementation)
# uv run tac-bootstrap add-agentic /path/to/repo --interactive
```

## Notes

### Wizard Features

- **Numbered Options**: All selections use numbered tables (1, 2, 3...) instead of typing values
- **Visual Defaults**: Default options marked with green `>` indicator
- **Filtered Choices**: Options dynamically filtered based on context (e.g., only valid frameworks for selected language)
- **Progress Feedback**: Green checkmarks (✓) after each selection
- **Color-Coded UI**: Green=success, yellow=warning, cyan=info, dim=secondary text
- **Summary Table**: Final review of all settings before confirmation
- **Abort Capability**: Users can cancel at confirmation step with clean exit

### Integration Status

- ✓ Wizard fully integrated with `init` command
- ✓ Wizard fully integrated with `add-agentic` command
- ✗ `add-agentic` wizard requires DetectService (Phase 6) to function
- ✓ Non-interactive mode preserved for CI/CD and automated workflows

### Architecture Decision

The wizard follows separation of concerns:
- **wizard.py**: Pure UI/interaction logic - builds TACConfig
- **cli.py**: Command orchestration - invokes wizard or builds config from flags
- **scaffold_service.py**: File generation logic - consumes TACConfig
- **detect_service.py** (future): Auto-detection logic - produces DetectedProject

This allows wizard to be reused, tested in isolation, and easily extended with new prompts.

### Future Enhancements

- Save user preferences to `~/.tac-bootstrap/defaults.yml` for reuse
- Add `--expert` mode with advanced configuration prompts
- Template preview before confirmation
- Wizard for `doctor --fix` command
