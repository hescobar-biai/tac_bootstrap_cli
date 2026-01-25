---
doc_type: feature
adw_id: feature_8_3
date: 2026-01-25
idk:
  - trigger_cron
  - polling_interval
  - workflow_detection
  - adw_workflows
  - configurable_triggers
  - template_rendering
  - agentic_spec
tags:
  - feature
  - triggers
  - automation
  - configuration
related_code:
  - adws/adw_triggers/trigger_cron.py
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2
  - tac_bootstrap_cli/tests/test_trigger_templates.py
---

# Configurable Trigger Cron with Multi-Workflow Support

**ADW ID:** feature_8_3
**Date:** 2026-01-25
**Specification:** specs/issue-189-adw-feature_8_3-sdlc_planner-improve-trigger-cron-configurable-workflows.md

## Overview

Enhanced the trigger_cron.py system to support configurable polling intervals and detection of all available ADW workflows, matching the webhook trigger's capabilities. The cron trigger now uses unified workflow detection logic and allows users to customize the polling frequency via CLI arguments and project configuration.

## What Was Built

- **Configurable polling interval** via CLI argument (`--interval`/`-i`) with project-level default
- **Domain model extension** (`AgenticSpec.cron_interval`) for project configuration
- **Template variable substitution** for project name and interval in Jinja2 template
- **Comprehensive test suite** for trigger template rendering with various configurations
- **Unified workflow detection** using `extract_adw_info()` from workflow_ops module

## Technical Implementation

### Files Modified

- `adws/adw_triggers/trigger_cron.py`: Added `DEFAULT_INTERVAL` constant and updated CLI help text to reference project name and configurable default interval
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Added `cron_interval` field to `AgenticSpec` with validation (5-3600 seconds)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`: Updated template to use `{{ config.project.name }}` and `{{ config.agentic.cron_interval | default(20) }}`
- `tac_bootstrap_cli/tests/test_trigger_templates.py`: New test file with comprehensive coverage for template rendering

### Key Changes

1. **Domain Model Extension**: Added `cron_interval` field to `AgenticSpec` (tac_bootstrap_cli/tac_bootstrap/domain/models.py:322-328) with validation constraints ensuring values between 5 and 3600 seconds

2. **Template Parameterization**: Updated trigger_cron.py.j2 template to interpolate project name in docstrings/messages and use configurable interval default from config

3. **CLI Enhancement**: Modified argument parser to use `DEFAULT_INTERVAL` constant and display it in help text, making the default value traceable to project configuration

4. **Test Coverage**: Created comprehensive test suite covering:
   - Custom interval rendering
   - Default interval fallback
   - Special character handling in project names
   - Syntax validation of rendered templates
   - Structural verification of all required components

## How to Use

### Using the Rendered Trigger (in generated projects)

1. Run with default interval (20 seconds or project-configured value):
```bash
uv run adws/adw_triggers/trigger_cron.py
```

2. Run with custom interval (e.g., 30 seconds):
```bash
uv run adws/adw_triggers/trigger_cron.py --interval 30
```

3. View help and supported workflows:
```bash
uv run adws/adw_triggers/trigger_cron.py --help
```

### Configuring in TAC Bootstrap Projects

When scaffolding a new project with TAC Bootstrap CLI, configure the default cron interval in your config file:

```yaml
agentic:
  cron_interval: 30  # Poll every 30 seconds (default: 20)
```

Or via interactive wizard when creating the project.

## Configuration

### Domain Model Field

The `AgenticSpec` model now includes:

- **Field**: `cron_interval`
- **Type**: `int`
- **Default**: 20 seconds
- **Constraints**: Between 5 and 3600 seconds (1 minute to 1 hour)
- **Description**: Polling interval in seconds for cron trigger

### Template Variables

The trigger_cron.py.j2 template uses:

- `{{ config.project.name }}`: Project name (sanitized to lowercase)
- `{{ config.agentic.cron_interval | default(20) }}`: Polling interval with fallback

## Testing

### Run Template Rendering Tests

Test that the template renders correctly with various configurations:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_trigger_templates.py -v
```

### Test Specific Scenarios

Test custom interval configuration:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_trigger_templates.py::test_trigger_cron_template_with_custom_interval -v
```

Test default interval fallback:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_trigger_templates.py::test_trigger_cron_template_with_default_interval -v
```

Test syntax validation:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_trigger_templates.py::test_trigger_cron_template_no_syntax_errors -v
```

### Full Validation Suite

Run all validation commands to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
uv run adws/adw_triggers/trigger_cron.py --help
```

## Notes

- The trigger_cron.py file in the repository root is the rendered version used by TAC Bootstrap itself - it serves both as the functional trigger and as a reference implementation
- The Jinja2 template must stay synchronized with the rendered version, except for variable substitutions
- The 5-second minimum interval prevents excessive API polling that could hit GitHub rate limits
- The 3600-second (1 hour) maximum ensures timely workflow detection while allowing for low-frequency scenarios
- Workflow detection logic is unified with trigger_webhook.py via shared `extract_adw_info()` function, ensuring consistent behavior across trigger types
- Test suite verifies that project names with special characters are properly sanitized in the rendered output
