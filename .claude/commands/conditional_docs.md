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
