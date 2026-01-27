# Feature: Add settings.local.json.j2 template for output style configuration

## Metadata
issue_number: `299`
adw_id: `feature_Tac_9_task_32`
issue_json: `{"number":299,"title":"Add settings.local.json.j2 template for output style configuration","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_32\n\n**Description:**\nCreate Jinja2 template for local settings override file that configures default output style.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/settings.local.concise.json`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.local.json` (CREATE - rendered)\n\n\n"}`

## Feature Description
This feature adds a Jinja2 template for generating settings.local.json files in generated projects. The settings.local.json file is a Claude Code-specific feature that allows developers to override default output styles without modifying version-controlled settings. This enables "hot swapping" of output styles to optimize token consumption for different scenarios (concise for automation, verbose for interactive development).

The template creates a minimal configuration file pointing to concise-done.md as the default output style. Users can modify this file locally to select different output styles from the available options in .claude/output-styles/.

## User Story
As a developer using TAC Bootstrap to generate projects
I want a settings.local.json template that configures output styles
So that I can customize Claude Code's verbosity locally without committing my preferences to version control

## Problem Statement
Generated projects currently lack a mechanism for developers to locally override Claude Code's output style preferences. Different developers and different workflows (interactive development vs. automated agent workflows) benefit from different output styles, but there's no local configuration file for this purpose. Without settings.local.json:

1. Developers cannot easily switch between concise and verbose output modes
2. Token costs cannot be optimized for automation scenarios
3. Personal preferences for output verbosity cannot be maintained locally
4. The TAC-9 output style "hot swap" pattern documented in the course cannot be utilized

## Solution Statement
Create a minimal Jinja2 template (settings.local.json.j2) that generates a local settings override file with a single field: output_style_file. The template will:

1. Use Claude Code's $CLAUDE_PROJECT_DIR runtime variable (not Jinja2 templating) for path flexibility
2. Default to concise-done.md output style for token efficiency
3. Provide clear documentation via comments on how to change output styles
4. Be added to .gitignore to prevent committing local preferences
5. Not overwrite existing files to preserve user customizations

This approach follows TAC principles of minimalism and YAGNI by focusing solely on output style configuration without additional complexity.

## Relevant Files
Files necessary for implementing this feature:

### Existing Template Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` - Main settings template, provides pattern reference
- `tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2` - Needs update to include settings.local.json
- `.claude/output-styles/concise-done.md` - Default output style referenced in template
- `.claude/output-styles/*.md` - Other available output styles for documentation

### Domain/Application Logic
- `tac_bootstrap_cli/tac_bootstrap/application/template_renderer.py` (likely exists) - Handles template rendering
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Configuration models

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2` (CREATE) - New template file
- `.claude/settings.local.json` (CREATE via rendering) - Rendered example for this repository

## Implementation Plan

### Phase 1: Foundation
1. Review existing template patterns in settings.json.j2 to understand structure
2. Review output-styles/*.md files to document available options
3. Identify where template rendering logic exists in codebase

### Phase 2: Core Implementation
1. Create settings.local.json.j2 template with minimal structure
2. Update .gitignore.j2 to exclude settings.local.json
3. Render settings.local.json for the tac_bootstrap repository itself as example

### Phase 3: Integration
1. Verify template integrates with existing rendering pipeline
2. Test that gitignore properly excludes the file
3. Document the feature in relevant documentation

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create settings.local.json.j2 template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2`
- Use minimal JSON structure with single field: `output_style_file`
- Use `$CLAUDE_PROJECT_DIR` runtime variable (NOT Jinja2 variable)
- Default path: `$CLAUDE_PROJECT_DIR/.claude/output-styles/concise-done.md`
- Add JSON comments (if supported) or documentation explaining how to change styles
- List available output styles: concise-done.md, concise-ultra.md, concise-tts.md, verbose-bullet-points.md, verbose-yaml-structured.md

Template structure:
```json
{
  "output_style_file": "$CLAUDE_PROJECT_DIR/.claude/output-styles/concise-done.md"
}
```

### Task 2: Update .gitignore template
- Open `tac_bootstrap_cli/tac_bootstrap/templates/config/.gitignore.j2`
- Add `.claude/settings.local.json` to gitignore entries
- Place it logically near other local config files (.env.local)
- Add comment explaining it's for local Claude Code preferences

### Task 3: Render settings.local.json for tac_bootstrap repository
- Create `.claude/settings.local.json` in the tac_bootstrap repository root
- Use exact content from the template (no Jinja2 variables since none are used)
- Verify the file uses $CLAUDE_PROJECT_DIR correctly
- This serves as both example and functional configuration

### Task 4: Verify template integration
- Check that template follows existing patterns
- Ensure file would not be overwritten on subsequent generations (user preference file)
- Verify gitignore correctly excludes the file

### Task 5: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No unit tests required for this feature as it's a static template file. The template will be validated through:
1. Manual rendering verification
2. JSON syntax validation
3. Integration with existing template rendering pipeline

### Edge Cases
1. **File already exists**: Should not overwrite (preserve user customizations)
2. **Invalid output style path**: Claude Code will handle validation
3. **Missing $CLAUDE_PROJECT_DIR**: Runtime variable resolved by Claude Code at execution time
4. **Non-existent output style file**: User error, Claude Code will report issue

## Acceptance Criteria
1. ✅ Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.local.json.j2`
2. ✅ Template contains valid JSON with `output_style_file` field
3. ✅ Template uses `$CLAUDE_PROJECT_DIR` runtime variable (not Jinja2 variable)
4. ✅ Default path points to `concise-done.md`
5. ✅ .gitignore.j2 includes `.claude/settings.local.json`
6. ✅ Rendered `.claude/settings.local.json` exists in tac_bootstrap repository
7. ✅ Template follows minimalist approach (single purpose, no bloat)
8. ✅ All validation commands pass with zero errors

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This feature implements the TAC-9 "output style hot swap" pattern documented in Tac-9_1.md:181-200
- The $CLAUDE_PROJECT_DIR variable is a Claude Code runtime variable, not a Jinja2 template variable
- Settings.local.json is analogous to .env.local - both represent local developer preferences
- Future enhancement could include a CLI command to switch output styles programmatically
- Template intentionally minimal following YAGNI principle - users can extend locally if needed
- No custom validation logic needed as Claude Code handles settings schema validation
