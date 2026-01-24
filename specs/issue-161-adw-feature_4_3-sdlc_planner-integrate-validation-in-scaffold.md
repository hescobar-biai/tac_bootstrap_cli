# Feature: Integrate Pre-Scaffold Validation in ScaffoldService

## Metadata
issue_number: `161`
adw_id: `feature_4_3`
issue_json: `{"number":161,"title":"Tarea 4.3: Integrar validacion en scaffold","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_4_3\n\n**Tipo**: feature\n**Ganancia**: El CLI valida ANTES de generar archivos, evitando estados parciales.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n2. En `apply_plan()`, agregar al inicio:\n   ```python\n   validation = self.validation_service.validate_pre_scaffold(config, output_dir)\n   if not validation.valid:\n       raise ScaffoldValidationError(validation)\n   if validation.warnings():\n       for warning in validation.warnings():\n           console.print(f\"[yellow]Warning: {warning.message}[/yellow]\")\n   ```\n3. Definir `ScaffoldValidationError` que formatea los issues en un mensaje legible\n\n**Criterios de aceptacion**:\n- Init con combinacion invalida muestra error ANTES de crear archivos\n- Warnings se muestran pero no bloquean\n- Error message incluye todas las issues y sugerencias\n- \n# FASE 4: Multi-layer Validation\n\n**Objetivo**: Validar en multiples capas antes de aplicar cambios al filesystem.\n\n**Ganancia de la fase**: Errores detectados temprano con mensajes claros. Evita generar archivos parciales que luego fallan en runtime.\n\n---"}`

## Feature Description
Esta feature integra la validación multi-capa en el punto crítico antes de que ScaffoldService comience a generar archivos. El ValidationService ya existe y provee validación completa de configuración, templates, filesystem y git. Esta tarea integra esa validación en `apply_plan()` para garantizar que todas las verificaciones pasen ANTES de crear cualquier archivo en disco.

La feature también define `ScaffoldValidationError`, una excepción personalizada de la capa de aplicación que convierte los resultados de validación estructurados del dominio en mensajes de error claros y accionables para usuarios del CLI.

## User Story
As a CLI user
I want to receive clear validation errors before any files are created
So that I can fix configuration issues without ending up with partial/broken project structures

## Problem Statement
Actualmente, ScaffoldService.apply_plan() comienza a crear archivos inmediatamente sin validar la configuración. Esto puede resultar en estados parciales si la configuración tiene errores (framework incompatible con language, templates faltantes, directorios sin permisos de escritura, etc.).

El usuario no descubre estos problemas hasta después de que algunos archivos ya se crearon, dejando el output_dir en un estado inconsistente que debe limpiarse manualmente.

ValidationService ya implementa todas las validaciones necesarias (issue #159), pero no está integrado en el flujo de scaffolding.

## Solution Statement
Integrar ValidationService.validate_pre_scaffold() al inicio de ScaffoldService.apply_plan(). Este método ya ejecuta todas las validaciones necesarias en las capas DOMAIN, TEMPLATE, FILESYSTEM y GIT.

Si hay errores (validation.valid == False), lanzar ScaffoldValidationError con un mensaje formateado que incluya todos los issues y sugerencias. Si solo hay warnings, imprimirlos a consola pero continuar con la generación.

Esto garantiza fail-fast: errores detectados antes de crear archivos, mensajes claros para debugging, y estado limpio del filesystem si algo falla.

## Relevant Files
Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:560-672` - apply_plan() method donde se agregará la validación
- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py:412-446` - validate_pre_scaffold() method que ejecuta todas las validaciones
- `tac_bootstrap_cli/tac_bootstrap/domain/validation.py` - ValidationResult, ValidationIssue models (si existen en domain layer, revisar)
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests existentes de ScaffoldService que se extenderán

### New Files
- `tac_bootstrap_cli/tac_bootstrap/application/exceptions.py` - Define ScaffoldValidationError y otras excepciones de aplicación

## Implementation Plan

### Phase 1: Foundation
Crear el módulo de excepciones de aplicación con ScaffoldValidationError que formatea ValidationResult en mensajes legibles.

### Phase 2: Core Implementation
Integrar ValidationService en ScaffoldService constructor y llamar validate_pre_scaffold() al inicio de apply_plan(). Manejar errors vs warnings apropiadamente.

### Phase 3: Integration
Agregar tests de integración que verifiquen que configuraciones inválidas bloquean la generación de archivos y que los mensajes de error son claros.

## Step by Step Tasks

### Task 1: Create application/exceptions.py module
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/application/exceptions.py`
- Definir clase base `ApplicationError(Exception)` para excepciones de aplicación
- Definir `ScaffoldValidationError(ApplicationError)` que acepta `ValidationResult` en constructor
- Implementar `__str__()` que formatea el mensaje en formato multi-línea:
  ```
  Validation failed with X error(s):
  1. [DOMAIN] Framework fastapi is not compatible with language rust
     → Use one of these languages with fastapi: python
  2. [TEMPLATE] Required template not found: settings.json.j2
     → Ensure template exists at /path/to/templates/settings.json.j2

  Suggestions:
  - Use one of these languages with fastapi: python
  - Ensure template exists at /path/to/templates/settings.json.j2
  ```
- El formato debe incluir header con conteo, lista numerada con severity y level, mensajes claros, y sección de suggestions

### Task 2: Add ValidationService to ScaffoldService
- Modificar `ScaffoldService.__init__()` para aceptar `validation_service: Optional[ValidationService] = None`
- Si no se provee, crear instancia con `ValidationService(self.template_repo)`
- Almacenar en `self.validation_service`
- ValidationService es dependencia requerida - no usar fallbacks silenciosos

### Task 3: Integrate validation at start of apply_plan()
- En `scaffold_service.py:apply_plan()`, agregar validación ANTES de la línea 578 (antes de metadata registration)
- Importar Rich Console para warnings: `from rich.console import Console`
- Crear console instance: `console = Console()`
- Ejecutar: `validation = self.validation_service.validate_pre_scaffold(config, output_dir)`
- Si `not validation.valid`: `raise ScaffoldValidationError(validation)`
- Si `validation.warnings()`: iterar y print cada warning con formato: `console.print(f"[yellow]Warning: {warning.message}[/yellow]")`
- Los warnings NO bloquean la ejecución, solo informan al usuario

### Task 4: Add unit tests for ScaffoldValidationError
- Crear `tac_bootstrap_cli/tests/test_application_exceptions.py`
- Test 1: `test_scaffold_validation_error_formats_single_error` - verifica formato con 1 error
- Test 2: `test_scaffold_validation_error_formats_multiple_errors` - verifica formato con múltiples errors
- Test 3: `test_scaffold_validation_error_includes_suggestions` - verifica sección de suggestions
- Test 4: `test_scaffold_validation_error_shows_severity_and_level` - verifica que [DOMAIN], [TEMPLATE], etc. aparecen
- Usar ValidationResult mock con diferentes combinaciones de issues

### Task 5: Add integration tests for validation blocking
- En `test_scaffold_service.py`, agregar clase `TestScaffoldServiceValidation`
- Test 1: `test_apply_plan_fails_on_invalid_framework_language` - FastAPI + Rust debe lanzar ScaffoldValidationError ANTES de crear archivos
- Test 2: `test_apply_plan_shows_warnings_but_continues` - Git warnings se muestran pero no bloquean (mock git unavailable)
- Test 3: `test_apply_plan_error_includes_all_issues` - Config con múltiples errores muestra todos en el mensaje
- Test 4: `test_apply_plan_no_files_created_on_validation_failure` - Verificar que output_dir queda vacío si validación falla
- Usar tmp_path fixture y captura de output para verificar warnings

### Task 6: Update existing tests to inject ValidationService
- Revisar tests existentes en `test_scaffold_service.py`
- Si algún test crea ScaffoldService directamente, verificar que no se rompa con el nuevo parámetro opcional
- Los tests que usan configs válidos deben seguir funcionando sin cambios (ValidationService auto-creado)
- Agregar comentarios donde sea relevante sobre la validación automática

### Task 7: Run Validation Commands
- Ejecutar: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Verificar que todos los tests pasen, incluyendo los nuevos
- Ejecutar: `cd tac_bootstrap_cli && uv run ruff check .`
- Ejecutar: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Ejecutar: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Todos los comandos deben completar sin errores

## Testing Strategy

### Unit Tests
- `test_application_exceptions.py`: Validar formato de ScaffoldValidationError con diferentes ValidationResult inputs
- `test_scaffold_service.py`: Validar que ValidationService se integra correctamente en constructor
- Mock ValidationService para aislar lógica de ScaffoldService de validación real

### Integration Tests
- Crear configuraciones inválidas reales (FastAPI + Rust, Django + Hexagonal, etc.)
- Verificar que `apply_plan()` lanza ScaffoldValidationError con mensaje legible
- Verificar que NO se crean archivos en output_dir cuando validación falla
- Capturar stdout/stderr para verificar warnings se imprimen correctamente
- Usar configs con solo warnings (git unavailable) para verificar que generación continúa

### Edge Cases
- ValidationService no inicializado (debe crearse automáticamente)
- ValidationResult sin errors ni warnings (debe continuar sin output)
- ValidationResult con solo warnings (debe imprimir y continuar)
- ValidationResult con múltiples errors de diferentes niveles (DOMAIN, TEMPLATE, FILESYSTEM)
- Output_dir sin permisos de escritura (debe fallar con mensaje claro)
- Parent directory inexistente (debe fallar con sugerencia de mkdir -p)

## Acceptance Criteria
- `tac-bootstrap init` con framework/language incompatible muestra error ANTES de crear archivos
- Mensaje de error incluye TODAS las issues encontradas, no solo la primera
- Mensaje de error incluye suggestions accionables para cada issue
- Warnings (git unavailable, uncommitted changes) se muestran en amarillo pero NO bloquean generación
- Error message formateado incluye severity levels ([ERROR]) y validation layers ([DOMAIN], [TEMPLATE], etc.)
- Si validación falla, output_dir permanece en estado original (sin archivos nuevos)
- Tests verifican que ningún archivo se crea cuando hay validation errors
- Todos los tests existentes de ScaffoldService continúan pasando sin modificación

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios e integración
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test del CLI

## Notes
- ScaffoldValidationError es una excepción de APPLICATION layer que traduce domain ValidationResult a formato user-facing
- No agregar logging por ahora (YAGNI) - solo console output para warnings
- No agregar formato JSON para errors - solo human-readable (CLI tool)
- La validación de configuración debe ejecutarse ANTES de validar filesystem para fail-fast en errores lógicos (más baratos de detectar)
- ValidationService.validate_pre_scaffold() ya existe y ejecuta TODAS las validaciones necesarias - solo integrarlo
- Rich Console ya está disponible en el proyecto - usarlo para warnings coloreados
- Auto-Resolved Clarifications confirman: exceptions.py en application/, formato multi-línea, warnings() retorna lista de ValidationIssue, solo console print (no logging), validation_service es dependencia requerida
