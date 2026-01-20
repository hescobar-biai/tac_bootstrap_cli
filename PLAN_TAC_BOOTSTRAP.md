# Plan de Implementacion: TAC Bootstrap CLI

## Resumen Ejecutivo

**TAC Bootstrap** es una CLI en Python que crea o inyecta una **Agentic Layer** basada en Claude Code para acelerar ingenieria con patrones TAC (Tactical Agentic Coding).

**Objetivo**: Reducir el tiempo de setup agentic de dias/semanas a **minutos** y estandarizar como se hace ingenieria con agentes en cualquier repositorio.

---

## Flujo de Usuario

```
Usuario ejecuta: tac-bootstrap init
                      |
                      v
        +---------------------------+
        |   Es proyecto NUEVO o     |
        |      EXISTENTE?           |
        +---------------------------+
              |             |
              v             v
          [NUEVO]      [EXISTENTE]
              |             |
              v             v
    Pregunta:         Auto-detecta:
    - Lenguaje        - Lenguaje
    - Framework       - Framework
    - Arquitectura    - Package manager
    - Pkg manager
    - Comandos        Pregunta:
                      - Comandos reales
                      - Worktrees on/off
              |             |
              v             v
        +---------------------------+
        |   GENERA AGENTIC LAYER    |
        +---------------------------+
                      |
                      v
            Proyecto listo para
            trabajar con agentes!
```

---

## Arquitectura de la Solucion

```
tac_bootstrap/
├── pyproject.toml
├── tac_bootstrap/
│   ├── __init__.py
│   ├── __main__.py
│   ├── domain/
│   │   ├── models.py          # ProjectSpec, AgenticSpec, Commands (Pydantic)
│   │   └── plan.py            # ScaffoldPlan, FileOperation
│   ├── application/
│   │   ├── scaffold_service.py # build_plan + apply_plan
│   │   ├── detect_service.py   # auto-detect stack
│   │   └── doctor_service.py   # validacion setup
│   ├── infrastructure/
│   │   ├── template_repo.py    # Jinja2 templates
│   │   ├── fs.py               # File operations idempotentes
│   │   └── git_adapter.py      # Git operations
│   ├── interfaces/
│   │   ├── cli.py              # Typer commands
│   │   └── wizard.py           # Rich interactive wizard
│   └── templates/              # Templates Jinja2 parametrizables
│       ├── claude/
│       ├── adws/
│       ├── scripts/
│       └── config/
└── tests/
```

---

## Comandos CLI

| Comando | Descripcion |
|---------|-------------|
| `tac-bootstrap init` | Crea proyecto nuevo (app + agentic layer) |
| `tac-bootstrap add-agentic --repo .` | Inyecta agentic layer en repo existente |
| `tac-bootstrap doctor --repo .` | Valida setup y sugiere correcciones |
| `tac-bootstrap render --config config.yml` | Re-genera desde YAML (idempotente) |

---

# PLAN DE TAREAS (0-100%)

Cada tarea esta escrita como un **prompt completo** para ser ejecutado por un agente LLM.

---

## FASE 1: Setup del Proyecto (0-10%)

---

### TAREA 1.1: Crear estructura base del paquete Python

```markdown
# Prompt para Agente

## Contexto
Estamos creando una CLI en Python llamada "tac-bootstrap" que generara Agentic Layers para proyectos.
Necesitamos crear la estructura base del paquete Python siguiendo buenas practicas.

## Objetivo
Crear la estructura de directorios y archivos base para el paquete Python `tac_bootstrap`.

## Ubicacion
Crear todo dentro de: `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/`

## Archivos a Crear

### 1. `pyproject.toml`
Crear archivo de configuracion del proyecto con:
- name: "tac-bootstrap"
- version: "0.1.0"
- description: "CLI to bootstrap Agentic Layer for Claude Code with TAC patterns"
- requires-python: ">=3.10"
- Sin dependencias aun (se agregaran en siguiente tarea)
- Entry point: tac-bootstrap = "tac_bootstrap.interfaces.cli:app"

### 2. `tac_bootstrap/__init__.py`
Archivo vacio con docstring:
```python
"""TAC Bootstrap - CLI to bootstrap Agentic Layer for Claude Code."""
__version__ = "0.1.0"
```

### 3. `tac_bootstrap/__main__.py`
Entry point para ejecutar como modulo:
```python
"""Allow running as python -m tac_bootstrap."""
from tac_bootstrap.interfaces.cli import app

if __name__ == "__main__":
    app()
```

### 4. Estructura de directorios
Crear los siguientes directorios con archivos `__init__.py` vacios:
- `tac_bootstrap/domain/`
- `tac_bootstrap/application/`
- `tac_bootstrap/infrastructure/`
- `tac_bootstrap/interfaces/`
- `tac_bootstrap/templates/`
- `tests/`

### 5. `tac_bootstrap/interfaces/cli.py` (stub inicial)
```python
"""CLI interface for TAC Bootstrap."""
import typer

app = typer.Typer(
    name="tac-bootstrap",
    help="Bootstrap Agentic Layer for Claude Code with TAC patterns",
    add_completion=False,
)

@app.command()
def version():
    """Show version."""
    from tac_bootstrap import __version__
    print(f"tac-bootstrap v{__version__}")

if __name__ == "__main__":
    app()
```

## Criterios de Aceptacion
1. [ ] Directorio `tac_bootstrap_cli/` creado con toda la estructura
2. [ ] `pyproject.toml` valido y parseable
3. [ ] Todos los `__init__.py` creados
4. [ ] Estructura sigue convencion de paquetes Python modernos

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
tree -I __pycache__
cat pyproject.toml
```

## NO hacer
- No instalar dependencias aun
- No crear archivos de templates aun
- No implementar logica de negocio
```

---

### TAREA 1.2: Configurar dependencias del proyecto

```markdown
# Prompt para Agente

## Contexto
Ya tenemos la estructura base del paquete `tac_bootstrap_cli`. Ahora necesitamos configurar
las dependencias del proyecto para poder usar las librerias necesarias.

## Objetivo
Actualizar `pyproject.toml` con todas las dependencias necesarias e instalarlas con `uv`.

## Archivo a Modificar
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`

## Dependencias Requeridas

### Dependencias de Produccion
```toml
dependencies = [
    "typer>=0.9.0",        # CLI framework - maneja comandos, argumentos, opciones
    "rich>=13.0.0",        # UI terminal - tablas, paneles, colores, progress bars
    "jinja2>=3.0.0",       # Templates - renderizado de archivos parametrizables
    "pydantic>=2.0.0",     # Validacion - schemas para config.yml y modelos
    "pyyaml>=6.0.0",       # YAML - lectura/escritura de config.yml
    "gitpython>=3.1.0",    # Git - operaciones git init, commit, etc.
]
```

### Dependencias de Desarrollo
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",       # Testing framework
    "pytest-cov>=4.0.0",   # Coverage reports
    "mypy>=1.0.0",         # Type checking
    "ruff>=0.1.0",         # Linting y formatting
]
```

### Entry Points
```toml
[project.scripts]
tac-bootstrap = "tac_bootstrap.interfaces.cli:app"
```

### Build System
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Acciones a Ejecutar

1. Actualizar `pyproject.toml` con el contenido completo
2. Ejecutar `uv sync` para instalar dependencias
3. Verificar que `tac-bootstrap --help` funciona

## pyproject.toml Completo

```toml
[project]
name = "tac-bootstrap"
version = "0.1.0"
description = "CLI to bootstrap Agentic Layer for Claude Code with TAC patterns"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "TAC Team"}
]
keywords = ["cli", "claude", "agentic", "tac", "bootstrap"]

dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "jinja2>=3.0.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0.0",
    "gitpython>=3.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
tac-bootstrap = "tac_bootstrap.interfaces.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

## Criterios de Aceptacion
1. [ ] `pyproject.toml` actualizado con todas las dependencias
2. [ ] `uv sync` ejecuta sin errores
3. [ ] `uv run tac-bootstrap --help` muestra ayuda
4. [ ] `uv run tac-bootstrap version` muestra "tac-bootstrap v0.1.0"

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv sync
uv run tac-bootstrap --help
uv run tac-bootstrap version
```

## NO hacer
- No implementar comandos adicionales aun
- No crear tests aun
```

---

## FASE 2: Modelos de Dominio (10-20%)

---

### TAREA 2.1: Crear modelos Pydantic para configuracion

```markdown
# Prompt para Agente

## Contexto
TAC Bootstrap usa un archivo `config.yml` como fuente de verdad declarativa. Necesitamos
modelos Pydantic que representen este schema y permitan validar la configuracion.

El config.yml tiene esta estructura:
- project: nombre, modo (new/existing), lenguaje, framework, arquitectura, package manager
- paths: rutas de app, agentic layer, prompts, adws, specs, logs, scripts, worktrees
- commands: start, build, test, lint, typecheck, format
- agentic: provider, model_policy, worktrees config, logging, safety, workflows
- claude: settings para .claude/settings.json, comandos slash
- templates: rutas a templates de prompts
- bootstrap: opciones para proyecto nuevo (git, license, readme)

## Objetivo
Crear modelos Pydantic completos en `domain/models.py` que representen todo el schema
de `config.yml` con validacion, defaults inteligentes y documentacion.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py`

## Contenido Completo

```python
"""Domain models for TAC Bootstrap configuration.

These models represent the config.yml schema and provide validation,
defaults, and documentation for all configuration options.
"""
from enum import Enum
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


# =============================================================================
# ENUMS - Opciones validas para configuracion
# =============================================================================

class Language(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"


class Framework(str, Enum):
    """Supported frameworks by language."""
    # Python
    FASTAPI = "fastapi"
    DJANGO = "django"
    FLASK = "flask"
    # TypeScript/JavaScript
    NEXT = "next"
    NEST = "nest"
    EXPRESS = "express"
    REACT = "react"
    VUE = "vue"
    # Go
    GIN = "gin"
    ECHO = "echo"
    # Generic
    CUSTOM = "custom"
    NONE = "none"


class Architecture(str, Enum):
    """Software architecture patterns."""
    SIMPLE = "simple"           # Flat structure, minimal organization
    LAYERED = "layered"         # Controllers/Services/Repositories
    DDD = "ddd"                 # Domain-Driven Design
    CLEAN = "clean"            # Clean Architecture (Uncle Bob)
    HEXAGONAL = "hexagonal"    # Ports & Adapters


class PackageManager(str, Enum):
    """Package managers by language."""
    # Python
    UV = "uv"
    POETRY = "poetry"
    PIP = "pip"
    # Node.js
    PNPM = "pnpm"
    NPM = "npm"
    BUN = "bun"
    YARN = "yarn"
    # Go
    GO = "go"
    # Rust
    CARGO = "cargo"


class ProjectMode(str, Enum):
    """Project initialization mode."""
    NEW = "new"           # Create new project from scratch
    EXISTING = "existing"  # Inject into existing project


class AgenticProvider(str, Enum):
    """Agentic provider options."""
    CLAUDE_CODE = "claude_code"


class RunIdStrategy(str, Enum):
    """Strategy for generating run IDs."""
    UUID = "uuid"
    TIMESTAMP = "timestamp"


class DefaultWorkflow(str, Enum):
    """Available default workflows."""
    SDLC_ISO = "sdlc_iso"
    PATCH_ISO = "patch_iso"
    PLAN_IMPLEMENT = "plan_implement"


# =============================================================================
# SUB-MODELS - Componentes de configuracion
# =============================================================================

class ProjectSpec(BaseModel):
    """Project specification from config.yml."""
    name: str = Field(..., description="Project name (used for directory and package)")
    mode: ProjectMode = Field(ProjectMode.EXISTING, description="new = create project, existing = inject only")
    repo_root: str = Field(".", description="Root directory of the repository")
    language: Language = Field(..., description="Primary programming language")
    framework: Optional[Framework] = Field(None, description="Framework to use (optional)")
    architecture: Architecture = Field(Architecture.SIMPLE, description="Software architecture pattern")
    package_manager: PackageManager = Field(..., description="Package manager for the language")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is valid for directory/package naming."""
        if not v or not v.strip():
            raise ValueError("Project name cannot be empty")
        # Remove spaces and special chars for safety
        return v.strip().lower().replace(" ", "-")


class PathsSpec(BaseModel):
    """Path configuration for the project."""
    app_root: str = Field("src", description="Where the application code lives")
    agentic_root: str = Field(".", description="Where to install agentic layer (usually root)")
    prompts_dir: str = Field("prompts", description="Directory for prompt templates")
    adws_dir: str = Field("adws", description="Directory for AI Developer Workflows")
    specs_dir: str = Field("specs", description="Directory for issue/feature specifications")
    logs_dir: str = Field("logs", description="Directory for session logs")
    scripts_dir: str = Field("scripts", description="Directory for utility scripts")
    worktrees_dir: str = Field("trees", description="Directory for git worktrees")


class CommandsSpec(BaseModel):
    """Commands for project operations.

    These are the actual shell commands to run the project.
    They will be used by agents and scripts.
    """
    start: str = Field(..., description="Command to start the application")
    build: Optional[str] = Field(None, description="Command to build/compile")
    test: str = Field(..., description="Command to run tests")
    lint: Optional[str] = Field(None, description="Command to run linter")
    typecheck: Optional[str] = Field(None, description="Command to run type checker")
    format: Optional[str] = Field(None, description="Command to format code")


class WorktreeConfig(BaseModel):
    """Git worktree configuration for parallel execution."""
    enabled: bool = Field(True, description="Enable git worktrees for isolation")
    max_parallel: int = Field(5, description="Maximum parallel worktrees", ge=1, le=20)
    naming: str = Field("feat-{slug}-{timestamp}", description="Worktree naming pattern")


class LoggingConfig(BaseModel):
    """Logging configuration for ADWs."""
    level: str = Field("INFO", description="Log level (DEBUG, INFO, WARNING, ERROR)")
    capture_agent_transcript: bool = Field(True, description="Save full agent transcripts")
    run_id_strategy: RunIdStrategy = Field(RunIdStrategy.UUID, description="How to generate run IDs")


class SafetyConfig(BaseModel):
    """Safety configuration for agent operations."""
    require_tests_pass: bool = Field(True, description="Require tests to pass before shipping")
    require_review_artifacts: bool = Field(True, description="Require review screenshots/logs")
    allowed_paths: List[str] = Field(
        default_factory=lambda: ["src/", "apps/", "adws/", "prompts/", "specs/", "scripts/"],
        description="Paths agents are allowed to modify"
    )
    forbidden_paths: List[str] = Field(
        default_factory=lambda: [".env", "secrets/", ".git/config"],
        description="Paths agents must never modify"
    )


class AgenticSpec(BaseModel):
    """Agentic layer configuration."""
    provider: AgenticProvider = Field(AgenticProvider.CLAUDE_CODE, description="Agentic provider")
    model_policy: Dict[str, str] = Field(
        default_factory=lambda: {"default": "sonnet", "heavy": "opus"},
        description="Model selection policy"
    )
    worktrees: WorktreeConfig = Field(default_factory=WorktreeConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    safety: SafetyConfig = Field(default_factory=SafetyConfig)
    workflows: List[str] = Field(
        default_factory=lambda: ["sdlc_iso", "patch_iso", "plan_implement"],
        description="Available workflows"
    )
    default_workflow: str = Field("sdlc_iso", description="Default workflow to use")


class ClaudeSettings(BaseModel):
    """Settings for .claude/settings.json."""
    project_name: str = Field(..., description="Project name for Claude Code")
    preferred_style: str = Field("concise", description="Response style preference")
    allow_shell: bool = Field(True, description="Allow shell command execution")


class ClaudeCommandsConfig(BaseModel):
    """Mapping of slash commands to prompt files."""
    prime: str = Field(".claude/commands/prime.md", description="Priming command")
    start: str = Field(".claude/commands/start.md", description="Start app command")
    build: str = Field(".claude/commands/build.md", description="Build command")
    test: str = Field(".claude/commands/test.md", description="Test command")
    review: str = Field(".claude/commands/review.md", description="Review command")
    ship: str = Field(".claude/commands/ship.md", description="Ship/deploy command")


class ClaudeConfig(BaseModel):
    """Claude Code configuration."""
    settings: ClaudeSettings
    commands: ClaudeCommandsConfig = Field(default_factory=ClaudeCommandsConfig)


class TemplatesConfig(BaseModel):
    """Template paths for meta-prompts."""
    plan_template: str = Field("prompts/templates/plan.md", description="Plan generation template")
    chore_template: str = Field("prompts/templates/chore.md", description="Chore task template")
    feature_template: str = Field("prompts/templates/feature.md", description="Feature planning template")
    bug_template: str = Field("prompts/templates/bug.md", description="Bug fixing template")
    review_template: str = Field("prompts/templates/review.md", description="Review checklist template")


class BootstrapConfig(BaseModel):
    """Bootstrap-specific configuration (for new projects only)."""
    create_git_repo: bool = Field(True, description="Initialize git repository")
    initial_commit: bool = Field(True, description="Create initial commit")
    license: str = Field("MIT", description="License type")
    readme: bool = Field(True, description="Generate README.md")


# =============================================================================
# ROOT MODEL - config.yml completo
# =============================================================================

class TACConfig(BaseModel):
    """Root configuration model for config.yml.

    This is the main model that represents the entire config.yml file.
    It validates all sections and provides smart defaults.

    Example usage:
        ```python
        import yaml
        from tac_bootstrap.domain.models import TACConfig

        with open("config.yml") as f:
            data = yaml.safe_load(f)

        config = TACConfig(**data)
        print(config.project.name)
        print(config.commands.start)
        ```
    """
    version: int = Field(1, description="Config schema version")
    project: ProjectSpec = Field(..., description="Project specification")
    paths: PathsSpec = Field(default_factory=PathsSpec, description="Path configuration")
    commands: CommandsSpec = Field(..., description="Shell commands")
    agentic: AgenticSpec = Field(default_factory=AgenticSpec, description="Agentic layer config")
    claude: ClaudeConfig = Field(..., description="Claude Code configuration")
    templates: TemplatesConfig = Field(default_factory=TemplatesConfig, description="Template paths")
    bootstrap: BootstrapConfig = Field(default_factory=BootstrapConfig, description="Bootstrap options")

    class Config:
        """Pydantic model configuration."""
        extra = "forbid"  # Raise error on unknown fields


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_frameworks_for_language(language: Language) -> List[Framework]:
    """Get available frameworks for a given language."""
    mapping = {
        Language.PYTHON: [Framework.FASTAPI, Framework.DJANGO, Framework.FLASK, Framework.NONE],
        Language.TYPESCRIPT: [Framework.NEXT, Framework.NEST, Framework.EXPRESS, Framework.REACT, Framework.NONE],
        Language.JAVASCRIPT: [Framework.NEXT, Framework.EXPRESS, Framework.REACT, Framework.VUE, Framework.NONE],
        Language.GO: [Framework.GIN, Framework.ECHO, Framework.NONE],
        Language.RUST: [Framework.NONE],
        Language.JAVA: [Framework.NONE],
    }
    return mapping.get(language, [Framework.NONE])


def get_package_managers_for_language(language: Language) -> List[PackageManager]:
    """Get available package managers for a given language."""
    mapping = {
        Language.PYTHON: [PackageManager.UV, PackageManager.POETRY, PackageManager.PIP],
        Language.TYPESCRIPT: [PackageManager.PNPM, PackageManager.NPM, PackageManager.BUN, PackageManager.YARN],
        Language.JAVASCRIPT: [PackageManager.PNPM, PackageManager.NPM, PackageManager.BUN, PackageManager.YARN],
        Language.GO: [PackageManager.GO],
        Language.RUST: [PackageManager.CARGO],
        Language.JAVA: [PackageManager.NPM],  # For build tools
    }
    return mapping.get(language, [PackageManager.NPM])


def get_default_commands(language: Language, package_manager: PackageManager) -> Dict[str, str]:
    """Get smart default commands for a language/package manager combination."""
    defaults = {
        (Language.PYTHON, PackageManager.UV): {
            "start": "uv run python -m app",
            "test": "uv run pytest",
            "lint": "uv run ruff check .",
            "typecheck": "uv run mypy .",
            "format": "uv run ruff format .",
            "build": "uv run python -m compileall .",
        },
        (Language.PYTHON, PackageManager.POETRY): {
            "start": "poetry run python -m app",
            "test": "poetry run pytest",
            "lint": "poetry run ruff check .",
            "typecheck": "poetry run mypy .",
            "format": "poetry run ruff format .",
            "build": "poetry build",
        },
        (Language.TYPESCRIPT, PackageManager.PNPM): {
            "start": "pnpm dev",
            "test": "pnpm test",
            "lint": "pnpm lint",
            "typecheck": "pnpm typecheck",
            "format": "pnpm format",
            "build": "pnpm build",
        },
        (Language.TYPESCRIPT, PackageManager.NPM): {
            "start": "npm run dev",
            "test": "npm test",
            "lint": "npm run lint",
            "typecheck": "npm run typecheck",
            "format": "npm run format",
            "build": "npm run build",
        },
        (Language.GO, PackageManager.GO): {
            "start": "go run .",
            "test": "go test ./...",
            "lint": "golangci-lint run",
            "typecheck": "go vet ./...",
            "format": "go fmt ./...",
            "build": "go build -o bin/app .",
        },
    }
    return defaults.get((language, package_manager), {
        "start": "echo 'Configure start command'",
        "test": "echo 'Configure test command'",
    })
```

## Criterios de Aceptacion
1. [ ] Archivo `models.py` creado con todos los modelos
2. [ ] Todos los enums tienen valores string validos
3. [ ] Todos los modelos tienen Field() con description
4. [ ] Funciones helper implementadas
5. [ ] Imports correctos, sin errores de sintaxis

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run python -c "from tac_bootstrap.domain.models import TACConfig; print('OK')"
uv run python -c "
from tac_bootstrap.domain.models import *
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)
print(config.model_dump_json(indent=2))
"
```

## NO hacer
- No crear archivos de test aun
- No implementar logica de scaffold
```

---

### TAREA 2.2: Crear modelos de plan de scaffolding

```markdown
# Prompt para Agente

## Contexto
El ScaffoldService necesita construir un "plan" de operaciones antes de ejecutarlas.
Este plan contiene listas de directorios a crear y archivos a generar/modificar.
Esto permite hacer dry-run, mostrar preview, y mantener idempotencia.

## Objetivo
Crear modelos Pydantic que representen el plan de scaffolding con operaciones
de archivos y directorios.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py`

## Contenido Completo

```python
"""Scaffolding plan models.

These models represent the plan of operations to execute when scaffolding
a project. The plan is built first, then can be previewed or executed.
"""
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class FileAction(str, Enum):
    """Type of file operation to perform."""
    CREATE = "create"    # Create new file (skip if exists)
    OVERWRITE = "overwrite"  # Create or overwrite existing
    PATCH = "patch"      # Append to existing file
    SKIP = "skip"        # Skip this file


class FileOperation(BaseModel):
    """Single file operation in the scaffold plan.

    Represents one file to be created, modified, or skipped.
    """
    path: str = Field(..., description="Relative path from project root")
    action: FileAction = Field(..., description="Type of operation")
    template: Optional[str] = Field(None, description="Jinja2 template name to render")
    content: Optional[str] = Field(None, description="Static content (if no template)")
    reason: Optional[str] = Field(None, description="Why this file is needed")
    executable: bool = Field(False, description="Make file executable after creation")

    def __str__(self) -> str:
        return f"[{self.action.value}] {self.path}"


class DirectoryOperation(BaseModel):
    """Directory creation operation.

    Represents a directory to be created.
    """
    path: str = Field(..., description="Relative path from project root")
    reason: str = Field("", description="Purpose of this directory")

    def __str__(self) -> str:
        return f"[mkdir] {self.path}/"


class ScaffoldPlan(BaseModel):
    """Complete scaffold plan for generation.

    Contains all directories and files to be created/modified.
    The plan is built first, allowing preview and validation before execution.

    Example:
        ```python
        plan = scaffold_service.build_plan(config)

        # Preview what will be created
        for dir_op in plan.directories:
            print(f"Will create: {dir_op.path}/")

        for file_op in plan.get_files_to_create():
            print(f"Will create: {file_op.path}")

        # Execute the plan
        scaffold_service.apply_plan(plan, output_dir)
        ```
    """
    directories: List[DirectoryOperation] = Field(default_factory=list)
    files: List[FileOperation] = Field(default_factory=list)

    def get_files_to_create(self) -> List[FileOperation]:
        """Get files that will be created (new files only)."""
        return [f for f in self.files if f.action == FileAction.CREATE]

    def get_files_to_overwrite(self) -> List[FileOperation]:
        """Get files that will be overwritten."""
        return [f for f in self.files if f.action == FileAction.OVERWRITE]

    def get_files_to_patch(self) -> List[FileOperation]:
        """Get files that will be patched (appended to)."""
        return [f for f in self.files if f.action == FileAction.PATCH]

    def get_files_skipped(self) -> List[FileOperation]:
        """Get files that will be skipped."""
        return [f for f in self.files if f.action == FileAction.SKIP]

    def get_executable_files(self) -> List[FileOperation]:
        """Get files that need to be made executable."""
        return [f for f in self.files if f.executable]

    @property
    def total_directories(self) -> int:
        """Total number of directories to create."""
        return len(self.directories)

    @property
    def total_files(self) -> int:
        """Total number of file operations."""
        return len(self.files)

    @property
    def summary(self) -> str:
        """Get a summary of the plan."""
        creates = len(self.get_files_to_create())
        patches = len(self.get_files_to_patch())
        skips = len(self.get_files_skipped())
        return (
            f"Plan: {self.total_directories} directories, "
            f"{creates} files to create, {patches} to patch, {skips} skipped"
        )

    def add_directory(self, path: str, reason: str = "") -> "ScaffoldPlan":
        """Add a directory to the plan (fluent interface)."""
        self.directories.append(DirectoryOperation(path=path, reason=reason))
        return self

    def add_file(
        self,
        path: str,
        action: FileAction = FileAction.CREATE,
        template: Optional[str] = None,
        content: Optional[str] = None,
        reason: Optional[str] = None,
        executable: bool = False,
    ) -> "ScaffoldPlan":
        """Add a file operation to the plan (fluent interface)."""
        self.files.append(FileOperation(
            path=path,
            action=action,
            template=template,
            content=content,
            reason=reason,
            executable=executable,
        ))
        return self
```

## Criterios de Aceptacion
1. [ ] Archivo `plan.py` creado
2. [ ] FileAction enum con todas las acciones
3. [ ] Metodos helper en ScaffoldPlan funcionan
4. [ ] Fluent interface permite encadenar add_directory/add_file

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run python -c "
from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction

plan = ScaffoldPlan()
plan.add_directory('.claude/commands', 'Claude Code commands')
plan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2')
plan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True)

print(plan.summary)
for d in plan.directories:
    print(d)
for f in plan.files:
    print(f)
"
```

## NO hacer
- No implementar la logica de ejecucion del plan (eso va en scaffold_service)
```

---

## FASE 3: Sistema de Templates (20-40%)

---

### TAREA 3.1: Crear infraestructura de templates Jinja2

```markdown
# Prompt para Agente

## Contexto
TAC Bootstrap genera archivos a partir de templates Jinja2. Necesitamos una clase
TemplateRepository que maneje la carga y renderizado de templates.

Los templates estaran en `tac_bootstrap/templates/` y se renderizaran con un contexto
que contiene el TACConfig completo.

## Objetivo
Crear la clase TemplateRepository que:
1. Carga templates desde el directorio de templates del paquete
2. Renderiza templates con contexto
3. Lista templates disponibles por categoria
4. Maneja errores de template no encontrado

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`

## Contenido Completo

```python
"""Template repository for loading and rendering Jinja2 templates.

This module provides the infrastructure for loading templates from the
package's templates directory and rendering them with configuration context.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape


class TemplateNotFoundError(Exception):
    """Raised when a template cannot be found."""
    pass


class TemplateRenderError(Exception):
    """Raised when a template fails to render."""
    pass


class TemplateRepository:
    """Repository for loading and rendering Jinja2 templates.

    Templates are loaded from the package's templates directory by default.
    The repository provides methods for rendering templates with context
    and listing available templates.

    Example:
        ```python
        repo = TemplateRepository()

        # Render a template
        content = repo.render("claude/settings.json.j2", {"config": tac_config})

        # List available templates
        templates = repo.list_templates("claude/commands")
        ```
    """

    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize the template repository.

        Args:
            template_dir: Custom template directory. If None, uses package default.
        """
        if template_dir is None:
            # Default to package templates directory
            template_dir = Path(__file__).parent.parent / "templates"

        self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            # Create directory if it doesn't exist (for development)
            self.template_dir.mkdir(parents=True, exist_ok=True)

        # Configure Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,      # Remove first newline after block tag
            lstrip_blocks=True,    # Strip leading whitespace from block tags
            keep_trailing_newline=True,  # Preserve trailing newline in templates
        )

        # Add custom filters
        self._register_filters()

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters."""

        def to_snake_case(value: str) -> str:
            """Convert string to snake_case."""
            import re
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        def to_kebab_case(value: str) -> str:
            """Convert string to kebab-case."""
            return to_snake_case(value).replace('_', '-')

        def to_pascal_case(value: str) -> str:
            """Convert string to PascalCase."""
            return ''.join(word.capitalize() for word in value.replace('-', '_').split('_'))

        self.env.filters['snake_case'] = to_snake_case
        self.env.filters['kebab_case'] = to_kebab_case
        self.env.filters['pascal_case'] = to_pascal_case

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context.

        Args:
            template_name: Name/path of the template file (e.g., "claude/settings.json.j2")
            context: Dictionary of variables to pass to the template

        Returns:
            Rendered template content as string

        Raises:
            TemplateNotFoundError: If template doesn't exist
            TemplateRenderError: If template fails to render
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound:
            raise TemplateNotFoundError(
                f"Template not found: {template_name}\n"
                f"Searched in: {self.template_dir}"
            )
        except Exception as e:
            raise TemplateRenderError(
                f"Failed to render template {template_name}: {e}"
            )

    def render_string(self, template_str: str, context: Dict[str, Any]) -> str:
        """Render a template string with the given context.

        Useful for inline templates or dynamic template generation.

        Args:
            template_str: Jinja2 template as a string
            context: Dictionary of variables to pass to the template

        Returns:
            Rendered content as string
        """
        try:
            template = self.env.from_string(template_str)
            return template.render(**context)
        except Exception as e:
            raise TemplateRenderError(f"Failed to render template string: {e}")

    def template_exists(self, template_name: str) -> bool:
        """Check if a template exists.

        Args:
            template_name: Name/path of the template file

        Returns:
            True if template exists, False otherwise
        """
        template_path = self.template_dir / template_name
        return template_path.exists()

    def list_templates(self, category: Optional[str] = None) -> List[str]:
        """List available templates, optionally filtered by category.

        Args:
            category: Optional subdirectory to filter by (e.g., "claude/commands")

        Returns:
            List of template names relative to template_dir
        """
        templates = []

        search_dir = self.template_dir
        if category:
            search_dir = self.template_dir / category

        if not search_dir.exists():
            return []

        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith(('.j2', '.jinja2')):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(self.template_dir)
                    templates.append(str(rel_path))

        return sorted(templates)

    def get_template_content(self, template_name: str) -> str:
        """Get raw template content without rendering.

        Useful for debugging or displaying templates.

        Args:
            template_name: Name/path of the template file

        Returns:
            Raw template content
        """
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise TemplateNotFoundError(f"Template not found: {template_name}")
        return template_path.read_text()
```

## Criterios de Aceptacion
1. [ ] Archivo `template_repo.py` creado
2. [ ] TemplateRepository se instancia sin errores
3. [ ] Metodos render(), list_templates(), template_exists() funcionan
4. [ ] Custom filters registrados (snake_case, kebab_case, pascal_case)
5. [ ] Errores custom definidos (TemplateNotFoundError, TemplateRenderError)

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

repo = TemplateRepository()
print(f'Template dir: {repo.template_dir}')
print(f'Templates found: {repo.list_templates()}')

# Test render_string
result = repo.render_string('Hello {{ name }}!', {'name': 'World'})
print(f'Render test: {result}')

# Test filters
result = repo.render_string('{{ name | snake_case }}', {'name': 'MyProjectName'})
print(f'Snake case: {result}')
"
```

## NO hacer
- No crear templates aun (eso es la siguiente tarea)
- No implementar la logica de scaffold
```

---

### TAREA 3.2: Crear templates para .claude/ (settings y comandos base)

```markdown
# Prompt para Agente

## Contexto
TAC Bootstrap genera la carpeta `.claude/` con:
- `settings.json` - permisos y hooks para Claude Code
- `commands/*.md` - comandos slash reutilizables

Estos archivos deben ser templates Jinja2 parametrizables que se renderizan
con el TACConfig del usuario.

## Objetivo
Crear los templates Jinja2 para `.claude/settings.json` y los comandos base:
prime, start, build, test, feature, bug, chore, patch, implement, commit,
pull_request, review, document, health_check.

## Directorio Base
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/`

## Archivos a Crear

### 1. `settings.json.j2`
Template para `.claude/settings.json`:

```jinja2
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash({{ config.project.package_manager.value }}:*)",
      "Bash(find:*)",
      "Bash(mv:*)",
      "Bash(grep:*)",
      "Bash(ls:*)",
      "Bash(cp:*)",
      "Write",
      "Bash(chmod:*)",
      "Bash(touch:*)",
      "Bash(git:*)"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(rm -rf:*)",
      "Bash(rm -r /:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/stop.py || true"
          }
        ]
      }
    ]
  }
}
```

### 2. `commands/prime.md.j2`
```jinja2
# Prime

Prepare the agent with project context.

## Variables
- $ARGUMENTS: Optional focus area

## Instructions

1. Read and understand the project structure:
   - Project: {{ config.project.name }}
   - Language: {{ config.project.language.value }}
   - Framework: {{ config.project.framework.value if config.project.framework else 'none' }}
   - Architecture: {{ config.project.architecture.value }}

2. Key directories:
   - App code: `{{ config.paths.app_root }}/`
   - Specs: `{{ config.paths.specs_dir }}/`
   - ADWs: `{{ config.paths.adws_dir }}/`
   - Scripts: `{{ config.paths.scripts_dir }}/`

3. Available commands:
   - Start: `{{ config.commands.start }}`
   - Test: `{{ config.commands.test }}`
{% if config.commands.lint %}
   - Lint: `{{ config.commands.lint }}`
{% endif %}
{% if config.commands.build %}
   - Build: `{{ config.commands.build }}`
{% endif %}

4. Rules:
   - Never modify files in: {{ config.agentic.safety.forbidden_paths | join(', ') }}
   - Always run tests before completing work
   - Follow {{ config.project.architecture.value }} architecture patterns

## Report
Confirm you understand the project context and are ready to work.
```

### 3. `commands/start.md.j2`
```jinja2
# Start

Start the application.

## Instructions

1. Ensure dependencies are installed
2. Run the start command:
   ```bash
   {{ config.commands.start }}
   ```
3. Verify the application is running
4. Report the URL/port if applicable

## Report
- Status: running/failed
- URL: (if applicable)
- Notes: any issues encountered
```

### 4. `commands/test.md.j2`
```jinja2
# Test

Run the test suite.

## Variables
- $ARGUMENTS: Optional test path or pattern

## Instructions

1. Run tests:
   ```bash
   {{ config.commands.test }} $ARGUMENTS
   ```

2. If tests fail:
   - Analyze the failure output
   - Identify the root cause
   - Do NOT attempt to fix unless explicitly asked

3. Report results

## Report
- Total tests: X
- Passed: X
- Failed: X
- Failures: (list if any)
```

### 5. `commands/feature.md.j2`
```jinja2
# Feature Planning

Plan a new feature implementation.

## Variables
- $ARGUMENTS: Feature description or issue reference

## Instructions

1. **Understand the Request**
   - Parse the feature description from $ARGUMENTS
   - Identify acceptance criteria
   - List any ambiguities to clarify

2. **Research the Codebase**
   - Find related existing code
   - Identify files that need modification
   - Note any patterns to follow

3. **Design the Solution**
   - Break down into discrete tasks
   - Identify dependencies between tasks
   - Consider edge cases and error handling

4. **Create the Plan**
   Write a plan file to `{{ config.paths.specs_dir }}/` with:
   - Summary of the feature
   - List of files to modify/create
   - Step-by-step implementation tasks
   - Test cases to add
   - Definition of done

## Plan Format
```markdown
# Feature: [Name]

## Summary
[1-2 sentence description]

## Files to Modify
- `path/to/file.py` - [what changes]
- `path/to/new_file.py` - [create new]

## Implementation Steps
1. [ ] Step one
2. [ ] Step two
...

## Test Cases
- [ ] Test case 1
- [ ] Test case 2

## Definition of Done
- [ ] All tests pass
- [ ] Code follows {{ config.project.architecture.value }} patterns
- [ ] No linting errors
```

## Report
- Plan file created: `{{ config.paths.specs_dir }}/feature-[name].md`
- Ready for implementation: yes/no
- Questions/blockers: (if any)
```

### 6. `commands/bug.md.j2`
```jinja2
# Bug Planning

Plan a bug fix.

## Variables
- $ARGUMENTS: Bug description or issue reference

## Instructions

1. **Understand the Bug**
   - Parse the bug description from $ARGUMENTS
   - Identify expected vs actual behavior
   - Determine reproduction steps if not provided

2. **Investigate**
   - Find the relevant code
   - Identify the root cause
   - Check for related issues

3. **Plan the Fix**
   - Determine the minimal fix
   - Identify any side effects
   - Plan regression tests

4. **Create the Plan**
   Write a plan file to `{{ config.paths.specs_dir }}/`

## Plan Format
```markdown
# Bug: [Title]

## Description
[What is broken]

## Root Cause
[Why it's broken]

## Fix
[How to fix it]

## Files to Modify
- `path/to/file.py` - [what changes]

## Test Cases
- [ ] Test that reproduces the bug
- [ ] Test for regression

## Definition of Done
- [ ] Bug is fixed
- [ ] Tests pass
- [ ] No regression introduced
```

## Report
- Plan file created: `{{ config.paths.specs_dir }}/bug-[name].md`
- Root cause identified: yes/no
- Ready for implementation: yes/no
```

### 7. `commands/chore.md.j2`
```jinja2
# Chore Planning

Plan a maintenance task (refactoring, dependencies, config, etc).

## Variables
- $ARGUMENTS: Chore description

## Instructions

1. **Understand the Task**
   - Parse the chore description from $ARGUMENTS
   - Identify scope and boundaries
   - Determine success criteria

2. **Plan the Work**
   - List all changes needed
   - Identify risks or breaking changes
   - Plan verification steps

3. **Create the Plan**
   Write a plan file to `{{ config.paths.specs_dir }}/`

## Plan Format
```markdown
# Chore: [Title]

## Description
[What needs to be done]

## Changes
- [ ] Change 1
- [ ] Change 2

## Files to Modify
- `path/to/file` - [what changes]

## Verification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] No breaking changes

## Definition of Done
- [ ] All changes complete
- [ ] Verified working
```

## Report
- Plan file created: `{{ config.paths.specs_dir }}/chore-[name].md`
```

### 8. `commands/implement.md.j2`
```jinja2
# Implement

Execute a plan file.

## Variables
- $1: Path to the plan file (e.g., `{{ config.paths.specs_dir }}/feature-auth.md`)

## Instructions

1. **Read the Plan**
   - Load and parse the plan file from $1
   - Understand all tasks and their order
   - Note the definition of done

2. **Execute Tasks**
   For each task in the plan:
   - Mark task as in-progress
   - Implement the change
   - Verify it works
   - Mark task as complete

3. **Validate**
   - Run tests: `{{ config.commands.test }}`
{% if config.commands.lint %}
   - Run linter: `{{ config.commands.lint }}`
{% endif %}
{% if config.commands.typecheck %}
   - Run typecheck: `{{ config.commands.typecheck }}`
{% endif %}

4. **Report Results**
   Update the plan file with completion status

## Report
- Plan: $1
- Tasks completed: X/Y
- Tests: pass/fail
- Ready for review: yes/no
```

### 9. `commands/commit.md.j2`
```jinja2
# Commit

Create a git commit with proper message format.

## Variables
- $ARGUMENTS: Optional commit message override

## Instructions

1. **Check Status**
   ```bash
   git status
   git diff --staged
   ```

2. **Stage Changes** (if needed)
   - Stage only relevant files
   - Do NOT stage: {{ config.agentic.safety.forbidden_paths | join(', ') }}

3. **Create Commit**
   - Use conventional commit format: `type(scope): description`
   - Types: feat, fix, chore, docs, refactor, test
   - Keep description under 72 characters

4. **Commit Message Format**
   ```
   type(scope): short description

   - Detail 1
   - Detail 2

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

## Report
- Commit created: yes/no
- Hash: [commit hash]
- Message: [commit message]
```

### 10. `commands/review.md.j2`
```jinja2
# Review

Review implementation against the plan/spec.

## Variables
- $1: Path to the plan/spec file

## Instructions

1. **Load the Spec**
   Read the plan file from $1

2. **Verify Completion**
   For each item in the plan:
   - Check if implemented correctly
   - Verify tests exist
   - Note any deviations

3. **Run Validation**
   - Tests: `{{ config.commands.test }}`
{% if config.commands.lint %}
   - Lint: `{{ config.commands.lint }}`
{% endif %}
{% if config.commands.build %}
   - Build: `{{ config.commands.build }}`
{% endif %}

4. **Check Quality**
   - Code follows {{ config.project.architecture.value }} patterns
   - No hardcoded values
   - Error handling present
   - No security issues

5. **Generate Report**

## Report Format
```markdown
# Review: [Plan Name]

## Checklist
- [ ] All tasks from plan completed
- [ ] Tests pass
- [ ] Lint passes
- [ ] Build succeeds
- [ ] Code quality acceptable

## Issues Found
- (list any issues)

## Verdict
- APPROVED / NEEDS_CHANGES
```
```

### 11. `commands/document.md.j2`
```jinja2
# Document

Generate documentation for recent changes.

## Variables
- $ARGUMENTS: Feature/component to document

## Instructions

1. **Identify What to Document**
   - Parse $ARGUMENTS for the target
   - Find related code and specs

2. **Generate Documentation**
   Create/update docs in `app_docs/`:
   - Overview of the feature
   - Usage examples
   - API reference (if applicable)
   - Configuration options

3. **Documentation Format**
   ```markdown
   # [Feature Name]

   ## Overview
   [What it does]

   ## Usage
   [How to use it]

   ## Examples
   [Code examples]

   ## Configuration
   [Any config options]
   ```

## Report
- Documentation created: `app_docs/[name].md`
```

### 12. `commands/health_check.md.j2`
```jinja2
# Health Check

Validate the project setup and agentic layer.

## Instructions

1. **Check Structure**
   Verify these directories exist:
   - `.claude/commands/`
   - `{{ config.paths.adws_dir }}/`
   - `{{ config.paths.specs_dir }}/`
   - `{{ config.paths.scripts_dir }}/`

2. **Check Configuration**
   - `.claude/settings.json` is valid JSON
   - `config.yml` exists and is valid

3. **Check Commands**
   Verify these work:
   - Start: `{{ config.commands.start }}`
   - Test: `{{ config.commands.test }}`

4. **Check Git**
   - Is a git repository
   - Has remote configured (optional)

## Report Format
```
Health Check Results
====================
Structure:    [PASS/FAIL]
Config:       [PASS/FAIL]
Commands:     [PASS/FAIL]
Git:          [PASS/FAIL]

Issues:
- (list any issues found)
```
```

## Criterios de Aceptacion
1. [ ] Directorio `templates/claude/` creado
2. [ ] `settings.json.j2` con permisos y hooks parametrizados
3. [ ] 12 comandos base creados como templates
4. [ ] Todos los templates usan variables de `config`
5. [ ] Sintaxis Jinja2 valida en todos los archivos

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
ls -la tac_bootstrap/templates/claude/
ls -la tac_bootstrap/templates/claude/commands/

# Test rendering
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()

# Create test config
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest', lint='uv run ruff check .'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

# Render settings.json
result = repo.render('claude/settings.json.j2', {'config': config})
print('=== settings.json ===')
print(result[:500])

# Render a command
result = repo.render('claude/commands/prime.md.j2', {'config': config})
print('=== prime.md ===')
print(result[:500])
"
```

## NO hacer
- No crear hooks aun (siguiente tarea)
- No crear templates de adws aun
```

---

### TAREA 3.3: Crear templates para .claude/hooks/

```markdown
# Prompt para Agente

## Contexto
Los hooks de Claude Code son scripts Python que se ejecutan automaticamente
en diferentes eventos (PreToolUse, PostToolUse, Stop, etc).

Necesitamos templates para estos hooks que:
- Validen comandos peligrosos antes de ejecutar
- Registren logs de operaciones
- Sean parametrizables segun config.yml

## Objetivo
Crear templates Jinja2 para los hooks de `.claude/hooks/`:
- pre_tool_use.py - validacion antes de ejecutar herramientas
- post_tool_use.py - logging despues de ejecutar
- stop.py - limpieza al terminar sesion
- utils/constants.py - configuracion compartida

## Directorio Base
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/`

## Archivos a Crear

### 1. `pre_tool_use.py.j2`
```jinja2
#!/usr/bin/env python3
"""Pre-tool-use hook for Claude Code.

This hook runs before any tool is executed. It validates commands
and can block dangerous operations.

Generated by TAC Bootstrap for: {{ config.project.name }}
"""
import json
import os
import sys
from pathlib import Path

# Forbidden patterns - block these commands
FORBIDDEN_PATTERNS = [
{% for path in config.agentic.safety.forbidden_paths %}
    "{{ path }}",
{% endfor %}
    "rm -rf /",
    "rm -rf ~",
    "> /dev/sda",
    ":(){ :|:& };:",  # Fork bomb
]

# Forbidden in file paths
FORBIDDEN_PATHS = [
{% for path in config.agentic.safety.forbidden_paths %}
    "{{ path }}",
{% endfor %}
]


def get_hook_input() -> dict:
    """Read hook input from environment."""
    hook_input = os.environ.get("CLAUDE_HOOK_INPUT", "{}")
    try:
        return json.loads(hook_input)
    except json.JSONDecodeError:
        return {}


def is_dangerous_command(command: str) -> tuple[bool, str]:
    """Check if a command is dangerous.

    Returns:
        Tuple of (is_dangerous, reason)
    """
    command_lower = command.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in command_lower:
            return True, f"Command contains forbidden pattern: {pattern}"

    return False, ""


def is_forbidden_path(path: str) -> tuple[bool, str]:
    """Check if a path is forbidden.

    Returns:
        Tuple of (is_forbidden, reason)
    """
    path_lower = path.lower()

    for forbidden in FORBIDDEN_PATHS:
        if forbidden.lower() in path_lower:
            return True, f"Path contains forbidden pattern: {forbidden}"

    return False, ""


def validate_tool_use(hook_input: dict) -> tuple[bool, str]:
    """Validate the tool use.

    Returns:
        Tuple of (is_valid, reason)
    """
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Check Bash commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        is_dangerous, reason = is_dangerous_command(command)
        if is_dangerous:
            return False, reason

    # Check file operations
    if tool_name in ("Write", "Edit", "Read"):
        file_path = tool_input.get("file_path", "")
        is_forbidden, reason = is_forbidden_path(file_path)
        if is_forbidden:
            return False, reason

    return True, ""


def main():
    """Main entry point."""
    hook_input = get_hook_input()

    is_valid, reason = validate_tool_use(hook_input)

    if not is_valid:
        # Output to stderr and exit with error
        print(json.dumps({
            "decision": "block",
            "reason": reason
        }))
        sys.exit(1)

    # Allow the operation
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
```

### 2. `post_tool_use.py.j2`
```jinja2
#!/usr/bin/env python3
"""Post-tool-use hook for Claude Code.

This hook runs after any tool is executed. It logs operations
for debugging and auditing.

Generated by TAC Bootstrap for: {{ config.project.name }}
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Log directory
LOG_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "{{ config.paths.logs_dir }}"


def get_hook_input() -> dict:
    """Read hook input from environment."""
    hook_input = os.environ.get("CLAUDE_HOOK_INPUT", "{}")
    try:
        return json.loads(hook_input)
    except json.JSONDecodeError:
        return {}


def get_session_id() -> str:
    """Get current session ID."""
    return os.environ.get("CLAUDE_SESSION_ID", "unknown")


def ensure_log_dir() -> Path:
    """Ensure log directory exists."""
    session_dir = LOG_DIR / get_session_id()
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def log_tool_use(hook_input: dict) -> None:
    """Log the tool use to file."""
    session_dir = ensure_log_dir()
    log_file = session_dir / "post_tool_use.json"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "tool_name": hook_input.get("tool_name", "unknown"),
        "tool_input": hook_input.get("tool_input", {}),
        "tool_output": hook_input.get("tool_output", {})[:500] if hook_input.get("tool_output") else None,
    }

    # Append to log file
    entries = []
    if log_file.exists():
        try:
            entries = json.loads(log_file.read_text())
        except:
            entries = []

    entries.append(entry)
    log_file.write_text(json.dumps(entries, indent=2, default=str))


def main():
    """Main entry point."""
    hook_input = get_hook_input()

    try:
        log_tool_use(hook_input)
    except Exception as e:
        # Don't fail on logging errors
        print(f"Warning: Failed to log tool use: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

### 3. `stop.py.j2`
```jinja2
#!/usr/bin/env python3
"""Stop hook for Claude Code.

This hook runs when the session ends. It can perform cleanup
and generate session summaries.

Generated by TAC Bootstrap for: {{ config.project.name }}
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / "{{ config.paths.logs_dir }}"


def get_session_id() -> str:
    """Get current session ID."""
    return os.environ.get("CLAUDE_SESSION_ID", "unknown")


def generate_summary() -> None:
    """Generate session summary."""
    session_dir = LOG_DIR / get_session_id()

    if not session_dir.exists():
        return

    # Count tool uses
    post_log = session_dir / "post_tool_use.json"
    tool_count = 0
    if post_log.exists():
        try:
            entries = json.loads(post_log.read_text())
            tool_count = len(entries)
        except:
            pass

    # Write summary
    summary = {
        "session_id": get_session_id(),
        "ended_at": datetime.now().isoformat(),
        "tool_uses": tool_count,
    }

    summary_file = session_dir / "summary.json"
    summary_file.write_text(json.dumps(summary, indent=2))


def main():
    """Main entry point."""
    try:
        generate_summary()
    except Exception as e:
        print(f"Warning: Failed to generate summary: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

### 4. `utils/__init__.py.j2`
```jinja2
"""Hook utilities for {{ config.project.name }}."""
```

### 5. `utils/constants.py.j2`
```jinja2
"""Constants for Claude Code hooks.

Generated by TAC Bootstrap for: {{ config.project.name }}
"""
from pathlib import Path

# Project configuration
PROJECT_NAME = "{{ config.project.name }}"
LANGUAGE = "{{ config.project.language.value }}"
PACKAGE_MANAGER = "{{ config.project.package_manager.value }}"

# Paths
LOG_DIR = Path("{{ config.paths.logs_dir }}")
SPECS_DIR = Path("{{ config.paths.specs_dir }}")
ADWS_DIR = Path("{{ config.paths.adws_dir }}")

# Safety
FORBIDDEN_PATHS = [
{% for path in config.agentic.safety.forbidden_paths %}
    "{{ path }}",
{% endfor %}
]

ALLOWED_PATHS = [
{% for path in config.agentic.safety.allowed_paths %}
    "{{ path }}",
{% endfor %}
]
```

## Criterios de Aceptacion
1. [ ] Directorio `templates/claude/hooks/` creado
2. [ ] 3 hooks principales creados (pre_tool_use, post_tool_use, stop)
3. [ ] Directorio utils con __init__ y constants
4. [ ] Todos usan variables de config correctamente
5. [ ] Scripts son ejecutables (shebang correcto)

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
ls -la tac_bootstrap/templates/claude/hooks/
ls -la tac_bootstrap/templates/claude/hooks/utils/

# Test rendering
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

result = repo.render('claude/hooks/pre_tool_use.py.j2', {'config': config})
print('=== pre_tool_use.py ===')
print(result[:800])
"
```
```

---

### TAREA 3.4: Crear templates para adws/ (modulos y workflows)

```markdown
# Prompt para Agente

## Contexto
Los ADWs (AI Developer Workflows) son el corazon de la automatizacion en TAC.
Son scripts Python que orquestan agentes y comandos deterministicos.

La estructura de adws/ incluye:
- adw_modules/ - modulos compartidos (agent, state, git_ops, etc)
- Workflows individuales (adw_sdlc_iso.py, adw_patch_iso.py, etc)
- adw_triggers/ - triggers para ejecucion automatica

## Objetivo
Crear templates Jinja2 para la estructura completa de adws/:
1. README.md explicativo
2. Modulos core en adw_modules/
3. Workflows principales
4. Triggers basicos

## Directorio Base
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/`

## Archivos a Crear

### 1. `README.md.j2`
```jinja2
# AI Developer Workflows (ADWs)

Este directorio contiene los workflows automatizados para {{ config.project.name }}.

## Estructura

```
{{ config.paths.adws_dir }}/
├── adw_modules/          # Modulos compartidos
│   ├── agent.py          # Wrapper de Claude Code CLI
│   ├── state.py          # Persistencia de estado
│   ├── git_ops.py        # Operaciones git
│   └── workflow_ops.py   # Orquestacion
├── adw_sdlc_iso.py       # Workflow SDLC completo
├── adw_patch_iso.py      # Workflow de patch rapido
└── adw_triggers/         # Triggers automaticos
    └── trigger_cron.py   # Polling de tareas
```

## Workflows Disponibles

### SDLC Iso (Isolated)
Workflow completo: Plan → Build → Test → Review → Ship

```bash
{{ config.project.package_manager.value }} run python {{ config.paths.adws_dir }}/adw_sdlc_iso.py --issue 123
```

### Patch Iso
Workflow rapido para fixes: Build → Test → Ship

```bash
{{ config.project.package_manager.value }} run python {{ config.paths.adws_dir }}/adw_patch_iso.py --issue 456
```

## Conceptos Clave

### Aislamiento (Iso)
Cada workflow corre en su propio git worktree para evitar conflictos.
Los worktrees se crean en `{{ config.paths.worktrees_dir }}/`.

### Estado Persistente
El estado de cada workflow se guarda en `agents/{adw_id}/adw_state.json`.

### Puertos
Cada worktree tiene puertos asignados para evitar conflictos:
- Backend: 9100-9114
- Frontend: 9200-9214
```

### 2. `adw_modules/__init__.py.j2`
```jinja2
"""ADW Modules for {{ config.project.name }}."""
from .agent import run_claude_command
from .state import ADWState
from .git_ops import GitOps
from .workflow_ops import WorkflowOps

__all__ = ["run_claude_command", "ADWState", "GitOps", "WorkflowOps"]
```

### 3. `adw_modules/agent.py.j2`
```jinja2
"""Claude Code agent wrapper.

Provides a clean interface for running Claude Code commands.
"""
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any


def run_claude_command(
    command: str,
    args: str = "",
    cwd: Optional[Path] = None,
    model: str = "{{ config.agentic.model_policy.default }}",
    capture_output: bool = True,
) -> Dict[str, Any]:
    """Run a Claude Code slash command.

    Args:
        command: The slash command to run (e.g., "implement", "test")
        args: Arguments to pass to the command
        cwd: Working directory (defaults to current)
        model: Model to use (sonnet/opus)
        capture_output: Whether to capture and return output

    Returns:
        Dict with 'success', 'output', and 'error' keys
    """
    full_command = f"/{command}"
    if args:
        full_command += f" {args}"

    cmd = [
        "claude",
        "--print",
        "--dangerously-skip-permissions",
        "--model", model,
        "-p", full_command,
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or Path.cwd(),
            capture_output=capture_output,
            text=True,
            timeout=3600,  # 1 hour timeout
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Command timed out after 1 hour",
            "returncode": -1,
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "returncode": -1,
        }


# Model selection based on command complexity
HEAVY_COMMANDS = ["implement", "feature", "bug", "review", "document"]

def get_model_for_command(command: str) -> str:
    """Get the appropriate model for a command."""
    if command in HEAVY_COMMANDS:
        return "{{ config.agentic.model_policy.heavy }}"
    return "{{ config.agentic.model_policy.default }}"
```

### 4. `adw_modules/state.py.j2`
```jinja2
"""ADW State management.

Handles persistence of workflow state across steps.
"""
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, List
from datetime import datetime


@dataclass
class ADWState:
    """State for an AI Developer Workflow run.

    Persisted to agents/{adw_id}/adw_state.json
    """
    adw_id: str
    issue_number: Optional[int] = None
    issue_class: Optional[str] = None  # feature, bug, chore
    branch_name: Optional[str] = None
    plan_file: Optional[str] = None
    worktree_path: Optional[str] = None
    backend_port: Optional[int] = None
    frontend_port: Optional[int] = None
    current_phase: str = "init"
    phases_completed: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    error: Optional[str] = None

    def save(self, base_dir: Path = Path("agents")) -> None:
        """Save state to disk."""
        state_dir = base_dir / self.adw_id
        state_dir.mkdir(parents=True, exist_ok=True)

        self.updated_at = datetime.now().isoformat()

        state_file = state_dir / "adw_state.json"
        state_file.write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls, adw_id: str, base_dir: Path = Path("agents")) -> Optional["ADWState"]:
        """Load state from disk."""
        state_file = base_dir / adw_id / "adw_state.json"

        if not state_file.exists():
            return None

        data = json.loads(state_file.read_text())
        return cls(**data)

    def mark_phase_complete(self, phase: str) -> None:
        """Mark a phase as completed."""
        if phase not in self.phases_completed:
            self.phases_completed.append(phase)
        self.current_phase = phase
        self.save()

    def set_error(self, error: str) -> None:
        """Set error state."""
        self.error = error
        self.save()
```

### 5. `adw_modules/git_ops.py.j2`
```jinja2
"""Git operations for ADWs."""
import subprocess
from pathlib import Path
from typing import Optional


class GitOps:
    """Git operations wrapper."""

    def __init__(self, cwd: Optional[Path] = None):
        self.cwd = cwd or Path.cwd()

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        """Run a git command."""
        return subprocess.run(
            ["git", *args],
            cwd=self.cwd,
            capture_output=True,
            text=True,
        )

    def create_branch(self, branch_name: str) -> bool:
        """Create and checkout a new branch."""
        result = self._run("checkout", "-b", branch_name)
        return result.returncode == 0

    def checkout(self, branch: str) -> bool:
        """Checkout a branch."""
        result = self._run("checkout", branch)
        return result.returncode == 0

    def add_all(self) -> bool:
        """Stage all changes."""
        result = self._run("add", "-A")
        return result.returncode == 0

    def commit(self, message: str) -> bool:
        """Create a commit."""
        result = self._run("commit", "-m", message)
        return result.returncode == 0

    def push(self, branch: str, set_upstream: bool = True) -> bool:
        """Push branch to remote."""
        args = ["push"]
        if set_upstream:
            args.extend(["-u", "origin", branch])
        else:
            args.append(branch)
        result = self._run(*args)
        return result.returncode == 0

    def create_worktree(self, path: Path, branch: str) -> bool:
        """Create a git worktree."""
        result = self._run("worktree", "add", str(path), "-b", branch)
        return result.returncode == 0

    def remove_worktree(self, path: Path) -> bool:
        """Remove a git worktree."""
        result = self._run("worktree", "remove", str(path), "--force")
        return result.returncode == 0

    def get_current_branch(self) -> str:
        """Get current branch name."""
        result = self._run("branch", "--show-current")
        return result.stdout.strip()
```

### 6. `adw_modules/workflow_ops.py.j2`
```jinja2
"""Workflow operations for ADWs."""
from pathlib import Path
from typing import Optional
from .agent import run_claude_command, get_model_for_command
from .state import ADWState


class WorkflowOps:
    """High-level workflow operations."""

    def __init__(self, state: ADWState, cwd: Optional[Path] = None):
        self.state = state
        self.cwd = cwd or Path.cwd()

    def plan(self, issue_description: str) -> bool:
        """Run planning phase."""
        # Determine issue class
        classify_result = run_claude_command(
            "classify_issue",
            issue_description,
            cwd=self.cwd,
        )

        if not classify_result["success"]:
            self.state.set_error(f"Classification failed: {classify_result['error']}")
            return False

        # Run appropriate planning command
        issue_class = self.state.issue_class or "chore"
        plan_result = run_claude_command(
            issue_class,  # feature, bug, or chore
            issue_description,
            cwd=self.cwd,
            model=get_model_for_command(issue_class),
        )

        if plan_result["success"]:
            self.state.mark_phase_complete("plan")

        return plan_result["success"]

    def build(self, plan_file: str) -> bool:
        """Run build/implementation phase."""
        result = run_claude_command(
            "implement",
            plan_file,
            cwd=self.cwd,
            model=get_model_for_command("implement"),
        )

        if result["success"]:
            self.state.mark_phase_complete("build")

        return result["success"]

    def test(self) -> bool:
        """Run test phase."""
        result = run_claude_command(
            "test",
            "",
            cwd=self.cwd,
        )

        if result["success"]:
            self.state.mark_phase_complete("test")

        return result["success"]

    def review(self, plan_file: str) -> bool:
        """Run review phase."""
        result = run_claude_command(
            "review",
            plan_file,
            cwd=self.cwd,
            model=get_model_for_command("review"),
        )

        if result["success"]:
            self.state.mark_phase_complete("review")

        return result["success"]

    def ship(self) -> bool:
        """Run ship phase (commit + PR)."""
        # Commit changes
        commit_result = run_claude_command("commit", "", cwd=self.cwd)
        if not commit_result["success"]:
            return False

        # Create PR
        pr_result = run_claude_command("pull_request", "", cwd=self.cwd)

        if pr_result["success"]:
            self.state.mark_phase_complete("ship")

        return pr_result["success"]
```

### 7. `adw_sdlc_iso.py.j2`
```jinja2
#!/usr/bin/env python3
"""SDLC Workflow (Isolated).

Complete software development lifecycle:
Plan → Build → Test → Review → Ship

Each run gets its own git worktree for isolation.
"""
import argparse
import sys
import uuid
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from adw_modules.state import ADWState
from adw_modules.git_ops import GitOps
from adw_modules.workflow_ops import WorkflowOps


def generate_adw_id() -> str:
    """Generate unique ADW ID."""
    return uuid.uuid4().hex[:8]


def main():
    parser = argparse.ArgumentParser(description="Run SDLC workflow")
    parser.add_argument("--issue", type=int, help="Issue number")
    parser.add_argument("--description", type=str, help="Issue description")
    parser.add_argument("--adw-id", type=str, help="Resume existing ADW")
    args = parser.parse_args()

    # Initialize or resume state
    if args.adw_id:
        state = ADWState.load(args.adw_id)
        if not state:
            print(f"Error: ADW {args.adw_id} not found")
            sys.exit(1)
    else:
        state = ADWState(
            adw_id=generate_adw_id(),
            issue_number=args.issue,
        )
        state.save()

    print(f"ADW ID: {state.adw_id}")

    # Setup worktree
    git = GitOps()
    worktree_path = Path("{{ config.paths.worktrees_dir }}") / state.adw_id
    branch_name = f"adw-{state.adw_id}"

    if not worktree_path.exists():
        print(f"Creating worktree: {worktree_path}")
        git.create_worktree(worktree_path, branch_name)
        state.worktree_path = str(worktree_path)
        state.branch_name = branch_name
        state.save()

    # Run workflow in worktree
    ops = WorkflowOps(state, cwd=worktree_path)

    description = args.description or f"Issue #{args.issue}"

    # Phase 1: Plan
    if "plan" not in state.phases_completed:
        print("Phase 1: Planning...")
        if not ops.plan(description):
            print("Planning failed")
            sys.exit(1)

    # Phase 2: Build
    if "build" not in state.phases_completed:
        print("Phase 2: Building...")
        plan_file = state.plan_file or f"{{ config.paths.specs_dir }}/issue-{args.issue}.md"
        if not ops.build(plan_file):
            print("Build failed")
            sys.exit(1)

    # Phase 3: Test
    if "test" not in state.phases_completed:
        print("Phase 3: Testing...")
        if not ops.test():
            print("Tests failed")
            sys.exit(1)

    # Phase 4: Review
    if "review" not in state.phases_completed:
        print("Phase 4: Reviewing...")
        plan_file = state.plan_file or f"{{ config.paths.specs_dir }}/issue-{args.issue}.md"
        if not ops.review(plan_file):
            print("Review failed")
            sys.exit(1)

    # Phase 5: Ship
    if "ship" not in state.phases_completed:
        print("Phase 5: Shipping...")
        if not ops.ship():
            print("Ship failed")
            sys.exit(1)

    print(f"SDLC workflow completed for ADW {state.adw_id}")


if __name__ == "__main__":
    main()
```

### 8. `adw_patch_iso.py.j2`
```jinja2
#!/usr/bin/env python3
"""Patch Workflow (Isolated).

Quick fix workflow: Build → Test → Ship
Skips planning phase for simple fixes.
"""
import argparse
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from adw_modules.state import ADWState
from adw_modules.git_ops import GitOps
from adw_modules.workflow_ops import WorkflowOps


def main():
    parser = argparse.ArgumentParser(description="Run patch workflow")
    parser.add_argument("--issue", type=int, required=True, help="Issue number")
    parser.add_argument("--fix", type=str, required=True, help="Fix description")
    args = parser.parse_args()

    state = ADWState(
        adw_id=uuid.uuid4().hex[:8],
        issue_number=args.issue,
        issue_class="patch",
    )
    state.save()

    print(f"Patch ADW ID: {state.adw_id}")

    # Setup worktree
    git = GitOps()
    worktree_path = Path("{{ config.paths.worktrees_dir }}") / state.adw_id
    branch_name = f"patch-{state.adw_id}"

    git.create_worktree(worktree_path, branch_name)
    state.worktree_path = str(worktree_path)
    state.branch_name = branch_name
    state.save()

    ops = WorkflowOps(state, cwd=worktree_path)

    # Direct implementation (no planning)
    print("Implementing patch...")
    from adw_modules.agent import run_claude_command
    result = run_claude_command("patch", args.fix, cwd=worktree_path)

    if not result["success"]:
        print("Patch failed")
        sys.exit(1)

    # Test
    print("Testing...")
    if not ops.test():
        print("Tests failed")
        sys.exit(1)

    # Ship
    print("Shipping...")
    if not ops.ship():
        print("Ship failed")
        sys.exit(1)

    print(f"Patch completed: {state.adw_id}")


if __name__ == "__main__":
    main()
```

### 9. `adw_triggers/__init__.py.j2`
```jinja2
"""ADW Triggers for {{ config.project.name }}."""
```

### 10. `adw_triggers/trigger_cron.py.j2`
```jinja2
#!/usr/bin/env python3
"""Cron trigger for ADWs.

Polls for new tasks and spawns workflows.
"""
import argparse
import time
import sys
from pathlib import Path

SPECS_DIR = Path("{{ config.paths.specs_dir }}")
POLL_INTERVAL = 20  # seconds


def get_pending_tasks() -> list:
    """Get pending task files from specs directory."""
    tasks = []
    for spec_file in SPECS_DIR.glob("*.md"):
        content = spec_file.read_text()
        if "status: pending" in content.lower():
            tasks.append(spec_file)
    return tasks


def main():
    parser = argparse.ArgumentParser(description="Poll for tasks")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=POLL_INTERVAL, help="Poll interval in seconds")
    args = parser.parse_args()

    print(f"Starting trigger (interval: {args.interval}s)")

    while True:
        tasks = get_pending_tasks()

        if tasks:
            print(f"Found {len(tasks)} pending tasks")
            for task in tasks:
                print(f"  - {task.name}")
                # Here you would spawn the appropriate workflow

        if args.once:
            break

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
```

## Criterios de Aceptacion
1. [ ] Directorio `templates/adws/` creado con toda la estructura
2. [ ] README.md.j2 documenta la estructura
3. [ ] Modulos en adw_modules/ completos y funcionales
4. [ ] Workflows adw_sdlc_iso.py y adw_patch_iso.py creados
5. [ ] Trigger cron basico creado
6. [ ] Todos los templates usan variables de config

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
find tac_bootstrap/templates/adws -name "*.j2" | head -20

# Test rendering
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

result = repo.render('adws/README.md.j2', {'config': config})
print(result[:1000])
"
```
```

---

### TAREA 3.5: Crear templates para scripts/ y config/

```markdown
# Prompt para Agente

## Contexto
TAC Bootstrap genera scripts de utilidad en `scripts/` y archivos de configuracion
como `config.yml` y `.mcp.json`.

## Objetivo
Crear templates para:
1. Scripts de utilidad (start.sh, test.sh, lint.sh, build.sh)
2. config.yml (archivo de configuracion generado)
3. .mcp.json (configuracion de MCP servers)
4. .gitignore

## Directorio Base
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`

## Archivos a Crear

### 1. `scripts/start.sh.j2`
```jinja2
#!/bin/bash
# Start the application
# Generated by TAC Bootstrap for {{ config.project.name }}

set -e

echo "Starting {{ config.project.name }}..."
{{ config.commands.start }}
```

### 2. `scripts/test.sh.j2`
```jinja2
#!/bin/bash
# Run tests
# Generated by TAC Bootstrap for {{ config.project.name }}

set -e

echo "Running tests..."
{{ config.commands.test }}
```

### 3. `scripts/lint.sh.j2`
```jinja2
#!/bin/bash
# Run linter
# Generated by TAC Bootstrap for {{ config.project.name }}

set -e

{% if config.commands.lint %}
echo "Running linter..."
{{ config.commands.lint }}
{% else %}
echo "No lint command configured"
{% endif %}
```

### 4. `scripts/build.sh.j2`
```jinja2
#!/bin/bash
# Build the application
# Generated by TAC Bootstrap for {{ config.project.name }}

set -e

{% if config.commands.build %}
echo "Building {{ config.project.name }}..."
{{ config.commands.build }}
{% else %}
echo "No build command configured"
{% endif %}
```

### 5. `config/config.yml.j2`
```jinja2
# TAC Bootstrap Configuration
# Generated for: {{ config.project.name }}
# Docs: https://github.com/tac-bootstrap/tac-bootstrap

version: 1

project:
  name: "{{ config.project.name }}"
  mode: "{{ config.project.mode.value }}"
  repo_root: "{{ config.project.repo_root }}"
  language: "{{ config.project.language.value }}"
{% if config.project.framework %}
  framework: "{{ config.project.framework.value }}"
{% endif %}
  architecture: "{{ config.project.architecture.value }}"
  package_manager: "{{ config.project.package_manager.value }}"

paths:
  app_root: "{{ config.paths.app_root }}"
  agentic_root: "{{ config.paths.agentic_root }}"
  prompts_dir: "{{ config.paths.prompts_dir }}"
  adws_dir: "{{ config.paths.adws_dir }}"
  specs_dir: "{{ config.paths.specs_dir }}"
  logs_dir: "{{ config.paths.logs_dir }}"
  scripts_dir: "{{ config.paths.scripts_dir }}"
  worktrees_dir: "{{ config.paths.worktrees_dir }}"

commands:
  start: "{{ config.commands.start }}"
  test: "{{ config.commands.test }}"
{% if config.commands.lint %}
  lint: "{{ config.commands.lint }}"
{% endif %}
{% if config.commands.build %}
  build: "{{ config.commands.build }}"
{% endif %}
{% if config.commands.typecheck %}
  typecheck: "{{ config.commands.typecheck }}"
{% endif %}
{% if config.commands.format %}
  format: "{{ config.commands.format }}"
{% endif %}

agentic:
  provider: "{{ config.agentic.provider.value }}"
  model_policy:
    default: "{{ config.agentic.model_policy.default }}"
    heavy: "{{ config.agentic.model_policy.heavy }}"
  worktrees:
    enabled: {{ config.agentic.worktrees.enabled | lower }}
    max_parallel: {{ config.agentic.worktrees.max_parallel }}
  logging:
    level: "{{ config.agentic.logging.level }}"
    capture_agent_transcript: {{ config.agentic.logging.capture_agent_transcript | lower }}

claude:
  settings:
    project_name: "{{ config.claude.settings.project_name }}"
    preferred_style: "{{ config.claude.settings.preferred_style }}"
    allow_shell: {{ config.claude.settings.allow_shell | lower }}
```

### 6. `config/.mcp.json.j2`
```jinja2
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--isolated",
        "--config",
        "./playwright-mcp-config.json"
      ]
    }
  }
}
```

### 7. `config/.gitignore.j2`
```jinja2
# TAC Bootstrap .gitignore
# Generated for {{ config.project.name }}

# Environment
.env
.env.local
.env.*.local

# Logs
{{ config.paths.logs_dir }}/
*.log

# Agent outputs (can be large)
agents/

# Git worktrees
{{ config.paths.worktrees_dir }}/

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
*.so
.eggs/
*.egg-info/
.venv/
venv/
.uv/

# Node
node_modules/
.npm
.pnpm-store/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
*.egg

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Secrets (never commit!)
secrets/
*.pem
*.key
credentials.json
```

### 8. `structure/specs/README.md.j2`
```jinja2
# Specifications

Este directorio contiene las especificaciones de issues y features.

## Estructura

```
{{ config.paths.specs_dir }}/
├── feature-*.md    # Planes de features
├── bug-*.md        # Planes de bugs
├── chore-*.md      # Planes de tareas
└── issue-*.md      # Specs de issues genericos
```

## Formato

Cada spec sigue este formato:

```markdown
# [Type]: [Title]

## Summary
[Descripcion breve]

## Files to Modify
- `path/to/file` - [cambios]

## Implementation Steps
1. [ ] Paso 1
2. [ ] Paso 2

## Test Cases
- [ ] Test 1
- [ ] Test 2

## Definition of Done
- [ ] Tests pasan
- [ ] Lint pasa
- [ ] Review aprobado
```
```

### 9. `structure/app_docs/README.md.j2`
```jinja2
# Application Documentation

Documentacion de {{ config.project.name }}.

## Estructura

```
app_docs/
├── features/       # Documentacion de features
├── api/            # Documentacion de API
└── guides/         # Guias de uso
```

## Generacion

La documentacion se genera automaticamente con:

```bash
claude -p "/document [feature]"
```
```

### 10. `structure/ai_docs/README.md.j2`
```jinja2
# AI Documentation

Documentacion generada por agentes para {{ config.project.name }}.

Este directorio contiene documentacion auto-generada durante el desarrollo.
```

## Criterios de Aceptacion
1. [ ] Directorio `templates/scripts/` con 4 scripts
2. [ ] Directorio `templates/config/` con config.yml, .mcp.json, .gitignore
3. [ ] Directorio `templates/structure/` con READMEs para specs, app_docs, ai_docs
4. [ ] Todos los templates usan variables de config correctamente

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
find tac_bootstrap/templates -name "*.j2" | wc -l
# Deberia ser ~40+ templates

# Test rendering de config.yml
uv run python -c "
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import *

repo = TemplateRepository()
config = TACConfig(
    project=ProjectSpec(name='my-app', language=Language.PYTHON, package_manager=PackageManager.UV, framework=Framework.FASTAPI),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest', lint='uv run ruff check .'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='my-app'))
)

result = repo.render('config/config.yml.j2', {'config': config})
print(result)
"
```
```

---

## FASE 4-9: Continuacion...

Las fases 4-9 siguen el mismo patron de prompts detallados. Por brevedad, aqui estan los titulos:

### FASE 4: CLI con Typer + Rich (40-55%)
- **TAREA 4.1**: Implementar comandos CLI (init, add-agentic, doctor, render)
- **TAREA 4.2**: Implementar wizard interactivo con Rich

### FASE 5: Servicio de Scaffold (55-70%)
- **TAREA 5.1**: Implementar ScaffoldService.build_plan()
- **TAREA 5.2**: Implementar ScaffoldService.apply_plan()
- **TAREA 5.3**: Implementar FileSystem operations

### FASE 6: Servicio de Deteccion (70-80%)
- **TAREA 6.1**: Implementar DetectService (auto-detect stack)

### FASE 7: Servicio Doctor (80-90%)
- **TAREA 7.1**: Implementar DoctorService (validacion)

### FASE 8: Tests (90-95%)
- **TAREA 8.1**: Tests unitarios para todos los modulos

### FASE 9: Documentacion (95-100%)
- **TAREA 9.1**: README y documentacion de uso

---

## Estructura Final Generada

Cuando el usuario ejecute `tac-bootstrap init` o `add-agentic`, se generara:

```
proyecto/
├── .claude/
│   ├── settings.json
│   ├── commands/
│   │   ├── prime.md, start.md, build.md, test.md
│   │   ├── feature.md, bug.md, chore.md, patch.md
│   │   ├── implement.md, commit.md, pull_request.md
│   │   ├── review.md, document.md, health_check.md
│   │   └── ...
│   └── hooks/
│       ├── pre_tool_use.py, post_tool_use.py, stop.py
│       └── utils/constants.py
├── adws/
│   ├── README.md
│   ├── adw_modules/ (agent, state, git_ops, workflow_ops)
│   ├── adw_sdlc_iso.py, adw_patch_iso.py
│   └── adw_triggers/trigger_cron.py
├── prompts/templates/ (plan.md, chore.md, feature.md)
├── scripts/ (start.sh, test.sh, lint.sh, build.sh)
├── specs/, logs/, agents/, trees/, app_docs/, ai_docs/
├── config.yml
├── .mcp.json
└── .gitignore
```

---

## Definition of Done (v1)

- [ ] `tac-bootstrap init` crea repo funcional
- [ ] `tac-bootstrap add-agentic` injerta agentic layer
- [ ] `.claude/commands` operables
- [ ] ADWs ejecutan y escriben logs
- [ ] `doctor` detecta fallas
- [ ] Tests con cobertura > 80%
- [ ] Documentacion completa
