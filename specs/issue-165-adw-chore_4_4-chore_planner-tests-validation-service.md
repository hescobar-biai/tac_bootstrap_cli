# Chore: Tests para ValidationService

## Metadata
issue_number: `165`
adw_id: `chore_4_4`
issue_json: `{"number":165,"title":"Tarea 4.4: Tests para validation","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_4_4\n\n***Tipo**: chore\n**Ganancia**: Cobertura de todas las reglas de validacion.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tests/test_validation_service.py`\n2. Tests:\n   - Combinaciones validas pasan\n   - Combinaciones invalidas fallan con mensaje correcto\n   - Template validation detecta templates faltantes\n   - Filesystem validation detecta directorio no-escribible\n   - Multiples errores se reportan juntos\n   - Warnings no bloquean\n\n**Criterios de aceptacion**:\n- `uv run pytest tests/test_validation_service.py` pasa\n- Cada regla de compatibilidad tiene al menos un test positivo y uno negativo\n# FASE 4: Multi-layer Validation\n\n**Objetivo**: Validar en multiples capas antes de aplicar cambios al filesystem.\n\n**Ganancia de la fase**: Errores detectados temprano con mensajes claros. Evita generar archivos parciales que luego fallan en runtime.\n\n---"}`

## Chore Description
Crear suite de tests unitarios completa para el ValidationService que valida configuraciones de TAC Bootstrap en múltiples capas (domain, template, filesystem, git). Los tests deben cubrir todas las reglas de compatibilidad framework-language-architecture, validación de templates, permisos de filesystem, y warnings de git que no bloquean la ejecución.

## Relevant Files

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py` - Servicio de validación completo con matrices de compatibilidad y validación multi-capa
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Modelos Pydantic (TACConfig, Language, Framework, Architecture)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository usado por ValidationService
- `tac_bootstrap_cli/tests/test_template_repo.py` - Tests existentes que sirven como patrón para fixtures y estructura

### New Files
- `tac_bootstrap_cli/tests/test_validation_service.py` - Nueva suite de tests para ValidationService

## Step by Step Tasks

### Task 1: Crear archivo de tests y fixtures básicos
- Crear `tac_bootstrap_cli/tests/test_validation_service.py`
- Importar ValidationService, ValidationResult, ValidationIssue, ValidationLevel
- Importar modelos del dominio: TACConfig, Language, Framework, Architecture, PackageManager
- Crear fixture `mock_template_repo` que retorne un mock de TemplateRepository
- Crear fixture `validation_service` que instancie ValidationService con mock_template_repo
- Crear fixture `sample_valid_config` con configuración válida (FastAPI + Python + Layered)

### Task 2: Tests de compatibilidad Framework-Language
- Clase `TestFrameworkLanguageCompatibility`
- Test positivo: framework + language compatible pasan validación (ej: FastAPI + Python)
- Test negativo: framework + language incompatible fallan (ej: FastAPI + JavaScript)
  - Verificar mensaje de error contiene framework y language
  - Verificar suggestion contiene lista de languages válidos
- Test con al menos 5 combinaciones positivas (una por categoría de framework)
- Test con al menos 5 combinaciones negativas
- Test con Framework.NONE acepta todos los languages

### Task 3: Tests de compatibilidad Framework-Architecture
- Clase `TestFrameworkArchitectureCompatibility`
- Test positivo: framework + architecture compatible pasan (ej: FastAPI + DDD)
- Test negativo: framework + architecture incompatible fallan (ej: Django + DDD)
  - Verificar mensaje de error contiene framework y architecture
  - Verificar suggestion contiene lista de architectures válidas
- Test con al menos 5 combinaciones positivas
- Test con al menos 5 combinaciones negativas
- Test con Framework.NONE solo acepta Architecture.SIMPLE

### Task 4: Tests de validación de templates
- Clase `TestTemplateValidation`
- Configurar mock_template_repo para simular templates existentes/faltantes
- Test positivo: critical templates existen, validación pasa
  - Mock `template_exists()` retorna True para `claude/settings.json.j2` y `claude/hooks/user_prompt_submit.py.j2`
- Test negativo: critical template faltante
  - Mock `template_exists()` retorna False para uno de los templates críticos
  - Verificar ValidationLevel.TEMPLATE en issue
  - Verificar mensaje contiene nombre del template faltante
- Test ambos templates faltantes genera 2 issues

### Task 5: Tests de validación de filesystem
- Clase `TestFilesystemValidation`
- Usar fixture `tmp_path` de pytest
- Test positivo: directorio no existe pero parent es escribible
- Test negativo: directorio no escribible
  - Crear directorio con `tmp_path`, remover permisos write con `os.chmod(dir, 0o555)`
  - Verificar error con ValidationLevel.FILESYSTEM
  - Restaurar permisos en teardown con `os.chmod(dir, 0o755)`
- Test negativo: directorio existe con .tac_config.yaml
  - Crear `output_dir/.tac_config.yaml`
  - Verificar error menciona conflicto
- Test negativo: parent directory no existe
- Test negativo: parent directory no escribible

### Task 6: Tests de validación de git (warnings)
- Clase `TestGitValidation`
- Test warning: git no instalado (mock `shutil.which("git")` retorna None)
  - Verificar issue con severity='warning'
  - Verificar ValidationLevel.GIT
  - Verificar `result.valid` es True (warnings no bloquean)
- Test warning: repositorio con cambios sin commit
  - Requiere mock de GitAdapter o crear git repo temporal
  - Verificar warning sobre uncommitted changes
  - Verificar result.valid es True
- Test sin warning: git instalado, repo limpio

### Task 7: Tests de acumulación de múltiples errores
- Clase `TestMultipleErrors`
- Test combinando 3 errores simultáneos:
  - Framework-language incompatible
  - Framework-architecture incompatible
  - Template faltante
- Verificar `result.valid = False`
- Verificar `len(result.issues) == 3`
- Verificar `len(result.errors()) == 3`
- Verificar cada issue tiene level, severity, message correcto

### Task 8: Tests de método validate_pre_scaffold
- Clase `TestPreScaffoldValidation`
- Test integración completa: validación pasa con config válida, output_dir válido, templates existentes
- Test integración: falla con múltiples capas (config inválida + filesystem problem)
- Verificar que warnings de git se incluyen pero no afectan result.valid

### Task 9: Tests de ValidationResult helpers
- Clase `TestValidationResult`
- Test `errors()` filtra solo issues con severity='error'
- Test `warnings()` filtra solo issues con severity='warning'
- Test lista mixta de 3 errors + 2 warnings retorna correctamente

### Task 10: Ejecutar validación y documentar cobertura
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py -v --tb=short`
- Verificar todos los tests pasan
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py --cov=tac_bootstrap.application.validation_service --cov-report=term`
- Documentar cobertura alcanzada (objetivo: >90%)
- Ejecutar suite completa de tests para verificar cero regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py -v --tb=short` - Tests nuevos
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Suite completa sin regresiones
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**Matrices de compatibilidad a testear:**

Framework-Language (líneas 160-182 de validation_service.py):
- FASTAPI → Python
- DJANGO → Python
- EXPRESS → TypeScript, JavaScript
- NESTJS → TypeScript
- GIN → Go
- AXUM → Rust
- SPRING → Java
- NONE → todos

Framework-Architecture (líneas 185-211 de validation_service.py):
- FASTAPI → SIMPLE, LAYERED, DDD, CLEAN, HEXAGONAL
- DJANGO → SIMPLE, LAYERED (NO DDD!)
- NESTJS → LAYERED, DDD, CLEAN
- NONE → solo SIMPLE

**Templates críticos a validar:**
- `claude/settings.json.j2`
- `claude/hooks/user_prompt_submit.py.j2`

**Patron de test existente (test_template_repo.py):**
- Usar fixtures para infraestructura (repos, directories)
- Datos de test inline en cada test
- Organizar en clases por categoría funcional
- Nombres descriptivos con docstrings
