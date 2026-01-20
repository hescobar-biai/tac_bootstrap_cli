# Claude Code Hooks Templates

**ADW ID:** fbc4585b
**Date:** 2026-01-20
**Specification:** specs/issue-14-adw-fbc4585b-sdlc_planner-create-hooks-templates.md

## Overview

Created Jinja2 templates for Claude Code hooks that provide validation, logging, and cleanup functionality for AI development workflows. These templates enable TAC Bootstrap CLI to generate parametrizable, safety-focused hooks for any project based on its configuration.

## What Was Built

This implementation includes five Jinja2 templates that generate Python hooks for Claude Code:

- **pre_tool_use.py.j2** - Pre-execution validation hook that blocks dangerous operations
- **post_tool_use.py.j2** - Post-execution logging hook for auditing tool usage
- **stop.py.j2** - Session cleanup hook that generates summaries
- **utils/__init__.py.j2** - Package initialization for hook utilities
- **utils/constants.py.j2** - Shared constants and helper functions

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`: Pre-execution validation hook with comprehensive rm command detection and forbidden path validation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2`: Post-execution logging hook that captures all tool usage to session logs
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2`: Session termination hook with optional chat transcript export
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2`: Package init file with project-specific docstring
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2`: Centralized constants for project metadata, paths, and safety configuration

### Key Changes

**Pre-Tool Use Hook (153 lines):**
- Implements comprehensive dangerous command detection with regex patterns for rm -rf variations
- Validates file operations against forbidden paths from `config.agentic.safety.forbidden_paths`
- Blocks tool calls by exiting with code 2 when violations detected
- Logs all pre-tool validation attempts to session-specific log files

**Post-Tool Use Hook (61 lines):**
- Captures all tool usage data (tool_name, tool_input, session_id) to JSON logs
- Creates session-specific log directories under `{{ config.paths.logs_dir }}/{session_id}/`
- Implements graceful error handling to prevent logging failures from breaking tool execution
- Maintains append-only log for complete audit trail

**Stop Hook (92 lines):**
- Generates session summary when Claude Code session ends
- Supports `--chat` flag to copy transcript to session logs as formatted JSON
- Converts JSONL transcript format to structured JSON array
- Handles missing transcripts and decode errors gracefully

**Utils Constants (77 lines):**
- Exposes all project configuration as Python constants (PROJECT_NAME, LANGUAGE, PACKAGE_MANAGER)
- Provides centralized path constants (LOG_DIR, SPECS_DIR, ADWS_DIR, etc.)
- Defines FORBIDDEN_PATHS and ALLOWED_PATHS lists from safety configuration
- Includes helper functions `get_session_log_dir()` and `ensure_session_log_dir()`

## How to Use

### 1. Templates are Used Automatically by TAC Bootstrap

When you run `tac-bootstrap init`, these templates are rendered with your project's configuration:

```bash
# Initialize a new project - hooks templates will be generated automatically
tac-bootstrap init my-project
```

### 2. Configuration Variables

The templates use variables from `config.yml`:

```yaml
project:
  name: "my-project"
  language: python
  package_manager: uv

paths:
  logs_dir: "logs"
  specs_dir: "specs"
  adws_dir: "adws"
  scripts_dir: "scripts"
  prompts_dir: "prompts"

agentic:
  safety:
    forbidden_paths:
      - ".env"
      - "secrets/"
      - "credentials.json"
    allowed_paths:
      - "src/"
      - "tests/"
```

### 3. Generated Hooks Location

After running `tac-bootstrap init`, the hooks will be generated in your project:

```
my-project/
└── .claude/
    └── hooks/
        ├── pre_tool_use.py      # Generated from .j2 template
        ├── post_tool_use.py     # Generated from .j2 template
        ├── stop.py              # Generated from .j2 template
        └── utils/
            ├── __init__.py      # Generated from .j2 template
            └── constants.py     # Generated from .j2 template
```

### 4. Hook Behavior

**Pre-Tool Use Hook:**
- Automatically validates every tool call before execution
- Blocks dangerous rm commands (rm -rf, rm -fr, etc.)
- Prevents access to forbidden paths (.env, secrets/, etc.)
- Logs validation attempts to `logs/{session_id}/pre_tool_use.json`

**Post-Tool Use Hook:**
- Automatically logs every successful tool execution
- Captures tool_name, tool_input, session_id
- Writes to `logs/{session_id}/post_tool_use.json`
- Never fails (best-effort logging)

**Stop Hook:**
- Runs when Claude Code session ends
- Logs session metadata to `logs/{session_id}/stop.json`
- With `--chat` flag: exports transcript to `logs/{session_id}/chat.json`

## Configuration

### Customizing Safety Rules

Edit your project's `config.yml` to customize hook behavior:

```yaml
agentic:
  safety:
    forbidden_paths:
      - ".env"
      - "secrets/"
      - "api_keys/"
      - ".ssh/"
    allowed_paths:
      - "src/"
      - "tests/"
      - "docs/"
```

### Customizing Log Paths

Change where hooks store session logs:

```yaml
paths:
  logs_dir: "custom/logs/path"  # Defaults to "logs"
```

### Template Variables Reference

All templates have access to these variables:

- `{{ config.project.name }}` - Project name
- `{{ config.project.language.value }}` - Programming language
- `{{ config.project.package_manager.value }}` - Package manager (npm, uv, etc.)
- `{{ config.paths.logs_dir }}` - Logs directory path
- `{{ config.paths.specs_dir }}` - Specs directory path
- `{{ config.paths.adws_dir }}` - ADWs directory path
- `{{ config.agentic.safety.forbidden_paths }}` - List of forbidden paths
- `{{ config.agentic.safety.allowed_paths }}` - List of allowed paths

## Testing

### Unit Tests

Run the test suite to verify template rendering:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "hooks"
```

### Manual Template Rendering Test

Test template rendering with sample configuration:

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig

# Load your config
config = TACConfig.from_yaml("config.yml")

# Render a template
repo = TemplateRepository()
rendered = repo.render_template("claude/hooks/pre_tool_use.py.j2", config=config)
print(rendered[:200])  # View first 200 characters
```

### Smoke Test

Verify the CLI works with new templates:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

- **Shebang Choice**: Templates use `#!/usr/bin/env python3` instead of `#!/usr/bin/env -S uv run --script` for maximum compatibility
- **No External Dependencies**: Hooks only use Python stdlib (json, sys, os, pathlib) to avoid dependency issues
- **Cross-Platform Paths**: All path handling uses `pathlib.Path()` for Windows/macOS/Linux compatibility
- **Best-Effort Logging**: Post-tool and stop hooks never fail - logging errors are silently handled
- **Strict Validation**: Pre-tool hook is strict - blocks and reports violations clearly

### Dangerous Command Detection

The pre_tool_use hook detects these rm patterns:
- `rm -rf` (and all flag order variations: -fr, -Rf, etc.)
- `rm --recursive --force` (long flags)
- `rm -r ... -f` (separated flags)
- Combined with dangerous paths: `/`, `~`, `*`, `..`, etc.

### Session Log Structure

Each Claude Code session creates a log directory:

```
logs/
└── {session_id}/
    ├── pre_tool_use.json    # All pre-validation events
    ├── post_tool_use.json   # All tool executions
    ├── stop.json            # Session termination data
    └── chat.json            # Optional transcript (with --chat)
```

### Future Enhancements

Potential improvements for future versions:
- Add more sophisticated command validation patterns
- Include statistics in session summaries (tool counts, error rates)
- Add support for custom validation rules via config
- Implement log rotation for long-running projects
