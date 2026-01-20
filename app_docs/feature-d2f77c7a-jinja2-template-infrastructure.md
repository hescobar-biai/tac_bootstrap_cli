# Jinja2 Template Infrastructure

**ADW ID:** d2f77c7a
**Date:** 2026-01-20
**Specification:** specs/issue-9-adw-d2f77c7a-sdlc_planner-create-jinja2-template-infrastructure.md

## Overview

This feature implements the core template infrastructure for TAC Bootstrap CLI, enabling the system to load, render, and manage Jinja2 templates that generate files for target projects. The implementation includes custom filters for case conversion, robust error handling, and template discovery capabilities.

## What Was Built

- **TemplateRepository**: Main class for managing Jinja2 template operations
- **Custom Filters**: Case conversion filters (snake_case, kebab-case, PascalCase)
- **Error Handling**: Custom exceptions for template-not-found and rendering errors
- **Template Discovery**: Methods to list, check existence, and retrieve template content
- **Comprehensive Tests**: Full test coverage with 475 lines of test code

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`: Core TemplateRepository implementation (378 lines)
- `tac_bootstrap_cli/tests/test_template_repo.py`: Comprehensive unit tests (475 lines)
- `specs/issue-9-adw-d2f77c7a-sdlc_planner-create-jinja2-template-infrastructure.md`: Task specification (117 lines)

### Key Changes

- **TemplateRepository Class**: Configures Jinja2 environment with customized settings:
  - `autoescape`: Only for HTML/XML files for security
  - `trim_blocks=True`: Removes first newline after block tags
  - `lstrip_blocks=True`: Removes leading whitespace in blocks
  - `keep_trailing_newline=True`: Preserves final newline in templates

- **Custom Jinja2 Filters**: Three case conversion filters for code generation:
  - `to_snake_case()`: "MyProject" → "my_project"
  - `to_kebab_case()`: "MyProject" → "my-project"
  - `to_pascal_case()`: "my_project" → "MyProject"

- **Core Methods**:
  - `render(template_name, context)`: Renders template from file
  - `render_string(template_str, context)`: Renders template from string
  - `template_exists(template_name)`: Checks if template exists
  - `list_templates(category)`: Lists available templates, optionally filtered
  - `get_template_content(template_name)`: Retrieves raw template content

- **Exception Handling**: Custom exceptions with descriptive error messages:
  - `TemplateNotFoundError`: Includes template name and search paths
  - `TemplateRenderError`: Wraps Jinja2 errors with context

## How to Use

### Basic Template Rendering

```python
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig

# Initialize the repository
repo = TemplateRepository()

# Load your TAC configuration
config = TACConfig(...)

# Render a template file
output = repo.render("claude/settings.json.j2", config)

# Check if template exists before rendering
if repo.template_exists("adws/sdlc.py.j2"):
    content = repo.render("adws/sdlc.py.j2", config)
```

### Using Custom Filters in Templates

```jinja2
{# In your .j2 template files #}
{{ config.project.name | snake_case }}  # "my-app" → "my_app"
{{ config.project.name | kebab_case }}  # "MyApp" → "my-app"
{{ config.project.name | pascal_case }} # "my_app" → "MyApp"
```

### Rendering Inline Templates

```python
# Render a template string directly
template_string = "{{ config.project.name | snake_case }}"
output = repo.render_string(template_string, config)
```

### Discovering Templates

```python
# List all templates
all_templates = repo.list_templates()

# List templates in a specific category (subdirectory)
claude_templates = repo.list_templates(category="claude")
adw_templates = repo.list_templates(category="adws")
```

## Configuration

### Template Directory Structure

Templates are stored in `tac_bootstrap/templates/` with the following structure:

```
tac_bootstrap/templates/
├── claude/           # Claude configuration templates
├── adws/            # AI Developer Workflow templates
├── scripts/         # Script templates
└── ...              # Other categories
```

### Custom Template Directory

```python
from pathlib import Path

# Use a custom template directory
custom_dir = Path("/path/to/custom/templates")
repo = TemplateRepository(template_dir=custom_dir)
```

## Testing

Run the comprehensive test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py -v
```

Test coverage includes:
- Repository initialization
- Template rendering with TACConfig context
- Custom filter functionality (all case conversions)
- Error handling (template not found, render errors)
- Template discovery and existence checks
- Inline template rendering
- Edge cases (empty strings, special characters, multiple word strings)

## Notes

### DDD Architecture

This module belongs to the Infrastructure layer:
- **Domain**: `TACConfig` (defined in `domain/models.py`)
- **Infrastructure**: `TemplateRepository` (this implementation)
- **Application**: Future services will consume `TemplateRepository`

### Prerequisites for Future Tasks

This infrastructure is required for:
- **TAREA 3.2**: Copying base templates from `.claude/`, `adws/`, `scripts/`
- **TAREA 3.3**: Creating TemplateGeneratorService
- **TAREA 4.x**: Generating real files in target projects

### Jinja2 Configuration Rationale

- `autoescape`: Only HTML/XML to prevent XSS in web templates while allowing Python code generation
- `trim_blocks` + `lstrip_blocks`: Produces cleaner output files without excessive whitespace
- `keep_trailing_newline`: Ensures generated files end with newline (POSIX standard)

### Filter Implementation Details

The case conversion filters handle:
- Camel case: "myProject"
- Pascal case: "MyProject"
- Kebab case: "my-project"
- Snake case: "my_project"
- Spaces: "my project"
- Multiple consecutive capitals: "HTTPServer" → "http_server"
