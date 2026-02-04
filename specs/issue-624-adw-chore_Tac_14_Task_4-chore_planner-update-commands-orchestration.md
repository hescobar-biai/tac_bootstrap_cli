# Chore: Actualizar comandos existentes con contexto de orquestación

## Metadata
issue_number: `624`
adw_id: `chore_Tac_14_Task_4`
issue_json: `{"number": 624, "title": "Actualizar comandos existentes con contexto de orquestación", "body": "..."}`

## Chore Description

Actualizar tres comandos slash existentes (`/plan`, `/build`, `/review`) en BASE y TEMPLATES para referenciar nuevos patrones de orquestación y agentes especializados introducidos en TAC-14. Este es trabajo de documentación que agrega nueva información sobre cuándo usar comandos de orquestación vs comandos directos, manteniendo total compatibilidad hacia atrás.

## Relevant Files

### Archivos BASE a modificar:
1. **`.claude/commands/plan.md`** - Agregar sección "Orchestration Patterns" con links a `orch_plan_w_scouts_build_review` y `planner` agent
2. **`.claude/commands/build.md`** - Agregar sección "Orchestration Patterns" con link a `build-agent`
3. **`.claude/commands/review.md`** - Agregar sección "Orchestration Patterns" con contexto de review agent

### Archivos TEMPLATES a sincronizar:
4. **`tac_bootstrap_cli/tac_bootstrap/templates/.claude/commands/plan.md.j2`** - Sincronizar con plan.md
5. **`tac_bootstrap_cli/tac_bootstrap/templates/.claude/commands/build.md.j2`** - Sincronizar con build.md
6. **`tac_bootstrap_cli/tac_bootstrap/templates/.claude/commands/review.md.j2`** - Sincronizar con review.md

### Archivos de referencia (ya existen):
- `.claude/commands/orch_plan_w_scouts_build_review.md` - Comando de orquestación completo
- `.claude/commands/orch_scout_and_build.md` - Comando de orquestación scout + build
- `.claude/commands/orch_one_shot_agent.md` - Comando de orquestación one-shot
- `.claude/agents/planner.md` - Definición del agente planner
- `.claude/agents/build-agent.md` - Definición del agente build
- `.claude/agents/scout-report-suggest.md` - Definición del agente scout

## Step by Step Tasks

### Task 1: Verificar existencia de archivos referenciados
- Verificar que existen todos los archivos de orquestación y agentes usando Glob/Read
- Confirmar que los archivos tienen el contenido esperado
- Si faltan archivos, anotar con TODO en lugar de crear links rotos

### Task 2: Actualizar .claude/commands/plan.md en BASE
- Leer el archivo actual para preservar contenido existente
- Agregar nueva sección "## Orchestration Patterns" al final (antes de cualquier "See Also" si existe)
- Incluir texto explicativo breve (2-3 oraciones) sobre cuándo usar orquestación vs comando directo
- Agregar link markdown relativo a `.claude/commands/orch_plan_w_scouts_build_review.md`
- Agregar link markdown relativo a `.claude/agents/planner.md`
- Preservar todo el contenido, tono, estructura y formato existente

### Task 3: Actualizar .claude/commands/build.md en BASE
- Leer el archivo actual para preservar contenido existente
- Agregar nueva sección "## Orchestration Patterns" al final
- Incluir texto explicativo breve (2-3 oraciones) sobre cuándo usar build-agent
- Agregar link markdown relativo a `.claude/agents/build-agent.md`
- Agregar link markdown relativo a `.claude/commands/orch_scout_and_build.md`
- Preservar todo el contenido, tono, estructura y formato existente

### Task 4: Actualizar .claude/commands/review.md en BASE
- Leer el archivo actual para preservar contenido existente
- Agregar nueva sección "## Orchestration Patterns" al final
- Incluir texto explicativo breve (1-2 oraciones) sobre agentes de review especializados
- Agregar referencia conceptual a review agents en workflows de orquestación
- Preservar todo el contenido, tono, estructura y formato existente

### Task 5: Sincronizar templates en tac_bootstrap_cli/tac_bootstrap/templates/
- Copiar contenido actualizado de plan.md a plan.md.j2 (sin variables Jinja2 necesarias)
- Copiar contenido actualizado de build.md a build.md.j2 (sin variables Jinja2 necesarias)
- Copiar contenido actualizado de review.md a review.md.j2 (sin variables Jinja2 necesarias)
- Verificar que los archivos .j2 son copias exactas de los .md (documentación estática)

### Task 6: Validar cambios
- Verificar que links markdown funcionan (archivos existen)
- Verificar que no se modificó funcionalidad existente
- Verificar que el tono y formato se mantienen consistentes
- Ejecutar comandos de validación

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `ls -la .claude/commands/plan.md .claude/commands/build.md .claude/commands/review.md` - Verificar archivos BASE existen
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/.claude/commands/plan.md.j2` - Verificar templates existen
- `grep -n "## Orchestration Patterns" .claude/commands/plan.md` - Verificar sección agregada
- `grep -n "## Orchestration Patterns" .claude/commands/build.md` - Verificar sección agregada
- `grep -n "## Orchestration Patterns" .claude/commands/review.md` - Verificar sección agregada

## Notes

**Backward Compatibility:** Este es trabajo puramente aditivo. No se modifica ninguna instrucción existente, solo se agrega nueva sección informativa al final de cada comando. Los comandos continúan funcionando exactamente igual.

**Sin Variables Jinja2:** La sección "Orchestration Patterns" es documentación estática a nivel de framework, no contenido específico del proyecto. Por lo tanto, los archivos .j2 son copias exactas de los .md sin necesidad de variables de template.

**Orchestration Patterns Content Template:**
```markdown
## Orchestration Patterns

Para tareas complejas multi-fase, considera usar comandos de orquestación que coordinan múltiples agentes especializados automáticamente:

- [orch_plan_w_scouts_build_review](./../commands/orch_plan_w_scouts_build_review.md) - Workflow completo: exploración → planificación → construcción → revisión
- [planner agent](./../agents/planner.md) - Agente especializado en crear planes de implementación estructurados

Usa comandos directos (como este) para tareas de fase única. Usa orquestación para workflows multi-agente coordinados.
```

**Dependencies:** Esta tarea depende de Tarea 2 (Agent Definitions) y Tarea 3 (Orchestrator Commands) del plan TAC-14. Si esos archivos no existen, se crearán links con TODO comments.
