---
doc_type: feature
adw_id: feature_Tac_9_task_32
date: 2026-01-26
idk:
  - jinja2-template
  - output-style
  - local-configuration
  - claude-code
  - gitignore
tags:
  - feature
  - template
  - configuration
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2
---

# Settings.local.json Template for Output Style Configuration

**ADW ID:** feature_Tac_9_task_32
**Date:** 2026-01-26
**Specification:** specs/issue-299-adw-feature_Tac_9_task_32-sdlc_planner-settings-local-template.md

## Overview

This feature adds a Jinja2 template for generating settings.local.json files in projects created with TAC Bootstrap. The settings.local.json file allows developers to override Claude Code's default output style without committing their preferences to version control, enabling "hot swapping" of output styles to optimize token consumption for different workflows.

## What Was Built

- **settings.local.json.j2 template**: Minimal JSON template with single field for output style configuration
- **.gitignore update**: Added .claude/settings.local.json to prevent committing local preferences
- **Runtime variable usage**: Uses $CLAUDE_PROJECT_DIR instead of Jinja2 templating for path flexibility
- **Default configuration**: Points to concise-done.md output style for token efficiency

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2`: New template file created with minimal JSON structure containing single output_style_file field
- `tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2`: Added .claude/settings.local.json with explanatory comment about local Claude Code preferences

### Key Changes

1. Created minimal settings.local.json.j2 template using $CLAUDE_PROJECT_DIR runtime variable (not Jinja2 variable)
2. Default output style set to concise-done.md for optimal token consumption
3. Added gitignore rule to exclude settings.local.json from version control
4. Template follows minimalist YAGNI principle with single-purpose configuration
5. No custom validation logic needed as Claude Code handles settings schema validation

### Template Structure

```json
{
  "output_style_file": "$CLAUDE_PROJECT_DIR/.claude/output-styles/concise-done.md"
}
```

The $CLAUDE_PROJECT_DIR variable is resolved at runtime by Claude Code, allowing the same configuration to work across different project paths.

## How to Use

### For Generated Projects

1. When generating a new project with TAC Bootstrap, the settings.local.json.j2 template will be available
2. After project generation, create `.claude/settings.local.json` in your project root
3. Copy the template content or customize the output_style_file path

### Changing Output Styles

1. Open `.claude/settings.local.json` in your project
2. Modify the output_style_file path to point to a different style:

Available output styles:
- `concise-done.md` - Minimal output for automation (default)
- `concise-ultra.md` - Ultra-brief responses
- `concise-tts.md` - Text-to-speech optimized
- `verbose-bullet-points.md` - Detailed bullet-point format
- `verbose-yaml-structured.md` - Structured YAML format

Example:
```json
{
  "output_style_file": "$CLAUDE_PROJECT_DIR/.claude/output-styles/verbose-bullet-points.md"
}
```

3. Save the file - changes take effect immediately in Claude Code

## Configuration

### Gitignore Entry

The .gitignore.j2 template now includes:
```gitignore
# Local Claude Code preferences (never commit!)
.claude/settings.local.json
```

This prevents accidentally committing personal output style preferences to shared repositories.

### Template Location

- **Template file**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2`
- **Generated file**: `.claude/settings.local.json` (in generated projects)
- **Referenced files**: Output styles in `.claude/output-styles/` directory

## Testing

### Verify Template Exists

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2
```

### Verify Gitignore Rule

```bash
grep -A 1 "Local Claude Code preferences" tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2
```

### Run Full Validation Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This feature implements the TAC-9 "output style hot swap" pattern documented in Tac-9_1.md:181-200
- The $CLAUDE_PROJECT_DIR variable is a Claude Code runtime variable, not a Jinja2 template variable
- Settings.local.json is analogous to .env.local - both represent local developer preferences that should not be version controlled
- Template intentionally minimal following YAGNI principle - users can extend locally if needed
- Future enhancement could include a CLI command to switch output styles programmatically
- No unit tests required as this is a static template file validated through integration with existing rendering pipeline
