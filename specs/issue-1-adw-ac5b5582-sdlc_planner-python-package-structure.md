# Feature: Crear estructura base del paquete Python para TAC Bootstrap CLI

## Metadata
issue_number: `1`
adw_id: `ac5b5582`
issue_json: `{"number":1,"title":"TAREA 1.1: Crear estructura base del paquete Python","body":"# Prompt para Agente\n\n## Contexto\nEstamos creando una CLI en Python llamada \"tac-bootstrap\" que generara Agentic Layers para proyectos.\nNecesitamos crear la estructura base del paquete Python siguiendo buenas practicas.\n\n## Objetivo\nCrear la estructura de directorios y archivos base para el paquete Python `tac_bootstrap`.\n\n## Ubicacion\nCrear todo dentro de: `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/`\n\n## Archivos a Crear\n\n### 1. `pyproject.toml`\nCrear archivo de configuracion del proyecto con:\n- name: \"tac-bootstrap\"\n- version: \"0.1.0\"\n- description: \"CLI to bootstrap Agentic Layer for Claude Code with TAC patterns\"\n- requires-python: \">=3.10\"\n- Sin dependencias aun (se agregaran en siguiente tarea)\n- Entry point: tac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n\n### 2. `tac_bootstrap/__init__.py`\nArchivo vacio con docstring:\n```python\n\"\"\"TAC Bootstrap - CLI to bootstrap Agentic Layer for Claude Code.\"\"\"\n__version__ = \"0.1.0\"\n```\n\n### 3. `tac_bootstrap/__main__.py`\nEntry point para ejecutar como modulo:\n```python\n\"\"\"Allow running as python -m tac_bootstrap.\"\"\"\nfrom tac_bootstrap.interfaces.cli import app\n\nif __name__ == \"__main__\":\n    app()\n```\n\n### 4. Estructura de directorios\nCrear los siguientes directorios con archivos `__init__.py` vacios:\n- `tac_bootstrap/domain/`\n- `tac_bootstrap/application/`\n- `tac_bootstrap/infrastructure/`\n- `tac_bootstrap/interfaces/`\n- `tac_bootstrap/templates/`\n- `tests/`\n\n### 5. `tac_bootstrap/interfaces/cli.py` (stub inicial)\n```python\n\"\"\"CLI interface for TAC Bootstrap.\"\"\"\nimport typer\n\napp = typer.Typer(\n    name=\"tac-bootstrap\",\n    help=\"Bootstrap Agentic Layer for Claude Code with TAC patterns\",\n    add_completion=False,\n)\n\n@app.command()\ndef version():\n    \"\"\"Show version.\"\"\"\n    from tac_bootstrap import __version__\n    print(f\"tac-bootstrap v{__version__}\")\n\nif __name__ == \"__main__\":\n    app()\n```\n\n## Criterios de Aceptacion\n1. [ ] Directorio `tac_bootstrap_cli/` creado con toda la estructura\n2. [ ] `pyproject.toml` valido y parseable\n3. [ ] Todos los `__init__.py` creados\n4. [ ] Estructura sigue convencion de paquetes Python modernos\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\ntree -I __pycache__\ncat pyproject.toml\n```\n\n## NO hacer\n- No instalar dependencias aun\n- No crear archivos de templates aun\n- No implementar logica de negocio"}`

## Feature Description
Esta feature establece la estructura base del paquete Python `tac_bootstrap_cli` que será el CLI principal del proyecto TAC Bootstrap. El CLI se usará para generar Agentic Layers en proyectos de desarrollo, siguiendo los patrones TAC (Total Agentic Coding). La estructura sigue arquitectura DDD (Domain-Driven Design) con separación clara de responsabilidades entre domain, application, infrastructure e interfaces.

## User Story
As a developer del proyecto TAC Bootstrap
I want to crear la estructura base del paquete Python con todas las convenciones modernas
So that puedo empezar a implementar la lógica del CLI de forma organizada y escalable

## Problem Statement
Actualmente no existe la estructura del paquete Python para el CLI tac-bootstrap. Necesitamos establecer una base sólida que:
- Siga convenciones modernas de empaquetado Python (PEP 621)
- Implemente arquitectura DDD para mantener el código organizado
- Proporcione entry points para ejecutar el CLI
- Sea extensible para futuras funcionalidades

## Solution Statement
Crear una estructura de paquete Python moderna usando:
- `pyproject.toml` con configuración PEP 621 y build system (hatchling)
- Arquitectura DDD con capas domain, application, infrastructure, interfaces
- Entry points configurados para ejecutar como comando `tac-bootstrap` o módulo Python
- CLI stub inicial usando Typer con comando `version` básico
- Directorio de templates separado para los templates Jinja2 futuros
- Directorio tests para pruebas unitarias

## Relevant Files
Archivos necesarios para implementar la feature:

- `PLAN_TAC_BOOTSTRAP.md` - Contiene el plan maestro con todas las tareas, incluyendo esta TAREA 1.1
- `CLAUDE.md` - Guía para agentes que documenta la estructura esperada del proyecto
- `config.yml` - Configuración del proyecto que puede contener configuraciones relevantes

### New Files
Todos los archivos son nuevos bajo `tac_bootstrap_cli/`:

- `tac_bootstrap_cli/pyproject.toml` - Configuración del paquete
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Package root con version
- `tac_bootstrap_cli/tac_bootstrap/__main__.py` - Entry point para módulo
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - Capa de dominio (vacío)
- `tac_bootstrap_cli/tac_bootstrap/application/__init__.py` - Capa de aplicación (vacío)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/__init__.py` - Capa de infraestructura (vacío)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/__init__.py` - Capa de interfaces (vacío)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI stub con Typer
- `tac_bootstrap_cli/tac_bootstrap/templates/__init__.py` - Templates directory (vacío)
- `tac_bootstrap_cli/tests/__init__.py` - Tests directory (vacío)

## Implementation Plan

### Phase 1: Foundation
1. Crear directorio raíz `tac_bootstrap_cli/` en el working directory
2. Crear estructura de subdirectorios siguiendo arquitectura DDD
3. Crear todos los archivos `__init__.py` necesarios

### Phase 2: Core Implementation
1. Crear `pyproject.toml` con configuración completa:
   - Metadata del proyecto (name, version, description)
   - Build system (hatchling)
   - Python version requirement (>=3.10)
   - Dependency: typer
   - Entry point: tac-bootstrap script
2. Crear `__init__.py` del paquete principal con version
3. Crear `__main__.py` para permitir ejecución como módulo
4. Crear `cli.py` stub con Typer y comando version

### Phase 3: Integration
1. Verificar que la estructura sea válida y parseable
2. Ejecutar comandos de verificación (tree, cat)
3. Confirmar que todos los criterios de aceptación se cumplen

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear directorio raíz y estructura DDD
- Crear directorio `tac_bootstrap_cli/` en el working directory actual
- Crear subdirectorio `tac_bootstrap/` como package principal
- Crear subdirectorios para arquitectura DDD:
  - `tac_bootstrap/domain/`
  - `tac_bootstrap/application/`
  - `tac_bootstrap/infrastructure/`
  - `tac_bootstrap/interfaces/`
  - `tac_bootstrap/templates/`
- Crear directorio `tests/` en la raíz del CLI

### Task 2: Crear archivos __init__.py
- Crear `tac_bootstrap/__init__.py` con docstring y __version__ = "0.1.0"
- Crear `tac_bootstrap/domain/__init__.py` (vacío)
- Crear `tac_bootstrap/application/__init__.py` (vacío)
- Crear `tac_bootstrap/infrastructure/__init__.py` (vacío)
- Crear `tac_bootstrap/interfaces/__init__.py` (vacío)
- Crear `tac_bootstrap/templates/__init__.py` (vacío)
- Crear `tests/__init__.py` (vacío)

### Task 3: Crear pyproject.toml
- Crear archivo `tac_bootstrap_cli/pyproject.toml` con:
  - [build-system] usando hatchling
  - [project] con metadata:
    - name = "tac-bootstrap"
    - version = "0.1.0"
    - description = "CLI to bootstrap Agentic Layer for Claude Code with TAC patterns"
    - requires-python = ">=3.10"
    - authors = []
    - dependencies = ["typer"]
  - [project.scripts] con entry point:
    - tac-bootstrap = "tac_bootstrap.interfaces.cli:app"

### Task 4: Crear __main__.py
- Crear `tac_bootstrap/__main__.py` que importa y ejecuta cli:app
- Incluir docstring apropiado

### Task 5: Crear CLI stub
- Crear `tac_bootstrap/interfaces/cli.py` con:
  - Import typer
  - Crear app Typer con name, help, add_completion=False
  - Implementar comando @app.command() version() que imprime versión
  - Incluir __name__ == "__main__" guard

### Task 6: Verificación y validación
- Ejecutar comando tree para verificar estructura
- Verificar que pyproject.toml es parseable
- Ejecutar todos los Validation Commands

## Testing Strategy

### Unit Tests
En esta fase no se requieren tests unitarios ya que solo estamos creando la estructura. Los tests vendrán en fases posteriores cuando haya lógica de negocio que probar.

### Edge Cases
- Verificar que el directorio `tac_bootstrap_cli/` no existe previamente
- Confirmar que todos los paths relativos son correctos
- Validar que pyproject.toml sigue PEP 621

## Acceptance Criteria
1. Directorio `tac_bootstrap_cli/` creado con toda la estructura DDD
2. `pyproject.toml` válido y parseable con build-system, metadata, y entry point
3. Todos los `__init__.py` creados en los lugares correctos
4. `tac_bootstrap/__init__.py` contiene __version__ = "0.1.0"
5. `cli.py` implementa comando version funcional
6. Estructura sigue convención de paquetes Python modernos (PEP 621, DDD)
7. Entry point configurado en [project.scripts]
8. Typer incluido como dependencia

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `tree tac_bootstrap_cli -I __pycache__ -I "*.pyc"` - Verificar estructura
- `cat tac_bootstrap_cli/pyproject.toml` - Validar configuración
- `python -c "import tomli; tomli.load(open('tac_bootstrap_cli/pyproject.toml', 'rb'))"` - Validar pyproject.toml parseable
- `cat tac_bootstrap_cli/tac_bootstrap/__init__.py` - Verificar version
- `ls -la tac_bootstrap_cli/tac_bootstrap/*/` - Verificar todos los __init__.py

## Notes
- La ubicación especificada en el issue (`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/`) es de otra máquina. Crear en `./tac_bootstrap_cli/` relativo al working directory actual
- Aunque el issue dice "Sin dependencias aun", typer debe incluirse porque el código de cli.py lo requiere
- El build backend elegido es hatchling por ser moderno, ligero y compatible con PEP 621
- Esta es la TAREA 1.1 del PLAN_TAC_BOOTSTRAP.md - las siguientes tareas agregarán más dependencias y funcionalidad
- NO instalar el paquete aún con `uv pip install -e .` - eso vendrá en tareas posteriores
- NO crear templates Jinja2 aún - eso es para tareas posteriores
