# Plan: Auto-Resolución de Clarificaciones en ADW Workflows

## Contexto

Actualmente cuando el workflow detecta ambigüedades en un issue:
1. Genera preguntas de clarificación
2. Publica las preguntas en GitHub
3. **PAUSA** el workflow (exit code 2)
4. Espera respuesta humana

**Objetivo**: Que Claude auto-resuelva las ambigüedades y continúe sin pausar.

---

## Estructura del Proyecto

Este proyecto tiene DOS lugares donde vive el código:

| Ubicación | Propósito |
|-----------|-----------|
| `adws/` | Código base que se usa en ESTE repo |
| `tac_bootstrap_cli/tac_bootstrap/templates/adws/` | Templates Jinja2 que generan código para OTROS proyectos |

**IMPORTANTE**: Cada tarea DEBE modificar AMBOS lugares para mantener sincronía.

---

## Tareas

### Tarea 1: Agregar función `resolve_clarifications()` en workflow_ops

**Archivos a modificar**:
1. `adws/adw_modules/workflow_ops.py` (base)
2. `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` (template)

**Prompt para el agente**:

```
Vas a agregar la función resolve_clarifications() en DOS archivos.

## ARCHIVO 1: adws/adw_modules/workflow_ops.py

Abre el archivo adws/adw_modules/workflow_ops.py

Busca el final de la función clarify_issue() (la línea que dice "return None, error_msg" dentro del except).

Después de esa función, agrega:

def resolve_clarifications(
    issue: GitHubIssue,
    clarification: ClarificationResponse,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """Auto-resolve clarification questions using AI.

    Returns (resolved_text, error_message) tuple.
    """
    logger.info("Auto-resolving clarifications...")

    questions_text = "\n".join([
        f"- [{q.category}] {q.question} (severity: {q.severity})"
        for q in clarification.questions
    ])
    assumptions_text = "\n".join([f"- {a}" for a in clarification.assumptions])

    prompt = f"""You are a senior software architect making implementation decisions.

## Issue
Title: {issue.title}
Body: {issue.body}

## Questions to Resolve
{questions_text}

## Current Assumptions
{assumptions_text}

For EACH question: make a clear decision with brief rationale.
Choose the simplest reasonable approach.

Return JSON:
{{
  "decisions": [{{"question": "...", "decision": "...", "rationale": "..."}}],
  "summary": "brief overall approach"
}}"""

    from adw_modules.agent import execute_prompt
    from adw_modules.data_types import AgentPromptRequest

    request = AgentPromptRequest(
        prompt=prompt,
        adw_id=adw_id,
        agent_name="resolver",
        model="sonnet",
        dangerously_skip_permissions=False,
        output_file=f"agents/{adw_id}/resolver/decisions.txt",
        working_dir=working_dir,
    )

    try:
        response = execute_prompt(request, logger)
        if not response.success:
            return None, response.output

        output = response.output.strip()
        if output.startswith("```"):
            lines = output.split("\n")
            start_idx, end_idx = 0, len(lines)
            for i, line in enumerate(lines):
                if line.startswith("```"):
                    if start_idx == 0:
                        start_idx = i + 1
                    else:
                        end_idx = i
                        break
            output = "\n".join(lines[start_idx:end_idx])

        data = parse_json(output, dict)

        resolved_md = "## Auto-Resolved Clarifications\n\n"
        resolved_md += f"**Summary:** {data.get('summary', 'N/A')}\n\n"
        for d in data.get("decisions", []):
            resolved_md += f"**Q:** {d.get('question', 'N/A')}\n"
            resolved_md += f"**A:** {d.get('decision', 'N/A')}\n"
            resolved_md += f"*{d.get('rationale', 'N/A')}*\n\n"

        logger.info(f"Auto-resolved {len(data.get('decisions', []))} clarifications")
        return resolved_md, None
    except Exception as e:
        return None, f"Error auto-resolving: {str(e)}"


## ARCHIVO 2: tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2

Abre el archivo tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2

Agrega la MISMA función en el mismo lugar, pero con esta diferencia para el prompt (escapar llaves para Jinja2):

    prompt = f"""You are a senior software architect making implementation decisions.

## Issue
Title: {issue.title}
Body: {issue.body}

## Questions to Resolve
{questions_text}

## Current Assumptions
{assumptions_text}

For EACH question: make a clear decision with brief rationale.
Choose the simplest reasonable approach.

Return JSON:
{% raw %}{{
  "decisions": [{{"question": "...", "decision": "...", "rationale": "..."}}],
  "summary": "brief overall approach"
}}{% endraw %}"""

El resto de la función es idéntico al archivo base.

## Verificación

Ejecuta: uv run pytest
Todos los tests deben pasar.
```

---

### Tarea 2: Modificar adw_plan_iso para auto-resolver en lugar de pausar

**Archivos a modificar**:
1. `adws/adw_plan_iso.py` (base)
2. `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2` (template)

**Prompt para el agente**:

```
Vas a modificar el flujo de clarificaciones en DOS archivos.

## ARCHIVO 1: adws/adw_plan_iso.py

Abre el archivo adws/adw_plan_iso.py

Busca el bloque que contiene "if not clarify_continue:" seguido de sys.exit(2).
Este bloque está aproximadamente entre las líneas 180-202.

REEMPLAZA todo ese bloque (desde "if not clarify_continue:" hasta el final del else) con:

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

TAMBIÉN elimina:
1. El argumento --clarify-continue del argparser (si existe)
2. La variable clarify_continue y su uso
3. El import de sys.exit(2) relacionado con clarificaciones


## ARCHIVO 2: tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2

Abre el archivo tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2

Aplica EXACTAMENTE los mismos cambios que en el archivo base.
El código es idéntico (no hay variables Jinja2 en esta sección).


## Verificación

Ejecuta: uv run pytest
Todos los tests deben pasar.
```

---

### Tarea 3: Ejecutar tests y verificar

**Prompt para el agente**:

```
Ejecuta los tests del proyecto para verificar que los cambios no rompieron nada:

uv run pytest

Si hay errores:
1. Lee el mensaje de error completo
2. Identifica el archivo y línea con el problema
3. Corrige el error en AMBOS archivos (base y template) si aplica
4. Vuelve a ejecutar los tests

Todos los tests deben pasar antes de continuar.

Verifica también que los archivos base y template estén sincronizados:
- adws/adw_modules/workflow_ops.py debe tener resolve_clarifications()
- tac_bootstrap_cli/.../workflow_ops.py.j2 debe tener la misma función (con {% raw %} en el JSON)
- adws/adw_plan_iso.py NO debe tener sys.exit(2) para clarificaciones
- tac_bootstrap_cli/.../adw_plan_iso.py.j2 debe tener los mismos cambios
```

---

### Tarea 4: Prueba manual del flujo

**Prompt para el agente**:

```
Realiza una prueba manual del nuevo flujo:

1. Crea un issue de prueba ambiguo:
   gh issue create --title "Add user feature" --body "Add some user functionality to the app"

2. Ejecuta el workflow de planning:
   uv run adws/adw_plan_iso.py --issue <numero_del_issue>

3. Verifica que:
   - El workflow detecta ambigüedades
   - Llama a resolve_clarifications() en lugar de pausar
   - Las decisiones auto-generadas aparecen en el issue de GitHub
   - El workflow continúa con la planificación (no exit code 2)
   - Se genera un archivo de plan en agents/<adw_id>/

4. Reporta el resultado:
   - Si funciona: confirma que el flujo está completo
   - Si falla: describe el error y en qué paso ocurrió
```

---

## Verificación Final

Después de completar todas las tareas:

- [ ] `resolve_clarifications()` existe en `adws/adw_modules/workflow_ops.py`
- [ ] `resolve_clarifications()` existe en `templates/.../workflow_ops.py.j2` (con {% raw %})
- [ ] `adws/adw_plan_iso.py` usa auto-resolve (no sys.exit(2))
- [ ] `templates/.../adw_plan_iso.py.j2` usa auto-resolve (no sys.exit(2))
- [ ] Todos los tests pasan
- [ ] Prueba manual exitosa

---

## Diagrama del Flujo Nuevo

```
┌─────────────────┐
│  GitHub Issue   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  clarify_issue  │ ──► Detecta ambigüedades
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  resolve_clarifications │ ──► Claude auto-responde
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ Post decisiones │ ──► Documenta en GitHub
│   en issue      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   build_plan    │ ──► Continúa sin pausar
└─────────────────┘
```

---

## Respuestas a Ambigüedades

| Pregunta | Respuesta |
|----------|-----------|
| ¿Manejar `questions` vacío? | No. Si `has_ambiguities=True`, siempre hay questions. |
| ¿JSON malformado? | El try-except captura y retorna error. Fallback a assumptions. |
| ¿Retry si falla? | No. Simplicidad sobre robustez. |
| ¿parse_json() falla? | Excepción capturada, retorna error message. |
| ¿Validar decisions == questions? | No. Confiar en el AI output. |
| ¿Línea 266 no existe? | Buscar "return None, error_msg" al final de clarify_issue(). |
| ¿Crear directorio output_file? | execute_prompt ya lo maneja. |
| ¿Límite de prompt? | No. Claude soporta 200k tokens. |
