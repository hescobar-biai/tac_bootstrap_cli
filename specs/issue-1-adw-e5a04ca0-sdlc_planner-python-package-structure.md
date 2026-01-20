# Feature: Create Python Package Base Structure

## Metadata
issue_number: `1`
adw_id: `e5a04ca0`
issue_json: `{"number":1,"title":"TAREA 1.1: Crear estructura base del paquete Python","body":"# Prompt para Agente\n\n## Contexto\nEstamos creando una CLI en Python llamada \"tac-bootstrap\" que generara Agentic Layers para proyectos.\nNecesitamos crear la estructura base del paquete Python siguiendo buenas practicas.\n\n## Objetivo\nCrear la estructura de directorios y archivos base para el paquete Python `tac_bootstrap`.\n\n## Ubicacion\nCrear todo dentro de: `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/`\n\n## Archivos a Crear\n\n### 1. `pyproject.toml`\nCrear archivo de configuracion del proyecto con:\n- name: \"tac-bootstrap\"\n- version: \"0.1.0\"\n- description: \"CLI to bootstrap Agentic Layer for Claude Code with TAC patterns\"\n- requires-python: \">=3.10\"\n- Sin dependencias aun (se agregaran en siguiente tarea)\n- Entry point: tac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n\n### 2. `tac_bootstrap/__init__.py`\nArchivo vacio con docstring:\n```python\n\"\"\"TAC Bootstrap - CLI to bootstrap Agentic Layer for Claude Code.\"\"\"\n__version__ = \"0.1.0\"\n```\n\n### 3. `tac_bootstrap/__main__.py`\nEntry point para ejecutar como modulo:\n```python\n\"\"\"Allow running as python -m tac_bootstrap.\"\"\"\nfrom tac_bootstrap.interfaces.cli import app\n\nif __name__ == \"__main__\":\n    app()\n```\n\n### 4. Estructura de directorios\nCrear los siguientes directorios con archivos `__init__.py` vacios:\n- `tac_bootstrap/domain/`\n- `tac_bootstrap/application/`\n- `tac_bootstrap/infrastructure/`\n- `tac_bootstrap/interfaces/`\n- `tac_bootstrap/templates/`\n- `tests/`\n\n### 5. `tac_bootstrap/interfaces/cli.py` (stub inicial)\n```python\n\"\"\"CLI interface for TAC Bootstrap.\"\"\"\nimport typer\n\napp = typer.Typer(\n    name=\"tac-bootstrap\",\n    help=\"Bootstrap Agentic Layer for Claude Code with TAC patterns\",\n    add_completion=False,\n)\n\n@app.command()\ndef version():\n    \"\"\"Show version.\"\"\"\n    from tac_bootstrap import __version__\n    print(f\"tac-bootstrap v{__version__}\")\n\nif __name__ == \"__main__\":\n    app()\n```\n\n## Criterios de Aceptacion\n1. [ ] Directorio `tac_bootstrap_cli/` creado con toda la estructura\n2. [ ] `pyproject.toml` valido y parseable\n3. [ ] Todos los `__init__.py` creados\n4. [ ] Estructura sigue convencion de paquetes Python modernos\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\ntree -I __pycache__\ncat pyproject.toml\n```\n\n## NO hacer\n- No instalar dependencias aun\n- No crear archivos de templates aun\n- No implementar logica de negocio"}`

## Feature Description
This feature establishes the foundational Python package structure for the TAC Bootstrap CLI tool. It creates a well-organized, modern Python package layout following Domain-Driven Design (DDD) architecture principles with clear separation of concerns across domain, application, infrastructure, and interface layers. This structure will serve as the foundation for all subsequent development of the CLI tool that generates Agentic Layers for projects.

## User Story
As a developer building the TAC Bootstrap CLI
I want to create a proper Python package structure
So that the codebase is organized, maintainable, and follows modern Python best practices with DDD architecture

## Problem Statement
Currently, the `tac_bootstrap_cli/` directory does not exist. We need to bootstrap a Python package from scratch with a clean, organized structure that will support the development of a CLI tool. The structure must follow Domain-Driven Design principles to ensure clear separation between business logic (domain), use cases (application), external concerns (infrastructure), and user interaction (interfaces).

## Solution Statement
Create a complete Python package structure under `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/` with:

1. A minimal `pyproject.toml` using modern Python packaging standards (PEP 621)
2. A package directory `tac_bootstrap/` with proper `__init__.py` and `__main__.py` for module execution
3. Four DDD architecture layers as subdirectories: `domain/`, `application/`, `infrastructure/`, `interfaces/`
4. A `templates/` directory for future Jinja2 templates
5. A `tests/` directory for unit tests
6. A minimal CLI stub using Typer framework with a version command

This approach ensures the package is immediately executable and provides a solid foundation for incremental development without installing dependencies yet.

## Relevant Files

### Existing Files (for context)
- `config.yml` - Contains project configuration showing `app_root: "tac_bootstrap_cli"` which confirms where to create the package
- `PLAN_TAC_BOOTSTRAP.md` - Master implementation plan containing this exact task (TAREA 1.1)
- `CLAUDE.md` - Guidelines showing the DDD architecture to follow

### New Files
All files will be created under `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/`:

1. `pyproject.toml` - Project metadata and packaging configuration
2. `tac_bootstrap/__init__.py` - Package initialization with version
3. `tac_bootstrap/__main__.py` - Module entry point
4. `tac_bootstrap/domain/__init__.py` - Domain layer initialization
5. `tac_bootstrap/application/__init__.py` - Application layer initialization
6. `tac_bootstrap/infrastructure/__init__.py` - Infrastructure layer initialization
7. `tac_bootstrap/interfaces/__init__.py` - Interface layer initialization
8. `tac_bootstrap/interfaces/cli.py` - CLI interface stub with Typer
9. `tac_bootstrap/templates/` - Directory for templates (no `__init__.py` needed)
10. `tests/__init__.py` - Tests directory initialization

## Implementation Plan

### Phase 1: Foundation
Create the root directory structure and essential package files to establish the package namespace.

**Tasks:**
1. Create root directory `tac_bootstrap_cli/`
2. Create main package directory `tac_bootstrap/`
3. Write `pyproject.toml` with minimal configuration (no dependencies)
4. Write `tac_bootstrap/__init__.py` with version string
5. Write `tac_bootstrap/__main__.py` for module execution support

### Phase 2: Core Implementation
Create the DDD architecture layer directories and the CLI interface stub.

**Tasks:**
1. Create four DDD layer directories with `__init__.py`:
   - `tac_bootstrap/domain/`
   - `tac_bootstrap/application/`
   - `tac_bootstrap/infrastructure/`
   - `tac_bootstrap/interfaces/`
2. Create `tac_bootstrap/templates/` directory (no `__init__.py` - data directory)
3. Create `tests/` directory with `__init__.py`
4. Write `tac_bootstrap/interfaces/cli.py` with minimal Typer app and version command

### Phase 3: Integration
Verify the package structure is correct and all files are properly connected.

**Tasks:**
1. Verify directory tree structure matches expected layout
2. Verify `pyproject.toml` syntax is valid
3. Verify all `__init__.py` files are in place
4. Document the structure in implementation notes

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create Root Package Directories
- Create `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/` directory
- Create `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/` directory
- This establishes the root and package namespace

### Task 2: Write pyproject.toml
- Create `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`
- Include: name, version, description, requires-python, readme, license, authors, keywords
- Include: empty dependencies array (dependencies will be added in next task)
- Include: [project.scripts] section with entry point `tac-bootstrap = "tac_bootstrap.interfaces.cli:app"`
- Include: [build-system] section with hatchling
- Do NOT include any actual dependencies yet - this task only creates structure

### Task 3: Write Package Initialization Files
- Create `tac_bootstrap/__init__.py` with docstring and `__version__ = "0.1.0"`
- Create `tac_bootstrap/__main__.py` that imports and calls `app()` from `tac_bootstrap.interfaces.cli`

### Task 4: Create DDD Layer Directories
- Create `tac_bootstrap/domain/` with empty `__init__.py`
- Create `tac_bootstrap/application/` with empty `__init__.py`
- Create `tac_bootstrap/infrastructure/` with empty `__init__.py`
- Create `tac_bootstrap/interfaces/` with empty `__init__.py`

### Task 5: Create Templates and Tests Directories
- Create `tac_bootstrap/templates/` directory (no `__init__.py` - this is a data directory)
- Create `tests/` directory with empty `__init__.py`

### Task 6: Write CLI Interface Stub
- Create `tac_bootstrap/interfaces/cli.py`
- Import typer
- Create Typer app with name="tac-bootstrap", help text, add_completion=False
- Add `@app.command()` version function that prints version from `tac_bootstrap.__version__`
- Add `if __name__ == "__main__"` block that calls `app()`

### Task 7: Verify Structure and Run Validation
- Run `tree -I __pycache__` to display directory structure
- Run `cat pyproject.toml` to verify content
- Verify all required files exist
- Execute Validation Commands (final step)

## Testing Strategy

### Unit Tests
No unit tests are required for this task as we're only creating file structure and stubs. Tests will be added in subsequent tasks when actual business logic is implemented.

### Edge Cases
- Verify the package can be imported: `python -c "import tac_bootstrap; print(tac_bootstrap.__version__)"`
- Verify the CLI stub runs without errors (note: will fail until dependencies are installed in next task)
- Verify directory structure follows Python package conventions

## Acceptance Criteria
1. Directory `tac_bootstrap_cli/` exists and contains complete package structure
2. `pyproject.toml` is valid, parseable, and contains all required metadata
3. All `__init__.py` files exist in appropriate directories (5 total: main package + 4 DDD layers + tests)
4. Package follows modern Python packaging conventions (PEP 621)
5. DDD architecture layers are clearly separated: domain, application, infrastructure, interfaces
6. Entry point for CLI is properly configured in `pyproject.toml`
7. Version command stub exists in `cli.py`
8. Structure matches the architecture defined in `PLAN_TAC_BOOTSTRAP.md`
9. No dependencies are installed yet (only structure is created)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && tree -I __pycache__` - Verify directory structure
- `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && cat pyproject.toml` - Verify pyproject.toml content
- `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && python -c "import tomllib; tomllib.loads(open('pyproject.toml').read())"` - Validate TOML syntax (Python 3.11+) or use `python -c "import tomli; tomli.loads(open('pyproject.toml', 'rb').read())"` for Python 3.10
- `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && find . -name "__init__.py" | wc -l` - Verify correct number of __init__.py files (should be 6)

## Notes
- This is TAREA 1.1 from PLAN_TAC_BOOTSTRAP.md, Phase 1 (Setup del Proyecto)
- Next task (TAREA 1.2) will add dependencies to pyproject.toml and install them with `uv sync`
- The CLI stub uses Typer but the import won't work until dependencies are installed
- Templates directory intentionally does not have `__init__.py` as it's a data directory
- The package follows src-layout indirectly (tac_bootstrap/ is the package, not src/tac_bootstrap/)
- Using hatchling as build backend (modern, simple alternative to setuptools)
- Entry point configuration allows running as: `tac-bootstrap` (after install), `python -m tac_bootstrap`, or `uv run tac-bootstrap`
- Architecture strictly follows DDD: domain (models), application (services), infrastructure (external systems), interfaces (CLI/UI)
