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

## FASE 4: CLI con Typer + Rich (40-55%)

---

### TAREA 4.1: Implementar comandos CLI principales

```markdown
# Prompt para Agente

## Contexto
Ya tenemos los modelos de dominio (TACConfig, ScaffoldPlan), el repositorio de templates,
y los templates Jinja2. Ahora necesitamos implementar los comandos CLI que el usuario
ejecutara para generar la Agentic Layer.

Los comandos principales son:
- `init` - Crear proyecto nuevo con agentic layer
- `add-agentic` - Inyectar agentic layer en repo existente
- `doctor` - Validar setup existente
- `render` - Re-generar desde config.yml

## Objetivo
Implementar los 4 comandos CLI usando Typer con opciones y argumentos apropiados.

## Archivo a Modificar
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`

## Contenido Completo

```python
"""CLI interface for TAC Bootstrap.

Commands:
    init        Create new project with Agentic Layer
    add-agentic Inject Agentic Layer into existing repo
    doctor      Validate existing setup
    render      Re-generate from config.yml
"""
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from tac_bootstrap import __version__
from tac_bootstrap.domain.models import (
    Language,
    Framework,
    PackageManager,
    Architecture,
    TACConfig,
    ProjectSpec,
    CommandsSpec,
    ClaudeConfig,
    ClaudeSettings,
    PathsSpec,
    get_default_commands,
)

app = typer.Typer(
    name="tac-bootstrap",
    help="Bootstrap Agentic Layer for Claude Code with TAC patterns",
    add_completion=False,
)

console = Console()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Bootstrap Agentic Layer for Claude Code with TAC patterns."""
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit(
            f"[bold blue]TAC Bootstrap[/bold blue] v{__version__}\n\n"
            "Use [green]--help[/green] for available commands",
            title="🚀 Agentic Layer Generator"
        ))


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"[bold]tac-bootstrap[/bold] v{__version__}")


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory (default: ./<name>)"
    ),
    language: Language = typer.Option(
        Language.PYTHON, "--language", "-l",
        help="Programming language"
    ),
    framework: Framework = typer.Option(
        Framework.NONE, "--framework", "-f",
        help="Web framework"
    ),
    package_manager: Optional[PackageManager] = typer.Option(
        None, "--package-manager", "-p",
        help="Package manager (auto-detected if not specified)"
    ),
    architecture: Architecture = typer.Option(
        Architecture.SIMPLE, "--architecture", "-a",
        help="Software architecture pattern"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i/-I",
        help="Use interactive wizard"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Show what would be created without creating"
    ),
) -> None:
    """Create a new project with Agentic Layer.

    Example:
        tac-bootstrap init my-app --language python --framework fastapi
    """
    from tac_bootstrap.application.scaffold_service import ScaffoldService
    from tac_bootstrap.interfaces.wizard import run_init_wizard

    # Use wizard if interactive
    if interactive:
        config = run_init_wizard(name, language, framework, package_manager, architecture)
    else:
        # Auto-detect package manager if not specified
        if package_manager is None:
            from tac_bootstrap.domain.models import get_package_managers_for_language
            managers = get_package_managers_for_language(language)
            package_manager = managers[0] if managers else PackageManager.PIP

        # Get default commands
        commands = get_default_commands(language, package_manager)

        config = TACConfig(
            project=ProjectSpec(
                name=name,
                language=language,
                framework=framework,
                architecture=architecture,
                package_manager=package_manager,
            ),
            paths=PathsSpec(app_root="src"),
            commands=CommandsSpec(**commands),
            claude=ClaudeConfig(
                settings=ClaudeSettings(project_name=name)
            ),
        )

    # Determine output directory
    target_dir = output_dir or Path.cwd() / config.project.name

    # Build and apply scaffold plan
    service = ScaffoldService()
    plan = service.build_plan(config)

    if dry_run:
        console.print(Panel(plan.summary, title="[yellow]Dry Run[/yellow]"))
        console.print("\n[bold]Directories to create:[/bold]")
        for d in plan.directories:
            console.print(f"  📁 {d.path}/")
        console.print("\n[bold]Files to create:[/bold]")
        for f in plan.get_files_to_create():
            console.print(f"  📄 {f.path}")
        return

    # Apply the plan
    result = service.apply_plan(plan, target_dir, config)

    if result.success:
        console.print(Panel.fit(
            f"[green]✓[/green] Project created at [bold]{target_dir}[/bold]\n\n"
            f"Created {result.directories_created} directories\n"
            f"Created {result.files_created} files\n\n"
            f"[dim]Next steps:[/dim]\n"
            f"  cd {config.project.name}\n"
            f"  claude -p '/prime'",
            title="🎉 Success"
        ))
    else:
        console.print(f"[red]Error:[/red] {result.error}")
        raise typer.Exit(1)


@app.command("add-agentic")
def add_agentic(
    repo_path: Path = typer.Argument(
        Path("."),
        help="Path to existing repository"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", "-i/-I",
        help="Use interactive wizard"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Show what would be created without creating"
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Overwrite existing files"
    ),
) -> None:
    """Inject Agentic Layer into an existing repository.

    Auto-detects the project's language, framework, and package manager.

    Example:
        cd my-existing-project
        tac-bootstrap add-agentic .
    """
    from tac_bootstrap.application.detect_service import DetectService
    from tac_bootstrap.application.scaffold_service import ScaffoldService
    from tac_bootstrap.interfaces.wizard import run_add_agentic_wizard

    repo_path = repo_path.resolve()

    if not repo_path.exists():
        console.print(f"[red]Error:[/red] Path does not exist: {repo_path}")
        raise typer.Exit(1)

    # Auto-detect project settings
    detector = DetectService()
    detected = detector.detect(repo_path)

    console.print(Panel(
        f"[bold]Detected:[/bold]\n"
        f"  Language: {detected.language.value}\n"
        f"  Framework: {detected.framework.value if detected.framework else 'none'}\n"
        f"  Package Manager: {detected.package_manager.value}",
        title="🔍 Auto-Detection"
    ))

    # Use wizard or auto-config
    if interactive:
        config = run_add_agentic_wizard(repo_path, detected)
    else:
        commands = get_default_commands(detected.language, detected.package_manager)
        config = TACConfig(
            project=ProjectSpec(
                name=repo_path.name,
                mode="existing",
                language=detected.language,
                framework=detected.framework or Framework.NONE,
                package_manager=detected.package_manager,
            ),
            paths=PathsSpec(app_root=detected.app_root or "src"),
            commands=CommandsSpec(**commands),
            claude=ClaudeConfig(
                settings=ClaudeSettings(project_name=repo_path.name)
            ),
        )

    # Build plan
    service = ScaffoldService()
    plan = service.build_plan(config, existing_repo=True)

    if dry_run:
        console.print(Panel(plan.summary, title="[yellow]Dry Run[/yellow]"))
        for f in plan.files:
            status = f.action.value
            console.print(f"  [{status}] {f.path}")
        return

    # Apply plan
    result = service.apply_plan(plan, repo_path, config, force=force)

    if result.success:
        console.print(Panel.fit(
            f"[green]✓[/green] Agentic Layer added to [bold]{repo_path}[/bold]\n\n"
            f"Created {result.files_created} files\n"
            f"Skipped {result.files_skipped} existing files\n\n"
            f"[dim]Next steps:[/dim]\n"
            f"  claude -p '/prime'",
            title="🎉 Success"
        ))
    else:
        console.print(f"[red]Error:[/red] {result.error}")
        raise typer.Exit(1)


@app.command()
def doctor(
    repo_path: Path = typer.Argument(
        Path("."),
        help="Path to repository to validate"
    ),
    fix: bool = typer.Option(
        False, "--fix",
        help="Attempt to fix issues automatically"
    ),
) -> None:
    """Validate an existing Agentic Layer setup.

    Checks for:
    - Required directories exist
    - Required files exist
    - Configuration is valid
    - Commands are executable

    Example:
        tac-bootstrap doctor .
    """
    from tac_bootstrap.application.doctor_service import DoctorService

    repo_path = repo_path.resolve()

    service = DoctorService()
    report = service.diagnose(repo_path)

    # Display results
    if report.healthy:
        console.print(Panel.fit(
            "[green]✓[/green] All checks passed!",
            title="🏥 Health Check"
        ))
    else:
        console.print(Panel.fit(
            f"[red]✗[/red] Found {len(report.issues)} issue(s)",
            title="🏥 Health Check"
        ))

        for issue in report.issues:
            severity_color = {
                "error": "red",
                "warning": "yellow",
                "info": "blue"
            }.get(issue.severity, "white")

            console.print(f"  [{severity_color}]{issue.severity.upper()}[/{severity_color}] {issue.message}")
            if issue.suggestion:
                console.print(f"         [dim]Suggestion: {issue.suggestion}[/dim]")

        if fix:
            console.print("\n[bold]Attempting fixes...[/bold]")
            fix_result = service.fix(repo_path, report)
            console.print(f"  Fixed {fix_result.fixed_count} issue(s)")

        raise typer.Exit(1)


@app.command()
def render(
    config_file: Path = typer.Argument(
        Path("config.yml"),
        help="Path to config.yml file"
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output directory (default: same as config file)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Show what would be created without creating"
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Overwrite existing files"
    ),
) -> None:
    """Re-generate Agentic Layer from config.yml.

    Useful for updating after modifying config.yml manually.

    Example:
        tac-bootstrap render config.yml
    """
    import yaml
    from tac_bootstrap.application.scaffold_service import ScaffoldService

    if not config_file.exists():
        console.print(f"[red]Error:[/red] Config file not found: {config_file}")
        raise typer.Exit(1)

    # Load config
    try:
        with open(config_file) as f:
            raw_config = yaml.safe_load(f)
        config = TACConfig(**raw_config)
    except Exception as e:
        console.print(f"[red]Error parsing config:[/red] {e}")
        raise typer.Exit(1)

    # Determine output directory
    target_dir = output_dir or config_file.parent

    # Build and apply plan
    service = ScaffoldService()
    plan = service.build_plan(config, existing_repo=True)

    if dry_run:
        console.print(Panel(plan.summary, title="[yellow]Dry Run[/yellow]"))
        for f in plan.files:
            console.print(f"  [{f.action.value}] {f.path}")
        return

    result = service.apply_plan(plan, target_dir, config, force=force)

    if result.success:
        console.print(Panel.fit(
            f"[green]✓[/green] Regenerated from [bold]{config_file}[/bold]\n\n"
            f"Updated {result.files_created} files",
            title="🔄 Render Complete"
        ))
    else:
        console.print(f"[red]Error:[/red] {result.error}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
```

## Criterios de Aceptacion
1. [ ] Comando `init` crea proyecto nuevo con opciones de lenguaje/framework
2. [ ] Comando `add-agentic` detecta e inyecta en repo existente
3. [ ] Comando `doctor` valida setup y reporta issues
4. [ ] Comando `render` regenera desde config.yml
5. [ ] Todos los comandos soportan `--dry-run`
6. [ ] Output usa Rich para formateo bonito

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Verificar que CLI carga sin errores
uv run tac-bootstrap --help
uv run tac-bootstrap init --help
uv run tac-bootstrap add-agentic --help
uv run tac-bootstrap doctor --help
uv run tac-bootstrap render --help

# Smoke test version
uv run tac-bootstrap version
```

## NO hacer
- No implementar la logica de ScaffoldService aun (siguiente tarea)
- No implementar DetectService aun (FASE 6)
- No implementar DoctorService aun (FASE 7)
- No implementar wizard aun (siguiente tarea)
```

---

### TAREA 4.2: Implementar wizard interactivo con Rich

```markdown
# Prompt para Agente

## Contexto
La CLI ya tiene los comandos basicos. Ahora necesitamos implementar el wizard
interactivo que guia al usuario para configurar el proyecto paso a paso.

El wizard usa Rich para:
- Prompts interactivos con opciones
- Colores y formateo bonito
- Confirmacion antes de ejecutar

## Objetivo
Crear el modulo wizard.py con funciones para guiar la configuracion interactiva.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`

## Contenido Completo

```python
"""Interactive wizard for TAC Bootstrap configuration.

Uses Rich for beautiful terminal UI with prompts and selections.
"""
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from tac_bootstrap.domain.models import (
    TACConfig,
    ProjectSpec,
    PathsSpec,
    CommandsSpec,
    ClaudeConfig,
    ClaudeSettings,
    AgenticSpec,
    Language,
    Framework,
    Architecture,
    PackageManager,
    ProjectMode,
    get_frameworks_for_language,
    get_package_managers_for_language,
    get_default_commands,
)

console = Console()


def select_from_enum(prompt: str, enum_class, default=None, filter_fn=None) -> any:
    """Interactive selection from enum values.

    Args:
        prompt: Question to ask
        enum_class: Enum class to select from
        default: Default value
        filter_fn: Optional function to filter valid options

    Returns:
        Selected enum value
    """
    options = list(enum_class)
    if filter_fn:
        options = [o for o in options if filter_fn(o)]

    # Build options table
    table = Table(show_header=False, box=None, padding=(0, 2))
    for i, opt in enumerate(options, 1):
        is_default = opt == default
        marker = "[green]>[/green]" if is_default else " "
        table.add_row(f"{marker} {i}.", f"[bold]{opt.value}[/bold]")

    console.print(f"\n[bold]{prompt}[/bold]")
    console.print(table)

    # Get selection
    default_num = options.index(default) + 1 if default in options else 1
    choice = Prompt.ask(
        "Select option",
        default=str(default_num),
        choices=[str(i) for i in range(1, len(options) + 1)]
    )

    return options[int(choice) - 1]


def run_init_wizard(
    name: str,
    language: Optional[Language] = None,
    framework: Optional[Framework] = None,
    package_manager: Optional[PackageManager] = None,
    architecture: Optional[Architecture] = None,
) -> TACConfig:
    """Run interactive wizard for project initialization.

    Args:
        name: Project name (already provided)
        language: Pre-selected language (or None to ask)
        framework: Pre-selected framework (or None to ask)
        package_manager: Pre-selected package manager (or None to ask)
        architecture: Pre-selected architecture (or None to ask)

    Returns:
        Configured TACConfig
    """
    console.print(Panel.fit(
        f"[bold blue]Creating new project:[/bold blue] {name}\n\n"
        "Let's configure your Agentic Layer!",
        title="🚀 TAC Bootstrap Wizard"
    ))

    # Step 1: Language
    if language is None:
        language = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON
        )
    console.print(f"  [green]✓[/green] Language: {language.value}")

    # Step 2: Framework
    if framework is None:
        valid_frameworks = get_frameworks_for_language(language)
        framework = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.NONE,
            filter_fn=lambda f: f in valid_frameworks
        )
    console.print(f"  [green]✓[/green] Framework: {framework.value}")

    # Step 3: Package Manager
    if package_manager is None:
        valid_managers = get_package_managers_for_language(language)
        package_manager = select_from_enum(
            "What package manager?",
            PackageManager,
            default=valid_managers[0] if valid_managers else None,
            filter_fn=lambda p: p in valid_managers
        )
    console.print(f"  [green]✓[/green] Package Manager: {package_manager.value}")

    # Step 4: Architecture
    if architecture is None:
        architecture = select_from_enum(
            "What architecture pattern?",
            Architecture,
            default=Architecture.SIMPLE
        )
    console.print(f"  [green]✓[/green] Architecture: {architecture.value}")

    # Step 5: Commands (with smart defaults)
    console.print("\n[bold]Commands Configuration[/bold]")
    default_commands = get_default_commands(language, package_manager)

    start_cmd = Prompt.ask(
        "  Start command",
        default=default_commands.get("start", "")
    )
    test_cmd = Prompt.ask(
        "  Test command",
        default=default_commands.get("test", "")
    )
    lint_cmd = Prompt.ask(
        "  Lint command (optional)",
        default=default_commands.get("lint", "")
    )

    # Step 6: Worktrees
    use_worktrees = Confirm.ask(
        "\nEnable git worktrees for parallel workflows?",
        default=True
    )

    # Build config
    config = TACConfig(
        project=ProjectSpec(
            name=name,
            mode=ProjectMode.NEW,
            language=language,
            framework=framework,
            architecture=architecture,
            package_manager=package_manager,
        ),
        paths=PathsSpec(
            app_root="src" if architecture != Architecture.SIMPLE else ".",
        ),
        commands=CommandsSpec(
            start=start_cmd,
            test=test_cmd,
            lint=lint_cmd,
        ),
        agentic=AgenticSpec(
            worktrees={"enabled": use_worktrees, "max_parallel": 5},
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name=name)
        ),
    )

    # Confirmation
    console.print("\n")
    _show_config_summary(config)

    if not Confirm.ask("\nProceed with this configuration?", default=True):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(0)

    return config


def run_add_agentic_wizard(
    repo_path: Path,
    detected: "DetectedProject",
) -> TACConfig:
    """Run wizard for adding agentic layer to existing project.

    Args:
        repo_path: Path to existing repository
        detected: Auto-detected project settings

    Returns:
        Configured TACConfig
    """
    console.print(Panel.fit(
        f"[bold blue]Adding Agentic Layer to:[/bold blue] {repo_path.name}\n\n"
        "Review detected settings and customize commands.",
        title="🔧 TAC Bootstrap Wizard"
    ))

    # Confirm or change detected settings
    language = select_from_enum(
        "Programming language (detected):",
        Language,
        default=detected.language
    )

    framework = select_from_enum(
        "Framework (detected):",
        Framework,
        default=detected.framework or Framework.NONE,
        filter_fn=lambda f: f in get_frameworks_for_language(language)
    )

    package_manager = select_from_enum(
        "Package manager (detected):",
        PackageManager,
        default=detected.package_manager,
        filter_fn=lambda p: p in get_package_managers_for_language(language)
    )

    # Commands - most important for existing projects
    console.print("\n[bold]Configure Commands[/bold]")
    console.print("[dim]These commands will be used by Claude Code and ADW workflows[/dim]\n")

    default_commands = get_default_commands(language, package_manager)

    start_cmd = Prompt.ask(
        "  Start command",
        default=detected.commands.get("start", default_commands.get("start", ""))
    )
    test_cmd = Prompt.ask(
        "  Test command",
        default=detected.commands.get("test", default_commands.get("test", ""))
    )
    lint_cmd = Prompt.ask(
        "  Lint command",
        default=detected.commands.get("lint", default_commands.get("lint", ""))
    )
    build_cmd = Prompt.ask(
        "  Build command",
        default=detected.commands.get("build", default_commands.get("build", ""))
    )

    # Worktrees
    use_worktrees = Confirm.ask(
        "\nEnable git worktrees for parallel workflows?",
        default=True
    )

    # Build config
    config = TACConfig(
        project=ProjectSpec(
            name=repo_path.name,
            mode=ProjectMode.EXISTING,
            repo_root=str(repo_path),
            language=language,
            framework=framework,
            package_manager=package_manager,
        ),
        paths=PathsSpec(
            app_root=detected.app_root or "src",
        ),
        commands=CommandsSpec(
            start=start_cmd,
            test=test_cmd,
            lint=lint_cmd,
            build=build_cmd,
        ),
        agentic=AgenticSpec(
            worktrees={"enabled": use_worktrees, "max_parallel": 5},
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name=repo_path.name)
        ),
    )

    # Confirmation
    console.print("\n")
    _show_config_summary(config)

    if not Confirm.ask("\nProceed with this configuration?", default=True):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(0)

    return config


def _show_config_summary(config: TACConfig) -> None:
    """Display configuration summary table."""
    table = Table(title="Configuration Summary", show_header=True)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", config.project.name)
    table.add_row("Language", config.project.language.value)
    table.add_row("Framework", config.project.framework.value)
    table.add_row("Package Manager", config.project.package_manager.value)
    table.add_row("Architecture", config.project.architecture.value)
    table.add_row("Start Command", config.commands.start)
    table.add_row("Test Command", config.commands.test)
    table.add_row("Worktrees Enabled", str(config.agentic.worktrees.enabled))

    console.print(table)
```

## Criterios de Aceptacion
1. [ ] select_from_enum muestra opciones numeradas
2. [ ] run_init_wizard guia configuracion completa
3. [ ] run_add_agentic_wizard usa valores detectados como defaults
4. [ ] Tabla de resumen muestra configuracion final
5. [ ] Confirmacion antes de proceder
6. [ ] UI es clara y bonita con Rich

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test import
uv run python -c "
from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard
from tac_bootstrap.domain.models import Language
print('Wizard module loaded successfully')
"

# Test con init interactivo (manual)
# uv run tac-bootstrap init test-project
```

## NO hacer
- No implementar logica de scaffolding (FASE 5)
- No implementar deteccion (FASE 6)
```

---

## FASE 5: Servicio de Scaffold (55-70%)

---

### TAREA 5.1: Implementar ScaffoldService.build_plan()

```markdown
# Prompt para Agente

## Contexto
El ScaffoldService es el servicio central que construye y aplica el plan de scaffolding.
Ya tenemos los modelos ScaffoldPlan, FileOperation y DirectoryOperation en domain/plan.py.
Ahora necesitamos implementar la logica que construye el plan basado en la configuracion.

## Objetivo
Implementar el metodo build_plan() que analiza la configuracion y construye un
ScaffoldPlan con todas las operaciones necesarias.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`

## Contenido Completo

```python
"""Scaffold Service for building and applying generation plans.

This service is responsible for:
1. Building a ScaffoldPlan from TACConfig
2. Applying the plan to create directories and files
3. Handling idempotency and existing files
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from tac_bootstrap.domain.models import TACConfig
from tac_bootstrap.domain.plan import (
    ScaffoldPlan,
    FileOperation,
    FileAction,
    DirectoryOperation,
)
from tac_bootstrap.infrastructure.template_repo import TemplateRepository


@dataclass
class ApplyResult:
    """Result of applying a scaffold plan."""
    success: bool = True
    directories_created: int = 0
    files_created: int = 0
    files_skipped: int = 0
    files_overwritten: int = 0
    error: Optional[str] = None
    errors: List[str] = field(default_factory=list)


class ScaffoldService:
    """Service for building and applying scaffold plans.

    Example:
        service = ScaffoldService()
        plan = service.build_plan(config)
        result = service.apply_plan(plan, output_dir, config)
    """

    def __init__(self, template_repo: Optional[TemplateRepository] = None):
        """Initialize scaffold service.

        Args:
            template_repo: Template repository (created if not provided)
        """
        self.template_repo = template_repo or TemplateRepository()

    def build_plan(
        self,
        config: TACConfig,
        existing_repo: bool = False,
    ) -> ScaffoldPlan:
        """Build a scaffold plan from configuration.

        Args:
            config: TAC configuration
            existing_repo: Whether scaffolding into existing repo

        Returns:
            ScaffoldPlan with all operations to perform
        """
        plan = ScaffoldPlan()

        # Add directory structure
        self._add_directories(plan, config)

        # Add Claude configuration files
        self._add_claude_files(plan, config, existing_repo)

        # Add ADW files
        self._add_adw_files(plan, config, existing_repo)

        # Add script files
        self._add_script_files(plan, config, existing_repo)

        # Add config files
        self._add_config_files(plan, config, existing_repo)

        # Add structure READMEs
        self._add_structure_files(plan, config, existing_repo)

        return plan

    def _add_directories(self, plan: ScaffoldPlan, config: TACConfig) -> None:
        """Add directory operations to plan."""
        directories = [
            (".claude", "Claude Code configuration"),
            (".claude/commands", "Slash commands"),
            (".claude/hooks", "Execution hooks"),
            (".claude/hooks/utils", "Hook utilities"),
            (config.paths.adws_dir, "AI Developer Workflows"),
            (f"{config.paths.adws_dir}/adw_modules", "ADW shared modules"),
            (f"{config.paths.adws_dir}/adw_triggers", "ADW triggers"),
            (config.paths.specs_dir, "Specifications"),
            (config.paths.logs_dir, "Execution logs"),
            (config.paths.scripts_dir, "Utility scripts"),
            (config.paths.prompts_dir, "Prompt templates"),
            (f"{config.paths.prompts_dir}/templates", "Document templates"),
            ("agents", "ADW agent state"),
            (config.paths.worktrees_dir, "Git worktrees"),
            ("app_docs", "Application documentation"),
            ("ai_docs", "AI-generated documentation"),
        ]

        for path, reason in directories:
            plan.add_directory(path, reason)

    def _add_claude_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add .claude/ configuration files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP

        # Settings
        plan.add_file(
            ".claude/settings.json",
            action=action,
            template="claude/settings.json.j2",
            reason="Claude Code settings and permissions",
        )

        # Commands - all slash commands
        commands = [
            "prime", "start", "build", "test", "lint",
            "feature", "bug", "chore", "patch",
            "implement", "commit", "pull_request",
            "review", "document", "health_check",
            "prepare_app", "install", "track_agentic_kpis",
        ]

        for cmd in commands:
            plan.add_file(
                f".claude/commands/{cmd}.md",
                action=action,
                template=f"claude/commands/{cmd}.md.j2",
                reason=f"/{cmd} slash command",
            )

        # Hooks
        hooks = [
            ("pre_tool_use.py", "Pre-execution validation"),
            ("post_tool_use.py", "Post-execution logging"),
            ("stop.py", "Session cleanup"),
        ]

        for hook, reason in hooks:
            plan.add_file(
                f".claude/hooks/{hook}",
                action=action,
                template=f"claude/hooks/{hook}.j2",
                reason=reason,
                executable=True,
            )

        # Hook utils
        plan.add_file(
            ".claude/hooks/utils/__init__.py",
            action=action,
            template="claude/hooks/utils/__init__.py.j2",
            reason="Hook utilities package",
        )
        plan.add_file(
            ".claude/hooks/utils/constants.py",
            action=action,
            template="claude/hooks/utils/constants.py.j2",
            reason="Shared constants for hooks",
        )

    def _add_adw_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add adws/ workflow files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP
        adws_dir = config.paths.adws_dir

        # README
        plan.add_file(
            f"{adws_dir}/README.md",
            action=action,
            template="adws/README.md.j2",
            reason="ADW documentation",
        )

        # Modules
        modules = [
            ("__init__.py", "Package init"),
            ("agent.py", "Claude Code wrapper"),
            ("state.py", "State persistence"),
            ("git_ops.py", "Git operations"),
            ("workflow_ops.py", "Workflow orchestration"),
        ]

        for module, reason in modules:
            plan.add_file(
                f"{adws_dir}/adw_modules/{module}",
                action=action,
                template=f"adws/adw_modules/{module}.j2",
                reason=reason,
            )

        # Workflows
        workflows = [
            ("adw_sdlc_iso.py", "SDLC workflow (isolated)"),
            ("adw_patch_iso.py", "Patch workflow (isolated)"),
        ]

        for workflow, reason in workflows:
            plan.add_file(
                f"{adws_dir}/{workflow}",
                action=action,
                template=f"adws/{workflow}.j2",
                reason=reason,
                executable=True,
            )

        # Triggers
        plan.add_file(
            f"{adws_dir}/adw_triggers/__init__.py",
            action=action,
            template="adws/adw_triggers/__init__.py.j2",
            reason="Triggers package",
        )
        plan.add_file(
            f"{adws_dir}/adw_triggers/trigger_cron.py",
            action=action,
            template="adws/adw_triggers/trigger_cron.py.j2",
            reason="Cron-based task polling",
            executable=True,
        )

    def _add_script_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add scripts/ utility files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP
        scripts_dir = config.paths.scripts_dir

        scripts = [
            ("start.sh", "Application starter"),
            ("test.sh", "Test runner"),
            ("lint.sh", "Linter runner"),
            ("build.sh", "Build script"),
        ]

        for script, reason in scripts:
            plan.add_file(
                f"{scripts_dir}/{script}",
                action=action,
                template=f"scripts/{script}.j2",
                reason=reason,
                executable=True,
            )

    def _add_config_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add configuration files."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP

        # config.yml - always create/overwrite to capture user settings
        plan.add_file(
            "config.yml",
            action=FileAction.OVERWRITE if existing_repo else FileAction.CREATE,
            template="config/config.yml.j2",
            reason="TAC Bootstrap configuration",
        )

        # .mcp.json
        plan.add_file(
            ".mcp.json",
            action=action,
            template="config/.mcp.json.j2",
            reason="MCP server configuration",
        )

        # .gitignore - append if exists
        plan.add_file(
            ".gitignore",
            action=FileAction.PATCH if existing_repo else FileAction.CREATE,
            template="config/.gitignore.j2",
            reason="Git ignore patterns",
        )

    def _add_structure_files(
        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
    ) -> None:
        """Add README files for directory structure."""
        action = FileAction.CREATE if not existing_repo else FileAction.SKIP

        structure_readmes = [
            (f"{config.paths.specs_dir}/README.md", "structure/specs/README.md.j2"),
            ("app_docs/README.md", "structure/app_docs/README.md.j2"),
            ("ai_docs/README.md", "structure/ai_docs/README.md.j2"),
        ]

        for path, template in structure_readmes:
            plan.add_file(
                path,
                action=action,
                template=template,
                reason="Directory documentation",
            )

    def apply_plan(
        self,
        plan: ScaffoldPlan,
        output_dir: Path,
        config: TACConfig,
        force: bool = False,
    ) -> ApplyResult:
        """Apply a scaffold plan to create files and directories.

        Args:
            plan: The scaffold plan to apply
            output_dir: Target directory
            config: Configuration for template rendering
            force: Overwrite existing files

        Returns:
            ApplyResult with statistics and any errors
        """
        from tac_bootstrap.infrastructure.fs import FileSystem

        result = ApplyResult()
        fs = FileSystem()
        template_context = {"config": config}

        # Create directories first
        for dir_op in plan.directories:
            dir_path = output_dir / dir_op.path
            try:
                fs.ensure_directory(dir_path)
                result.directories_created += 1
            except Exception as e:
                result.errors.append(f"Failed to create {dir_op.path}: {e}")

        # Process files
        for file_op in plan.files:
            file_path = output_dir / file_op.path

            try:
                # Determine action based on existence and force flag
                if file_path.exists() and file_op.action == FileAction.CREATE:
                    if not force:
                        result.files_skipped += 1
                        continue
                    # Force mode - treat as overwrite
                    actual_action = FileAction.OVERWRITE
                else:
                    actual_action = file_op.action

                if actual_action == FileAction.SKIP:
                    result.files_skipped += 1
                    continue

                # Render content
                if file_op.template:
                    content = self.template_repo.render(
                        file_op.template, template_context
                    )
                elif file_op.content:
                    content = file_op.content
                else:
                    content = ""

                # Apply based on action
                if actual_action == FileAction.PATCH:
                    fs.append_file(file_path, content)
                else:
                    fs.write_file(file_path, content)

                # Make executable if needed
                if file_op.executable:
                    fs.make_executable(file_path)

                if actual_action == FileAction.OVERWRITE and file_path.exists():
                    result.files_overwritten += 1
                else:
                    result.files_created += 1

            except Exception as e:
                result.errors.append(f"Failed to create {file_op.path}: {e}")

        # Set success based on errors
        if result.errors:
            result.success = False
            result.error = f"{len(result.errors)} error(s) occurred"

        return result
```

## Criterios de Aceptacion
1. [ ] build_plan() genera plan completo con ~50+ operaciones
2. [ ] Directorios se agregan en orden correcto
3. [ ] Archivos .claude/ incluyen settings, commands y hooks
4. [ ] Archivos adws/ incluyen modules y workflows
5. [ ] Scripts son marcados como ejecutables
6. [ ] apply_plan() crea estructura correctamente

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test build_plan
uv run python -c "
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import *

service = ScaffoldService()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

plan = service.build_plan(config)
print(plan.summary)
print(f'Directories: {plan.total_directories}')
print(f'Files: {plan.total_files}')
"
```

## NO hacer
- No crear los archivos reales aun (eso es apply_plan)
- No implementar FileSystem aun (siguiente tarea)
```

---

### TAREA 5.2: Implementar FileSystem operations

```markdown
# Prompt para Agente

## Contexto
El ScaffoldService necesita operaciones de filesystem para crear directorios y archivos.
Estas operaciones deben ser idempotentes y seguras.

## Objetivo
Implementar el modulo fs.py con operaciones de filesystem idempotentes.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py`

## Contenido Completo

```python
"""File system operations for scaffold generation.

Provides idempotent, safe file system operations.
"""
import os
import stat
from pathlib import Path
from typing import Optional


class FileSystem:
    """Safe file system operations.

    All operations are idempotent where possible.
    """

    def ensure_directory(self, path: Path) -> bool:
        """Ensure directory exists, creating if necessary.

        Args:
            path: Directory path to ensure

        Returns:
            True if created, False if already existed
        """
        if path.exists():
            return False
        path.mkdir(parents=True, exist_ok=True)
        return True

    def write_file(
        self,
        path: Path,
        content: str,
        encoding: str = "utf-8",
    ) -> None:
        """Write content to file, creating parent directories.

        Args:
            path: File path
            content: Content to write
            encoding: File encoding
        """
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        path.write_text(content, encoding=encoding)

    def append_file(
        self,
        path: Path,
        content: str,
        encoding: str = "utf-8",
        separator: str = "\n\n",
    ) -> None:
        """Append content to file, creating if doesn't exist.

        Args:
            path: File path
            content: Content to append
            encoding: File encoding
            separator: Separator between existing and new content
        """
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists():
            existing = path.read_text(encoding=encoding)
            # Don't append if content already present
            if content.strip() in existing:
                return
            new_content = existing.rstrip() + separator + content
        else:
            new_content = content

        path.write_text(new_content, encoding=encoding)

    def make_executable(self, path: Path) -> None:
        """Make file executable (chmod +x).

        Args:
            path: File path to make executable
        """
        if not path.exists():
            return

        current_mode = path.stat().st_mode
        # Add execute permission for user, group, other (if they have read)
        new_mode = current_mode | stat.S_IXUSR
        if current_mode & stat.S_IRGRP:
            new_mode |= stat.S_IXGRP
        if current_mode & stat.S_IROTH:
            new_mode |= stat.S_IXOTH

        os.chmod(path, new_mode)

    def file_exists(self, path: Path) -> bool:
        """Check if file exists.

        Args:
            path: File path

        Returns:
            True if file exists
        """
        return path.is_file()

    def dir_exists(self, path: Path) -> bool:
        """Check if directory exists.

        Args:
            path: Directory path

        Returns:
            True if directory exists
        """
        return path.is_dir()

    def read_file(
        self,
        path: Path,
        encoding: str = "utf-8",
        default: Optional[str] = None,
    ) -> Optional[str]:
        """Read file content.

        Args:
            path: File path
            encoding: File encoding
            default: Default value if file doesn't exist

        Returns:
            File content or default
        """
        if not path.exists():
            return default
        return path.read_text(encoding=encoding)

    def copy_file(self, src: Path, dst: Path) -> None:
        """Copy file from src to dst.

        Args:
            src: Source file path
            dst: Destination file path
        """
        import shutil
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def remove_file(self, path: Path) -> bool:
        """Remove file if exists.

        Args:
            path: File path

        Returns:
            True if removed, False if didn't exist
        """
        if path.exists():
            path.unlink()
            return True
        return False

    def remove_directory(self, path: Path, recursive: bool = False) -> bool:
        """Remove directory.

        Args:
            path: Directory path
            recursive: Remove contents recursively

        Returns:
            True if removed, False if didn't exist
        """
        import shutil
        if not path.exists():
            return False

        if recursive:
            shutil.rmtree(path)
        else:
            path.rmdir()
        return True
```

## Criterios de Aceptacion
1. [ ] ensure_directory es idempotente
2. [ ] write_file crea directorios padres
3. [ ] append_file no duplica contenido
4. [ ] make_executable funciona correctamente
5. [ ] Todas las operaciones manejan paths que no existen

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test FileSystem
uv run python -c "
from tac_bootstrap.infrastructure.fs import FileSystem
from pathlib import Path
import tempfile

fs = FileSystem()
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)

    # Test ensure_directory
    test_dir = tmp_path / 'a/b/c'
    created = fs.ensure_directory(test_dir)
    print(f'Created: {created}, Exists: {test_dir.exists()}')

    # Test write_file
    test_file = tmp_path / 'test.txt'
    fs.write_file(test_file, 'Hello World')
    print(f'Content: {test_file.read_text()}')

    # Test append_file
    fs.append_file(test_file, 'New line')
    print(f'After append: {test_file.read_text()}')

    # Test make_executable
    script = tmp_path / 'script.sh'
    fs.write_file(script, '#!/bin/bash\\necho hi')
    fs.make_executable(script)
    import os
    print(f'Executable: {os.access(script, os.X_OK)}')

print('All tests passed!')
"
```

## NO hacer
- No agregar funcionalidad de git (eso va en git_adapter)
- No agregar logging complejo
```

---

### TAREA 5.3: Implementar GitAdapter

```markdown
# Prompt para Agente

## Contexto
Necesitamos un adaptador para operaciones Git que se usan durante scaffolding,
como inicializar repositorio, crear commits iniciales, etc.

## Objetivo
Implementar git_adapter.py con operaciones Git basicas.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py`

## Contenido Completo

```python
"""Git adapter for repository operations.

Provides a clean interface for Git operations during scaffolding.
"""
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


@dataclass
class GitResult:
    """Result of a git operation."""
    success: bool
    output: str = ""
    error: str = ""


class GitAdapter:
    """Adapter for Git operations.

    Example:
        git = GitAdapter(repo_path)
        git.init()
        git.add_all()
        git.commit("Initial commit")
    """

    def __init__(self, repo_path: Path):
        """Initialize Git adapter.

        Args:
            repo_path: Path to repository root
        """
        self.repo_path = repo_path

    def _run(self, *args: str, check: bool = True) -> GitResult:
        """Run a git command.

        Args:
            *args: Git command arguments
            check: Raise on non-zero exit

        Returns:
            GitResult with output
        """
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check,
            )
            return GitResult(
                success=result.returncode == 0,
                output=result.stdout.strip(),
                error=result.stderr.strip(),
            )
        except subprocess.CalledProcessError as e:
            return GitResult(
                success=False,
                output=e.stdout.strip() if e.stdout else "",
                error=e.stderr.strip() if e.stderr else str(e),
            )
        except FileNotFoundError:
            return GitResult(
                success=False,
                error="Git is not installed or not in PATH",
            )

    def is_repo(self) -> bool:
        """Check if path is a git repository.

        Returns:
            True if .git exists
        """
        return (self.repo_path / ".git").is_dir()

    def init(self, initial_branch: str = "main") -> GitResult:
        """Initialize a new git repository.

        Args:
            initial_branch: Name of initial branch

        Returns:
            GitResult
        """
        return self._run("init", "-b", initial_branch)

    def add(self, *paths: str) -> GitResult:
        """Stage files for commit.

        Args:
            *paths: Paths to stage (or "." for all)

        Returns:
            GitResult
        """
        return self._run("add", *paths)

    def add_all(self) -> GitResult:
        """Stage all changes.

        Returns:
            GitResult
        """
        return self._run("add", "-A")

    def commit(self, message: str, allow_empty: bool = False) -> GitResult:
        """Create a commit.

        Args:
            message: Commit message
            allow_empty: Allow empty commits

        Returns:
            GitResult
        """
        args = ["commit", "-m", message]
        if allow_empty:
            args.append("--allow-empty")
        return self._run(*args)

    def status(self, porcelain: bool = True) -> GitResult:
        """Get repository status.

        Args:
            porcelain: Use porcelain format

        Returns:
            GitResult with status
        """
        args = ["status"]
        if porcelain:
            args.append("--porcelain")
        return self._run(*args)

    def get_current_branch(self) -> Optional[str]:
        """Get current branch name.

        Returns:
            Branch name or None
        """
        result = self._run("branch", "--show-current", check=False)
        return result.output if result.success else None

    def branch_exists(self, branch: str) -> bool:
        """Check if branch exists.

        Args:
            branch: Branch name

        Returns:
            True if branch exists
        """
        result = self._run("rev-parse", "--verify", branch, check=False)
        return result.success

    def checkout(self, branch: str, create: bool = False) -> GitResult:
        """Checkout a branch.

        Args:
            branch: Branch name
            create: Create branch if doesn't exist

        Returns:
            GitResult
        """
        args = ["checkout"]
        if create:
            args.append("-b")
        args.append(branch)
        return self._run(*args)

    def create_worktree(
        self, path: Path, branch: str, create_branch: bool = True
    ) -> GitResult:
        """Create a git worktree.

        Args:
            path: Path for worktree
            branch: Branch name
            create_branch: Create new branch

        Returns:
            GitResult
        """
        args = ["worktree", "add", str(path)]
        if create_branch:
            args.extend(["-b", branch])
        else:
            args.append(branch)
        return self._run(*args)

    def remove_worktree(self, path: Path, force: bool = False) -> GitResult:
        """Remove a git worktree.

        Args:
            path: Worktree path
            force: Force removal

        Returns:
            GitResult
        """
        args = ["worktree", "remove", str(path)]
        if force:
            args.append("--force")
        return self._run(*args)

    def list_worktrees(self) -> List[str]:
        """List all worktrees.

        Returns:
            List of worktree paths
        """
        result = self._run("worktree", "list", "--porcelain", check=False)
        if not result.success:
            return []

        worktrees = []
        for line in result.output.split("\n"):
            if line.startswith("worktree "):
                worktrees.append(line[9:])
        return worktrees

    def has_changes(self) -> bool:
        """Check if there are uncommitted changes.

        Returns:
            True if there are changes
        """
        result = self.status(porcelain=True)
        return bool(result.output.strip())

    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get URL of a remote.

        Args:
            remote: Remote name

        Returns:
            Remote URL or None
        """
        result = self._run("remote", "get-url", remote, check=False)
        return result.output if result.success else None
```

## Criterios de Aceptacion
1. [ ] is_repo detecta repositorios existentes
2. [ ] init crea nuevo repositorio
3. [ ] add_all y commit funcionan correctamente
4. [ ] Worktree operations funcionan
5. [ ] Errores se manejan gracefully

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test GitAdapter
uv run python -c "
from tac_bootstrap.infrastructure.git_adapter import GitAdapter
from pathlib import Path
import tempfile

with tempfile.TemporaryDirectory() as tmp:
    git = GitAdapter(Path(tmp))

    # Test init
    result = git.init()
    print(f'Init: {result.success}')

    # Test is_repo
    print(f'Is repo: {git.is_repo()}')

    # Test branch
    print(f'Branch: {git.get_current_branch()}')

print('GitAdapter tests passed!')
"
```

## NO hacer
- No implementar push (requiere autenticacion)
- No implementar clone (fuera de scope)
```

---

## FASE 6: Servicio de Deteccion (70-80%)

---

### TAREA 6.1: Implementar DetectService

```markdown
# Prompt para Agente

## Contexto
El comando `add-agentic` necesita auto-detectar el lenguaje, framework y package manager
de un repositorio existente para sugerir configuracion apropiada.

## Objetivo
Implementar DetectService que analiza un repositorio y detecta su stack tecnologico.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`

## Contenido Completo

```python
"""Detection service for existing repositories.

Analyzes repository structure to detect:
- Programming language
- Framework
- Package manager
- Project commands
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import json

from tac_bootstrap.domain.models import Language, Framework, PackageManager


@dataclass
class DetectedProject:
    """Result of project detection."""
    language: Language
    framework: Optional[Framework] = None
    package_manager: PackageManager = PackageManager.PIP
    app_root: Optional[str] = None
    commands: Dict[str, str] = field(default_factory=dict)
    confidence: float = 0.0  # 0-1 confidence score


class DetectService:
    """Service for detecting project configuration.

    Example:
        detector = DetectService()
        detected = detector.detect(Path("/path/to/repo"))
        print(f"Language: {detected.language}")
    """

    def detect(self, repo_path: Path) -> DetectedProject:
        """Detect project configuration from repository.

        Args:
            repo_path: Path to repository root

        Returns:
            DetectedProject with detected settings
        """
        # Detect language first
        language = self._detect_language(repo_path)

        # Detect package manager based on language
        package_manager = self._detect_package_manager(repo_path, language)

        # Detect framework based on language
        framework = self._detect_framework(repo_path, language)

        # Detect app root
        app_root = self._detect_app_root(repo_path, language)

        # Detect commands from config files
        commands = self._detect_commands(repo_path, language, package_manager)

        return DetectedProject(
            language=language,
            framework=framework,
            package_manager=package_manager,
            app_root=app_root,
            commands=commands,
            confidence=0.8,  # TODO: Calculate actual confidence
        )

    def _detect_language(self, repo_path: Path) -> Language:
        """Detect primary programming language.

        Checks for language-specific files in order of priority.
        """
        # Python indicators
        python_files = [
            "pyproject.toml", "setup.py", "requirements.txt",
            "Pipfile", "poetry.lock", "uv.lock"
        ]
        if any((repo_path / f).exists() for f in python_files):
            return Language.PYTHON

        # TypeScript indicators
        ts_files = ["tsconfig.json", "*.ts", "*.tsx"]
        if (repo_path / "tsconfig.json").exists():
            return Language.TYPESCRIPT

        # JavaScript indicators (check after TS)
        js_files = ["package.json"]
        if (repo_path / "package.json").exists():
            # Check if it has TypeScript
            pkg_json = self._read_package_json(repo_path)
            if pkg_json:
                deps = {**pkg_json.get("dependencies", {}),
                        **pkg_json.get("devDependencies", {})}
                if "typescript" in deps:
                    return Language.TYPESCRIPT
            return Language.JAVASCRIPT

        # Go indicators
        if (repo_path / "go.mod").exists():
            return Language.GO

        # Rust indicators
        if (repo_path / "Cargo.toml").exists():
            return Language.RUST

        # Java indicators
        java_files = ["pom.xml", "build.gradle", "build.gradle.kts"]
        if any((repo_path / f).exists() for f in java_files):
            return Language.JAVA

        # Default to Python
        return Language.PYTHON

    def _detect_package_manager(
        self, repo_path: Path, language: Language
    ) -> PackageManager:
        """Detect package manager for language."""
        if language == Language.PYTHON:
            if (repo_path / "uv.lock").exists() or (repo_path / ".python-version").exists():
                return PackageManager.UV
            if (repo_path / "poetry.lock").exists():
                return PackageManager.POETRY
            if (repo_path / "Pipfile.lock").exists():
                return PackageManager.PIPENV
            return PackageManager.PIP

        if language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            if (repo_path / "pnpm-lock.yaml").exists():
                return PackageManager.PNPM
            if (repo_path / "yarn.lock").exists():
                return PackageManager.YARN
            if (repo_path / "bun.lockb").exists():
                return PackageManager.BUN
            return PackageManager.NPM

        if language == Language.GO:
            return PackageManager.GO_MOD

        if language == Language.RUST:
            return PackageManager.CARGO

        if language == Language.JAVA:
            if (repo_path / "pom.xml").exists():
                return PackageManager.MAVEN
            return PackageManager.GRADLE

        return PackageManager.PIP

    def _detect_framework(
        self, repo_path: Path, language: Language
    ) -> Optional[Framework]:
        """Detect web framework."""
        if language == Language.PYTHON:
            # Check pyproject.toml or requirements.txt
            deps = self._get_python_deps(repo_path)
            if "fastapi" in deps:
                return Framework.FASTAPI
            if "django" in deps:
                return Framework.DJANGO
            if "flask" in deps:
                return Framework.FLASK

        if language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            pkg_json = self._read_package_json(repo_path)
            if pkg_json:
                deps = {**pkg_json.get("dependencies", {}),
                        **pkg_json.get("devDependencies", {})}
                if "next" in deps:
                    return Framework.NEXTJS
                if "@nestjs/core" in deps:
                    return Framework.NESTJS
                if "express" in deps:
                    return Framework.EXPRESS
                if "react" in deps:
                    return Framework.REACT
                if "vue" in deps:
                    return Framework.VUE

        if language == Language.GO:
            # Check go.mod for framework imports
            go_mod = repo_path / "go.mod"
            if go_mod.exists():
                content = go_mod.read_text()
                if "gin-gonic/gin" in content:
                    return Framework.GIN
                if "labstack/echo" in content:
                    return Framework.ECHO

        if language == Language.RUST:
            cargo_toml = repo_path / "Cargo.toml"
            if cargo_toml.exists():
                content = cargo_toml.read_text()
                if "axum" in content:
                    return Framework.AXUM
                if "actix" in content:
                    return Framework.ACTIX

        if language == Language.JAVA:
            pom = repo_path / "pom.xml"
            if pom.exists() and "spring" in pom.read_text().lower():
                return Framework.SPRING

        return Framework.NONE

    def _detect_app_root(
        self, repo_path: Path, language: Language
    ) -> Optional[str]:
        """Detect application root directory."""
        # Common patterns
        common_roots = ["src", "app", "lib"]
        for root in common_roots:
            if (repo_path / root).is_dir():
                return root

        # Language-specific
        if language == Language.PYTHON:
            # Look for package directory
            for item in repo_path.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    return item.name

        return "."

    def _detect_commands(
        self,
        repo_path: Path,
        language: Language,
        package_manager: PackageManager,
    ) -> Dict[str, str]:
        """Detect existing project commands."""
        commands = {}

        # Check package.json scripts
        if language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            pkg_json = self._read_package_json(repo_path)
            if pkg_json and "scripts" in pkg_json:
                scripts = pkg_json["scripts"]
                if "start" in scripts or "dev" in scripts:
                    cmd = scripts.get("dev", scripts.get("start"))
                    commands["start"] = f"{package_manager.value} run {cmd.split()[0] if cmd else 'dev'}"
                if "test" in scripts:
                    commands["test"] = f"{package_manager.value} test"
                if "lint" in scripts:
                    commands["lint"] = f"{package_manager.value} run lint"
                if "build" in scripts:
                    commands["build"] = f"{package_manager.value} run build"

        # Check pyproject.toml scripts
        if language == Language.PYTHON:
            pyproject = repo_path / "pyproject.toml"
            if pyproject.exists():
                try:
                    import tomllib
                    with open(pyproject, "rb") as f:
                        data = tomllib.load(f)
                    scripts = data.get("project", {}).get("scripts", {})
                    # Use common script names if defined
                except Exception:
                    pass

        return commands

    def _read_package_json(self, repo_path: Path) -> Optional[dict]:
        """Read and parse package.json."""
        pkg_path = repo_path / "package.json"
        if not pkg_path.exists():
            return None
        try:
            return json.loads(pkg_path.read_text())
        except json.JSONDecodeError:
            return None

    def _get_python_deps(self, repo_path: Path) -> List[str]:
        """Get list of Python dependencies."""
        deps = []

        # Check pyproject.toml
        pyproject = repo_path / "pyproject.toml"
        if pyproject.exists():
            try:
                import tomllib
                with open(pyproject, "rb") as f:
                    data = tomllib.load(f)
                project_deps = data.get("project", {}).get("dependencies", [])
                deps.extend(d.split("[")[0].split(">=")[0].split("==")[0].lower()
                           for d in project_deps)
            except Exception:
                pass

        # Check requirements.txt
        reqs = repo_path / "requirements.txt"
        if reqs.exists():
            for line in reqs.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg = line.split("[")[0].split(">=")[0].split("==")[0]
                    deps.append(pkg.lower())

        return deps
```

## Criterios de Aceptacion
1. [ ] Detecta Python por pyproject.toml, requirements.txt, etc
2. [ ] Detecta TypeScript por tsconfig.json
3. [ ] Detecta package managers correctamente
4. [ ] Detecta frameworks populares (FastAPI, Next.js, etc)
5. [ ] Extrae comandos de package.json scripts

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test on self (this is a Python project)
uv run python -c "
from tac_bootstrap.application.detect_service import DetectService
from pathlib import Path

detector = DetectService()
detected = detector.detect(Path('.'))
print(f'Language: {detected.language}')
print(f'Package Manager: {detected.package_manager}')
print(f'Framework: {detected.framework}')
print(f'App Root: {detected.app_root}')
"
```

## NO hacer
- No usar APIs externas para deteccion
- No analizar contenido de archivos grandes
```

---

## FASE 7: Servicio Doctor (80-90%)

---

### TAREA 7.1: Implementar DoctorService

```markdown
# Prompt para Agente

## Contexto
El comando `doctor` necesita validar que un setup de Agentic Layer esta completo
y funcional. Debe detectar problemas comunes y sugerir correcciones.

## Objetivo
Implementar DoctorService que diagnostica y puede reparar setups de Agentic Layer.

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py`

## Contenido Completo

```python
"""Doctor service for validating Agentic Layer setups.

Performs health checks and can auto-fix common issues.
"""
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Callable
import subprocess


class Severity(str, Enum):
    """Issue severity levels."""
    ERROR = "error"      # Must fix for functionality
    WARNING = "warning"  # Should fix for best results
    INFO = "info"        # Optional improvement


@dataclass
class Issue:
    """A detected issue."""
    severity: Severity
    message: str
    suggestion: Optional[str] = None
    fix_fn: Optional[Callable[[Path], bool]] = None


@dataclass
class DiagnosticReport:
    """Result of diagnostic check."""
    healthy: bool = True
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue) -> None:
        """Add an issue to the report."""
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.healthy = False


@dataclass
class FixResult:
    """Result of attempting fixes."""
    fixed_count: int = 0
    failed_count: int = 0
    messages: List[str] = field(default_factory=list)


class DoctorService:
    """Service for diagnosing and fixing Agentic Layer setups.

    Example:
        doctor = DoctorService()
        report = doctor.diagnose(repo_path)
        if not report.healthy:
            fix_result = doctor.fix(repo_path, report)
    """

    def diagnose(self, repo_path: Path) -> DiagnosticReport:
        """Run all diagnostic checks.

        Args:
            repo_path: Path to repository

        Returns:
            DiagnosticReport with all issues found
        """
        report = DiagnosticReport()

        # Run all checks
        self._check_directory_structure(repo_path, report)
        self._check_claude_config(repo_path, report)
        self._check_commands(repo_path, report)
        self._check_hooks(repo_path, report)
        self._check_adws(repo_path, report)
        self._check_config_yml(repo_path, report)

        return report

    def fix(self, repo_path: Path, report: DiagnosticReport) -> FixResult:
        """Attempt to fix issues in report.

        Args:
            repo_path: Path to repository
            report: Diagnostic report with issues

        Returns:
            FixResult with statistics
        """
        result = FixResult()

        for issue in report.issues:
            if issue.fix_fn:
                try:
                    if issue.fix_fn(repo_path):
                        result.fixed_count += 1
                        result.messages.append(f"Fixed: {issue.message}")
                    else:
                        result.failed_count += 1
                except Exception as e:
                    result.failed_count += 1
                    result.messages.append(f"Failed to fix {issue.message}: {e}")

        return result

    def _check_directory_structure(
        self, repo_path: Path, report: DiagnosticReport
    ) -> None:
        """Check required directories exist."""
        required_dirs = [
            ".claude",
            ".claude/commands",
            ".claude/hooks",
        ]

        for dir_path in required_dirs:
            full_path = repo_path / dir_path
            if not full_path.is_dir():
                report.add_issue(Issue(
                    severity=Severity.ERROR,
                    message=f"Missing required directory: {dir_path}",
                    suggestion=f"Run: mkdir -p {dir_path}",
                    fix_fn=lambda p, d=dir_path: self._fix_create_dir(p, d),
                ))

        # Optional directories (warnings)
        optional_dirs = ["adws", "specs", "scripts"]
        for dir_path in optional_dirs:
            full_path = repo_path / dir_path
            if not full_path.is_dir():
                report.add_issue(Issue(
                    severity=Severity.WARNING,
                    message=f"Missing optional directory: {dir_path}",
                    suggestion=f"Consider creating {dir_path}/ for better organization",
                ))

    def _check_claude_config(
        self, repo_path: Path, report: DiagnosticReport
    ) -> None:
        """Check Claude Code configuration."""
        settings_path = repo_path / ".claude" / "settings.json"

        if not settings_path.exists():
            report.add_issue(Issue(
                severity=Severity.ERROR,
                message="Missing .claude/settings.json",
                suggestion="Run: tac-bootstrap add-agentic . to create configuration",
            ))
            return

        # Validate JSON
        try:
            import json
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError as e:
            report.add_issue(Issue(
                severity=Severity.ERROR,
                message=f"Invalid JSON in settings.json: {e}",
                suggestion="Fix the JSON syntax error",
            ))
            return

        # Check for required fields
        if "permissions" not in settings:
            report.add_issue(Issue(
                severity=Severity.WARNING,
                message="settings.json missing 'permissions' field",
                suggestion="Add permissions configuration for better security",
            ))

    def _check_commands(self, repo_path: Path, report: DiagnosticReport) -> None:
        """Check slash commands exist."""
        commands_dir = repo_path / ".claude" / "commands"
        if not commands_dir.is_dir():
            return  # Already reported in directory check

        # Essential commands
        essential_commands = ["prime.md", "test.md", "commit.md"]
        for cmd in essential_commands:
            cmd_path = commands_dir / cmd
            if not cmd_path.exists():
                report.add_issue(Issue(
                    severity=Severity.WARNING,
                    message=f"Missing essential command: /{cmd.replace('.md', '')}",
                    suggestion="This command is commonly used in workflows",
                ))

        # Check if any commands exist
        md_files = list(commands_dir.glob("*.md"))
        if not md_files:
            report.add_issue(Issue(
                severity=Severity.ERROR,
                message="No slash commands found in .claude/commands/",
                suggestion="Add at least prime.md and test.md",
            ))

    def _check_hooks(self, repo_path: Path, report: DiagnosticReport) -> None:
        """Check hook scripts."""
        hooks_dir = repo_path / ".claude" / "hooks"
        if not hooks_dir.is_dir():
            return

        hook_files = ["pre_tool_use.py", "post_tool_use.py"]
        for hook in hook_files:
            hook_path = hooks_dir / hook
            if hook_path.exists():
                # Check if executable
                import os
                if not os.access(hook_path, os.X_OK):
                    report.add_issue(Issue(
                        severity=Severity.WARNING,
                        message=f"Hook {hook} is not executable",
                        suggestion=f"Run: chmod +x .claude/hooks/{hook}",
                        fix_fn=lambda p, h=hook: self._fix_make_executable(p, h),
                    ))

    def _check_adws(self, repo_path: Path, report: DiagnosticReport) -> None:
        """Check ADW setup."""
        adws_dir = repo_path / "adws"
        if not adws_dir.is_dir():
            return  # Optional, already warned

        # Check for modules
        modules_dir = adws_dir / "adw_modules"
        if not modules_dir.is_dir():
            report.add_issue(Issue(
                severity=Severity.WARNING,
                message="Missing adws/adw_modules/ directory",
                suggestion="ADW workflows need shared modules",
            ))

        # Check for at least one workflow
        workflows = list(adws_dir.glob("adw_*.py"))
        if not workflows:
            report.add_issue(Issue(
                severity=Severity.INFO,
                message="No ADW workflows found",
                suggestion="Consider adding adw_sdlc_iso.py for automated workflows",
            ))

    def _check_config_yml(self, repo_path: Path, report: DiagnosticReport) -> None:
        """Check config.yml exists and is valid."""
        config_path = repo_path / "config.yml"

        if not config_path.exists():
            report.add_issue(Issue(
                severity=Severity.WARNING,
                message="Missing config.yml",
                suggestion="config.yml enables idempotent regeneration with 'tac-bootstrap render'",
            ))
            return

        # Validate YAML
        try:
            import yaml
            config = yaml.safe_load(config_path.read_text())
        except yaml.YAMLError as e:
            report.add_issue(Issue(
                severity=Severity.ERROR,
                message=f"Invalid YAML in config.yml: {e}",
                suggestion="Fix the YAML syntax error",
            ))
            return

        # Check required fields
        if not config:
            report.add_issue(Issue(
                severity=Severity.ERROR,
                message="config.yml is empty",
                suggestion="Run tac-bootstrap add-agentic to regenerate",
            ))
            return

        required_fields = ["project", "commands"]
        for field_name in required_fields:
            if field_name not in config:
                report.add_issue(Issue(
                    severity=Severity.ERROR,
                    message=f"config.yml missing required field: {field_name}",
                    suggestion="Add the missing configuration section",
                ))

    # Fix functions
    def _fix_create_dir(self, repo_path: Path, dir_path: str) -> bool:
        """Fix by creating directory."""
        full_path = repo_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path.is_dir()

    def _fix_make_executable(self, repo_path: Path, hook: str) -> bool:
        """Fix by making hook executable."""
        import os
        import stat
        hook_path = repo_path / ".claude" / "hooks" / hook
        if hook_path.exists():
            current = hook_path.stat().st_mode
            hook_path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            return os.access(hook_path, os.X_OK)
        return False
```

## Criterios de Aceptacion
1. [ ] Detecta directorios faltantes (error vs warning)
2. [ ] Valida JSON de settings.json
3. [ ] Valida YAML de config.yml
4. [ ] Detecta hooks no ejecutables
5. [ ] fix() puede crear directorios y chmod hooks

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test on a directory without agentic layer
uv run python -c "
from tac_bootstrap.application.doctor_service import DoctorService
from pathlib import Path
import tempfile

doctor = DoctorService()

# Test on empty directory
with tempfile.TemporaryDirectory() as tmp:
    report = doctor.diagnose(Path(tmp))
    print(f'Healthy: {report.healthy}')
    print(f'Issues: {len(report.issues)}')
    for issue in report.issues[:5]:
        print(f'  [{issue.severity.value}] {issue.message}')
"
```

## NO hacer
- No intentar fixes que requieran network
- No modificar archivos de usuario sin fix_fn
```

---

## FASE 8: Tests (90-95%)

---

### TAREA 8.1: Tests unitarios completos

```markdown
# Prompt para Agente

## Contexto
Necesitamos tests unitarios para todos los modulos implementados para asegurar
calidad y prevenir regresiones.

## Objetivo
Crear tests unitarios completos para:
- domain/models.py
- domain/plan.py
- application/scaffold_service.py
- application/detect_service.py
- application/doctor_service.py
- infrastructure/template_repo.py
- infrastructure/fs.py

## Archivos a Crear

### 1. `tests/test_models.py`

```python
"""Tests for domain models."""
import pytest
from tac_bootstrap.domain.models import (
    TACConfig,
    ProjectSpec,
    CommandsSpec,
    ClaudeConfig,
    ClaudeSettings,
    Language,
    Framework,
    PackageManager,
    get_frameworks_for_language,
    get_package_managers_for_language,
    get_default_commands,
)


class TestProjectSpec:
    """Tests for ProjectSpec model."""

    def test_name_sanitization(self):
        """Project name should be sanitized."""
        spec = ProjectSpec(
            name="  My Project  ",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        )
        assert spec.name == "my-project"

    def test_empty_name_raises(self):
        """Empty name should raise ValueError."""
        with pytest.raises(ValueError):
            ProjectSpec(
                name="",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            )


class TestTACConfig:
    """Tests for TACConfig model."""

    def test_minimal_config(self):
        """Minimal config should have defaults."""
        config = TACConfig(
            project=ProjectSpec(
                name="test",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test")),
        )
        assert config.version == 1
        assert config.paths.adws_dir == "adws"
        assert config.agentic.provider.value == "claude_code"


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_frameworks_for_python(self):
        """Python should have FastAPI, Django, Flask."""
        frameworks = get_frameworks_for_language(Language.PYTHON)
        assert Framework.FASTAPI in frameworks
        assert Framework.DJANGO in frameworks

    def test_package_managers_for_typescript(self):
        """TypeScript should have pnpm, npm, yarn, bun."""
        managers = get_package_managers_for_language(Language.TYPESCRIPT)
        assert PackageManager.PNPM in managers
        assert PackageManager.NPM in managers

    def test_default_commands_python_uv(self):
        """Python + UV should have correct defaults."""
        commands = get_default_commands(Language.PYTHON, PackageManager.UV)
        assert "uv run pytest" in commands["test"]
        assert "uv run ruff" in commands["lint"]
```

### 2. `tests/test_plan.py`

```python
"""Tests for scaffold plan models."""
import pytest
from tac_bootstrap.domain.plan import (
    ScaffoldPlan,
    FileOperation,
    FileAction,
    DirectoryOperation,
)


class TestScaffoldPlan:
    """Tests for ScaffoldPlan model."""

    def test_empty_plan(self):
        """Empty plan should have zero counts."""
        plan = ScaffoldPlan()
        assert plan.total_directories == 0
        assert plan.total_files == 0

    def test_add_directory_fluent(self):
        """add_directory should return self for chaining."""
        plan = ScaffoldPlan()
        result = plan.add_directory("test", "Test dir")
        assert result is plan
        assert plan.total_directories == 1

    def test_add_file_fluent(self):
        """add_file should return self for chaining."""
        plan = ScaffoldPlan()
        result = plan.add_file("test.txt", FileAction.CREATE)
        assert result is plan
        assert plan.total_files == 1

    def test_chaining(self):
        """Should support method chaining."""
        plan = (
            ScaffoldPlan()
            .add_directory("dir1")
            .add_directory("dir2")
            .add_file("file1.txt")
            .add_file("file2.txt")
        )
        assert plan.total_directories == 2
        assert plan.total_files == 2

    def test_get_files_by_action(self):
        """Should filter files by action."""
        plan = ScaffoldPlan()
        plan.add_file("create.txt", FileAction.CREATE)
        plan.add_file("skip.txt", FileAction.SKIP)
        plan.add_file("patch.txt", FileAction.PATCH)

        assert len(plan.get_files_to_create()) == 1
        assert len(plan.get_files_skipped()) == 1
        assert len(plan.get_files_to_patch()) == 1

    def test_summary(self):
        """Summary should include counts."""
        plan = ScaffoldPlan()
        plan.add_directory("dir")
        plan.add_file("file.txt", FileAction.CREATE)
        plan.add_file("skip.txt", FileAction.SKIP)

        summary = plan.summary
        assert "1 directories" in summary
        assert "1 files to create" in summary
        assert "1 skipped" in summary
```

### 3. `tests/test_scaffold_service.py`

```python
"""Tests for scaffold service."""
import pytest
from pathlib import Path
import tempfile

from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import (
    TACConfig,
    ProjectSpec,
    CommandsSpec,
    ClaudeConfig,
    ClaudeSettings,
    Language,
    PackageManager,
)


@pytest.fixture
def config():
    """Create a test config."""
    return TACConfig(
        project=ProjectSpec(
            name="test-project",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(start="uv run python -m app", test="uv run pytest"),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-project")),
    )


class TestScaffoldService:
    """Tests for ScaffoldService."""

    def test_build_plan_creates_directories(self, config):
        """build_plan should include required directories."""
        service = ScaffoldService()
        plan = service.build_plan(config)

        dir_paths = [d.path for d in plan.directories]
        assert ".claude" in dir_paths
        assert ".claude/commands" in dir_paths
        assert "adws" in dir_paths

    def test_build_plan_creates_files(self, config):
        """build_plan should include required files."""
        service = ScaffoldService()
        plan = service.build_plan(config)

        file_paths = [f.path for f in plan.files]
        assert ".claude/settings.json" in file_paths
        assert "config.yml" in file_paths

    def test_build_plan_marks_scripts_executable(self, config):
        """Script files should be marked executable."""
        service = ScaffoldService()
        plan = service.build_plan(config)

        script_files = [f for f in plan.files if f.path.endswith(".sh")]
        assert all(f.executable for f in script_files)

    def test_apply_plan_creates_structure(self, config):
        """apply_plan should create directories and files."""
        service = ScaffoldService()
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            result = service.apply_plan(plan, Path(tmp), config)

            assert result.success
            assert result.directories_created > 0
            assert result.files_created > 0
            assert (Path(tmp) / ".claude").is_dir()
            assert (Path(tmp) / "config.yml").is_file()
```

### 4. `tests/test_detect_service.py`

```python
"""Tests for detect service."""
import pytest
from pathlib import Path
import tempfile
import json

from tac_bootstrap.application.detect_service import DetectService
from tac_bootstrap.domain.models import Language, PackageManager, Framework


class TestDetectService:
    """Tests for DetectService."""

    def test_detect_python_by_pyproject(self):
        """Should detect Python by pyproject.toml."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").write_text("[project]\nname='test'")
            result = detector.detect(Path(tmp))

            assert result.language == Language.PYTHON

    def test_detect_uv_by_lock(self):
        """Should detect UV by uv.lock."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "uv.lock").touch()
            result = detector.detect(Path(tmp))

            assert result.package_manager == PackageManager.UV

    def test_detect_typescript_by_tsconfig(self):
        """Should detect TypeScript by tsconfig.json."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")
            result = detector.detect(Path(tmp))

            assert result.language == Language.TYPESCRIPT

    def test_detect_nextjs_from_package_json(self):
        """Should detect Next.js framework."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "tsconfig.json").write_text("{}")
            (Path(tmp) / "package.json").write_text(
                json.dumps({"dependencies": {"next": "^14.0.0"}})
            )
            result = detector.detect(Path(tmp))

            assert result.framework == Framework.NEXTJS

    def test_detect_app_root(self):
        """Should detect src as app root."""
        detector = DetectService()

        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "pyproject.toml").touch()
            (Path(tmp) / "src").mkdir()
            result = detector.detect(Path(tmp))

            assert result.app_root == "src"
```

### 5. `tests/test_doctor_service.py`

```python
"""Tests for doctor service."""
import pytest
from pathlib import Path
import tempfile
import json

from tac_bootstrap.application.doctor_service import DoctorService, Severity


class TestDoctorService:
    """Tests for DoctorService."""

    def test_diagnose_empty_directory(self):
        """Empty directory should have errors."""
        doctor = DoctorService()

        with tempfile.TemporaryDirectory() as tmp:
            report = doctor.diagnose(Path(tmp))

            assert not report.healthy
            assert any(i.severity == Severity.ERROR for i in report.issues)

    def test_diagnose_valid_setup(self):
        """Valid setup should be healthy."""
        doctor = DoctorService()

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Create minimal valid structure
            (tmp_path / ".claude" / "commands").mkdir(parents=True)
            (tmp_path / ".claude" / "hooks").mkdir(parents=True)
            (tmp_path / ".claude" / "settings.json").write_text('{"version": 1}')
            (tmp_path / ".claude" / "commands" / "prime.md").write_text("# Prime")
            (tmp_path / ".claude" / "commands" / "test.md").write_text("# Test")
            (tmp_path / ".claude" / "commands" / "commit.md").write_text("# Commit")
            (tmp_path / "config.yml").write_text("project:\n  name: test\ncommands:\n  start: echo")

            report = doctor.diagnose(tmp_path)

            # Should have no errors (may have warnings for optional stuff)
            errors = [i for i in report.issues if i.severity == Severity.ERROR]
            assert len(errors) == 0

    def test_fix_creates_directories(self):
        """fix() should create missing directories."""
        doctor = DoctorService()

        with tempfile.TemporaryDirectory() as tmp:
            report = doctor.diagnose(Path(tmp))
            result = doctor.fix(Path(tmp), report)

            # Should have fixed some directory issues
            assert result.fixed_count > 0
            assert (Path(tmp) / ".claude").is_dir()
```

## Criterios de Aceptacion
1. [ ] Tests para models.py cubren validacion y helpers
2. [ ] Tests para plan.py cubren fluent interface y queries
3. [ ] Tests para scaffold_service cubren build y apply
4. [ ] Tests para detect_service cubren cada lenguaje
5. [ ] Tests para doctor_service cubren diagnose y fix
6. [ ] Coverage > 80%

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Run all tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_models.py -v
```

## NO hacer
- No crear tests de integracion complejos
- No mockear filesystem innecesariamente
```

---

## FASE 9: Documentacion (95-100%)

---

### TAREA 9.1: README y documentacion de uso

```markdown
# Prompt para Agente

## Contexto
TAC Bootstrap necesita documentacion clara para que los usuarios puedan
instalarlo y usarlo efectivamente.

## Objetivo
Crear README.md completo con:
- Descripcion del proyecto
- Instalacion
- Uso de comandos
- Ejemplos
- Configuracion

## Archivo a Crear
`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`

## Contenido Completo

```markdown
# TAC Bootstrap

CLI to bootstrap Agentic Layer for Claude Code with TAC (Tactical Agentic Coding) patterns.

Transform any repository into an AI-assisted development environment in minutes.

## Features

- **Quick Setup**: Add complete agentic layer to any project in minutes
- **Auto-Detection**: Automatically detects language, framework, and package manager
- **Smart Defaults**: Sensible defaults based on your tech stack
- **Idempotent**: Safe to run multiple times without duplicating files
- **Customizable**: Full control via config.yml

## Installation

```bash
# With UV (recommended)
uv tool install tac-bootstrap

# With pip
pip install tac-bootstrap

# From source
git clone https://github.com/your-org/tac-bootstrap
cd tac-bootstrap/tac_bootstrap_cli
uv pip install -e .
```

## Quick Start

### For New Projects

```bash
# Interactive wizard
tac-bootstrap init my-awesome-app

# Non-interactive with options
tac-bootstrap init my-app --language python --framework fastapi --no-interactive
```

### For Existing Projects

```bash
cd your-existing-project

# Interactive (recommended)
tac-bootstrap add-agentic .

# Auto-detect and apply
tac-bootstrap add-agentic . --no-interactive
```

## Commands

### `init`

Create a new project with Agentic Layer.

```bash
tac-bootstrap init <name> [options]

Options:
  -l, --language          Programming language (python, typescript, go, rust, java)
  -f, --framework         Web framework (fastapi, nextjs, etc.)
  -p, --package-manager   Package manager (uv, npm, pnpm, etc.)
  -a, --architecture      Architecture pattern (simple, layered, ddd)
  -o, --output            Output directory
  -i/-I, --interactive    Enable/disable interactive wizard
  --dry-run               Preview without creating files
```

### `add-agentic`

Inject Agentic Layer into existing repository.

```bash
tac-bootstrap add-agentic [path] [options]

Options:
  -i/-I, --interactive    Enable/disable interactive wizard
  -f, --force             Overwrite existing files
  --dry-run               Preview without creating files
```

### `doctor`

Validate Agentic Layer setup.

```bash
tac-bootstrap doctor [path] [options]

Options:
  --fix                   Attempt to fix issues automatically
```

### `render`

Regenerate Agentic Layer from config.yml.

```bash
tac-bootstrap render [config.yml] [options]

Options:
  -o, --output            Output directory
  -f, --force             Overwrite existing files
  --dry-run               Preview without creating files
```

## Generated Structure

After running `tac-bootstrap`, your project will have:

```
project/
├── .claude/
│   ├── settings.json     # Claude Code settings
│   ├── commands/         # Slash commands (/prime, /test, etc.)
│   └── hooks/            # Execution hooks
├── adws/
│   ├── adw_modules/      # Shared workflow modules
│   ├── adw_sdlc_iso.py   # SDLC workflow
│   └── adw_patch_iso.py  # Quick patch workflow
├── scripts/              # Utility scripts
├── specs/                # Feature/bug specifications
├── logs/                 # Execution logs
├── config.yml            # TAC configuration
└── .mcp.json            # MCP server config
```

## Configuration

### config.yml

```yaml
version: 1

project:
  name: "my-app"
  language: "python"
  framework: "fastapi"
  package_manager: "uv"

commands:
  start: "uv run python -m app"
  test: "uv run pytest"
  lint: "uv run ruff check ."

agentic:
  provider: "claude_code"
  model_policy:
    default: "sonnet"
    heavy: "opus"
  worktrees:
    enabled: true
    max_parallel: 5
```

## Workflows

### SDLC Workflow

Complete development lifecycle: Plan → Build → Test → Review → Ship

```bash
uv run adws/adw_sdlc_iso.py --issue 123
```

### Patch Workflow

Quick fixes: Build → Test → Ship

```bash
uv run adws/adw_patch_iso.py --issue 456 --fix "Fix typo in README"
```

## Slash Commands

After setup, use these commands with Claude Code:

| Command | Description |
|---------|-------------|
| `/prime` | Load project context |
| `/start` | Start the application |
| `/test` | Run tests |
| `/feature <desc>` | Plan a new feature |
| `/bug <desc>` | Plan a bug fix |
| `/implement <plan>` | Implement from plan |
| `/commit` | Create git commit |
| `/review <plan>` | Review implementation |

## Requirements

- Python 3.10+
- Git
- Claude Code CLI

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT
```

## Criterios de Aceptacion
1. [ ] README tiene instalacion clara
2. [ ] Todos los comandos documentados con ejemplos
3. [ ] Estructura generada explicada
4. [ ] config.yml documentado
5. [ ] Workflows explicados

## Comandos de Verificacion
```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Check README exists and has content
wc -l README.md
head -50 README.md
```

## NO hacer
- No agregar badges aun (requiere CI setup)
- No documentar features no implementadas
```

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
