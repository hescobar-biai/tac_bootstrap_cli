# Conditional Documentation Guide

Esta guía ayuda a determinar qué documentación leer basado en los cambios específicos que necesitas hacer en el codebase de TAC Bootstrap CLI.

## Instructions
- Revisar la tarea que te han asignado
- Verificar cada path de documentación en la sección Conditional Documentation
- Para cada path, evaluar si alguna de las condiciones aplica a tu tarea
  - IMPORTANTE: Solo leer la documentación si alguna condición coincide con tu tarea
- IMPORTANTE: No leer documentación excesivamente. Solo leer si es relevante.

## Conditional Documentation

- PLAN_TAC_BOOTSTRAP.md
  - Conditions:
    - Cuando necesites entender el plan completo de implementación
    - Cuando implementes cualquier tarea del CLI
    - Cuando necesites saber qué fase/tarea trabajar a continuación
    - Cuando necesites entender la arquitectura DDD del CLI

- CLAUDE.md
  - Conditions:
    - Cuando necesites entender cómo los agentes deben trabajar en el proyecto
    - Cuando empieces a trabajar en cualquier tarea del CLI
    - Cuando necesites referencia rápida de comandos y estructura

- config.yml
  - Conditions:
    - Cuando trabajes con configuración del proyecto
    - Cuando necesites entender los paths y comandos configurados
    - Cuando trabajes con el sistema de templates

- README.md
  - Conditions:
    - Cuando necesites entender el propósito del proyecto
    - Cuando necesites saber cómo usar el CLI
    - Al primer contacto con el proyecto

- tac_bootstrap_cli/tac_bootstrap/domain/models.py
  - Conditions:
    - Cuando trabajes con modelos Pydantic
    - Cuando necesites entender TACConfig, ProjectSpec, AgenticSpec
    - Cuando modifiques validación de configuración

- tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - Conditions:
    - Cuando trabajes con generación de archivos
    - Cuando implementes build_plan o apply_plan
    - Cuando necesites entender cómo se crean los archivos

- tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py
  - Conditions:
    - Cuando trabajes con comandos CLI (init, add-agentic, doctor, render)
    - Cuando agregues nuevos comandos
    - Cuando modifiques la interfaz de usuario

- tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py
  - Conditions:
    - Cuando trabajes con el wizard interactivo
    - Cuando modifiques preguntas al usuario
    - Cuando trabajes con Rich para UI de terminal

- tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py
  - Conditions:
    - Cuando trabajes con templates Jinja2
    - Cuando agregues o modifiques templates
    - Cuando necesites entender el sistema de renderizado

- adws/README.md
  - Conditions:
    - Cuando trabajes en el directorio `adws/`
    - Cuando modifiques AI Developer Workflows
    - Cuando necesites entender la estructura de ADWs

- .claude/commands/classify_adw.md
  - Conditions:
    - Cuando agregues o elimines archivos `adws/adw_*.py`

- prompts/templates/*.md
  - Conditions:
    - Cuando trabajes con templates de prompts
    - Cuando modifiques formatos de plan, feature, bug, o review

- app_docs/feature-e5a04ca0-python-package-structure.md
  - Conditions:
    - Cuando necesites entender la estructura base del paquete Python
    - Cuando trabajes con la arquitectura DDD del CLI
    - Cuando necesites referencia sobre configuración de pyproject.toml
    - Cuando necesites entender los entry points del CLI

- app_docs/feature-e29f22c3-configure-project-dependencies.md
  - Conditions:
    - Cuando trabajes con dependencias del proyecto (pyproject.toml)
    - Cuando configures herramientas de desarrollo (ruff, mypy, pytest)
    - Cuando necesites entender las dependencias de producción instaladas
    - Cuando trabajes con gitpython para operaciones Git
    - Cuando necesites referencia sobre configuraciones de linting y type checking

- app_docs/feature-e80a5f17-pydantic-config-models.md
  - Conditions:
    - Cuando trabajes con los modelos Pydantic de configuración
    - Cuando necesites entender TACConfig y sus sub-modelos (ProjectSpec, PathsSpec, CommandsSpec, AgenticSpec, etc.)
    - Cuando implementes validación de configuración
    - Cuando uses los helper functions (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
    - Cuando necesites referencia de enums (Language, Framework, Architecture, PackageManager)
    - Cuando trabajes con el wizard interactivo y necesites defaults contextuales
    - Cuando implementes carga/guardado de config.yml

- app_docs/feature-72bb26fe-scaffolding-plan-models.md
  - Conditions:
    - Cuando trabajes con modelos de plan de scaffolding
    - Cuando necesites entender FileAction, FileOperation, DirectoryOperation, ScaffoldPlan
    - Cuando implementes ScaffoldService.build_plan() o apply_plan()
    - Cuando necesites construir planes de operaciones de archivos/directorios
    - Cuando trabajes con preview/dry-run de generación de proyectos
    - Cuando necesites query methods para filtrar operaciones por tipo (create, overwrite, patch, skip)
    - Cuando uses fluent interface para construcción de planes

- app_docs/feature-d2f77c7a-jinja2-template-infrastructure.md
  - Conditions:
    - Cuando trabajes con el sistema de templates Jinja2
    - Cuando necesites entender TemplateRepository y sus métodos
    - Cuando uses filtros personalizados (snake_case, kebab_case, pascal_case)
    - Cuando implementes generación de archivos desde templates
    - Cuando trabajes con render(), render_string(), template_exists(), list_templates()
    - Cuando necesites manejar excepciones de templates (TemplateNotFoundError, TemplateRenderError)
    - Cuando trabajes en TAREA 3.2 (copiar templates base) o TAREA 3.3 (TemplateGeneratorService)

- app_docs/feature-d30e0391-claude-templates.md
  - Conditions:
    - Cuando trabajes con templates de configuración Claude (.claude/)
    - Cuando necesites entender los templates de settings.json y comandos slash
    - Cuando modifiques o agregues comandos en templates/claude/commands/
    - Cuando trabajes con parametrización de permisos y hooks de Claude Code
    - Cuando necesites referencia sobre variables TACConfig usadas en templates Claude
    - Cuando implementes generación de .claude/ en proyectos target
    - Cuando trabajes en TAREA 3.3 (hooks templates) o comandos slash personalizados

- app_docs/feature-fbc4585b-claude-hooks-templates.md
  - Conditions:
    - Cuando trabajes con templates de hooks de Claude Code
    - Cuando necesites entender pre_tool_use.py, post_tool_use.py, stop.py templates
    - Cuando modifiques validación de comandos peligrosos o forbidden paths
    - Cuando trabajes con logging de tool usage o session cleanup
    - Cuando necesites entender la estructura de logs de sesión
    - Cuando implementes generación de .claude/hooks/ en proyectos target
    - Cuando trabajes con hooks de safety y auditoría

- app_docs/feature-f0f4ea73-adw-templates.md
  - Conditions:
    - Cuando trabajes con templates de ADWs (AI Developer Workflows)
    - Cuando necesites entender los templates de adw_modules/ (agent.py, state.py, git_ops.py, workflow_ops.py)
    - Cuando modifiques o agregues workflows (adw_sdlc_iso.py, adw_patch_iso.py)
    - Cuando trabajes con triggers automaticos (adw_triggers/)
    - Cuando necesites entender el patrón de worktree isolation
    - Cuando trabajes con state management y persistencia de workflows
    - Cuando implementes model selection logic (HEAVY_COMMANDS)
    - Cuando necesites referencia sobre variables TACConfig usadas en templates ADW
    - Cuando implementes generación de adws/ en proyectos target

- app_docs/feature-feff53ac-scripts-config-templates.md
  - Conditions:
    - Cuando trabajes con templates de scripts bash (start.sh, test.sh, lint.sh, build.sh)
    - Cuando necesites entender templates de configuración (config.yml, .mcp.json, .gitignore)
    - Cuando modifiques o agregues templates en templates/scripts/ o templates/config/
    - Cuando trabajes con templates de documentación de estructura (specs/README.md, app_docs/README.md, ai_docs/README.md)
    - Cuando necesites entender convenciones de templates Jinja2 (enums con .value, booleans con | lower)
    - Cuando implementes renderizado de archivos de configuración del proyecto
    - Cuando necesites referencia sobre variables TACConfig usadas en templates de scripts/config
    - Cuando trabajes con conditional rendering de comandos opcionales (lint, build, typecheck)

- app_docs/feature-a83dbd52-implement-main-cli-commands.md
  - Conditions:
    - Cuando trabajes con los comandos CLI principales (init, add-agentic, doctor, render, version)
    - Cuando necesites entender la estructura completa de la interfaz CLI de TAC Bootstrap
    - Cuando modifiques o agregues comandos CLI usando Typer
    - Cuando trabajes con Rich para formateo de output en terminal (paneles, colores)
    - Cuando necesites entender cómo integrar con ScaffoldService, DetectService, DoctorService (placeholder services)
    - Cuando implementes dry-run mode o force flags en comandos
    - Cuando trabajes con manejo de errores y mensajes de usuario en CLI
    - Cuando necesites referencia sobre argumentos, opciones y help text de comandos
    - Cuando implementes wizard interactivo (interactive mode) en comandos
    - Cuando trabajes con validación de paths, carga de YAML, o construcción de TACConfig desde CLI

- app_docs/feature-ede93862-interactive-wizard.md
  - Conditions:
    - Cuando trabajes con el wizard interactivo implementado con Rich UI
    - Cuando necesites entender la integración del wizard con comandos CLI (init, add-agentic)
    - Cuando modifiques o extiendas el flujo de configuración interactiva
    - Cuando necesites referencia sobre run_init_wizard() o run_add_agentic_wizard()
    - Cuando trabajes con selección de opciones numeradas y defaults contextuales
    - Cuando implementes nuevas preguntas o pasos en el wizard
    - Cuando necesites entender el patrón de confirmación y preview de configuración
    - Cuando trabajes con modo interactive vs non-interactive en CLI
    - Cuando necesites referencia sobre UI patterns con Rich (tablas, paneles, prompts coloridos)

- app_docs/feature-c9d3ab60-scaffold-service-build-plan.md
  - Conditions:
    - Cuando trabajes con ScaffoldService.build_plan() o apply_plan()
    - Cuando necesites entender la orquestación de construcción de planes de scaffolding
    - Cuando trabajes con métodos privados de construcción (_add_directories, _add_claude_files, _add_adw_files, etc.)
    - Cuando necesites entender la lógica de acciones de archivos basada en existing_repo flag
    - Cuando implementes manejo de idempotencia (CREATE, SKIP, OVERWRITE, PATCH)
    - Cuando trabajes con ApplyResult y tracking de estadísticas de scaffolding
    - Cuando necesites entender la integración entre ScaffoldService y TemplateRepository/FileSystem
    - Cuando modifiques la lista de archivos generados (comandos, hooks, workflows, scripts)
    - Cuando necesites referencia sobre template context y rendering
    - Cuando trabajes en TAREA 5.1 o features relacionadas con aplicación de planes

- app_docs/feature-b6479a0a-filesystem-operations.md
  - Conditions:
    - Cuando trabajes con el módulo FileSystem en infrastructure/fs.py
    - Cuando necesites entender operaciones de filesystem idempotentes (ensure_directory, append_file)
    - Cuando implementes creación, lectura, escritura o eliminación de archivos/directorios
    - Cuando trabajes con permisos de archivos (make_executable)
    - Cuando necesites entender la integración de FileSystem con ScaffoldService
    - Cuando modifiques operaciones de filesystem en apply_plan()
    - Cuando necesites referencia sobre manejo de edge cases (archivos faltantes, directorios padre)
    - Cuando trabajes con operaciones cross-platform usando pathlib.Path
    - Cuando implementes funcionalidad que requiera append sin duplicación

- app_docs/feature-8a2e9cbb-git-adapter.md
  - Conditions:
    - Cuando trabajes con el módulo GitAdapter en infrastructure/git_adapter.py
    - Cuando necesites realizar operaciones Git durante scaffolding o ADWs
    - Cuando implementes operaciones de repositorio (init, is_repo, add, commit)
    - Cuando trabajes con branches (checkout, branch_exists, get_current_branch)
    - Cuando necesites gestionar worktrees (create_worktree, remove_worktree, list_worktrees)
    - Cuando trabajes con status de repositorio (status, has_changes)
    - Cuando necesites integrar GitAdapter con ScaffoldService o workflows ADW
    - Cuando necesites entender el manejo de errores de Git (GitResult dataclass)
    - Cuando implementes operaciones de remote (get_remote_url)
    - Cuando necesites referencia sobre uso de subprocess para comandos Git

- app_docs/feature-3b39c634-detect-service.md
  - Conditions:
    - Cuando trabajes con el módulo DetectService en application/detect_service.py
    - Cuando necesites auto-detectar el stack tecnológico de un repositorio
    - Cuando implementes detección de lenguaje (Python, TypeScript, JavaScript, Go, Rust, Java)
    - Cuando trabajes con detección de package managers (uv, pip, poetry, npm, pnpm, yarn, bun, cargo, maven, gradle)
    - Cuando necesites detectar frameworks (FastAPI, Django, Flask, Next.js, NestJS, Express, React, Vue, Gin, Echo, Axum, Actix, Spring)
    - Cuando implementes detección de app root directory o comandos de proyecto
    - Cuando integres DetectService con WizardService para pre-poblar defaults en add-agentic
    - Cuando necesites entender parsing defensivo de package.json, pyproject.toml, requirements.txt
    - Cuando trabajes con helpers (_read_package_json, _get_python_deps)
    - Cuando necesites referencia sobre manejo de compatibilidad Python 3.10/3.11 con tomllib/tomli

- app_docs/feature-7f57eb36-doctor-service.md
  - Conditions:
    - Cuando trabajes con el módulo DoctorService en application/doctor_service.py
    - Cuando necesites validar setups de Agentic Layer (health checks)
    - Cuando implementes el comando tac-bootstrap doctor
    - Cuando trabajes con diagnósticos de directorios, configuración, hooks, o ADWs
    - Cuando necesites auto-fix de issues comunes (directorios faltantes, hooks no ejecutables)
    - Cuando trabajes con modelos de diagnóstico (Issue, DiagnosticReport, FixResult, Severity)
    - Cuando implementes checks de JSON/YAML (settings.json, config.yml)
    - Cuando necesites entender validación de estructura de proyecto
    - Cuando trabajes con permisos de archivos y executability checks
    - Cuando necesites referencia sobre patrón de auto-fix con callbacks fix_fn
