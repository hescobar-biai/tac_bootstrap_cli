# Plan: Auto-Resolución de Clarificaciones en ADW Workflows

## Contexto

Actualmente cuando el workflow detecta ambigüedades en un issue:
1. Genera preguntas de clarificación
2. Publica las preguntas en GitHub
3. **PAUSA** el workflow (exit code 2)
4. Espera respuesta humana

**Objetivo**: Que Claude auto-resuelva las ambigüedades y continúe sin pausar.

---

## Tareas

### Tarea 1: Agregar función `resolve_clarifications()` en workflow_ops.py

**Archivo**: `adws/adw_modules/workflow_ops.py`

**Prompt para el agente**:

```
Abre el archivo adws/adw_modules/workflow_ops.py

Después de la función `clarify_issue()` (línea 266), agrega la siguiente función:

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
        # Remove markdown if present
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

Verifica que la función esté correctamente indentada y que los imports necesarios estén disponibles (GitHubIssue, ClarificationResponse, Tuple, Optional, logging ya están importados en el archivo).
```

---

### Tarea 2: Modificar adw_plan_iso.py para auto-resolver en lugar de pausar

**Archivo**: `adws/adw_plan_iso.py`

**Prompt para el agente**:

```
Abre el archivo adws/adw_plan_iso.py

Busca el bloque de código entre las líneas 180-202 que contiene:

if not clarify_continue:
    # Pause workflow - exit with code 2 (paused, not error)
    logger.info("Workflow paused - awaiting user clarifications")
    make_issue_comment(
        issue_number,
        format_issue_message(
            adw_id, "ops",
            "⏸️ Workflow paused - awaiting clarifications.\n\n"
            "Please answer the questions above, then re-run this workflow to continue."
        ),
    )
    # Exit code 2 = paused (distinguishes from 0=success, 1=error)
    sys.exit(2)
else:
    # Continue mode - document assumptions
    logger.info("Continuing with documented assumptions")
    make_issue_comment(
        issue_number,
        format_issue_message(
            adw_id, "ops",
            "✅ Ambiguities detected, continuing with documented assumptions"
        ),
    )

Reemplázalo con:

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
    # Use original assumptions as fallback
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

IMPORTANTE: Elimina la opción --clarify-continue del argparser ya que ya no es necesaria (el workflow siempre auto-resuelve).
```

---

### Tarea 3: Actualizar template workflow_ops.py.j2

**Archivo**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`

**Prompt para el agente**:

```
Abre el archivo tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2

Este es un template Jinja2 que genera workflow_ops.py para proyectos nuevos.

Después de la función clarify_issue() (busca la línea que contiene "return None, error_msg" al final de clarify_issue), agrega la misma función resolve_clarifications() que agregaste en la Tarea 1.

IMPORTANTE: Como es un template Jinja2, las llaves dobles {{ }} en el prompt de Python deben escaparse como {{ "{{" }} y {{ "}}" }} o usar {% raw %}...{% endraw %}.

El prompt dentro de la función debe verse así:

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

Verifica que el template sea válido ejecutando: uv run pytest tac_bootstrap_cli/tests/
```

---

### Tarea 4: Actualizar template adw_plan_iso.py.j2

**Archivo**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`

**Prompt para el agente**:

```
Abre el archivo tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2

Aplica los mismos cambios que en la Tarea 2:

1. Busca el bloque que contiene "if not clarify_continue:" y el sys.exit(2)

2. Reemplázalo con el código de auto-resolución:

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

3. Elimina el argumento --clarify-continue del argparser si existe.

Verifica que el template sea válido ejecutando: uv run pytest tac_bootstrap_cli/tests/
```

---

### Tarea 5: Ejecutar tests y verificar

**Prompt para el agente**:

```
Ejecuta los tests del proyecto para verificar que los cambios no rompieron nada:

uv run pytest

Si hay errores:
1. Lee el mensaje de error
2. Identifica el archivo y línea con el problema
3. Corrige el error
4. Vuelve a ejecutar los tests

Todos los tests deben pasar antes de continuar.
```

---

### Tarea 6: Prueba manual del flujo

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

- [ ] `resolve_clarifications()` existe en `workflow_ops.py`
- [ ] `adw_plan_iso.py` llama a `resolve_clarifications()` en lugar de pausar
- [ ] Templates actualizados con los mismos cambios
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
