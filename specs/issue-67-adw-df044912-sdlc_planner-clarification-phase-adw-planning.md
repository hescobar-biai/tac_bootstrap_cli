# Feature: Fase de Clarificación en ADW Planning

## Metadata
issue_number: `67`
adw_id: `df044912`
issue_json: `{"number":67,"title":"Tarea 3: Fase de Clarificación en ADW Planning","body":"### Descripción\nAñadir una fase opcional de clarificación en `adw_plan_iso.py` que identifique ambigüedades en el issue antes de generar el plan. Inspirado en `/speckit.clarify`.\n\n### Beneficio\n- Reduce implementaciones incorrectas\n- Fuerza definición clara de requisitos\n- Documenta decisiones tomadas\n\n### Prompt para Ejecutar\n\n```\nNecesito añadir una fase de clarificación opcional en el workflow adw_plan_iso.py de TAC Bootstrap CLI.\n\nLa fase de clarificación debe:\n1. Analizar el issue de GitHub buscando:\n   - Requisitos ambiguos o vagos\n   - Información faltante\n   - Decisiones técnicas no especificadas\n   - Casos edge no definidos\n\n2. Si encuentra ambigüedades:\n   - Generar lista de preguntas específicas\n   - Postear comentario en el issue pidiendo clarificación\n   - Pausar el workflow hasta obtener respuestas\n   - O continuar con assumptions documentadas\n\n3. Documentar clarificaciones:\n   - Guardar preguntas y respuestas en el spec\n   - Incluir assumptions tomadas\n\nArchivos a modificar:\n- tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2\n- Posiblemente adw_modules/workflow_ops.py.j2\n\nEl flag --skip-clarify debe permitir saltar esta fase si no se necesita.\n```\n\n### Archivos Involucrados\n- `templates/adws/adw_plan_iso.py.j2`\n- `templates/adws/adw_modules/workflow_ops.py.j2`\n\n### Criterios de Aceptación\n- [ ] adw_plan_iso tiene fase de clarificación\n- [ ] Detecta ambigüedades en issues\n- [ ] Puede postear preguntas en GitHub\n- [ ] Flag --skip-clarify funciona\n- [ ] Clarificaciones se documentan en spec\n"}`

## Feature Description
Esta feature añade una fase de clarificación inteligente al workflow de planificación ADW (`adw_plan_iso.py`). Antes de generar un plan de implementación, el sistema analizará el issue de GitHub usando un agente LLM para detectar requisitos ambiguos, información faltante o decisiones técnicas no especificadas. Si se detectan ambigüedades, puede pausar el workflow para solicitar clarificaciones al usuario mediante comentarios en el issue, o puede continuar documentando las assumptions tomadas en el spec generado.

## User Story
As a developer using ADW workflows
I want to identify and resolve ambiguities in issue descriptions before planning implementation
So that I reduce the risk of implementing the wrong solution and ensure all requirements are clearly defined

## Problem Statement
Actualmente, `adw_plan_iso.py` procede directamente a generar un plan de implementación sin analizar si el issue contiene información suficiente y clara. Esto puede resultar en:
- Planes de implementación basados en assumptions incorrectas
- Decisiones técnicas importantes tomadas sin consultar al usuario
- Casos edge no considerados que causan bugs o re-trabajo
- Falta de documentación sobre por qué se tomaron ciertas decisiones de diseño

## Solution Statement
Implementar una fase de clarificación opcional (activada por defecto, desactivable con `--skip-clarify`) que:
1. Usa un agente LLM para analizar el issue y detectar ambigüedades en categorías específicas (requisitos, decisiones técnicas, casos edge, información faltante)
2. Si se detectan ambigüedades, genera preguntas específicas y las postea como comentario en el issue
3. Ofrece dos modos de operación:
   - **Interactive mode** (default): Pausa el workflow hasta que el usuario responda en el issue
   - **Continue mode** (`--clarify-continue`): Documenta las assumptions y continúa con el plan
4. Guarda todas las clarificaciones y assumptions en el spec file generado para trazabilidad

## Relevant Files
Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2` - Workflow principal de planificación que necesita la nueva fase de clarificación
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` - Módulo de operaciones de workflow donde se puede añadir función `clarify_issue()`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/github.py.j2` - Funciones para interactuar con GitHub (ya tiene `make_issue_comment`, `fetch_issue`)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2` - Sistema de agentes para ejecutar comandos Claude (se usará para análisis LLM)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2` - Tipos de datos, necesitará nuevos modelos para clarificaciones

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/clarify.md.j2` - Template del comando `/clarify` para el agente que detecta ambigüedades (opcional, puede usar agente inline)

## Implementation Plan

### Phase 1: Foundation
1. Añadir nuevos argumentos CLI a `adw_plan_iso.py`:
   - `--skip-clarify`: Flag booleano para deshabilitar fase de clarificación
   - `--clarify-continue`: Flag booleano para continuar con assumptions sin pausar
2. Crear modelos Pydantic en `data_types.py.j2`:
   - `ClarificationQuestion` (question: str, category: str, severity: str)
   - `ClarificationResponse` (has_ambiguities: bool, questions: List[ClarificationQuestion], assumptions: List[str])
3. Diseñar el prompt del agente clarificador que analizará el issue

### Phase 2: Core Implementation
1. Implementar función `clarify_issue()` en `workflow_ops.py.j2`:
   - Recibe GitHubIssue, adw_id, logger, working_dir
   - Construye prompt para agente LLM con instrucciones de análisis
   - Ejecuta agente usando `execute_template()` con modelo apropiado
   - Parsea respuesta del agente a ClarificationResponse
   - Retorna (ClarificationResponse, error)
2. Crear lógica de manejo de ambigüedades en `adw_plan_iso.py`:
   - Si no hay ambigüedades: continuar directamente a build_plan
   - Si hay ambigüedades y modo interactive: postear preguntas y exit(0) con mensaje
   - Si hay ambigüedades y modo continue: documentar assumptions y continuar
3. Implementar función para extraer respuestas del usuario desde comentarios del issue
4. Añadir lógica para guardar clarificaciones en el state ADW

### Phase 3: Integration
1. Integrar fase de clarificación en el flujo principal de `adw_plan_iso.py`:
   - Después de fetch_issue y antes de classify_issue
   - Guardar resultado de clarificación en state
   - Pasar clarificaciones al agente de planning para que las incluya en el spec
2. Modificar `build_plan()` para aceptar clarificaciones como parámetro opcional
3. Actualizar template del spec file para incluir sección de Clarifications
4. Añadir logging y comentarios en GitHub para visibilidad del proceso

## Step by Step Tasks

### Task 1: Añadir modelos de datos para clarificación
- Abrir `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`
- Añadir modelo `ClarificationQuestion` con campos:
  - `question: str` - La pregunta específica
  - `category: str` - Categoría: "requirements", "technical_decision", "edge_case", "missing_info"
  - `severity: str` - "critical", "important", "nice_to_have"
- Añadir modelo `ClarificationResponse` con campos:
  - `has_ambiguities: bool`
  - `questions: List[ClarificationQuestion]`
  - `assumptions: List[str]`
  - `analysis: str` - Explicación del análisis

### Task 2: Crear función clarify_issue en workflow_ops
- Abrir `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`
- Añadir imports necesarios (ClarificationQuestion, ClarificationResponse, execute_template)
- Implementar función `clarify_issue(issue: GitHubIssue, adw_id: str, logger, working_dir: Optional[str] = None) -> Tuple[Optional[ClarificationResponse], Optional[str]]`
- Construir prompt detallado para el agente LLM:
  - Instrucciones de analizar el issue buscando ambigüedades
  - Categorías específicas a revisar
  - Formato de output esperado (JSON con estructura de ClarificationResponse)
- Ejecutar agente usando AgentTemplateRequest con el prompt inline
- Parsear JSON response a ClarificationResponse
- Retornar (response, None) si exitoso, (None, error) si falla

### Task 3: Añadir flags CLI a adw_plan_iso
- Abrir `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`
- Modificar argparse para aceptar:
  - `--skip-clarify`: action="store_true", help="Skip clarification phase"
  - `--clarify-continue`: action="store_true", help="Continue with assumptions if ambiguities found"
- Parsear estos flags y guardarlos en variables
- Añadir lógica: si `--skip-clarify` está presente, saltar toda la fase de clarificación

### Task 4: Integrar fase de clarificación en adw_plan_iso
- En `adw_plan_iso.py`, después de `fetch_issue` (línea 96) y antes de `classify_issue` (línea 108)
- Añadir bloque condicional: `if not skip_clarify:`
- Llamar a `clarify_issue()` pasando issue, adw_id, logger, worktree_path
- Manejar errores: si retorna error, loggear y continuar
- Si `has_ambiguities == True`:
  - Construir mensaje con las preguntas formateadas en markdown
  - Postear comentario en el issue usando `make_issue_comment()`
  - Si modo interactive (no `--clarify-continue`):
    - Guardar state con fase "awaiting_clarification"
    - Postear mensaje indicando que workflow está pausado
    - `sys.exit(0)` con mensaje de éxito
  - Si modo continue (`--clarify-continue`):
    - Guardar assumptions en state
    - Continuar con el workflow
- Guardar ClarificationResponse en state bajo key "clarification"

### Task 5: Modificar build_plan para incluir clarificaciones
- En `workflow_ops.py.j2`, modificar función `build_plan()` para aceptar parámetro opcional `clarifications: Optional[str] = None`
- Si clarifications está presente, añadirlo al contexto del agente de planning
- Modificar el prompt de planning para incluir sección de clarificaciones/assumptions
- El spec generado debe tener sección "## Clarifications & Assumptions" si hay datos

### Task 6: Añadir lógica de resume para workflow pausado
- En `adw_plan_iso.py`, al inicio del main, verificar si state tiene `awaiting_clarification`
- Si es true, buscar comentarios nuevos del usuario en el issue usando `find_keyword_from_comment()` o función similar
- Extraer respuestas del usuario y guardarlas en state
- Actualizar state a fase normal y continuar workflow

### Task 7: Actualizar logging y mensajes de GitHub
- Añadir mensajes informativos en cada paso de clarificación:
  - "Analyzing issue for ambiguities..."
  - "Found X ambiguities - posting questions to issue"
  - "No ambiguities detected - proceeding with planning"
  - "Workflow paused - awaiting user clarifications"
- Formatear preguntas en markdown para mejor legibilidad en GitHub
- Añadir sección de assumptions claramente visible en comentarios

### Task 8: Testing manual del workflow
- Crear un issue de prueba con requisitos vagos intencionalmente
- Ejecutar `uv run adw_plan_iso.py <issue> --adw-id test123`
- Verificar que detecta ambigüedades
- Verificar que postea preguntas en el issue
- Verificar que pausa el workflow correctamente
- Responder en el issue y re-ejecutar
- Verificar que continúa con las respuestas
- Probar modo `--clarify-continue` y verificar que documenta assumptions
- Probar `--skip-clarify` y verificar que salta la fase completamente

### Task 9: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación para asegurar cero regresiones
- Corregir cualquier error de linting, type checking o tests
- Verificar que el workflow completo funciona end-to-end

## Testing Strategy

### Unit Tests
No se requieren unit tests formales en esta iteración (el proyecto usa testing manual principalmente), pero se debe validar:
- Parsing correcto de ClarificationResponse desde JSON
- Manejo de errores cuando el agente falla
- Flags CLI funcionan correctamente

### Edge Cases
- Issue sin body (solo título): debe detectar falta de información
- Issue muy detallado sin ambigüedades: debe continuar sin pausa
- Agente LLM retorna JSON malformado: debe loggear error y continuar
- Usuario nunca responde preguntas: workflow queda pausado indefinidamente (esperado)
- Flag `--skip-clarify` salta fase completamente
- Flag `--clarify-continue` documenta assumptions y no pausa

## Acceptance Criteria
- `adw_plan_iso.py` tiene fase de clarificación integrada que se ejecuta después de fetch_issue y antes de classify_issue
- La fase analiza el issue usando un agente LLM y detecta ambigüedades en categorías específicas
- Si se detectan ambigüedades, genera preguntas específicas y las postea como comentario en el issue de GitHub
- Flag `--skip-clarify` permite saltar la fase de clarificación completamente
- Flag `--clarify-continue` permite continuar el workflow documentando assumptions en lugar de pausar
- Todas las clarificaciones (preguntas, respuestas, assumptions) se documentan en el state ADW
- Las clarificaciones se pasan al agente de planning y se incluyen en el spec file generado
- El workflow puede pausarse esperando respuesta del usuario y resumirse correctamente
- Validation commands ejecutan sin errores: pytest, ruff, mypy, smoke test

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Prompt del Agente Clarificador
El prompt para el agente LLM debe ser específico y estructurado:

```
You are an expert software requirements analyst. Analyze the following GitHub issue and identify any ambiguities, missing information, or unclear decisions.

Issue Title: {title}
Issue Body: {body}

Analyze the issue for:
1. **Requirements**: Are the functional requirements clear and complete? Are success criteria defined?
2. **Technical Decisions**: Are technology choices, architectural patterns, or implementation approaches specified?
3. **Edge Cases**: Are error scenarios, boundary conditions, or special cases considered?
4. **Missing Information**: Is any critical context, data, or specification missing?

For each ambiguity found, generate a specific question categorized as:
- "requirements" - unclear functional requirements
- "technical_decision" - unspecified technical choices
- "edge_case" - unhandled scenarios
- "missing_info" - absent critical information

Rate severity as: "critical", "important", or "nice_to_have"

If NO ambiguities are found, explain why the issue is sufficiently clear.

Return your analysis as JSON:
{
  "has_ambiguities": boolean,
  "questions": [
    {"question": "...", "category": "...", "severity": "..."}
  ],
  "assumptions": ["assumption if continuing without answer"],
  "analysis": "brief explanation"
}
```

### Consideraciones de Diseño
- La fase de clarificación debe ser rápida (< 30s) para no ralentizar workflows simples
- Usar modelo apropiado para el análisis (sonnet probablemente suficiente, no opus)
- El formato de preguntas debe ser markdown-friendly para GitHub
- Considerar rate limiting de GitHub API al postear comentarios
- El state debe ser robusto para manejar interrupciones y resumes

### Posibles Extensiones Futuras
- Soporte para múltiples rondas de clarificación
- Integración con issue templates para reducir ambigüedades desde el inicio
- Métricas de calidad de issues (% que requieren clarificación)
- Auto-sugerencias de mejoras al issue description
- Integración con /speckit si se implementa en el futuro
