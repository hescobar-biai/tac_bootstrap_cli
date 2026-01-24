# Chore: Aplicar IDK docstrings al CLI

## Metadata
issue_number: `167`
adw_id: `chore_5_2`
issue_json: `{"number":167,"title":"Tarea 5.2: Aplicar IDK docstrings al CLI","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_5_2\n\n**Tipo**: chore\n**Ganancia**: Cada modulo del CLI tiene docstrings con Information Dense Keywords, facilitando que agentes AI encuentren el codigo relevante por busqueda semantica.\n\n**Instrucciones para el agente**:\n\n1. Agregar IDK docstrings a los modulos principales del CLI:\n   - `scaffold_service.py`:\n     ```python\n     \"\"\"\n     IDK: scaffold-service, plan-builder, code-generation, template-rendering, file-operations\n     Responsibility: Builds scaffold plans from TACConfig and applies them to filesystem\n     Invariants: Plans are idempotent, templates must exist, output directory must be writable\n     \"\"\"\n     ```\n   - `detect_service.py`:\n     ```python\n     \"\"\"\n     IDK: detect-service, auto-detection, tech-stack, language-detection, framework-detection\n     Responsibility: Auto-detects project technology stack from existing files\n     Invariants: Detection is read-only, never modifies files, returns confidence scores\n     \"\"\"\n     ```\n   - Aplicar a: `generate_service.py`, `validation_service.py`, `doctor_service.py`, `upgrade_service.py`, `template_repo.py`, `fs.py`, `git_adapter.py`\n2. Formato IDK:\n   - `IDK:` 5-12 keywords en kebab-case\n   - `Responsibility:` 1 linea\n   - `Invariants:` Condiciones que siempre se cumplen\n3. NO agregar docstrings a funciones/metodos internos, solo a modulos y clases publicas\n\n**Criterios de aceptacion**:\n- Todos los modulos de application/ e infrastructure/ tienen IDK docstring\n- Keywords son relevantes y no-redundantes\n- No se modifico logica, solo docstrings\n- \n# FASE 5: Value Objects y IDK Docstrings\n\n**Objetivo**: Mejorar la calidad del codigo del CLI con value objects tipados y documentacion estandarizada.\n\n**Ganancia de la fase**: Codigo mas mantenible, menos bugs por strings invalidos, y documentacion que facilita la busqueda semantica por agentes AI.\n"}`

## Chore Description
Agregar IDK (Information Dense Keywords) docstrings a todos los modulos y clases publicas en `application/` e `infrastructure/` del CLI TAC Bootstrap. Los IDK docstrings facilitan que agentes AI encuentren codigo relevante mediante busqueda semantica, usando un formato estandarizado de tres lineas: keywords, responsabilidad, e invariantes.

El formato IDK es:
```python
"""
IDK: keyword-1, keyword-2, keyword-3, keyword-4, keyword-5, keyword-6
Responsibility: One-line description of what this module/class does
Invariants: Operational constraints that always hold true
"""
```

## Relevant Files
Archivos que necesitan IDK docstrings:

### Application Services
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Servicio principal de scaffolding, construye y aplica planes
- `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py` - Deteccion automatica de tech stack
- `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py` - Generacion de entidades/templates
- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py` - Validacion de configuracion y pre-scaffold
- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py` - Diagnostico y health checks
- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - Upgrade de proyectos existentes
- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py` - Generacion de entidades DDD
- `tac_bootstrap_cli/tac_bootstrap/application/exceptions.py` - Excepciones de aplicacion

### Infrastructure
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Repositorio de templates Jinja2
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` - Operaciones de filesystem
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py` - Operaciones de Git

### New Files
Ninguno - solo se agregan/actualizan docstrings

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Agregar IDK docstrings a application/scaffold_service.py
- Reemplazar el docstring del modulo con formato IDK
- Keywords: `scaffold-service, plan-builder, code-generation, template-rendering, file-operations, idempotency`
- Responsibility: `Builds scaffold plans from TACConfig and applies them to filesystem`
- Invariants: `Plans are idempotent, templates must exist, output directory must be writable`
- Agregar IDK docstring a clase `ScaffoldService`
- Keywords: `plan-execution, template-application, directory-creation, validation-gate`
- Responsibility: `Orchestrates scaffold plan building and application with pre-validation`
- Invariants: `Validates before applying, tracks operation statistics, handles errors gracefully`
- Agregar IDK docstring a clase `ApplyResult`
- Keywords: `operation-result, statistics-tracking, error-reporting`
- Responsibility: `Tracks scaffold application statistics and errors`
- Invariants: `Success is false when errors exist, counters are always non-negative`

### Task 2: Agregar IDK docstrings a application/detect_service.py
- Reemplazar el docstring del modulo con formato IDK
- Keywords: `detect-service, auto-detection, tech-stack, language-detection, framework-detection, package-manager`
- Responsibility: `Auto-detects project technology stack from existing files`
- Invariants: `Detection is read-only, never modifies files, returns confidence scores`
- Agregar IDK docstring a clase `DetectService`
- Keywords: `stack-analysis, dependency-parsing, file-inspection`
- Responsibility: `Analyzes repository to identify language, framework, package manager, and commands`
- Invariants: `All detection methods are pure functions, defaults to Python if unknown`
- Agregar IDK docstring a clase `DetectedProject`
- Keywords: `detection-result, confidence-scoring, tech-metadata`
- Responsibility: `Contains detected technology stack with confidence score`
- Invariants: `Confidence is between 0-1, language is always set, framework may be None`

### Task 3: Agregar IDK docstrings a application/generate_service.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo (6-8 keywords basados en responsabilidad)
- Keywords sugeridos: `code-generation, entity-creation, template-instantiation, ddd-scaffolding`
- Agregar IDK docstrings a todas las clases publicas

### Task 4: Agregar IDK docstrings a application/validation_service.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `validation-service, config-validation, pre-scaffold-checks, template-verification`
- Agregar IDK docstrings a todas las clases publicas

### Task 5: Agregar IDK docstrings a application/doctor_service.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `health-check, diagnostics, project-analysis, configuration-validation`
- Agregar IDK docstrings a todas las clases publicas

### Task 6: Agregar IDK docstrings a application/upgrade_service.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `upgrade-service, migration, config-update, backward-compatibility`
- Agregar IDK docstrings a todas las clases publicas

### Task 7: Agregar IDK docstrings a application/entity_generator_service.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `entity-generation, ddd-entities, code-scaffolding, template-based-generation`
- Agregar IDK docstrings a todas las clases publicas

### Task 8: Agregar IDK docstrings a application/exceptions.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `exception-hierarchy, error-types, validation-errors, domain-exceptions`
- Agregar IDK docstrings a todas las clases de excepciones publicas

### Task 9: Agregar IDK docstrings a infrastructure/template_repo.py
- Reemplazar el docstring del modulo con formato IDK
- Keywords: `template-repository, jinja2-rendering, case-conversion, template-discovery`
- Responsibility: `Manages Jinja2 template loading, rendering, and custom filters`
- Invariants: `Templates are immutable, rendering is idempotent, filters are stateless`
- Agregar IDK docstring a clase `TemplateRepository`
- Keywords: `template-management, jinja2-environment, filter-registration`
- Responsibility: `Loads and renders Jinja2 templates with custom case conversion filters`
- Invariants: `Templates dir exists, filters are registered at init, rendering never modifies templates`

### Task 10: Agregar IDK docstrings a infrastructure/fs.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `filesystem-operations, file-io, directory-creation, safe-writes`
- Agregar IDK docstrings a todas las clases publicas

### Task 11: Agregar IDK docstrings a infrastructure/git_adapter.py
- Leer archivo primero para entender su contenido
- Agregar IDK docstring al modulo
- Keywords sugeridos: `git-operations, repository-management, git-commands, version-control`
- Agregar IDK docstrings a todas las clases publicas

### Task 12: Validacion y testing
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check .`
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verificar que todos los tests pasan
- Verificar que no hay errores de linting
- Confirmar que el CLI funciona correctamente

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Solo modificar docstrings a nivel de modulo y clase, NO agregar docstrings a metodos/funciones
- Apuntar a 6-8 keywords por docstring, rango aceptable 5-12
- Keywords deben estar ordenados por importancia (responsabilidad primaria primero)
- Evitar redundancia semantica entre keywords
- Usar el formato de tres lineas consistentemente: IDK, Responsibility, Invariants
- Esta chore no debe modificar ninguna logica de codigo, solo documentacion
- Si un modulo necesita >12 keywords, es señal de que tiene demasiadas responsabilidades (documentar pero no refactorizar en esta tarea)
