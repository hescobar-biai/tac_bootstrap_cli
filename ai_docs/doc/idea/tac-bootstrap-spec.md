# TAC Bootstrap — Especificación de Producto y Diseño Técnico (v1)

> **Resumen**: *TAC Bootstrap* es una CLI/app en Python que **crea** (proyecto nuevo) o **inyecta** (proyecto existente) una **Agentic Layer** basada en *Claude Code* para acelerar ingeniería con patrones de *Tactical Agentic Coding (TAC)*: prompts, templates (meta-prompts), ADWs (AI Developer Workflows), triggers, logs y una carpeta `.claude/` lista para operar.

---

## 1) Objetivo del producto

### Problema que resuelve
Hoy, incluso usando IA, muchos equipos siguen trabajando “en loop” (chat/IDE) y no logran:
- estandarizar prompts de ingeniería
- orquestar flujos repetibles (plan/build/test/review/ship)
- ejecutar en paralelo (worktrees / entornos aislados)
- tener trazabilidad completa (logs, specs, evidencias)
- integrar un sistema de *triggers* (cron/webhook/tareas)

### Solución
Una herramienta que:
1) Le pregunta al usuario si el proyecto es **nuevo** o **existente**.
2) Recoge decisiones claves (lenguaje, framework, arquitectura, comandos).
3) Genera la **estructura inicial** del proyecto (si es nuevo).
4) Genera o inyecta la **Agentic Layer TAC**, incluyendo **`.claude/`**.
5) Deja el repo listo para operar *in-loop* y *out-loop* con flujos ADW.

### Resultado esperado
- Reducir tiempo de “setup agentic” de días/semanas a **minutos**
- Estandarizar “cómo se hace ingeniería con agentes” en un repo
- Preparar el terreno para *outloop* y luego *ZTE* (zero-touch engineering)

---

## 2) Alcance del MVP (v1)

### Incluye (MVP)
- CLI en Python: `tac-bootstrap`
- Modo **new**: genera app base + agentic layer
- Modo **existing**: solo inyecta agentic layer
- Plantillas base:
  - `.claude/settings.json`
  - `.claude/commands/*.md` (prime/start/build/test/review/ship)
  - `prompts/templates/*.md` (chore/feature/plan)
  - `adws/` con módulos mínimos + flujos SDLC
- `config.yml` (declarativo) para:
  - stack del proyecto
  - comandos de ejecución/validación
  - preferencias de worktrees y logging
  - rutas de app/agentic layer
- `doctor`: valida setup y sugiere correcciones
- `README.md` generado para operación

### No incluye (v1)
- Integración real con GitHub Issues / Notion (se deja “stub”)
- Autodeploy a cloud (se deja como plantilla)
- Observabilidad avanzada (OpenTelemetry) (se deja para v2)
- Plugins “por framework” muy extensos (se agregan iterativamente)

---

## 3) Experiencia de usuario (UX) — Flujos

### 3.1 Comandos principales
- `tac-bootstrap init`  
  Crea proyecto nuevo (app + agentic layer).

- `tac-bootstrap add-agentic --repo .`  
  Inyecta agentic layer en un repo existente.

- `tac-bootstrap doctor --repo .`  
  Valida `.claude/`, comandos, rutas, dependencias y comandos de build/test.

- `tac-bootstrap render --config config.yml`  
  Re-genera / sincroniza artefactos de la agentic layer desde el YAML (idempotente).

### 3.2 Wizard: proyecto nuevo
Preguntas mínimas:
1) Nombre del proyecto
2) Lenguaje (`python|javascript|typescript|go|...`)
3) Framework (depende del lenguaje)
4) Arquitectura (`ddd|clean|hexagonal|layered|simple`)
5) Package manager (ej: `uv|poetry|pip`, `pnpm|npm|bun`)
6) Comandos: `start`, `test`, `lint`, `typecheck`, `build` (defaults + editable)
7) Ruta de app (ej: `apps/api`, `src`, `backend`)

Entrega:
- skeleton del framework + arquitectura elegida
- agentic layer instalada y configurada

### 3.3 Wizard: proyecto existente
Preguntas mínimas:
1) Ruta del repo
2) Tipo (`backend|frontend|monorepo`) o auto-detect
3) Dónde instalar agentic layer (default: root con `adws/`, `prompts/`, `.claude/`)
4) Comandos reales de `start/test/lint/typecheck/build`
5) Estrategia de worktrees (on/off + carpeta `trees/`)

Entrega:
- agentic layer injertada sin modificar el app (mínimamente invasivo)

---

## 4) Principios de diseño

1) **Separación estricta**: Application Layer vs Agentic Layer  
2) **Idempotencia**: correr la herramienta 2 veces no debe romper nada  
3) **Declarativo primero**: `config.yml` es la fuente de verdad  
4) **Plantillas versionadas**: templates versionadas por release del generador  
5) **Extensible por plugins**: “drivers” por lenguaje/framework  
6) **Trazabilidad por defecto**: logs + specs + evidencias

---

## 5) Estructura recomendada (repositorio generado)

> Estructura base compatible con Claude Code: **incluye `.claude/`**

```text
<repo>/
  .claude/
    settings.json
    commands/
      prime.md
      start.md
      build.md
      test.md
      review.md
      ship.md
    hooks/                      # opcional (v2)
  adws/
    README.md
    adw_modules/
      agent.py                  # invocación agente / CLI wrapper
      workflow_ops.py           # orquestación (plan/build/test/review/ship)
      worktree_ops.py           # git worktrees (aislamiento)
      git_ops.py
      fs_ops.py
      logger.py
      state.py
      utils.py
    workflows/
      sdlc_iso.py               # Plan->Build->Test->Review->Ship (isolated)
      patch_iso.py              # flujo corto para fixes simples
      plan_implement.py         # arquitecto/editor
      build_update_task.py      # tareas tipo lista/board (v2 stub)
    triggers/
      trigger_cron.py           # cron / once
      trigger_webhook.py        # stub
  prompts/
    templates/
      plan.md
      chore.md
      feature.md
      review.md
    commands/                   # prompts usados por .claude/commands
      prime.md
      start.md
      build.md
      test.md
      ship.md
  specs/
    README.md
    issue-0001.md
  logs/
    .gitkeep
  ai_docs/
    README.md
  app_docs/
    README.md
  scripts/
    start.sh
    test.sh
    lint.sh
    typecheck.sh
    build.sh
  config.yml
  .env.sample
  .gitignore
  README.md
```

**Notas**
- `.claude/commands/*.md` apunta a prompts/acciones reales de tu repo.
- `adws/` es el “motor” que combina *código determinista* + *prompts no deterministas*.
- `scripts/` expone comandos estables para que agentes los usen como “feedback loops”.

---

## 6) Configuración declarativa — `config.yml` (Fuente de verdad)

### 6.1 Objetivo del YAML
- Evitar hardcode por repo
- Parametrizar prompts, ADWs, comandos y rutas
- Hacer reproducible el setup en equipos/CI

### 6.2 Esquema propuesto (v1)

```yaml
version: 1

project:
  name: "my-project"
  mode: "new"              # new | existing
  repo_root: "."           # ruta del repo
  language: "python"       # python|typescript|javascript|go|...
  framework: "fastapi"     # depende del lenguaje
  architecture: "ddd"      # ddd|clean|hexagonal|layered|simple
  package_manager: "uv"    # uv|poetry|pip|pnpm|npm|bun|go

paths:
  app_root: "apps/api"     # dónde vive el código de la app
  agentic_root: "."        # dónde vive la agentic layer (root recomendado)
  prompts_dir: "prompts"
  adws_dir: "adws"
  specs_dir: "specs"
  logs_dir: "logs"
  scripts_dir: "scripts"
  worktrees_dir: "trees"   # si se usa

commands:
  start: "uv run python -m apps.api"
  build: "uv run python -m compileall apps/api"
  test: "uv run pytest -q"
  lint: "uv run ruff check ."
  typecheck: "uv run mypy ."
  format: "uv run ruff format ."

agentic:
  provider: "claude_code"  # claude_code (v1)
  model_policy:            # no bloquea, solo guía templates
    default: "sonnet"
    heavy: "opus"
  worktrees:
    enabled: true
    max_parallel: 5
    naming: "feat-{slug}-{timestamp}"
  logging:
    level: "INFO"
    capture_agent_transcript: true
    run_id_strategy: "uuid"    # uuid|timestamp
  safety:
    require_tests_pass: true
    require_review_artifacts: true
    allowed_paths:
      - "apps/"
      - "src/"
      - "adws/"
      - "prompts/"
      - "specs/"
      - "scripts/"
    forbidden_paths:
      - ".env"
      - "secrets/"
  workflows:
    default: "sdlc_iso"
    available:
      - "sdlc_iso"
      - "patch_iso"
      - "plan_implement"

claude:
  settings:
    # contenido a renderizar a .claude/settings.json
    project_name: "my-project"
    preferred_style: "concise"
    allow_shell: true
  commands:
    # mapea slash commands -> prompt files / adws
    prime: ".claude/commands/prime.md"
    start: ".claude/commands/start.md"
    build: ".claude/commands/build.md"
    test: ".claude/commands/test.md"
    review: ".claude/commands/review.md"
    ship: ".claude/commands/ship.md"

templates:
  # templates/meta-prompts para problem classes
  plan_template: "prompts/templates/plan.md"
  chore_template: "prompts/templates/chore.md"
  feature_template: "prompts/templates/feature.md"
  review_template: "prompts/templates/review.md"

bootstrap:
  # solo para modo new
  create_git_repo: true
  initial_commit: true
  license: "MIT"
  readme: true
```

### 6.3 Ejemplo minimal (existing)
```yaml
version: 1
project:
  name: "existing-repo"
  mode: "existing"
  repo_root: "."
  language: "typescript"
  framework: "next"
  architecture: "clean"
  package_manager: "pnpm"

paths:
  app_root: "apps/web"
  agentic_root: "."
  worktrees_dir: "trees"

commands:
  start: "pnpm -C apps/web dev"
  test: "pnpm -C apps/web test"
  lint: "pnpm -C apps/web lint"
  build: "pnpm -C apps/web build"

agentic:
  provider: "claude_code"
  worktrees:
    enabled: true
    max_parallel: 3
```

---

## 7) `.claude/` — Requisito clave

### 7.1 ¿Qué debe contener?
- `settings.json`: preferencias del proyecto para Claude Code
- `commands/*.md`: comandos slash reutilizables

### 7.2 Comandos recomendados (mínimo)
- `prime.md`: “priming” del agente (contexto + reglas + rutas + comandos)
- `start.md`: cómo correr el stack
- `build.md`: build / compile
- `test.md`: tests (feedback loop)
- `review.md`: checklist de revisión y artefactos (screenshots/logs)
- `ship.md`: lineamientos para PR/merge/release

### 7.3 Ejemplo de `prime.md` (estructura)
- Objetivo del repo
- Arquitectura (DDD/Clean/etc.)
- Carpetas importantes
- Comandos estables (start/test/lint/build)
- Reglas de edición (no tocar secretos, no romper APIs)
- Definición de “hecho” (tests pasan, lint pasa, docs mínimas)

---

## 8) ADWs (AI Developer Workflows)

### 8.1 ¿Qué son?
Scripts (Python/UV recomendado) que combinan:
- prompts (Claude Code)
- comandos deterministas (tests, lint, build)
- control de estado (worktrees, logs, specs)

### 8.2 Workflows base (v1)
1) **SDLC ISO** (*end-to-end aislado*)  
   Plan → Build → Test → Review → Ship  
2) **Patch ISO** (*fix rápido*)  
   Build → Test → Ship (o solo Build/Test)  
3) **Plan + Implement** (*arquitecto/editor*)  
   - Agente A crea plan
   - Agente B implementa siguiendo plan

### 8.3 Contrato de outputs
Todo workflow debe producir:
- `logs/<run_id>/transcript.md`
- `specs/<ticket_or_run>.md` (opcional pero recomendado)
- `review_artifacts/` (si aplica)
- commit message estándar

---

## 9) Triggers (Outloop)

### v1 (básico)
- `trigger_cron.py` con:
  - `--once` (para pruebas)
  - `--interval-seconds 15` (polling)
- Fuente de tareas:
  - v1: `specs/` o `tasks.md` (simple)
  - v2: GitHub Issues / Notion / Jira

### Peter framework (referencia)
- Prompt Input (tareas/issue)
- Trigger Environment (cron/webhook)
- Review System (PR, logs, board, etc.)

---

## 10) Arquitectura interna del generador (Python)

### Stack recomendado
- **Typer** (CLI)
- **Jinja2** (templates)
- **Pydantic** (schema del YAML)
- **Rich** (UI terminal)
- **PyYAML** (lectura YAML)
- **GitPython** (opcional) para init/commit

### Paquetes internos (estructura del generador)
```text
tac_bootstrap/
  domain/
    models.py            # ProjectSpec, Paths, Commands, AgenticSpec
  application/
    scaffold_service.py  # build_plan + apply_plan
    detect_service.py    # auto-detect de stack
    doctor_service.py    # validación setup
  infrastructure/
    template_repo.py     # load templates (tac-7 como base)
    fs.py                # file operations idempotentes
    patcher.py           # patch seguro de archivos
    git_adapter.py       # init repo / commits
  interfaces/
    cli.py               # typer commands
  templates/
    (copias parametrizables del tac-7)
```

---

## 11) “Doctor” (validador) — checklist

Valida:
- Existe `.claude/settings.json`
- Existen `.claude/commands/*.md`
- `config.yml` presente y consistente
- Comandos declarados funcionan (o al menos existen scripts)
- Rutas `app_root` existen
- Si `worktrees.enabled=true`, existe `worktrees_dir` y git está inicializado
- `scripts/` incluye wrappers para start/test/lint/build (recomendado)

Salida:
- reporte con ✅ / ⚠️ / ❌
- sugerencias de fix automáticas (cuando sea seguro)

---

## 12) Roadmap sugerido

### v1 (MVP)
- CLI + YAML + `.claude/` + prompts/templates + ADWs base + doctor

### v1.1
- auto-detect real de frameworks (FastAPI/Next/Nest/etc.)
- mejores defaults por stack
- más plantillas de arquitectura (DDD/Clean/Hexagonal)

### v2
- GitHub Issues trigger (webhook + parser)
- Notion board trigger
- PR automation (crear PR, labels, reviewers)
- Review artifacts automáticos (screenshots/logs)
- Integración CI (ejecutar ADWs en CI runner)

### v3
- Observabilidad (OpenTelemetry + métricas KPIs agentic)
- Catálogo de “problem classes” por dominio (data/etl/web/mobile)

---

## 13) KPIs (para vender la idea)

- **Setup time**: minutos para dejar `.claude/` + ADWs listos
- **Attempt reduction**: menos iteraciones humanas para entregar un cambio
- **Work size**: tamaño de cambios que el agente entrega por ejecución
- **Streak**: rachas de ejecuciones exitosas
- **Presence**: tiempo humano requerido (objetivo: tender a 0)

---

## 14) Entregables para el equipo que lo va a desarrollar

1) Repo `tac-bootstrap` (Python) con CLI + templates  
2) `templates/` basado en el zip `tac-7` (parametrizable)  
3) `config.yml` schema + validación pydantic  
4) `README` del generador con ejemplos:
   - new: fastapi+ddd
   - existing: nextjs+clean
5) Tests mínimos:
   - genera estructura correcta
   - idempotencia
   - doctor report

---

## 15) Ejemplo de “pitch” (para tu idea)

> “Queremos un generador que cree o inyecte una *Agentic Layer* estándar en cualquier repo, siguiendo TAC.  
> La herramienta produce `.claude/`, prompts, templates y workflows (ADWs) que combinan agentes y comandos deterministas para entregar cambios repetibles con trazabilidad.  
> El setup se controla desde `config.yml`, permitiendo que equipos adopten agentic engineering de forma consistente.”

---

## 16) Checklist final de definición de hecho (Definition of Done) para v1

- [ ] `tac-bootstrap init` crea repo funcional (app mínima + agentic layer)
- [ ] `tac-bootstrap add-agentic` injerta agentic layer sin romper app
- [ ] `.claude/commands` operables y coherentes con `config.yml`
- [ ] ADWs SDLC/Patch/PlanImplement ejecutan y escriben logs
- [ ] `doctor` detecta fallas comunes y sugiere fixes
- [ ] Documentación lista para presentación a un equipo

---

## Anexo A — Recomendación sobre plantilla base (`tac-7.zip`)
Tu zip es un excelente baseline porque ya trae:
- `.claude/settings.json` + `.claude/commands/`
- `adws/` + módulos y workflows
- `specs/`, `logs/`, `scripts/`, `ai_docs/`, `app_docs/`

El trabajo del generador es:
1) convertirlo en **template parametrizable**
2) renderizarlo según `config.yml`
3) ajustar comandos / rutas / scripts según stack del usuario
