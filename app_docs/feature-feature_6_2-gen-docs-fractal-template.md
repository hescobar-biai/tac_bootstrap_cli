# Fractal Documentation Generator Template (gen_docs_fractal)

**ADW ID:** feature_6_2
**Date:** 2026-01-24
**Specification:** specs/issue-170-adw-feature_6_2-sdlc_planner-gen-docs-fractal-template.md

## Overview

Added a Jinja2 template for generating bottom-up fractal documentation that creates one markdown file per directory under `docs/`. The generated script reads Python docstrings and TypeScript JSDoc comments to build comprehensive folder-level documentation with structured frontmatter, processing from deepest directories upward to allow parent folders to summarize child folders.

## What Was Built

- **Template file**: `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2` - Jinja2 template with project-specific variables
- **Generated script**: `scripts/gen_docs_fractal.py` - Rendered output for validation (807 lines)
- **Integration**: Updated `scaffold_service.py` to include script in all generated projects
- **Review checklist**: Comprehensive 58-line checklist for validating implementation

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2`: New Jinja2 template based on reference implementation from `ai_docs/doc/create-crud-entity/generating-fractal-docs/scripts/gen_docs_fractal.py` (816 lines)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:404-411`: Added `gen_docs_fractal.py` to scripts list rendered during scaffolding
- `scripts/gen_docs_fractal.py`: Rendered validation instance with tac-bootstrap project configuration
- `specs/issue-170-adw-feature_6_2-sdlc_planner-gen-docs-fractal-template.md`: Complete 304-line specification
- `specs/issue-170-adw-feature_6_2-sdlc_planner-gen-docs-fractal-template-checklist.md`: Implementation review checklist

### Key Changes

- **PEP 723 inline dependencies**: Added `# dependencies = ["openai", "python-dotenv", "pyyaml"]` header for uv compatibility
- **Jinja2 variable injection**:
  - `{{ config.paths.app_root | default("src") }}` for `--include-root` default
  - `{{ config.project.name }}` in module docstring and LLM prompts
  - `{{ config.project.language }}` for determining file extensions (.py, .ts/.tsx, etc.)
- **OpenAI API integration**: Default to `gpt-4o-mini` model, requires `OPENAI_API_KEY` with fail-fast validation
- **Bottom-up processing**: Processes deepest directories first so parent docs can reference children
- **Complement mode default**: Preserves existing documentation body, only updates frontmatter to prevent data loss
- **Structured frontmatter**: Auto-generates `doc_type`, `domain`, `owner`, `level`, `tags`, `idk`, `related_code`, `children` fields
- **Multi-language support**: Python (*.py) and TypeScript (*.ts, *.tsx) with graceful degradation for unsupported languages
- **Optional canonical IDK**: Loads `canonical_idk.yml` if present, proceeds silently if missing
- **File preservation**: Only modifies files matching generated naming pattern (path-concatenated), preserves all other files

### Architecture Pattern

The template follows a fractal documentation pattern where each directory gets a single markdown file named by concatenating the directory path:

```
src/backend/shared/domain → docs/src/backend/shared/domain.md
src/backend/shared       → docs/src/backend/shared.md
src/backend              → docs/src/backend.md
```

Processing order is depth-first (bottom-up) so:
1. Leaf directories are documented first
2. Parent directories can reference child documentation
3. Frontmatter `children` field is auto-populated from subdirectories

## How to Use

### In Generated Projects

After running `tac-bootstrap init <project>`, the generated project will include:

```bash
# Generate/update fractal documentation
uv run scripts/gen_docs_fractal.py

# Dry run to preview changes
uv run scripts/gen_docs_fractal.py --dry-run

# Specify custom include root
uv run scripts/gen_docs_fractal.py --include-root src/backend

# Regenerate mode (overwrites existing)
uv run scripts/gen_docs_fractal.py --mode generate
```

### CLI Arguments

- `--repo`: Repository root directory (default: current directory)
- `--docs-root`: Output directory for documentation (default: `docs`)
- `--include-root`: Root directory to document (default: from `config.paths.app_root`)
- `--mode`: `complement` (default, preserves body) or `generate` (overwrites)
- `--model`: OpenAI model to use (default: `gpt-4o-mini`)
- `--dry-run`: Preview changes without writing files

### Environment Variables

Required:
- `OPENAI_API_KEY`: OpenAI API key for LLM-based documentation generation

Optional:
- `OPENAI_BASE_URL`: Custom API endpoint (default: `https://api.openai.com/v1`)
- `OPENAI_MODEL`: Override default model

## Configuration

### Project Configuration (config.yml)

The template uses these configuration values:

```yaml
project:
  name: my-project          # Used in frontmatter domain field
  language: python          # Determines file extensions (.py, .ts, etc.)

paths:
  app_root: src            # Default --include-root value
```

### Language Support

Explicitly supported:
- **Python**: Reads module/class/function docstrings from `*.py` files
- **TypeScript**: Reads JSDoc blocks from `*.ts`, `*.tsx` files

For unsupported languages:
- Generates structure-based documentation
- Logs warning but continues processing
- Includes files without docstrings with "No documentation available" placeholder

### Frontmatter Schema

Generated documentation includes YAML frontmatter:

```yaml
---
doc_type: domain           # Auto-detected from path
domain: my-project         # From config.project.name
owner: ""                  # Empty for manual curation
level: 3                   # Auto-calculated from directory depth
tags: ["topic:api"]        # LLM-generated from code analysis
idk: "api routing http"    # Information-dense keywords (5-12)
related_code: []           # Empty for manual curation
children:                  # Auto-populated from subdirectories
  - docs/src/backend/api/routes.md
  - docs/src/backend/api/handlers.md
source_readmes:            # Local READMEs found in folder
  - README.md
last_reviewed: 2026-01-24
---
```

## Testing

### Validation Commands

```bash
# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Generate test project
cd tac_bootstrap_cli && uv run tac-bootstrap init test-project --language python --framework none --architecture ddd

# Test generated script
cd test-project && uv run scripts/gen_docs_fractal.py --dry-run
```

### Edge Cases Handled

- Empty directories (no code files): Generates structure-only documentation
- Directories with only non-Python/TS files: Graceful degradation with warning
- Files without docstrings: Includes with placeholder text
- Invalid YAML in existing docs: Complement mode preserves body, normalizes frontmatter
- Missing parent directories in docs/: Creates automatically
- Missing `OPENAI_API_KEY`: Fails fast with clear error message
- Missing `canonical_idk.yml`: Proceeds silently (optional feature)
- Existing non-generated files in docs/: Preserved (only touches path-concatenated files)

## Notes

### Design Decisions

- **Default to complement mode**: Prevents accidental data loss from user-edited documentation
- **Fail-fast on missing API key**: Clear error message guides users to set `OPENAI_API_KEY`
- **Silent on missing canonical_idk.yml**: IDK vocabulary is optional enhancement, not required
- **Bottom-up processing**: Critical for parent folders to reference children in summaries
- **Path-concatenated naming**: Ensures one-to-one mapping between directories and documentation files
- **Executable permissions**: Script is rendered with 0o755 for direct execution

### Integration with TAC Bootstrap

The template is integrated into `scaffold_service.py:404-411` and rendered for all projects during `tac-bootstrap init`. The script respects project-specific configuration from `config.yml`:

- Python projects get `*.py` file processing by default
- TypeScript projects get `*.ts`, `*.tsx` file processing by default
- Custom `app_root` paths are used for `--include-root` default

### Future Enhancements

- Support for additional languages (Go, Rust, Java)
- Import/dependency analysis for auto-populating `related_code` field
- Interactive mode for confirming overwrites
- Parallel processing for large codebases
- Local LLM support (Ollama integration)
- Metrics dashboard showing documentation coverage
