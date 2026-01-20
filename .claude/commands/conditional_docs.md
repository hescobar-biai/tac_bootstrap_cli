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
