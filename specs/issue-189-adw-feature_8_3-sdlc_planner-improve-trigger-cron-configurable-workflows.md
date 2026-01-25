# Feature: Mejorar trigger_cron.py con deteccion de workflows configurable

## Metadata
issue_number: `189`
adw_id: `feature_8_3`
issue_json: `{"number":189,"title":"Tarea 8.3: Mejorar trigger_cron.py con deteccion de workflows configurable","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_8_3\n\n**Tipo**: feature\n**Estado**: COMPLETADA\n**Ganancia**: El trigger cron ahora soporta todos los ADW workflows (igual que el webhook), con intervalo de polling configurable via argumento CLI. Ya no esta limitado a un solo workflow hardcodeado.\n\n**Instrucciones para el agente**:\n\n1. Reescribir `adws/adw_triggers/trigger_cron.py` con:\n   - Argumento CLI `--interval` / `-i` para configurar intervalo de polling (default: 20s)\n   - Deteccion de workflows usando `extract_adw_info()` de `adw_modules.workflow_ops` (misma logica que webhook)\n   - Soporte para TODOS los workflows en `AVAILABLE_ADW_WORKFLOWS`\n   - Validacion de workflows dependientes (requieren ADW ID existente)\n   - Gestion de estado con `ADWState`\n   - Comentarios en issues al detectar/lanzar workflows\n   - Proteccion anti-loop con `ADW_BOT_IDENTIFIER`\n   - Logger por ADW ID con `setup_logger()`\n   - Lanzamiento de workflows en background con `subprocess.Popen`\n\n2. Actualizar template Jinja2 `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`:\n   - Usar `{{ config.project.name }}` en docstring y mensajes\n   - Usar `{{ config.agentic.cron_interval | default(20) }}` como intervalo por defecto\n   - Mantener toda la logica de deteccion identica al archivo renderizado\n\n**Archivos creados/modificados**:\n- `adws/adw_triggers/trigger_cron.py` (renderizado en raiz)\n- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2` (template)\n\n**Criterios de aceptacion**:\n- `uv run adws/adw_triggers/trigger_cron.py --help` muestra ayuda con todos los workflows soportados\n- `uv run adws/adw_triggers/trigger_cron.py -i 30` inicia con intervalo de 30s\n- Detecta `adw_plan_iso`, `adw_sdlc_iso`, `adw_patch_iso` y todos los demas workflows\n- Valida que workflows dependientes (build, test, review, document, ship) requieren ADW ID\n- Publica comentario en issue al detectar workflow\n- No re-procesa comentarios ya procesados\n- Ignora comentarios del bot (anti-loop)\n- Template usa variables de config correctamente\n"}`

## Feature Description
Esta feature mejora el trigger cron (`trigger_cron.py`) para que soporte la detección y lanzamiento de TODOS los workflows ADW disponibles (no solo uno hardcodeado), usando la misma lógica de detección que el webhook trigger. Adicionalmente, permite configurar el intervalo de polling mediante un argumento CLI.

El trigger cron es un sistema que monitorea GitHub issues periódicamente (polling) buscando comandos de workflow ADW en el cuerpo del issue o en comentarios. Cuando encuentra un comando válido, lanza el workflow correspondiente en background.

## User Story
As a TAC Bootstrap CLI user
I want the cron trigger to support all available ADW workflows with configurable polling interval
So that I can use any workflow with automated detection without being limited to a single workflow, and I can adjust polling frequency based on my needs

## Problem Statement
El trigger cron actual (`adws/adw_triggers/trigger_cron.py`) ya está implementado pero debe:
1. Usar el intervalo de polling configurado vía CLI (`--interval` / `-i`)
2. Detectar workflows usando `extract_adw_info()` (mismo método que webhook)
3. Soportar todos los workflows en `AVAILABLE_ADW_WORKFLOWS`
4. Validar workflows dependientes que requieren ADW ID
5. Gestionar estado con `ADWState`
6. Prevenir loops con `ADW_BOT_IDENTIFIER`

El template Jinja2 debe mantenerse sincronizado con la lógica del archivo renderizado.

## Solution Statement
Verificar que tanto el archivo renderizado (`adws/adw_triggers/trigger_cron.py`) como el template Jinja2 (`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`) tienen la implementación correcta:

1. **Argumento CLI configurable**: `--interval` / `-i` con default configurable
2. **Detección unificada**: usar `extract_adw_info()` como webhook
3. **Soporte completo**: todos los workflows de `AVAILABLE_ADW_WORKFLOWS`
4. **Validación de dependencias**: workflows que requieren ADW ID existente
5. **Gestión de estado**: actualizar/crear `ADWState` correctamente
6. **Anti-loop**: ignorar comentarios del bot
7. **Variables de template**: usar `{{ config.project.name }}` y `{{ config.agentic.cron_interval | default(20) }}`

## Relevant Files
Archivos clave para esta feature:

### Archivos existentes
- `adws/adw_triggers/trigger_cron.py` - Implementación renderizada (ya existe)
- `adws/adw_triggers/trigger_webhook.py` - Referencia para la lógica de detección
- `adws/adw_modules/workflow_ops.py` - Función `extract_adw_info()` y `AVAILABLE_ADW_WORKFLOWS`
- `adws/adw_modules/state.py` - Gestión de estado ADW
- `adws/adw_modules/github.py` - Funciones de GitHub y `ADW_BOT_IDENTIFIER`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2` - Template Jinja2

### Files no se crean archivos nuevos
No se crean archivos nuevos - solo se verifica/actualiza el template existente.

## Implementation Plan

### Phase 1: Verificación del archivo renderizado
1. Leer `adws/adw_triggers/trigger_cron.py` y verificar que:
   - Tiene argumento CLI `--interval` / `-i` con default 20s
   - Usa `extract_adw_info()` para detectar workflows
   - Lista `DEPENDENT_WORKFLOWS` coincide con webhook
   - Gestión de estado con `ADWState` es correcta
   - Anti-loop con `ADW_BOT_IDENTIFIER` funciona
   - Lanzamiento con `subprocess.Popen` en background

### Phase 2: Actualización del template Jinja2
1. Comparar template con archivo renderizado
2. Asegurar que usa variables de configuración:
   - `{{ config.project.name }}` en docstrings y mensajes
   - `{{ config.agentic.cron_interval | default(20) }}` como default del intervalo
3. Mantener lógica idéntica al renderizado (excepto variables config)

### Phase 3: Validación
1. Ejecutar tests de validación
2. Verificar que template genera código correcto
3. Confirmar criterios de aceptación

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verificar implementación del archivo renderizado
- Leer `adws/adw_triggers/trigger_cron.py`
- Confirmar que tiene:
  - Argumento CLI `--interval` / `-i` con default
  - Uso de `extract_adw_info()` en `check_issue_for_workflow()`
  - Lista `DEPENDENT_WORKFLOWS` para validación
  - Gestión de `ADWState` en `trigger_workflow()`
  - Protección anti-loop con `ADW_BOT_IDENTIFIER`
  - Background launch con `subprocess.Popen`
- Comparar con `trigger_webhook.py` para verificar consistencia

### Task 2: Verificar/actualizar template Jinja2
- Leer `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`
- Verificar uso de variables config:
  - `{{ config.project.name }}` en líneas 12, 306, 332
  - `{{ config.agentic.cron_interval | default(20) }}` en líneas 21, 57
  - DEFAULT_INTERVAL usa la variable config (línea 57)
- Asegurar que la lógica es idéntica al renderizado
- Si faltan variables config, actualizar el template

### Task 3: Validar template con test de rendering
- Crear un test que renderice el template con valores de config
- Verificar que el output tiene:
  - Nombre del proyecto interpolado
  - Intervalo default interpolado
  - Toda la lógica de detección presente
- Confirmar que pasa linting y type check

### Task 4: Ejecutar Validation Commands
Ejecutar todos los comandos para validar con cero regresiones.

## Testing Strategy

### Unit Tests
No se requieren tests unitarios adicionales - el trigger cron ya está funcionando en producción.

Se debe crear un test de rendering para el template:
```python
def test_trigger_cron_template_rendering():
    """Verify trigger_cron.py template renders correctly with config variables."""
    config = {
        "project": {"name": "TestProject"},
        "agentic": {"cron_interval": 30}
    }
    # Render template
    # Verify project name appears in docstring
    # Verify interval appears as default
    # Verify all workflow detection logic is present
```

### Edge Cases
- Config sin `agentic.cron_interval` debe usar default 20
- Template debe manejar nombres de proyecto con caracteres especiales
- Verificar que comentarios del bot son ignorados correctamente

## Acceptance Criteria
1. ✅ `uv run adws/adw_triggers/trigger_cron.py --help` muestra:
   - Descripción del comando
   - Argumento `-i` / `--interval`
   - Lista completa de workflows soportados de `AVAILABLE_ADW_WORKFLOWS`

2. ✅ `uv run adws/adw_triggers/trigger_cron.py -i 30` inicia con intervalo de 30s:
   - Muestra mensaje "Polling interval: 30 seconds"
   - Ejecuta ciclos cada 30s

3. ✅ Detecta todos los workflows:
   - `adw_plan_iso`, `adw_sdlc_iso`, `adw_patch_iso`
   - `adw_build_iso`, `adw_test_iso`, `adw_review_iso`
   - `adw_document_iso`, `adw_ship_iso`
   - Workflows compuestos: `adw_plan_build_iso`, etc.

4. ✅ Valida workflows dependientes:
   - Workflows en `DEPENDENT_WORKFLOWS` requieren ADW ID
   - Publica mensaje de error si no se proporciona ADW ID
   - No lanza workflow si falta ADW ID requerido

5. ✅ Publica comentario en issue al detectar workflow:
   - Comentario incluye ADW ID
   - Comentario incluye nombre del workflow
   - Comentario incluye model_set
   - Comentario incluye ruta de logs

6. ✅ No re-procesa comentarios:
   - Mantiene registro de comment_id procesados
   - Skip comentarios ya vistos

7. ✅ Ignora comentarios del bot:
   - Detecta `ADW_BOT_IDENTIFIER` en comentarios
   - No procesa comentarios del bot
   - Previene loops infinitos

8. ✅ Template usa variables de config:
   - `{{ config.project.name }}` aparece en docstring y mensajes
   - `{{ config.agentic.cron_interval | default(20) }}` define DEFAULT_INTERVAL
   - Rendering produce código funcional

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `uv run adws/adw_triggers/trigger_cron.py --help` - Smoke test del trigger
- `uv run pytest adws/adw_tests/test_triggers.py -v` - Tests de triggers (si existe)

## Notes
- El archivo renderizado `adws/adw_triggers/trigger_cron.py` ya está implementado y funcionando
- El template Jinja2 debe mantenerse sincronizado con el renderizado
- El trigger cron usa polling (revisa periódicamente), diferente del webhook que responde a eventos
- La lógica de detección debe ser idéntica entre cron y webhook para consistencia
- Los workflows dependientes (`adw_build_iso`, `adw_test_iso`, etc.) requieren un worktree existente, por eso necesitan ADW ID
- El anti-loop con `ADW_BOT_IDENTIFIER` es crítico para evitar que el bot procese sus propios comentarios
- El estado `ADWState` permite rastrear workflows a través de múltiples fases (plan, build, test, etc.)
