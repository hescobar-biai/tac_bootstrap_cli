# Chore: Enable Skipped Tests in scaffold_service

## Metadata
issue_number: `48`
adw_id: `b408e27f`
issue_json: `{"number":48,"title":"TAREA 7: Habilitar Tests @skip en scaffold_service","body":"**Archivo a modificar:** `tests/test_scaffold_service.py`\n\n**Prompt:**\n```\nRevisa tests/test_scaffold_service.py y habilita los tests marcados con @pytest.mark.skip.\n\nActualmente hay ~15 tests deshabilitados con reason=\"Requires real templates\".\n\nPara cada test @skip:\n1. Analiza qué template necesita\n2. Verifica que el template existe\n3. Si existe, remueve el decorador @skip\n4. Si no existe, documenta cuál falta\n\nLos templates están en: tac_bootstrap/templates/\n\nDespués de habilitar, corre:\nuv run pytest tests/test_scaffold_service.py -v\n\nAsegúrate de que todos los tests pasen.\n```\n\n**Criterios de aceptación:**\n- [ ] Todos los @skip removidos o justificados\n- [ ] Tests pasan después de habilitarlos\n- [ ] Cobertura de scaffold_service > 80%\n"}`

## Chore Description
Actualmente hay 15 tests en `tac_bootstrap_cli/tests/test_scaffold_service.py` marcados con `@pytest.mark.skip(reason="Requires real templates - integration test")`. Estos tests validan la aplicación de planes de scaffold que requieren templates Jinja2 reales.

El sistema de templates ya está implementado en `tac_bootstrap/templates/` con 44 templates .j2 distribuidos en 5 subdirectorios (adws, claude, config, scripts, structure).

Esta chore habilita estos tests de integración verificando que:
1. Los templates requeridos existen en el sistema
2. Los tests pasan correctamente cuando se habilitan
3. Se identifica cualquier template faltante

## Relevant Files
Archivos para completar la chore:

- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests a habilitar (15 tests con @skip)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Servicio bajo test que usa templates
- `tac_bootstrap_cli/tac_bootstrap/templates/` - Directorio con 44 templates Jinja2
  - `claude/*.j2` - Templates de configuración Claude
  - `adws/*.j2` - Templates de workflows ADW
  - `scripts/*.j2` - Templates de scripts shell
  - `config/*.j2` - Templates de configuración
  - `structure/*.j2` - Templates de READMEs
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Repositorio de templates

### New Files
Ningún archivo nuevo requerido.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Auditoría de Tests y Templates
- Leer `tac_bootstrap_cli/tests/test_scaffold_service.py` completamente
- Identificar los 15 tests con `@pytest.mark.skip`
- Listar qué templates usa cada test (basado en scaffold_service.py)
- Verificar existencia de templates en `tac_bootstrap/templates/`
- Crear lista de templates faltantes (si alguno)

### Task 2: Habilitar Tests con Templates Existentes
- Para cada test con @skip:
  - Verificar que todos los templates requeridos existen
  - Si existen, remover el decorador `@pytest.mark.skip`
  - Si no existen, documentar en comentario qué falta
- Remover decoradores solo de tests verificados

### Task 3: Ejecutar Tests Habilitados
- Correr `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v`
- Verificar que todos los tests habilitados pasan
- Si hay fallos, analizar y corregir:
  - Problemas de templates
  - Problemas de paths
  - Problemas de permisos

### Task 4: Validación Final
- Ejecutar suite completa de tests unitarios
- Verificar cobertura de scaffold_service
- Ejecutar comandos de validación
- Confirmar cero regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short` - Tests específicos de scaffold_service
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios completos
- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py --cov=tac_bootstrap.application.scaffold_service --cov-report=term` - Verificar cobertura > 80%
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Todos los templates ya están implementados (44 archivos .j2)
- Los tests fueron marcados como @skip durante desarrollo inicial
- Son tests de integración que requieren filesystem real (usan tempfile)
- El ScaffoldService usa TemplateRepository que carga templates de `tac_bootstrap/templates/`
- Los tests verifican: creación de estructura, rendering de templates, permisos ejecutables, idempotencia, force mode
- Cobertura actual de scaffold_service debe aumentar significativamente al habilitar estos tests
