# Plan de Implementación TAC-14: Codebase Singularity & Orchestrator

## Resumen Ejecutivo

Este plan implementa TAC-14 para elevar tac_bootstrap desde Class 1 (Agentic Layer) hacia Class 2 (Outloop Systems) y Class 3 (Orchestrator Agent), incorporando Skills System, Agent SDK, base de datos PostgreSQL, WebSockets, y una aplicación web de orquestación.

**Versión objetivo**: 0.8.0
**Baseline**: TAC-13 completo (v0.7.x)

---

## Estructura de Rutas

Cada tarea trabaja en DOS ubicaciones:

1. **BASE**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`
   - Archivos funcionales del repositorio
   - Se usan directamente en tac_bootstrap

2. **TEMPLATES**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`
   - Templates Jinja2 (.j2)
   - Se usan para generar nuevos proyectos con `tac-bootstrap init`
   - DEBEN registrarse en `scaffold_service.py`

**IMPORTANTE**: Cada tarea FEATURE debe crear/modificar archivos en AMBAS ubicaciones.

---

## Supuestos (Assumptions)

1. **PostgreSQL disponible**: Se asume PostgreSQL 14+ instalado y accesible en localhost
2. **Node.js/npm disponible**: Para build del frontend (Vue.js 3 + TypeScript)
3. **Backward compatibility**: Los ADWs basados en archivos (adw_state.json) seguirán funcionando
4. **Opt-in database**: La integración con base de datos será opcional vía configuración
5. **Orchestrator app opcional**: La aplicación web será un componente opcional del bootstrap
6. **Agent SDK version**: claude-agent-sdk>=0.1.18 disponible en PyPI

---

## Tareas

### FASE 1: Skills System (Class 1 Grade 7)

#### Tarea 1

**[FEATURE] Implementar Skills System completo (BASE + TEMPLATES)**

**Descripción**:
Crear el directorio `.claude/skills/` con el meta-skill en BASE y generar templates Jinja2 correspondientes en CLI para que nuevos proyectos incluyan automáticamente el Skills System.

**Pasos técnicos**:

**BASE**:
1. Crear directorio `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/`
2. Crear subdirectorio `meta-skill/` con estructura completa
3. Copiar SKILL.md desde `/Volumes/MAc1/Celes/TAC/tac-14/.claude/skills/meta-skill/SKILL.md`
4. Crear subdirectorio `docs/` con 3 archivos de documentación
5. Adaptar rutas y contexto a tac_bootstrap

**TEMPLATES**:
6. Crear `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/`
7. Copiar toda la estructura a templates con extensión .j2 para archivos Markdown
8. Preservar YAML frontmatter sin variables Jinja2
9. Registrar templates en `scaffold_service.py`

**Criterios de aceptación**:
- Directorio skills existe en BASE con meta-skill funcional
- SKILL.md contiene YAML frontmatter válido
- Templates .j2 creados en CLI
- Registration en scaffold_service.py completa
- Progressive disclosure funcionando

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
.claude/skills/                                                              [CREAR]
.claude/skills/meta-skill/                                                   [CREAR]
.claude/skills/meta-skill/SKILL.md                                           [CREAR]
.claude/skills/meta-skill/docs/                                              [CREAR]
.claude/skills/meta-skill/docs/claude_code_agent_skills.md                   [CREAR]
.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md          [CREAR]
.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md          [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
.claude/skills/                                                              [CREAR]
.claude/skills/meta-skill/                                                   [CREAR]
.claude/skills/meta-skill/SKILL.md.j2                                        [CREAR]
.claude/skills/meta-skill/docs/claude_code_agent_skills.md                   [CREAR]
.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md          [CREAR]
.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md          [CREAR]
```

**CLI** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/`):
```
scaffold_service.py  [MODIFICAR - agregar renderizado de skills]
```

**Metadata**:
- Categoría: Skills System
- Prioridad: Alta
- Estimación: 2h
- Dependencias: Ninguna

**Keywords**: skills, meta-skill, progressive-disclosure, yaml-frontmatter, class-1-grade-7, jinja2-templates

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_1`

---

### FASE 2: Custom Agent Definitions (Class 2)

#### Tarea 2

**[FEATURE] Implementar Agent Definitions completas (BASE + TEMPLATES)**

**Descripción**:
Crear 7 definiciones de agentes especializados en BASE y generar templates Jinja2 correspondientes para nuevos proyectos.

**Pasos técnicos**:

**BASE**:
1. Verificar/crear directorio `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/`
2. Copiar `build-agent.md` desde `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/`
3. Copiar `scout-report-suggest.md` y `scout-report-suggest-fast.md`
4. Copiar `planner.md`
5. Copiar `playwright-validator.md`
6. Copiar `meta-agent.md`
7. Copiar `docs-scraper.md`
8. Validar YAML frontmatter en cada archivo
9. Adaptar rutas a contexto tac_bootstrap

**TEMPLATES**:
10. Crear `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/`
11. Copiar cada .md a template .md.j2 (7 archivos)
12. Preservar YAML frontmatter
13. Registrar en scaffold_service.py

**Criterios de aceptación**:
- 7 archivos .md creados en BASE
- YAML frontmatter válido en cada uno
- 7 templates .md.j2 creados en CLI
- Registro en scaffold_service.py completo
- Tools configuradas correctamente

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
.claude/agents/build-agent.md                [CREAR]
.claude/agents/scout-report-suggest.md       [CREAR]
.claude/agents/scout-report-suggest-fast.md  [CREAR]
.claude/agents/planner.md                    [CREAR]
.claude/agents/playwright-validator.md       [CREAR]
.claude/agents/meta-agent.md                 [CREAR]
.claude/agents/docs-scraper.md               [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
.claude/agents/build-agent.md.j2                [CREAR]
.claude/agents/scout-report-suggest.md.j2       [CREAR]
.claude/agents/scout-report-suggest-fast.md.j2  [CREAR]
.claude/agents/planner.md.j2                    [CREAR]
.claude/agents/playwright-validator.md.j2       [CREAR]
.claude/agents/meta-agent.md.j2                 [CREAR]
.claude/agents/docs-scraper.md.j2               [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR - agregar renderizado de agents]
```

**Metadata**:
- Categoría: Agent Definitions
- Prioridad: Alta
- Estimación: 2.5h
- Dependencias: Ninguna

**Keywords**: custom-agents, agent-definitions, yaml-frontmatter, class-2, orchestration, jinja2-templates

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_2`

---

### FASE 3: Orchestrator Commands (Class 2)

#### Tarea 3

**[FEATURE] Implementar Orchestrator Commands (BASE + TEMPLATES)**

**Descripción**:
Crear 5 comandos slash de orquestación multi-agente en BASE y templates para nuevos proyectos.

**Pasos técnicos**:

**BASE**:
1. Copiar `orch_plan_w_scouts_build_review.md` desde `/Volumes/MAc1/Celes/TAC/tac-14/.claude/commands/`
2. Copiar `orch_scout_and_build.md`
3. Copiar `orch_one_shot_agent.md`
4. Copiar `build_in_parallel.md`
5. Copiar `parallel_subagents.md`
6. Adaptar referencias a agent definitions
7. Validar YAML frontmatter

**TEMPLATES**:
8. Crear templates en CLI commands
9. Copiar cada orch_*.md a .md.j2
10. Registrar en scaffold_service.py

**Criterios de aceptación**:
- 5 comandos orch_*.md creados en BASE
- YAML frontmatter válido
- Referencias a agents correctas
- 5 templates creados en CLI
- Registro completo

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
.claude/commands/orch_plan_w_scouts_build_review.md  [CREAR]
.claude/commands/orch_scout_and_build.md              [CREAR]
.claude/commands/orch_one_shot_agent.md               [CREAR]
.claude/commands/build_in_parallel.md                 [CREAR]
.claude/commands/parallel_subagents.md                [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
.claude/commands/orch_plan_w_scouts_build_review.md.j2  [CREAR]
.claude/commands/orch_scout_and_build.md.j2              [CREAR]
.claude/commands/orch_one_shot_agent.md.j2               [CREAR]
.claude/commands/build_in_parallel.md.j2                 [CREAR]
.claude/commands/parallel_subagents.md.j2                [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR - agregar renderizado de orch commands]
```

**Metadata**:
- Categoría: Orchestrator Commands
- Prioridad: Alta
- Estimación: 2.5h
- Dependencias: Tarea 2

**Keywords**: orchestrator-commands, multi-agent, plan-build-review, class-2, outloop-systems

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_3`

---

#### Tarea 4

**[CHORE] Actualizar comandos existentes con contexto de orquestación**

**Descripción**:
Actualizar comandos `/plan`, `/build`, `/review` existentes en BASE para referenciar nuevos patrones de orquestación y agentes especializados.

**Pasos técnicos**:

**BASE**:
1. Abrir `.claude/commands/plan.md`
2. Agregar sección "## Orchestration Patterns" referenciando `orch_plan_w_scouts_build_review`
3. Agregar link a `planner` agent definition
4. Actualizar `.claude/commands/build.md` con link a `build-agent`
5. Actualizar `.claude/commands/review.md` con contexto de review agent
6. Mantener backward compatibility

**TEMPLATES**:
7. Sincronizar cambios en templates correspondientes en CLI

**Criterios de aceptación**:
- 3 comandos actualizados en BASE
- Sección "Orchestration Patterns" agregada
- Links a agent definitions
- Templates sincronizados
- Backward compatibility preservada

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
.claude/commands/plan.md    [MODIFICAR]
.claude/commands/build.md   [MODIFICAR]
.claude/commands/review.md  [MODIFICAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
.claude/commands/plan.md.j2    [MODIFICAR]
.claude/commands/build.md.j2   [MODIFICAR]
.claude/commands/review.md.j2  [MODIFICAR]
```

**Metadata**:
- Categoría: Documentation
- Prioridad: Media
- Estimación: 1h
- Dependencias: Tarea 2, Tarea 3

**Keywords**: command-updates, orchestration-context, backward-compatibility

**ADW Metadata**:
- Tipo: `/chore`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: chore_Tac_14_Task_4`

---

### FASE 4: Agent SDK Integration (Class 2)

#### Tarea 5

**[FEATURE] Implementar Agent SDK module (BASE + TEMPLATES)**

**Descripción**:
Crear módulo adw_agent_sdk.py con modelos Pydantic para control programático de agentes, en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_agent_sdk.py`
2. Validar PEP 723 dependencies header
3. Incluir enums: ModelName, SettingSource, HookEventName, PermissionDecision
4. Incluir modelos Pydantic completos
5. Agregar docstrings

**TEMPLATES**:
6. Copiar a template .j2 sin modificaciones
7. Registrar en scaffold_service.py

**Criterios de aceptación**:
- adw_agent_sdk.py creado en BASE
- Todos los enums definidos
- Pydantic models con validators
- Template .j2 creado
- Registro completo

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_modules/adw_agent_sdk.py  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_modules/adw_agent_sdk.py.j2  [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Agent SDK
- Prioridad: Alta
- Estimación: 2h
- Dependencias: Ninguna

**Keywords**: agent-sdk, pydantic-models, type-safety, programmatic-agents, class-2

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_5`

---

### FASE 5: Database-Backed ADWs (Class 3)

#### Tarea 6

**[FEATURE] Implementar Database Schema (BASE + TEMPLATES)**

**Descripción**:
Crear schema PostgreSQL completo con 5 tablas para orchestrator en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Crear directorio `adws/schema/`
2. Extraer schema desde `/Volumes/MAc1/Celes/TAC/tac-14/apps/orchestrator_3_stream/backend/`
3. Crear `schema_orchestrator.sql` con 5 tablas:
   - orchestrator_agents
   - agents
   - prompts
   - agent_logs
   - system_logs
4. Incluir índices y constraints
5. Crear subdirectorio `migrations/`
6. Agregar README.md con setup instructions

**TEMPLATES**:
7. Copiar schema a templates
8. Copiar README.md
9. Registrar en scaffold_service.py

**Criterios de aceptación**:
- schema_orchestrator.sql creado
- 5 tablas definidas
- migrations/ directory creado
- README.md con instrucciones
- Templates sincronizados

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/schema/                        [CREAR]
adws/schema/schema_orchestrator.sql [CREAR]
adws/schema/migrations/             [CREAR]
adws/schema/README.md               [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/schema/schema_orchestrator.sql.j2 [CREAR]
adws/schema/README.md.j2               [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Database Schema
- Prioridad: Alta
- Estimación: 2h
- Dependencias: Ninguna

**Keywords**: postgresql, database-schema, orchestrator-agents, class-3, state-management

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_6`

---

#### Tarea 7

**[FEATURE] Implementar Database Models (BASE + TEMPLATES)**

**Descripción**:
Crear orch_database_models.py con 5 modelos Pydantic que mapean a PostgreSQL en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/orch_database_models.py`
2. Crear clases: OrchestratorAgent, Agent, Prompt, AgentLog, SystemLog
3. Implementar field_validator para UUID/Decimal conversion
4. Configurar json_encoders
5. Agregar docstrings

**TEMPLATES**:
6. Copiar a template .j2
7. Registrar en scaffold_service.py

**Criterios de aceptación**:
- 5 modelos Pydantic creados
- UUID/Decimal converters implementados
- JSON serialization configurada
- Template creado

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_modules/orch_database_models.py  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_modules/orch_database_models.py.j2  [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Database Models
- Prioridad: Alta
- Estimación: 2h
- Dependencias: Tarea 6

**Keywords**: pydantic-models, database-orm, uuid-conversion, type-safety

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_7`

---

#### Tarea 8

**[FEATURE] Implementar Database Operations (BASE + TEMPLATES)**

**Descripción**:
Crear adw_database.py con CRUD operations y connection pooling en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_database.py`
2. Implementar connection pool (asyncpg)
3. Implementar CRUD para orchestrator_agents
4. Implementar CRUD para agents
5. Implementar CRUD para prompts (ADWs)
6. Implementar CRUD para logs
7. Agregar PEP 723 dependency: asyncpg>=0.29.0
8. Implementar error handling

**TEMPLATES**:
9. Copiar a template .j2
10. Registrar en scaffold_service.py

**Criterios de aceptación**:
- Connection pooling implementado
- CRUD completo para 5 tablas
- Error handling robusto
- Template creado

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_modules/adw_database.py  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_modules/adw_database.py.j2  [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Database Operations
- Prioridad: Alta
- Estimación: 3h
- Dependencias: Tarea 7

**Keywords**: database-crud, asyncpg, connection-pooling, error-handling

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_8`

---

#### Tarea 9

**[FEATURE] Implementar Database Logging (BASE + TEMPLATES)**

**Descripción**:
Crear adw_logging.py para logging estructurado a database en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_logging.py`
2. Implementar init_logging()
3. Implementar close_logging()
4. Implementar log_step_start()
5. Implementar log_step_end()
6. Implementar log_agent_event()
7. Implementar log_system_event()
8. Integrar con orch_database_models.py

**TEMPLATES**:
9. Copiar a template .j2
10. Registrar en scaffold_service.py

**Criterios de aceptación**:
- 6 funciones de logging implementadas
- Integración con database
- Validación Pydantic
- Template creado

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_modules/adw_logging.py  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_modules/adw_logging.py.j2  [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Logging Infrastructure
- Prioridad: Alta
- Estimación: 2h
- Dependencias: Tarea 8

**Keywords**: database-logging, structured-logging, event-tracking, observability

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_9`

---

#### Tarea 10

**[FEATURE] Implementar Consolidated Workflows (BASE + TEMPLATES)**

**Descripción**:
Crear 3 workflows database-backed con Agent SDK en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Crear directorio `adws/adw_workflows/`
2. Copiar `adw_plan_build.py` desde `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_workflows/`
3. Copiar `adw_plan_build_review.py`
4. Copiar `adw_plan_build_review_fix.py`
5. Adaptar imports
6. Implementar CLI arg parsing (--adw-id)
7. Integrar con adw_database.py
8. Integrar con adw_agent_sdk.py
9. Integrar con adw_logging.py
10. Agregar PEP 723 dependencies

**TEMPLATES**:
11. Copiar 3 workflows a templates .j2
12. Registrar en scaffold_service.py

**Criterios de aceptación**:
- 3 workflows creados en BASE
- Database integration funcional
- Agent SDK control implementado
- Templates creados

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_workflows/                               [CREAR]
adws/adw_workflows/adw_plan_build.py              [CREAR]
adws/adw_workflows/adw_plan_build_review.py       [CREAR]
adws/adw_workflows/adw_plan_build_review_fix.py   [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_workflows/adw_plan_build.py.j2              [CREAR]
adws/adw_workflows/adw_plan_build_review.py.j2       [CREAR]
adws/adw_workflows/adw_plan_build_review_fix.py.j2   [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Workflows
- Prioridad: Alta
- Estimación: 4h
- Dependencias: Tarea 5, Tarea 8, Tarea 9

**Keywords**: consolidated-workflows, database-backed, agent-sdk-control, orchestration

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_10`

---

### FASE 6: WebSockets Infrastructure (Class 3)

#### Tarea 11

**[FEATURE] Implementar WebSockets module (BASE + TEMPLATES)**

**Descripción**:
Crear adw_websockets.py para comunicación real-time en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Copiar `/Volumes/MAc1/Celes/TAC/tac-14/adws/adw_modules/adw_websockets.py`
2. Implementar WebSocket connection manager
3. Implementar broadcast de agent events
4. Implementar connection pooling
5. Implementar heartbeat/ping-pong
6. Agregar PEP 723 dependency: websockets>=12.0
7. Integrar con adw_logging.py

**TEMPLATES**:
8. Copiar a template .j2
9. Agregar variable {{ config.websocket_port }}
10. Registrar en scaffold_service.py

**Criterios de aceptación**:
- WebSocket server implementado
- Connection management robusto
- Event broadcasting funcional
- Template creado con variables

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_modules/adw_websockets.py  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_modules/adw_websockets.py.j2  [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: WebSockets
- Prioridad: Alta
- Estimación: 3h
- Dependencias: Tarea 9

**Keywords**: websockets, real-time, event-streaming, connection-pooling, class-3

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_11`

---

### FASE 7: Orchestrator Web Application (Class 3)

#### Tarea 12

**[FEATURE] Implementar Orchestrator Backend (BASE + TEMPLATES)**

**Descripción**:
Crear aplicación FastAPI completa con REST endpoints y WebSocket en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Crear directorio `apps/orchestrator_3_stream/backend/`
2. Copiar estructura desde `/Volumes/MAc1/Celes/TAC/tac-14/apps/orchestrator_3_stream/backend/`
3. Crear `main.py` con FastAPI app
4. Crear subdirectorios: `modules/`, `prompts/`
5. Implementar 7 endpoints REST + 1 WebSocket
6. Crear `.env.sample` y `pyproject.toml`
7. Integrar con adw_database.py, adw_websockets.py, adw_agent_sdk.py

**TEMPLATES**:
8. Copiar toda estructura backend a templates
9. Agregar variables Jinja2 para configuración
10. Registrar en scaffold_service.py

**Criterios de aceptación**:
- FastAPI app funcional en BASE
- 8 endpoints implementados
- Templates backend completos
- Configuración con variables

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
apps/orchestrator_3_stream/                  [CREAR]
apps/orchestrator_3_stream/backend/          [CREAR]
apps/orchestrator_3_stream/backend/main.py   [CREAR]
apps/orchestrator_3_stream/backend/modules/  [CREAR]
apps/orchestrator_3_stream/backend/prompts/  [CREAR]
apps/orchestrator_3_stream/backend/.env.sample     [CREAR]
apps/orchestrator_3_stream/backend/pyproject.toml  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
apps/orchestrator_3_stream/backend/  [CREAR - estructura completa]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Orchestrator Backend
- Prioridad: Alta
- Estimación: 6h
- Dependencias: Tarea 8, Tarea 11, Tarea 5

**Keywords**: fastapi, rest-api, websocket-endpoint, orchestrator-backend, class-3

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_12`

---

#### Tarea 13

**[FEATURE] Implementar Orchestrator Frontend (BASE + TEMPLATES)**

**Descripción**:
Crear aplicación Vue.js 3 + TypeScript con swimlane visualization en BASE y templates.

**Pasos técnicos**:

**BASE**:
1. Crear directorio `apps/orchestrator_3_stream/frontend/`
2. Copiar estructura desde `/Volumes/MAc1/Celes/TAC/tac-14/apps/orchestrator_3_stream/frontend/`
3. Crear `package.json`, `vite.config.ts`
4. Crear `src/` con: App.vue, components/, composables/, services/, stores/
5. Implementar swimlane visualization
6. Implementar WebSocket client
7. Implementar autocomplete y keyboard shortcuts

**TEMPLATES**:
8. Copiar estructura frontend a templates
9. Agregar variables Jinja2 para ports
10. Registrar en scaffold_service.py

**Criterios de aceptación**:
- Vue.js app funcional
- Swimlane rendering
- WebSocket client conectado
- Templates completos

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
apps/orchestrator_3_stream/frontend/                [CREAR]
apps/orchestrator_3_stream/frontend/package.json    [CREAR]
apps/orchestrator_3_stream/frontend/vite.config.ts  [CREAR]
apps/orchestrator_3_stream/frontend/src/            [CREAR - estructura completa]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
apps/orchestrator_3_stream/frontend/  [CREAR - estructura completa]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Orchestrator Frontend
- Prioridad: Alta
- Estimación: 8h
- Dependencias: Tarea 12

**Keywords**: vue-js, typescript, vite, swimlane-visualization, websocket-client, real-time-ui

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_13`

---

#### Tarea 14

**[CHORE] Crear documentación del Orchestrator (BASE + TEMPLATES)**

**Descripción**:
Crear README y documentación técnica para deployment y arquitectura.

**Pasos técnicos**:

**BASE**:
1. Crear `apps/orchestrator_3_stream/README.md`
2. Documentar arquitectura (backend + frontend)
3. Documentar setup de PostgreSQL
4. Crear `docs/` con architecture.md, deployment.md, api_reference.md

**TEMPLATES**:
5. Copiar documentación a templates
6. Registrar en scaffold_service.py

**Criterios de aceptación**:
- README.md completo
- 3 docs técnicos creados
- Templates sincronizados

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
apps/orchestrator_3_stream/README.md               [CREAR]
apps/orchestrator_3_stream/docs/                   [CREAR]
apps/orchestrator_3_stream/docs/architecture.md    [CREAR]
apps/orchestrator_3_stream/docs/deployment.md      [CREAR]
apps/orchestrator_3_stream/docs/api_reference.md   [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
apps/orchestrator_3_stream/README.md.j2  [CREAR]
apps/orchestrator_3_stream/docs/         [CREAR - 3 archivos]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Documentation
- Prioridad: Media
- Estimación: 3h
- Dependencias: Tarea 12, Tarea 13

**Keywords**: orchestrator-docs, deployment-guide, api-reference, architecture-diagram

**ADW Metadata**:
- Tipo: `/chore`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: chore_Tac_14_Task_14`

---

### FASE 8: Testing Infrastructure

#### Tarea 15

**[FEATURE] Implementar Test Suites (BASE + TEMPLATES)**

**Descripción**:
Crear suites pytest para database modules y Playwright para orchestrator UI.

**Pasos técnicos**:

**BASE - Pytest**:
1. Crear directorio `adws/adw_tests/`
2. Crear `conftest.py` con fixtures
3. Crear `test_database.py`, `test_workflows.py`, `test_agent_sdk.py`, `test_websockets.py`
4. Crear `pytest.ini`

**BASE - Playwright**:
5. Crear `apps/orchestrator_3_stream/playwright-tests/`
6. Crear `playwright.config.ts`
7. Crear 6 tests E2E

**TEMPLATES**:
8. Copiar estructura de tests a templates
9. Registrar en scaffold_service.py

**Criterios de aceptación**:
- 4 archivos pytest creados
- 6 tests E2E creados
- Templates sincronizados
- Todos los tests passing

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
adws/adw_tests/                     [CREAR]
adws/adw_tests/conftest.py          [CREAR]
adws/adw_tests/test_database.py     [CREAR]
adws/adw_tests/test_workflows.py    [CREAR]
adws/adw_tests/test_agent_sdk.py    [CREAR]
adws/adw_tests/test_websockets.py   [CREAR]
adws/adw_tests/pytest.ini           [CREAR]

apps/orchestrator_3_stream/playwright-tests/  [CREAR - 6 test files]
apps/orchestrator_3_stream/playwright.config.ts  [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
adws/adw_tests/                                   [CREAR - estructura completa]
apps/orchestrator_3_stream/playwright-tests/      [CREAR - estructura completa]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Testing
- Prioridad: Alta
- Estimación: 6h
- Dependencias: Tarea 7, Tarea 8, Tarea 9, Tarea 11, Tarea 12, Tarea 13

**Keywords**: pytest, playwright, unit-tests, e2e-tests, test-coverage

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_15`

---

### FASE 9: CLI Enhancements & Documentation

#### Tarea 16

**[FEATURE] Implementar OrchestratorConfig y Generator Logic**

**Descripción**:
Actualizar domain/config.py con OrchestratorConfig y generator.py con lógica condicional.

**Pasos técnicos**:

**CLI**:
1. Abrir `tac_bootstrap_cli/tac_bootstrap/domain/config.py`
2. Agregar clase OrchestratorConfig con campos: enabled, database_url, websocket_port, web_ui_port
3. Agregar campo en ProjectConfig
4. Abrir `tac_bootstrap_cli/tac_bootstrap/application/generator.py`
5. Agregar lógica condicional: if config.orchestrator.enabled
6. Implementar CLI flag `--with-orchestrator`
7. Actualizar help text

**Criterios de aceptación**:
- OrchestratorConfig definida
- enabled=False por defecto (opt-in)
- Lógica condicional implementada
- CLI flag funcional

**Rutas impactadas**:

**CLI** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/`):
```
domain/config.py               [MODIFICAR - agregar OrchestratorConfig]
application/generator.py       [MODIFICAR - agregar conditional logic]
```

**Metadata**:
- Categoría: Configuration & Generator
- Prioridad: Alta
- Estimación: 2h
- Dependencias: Ninguna

**Keywords**: pydantic-config, orchestrator-config, generator-logic, cli-flag, opt-in

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_16`

---

#### Tarea 17

**[CHORE] Actualizar CLI README con tabla de componentes TAC-14**

**Descripción**:
Actualizar README del CLI con documentación completa de TAC-14 incluyendo tabla de componentes.

**Pasos técnicos**:

**BASE**:
1. Abrir `tac_bootstrap_cli/README.md`
2. Agregar sección "## TAC-14: Codebase Singularity & Orchestrator"
3. Documentar Class 1-3 architecture
4. Agregar subsecciones: Skills System, Agent Definitions, Orchestrator Commands, Database-Backed ADWs, Orchestrator Web App
5. Crear tabla Markdown con 12 componentes (Skills, Agents, Commands, SDK, Database, WebSockets, Workflows, Orchestrator)
6. Agregar ejemplos de uso con/sin orchestrator
7. Documentar setup de PostgreSQL

**Criterios de aceptación**:
- Sección TAC-14 agregada
- Tabla de componentes completa (12 filas)
- Ejemplos de uso documentados
- Setup instructions claras

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
tac_bootstrap_cli/README.md  [MODIFICAR - agregar sección TAC-14 con tabla]
```

**Metadata**:
- Categoría: Documentation
- Prioridad: Alta
- Estimación: 3h
- Dependencias: Todas las tareas anteriores

**Keywords**: readme-update, documentation-table, tac-14-guide, component-table, usage-examples

**ADW Metadata**:
- Tipo: `/chore`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: chore_Tac_14_Task_17`

---

#### Tarea 18

**[CHORE] Crear guías TAC-14 completas en ai_docs/**

**Descripción**:
Crear 2 guías técnicas completas: guía general TAC-14 y guía específica de Skills.

**Pasos técnicos**:

**BASE**:
1. Crear `ai_docs/doc/Tac-14_complete_guide.md`
2. Documentar arquitectura Class 1-3
3. Documentar cada componente en detalle
4. Agregar migration guide TAC-13 → TAC-14
5. Agregar diagramas Mermaid
6. Crear `ai_docs/doc/Tac-14_skills_guide.md`
7. Explicar Skills vs Commands
8. Documentar progressive disclosure
9. Agregar 5 ejemplos completos
10. Agregar troubleshooting

**Criterios de aceptación**:
- 2 guías creadas
- Arquitectura completa documentada
- Migration guide incluido
- Ejemplos completos

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
ai_docs/doc/Tac-14_complete_guide.md  [CREAR]
ai_docs/doc/Tac-14_skills_guide.md    [CREAR]
```

**Metadata**:
- Categoría: Documentation
- Prioridad: Alta
- Estimación: 5h
- Dependencias: Todas las tareas de implementación

**Keywords**: complete-guide, skills-guide, tac-14-docs, architecture-guide, migration-guide

**ADW Metadata**:
- Tipo: `/chore`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: chore_Tac_14_Task_18`

---

### FASE 10: Migration & Utility Scripts

#### Tarea 19

**[FEATURE] Implementar Utility Scripts (BASE + TEMPLATES)**

**Descripción**:
Crear 3 scripts bash de utilidad: setup_database.sh, start_orchestrator.sh, migrate_to_tac14.sh.

**Pasos técnicos**:

**BASE**:
1. Crear `scripts/setup_database.sh` con lógica de PostgreSQL setup
2. Crear `scripts/start_orchestrator.sh` con health checks
3. Crear `scripts/migrate_to_tac14.sh` con backup y opt-in features
4. Hacer scripts executable (chmod +x)

**TEMPLATES**:
5. Copiar scripts a templates .sh.j2
6. Agregar variables Jinja2 para configuración
7. Registrar en scaffold_service.py
8. Implementar chmod +x en scripts generados

**Criterios de aceptación**:
- 3 scripts creados en BASE
- Scripts executable
- Templates con variables
- Registration completo

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
scripts/setup_database.sh      [CREAR]
scripts/start_orchestrator.sh  [CREAR]
scripts/migrate_to_tac14.sh    [CREAR]
```

**TEMPLATES** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/`):
```
scripts/setup_database.sh.j2      [CREAR]
scripts/start_orchestrator.sh.j2  [CREAR]
```

**CLI**:
```
application/scaffold_service.py  [MODIFICAR]
```

**Metadata**:
- Categoría: Utility Scripts
- Prioridad: Alta
- Estimación: 4h
- Dependencias: Tarea 6, Tarea 12, Tarea 13

**Keywords**: database-setup, orchestrator-startup, migration-script, automation

**ADW Metadata**:
- Tipo: `/feature`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: feature_Tac_14_Task_19`

---

### FASE 11: Versioning & Release

#### Tarea 20

**[CHORE] Actualizar CHANGELOG.md y bump version a 0.8.0**

**Descripción**:
Actualizar CHANGELOG con todas las features TAC-14 y bump version siguiendo Semantic Versioning.

**Pasos técnicos**:

**BASE**:
1. Abrir `CHANGELOG.md`
2. Agregar sección `## [0.8.0] - 2026-XX-XX`
3. Listar todas las features: Skills System, 7 Agent Definitions, 5 Orchestrator Commands, Agent SDK, Database modules, WebSockets, Orchestrator App, Tests, Scripts
4. Listar dependencies: claude-agent-sdk, asyncpg, websockets, fastapi, uvicorn, Vue.js, TypeScript
5. Actualizar version en `tac_bootstrap_cli/pyproject.toml`

**Criterios de aceptación**:
- CHANGELOG.md actualizado con sección 0.8.0
- Todas las features listadas (15+)
- Dependencies listadas
- Version bumped en pyproject.toml

**Rutas impactadas**:

**BASE** (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/`):
```
CHANGELOG.md                          [MODIFICAR - agregar sección 0.8.0]
tac_bootstrap_cli/pyproject.toml      [MODIFICAR - bump version]
```

**Metadata**:
- Categoría: Release Management
- Prioridad: Crítica
- Estimación: 2h
- Dependencias: **TODAS las tareas anteriores (1-19)**

**Keywords**: changelog, semantic-versioning, release-notes, version-bump, v0.8.0

**ADW Metadata**:
- Tipo: `/chore`
- Workflow: `/adw_sdlc_zte_iso`
- ID: `/adw_id: chore_Tac_14_Task_20`

---

## Grupos de Ejecución Paralela

La siguiente tabla define grupos de tareas que pueden ejecutarse en paralelo usando agentic parallelism:

| Grupo | Tareas | Cantidad | Dependencia | Descripción |
|-------|--------|----------|-------------|-------------|
| **P1** | 1, 2, 5, 6, 16 | 5 | Ninguna | Skills, Agents, Agent SDK, DB Schema, Config (independientes) |
| **P2** | 3, 7 | 2 | P1 | Orchestrator commands (dep: agents), DB models (dep: schema) |
| **P3** | 4, 8 | 2 | P2 | Command updates, DB operations |
| **P4** | 9, 11 | 2 | P3 | DB logging, WebSockets |
| **P5** | 10 | 1 | P4 | Workflows consolidados (dep: logging + SDK) |
| **P6** | 12 | 1 | P5 | Orchestrator backend (dep: workflows + websockets) |
| **P7** | 13, 19 | 2 | P6 | Orchestrator frontend, Utility scripts |
| **P8** | 14, 15 | 2 | P7 | Orchestrator docs, Test suites |
| **P9** | 17, 18 | 2 | P8 | README update, Guías TAC-14 |
| **SEQ** | 20 | 1 | **TODOS** | **CHANGELOG y version bump (ÚLTIMA TAREA)** |

**Notas**:
- Tareas dentro de cada grupo son independientes y pueden ejecutarse en paralelo
- Cada grupo depende del grupo anterior completo
- **SEQ** es secuencial y DEBE ejecutarse al final
- Total de tareas: 20 (consolidadas desde 34 originales)
- Total de grupos: 9 paralelos + 1 secuencial

---

## Referencias

**TAC-14 Course Materials**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-14_1.md`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-14_2.md`

**TAC-14 Reference Codebase**:
- `/Volumes/MAc1/Celes/TAC/tac-14`

**Completed Work (TAC-13)**:
- Act → Learn → Reuse cycle
- Expert system with expertise.yaml
- Default-ON for orchestrated workflows

---

## Resumen de Impacto

**Archivos nuevos**: ~150+
- Skills System (BASE + TEMPLATES)
- 7 Agent Definitions (BASE + TEMPLATES)
- 5 Orchestrator Commands (BASE + TEMPLATES)
- 6 Database Modules (BASE + TEMPLATES)
- 3 Workflows (BASE + TEMPLATES)
- 1 WebSocket Module (BASE + TEMPLATES)
- Orchestrator App (backend + frontend, BASE + TEMPLATES)
- Test Suites (BASE + TEMPLATES)
- 3 Utility Scripts (BASE + TEMPLATES)
- Documentación completa

**Archivos modificados**: ~8
- scaffold_service.py (registration de todos los templates)
- config.py (OrchestratorConfig)
- generator.py (conditional logic)
- 3 comandos existentes (plan, build, review)
- CLI README.md
- CHANGELOG.md
- pyproject.toml

**Nuevas dependencies**:
- Python: claude-agent-sdk, asyncpg, websockets, fastapi, uvicorn
- JavaScript: vue, typescript, vite

**Versión**: 0.7.x → **0.8.0**

---

FIN DEL PLAN
