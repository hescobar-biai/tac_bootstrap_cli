# Feature: Jinja2 Template Infrastructure

## Metadata
issue_number: `9`
adw_id: `9124c742`
issue_json: `{"number":9,"title":"TAREA 3.1: Crear infraestructura de templates Jinja2","body":"# Prompt para Agente\n\n## Contexto\nTAC Bootstrap genera archivos a partir de templates Jinja2. Necesitamos una clase\nTemplateRepository que maneje la carga y renderizado de templates.\n\nLos templates estaran en `tac_bootstrap/templates/` y se renderizaran con un contexto\nque contiene el TACConfig completo.\n\n## Objetivo\nCrear la clase TemplateRepository que:\n1. Carga templates desde el directorio de templates del paquete\n2. Renderiza templates con contexto\n3. Lista templates disponibles por categoria\n4. Maneja errores de template no encontrado\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`\n\n## Contenido Completo\n\n```python\n\"\"\"Template repository for loading and rendering Jinja2 templates.\n\nThis module provides the infrastructure for loading templates from the\npackage's templates directory and rendering them with configuration context.\n\"\"\"\nimport os\nfrom pathlib import Path\nfrom typing import Dict, Any, Optional, List\nfrom jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape\n\n\nclass TemplateNotFoundError(Exception):\n    \"\"\"Raised when a template cannot be found.\"\"\"\n    pass\n\n\nclass TemplateRenderError(Exception):\n    \"\"\"Raised when a template fails to render.\"\"\"\n    pass\n\n\nclass TemplateRepository:\n    \"\"\"Repository for loading and rendering Jinja2 templates.\n\n    Templates are loaded from the package's templates directory by default.\n    The repository provides methods for rendering templates with context\n    and listing available templates.\n\n    Example:\n        ```python\n        repo = TemplateRepository()\n\n        # Render a template\n        content = repo.render(\"claude/settings.json.j2\", {\"config\": tac_config})\n\n        # List available templates\n        templates = repo.list_templates(\"claude/commands\")\n        ```\n    \"\"\"\n\n    def __init__(self, template_dir: Optional[Path] = None):\n        \"\"\"Initialize the template repository.\n\n        Args:\n            template_dir: Custom template directory. If None, uses package default.\n        \"\"\"\n        if template_dir is None:\n            # Default to package templates directory\n            template_dir = Path(__file__).parent.parent / \"templates\"\n\n        self.template_dir = Path(template_dir)\n\n        if not self.template_dir.exists():\n            # Create directory if it doesn't exist (for development)\n            self.template_dir.mkdir(parents=True, exist_ok=True)\n\n        # Configure Jinja2 environment\n        self.env = Environment(\n            loader=FileSystemLoader(str(self.template_dir)),\n            autoescape=select_autoescape(['html', 'xml']),\n            trim_blocks=True,      # Remove first newline after block tag\n            lstrip_blocks=True,    # Strip leading whitespace from block tags\n            keep_trailing_newline=True,  # Preserve trailing newline in templates\n        )\n\n        # Add custom filters\n        self._register_filters()\n\n    def _register_filters(self) -> None:\n        \"\"\"Register custom Jinja2 filters.\"\"\"\n\n        def to_snake_case(value: str) -> str:\n            \"\"\"Convert string to snake_case.\"\"\"\n            import re\n            s1 = re.sub('(.)([A-Z][a-z]+)', r'\\1_\\2', value)\n            return re.sub('([a-z0-9])([A-Z])', r'\\1_\\2', s1).lower()\n\n        def to_kebab_case(value: str) -> str:\n            \"\"\"Convert string to kebab-case.\"\"\"\n            return to_snake_case(value).replace('_', '-')\n\n        def to_pascal_case(value: str) -> str:\n            \"\"\"Convert string to PascalCase.\"\"\"\n            return ''.join(word.capitalize() for word in value.replace('-', '_').split('_'))\n\n        self.env.filters['snake_case'] = to_snake_case\n        self.env.filters['kebab_case'] = to_kebab_case\n        self.env.filters['pascal_case'] = to_pascal_case\n\n    def render(self, template_name: str, context: Dict[str, Any]) -> str:\n        \"\"\"Render a template with the given context.\n\n        Args:\n            template_name: Name/path of the template file (e.g., \"claude/settings.json.j2\")\n            context: Dictionary of variables to pass to the template\n\n        Returns:\n            Rendered template content as string\n\n        Raises:\n            TemplateNotFoundError: If template doesn't exist\n            TemplateRenderError: If template fails to render\n        \"\"\"\n        try:\n            template = self.env.get_template(template_name)\n            return template.render(**context)\n        except TemplateNotFound:\n            raise TemplateNotFoundError(\n                f\"Template not found: {template_name}\\n\"\n                f\"Searched in: {self.template_dir}\"\n            )\n        except Exception as e:\n            raise TemplateRenderError(\n                f\"Failed to render template {template_name}: {e}\"\n            )\n\n    def render_string(self, template_str: str, context: Dict[str, Any]) -> str:\n        \"\"\"Render a template string with the given context.\n\n        Useful for inline templates or dynamic template generation.\n\n        Args:\n            template_str: Jinja2 template as a string\n            context: Dictionary of variables to pass to the template\n\n        Returns:\n            Rendered content as string\n        \"\"\"\n        try:\n            template = self.env.from_string(template_str)\n            return template.render(**context)\n        except Exception as e:\n            raise TemplateRenderError(f\"Failed to render template string: {e}\")\n\n    def template_exists(self, template_name: str) -> bool:\n        \"\"\"Check if a template exists.\n\n        Args:\n            template_name: Name/path of the template file\n\n        Returns:\n            True if template exists, False otherwise\n        \"\"\"\n        template_path = self.template_dir / template_name\n        return template_path.exists()\n\n    def list_templates(self, category: Optional[str] = None) -> List[str]:\n        \"\"\"List available templates, optionally filtered by category.\n\n        Args:\n            category: Optional subdirectory to filter by (e.g., \"claude/commands\")\n\n        Returns:\n            List of template names relative to template_dir\n        \"\"\"\n        templates = []\n\n        search_dir = self.template_dir\n        if category:\n            search_dir = self.template_dir / category\n\n        if not search_dir.exists():\n            return []\n\n        for root, _, files in os.walk(search_dir):\n            for file in files:\n                if file.endswith(('.j2', '.jinja2')):\n                    full_path = Path(root) / file\n                    rel_path = full_path.relative_to(self.template_dir)\n                    templates.append(str(rel_path))\n\n        return sorted(templates)\n\n    def get_template_content(self, template_name: str) -> str:\n        \"\"\"Get raw template content without rendering.\n\n        Useful for debugging or displaying templates.\n\n        Args:\n            template_name: Name/path of the template file\n\n        Returns:\n            Raw template content\n        \"\"\"\n        template_path = self.template_dir / template_name\n        if not template_path.exists():\n            raise TemplateNotFoundError(f\"Template not found: {template_name}\")\n        return template_path.read_text()"}`

## Feature Description

The TemplateRepository class is the foundational infrastructure for TAC Bootstrap's template system. It provides a clean, type-safe interface for loading and rendering Jinja2 templates that will be used to generate all project files (.claude/settings.json, ADW workflows, command files, etc.). The repository handles template discovery, custom filtering for naming conventions, and robust error handling.

This infrastructure is essential because TAC Bootstrap needs to generate dozens of files across different naming conventions (Python snake_case, CLI kebab-case, class PascalCase) from a single configuration source. The template repository abstracts away Jinja2 complexity and provides a consistent API for all generation services.

## User Story

As a TAC Bootstrap developer
I want a centralized template management system
So that I can reliably render project files from Jinja2 templates with proper error handling and naming convention support

## Problem Statement

TAC Bootstrap must generate multiple file types (Python, JSON, YAML, Markdown, shell scripts) from templates that are parameterized by TACConfig. The current codebase already has a `template_repo.py` file, but issue #9 requires verifying and potentially refactoring it to match the exact specification provided in PLAN_TAC_BOOTSTRAP.md Task 3.1.

The problem is ensuring the template infrastructure:
1. Correctly locates templates in `tac_bootstrap/templates/`
2. Provides custom filters (snake_case, kebab_case, pascal_case) for naming convention conversions
3. Handles missing templates with clear error messages
4. Supports both file-based and string-based template rendering
5. Lists available templates by category for discovery

## Solution Statement

The solution is to review the existing `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` file and ensure it matches the specification in issue #9. The file already exists but needs to be validated against requirements:

1. **TemplateRepository class** with configurable template directory
2. **Custom Jinja2 filters** (to_snake_case, to_kebab_case, to_pascal_case)
3. **Error handling** (TemplateNotFoundError, TemplateRenderError)
4. **Core methods**: render(), render_string(), template_exists(), list_templates(), get_template_content()
5. **Jinja2 configuration**: trim_blocks, lstrip_blocks, keep_trailing_newline, autoescape for HTML/XML only

If the existing implementation differs from the specification, update it to match. If it already matches, document the validation and proceed to testing.

## Relevant Files

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Existing template repository implementation (needs validation)
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig models that will be passed as context
- `tac_bootstrap_cli/tests/test_template_repo.py` - Existing tests for template repository
- `ai_docs/doc/PLAN_TAC_BOOTSTRAP.md` - Master plan with Task 3.1 specification

### Related Files (Context)
- `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py` - Service that will use TemplateRepository
- `tac_bootstrap_cli/tac_bootstrap/templates/` - Template directory (currently exists)

### New Files
None - this task verifies and potentially updates an existing file

## Implementation Plan

### Phase 1: Validation and Analysis
Review the existing template_repo.py implementation against the Task 3.1 specification. Identify any deviations from requirements including exception types, method signatures, Jinja2 configuration, and custom filters.

### Phase 2: Specification Alignment
If deviations are found, update the implementation to match the exact specification. Ensure backward compatibility with existing tests and services that use TemplateRepository.

### Phase 3: Testing and Verification
Run existing tests to verify functionality. Add any missing test cases for edge conditions. Validate that the repository correctly handles template discovery, rendering, and error scenarios.

## Step by Step Tasks

### Task 1: Review Existing Implementation
- Read current `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`
- Compare against specification in issue #9 body
- Document differences in class structure, methods, error handling, and Jinja2 configuration
- Check if custom filters (snake_case, kebab_case, pascal_case) exist and match specification

### Task 2: Validate or Update Exception Classes
- Verify TemplateNotFoundError matches spec (simple pass-through exception)
- Verify TemplateRenderError matches spec (simple pass-through exception)
- If current implementation is more sophisticated (e.g., stores context), decide whether to keep enhancements or match spec exactly
- Document decision and rationale

### Task 3: Validate or Update TemplateRepository.__init__()
- Verify template_dir parameter with Optional[Path] type
- Verify default: `Path(__file__).parent.parent / "templates"`
- Verify auto-creation: `mkdir(parents=True, exist_ok=True)`
- Verify Jinja2 Environment configuration matches:
  - FileSystemLoader with str(template_dir)
  - autoescape=select_autoescape(['html', 'xml'])
  - trim_blocks=True
  - lstrip_blocks=True
  - keep_trailing_newline=True
- Update if necessary

### Task 4: Validate or Update Custom Filters
- Verify _register_filters() method exists
- Verify to_snake_case() implementation with regex patterns
- Verify to_kebab_case() implementation (uses to_snake_case().replace('_', '-'))
- Verify to_pascal_case() implementation with word capitalization
- Verify filters are registered: env.filters['snake_case'], env.filters['kebab_case'], env.filters['pascal_case']
- Test filters with sample inputs (e.g., "MyProjectName" -> "my_project_name", "my-project-name", "MyProjectName")

### Task 5: Validate or Update Core Methods
- Verify render(template_name, context) signature and implementation
- Verify render_string(template_str, context) for inline templates
- Verify template_exists(template_name) returns bool
- Verify list_templates(category: Optional[str]) walks directory and filters .j2/.jinja2 files
- Verify get_template_content(template_name) reads raw template
- Ensure all methods have proper docstrings matching specification

### Task 6: Update Documentation
- Ensure class docstring includes usage example with render() and list_templates()
- Verify all method docstrings include Args, Returns, Raises sections
- Add comments explaining Jinja2 configuration choices (trim_blocks, autoescape scope)

### Task 7: Run Tests and Validation Commands
- Run `cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py -v --tb=short`
- Run `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/infrastructure/template_repo.py`
- Run `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/infrastructure/template_repo.py`
- Fix any failing tests or linting/type issues
- Verify all acceptance criteria are met

## Testing Strategy

### Unit Tests
Existing tests should cover:
- **Initialization**: Template directory creation, default vs custom paths
- **Rendering**: Valid templates with context, template not found errors, render errors
- **Filters**: snake_case, kebab_case, pascal_case conversions with various inputs
- **Discovery**: list_templates() with and without category filter
- **Error Handling**: TemplateNotFoundError with clear messages, TemplateRenderError with context

### Edge Cases
- Empty template directory (list_templates returns [])
- Template with Jinja2 syntax errors (raises TemplateRenderError)
- Missing context variables in template (raises TemplateRenderError)
- Templates in nested subdirectories (correctly listed with relative paths)
- Both .j2 and .jinja2 extensions are discovered
- Non-template files (.py, .txt) are ignored by list_templates()
- Autoescape only affects .html and .xml files, not .py/.json/.yaml

## Acceptance Criteria

1. [ ] TemplateRepository class exists in `tac_bootstrap/infrastructure/template_repo.py`
2. [ ] TemplateNotFoundError and TemplateRenderError exceptions defined
3. [ ] __init__ accepts optional template_dir parameter, defaults to package templates/
4. [ ] Template directory auto-created if missing (for development)
5. [ ] Jinja2 Environment configured with correct settings (trim_blocks, lstrip_blocks, keep_trailing_newline, autoescape for html/xml only)
6. [ ] Custom filters registered: snake_case, kebab_case, pascal_case
7. [ ] render() method handles template loading and context rendering with clear errors
8. [ ] render_string() method supports inline template strings
9. [ ] template_exists() checks template file existence
10. [ ] list_templates() discovers .j2/.jinja2 files with optional category filter
11. [ ] get_template_content() reads raw template without rendering
12. [ ] All methods have type hints and docstrings
13. [ ] Existing tests pass without modification
14. [ ] No regressions in services that use TemplateRepository

## Validation Commands

Execute all commands to verify implementation with zero regressions:

```bash
# Unit tests for template repository
cd tac_bootstrap_cli && uv run pytest tests/test_template_repo.py -v --tb=short

# Lint check
cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/infrastructure/template_repo.py

# Type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/infrastructure/template_repo.py

# Full test suite (ensure no regressions)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Verify CLI still works (smoke test)
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

**Key Design Decisions:**

1. **Auto-directory creation**: The spec includes `mkdir(parents=True, exist_ok=True)` which is a development convenience. This allows infrastructure to be tested before templates exist. In production, the templates directory will always exist within the package.

2. **Autoescape configuration**: `select_autoescape(['html', 'xml'])` only enables autoescaping for HTML/XML files. This is correct because TAC Bootstrap generates Python, JSON, YAML, and Markdown files where autoescape would break the output. This prevents XSS in web templates while preserving code generation correctness.

3. **Both .j2 and .jinja2 extensions**: Supporting both provides flexibility. The codebase can standardize on one in documentation, but the infrastructure handles both without added complexity.

4. **Optional template_dir parameter**: Essential for testing (inject test template directories) and provides flexibility for future use cases (custom template paths). The default behavior (package templates/) works for normal operation.

5. **Custom filters rationale**: The three case conversion filters (snake_case, kebab_case, pascal_case) enable templates to generate files across different naming conventions from a single config value. For example, `{{ config.project.name | snake_case }}` for Python modules, `{{ config.project.name | kebab_case }}` for CLI commands, and `{{ config.project.name | pascal_case }}` for class names.

**Auto-Resolved Clarifications Summary:**
- Include all three custom filters as specified
- Create at current working directory path (not absolute path from different machine)
- Keep auto-creation of templates directory
- Support both .j2 and .jinja2 extensions
- Keep autoescape configuration (only affects HTML/XML)
- Create infrastructure file only, no tests in this task (tests already exist)
- Include optional template_dir parameter

**Implementation Status:**
The file `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` already exists. This task verifies it matches the specification and updates if necessary. The existing implementation may have evolved beyond the spec (e.g., enhanced error messages, IDK comments), which is acceptable as long as core functionality matches.
