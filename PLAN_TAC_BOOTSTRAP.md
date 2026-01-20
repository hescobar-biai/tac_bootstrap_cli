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

## Plan de Tareas (0-100%)

### FASE 1: Setup del Proyecto (0-10%)

#### Tarea 1.1: Crear estructura base del paquete Python
**Archivos a crear:**
- `tac_bootstrap/pyproject.toml`
- `tac_bootstrap/tac_bootstrap/__init__.py`
- `tac_bootstrap/tac_bootstrap/__main__.py`
- Estructura de directorios: domain/, application/, infrastructure/, interfaces/, templates/

**Criterio de Done:** `uv init` completa, estructura creada

---

#### Tarea 1.2: Configurar dependencias
**Archivo:** `pyproject.toml`

```toml
[project]
name = "tac-bootstrap"
version = "0.1.0"
description = "CLI to bootstrap Agentic Layer for Claude Code"
requires-python = ">=3.10"

dependencies = [
    "typer>=0.9.0",      # CLI framework
    "rich>=13.0.0",      # UI terminal bonita
    "jinja2>=3.0.0",     # Templates parametrizables
    "pydantic>=2.0.0",   # Validacion de config
    "pyyaml>=6.0.0",     # Lectura de YAML
    "gitpython>=3.1.0",  # Operaciones git
]

[project.scripts]
tac-bootstrap = "tac_bootstrap.interfaces.cli:app"
```

**Criterio de Done:** `uv sync` instala dependencias, `tac-bootstrap --help` funciona

---

### FASE 2: Modelos de Dominio (10-20%)

#### Tarea 2.1: Modelos Pydantic para configuracion
**Archivo:** `tac_bootstrap/domain/models.py`

**Modelos a crear:**

```python
# Enums
class Language(str, Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GO = "go"

class Framework(str, Enum):
    FASTAPI = "fastapi"
    DJANGO = "django"
    FLASK = "flask"
    NEXT = "next"
    NEST = "nest"
    EXPRESS = "express"

class Architecture(str, Enum):
    DDD = "ddd"
    CLEAN = "clean"
    HEXAGONAL = "hexagonal"
    LAYERED = "layered"
    SIMPLE = "simple"

class PackageManager(str, Enum):
    UV = "uv"
    POETRY = "poetry"
    PIP = "pip"
    PNPM = "pnpm"
    NPM = "npm"
    BUN = "bun"

# Modelos principales
class ProjectSpec(BaseModel):
    name: str
    mode: Literal["new", "existing"]
    language: Language
    framework: Optional[Framework]
    architecture: Architecture
    package_manager: PackageManager

class CommandsSpec(BaseModel):
    start: str
    build: Optional[str]
    test: str
    lint: Optional[str]
    typecheck: Optional[str]

class TACConfig(BaseModel):
    """Root model - representa config.yml"""
    version: int = 1
    project: ProjectSpec
    paths: PathsSpec
    commands: CommandsSpec
    agentic: AgenticSpec
    claude: ClaudeConfig
```

**Criterio de Done:** config.yml de ejemplo parsea sin errores

---

#### Tarea 2.2: Modelos de plan de scaffolding
**Archivo:** `tac_bootstrap/domain/plan.py`

```python
class FileAction(str, Enum):
    CREATE = "create"
    PATCH = "patch"
    SKIP = "skip"

class FileOperation(BaseModel):
    path: str
    action: FileAction
    template: Optional[str] = None
    content: Optional[str] = None

class ScaffoldPlan(BaseModel):
    directories: List[DirectoryOperation]
    files: List[FileOperation]
```

---

### FASE 3: Sistema de Templates (20-40%)

#### Tarea 3.1: Infraestructura de templates Jinja2
**Archivo:** `tac_bootstrap/infrastructure/template_repo.py`

```python
class TemplateRepository:
    def __init__(self, template_dir: Path = None):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render(self, template_name: str, context: dict) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)
```

---

#### Tarea 3.2: Templates .claude/ (comandos y hooks)
**Directorio:** `tac_bootstrap/templates/claude/`

**Archivos a crear (25+ templates):**

```
templates/claude/
├── settings.json.j2              # Permisos y hooks
├── commands/
│   ├── prime.md.j2               # Priming del agente
│   ├── start.md.j2               # Como correr el stack
│   ├── build.md.j2               # Build/compile
│   ├── test.md.j2                # Tests (feedback loop)
│   ├── feature.md.j2             # Planificacion de features
│   ├── bug.md.j2                 # Planificacion de bugs
│   ├── chore.md.j2               # Tareas de mantenimiento
│   ├── patch.md.j2               # Fixes rapidos
│   ├── implement.md.j2           # Ejecutar un plan
│   ├── commit.md.j2              # Crear commits
│   ├── pull_request.md.j2        # Crear PRs
│   ├── review.md.j2              # Checklist de revision
│   ├── document.md.j2            # Generar documentacion
│   ├── health_check.md.j2        # Validar salud
│   ├── install.md.j2             # Instalar dependencias
│   ├── install_worktree.md.j2    # Crear worktree
│   ├── classify_issue.md.j2      # Clasificar issue
│   ├── resolve_failed_test.md.j2 # Debug tests fallidos
│   ├── test_e2e.md.j2            # Tests E2E
│   └── e2e/
│       ├── test_basic_query.md.j2
│       └── test_complex_query.md.j2
└── hooks/
    ├── pre_tool_use.py.j2        # Validacion pre-ejecucion
    ├── post_tool_use.py.j2       # Logging post-ejecucion
    ├── notification.py.j2
    ├── stop.py.j2
    └── utils/
        └── constants.py.j2
```

**Ejemplo de template `settings.json.j2`:**

```jinja2
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash({{ config.project.package_manager }}:*)",
      "Bash(find:*)",
      "Write",
      "Bash(chmod:*)"
    ],
    "deny": [
      "Bash(git push --force:*)",
      "Bash(rm -rf:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "{{ config.project.package_manager }} run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
      }]
    }]
  }
}
```

---

#### Tarea 3.3: Templates adws/ (workflows y modulos)
**Directorio:** `tac_bootstrap/templates/adws/`

```
templates/adws/
├── README.md.j2
├── adw_modules/
│   ├── __init__.py.j2
│   ├── agent.py.j2           # Claude Code CLI wrapper
│   ├── data_types.py.j2      # Modelos Pydantic
│   ├── git_ops.py.j2         # Operaciones git
│   ├── github.py.j2          # GitHub API
│   ├── state.py.j2           # ADWState persistence
│   ├── utils.py.j2
│   ├── workflow_ops.py.j2    # Orquestacion
│   └── worktree_ops.py.j2    # Git worktrees
├── adw_plan_iso.py.j2        # Planning aislado
├── adw_build_iso.py.j2       # Implementation aislada
├── adw_test_iso.py.j2        # Testing aislado
├── adw_review_iso.py.j2      # Review con screenshots
├── adw_document_iso.py.j2    # Documentacion
├── adw_patch_iso.py.j2       # Fixes rapidos
├── adw_sdlc_iso.py.j2        # SDLC completo (Plan->Build->Test->Review->Ship)
├── adw_sdlc_zte_iso.py.j2    # Zero-Touch Engineering
├── adw_ship_iso.py.j2        # Merge PR
└── adw_triggers/
    ├── trigger_cron.py.j2    # Polling cada N segundos
    └── trigger_webhook.py.j2 # Servidor webhook
```

---

#### Tarea 3.4: Templates auxiliares
**Directorios adicionales:**

```
templates/
├── scripts/
│   ├── start.sh.j2
│   ├── test.sh.j2
│   ├── lint.sh.j2
│   ├── build.sh.j2
│   └── stop_apps.sh.j2
├── config/
│   ├── config.yml.j2         # Fuente de verdad
│   ├── .mcp.json.j2          # MCP servers (Playwright)
│   └── .gitignore.j2
├── prompts/templates/
│   ├── plan.md.j2
│   ├── chore.md.j2
│   ├── feature.md.j2
│   └── review.md.j2
└── structure/
    ├── specs/README.md.j2
    ├── app_docs/README.md.j2
    └── ai_docs/README.md.j2
```

---

### FASE 4: CLI con Typer + Rich (40-55%)

#### Tarea 4.1: Estructura base del CLI
**Archivo:** `tac_bootstrap/interfaces/cli.py`

```python
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="tac-bootstrap",
    help="Bootstrap Agentic Layer for Claude Code with TAC patterns",
)
console = Console()

@app.command()
def init(
    path: Path = typer.Argument(None, help="Directory for new project"),
    name: str = typer.Option(None, "--name", "-n"),
    language: str = typer.Option(None, "--language", "-l"),
    framework: str = typer.Option(None, "--framework", "-f"),
    skip_wizard: bool = typer.Option(False, "--skip-wizard"),
):
    """Create a new project with full Agentic Layer."""
    if not skip_wizard:
        config = run_new_project_wizard(name, language, framework, path)

    service = ScaffoldService()
    service.scaffold_new_project(config)

    console.print(Panel.fit(
        f"[green]Proyecto creado![/green]\n"
        f"cd {config.project.name} && {config.commands.start}",
        title="TAC Bootstrap"
    ))

@app.command("add-agentic")
def add_agentic(
    repo: Path = typer.Option(".", "--repo", "-r"),
    config: Path = typer.Option(None, "--config", "-c"),
    skip_wizard: bool = typer.Option(False, "--skip-wizard"),
):
    """Inject Agentic Layer into existing repository."""
    ...

@app.command()
def doctor(
    repo: Path = typer.Option(".", "--repo", "-r"),
    fix: bool = typer.Option(False, "--fix"),
):
    """Validate Agentic Layer setup."""
    ...

@app.command()
def render(
    config: Path = typer.Argument(...),
    output: Path = typer.Option(".", "--output", "-o"),
    dry_run: bool = typer.Option(False, "--dry-run"),
):
    """Re-generate Agentic Layer from config.yml."""
    ...
```

---

#### Tarea 4.2: Wizard interactivo con Rich
**Archivo:** `tac_bootstrap/interfaces/wizard.py`

```python
from rich.prompt import Prompt, Confirm
from rich.table import Table

def run_new_project_wizard(name, language, framework, path) -> TACConfig:
    """Wizard interactivo para proyecto nuevo."""

    console.print(Panel.fit(
        "[bold blue]TAC Bootstrap - New Project Wizard[/bold blue]"
    ))

    # 1. Nombre del proyecto
    if not name:
        name = Prompt.ask("Nombre del proyecto", default="my-project")

    # 2. Lenguaje
    if not language:
        language = prompt_choice("Lenguaje", [
            ("python", "Python"),
            ("typescript", "TypeScript"),
            ("javascript", "JavaScript"),
            ("go", "Go"),
        ], default="python")

    # 3. Framework (segun lenguaje)
    frameworks = get_frameworks_for_language(language)
    if not framework and frameworks:
        framework = prompt_choice("Framework", frameworks)

    # 4. Arquitectura
    architecture = prompt_choice("Arquitectura", [
        ("simple", "Simple (flat structure)"),
        ("layered", "Layered (controllers/services/repos)"),
        ("ddd", "DDD (domain-driven design)"),
        ("clean", "Clean Architecture"),
        ("hexagonal", "Hexagonal (ports & adapters)"),
    ], default="simple")

    # 5. Package manager
    pkg_managers = get_package_managers_for_language(language)
    pkg_manager = prompt_choice("Package manager", pkg_managers)

    # 6. Comandos (con defaults inteligentes)
    commands = prompt_commands(language, pkg_manager)

    return TACConfig(...)

def prompt_choice(title: str, choices: list, default: str = None) -> str:
    """Muestra opciones en tabla y retorna seleccion."""
    table = Table(show_header=False, box=None)
    for i, (value, display) in enumerate(choices, 1):
        marker = "[green]>[/green]" if value == default else " "
        table.add_row(marker, f"[{i}]", display)

    console.print(f"\n[bold]{title}[/bold]")
    console.print(table)

    selection = Prompt.ask("Selecciona", default="1")
    return choices[int(selection) - 1][0]
```

---

### FASE 5: Servicio de Scaffold (55-70%)

#### Tarea 5.1: ScaffoldService - build_plan
**Archivo:** `tac_bootstrap/application/scaffold_service.py`

```python
class ScaffoldService:
    def __init__(self):
        self.templates = TemplateRepository()
        self.fs = FileSystem()

    def build_plan(self, config: TACConfig) -> ScaffoldPlan:
        """Construye plan de scaffolding."""
        directories = []
        files = []

        # Directorios core
        directories.extend([
            DirectoryOperation(path=".claude/commands"),
            DirectoryOperation(path=".claude/commands/e2e"),
            DirectoryOperation(path=".claude/hooks/utils"),
            DirectoryOperation(path=f"{config.paths.adws_dir}/adw_modules"),
            DirectoryOperation(path=f"{config.paths.adws_dir}/adw_triggers"),
            DirectoryOperation(path=config.paths.prompts_dir),
            DirectoryOperation(path=config.paths.specs_dir),
            DirectoryOperation(path=config.paths.logs_dir),
            DirectoryOperation(path=config.paths.scripts_dir),
            DirectoryOperation(path="agents"),
            DirectoryOperation(path="app_docs"),
            DirectoryOperation(path="ai_docs"),
        ])

        if config.agentic.worktrees.enabled:
            directories.append(DirectoryOperation(path=config.paths.worktrees_dir))

        # Archivos .claude/
        files.extend(self._build_claude_files(config))

        # Archivos adws/
        files.extend(self._build_adw_files(config))

        # Scripts
        files.extend(self._build_script_files(config))

        # Config files
        files.extend(self._build_config_files(config))

        return ScaffoldPlan(directories=directories, files=files)

    def apply_plan(self, config: TACConfig, output_dir: Path):
        """Aplica el plan al filesystem."""
        plan = self.build_plan(config)
        context = {"config": config}

        # Crear directorios
        for dir_op in plan.directories:
            self.fs.ensure_directory(output_dir / dir_op.path)

        # Crear archivos
        for file_op in plan.files:
            if file_op.action == FileAction.CREATE:
                content = self.templates.render(file_op.template, context)
                self.fs.write_file(output_dir / file_op.path, content)

                # Hacer scripts ejecutables
                if file_op.path.endswith(".sh"):
                    self.fs.make_executable(output_dir / file_op.path)
```

---

#### Tarea 5.2: FileSystem operations
**Archivo:** `tac_bootstrap/infrastructure/fs.py`

```python
class FileSystem:
    """Operaciones de filesystem idempotentes."""

    def ensure_directory(self, path: Path) -> bool:
        """Crea directorio si no existe."""
        if path.exists():
            return False
        path.mkdir(parents=True, exist_ok=True)
        return True

    def write_file(self, path: Path, content: str, overwrite: bool = False) -> bool:
        """Escribe archivo. No sobrescribe por defecto."""
        if path.exists() and not overwrite:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return True

    def make_executable(self, path: Path):
        """chmod +x"""
        import stat
        current = path.stat().st_mode
        path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
```

---

### FASE 6: Servicio de Deteccion (70-80%)

#### Tarea 6.1: DetectService
**Archivo:** `tac_bootstrap/application/detect_service.py`

```python
class DetectService:
    """Auto-detecta stack tecnologico de un proyecto."""

    def __init__(self, repo: Path):
        self.repo = repo

    def detect(self) -> Optional[DetectedStack]:
        language = self._detect_language()
        if not language:
            return None

        framework = self._detect_framework(language)
        package_manager = self._detect_package_manager(language)

        return DetectedStack(language, framework, package_manager)

    def _detect_language(self) -> Optional[Language]:
        # Python
        if (self.repo / "pyproject.toml").exists():
            return Language.PYTHON
        if (self.repo / "requirements.txt").exists():
            return Language.PYTHON

        # TypeScript
        if (self.repo / "tsconfig.json").exists():
            return Language.TYPESCRIPT

        # JavaScript/TypeScript via package.json
        if (self.repo / "package.json").exists():
            pkg = self._read_json(self.repo / "package.json")
            if "typescript" in pkg.get("devDependencies", {}):
                return Language.TYPESCRIPT
            return Language.JAVASCRIPT

        # Go
        if (self.repo / "go.mod").exists():
            return Language.GO

        return None

    def _detect_framework(self, language: Language) -> Optional[Framework]:
        if language == Language.PYTHON:
            pyproject = self.repo / "pyproject.toml"
            if pyproject.exists():
                content = pyproject.read_text().lower()
                if "fastapi" in content: return Framework.FASTAPI
                if "django" in content: return Framework.DJANGO
                if "flask" in content: return Framework.FLASK

        elif language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            pkg = self._read_json(self.repo / "package.json") or {}
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps: return Framework.NEXT
            if "@nestjs/core" in deps: return Framework.NEST
            if "express" in deps: return Framework.EXPRESS

        return None

    def _detect_package_manager(self, language: Language) -> PackageManager:
        if language == Language.PYTHON:
            if (self.repo / "uv.lock").exists(): return PackageManager.UV
            if (self.repo / "poetry.lock").exists(): return PackageManager.POETRY
            return PackageManager.PIP

        elif language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
            if (self.repo / "pnpm-lock.yaml").exists(): return PackageManager.PNPM
            if (self.repo / "bun.lockb").exists(): return PackageManager.BUN
            return PackageManager.NPM

        return PackageManager.PIP
```

---

### FASE 7: Servicio Doctor (80-90%)

#### Tarea 7.1: DoctorService
**Archivo:** `tac_bootstrap/application/doctor_service.py`

```python
class DoctorService:
    """Diagnostica y valida setup de Agentic Layer."""

    def diagnose(self) -> DiagnosticReport:
        report = DiagnosticReport()

        # Checks
        report.checks.append(self._check_claude_directory())
        report.checks.append(self._check_settings_json())
        report.checks.append(self._check_claude_commands())
        report.checks.append(self._check_hooks())
        report.checks.append(self._check_config_yml())
        report.checks.append(self._check_adws_directory())
        report.checks.append(self._check_scripts())
        report.checks.append(self._check_git_initialized())

        return report

    def _check_claude_directory(self) -> Check:
        if (self.repo / ".claude").exists():
            return Check("/.claude directory", CheckStatus.PASS, "Existe")
        return Check("/.claude directory", CheckStatus.FAIL, "No encontrado", fixable=True)

    def _check_settings_json(self) -> Check:
        path = self.repo / ".claude" / "settings.json"
        if not path.exists():
            return Check("settings.json", CheckStatus.FAIL, "No encontrado")

        try:
            import json
            data = json.loads(path.read_text())
            if "permissions" in data:
                return Check("settings.json", CheckStatus.PASS, "Valido")
            return Check("settings.json", CheckStatus.WARN, "Falta 'permissions'")
        except:
            return Check("settings.json", CheckStatus.FAIL, "JSON invalido")
```

**Output del doctor:**

```
┌─────────────────────────────────────────────────────────┐
│              TAC Bootstrap Health Check                  │
├──────────────────────┬────────┬─────────────────────────┤
│ Check                │ Status │ Message                 │
├──────────────────────┼────────┼─────────────────────────┤
│ .claude/ directory   │ PASS   │ Directory exists        │
│ settings.json        │ PASS   │ Valid configuration     │
│ .claude/commands/    │ PASS   │ 25 commands found       │
│ .claude/hooks/       │ PASS   │ Hooks configured        │
│ config.yml           │ PASS   │ Valid configuration     │
│ adws/ directory      │ PASS   │ 15 workflows found      │
│ scripts/ directory   │ PASS   │ 5 scripts found         │
│ Git repository       │ PASS   │ Repository initialized  │
└──────────────────────┴────────┴─────────────────────────┘
```

---

### FASE 8: Tests (90-95%)

#### Tarea 8.1: Tests unitarios
**Directorio:** `tests/`

```
tests/
├── conftest.py              # Fixtures comunes
├── test_models.py           # Validacion Pydantic
├── test_template_repo.py    # Renderizado templates
├── test_scaffold_service.py # Generacion de plan
├── test_detect_service.py   # Auto-deteccion
├── test_doctor_service.py   # Diagnosticos
└── test_cli.py              # Comandos CLI
```

**Criterio de Done:** Cobertura > 80%

---

### FASE 9: Documentacion (95-100%)

#### Tarea 9.1: README y docs
**Archivos:**
- `README.md` - Instalacion, quick start, ejemplos
- `docs/configuration.md` - Schema de config.yml
- `docs/commands.md` - Referencia CLI
- `docs/templates.md` - Como extender

---

## Estructura Final Generada

Cuando el usuario ejecute `tac-bootstrap init` o `add-agentic`, se generara:

```
proyecto/
├── .claude/
│   ├── settings.json                 # Permisos y hooks
│   ├── commands/
│   │   ├── prime.md                  # Priming del agente
│   │   ├── start.md                  # Como correr el stack
│   │   ├── build.md                  # Build/compile
│   │   ├── test.md                   # Tests (feedback loop)
│   │   ├── feature.md                # Planificacion features
│   │   ├── bug.md                    # Planificacion bugs
│   │   ├── chore.md                  # Tareas mantenimiento
│   │   ├── patch.md                  # Fixes rapidos
│   │   ├── implement.md              # Ejecutar un plan
│   │   ├── commit.md                 # Crear commits
│   │   ├── pull_request.md           # Crear PRs
│   │   ├── review.md                 # Revision
│   │   ├── document.md               # Documentacion
│   │   ├── health_check.md           # Validar salud
│   │   ├── install.md                # Dependencias
│   │   ├── install_worktree.md       # Crear worktree
│   │   └── e2e/                      # Tests E2E
│   │       ├── test_basic_query.md
│   │       └── test_complex_query.md
│   └── hooks/
│       ├── pre_tool_use.py           # Validacion pre-ejecucion
│       ├── post_tool_use.py          # Logging post-ejecucion
│       ├── notification.py
│       ├── stop.py
│       └── utils/
│           └── constants.py
├── adws/
│   ├── README.md
│   ├── adw_modules/
│   │   ├── agent.py                  # Claude Code CLI wrapper
│   │   ├── data_types.py             # Modelos Pydantic
│   │   ├── git_ops.py
│   │   ├── github.py
│   │   ├── state.py                  # ADWState persistence
│   │   ├── workflow_ops.py           # Orquestacion
│   │   └── worktree_ops.py           # Git worktrees
│   ├── adw_plan_iso.py               # Planning aislado
│   ├── adw_build_iso.py              # Implementation
│   ├── adw_test_iso.py               # Testing
│   ├── adw_review_iso.py             # Review + screenshots
│   ├── adw_document_iso.py           # Documentacion
│   ├── adw_patch_iso.py              # Fixes rapidos
│   ├── adw_sdlc_iso.py               # SDLC completo
│   ├── adw_sdlc_zte_iso.py           # Zero-Touch Engineering
│   ├── adw_ship_iso.py               # Merge PR
│   └── adw_triggers/
│       ├── trigger_cron.py           # Polling
│       └── trigger_webhook.py        # Webhook server
├── prompts/
│   └── templates/
│       ├── plan.md
│       ├── chore.md
│       ├── feature.md
│       └── review.md
├── scripts/
│   ├── start.sh
│   ├── test.sh
│   ├── lint.sh
│   ├── build.sh
│   └── stop_apps.sh
├── specs/                            # Issue specifications
│   └── README.md
├── logs/                             # Session logs
│   └── .gitkeep
├── agents/                           # Agent outputs (auto-generated)
├── trees/                            # Git worktrees (auto-generated)
├── app_docs/                         # App documentation
├── ai_docs/                          # AI-generated docs
├── config.yml                        # Fuente de verdad
├── .mcp.json                         # MCP servers (Playwright)
└── .gitignore
```

---

## Verificacion

### Test 1: Proyecto nuevo
```bash
tac-bootstrap init test-project --language python --framework fastapi
cd test-project
tac-bootstrap doctor
# Debe mostrar todos PASS
```

### Test 2: Proyecto existente
```bash
cd mi-repo-existente
tac-bootstrap add-agentic
tac-bootstrap doctor
```

### Test 3: Idempotencia
```bash
tac-bootstrap render --config config.yml
tac-bootstrap render --config config.yml  # Debe ser identico
```

### Test 4: Tests automatizados
```bash
uv run pytest tests/ -v --cov=tac_bootstrap
# Cobertura > 80%
```

---

## Dependencias entre Tareas

```
FASE 1 (Setup)
    |
    v
FASE 2 (Modelos)
    |
    v
FASE 3 (Templates) ----+
    |                  |
    v                  |
FASE 4 (CLI) <---------+
    |
    v
FASE 5 (Scaffold Service)
    |
    v
FASE 6 (Detect Service)
    |
    v
FASE 7 (Doctor Service)
    |
    v
FASE 8 (Tests)
    |
    v
FASE 9 (Documentacion)
```

---

## Definition of Done (v1)

- [ ] `tac-bootstrap init` crea repo funcional (app minima + agentic layer)
- [ ] `tac-bootstrap add-agentic` injerta agentic layer sin romper app
- [ ] `.claude/commands` operables y coherentes con `config.yml`
- [ ] ADWs SDLC/Patch/PlanImplement ejecutan y escriben logs
- [ ] `doctor` detecta fallas comunes y sugiere fixes
- [ ] Documentacion lista para presentacion a un equipo
- [ ] Tests con cobertura > 80%
