---
doc_type: feature
adw_id: 0715f107
date: 2026-01-27
idk:
  - template-repository
  - jinja2-rendering
  - case-conversion
  - template-discovery
  - ddd-infrastructure
  - code-generation
tags:
  - feature
  - infrastructure
  - templates
related_code:
  - tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py
  - tac_bootstrap_cli/tests/test_template_repo.py
  - tac_bootstrap_cli/tac_bootstrap/domain/models.py
---

# Jinja2 Template Infrastructure

**ADW ID:** 0715f107
**Date:** 2026-01-27
**Specification:** specs/issue-9-adw-0715f107-sdlc_planner-jinja2-template-infrastructure.md

## Overview

Implemented a robust Jinja2 template infrastructure that serves as the foundation for all code generation in TAC Bootstrap CLI. The TemplateRepository class manages template loading, rendering with flexible context handling, custom case conversion filters, template discovery, and comprehensive error handling.

## What Was Built

- **TemplateRepository Class**: Core infrastructure class in DDD infrastructure layer
- **Custom Exception Types**: TemplateNotFoundError and TemplateRenderError with detailed context
- **Case Conversion Filters**: Three Jinja2 filters for snake_case, kebab-case, and PascalCase transformations
- **Template Discovery**: Methods to list templates by category and check existence
- **Flexible Context Rendering**: Support for both dict and object (TACConfig) contexts
- **Comprehensive Test Suite**: 31+ test cases covering all functionality and edge cases

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`: Complete TemplateRepository implementation with 350+ lines of production code
- `tac_bootstrap_cli/tests/test_template_repo.py`: Comprehensive test suite with 31+ test cases
- `specs/issue-9-adw-0715f107-sdlc_planner-jinja2-template-infrastructure.md`: Feature specification (249 lines)
- `specs/issue-9-adw-0715f107-sdlc_planner-jinja2-template-infrastructure-checklist.md`: Validation checklist

### Key Changes

1. **Exception Handling**: Custom exceptions include template name and search paths for debugging
2. **Jinja2 Environment Configuration**: Configured with trim_blocks, lstrip_blocks, keep_trailing_newline for consistent formatting
3. **Smart Autoescape**: Only HTML/XML templates are autoescaped; code templates (Python, JSON, YAML) render literally
4. **Filter Registration**: Six filter aliases registered (to_snake_case/snake_case, to_kebab_case/kebab_case, to_pascal_case/pascal_case)
5. **Context Flexibility**: render() method accepts dicts (unpacked as kwargs) or objects (passed as 'config' variable)

### Architecture Decisions

Following DDD principles, the TemplateRepository resides in the infrastructure layer (`tac_bootstrap/infrastructure/`), keeping template management separate from domain logic. This enables:
- Domain models (TACConfig) remain independent of rendering concerns
- Application services can use TemplateRepository without coupling to Jinja2 specifics
- Templates directory structure mirrors the generated output structure (claude/, adws/, scripts/)

## How to Use

### Basic Template Rendering

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig

# Initialize repository (uses package templates/ directory by default)
repo = TemplateRepository()

# Create configuration object
config = TACConfig(
    project=ProjectConfig(name="my-project"),
    # ... other config
)

# Render template with object context
output = repo.render("settings.json.j2", config)
```

### Using Case Conversion Filters

Templates can use custom filters for naming convention conversions:

```jinja2
{# Template: example.py.j2 #}
# Project: {{ config.project.name }}
# Snake case: {{ config.project.name | snake_case }}
# Kebab case: {{ config.project.name | kebab_case }}
# Pascal case: {{ config.project.name | pascal_case }}
```

### Template Discovery

```python
# List all templates
all_templates = repo.list_templates()

# List templates in specific category
claude_templates = repo.list_templates("claude")

# Check if template exists
if repo.template_exists("settings.json.j2"):
    output = repo.render("settings.json.j2", config)
```

### Rendering Inline Strings

```python
# Render template string directly
template_str = "Project: {{ config.project.name | snake_case }}"
output = repo.render_string(template_str, config)
```

## Configuration

The TemplateRepository supports optional custom templates directory:

```python
from pathlib import Path

# Use custom templates directory
custom_repo = TemplateRepository(templates_dir=Path("/custom/templates"))
```

By default, templates are loaded from `tac_bootstrap/templates/` within the package directory.

### Jinja2 Environment Settings

- **trim_blocks**: True - Remove newline after template tags
- **lstrip_blocks**: True - Strip leading whitespace from lines
- **keep_trailing_newline**: True - Preserve trailing newline in rendered output
- **autoescape**: Enabled only for .html, .htm, .xml, .xhtml files

## Testing

Run the complete test suite for TemplateRepository:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py -v --tb=short
```

Test specific functionality:

```bash
# Test only case conversion filters
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::test_snake_case_filter -v

# Test template rendering
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py::test_render_with_dict_context -v
```

Run full validation suite:

```bash
# All unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/infrastructure/template_repo.py

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/infrastructure/template_repo.py
```

## Notes

### Case Conversion Examples

The custom filters handle various input formats:

- **to_snake_case**: "MyProject" → "my_project", "my-project" → "my_project", "myProject" → "my_project"
- **to_kebab_case**: "MyProject" → "my-project", "my_project" → "my-project", "myProject" → "my-project"
- **to_pascal_case**: "my-project" → "MyProject", "my_project" → "MyProject", "myProject" → "MyProject"

### Future Enhancements

Potential improvements not included in initial implementation:
- Template validation/linting tool for syntax checking
- Template caching for large template sets (currently relies on Jinja2's internal caching)
- Additional filters (pluralize, truncate, date formatting)
- Template inheritance validation
- Template documentation auto-generation

### Related Features

This infrastructure supports upcoming features:
- TAREA 3.2: Create actual Jinja2 templates for .claude/, adws/, scripts/ directories
- TAREA 4.x: Generator service that uses TemplateRepository to generate files
- TAREA 5.x: CLI commands that trigger template rendering for project initialization

### Test Coverage

The test suite includes 31+ test cases covering:
- Template rendering with dict and object contexts
- All three case conversion filters with edge cases
- Template discovery and listing by category
- Error handling for missing templates and syntax errors
- Autoescape behavior for HTML vs code templates
- Template existence checking and raw content retrieval
