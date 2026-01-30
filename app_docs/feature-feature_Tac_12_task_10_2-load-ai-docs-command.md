---
doc_type: feature
adw_id: feature_Tac_12_task_10_2
date: 2026-01-30
idk:
  - jinja2
  - template
  - configuration
  - command
  - ai-documentation
  - explore-agent
tags:
  - feature
  - command
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2
  - specs/issue-462-adw-feature_Tac_12_task_10_2-sdlc_planner-load-ai-docs-command.md
---

# Load AI Docs Command - Configurable Path Support

**ADW ID:** feature_Tac_12_task_10_2
**Date:** 2026-01-30
**Specification:** specs/issue-462-adw-feature_Tac_12_task_10_2-sdlc_planner-load-ai-docs-command.md

## Overview

Enhanced the `/load_ai_docs` command template to support configurable AI documentation paths. The template now uses Jinja2 variables to allow generated projects to specify custom documentation directory paths while maintaining the default `ai_docs/doc` path for TAC Bootstrap itself.

## What Was Built

- Updated Jinja2 template with configurable `ai_docs_path` variable
- Added default fallback to `ai_docs/doc` directory
- Maintained all existing command functionality (filtering, Explore agent, error handling)
- Created specification and checklist for implementation tracking

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`: Replaced hardcoded `ai_docs/doc/` paths with Jinja2 variable `{{ config.ai_docs_path | default('ai_docs/doc') }}`

### Key Changes

1. **Configurable Documentation Path**: Replaced all 13 occurrences of hardcoded `ai_docs/doc/` path with `{{ config.ai_docs_path | default('ai_docs/doc') }}`
2. **Default Fallback**: Used Jinja2 `default()` filter to ensure projects without explicit `ai_docs_path` configuration still use the standard TAC path
3. **Preserved All Logic**: No changes to command behavior, filtering syntax, Explore agent usage, or error handling
4. **Template Consistency**: Maintained identical workflow logic between base command and template

## How to Use

### For TAC Bootstrap Development

The base command file `.claude/commands/load_ai_docs.md` continues to use hardcoded `ai_docs/doc/` path:

```bash
/load_ai_docs                    # Load all AI docs from ai_docs/doc/
/load_ai_docs doc_filter=1-3     # Load TAC courses 1-3
/load_ai_docs doc_filter=5       # Load only doc/5.md
```

### For Generated Projects

When generating a new project with `tac-bootstrap`, the command will use the configured path:

```python
# In your project's tac_config.yml
ai_docs_path: "docs/ai"  # Custom path
```

The generated command will automatically use `docs/ai` instead of `ai_docs/doc`:

```bash
/load_ai_docs  # Loads from docs/ai/ directory
```

If no `ai_docs_path` is configured, defaults to `ai_docs/doc`.

## Configuration

### Template Variable

The template accepts a single configuration variable:

- **`config.ai_docs_path`**: Path to AI documentation directory
  - Type: String
  - Default: `"ai_docs/doc"`
  - Example: `"docs/ai"`, `"documentation/guidelines"`, `"ai_docs/doc"`

### Usage in Config Files

Projects can specify custom documentation paths in their configuration:

```yaml
# tac_config.yml (or equivalent)
ai_docs_path: "custom/docs/path"
```

## Testing

### Test Template Rendering

Verify the template renders correctly with default values:

```bash
cd tac_bootstrap_cli
uv run python -c "
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('tac_bootstrap/templates/claude/commands'))
template = env.get_template('load_ai_docs.md.j2')
config = {'ai_docs_path': None}  # Test default
print(template.render(config={'ai_docs_path': None}))
"
```

### Test Custom Path Rendering

Verify the template renders with custom path:

```bash
cd tac_bootstrap_cli
uv run python -c "
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('tac_bootstrap/templates/claude/commands'))
template = env.get_template('load_ai_docs.md.j2')
print(template.render(config={'ai_docs_path': 'docs/ai'}))
" | grep -o "docs/ai" | wc -l
# Should output 13 (number of path references in template)
```

### Run Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Validate Linting and Type Checking

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

- **Default Path Preserved**: Maintained `ai_docs/doc` as default to ensure backward compatibility with existing TAC projects
- **Jinja2 Default Filter**: Used `| default('ai_docs/doc')` instead of conditional logic for cleaner template syntax
- **No Base File Changes**: The base command file `.claude/commands/load_ai_docs.md` remains unchanged with hardcoded paths (as intended for TAC Bootstrap itself)
- **Template-Only Update**: Changes isolated to template file to avoid affecting TAC Bootstrap's own command usage

### Implementation Pattern

This follows the established pattern for TAC Bootstrap templates:
1. Base repository uses hardcoded paths specific to TAC Bootstrap
2. Templates use Jinja2 variables with sensible defaults
3. Generated projects can override defaults via configuration
4. No breaking changes to existing functionality

### Compatibility

- Existing projects using default `ai_docs/doc` path: No changes required
- New projects with custom paths: Configure `ai_docs_path` in project config
- TAC Bootstrap itself: Continues using hardcoded `ai_docs/doc` path from base command file
