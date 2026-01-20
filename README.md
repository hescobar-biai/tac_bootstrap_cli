# TAC Bootstrap

CLI en Python que crea o inyecta una **Agentic Layer** basada en Claude Code para acelerar ingenieria con patrones TAC (Tactical Agentic Coding).

## Problema que Resuelve

Muchos equipos usando IA siguen trabajando "en loop" (chat/IDE) y no logran:
- Estandarizar prompts de ingenieria
- Orquestar flujos repetibles (plan/build/test/review/ship)
- Ejecutar en paralelo (worktrees / entornos aislados)
- Tener trazabilidad completa (logs, specs, evidencias)
- Integrar triggers automaticos (cron/webhook/tareas)

## Solucion

TAC Bootstrap genera automaticamente toda la infraestructura agentica:

```
proyecto/
├── .claude/                    # Configuracion Claude Code
│   ├── settings.json           # Permisos y hooks
│   ├── commands/               # 25+ comandos slash
│   │   ├── prime.md            # Priming del agente
│   │   ├── feature.md          # Planificacion features
│   │   ├── implement.md        # Ejecucion de planes
│   │   └── ...
│   └── hooks/                  # Automatizacion
│       ├── pre_tool_use.py     # Validacion pre-ejecucion
│       └── post_tool_use.py    # Logging post-ejecucion
├── adws/                       # AI Developer Workflows
│   ├── adw_modules/            # Modulos compartidos
│   ├── adw_sdlc_iso.py         # Workflow SDLC completo
│   └── adw_triggers/           # Triggers automaticos
├── scripts/                    # Scripts de utilidad
├── specs/                      # Especificaciones
├── logs/                       # Logs de sesiones
└── config.yml                  # Fuente de verdad
```

## Comandos

```bash
# Crear proyecto nuevo con Agentic Layer
tac-bootstrap init my-project

# Inyectar Agentic Layer en proyecto existente
tac-bootstrap add-agentic --repo .

# Validar setup
tac-bootstrap doctor --repo .

# Re-generar desde config.yml
tac-bootstrap render --config config.yml
```

## Flujo de Usuario

```
tac-bootstrap init
       |
       v
¿Proyecto NUEVO o EXISTENTE?
       |
   [NUEVO]              [EXISTENTE]
       |                     |
       v                     v
  Pregunta:            Auto-detecta:
  - Lenguaje           - Lenguaje
  - Framework          - Framework
  - Arquitectura       - Package manager
  - Comandos
       |                     |
       v                     v
    GENERA AGENTIC LAYER
       |
       v
  Proyecto listo para
  trabajar con agentes!
```

## Stack Soportado

| Lenguaje | Frameworks | Package Managers |
|----------|------------|------------------|
| Python | FastAPI, Django, Flask | uv, poetry, pip |
| TypeScript | Next.js, Nest.js, Express | pnpm, npm, bun |
| JavaScript | Next.js, Express, React | pnpm, npm, bun |
| Go | Gin, Echo | go |

## Arquitecturas Soportadas

- **Simple** - Estructura plana
- **Layered** - Controllers/Services/Repositories
- **DDD** - Domain-Driven Design
- **Clean** - Clean Architecture
- **Hexagonal** - Ports & Adapters

---

## Desarrollo del Generador

Este repositorio contiene el codigo fuente del generador TAC Bootstrap.

### Estructura del Generador

```
tac_bootstrap/
├── .claude/                    # [TEMPLATE] Comandos y hooks de ejemplo
│   ├── commands/               # 25+ comandos slash como templates
│   └── hooks/                  # Hooks Python como templates
├── adws/                       # [TEMPLATE] AI Developer Workflows
│   ├── adw_modules/            # Modulos reutilizables
│   └── adw_triggers/           # Triggers para automatizacion
├── scripts/                    # [TEMPLATE] Scripts de utilidad
├── ai_docs/                    # Documentacion de referencia (TAC 1-8)
├── PLAN_TAC_BOOTSTRAP.md       # Plan de implementacion detallado
└── tac_bootstrap_cli/          # [A CREAR] CLI Python del generador
    ├── domain/models.py        # Modelos Pydantic
    ├── application/            # Servicios (scaffold, detect, doctor)
    ├── infrastructure/         # Templates Jinja2, filesystem
    └── interfaces/cli.py       # Comandos Typer
```

### Plan de Implementacion

Ver [PLAN_TAC_BOOTSTRAP.md](PLAN_TAC_BOOTSTRAP.md) para el plan completo con:
- 9 fases de desarrollo
- Cada tarea como prompt para agente LLM
- Codigo de templates completo
- Criterios de aceptacion

### Desarrollo con Agentic Coding

Cada tarea del plan esta escrita como un prompt completo. Para implementar:

```bash
# 1. Abrir el plan
cat PLAN_TAC_BOOTSTRAP.md

# 2. Copiar el prompt de la tarea (ej: TAREA 1.1)
# 3. Ejecutar con Claude Code
claude -p "[prompt de la tarea]"

# 4. Verificar criterios de aceptacion
# 5. Continuar con siguiente tarea
```

### Comandos Disponibles (Desarrollo)

```bash
# Slash commands para desarrollo
/prime              # Preparar contexto del proyecto
/feature            # Planificar nueva funcionalidad
/implement <plan>   # Ejecutar un plan
/test               # Correr tests
/commit             # Crear commit

# ADW Workflows
uv run adws/adw_sdlc_iso.py --issue 123
uv run adws/adw_patch_iso.py --issue 456 --fix "descripcion"
```

---

## Arquitectura Interna

### Modelos de Dominio

```python
# config.yml -> TACConfig
TACConfig
├── project: ProjectSpec       # nombre, lenguaje, framework, arquitectura
├── paths: PathsSpec           # rutas de directorios
├── commands: CommandsSpec     # start, test, lint, build
├── agentic: AgenticSpec       # worktrees, logging, safety
└── claude: ClaudeConfig       # settings.json, comandos
```

### Flujo de Generacion

```
config.yml
    |
    v
TACConfig (Pydantic validation)
    |
    v
ScaffoldService.build_plan()
    |
    v
ScaffoldPlan (lista de operaciones)
    |
    v
ScaffoldService.apply_plan()
    |
    v
Templates Jinja2 renderizados
    |
    v
Archivos generados en disco
```

---

## Referencia: Curso TAC

Este proyecto implementa los conceptos del curso **Tactical Agentic Coding (TAC)**:

| Leccion | Concepto | Implementacion |
|---------|----------|----------------|
| TAC-1 | Stop Coding | CLI genera codigo, no lo escribes |
| TAC-2 | KPIs Agenticos | Tracking en adw_modules |
| TAC-3 | Templates | .claude/commands/*.md |
| TAC-4 | ADWs | adws/*.py workflows |
| TAC-5 | Feedback Loops | hooks/ + tests |
| TAC-6 | Review & Document | /review, /document |
| TAC-7 | Zero-Touch | adw_sdlc_zte_iso.py |
| TAC-8 | Prioritize Agentics | 50%+ tiempo en capa agentica |

Ver [ai_docs/doc/](ai_docs/doc/) para documentacion completa del curso.

---

## Licencia

MIT
