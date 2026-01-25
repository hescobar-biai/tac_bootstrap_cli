# Chore: Tests para document workflow mejorado

## Metadata
issue_number: `186`
adw_id: `feature_7_3`
issue_json: `{"number":186,"title":"Tarea 7.3: Tests para document workflow mejorado","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_7_3\n\n**Tipo**: chore\n**Ganancia**: Verificar que las mejoras al workflow de documentacion no rompen el flujo existente.\n\n**Instrucciones para el agente**:\n\n1. Agregar tests en tac_bootstrap_cli/tests/test_fractal_docs_templates.py:\n   - test_document_command_has_idk_frontmatter - Template incluye instrucciones de frontmatter\n   - test_adw_document_includes_fractal_step - Workflow template incluye paso de fractal docs\n   - test_adw_document_fractal_is_non_blocking - Fallo no bloquea workflow\n2. Verificar que el template de /document es compatible con el formato actual (no rompe proyectos existentes)\n\n**Criterios de aceptacion**:\n- Tests pasan\n- Templates son backward-compatible\n\n# FASE 7: Document Workflow Mejorado\n\n**Objetivo**: Mejorar el template existente de /document para incluir frontmatter IDK y integracion con docs fractal.\n\n**Ganancia de la fase**: La documentacion de features generada automaticamente es mas rica, consistente, y encontrable por agentes AI.\n"}`

## Chore Description

Esta tarea es de verificación y testing para validar que las mejoras implementadas en Tareas 7.1 y 7.2 funcionan correctamente:

- **Tarea 7.1**: Agregó frontmatter IDK al template `document.md.j2` (líneas 47-61)
- **Tarea 7.2**: Integró fractal docs en `adw_document_iso.py` (líneas 162-180)

Esta chore (7.3) NO implementa nuevas funcionalidades, solo verifica que:
1. El template de /document contiene el frontmatter IDK esperado
2. El workflow template de adw_document incluye el paso de fractal docs
3. El paso de fractal docs está envuelto en try-except para ser no-bloqueante
4. Los templates son backward-compatible (renderizan sin errores)

## Relevant Files

### Archivos de Tests
- `tac_bootstrap_cli/tests/test_fractal_docs_templates.py` - Archivo existente donde se agregarán los 3 tests nuevos

### Templates a Validar
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/document.md.j2` - Template del comando /document (contiene frontmatter IDK en líneas 47-61)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2` - Template del workflow de documentación (contiene integración fractal docs en líneas 162-180)

### Referencias
- `adws/adw_document_iso.py` - Implementación base del workflow (para comparar con template)
- `tac_bootstrap_cli/tests/test_fractal_docs_templates.py` - Tests existentes para usar como patrones

## Step by Step Tasks

### Task 1: Agregar test_document_command_has_idk_frontmatter
Verificar que el template `document.md.j2` contiene el frontmatter IDK con estructura YAML válida.

**Detalles**:
- Renderizar template `claude/commands/document.md.j2` con config de prueba
- Verificar que comienza con `---` (inicio de frontmatter YAML)
- Verificar que contiene campos requeridos: `doc_type`, `adw_id`, `date`, `idk`, `tags`, `related_code`
- Verificar que el YAML es parseable
- Seguir patrón de tests existentes en `TestSlashCommandTemplates`

### Task 2: Agregar test_adw_document_includes_fractal_step
Verificar que el template del workflow `adw_document_iso.py.j2` incluye la llamada a `/generate_fractal_docs`.

**Detalles**:
- Renderizar template `adws/adw_document_iso.py.j2` con config de prueba
- Verificar que el contenido incluye `slash_command="/generate_fractal_docs"`
- Verificar que incluye `args=["changed"]`
- Verificar que incluye `agent_name="fractal_docs_generator"`
- Verificar que el código Python generado es sintácticamente válido usando `ast.parse()`
- Seguir patrón de tests existentes en `TestPythonScriptRendering`

### Task 3: Agregar test_adw_document_fractal_is_non_blocking
Verificar que el paso de fractal docs está envuelto en try-except para manejar fallos sin bloquear el workflow.

**Detalles**:
- Renderizar template `adws/adw_document_iso.py.j2` con config de prueba
- Verificar que el código contiene `try:` seguido de la llamada a fractal docs
- Verificar que contiene `except Exception as e:` o similar
- Verificar que dentro del except hay `logger.warning` (no-bloqueante)
- Verificar que NO hay `raise` sin condiciones dentro del except (asegurar que no re-lanza excepción)
- El código Python debe parsear correctamente con `ast.parse()`

### Task 4: Ejecutar Validation Commands
Correr todos los comandos de validación para asegurar que no hay regresiones.

**Detalles**:
- Ejecutar tests unitarios
- Ejecutar linting
- Ejecutar smoke test del CLI

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestDocumentWorkflowTemplates -v --tb=short` - Tests específicos de document workflow
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Suite completa de tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**Contexto de las Tareas Previas**:
- Tarea 7.1 agregó el frontmatter IDK (doc_type, adw_id, date, idk array, tags, related_code) al template document.md.j2
- Tarea 7.2 integró la llamada a /generate_fractal_docs en adw_document_iso.py dentro de try-except no-bloqueante

**Patrón de Tests**:
- Usar `TemplateRepository.render()` para renderizar templates
- No ejecutar código generado, solo verificar contenido
- Para Python scripts: usar `ast.parse()` para validar sintaxis
- Para YAML: usar `yaml.safe_load()` para validar estructura
- Seguir convenciones de los tests existentes en el archivo

**Backward Compatibility**:
- Los templates son copiados en tiempo de generación (no dinámicos)
- Proyectos viejos mantienen sus templates originales
- Esta mejora solo afecta proyectos nuevos generados con tac-bootstrap
- No se requiere migración de proyectos existentes
