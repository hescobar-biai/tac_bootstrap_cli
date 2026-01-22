# Chore: Modificar adw_plan_iso para auto-resolver clarificaciones en lugar de pausar

## Metadata
issue_number: `100`
adw_id: `46eb5097`
issue_json: `{"number":100,"title":"Tarea 2: Modificar adw_plan_iso para auto-resolver en lugar de pausar","body":"/chore\n**Archivos a modificar**:\n1. `adws/adw_plan_iso.py` (base)\n2. `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2` (template)\n\n**Prompt para el agente**:\n\n```\nVas a modificar el flujo de clarificaciones en DOS archivos.\n\n## ARCHIVO 1: adws/adw_plan_iso.py\n\nAbre el archivo adws/adw_plan_iso.py\n\nBusca el bloque que contiene \"if not clarify_continue:\" seguido de sys.exit(2).\nEste bloque está aproximadamente entre las líneas 180-202.\n\nREEMPLAZA todo ese bloque (desde \"if not clarify_continue:\" hasta el final del else) con:\n\n            # Auto-resolve clarifications instead of pausing\n            from adw_modules.workflow_ops import resolve_clarifications\n\n            resolved_text, resolve_error = resolve_clarifications(\n                issue, clarification_response, adw_id, logger, working_dir=None\n            )\n\n            if resolve_error:\n                logger.warning(f\"Auto-resolution failed: {resolve_error}\")\n                make_issue_comment(\n                    issue_number,\n                    format_issue_message(adw_id, \"ops\",\n                        f\"⚠️ Auto-resolution failed, using assumptions: {resolve_error}\"),\n                )\n                clarification_text = f\"## Assumptions\\n\\n\" + \"\\n\".join([\n                    f\"- {a}\" for a in clarification_response.assumptions\n                ])\n            else:\n                clarification_text = resolved_text\n                make_issue_comment(\n                    issue_number,\n                    format_issue_message(adw_id, \"ops\",\n                        \"🤖 Auto-resolved clarifications:\\n\\n\" + resolved_text),\n                )\n\n            logger.info(\"Continuing with auto-resolved decisions\")\n\nTAMBIÉN elimina:\n1. El argumento --clarify-continue del argparser (si existe)\n2. La variable clarify_continue y su uso\n3. El import de sys.exit(2) relacionado con clarificaciones\n\n\n## ARCHIVO 2: tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2\n\nAbre el archivo tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2\n\nAplica EXACTAMENTE los mismos cambios que en el archivo base.\nEl código es idéntico (no hay variables Jinja2 en esta sección).\n\n\n## Verificación\n\nEjecuta: uv run pytest\nTodos los tests deben pasar.\n<h2 style=\"margin-top: 0px; color: rgb(204, 204, 204); font-family: -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, Roboto, sans-serif; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(9, 15, 36); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\">Respuestas a las Ambigüedades - Tarea 2</h2>\nPregunta | Respuesta\n-- | --\n¿Qué si resolved_text está vacío/inválido? | Tratarlo como error. Usar fallback a assumptions.\n¿Continuar o salir si falla auto-resolution? | Continuar con assumptions. No exit. El workflow debe avanzar.\n¿clarification_response.assumptions siempre existe? | Sí. Es lista de strings (puede estar vacía). Definido en ClarificationResponse.\n¿Eliminar sys.exit(2) import? | No eliminar el import. sys se usa en otros lugares. Solo eliminar el sys.exit(2) de clarificaciones.\n¿Otras referencias a clarify_continue? | Sí. Buscar y eliminar: argparser flag, variable, y el bloque if not clarify_continue.\n¿Logging adicional? | Ya hay logger.info(\"Continuing with auto-resolved decisions\"). Suficiente.\n¿Qué si make_issue_comment falla? | Ignorar. El workflow continúa. Los comentarios son informativos, no críticos.\n¿working_dir=None intencional? | Sí. Usa el directorio actual por defecto. Consistente con otras llamadas.\n\n<hr style=\"font-family: -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, Roboto, sans-serif; font-size: 13px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(9, 15, 36); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\"><p style=\"margin-top: 0.1em; margin-bottom: 0.2em; white-space: pre-wrap; color: rgb(204, 204, 204); font-family: -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, Roboto, sans-serif; font-size: 13px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(9, 15, 36); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\"><strong>Resumen</strong>: Proceder como está. Si falla, usar assumptions. Eliminar <code style=\"font-family: monospace; color: rgb(215, 186, 125); background-color: rgba(255, 255, 255, 0.1); padding: 2px 4px; border-radius: 3px; font-size: 0.9em; word-break: break-word;\">clarify_continue</code> y su argparser, pero mantener import de <code style=\"font-family: monospace; color: rgb(215, 186, 125); background-color: rgba(255, 255, 255, 0.1); padding: 2px 4px; border-radius: 3px; font-size: 0.9em; word-break: break-word;\">sys</code>.</p>\n"}`

## Chore Description

Esta chore modifica el workflow de planificación aislada (`adw_plan_iso.py`) para que, cuando se detecten ambigüedades en un issue, en lugar de pausar la ejecución y esperar respuestas del usuario, automáticamente resuelva las preguntas de clarificación usando la función `resolve_clarifications` del módulo `workflow_ops`.

El cambio elimina el flag `--clarify-continue` y el comportamiento de pausar (`sys.exit(2)`), haciendo que el workflow siempre intente auto-resolver las clarificaciones. Si la auto-resolución falla, el workflow continúa usando las assumptions predefinidas, garantizando que nunca se detenga.

Los cambios deben aplicarse tanto al archivo base (`adws/adw_plan_iso.py`) como a su template Jinja2 (`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`), ya que ambos contienen código idéntico en la sección de clarificaciones.

## Relevant Files

### Archivos a Modificar

1. **adws/adw_plan_iso.py** (líneas 72, 79, 180-202)
   - Archivo base del workflow de planificación aislada
   - Contiene el bloque `if not clarify_continue:` que debe ser reemplazado
   - Define el argumento `--clarify-continue` en argparser que debe eliminarse

2. **tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2** (líneas 72, 79, 180-202)
   - Template Jinja2 del archivo base
   - Contiene código idéntico al archivo base en esta sección
   - Debe recibir los mismos cambios exactos

### Archivos de Referencia

3. **adws/adw_modules/workflow_ops.py** (líneas 269-340 aprox)
   - Contiene la función `resolve_clarifications` que se importará
   - Ya implementada y funcional (Issue #98)
   - No requiere modificaciones

4. **adws/adw_modules/data_types.py**
   - Define `ClarificationResponse` con campo `assumptions`
   - Garantiza que `assumptions` siempre existe como lista

### New Files

Ningún archivo nuevo es necesario. Esta chore solo modifica archivos existentes.

## Step by Step Tasks

### Task 1: Modificar adws/adw_plan_iso.py - Eliminar argumento --clarify-continue

Abrir el archivo `adws/adw_plan_iso.py` y localizar la línea 72 donde se define el argumento `--clarify-continue`:

```python
parser.add_argument("--clarify-continue", action="store_true", help="Continue with assumptions if ambiguities found (don't pause)")
```

Eliminar completamente esta línea del argparser.

### Task 2: Modificar adws/adw_plan_iso.py - Eliminar variable clarify_continue

Localizar la línea 79 donde se asigna la variable:

```python
clarify_continue = args.clarify_continue
```

Eliminar completamente esta línea.

### Task 3: Modificar adws/adw_plan_iso.py - Reemplazar bloque de clarificaciones

Localizar el bloque entre las líneas 180-202 que comienza con `if not clarify_continue:` y termina con el final del else (línea 202).

Reemplazar TODO el bloque (desde `if not clarify_continue:` hasta el cierre del else) con el siguiente código:

```python
            # Auto-resolve clarifications instead of pausing
            from adw_modules.workflow_ops import resolve_clarifications

            resolved_text, resolve_error = resolve_clarifications(
                issue, clarification_response, adw_id, logger, working_dir=None
            )

            if resolve_error:
                logger.warning(f"Auto-resolution failed: {resolve_error}")
                make_issue_comment(
                    issue_number,
                    format_issue_message(adw_id, "ops",
                        f"⚠️ Auto-resolution failed, using assumptions: {resolve_error}"),
                )
                clarification_text = f"## Assumptions\n\n" + "\n".join([
                    f"- {a}" for a in clarification_response.assumptions
                ])
            else:
                clarification_text = resolved_text
                make_issue_comment(
                    issue_number,
                    format_issue_message(adw_id, "ops",
                        "🤖 Auto-resolved clarifications:\n\n" + resolved_text),
                )

            logger.info("Continuing with auto-resolved decisions")
```

**Importante:**
- NO eliminar el import de `sys` al inicio del archivo (línea 25), ya que se usa en otros lugares
- Solo eliminar el `sys.exit(2)` dentro del bloque de clarificaciones
- Mantener la indentación correcta (12 espacios, dentro del elif)

### Task 4: Modificar tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2 - Aplicar cambios idénticos

Abrir el archivo template `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2` y aplicar EXACTAMENTE los mismos tres cambios de las tareas 1, 2 y 3:

1. Eliminar línea 72: argumento `--clarify-continue`
2. Eliminar línea 79: variable `clarify_continue = args.clarify_continue`
3. Reemplazar bloque líneas 180-202 con el código de auto-resolución

**Nota:** El código en esta sección del template es idéntico al archivo base (no contiene variables Jinja2), por lo que los cambios son exactamente los mismos.

### Task 5: Validar cambios ejecutando tests

Ejecutar el suite completo de tests para verificar que no hay regresiones:

```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/trees/46eb5097
uv run pytest
```

Todos los tests deben pasar. Si hay fallos, revisar los cambios aplicados.

### Task 6: Ejecutar validación adicional

Ejecutar los comandos de validación del proyecto:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Verificar que:
- Todos los tests unitarios pasan
- No hay errores de linting
- El CLI funciona correctamente

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/46eb5097 && uv run pytest` - Tests del worktree
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios del CLI
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test del CLI

## Notes

### Decisiones de Diseño

1. **Auto-resolución siempre activa**: El workflow ahora SIEMPRE intenta auto-resolver. No hay opción de pausar manualmente.

2. **Fallback a assumptions**: Si `resolve_clarifications` falla o devuelve texto vacío, el sistema usa las assumptions predefinidas en `clarification_response.assumptions`.

3. **Workflow nunca se detiene**: El comportamiento `sys.exit(2)` es eliminado completamente. El workflow continúa incluso si hay errores en la auto-resolución.

4. **Comentarios informativos no críticos**: Si `make_issue_comment` falla, no afecta la ejecución del workflow. Los comentarios son solo para visibilidad del usuario.

5. **working_dir=None es intencional**: Usa el directorio de trabajo actual por defecto, consistente con otras llamadas en el código.

### Respuestas a Ambigüedades (del Issue)

- **¿Qué si resolved_text está vacío/inválido?** → Tratarlo como error. Usar fallback a assumptions.
- **¿Continuar o salir si falla auto-resolution?** → Continuar con assumptions. No exit. El workflow debe avanzar.
- **¿clarification_response.assumptions siempre existe?** → Sí. Es lista de strings (puede estar vacía). Definido en ClarificationResponse.
- **¿Eliminar sys.exit(2) import?** → No eliminar el import de sys. Se usa en otros lugares (líneas 108, 192, 219, 240, 259, 282, 308, 363). Solo eliminar el `sys.exit(2)` de clarificaciones.
- **¿Otras referencias a clarify_continue?** → Sí. Buscar y eliminar: argparser flag (línea 72), variable (línea 79), y el bloque `if not clarify_continue` (líneas 180-202).
- **¿Logging adicional?** → Ya hay `logger.info("Continuing with auto-resolved decisions")`. Suficiente.
- **¿Qué si make_issue_comment falla?** → Ignorar. El workflow continúa. Los comentarios son informativos, no críticos.
- **¿working_dir=None intencional?** → Sí. Usa el directorio actual por defecto. Consistente con otras llamadas.

### Archivos Relacionados

- Issue #98: Implementó la función `resolve_clarifications` usada en esta chore
- `adws/adw_modules/workflow_ops.py`: Contiene la función `resolve_clarifications` (líneas 269+)
- `adws/adw_modules/data_types.py`: Define `ClarificationResponse` y `ClarificationQuestion`
