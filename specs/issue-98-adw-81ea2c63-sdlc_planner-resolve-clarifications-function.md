# Feature: Agregar función `resolve_clarifications()` en workflow_ops.py

## Metadata
issue_number: `98`
adw_id: `81ea2c63`
issue_json: `{"number":98,"title":"Tarea 1: Agregar función \`resolve_clarifications()\` en workflow_ops.py","body":"**Archivo**: \`adws/adw_modules/workflow_ops.py\`\n\n**Prompt para el agente**:\n\n\`\`\`\nAbre el archivo adws/adw_modules/workflow_ops.py\n\nDespués de la función \`clarify_issue()\` (línea 266), agrega la siguiente función:\n\ndef resolve_clarifications(\n    issue: GitHubIssue,\n    clarification: ClarificationResponse,\n    adw_id: str,\n    logger: logging.Logger,\n    working_dir: Optional[str] = None,\n) -> Tuple[Optional[str], Optional[str]]:\n    \"\"\"Auto-resolve clarification questions using AI.\n\n    Returns (resolved_text, error_message) tuple.\n    \"\"\"\n    logger.info(\"Auto-resolving clarifications...\")\n\n    questions_text = \"\\n\".join([\n        f\"- [{q.category}] {q.question} (severity: {q.severity})\"\n        for q in clarification.questions\n    ])\n    assumptions_text = \"\\n\".join([f\"- {a}\" for a in clarification.assumptions])\n\n    prompt = f\"\"\"You are a senior software architect making implementation decisions.\n\n## Issue\nTitle: {issue.title}\nBody: {issue.body}\n\n## Questions to Resolve\n{questions_text}\n\n## Current Assumptions\n{assumptions_text}\n\nFor EACH question: make a clear decision with brief rationale.\nChoose the simplest reasonable approach.\n\nReturn JSON:\n{{\n  \"decisions\": [{{\"question\": \"...\", \"decision\": \"...\", \"rationale\": \"...\"}}],\n  \"summary\": \"brief overall approach\"\n}}\"\"\"\n\n    from adw_modules.agent import execute_prompt\n    from adw_modules.data_types import AgentPromptRequest\n\n    request = AgentPromptRequest(\n        prompt=prompt,\n        adw_id=adw_id,\n        agent_name=\"resolver\",\n        model=\"sonnet\",\n        dangerously_skip_permissions=False,\n        output_file=f\"agents/{adw_id}/resolver/decisions.txt\",\n        working_dir=working_dir,\n    )\n\n    try:\n        response = execute_prompt(request, logger)\n        if not response.success:\n            return None, response.output\n\n        output = response.output.strip()\n        # Remove markdown if present\n        if output.startswith(\"\`\`\`\"):\n            lines = output.split(\"\\n\")\n            start_idx, end_idx = 0, len(lines)\n            for i, line in enumerate(lines):\n                if line.startswith(\"\`\`\`\"):\n                    if start_idx == 0:\n                        start_idx = i + 1\n                    else:\n                        end_idx = i\n                        break\n            output = \"\\n\".join(lines[start_idx:end_idx])\n\n        data = parse_json(output, dict)\n\n        resolved_md = \"## Auto-Resolved Clarifications\\n\\n\"\n        resolved_md += f\"**Summary:** {data.get('summary', 'N/A')}\\n\\n\"\n        for d in data.get(\"decisions\", []):\n            resolved_md += f\"**Q:** {d.get('question', 'N/A')}\\n\"\n            resolved_md += f\"**A:** {d.get('decision', 'N/A')}\\n\"\n            resolved_md += f\"*{d.get('rationale', 'N/A')}*\\n\\n\"\n\n        logger.info(f\"Auto-resolved {len(data.get('decisions', []))} clarifications\")\n        return resolved_md, None\n    except Exception as e:\n        return None, f\"Error auto-resolving: {str(e)}\"\n\nVerifica que la función esté correctamente indentada y que los imports necesarios estén disponibles (GitHubIssue, ClarificationResponse, Tuple, Optional, logging ya están importados en el archivo).\n\nPregunta | Respuesta\n-- | --\n¿Manejar clarification.questions vacío o None? | No. Si has_ambiguities=True, siempre hay questions. El caller (adw_plan_iso.py) ya valida esto antes de llamar.\n¿JSON malformado o campos faltantes? | El try-except ya captura esto. Retorna (None, \"Error auto-resolving: ...\"). El caller usará las assumptions como fallback.\n¿Retry si el agente falla? | No. Sin retry. Si falla, se usan las assumptions originales. Simplicidad sobre robustez.\n¿Qué pasa si parse_json() falla? | Lanza excepción, capturada por try-except. Retorna error message.\n¿Validar que decisions == questions? | No. El AI puede consolidar o expandir. Confiar en el output.\n¿Qué si clarify_issue() no está en línea 266? | Buscar \"return None, error_msg\" al final de clarify_issue() y agregar después. Ignorar número de línea.\n¿Crear directorio para output_file? | execute_prompt ya maneja creación de directorios. No hacer nada extra.\n¿Límite de longitud del prompt? | No. Claude soporta 200k tokens. Issues + questions nunca llegarán a ese límite.\n\n<hr style=\"font-family: -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, Roboto, sans-serif; font-size: 13px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; white-space: normal; background-color: rgb(9, 15, 36); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\"><p style=\"margin-top: 0.1em; margin-bottom: 0.2em; white-space: pre-wrap; color: rgb(204, 204, 204); font-family: -apple-system, &quot;system-ui&quot;, &quot;Segoe UI&quot;, Roboto, sans-serif; font-size: 13px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: 400; letter-spacing: normal; orphans: 2; text-align: start; text-indent: 0px; text-transform: none; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(9, 15, 36); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial;\"><strong>Resumen</strong>: Proceder con la implementación tal como está. El <code style=\"font-family: monospace; color: rgb(215, 186, 125); background-color: rgba(255, 255, 255, 0.1); padding: 2px 4px; border-radius: 3px; font-size: 0.9em; word-break: break-word;\">try-except</code> maneja todos los edge cases retornando error, y el caller usa assumptions como fallback</p>\n"}`

## Feature Description
Esta feature agrega una nueva función `resolve_clarifications()` al módulo `workflow_ops.py` que permite auto-resolver preguntas de clarificación identificadas durante la fase de análisis de issues. La función utiliza un agente LLM (Claude Sonnet) para tomar decisiones de implementación razonables basadas en el contexto del issue, las preguntas pendientes y las assumptions actuales. Esto elimina la necesidad de intervención manual para responder preguntas de clarificación en workflows automatizados.

## User Story
As a developer using ADW workflows in automatic/ZTE mode
I want clarification questions to be auto-resolved by AI when appropriate
So that my workflows can run end-to-end without manual intervention while still documenting design decisions

## Problem Statement
Actualmente, la fase de clarificación en `adw_plan_iso.py` puede pausar el workflow esperando respuestas manuales del usuario cuando detecta ambigüedades. Esto rompe el flujo en workflows automatizados (como ADW ZTE - Zero Touch Execution). Para habilitar workflows verdaderamente automatizados, necesitamos una función que pueda tomar decisiones razonables basadas en el contexto disponible, documentando las decisiones tomadas para trazabilidad.

## Solution Statement
Implementar una función `resolve_clarifications()` en `workflow_ops.py` que:
1. Recibe el issue original y la respuesta de clarificación con preguntas/assumptions
2. Construye un prompt especializado para un agente LLM actuando como arquitecto senior
3. Solicita al agente que tome decisiones claras para cada pregunta con rationale
4. Parsea la respuesta JSON del agente
5. Formatea las decisiones como markdown para incluir en el spec file
6. Maneja errores apropiadamente retornando None para que el caller use assumptions como fallback

## Relevant Files
Archivos necesarios para implementar la feature:

- `adws/adw_modules/workflow_ops.py` - Archivo principal donde se agregará la nueva función después de `clarify_issue()` (línea 266)
- `adws/adw_modules/data_types.py` - Contiene tipos `GitHubIssue` y `ClarificationResponse` ya importados
- `adws/adw_modules/agent.py` - Contiene `execute_prompt()` para ejecutar agentes LLM
- `adws/adw_modules/utils.py` - Contiene `parse_json()` para parsear respuestas del agente

### New Files
Ningún archivo nuevo será creado.

## Implementation Plan

### Phase 1: Foundation
No se requiere trabajo fundacional. Todos los tipos de datos, funciones helper y imports necesarios ya existen en el codebase:
- `GitHubIssue` y `ClarificationResponse` están definidos en data_types.py y ya importados en workflow_ops.py
- `execute_prompt()` existe en agent.py
- `parse_json()` existe en utils.py

### Phase 2: Core Implementation
Implementar la función `resolve_clarifications()` con la firma exacta especificada:
1. Construir el prompt estructurado para el agente LLM
2. Crear el `AgentPromptRequest` con los parámetros correctos
3. Ejecutar el agente y capturar la respuesta
4. Parsear el JSON, manejando markdown code fences
5. Formatear las decisiones como markdown
6. Retornar tuple (resolved_text, error_message)

### Phase 3: Integration
La función está lista para ser integrada por otras tareas. No requiere integración en esta tarea específica, ya que será utilizada por `adw_plan_iso.py` en tareas posteriores.

## Step by Step Tasks

### Task 1: Localizar el punto de inserción en workflow_ops.py
- Abrir el archivo `adws/adw_modules/workflow_ops.py`
- Buscar la función `clarify_issue()` usando grep o búsqueda en el editor
- Identificar el final de la función (buscar `return None, error_msg` al final de `clarify_issue()`)
- Nota: El número de línea 266 puede ser inexacto, usar la búsqueda en vez del número

### Task 2: Agregar la función resolve_clarifications()
- Posicionar el cursor después del final de la función `clarify_issue()`
- Agregar dos líneas en blanco para separar las funciones
- Copiar e insertar la función completa tal como está especificada en el issue
- Verificar que la indentación sea consistente con las demás funciones del archivo (sin indentación adicional - nivel de módulo)

### Task 3: Verificar imports existentes
- Confirmar que los siguientes tipos ya están importados en la sección de imports:
  - `GitHubIssue` (de data_types)
  - `ClarificationResponse` (de data_types)
  - `Tuple`, `Optional` (de typing)
  - `logging` (módulo estándar)
- Los imports dentro de la función (`execute_prompt`, `AgentPromptRequest`, `parse_json`) están correctamente colocados como imports locales

### Task 4: Validar sintaxis y linting
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check adws/adw_modules/workflow_ops.py` para verificar linting
- Corregir cualquier error de formato o estilo reportado por ruff
- Ejecutar `cd tac_bootstrap_cli && uv run mypy adws/adw_modules/` para verificar tipos
- Nota: No hay tests unitarios para esta función todavía (se agregarán en tareas futuras)

### Task 5: Ejecutar validación completa
- Ejecutar todos los comandos de validación listados abajo
- Confirmar que no hay regresiones
- Confirmar que el archivo se puede importar sin errores

## Testing Strategy

### Unit Tests
Los unit tests para esta función se agregarán en una tarea posterior. Por ahora, la validación es:
1. Sintaxis correcta (verificado por Python parser)
2. Tipos correctos (verificado por mypy)
3. Linting correcto (verificado por ruff)
4. Imports resuelven correctamente

### Edge Cases
Los edge cases están documentados en el issue y manejados por la función:
- JSON malformado → capturado por try-except, retorna error
- Agente falla → retorna None, caller usa assumptions
- parse_json() falla → excepción capturada, retorna error
- clarification.questions vacío → no es problema, el caller valida antes de llamar

## Acceptance Criteria
- La función `resolve_clarifications()` existe en workflow_ops.py después de `clarify_issue()`
- La firma de la función es exactamente como se especifica (parámetros y tipos)
- El docstring está presente y describe el retorno
- La función construye un prompt estructurado para el agente
- La función usa `execute_prompt()` con los parámetros correctos
- La función parsea JSON manejando markdown code fences
- La función formatea las decisiones como markdown
- La función maneja errores apropiadamente con try-except
- No hay errores de linting (ruff check pasa)
- No hay errores de tipo (mypy pasa)
- Todos los imports necesarios están disponibles

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/81ea2c63 && uv run ruff check adws/adw_modules/workflow_ops.py` - Linting del archivo modificado
- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/81ea2c63 && uv run mypy adws/adw_modules/` - Type check del módulo
- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/81ea2c63 && python -c "from adws.adw_modules.workflow_ops import resolve_clarifications; print('Import successful')"` - Verificar que la función se puede importar

## Notes
- Esta es la Tarea 1 de una serie que agrega auto-resolución de clarificaciones a workflows ADW
- La función está diseñada para simplicidad sobre robustez (sin retries, confiar en el caller para manejo de fallback)
- El caller (adw_plan_iso.py en tareas futuras) manejará el caso cuando esta función retorna None usando las assumptions originales
- El output_file se guarda en `agents/{adw_id}/resolver/decisions.txt` para trazabilidad
- No se requieren nuevas dependencias - todas las funciones helper ya existen
