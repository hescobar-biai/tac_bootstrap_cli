# Plan de tareas — TAC Bootstrap (mejoras)

Orden sugerido de ejecucion. Cada tarea indica tipo al inicio y especifica archivo raiz y template.

---

## 1) [Bug] Corregir estructura y consistencia de `config.yml` con el schema actual

### Archivos a modificar
- **Archivo raiz**: `config.yml`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`

### Contexto
El archivo `config.yml` actual tiene claves que estan fuera de sus secciones correspondientes segun el modelo `TACConfig` definido en `tac_bootstrap_cli/tac_bootstrap/domain/models.py`. Esto causa errores de validacion al cargar la configuracion.

### Problema especifico
Las siguientes claves estan mal ubicadas en `config.yml`:
1. `allowed_paths` y `forbidden_paths` estan a nivel raiz, pero deben estar dentro de `agentic.safety`
2. `workflows` a nivel raiz tiene estructura incorrecta - debe estar dentro de `agentic.workflows`
3. Falta la seccion `claude` con `settings` y `commands`
4. Las claves `workflows.settings` y `workflows.commands` no corresponden al schema

### Estructura correcta segun TACConfig
```yaml
version: "0.x.x"
schema_version: 1

project:
  name: "..."
  mode: "existing"
  repo_root: "."
  language: "python"
  framework: "none"
  architecture: "ddd"
  package_manager: "uv"

paths:
  app_root: "..."
  agentic_root: "."
  prompts_dir: "prompts"
  adws_dir: "adws"
  specs_dir: "specs"
  logs_dir: "logs"
  scripts_dir: "scripts"
  worktrees_dir: "trees"

commands:
  start: "..."
  test: "..."
  lint: "..."
  typecheck: "..."
  format: "..."
  build: "..."

agentic:
  provider: "claude_code"
  target_branch: "main"
  model_policy:
    default: "sonnet"
    heavy: "opus"
  worktrees:
    enabled: true
    max_parallel: 5
    naming: "feat-{slug}-{timestamp}"
  logging:
    level: "INFO"
    capture_agent_transcript: true
    run_id_strategy: "uuid"
  safety:
    require_tests_pass: true
    require_review_artifacts: true
    allowed_paths:
      - "tac_bootstrap_cli/"
      - "adws/"
      - "scripts/"
      - "specs/"
      - "tests/"
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
    project_name: "tac-bootstrap"
    preferred_style: "concise"
    allow_shell: true
  commands:
    prime: ".claude/commands/prime.md"
    start: ".claude/commands/start.md"
    build: ".claude/commands/build.md"
    test: ".claude/commands/test.md"
    review: ".claude/commands/review.md"
    ship: ".claude/commands/ship.md"

templates:
  plan_template: "prompts/templates/plan.md"
  chore_template: "prompts/templates/chore.md"
  feature_template: "prompts/templates/feature.md"
  bug_template: "prompts/templates/bug.md"
  review_template: "prompts/templates/review.md"

bootstrap:
  create_git_repo: false
  initial_commit: false
  license: "MIT"
  readme: true
```

### Pasos a ejecutar
1. Leer el archivo `config.yml` actual
2. Leer el modelo `TACConfig` en `tac_bootstrap_cli/tac_bootstrap/domain/models.py` para confirmar estructura
3. Reorganizar las claves del `config.yml` para que coincidan con el schema:
   - Mover `allowed_paths` y `forbidden_paths` dentro de `agentic.safety`
   - Reestructurar `workflows` dentro de `agentic.workflows` con solo `default` y `available`
   - Agregar seccion `claude` con `settings` y `commands`
   - Eliminar claves que no pertenecen al schema (`workflows.settings`, `workflows.commands` a nivel raiz)
4. Actualizar el template Jinja2 `config.yml.j2` para que genere la estructura correcta
5. Verificar que la configuracion carga sin errores

### Criterios de aceptacion
- [ ] El archivo `config.yml` tiene todas las claves dentro de sus secciones correctas segun `TACConfig`
- [ ] No hay claves a nivel raiz que no esten en el schema (`allowed_paths`, `forbidden_paths`, `workflows` mal estructurado)
- [ ] El template `config.yml.j2` genera YAML con la estructura correcta
- [ ] El comando de validacion ejecuta sin errores:
  ```bash
  cd tac_bootstrap_cli && uv run python -c "
  import yaml
  from tac_bootstrap.domain.models import TACConfig
  with open('../config.yml') as f:
      data = yaml.safe_load(f)
  config = TACConfig(**data)
  print('Validacion exitosa:', config.project.name)
  "
  ```

---

## 2) [Feature] Agregar modo de ejecucion unica (`--once`) en triggers cron

### Archivos a modificar
- **Archivo raiz**: `adws/adw_triggers/trigger_cron.py`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2`

### Contexto
El trigger cron actualmente solo funciona en modo bucle infinito con scheduler. Para pruebas y debugging es necesario poder ejecutar un solo ciclo de verificacion y terminar limpiamente.

### Comportamiento actual
```python
def main():
    # ... setup ...
    schedule.every(interval).seconds.do(check_and_process_issues)
    check_and_process_issues()  # Initial check
    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)
```

### Comportamiento esperado con `--once`
```python
def main():
    args = parse_args()
    # ... setup ...

    if args.once:
        # Single execution mode
        print("INFO: Running single check cycle (--once mode)")
        check_and_process_issues()
        print("INFO: Single cycle complete, exiting")
        return

    # Normal loop mode
    schedule.every(interval).seconds.do(check_and_process_issues)
    check_and_process_issues()
    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)
```

### Pasos a ejecutar
1. Abrir `adws/adw_triggers/trigger_cron.py`
2. En la funcion `parse_args()`, agregar el argumento `--once`:
   ```python
   parser.add_argument(
       "--once",
       action="store_true",
       default=False,
       help="Run a single check cycle and exit (useful for testing)",
   )
   ```
3. En la funcion `main()`, agregar la logica condicional:
   - Si `args.once` es True: ejecutar `check_and_process_issues()` una vez y retornar
   - Si `args.once` es False: continuar con el bucle normal del scheduler
4. Actualizar el docstring del modulo para documentar el nuevo flag
5. Replicar los mismos cambios en el archivo template `trigger_cron.py.j2`

### Criterios de aceptacion
- [ ] El argumento `--once` esta disponible en el parser
- [ ] `uv run adws/adw_triggers/trigger_cron.py --once` ejecuta exactamente UN ciclo de verificacion
- [ ] El script termina con codigo de salida 0 despues del ciclo unico
- [ ] El modo normal (sin `--once`) sigue funcionando con el bucle infinito
- [ ] El template `.j2` tiene los mismos cambios
- [ ] Verificar con:
  ```bash
  # Debe ejecutar un ciclo y terminar
  timeout 10 uv run adws/adw_triggers/trigger_cron.py --once && echo "SUCCESS: Exited cleanly"

  # Verificar que el help muestra el nuevo flag
  uv run adws/adw_triggers/trigger_cron.py --help | grep -A1 "\-\-once"
  ```

---

## 3) [Feature] Agregar modo de ejecucion unica (`--once`) en trigger de cadena

### Archivos a modificar
- **Archivo raiz**: `adws/adw_triggers/trigger_issue_chain.py`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2`

### Contexto
Similar al trigger cron, el trigger de cadena necesita un modo de ejecucion unica para validar rapidamente el orden de issues sin entrar en un bucle infinito.

### Comportamiento actual
```python
def main():
    args = parse_args()
    issue_chain = resolve_issue_chain(args)
    # ... setup ...
    schedule.every(interval).seconds.do(check_and_process_issues, issue_chain)
    check_and_process_issues(issue_chain)
    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)
```

### Comportamiento esperado con `--once`
```python
def main():
    args = parse_args()
    issue_chain = resolve_issue_chain(args)
    # ... setup ...

    if args.once:
        print("INFO: Running single chain check cycle (--once mode)")
        check_and_process_issues(issue_chain)
        print("INFO: Single cycle complete, exiting")
        return

    # Normal loop mode
    schedule.every(interval).seconds.do(check_and_process_issues, issue_chain)
    check_and_process_issues(issue_chain)
    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)
```

### Pasos a ejecutar
1. Abrir `adws/adw_triggers/trigger_issue_chain.py`
2. En la funcion `parse_args()`, agregar el argumento `--once`:
   ```python
   parser.add_argument(
       "--once",
       action="store_true",
       default=False,
       help="Run a single chain check cycle and exit (useful for testing)",
   )
   ```
3. En la funcion `main()`, agregar la logica condicional despues de `resolve_issue_chain(args)`:
   - Si `args.once` es True: ejecutar `check_and_process_issues(issue_chain)` una vez y retornar
   - Si `args.once` es False: continuar con el bucle normal
4. Actualizar el docstring del modulo para incluir ejemplo con `--once`
5. Replicar los mismos cambios en el archivo template `trigger_issue_chain.py.j2`

### Criterios de aceptacion
- [ ] El argumento `--once` esta disponible en el parser
- [ ] `uv run adws/adw_triggers/trigger_issue_chain.py --issues 1,2,3 --once` ejecuta un ciclo y termina
- [ ] El script verifica el primer issue abierto de la cadena y sale
- [ ] El modo normal (sin `--once`) sigue funcionando con el bucle infinito
- [ ] El template `.j2` tiene los mismos cambios
- [ ] Verificar con:
  ```bash
  # Debe ejecutar un ciclo y terminar (usa issues ficticios para test)
  timeout 10 uv run adws/adw_triggers/trigger_issue_chain.py --issues 1 --once && echo "SUCCESS: Exited cleanly"

  # Verificar que el help muestra el nuevo flag
  uv run adws/adw_triggers/trigger_issue_chain.py --help | grep -A1 "\-\-once"
  ```

---

## 4) [Feature] Documentar el trigger de cadena en el README de ADWs

### Archivos a modificar
- **Archivo raiz**: `adws/README.md`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`

### Contexto
El README actual de ADWs documenta `trigger_cron.py` y `trigger_webhook.py`, pero no incluye documentacion para `trigger_issue_chain.py`. Los usuarios necesitan saber como usar este trigger para procesar issues en orden secuencial.

### Ubicacion en el README
Agregar una nueva subseccion dentro de "### Automation Triggers" (linea ~333), despues de la documentacion de `trigger_cron.py`.

### Contenido a agregar
```markdown
#### trigger_issue_chain.py - Sequential Issue Processing
Processes issues in a specific order, waiting for each to close before starting the next.

**Usage:**
```bash
# Process issues 123, 456, 789 in order
uv run adw_triggers/trigger_issue_chain.py 123 456 789

# Using comma-separated format
uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789

# Custom polling interval (default: 20 seconds)
uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --interval 30

# Single check cycle (for testing)
uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --once
```

**Behavior:**
- Only processes the first OPEN issue in the chain
- Waits for issue N to be CLOSED before processing issue N+1
- Polls GitHub at configurable intervals to check issue status
- Supports all workflow triggers (adw_plan_iso, adw_sdlc_iso, etc.)

**Use Cases:**
- Processing dependent issues in sequence
- Ensuring ordered feature implementation
- Batch processing with dependencies between tasks

**Example Workflow:**
1. Create issues #10, #11, #12 with dependencies
2. Run: `uv run adw_triggers/trigger_issue_chain.py --issues 10,11,12`
3. Trigger starts processing #10
4. When #10 is closed (manually or by merged PR), trigger processes #11
5. Process continues until all issues are closed
```

### Pasos a ejecutar
1. Abrir `adws/README.md`
2. Localizar la seccion "### Automation Triggers" (aproximadamente linea 333)
3. Despues del bloque de `trigger_cron.py` y antes de `trigger_webhook.py`, insertar la nueva seccion documentando `trigger_issue_chain.py`
4. Asegurar que el formato markdown es consistente con el resto del documento
5. Replicar los mismos cambios en el archivo template `README.md.j2`

### Criterios de aceptacion
- [ ] El README incluye seccion completa para `trigger_issue_chain.py`
- [ ] La documentacion explica el comportamiento de espera hasta cierre del issue anterior
- [ ] Incluye al menos 4 ejemplos de comando (posicional, --issues, --interval, --once)
- [ ] Describe los casos de uso principales
- [ ] El formato es consistente con el resto del README
- [ ] El template `.j2` tiene los mismos cambios
- [ ] Verificar con:
  ```bash
  # Verificar que la seccion existe
  grep -A5 "trigger_issue_chain.py" adws/README.md

  # Verificar ejemplos de comando
  grep "\-\-issues" adws/README.md | head -3
  ```

---

## 5) [Chore] Enumerar triggers disponibles en paquete `adw_triggers`

### Archivos a modificar
- **Archivo raiz**: `adws/adw_triggers/__init__.py`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`

### Contexto
El archivo `__init__.py` del paquete `adw_triggers` actualmente solo contiene un comentario basico. Necesita un docstring completo que liste todos los triggers disponibles y su proposito, sirviendo como documentacion de referencia rapida.

### Contenido actual
```python
# ADW Triggers Package
```

### Contenido esperado
```python
"""
ADW Triggers Package - Automation entry points for AI Developer Workflows.

This package contains trigger scripts that monitor GitHub and automatically
invoke ADW workflows based on events or schedules.

Available Triggers:
    trigger_cron.py
        Polling-based monitor that checks GitHub issues at regular intervals.
        Detects workflow commands (adw_plan_iso, adw_sdlc_iso, etc.) in issue
        bodies or comments and triggers the corresponding workflow.
        Usage: uv run adw_triggers/trigger_cron.py [--interval N] [--once]

    trigger_issue_chain.py
        Sequential issue processor that handles issues in a specific order.
        Only processes issue N+1 after issue N is closed, enabling dependent
        workflows and ordered batch processing.
        Usage: uv run adw_triggers/trigger_issue_chain.py --issues 1,2,3 [--once]

    trigger_webhook.py
        Real-time webhook server that receives GitHub events instantly.
        Faster response than polling but requires public endpoint and
        webhook configuration in GitHub repository settings.
        Usage: uv run adw_triggers/trigger_webhook.py [--port N]

Common Features:
    - All triggers support workflow detection via keywords (adw_plan_iso, etc.)
    - All triggers post status comments to GitHub issues
    - All triggers create isolated worktrees for parallel execution
    - Graceful shutdown on SIGINT/SIGTERM signals

Environment Variables:
    GITHUB_TOKEN or gh auth: GitHub authentication
    ANTHROPIC_API_KEY: Claude API access
    GITHUB_WEBHOOK_SECRET: (webhook only) Signature validation

See Also:
    - adws/README.md for complete documentation
    - config.yml for interval and workflow configuration
"""
```

### Pasos a ejecutar
1. Abrir `adws/adw_triggers/__init__.py`
2. Reemplazar el contenido actual con el docstring completo mostrado arriba
3. Verificar que el docstring es accesible via `help()` o `__doc__`
4. Replicar los mismos cambios en el archivo template `__init__.py.j2`

### Criterios de aceptacion
- [ ] El archivo `__init__.py` contiene docstring completo con todos los triggers
- [ ] Cada trigger tiene: nombre, descripcion breve, y ejemplo de uso
- [ ] El docstring incluye seccion de variables de entorno requeridas
- [ ] El docstring es accesible programaticamente
- [ ] El template `.j2` tiene los mismos cambios
- [ ] Verificar con:
  ```bash
  # Verificar que el docstring es accesible
  uv run python -c "import sys; sys.path.insert(0, 'adws'); from adw_triggers import __doc__; print(__doc__[:200])"

  # Verificar que menciona los tres triggers
  grep -c "trigger_" adws/adw_triggers/__init__.py  # Debe ser >= 3
  ```

---

## 6) [Feature] Incluir configuracion de intervalos en docs de triggers

### Archivos a modificar
- **Archivo raiz**: `adws/README.md`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`

### Contexto
El README de ADWs no documenta claramente como configurar los intervalos de polling para los triggers. Los usuarios necesitan saber:
1. Cual es el intervalo por defecto (20 segundos)
2. Como cambiarlo via CLI (`--interval`)
3. Si existe configuracion en `config.yml` (actualmente no, pero podria agregarse)

### Ubicacion en el README
Agregar una nueva subseccion dentro de "## Configuration" (aproximadamente linea 604), despues de "### ADW Tracking".

### Contenido a agregar
```markdown
### Trigger Polling Configuration

ADW triggers use polling intervals to check GitHub for new workflow commands.

#### Default Interval
All polling-based triggers default to **20 seconds** between checks.

#### Overriding via CLI
Use the `--interval` or `-i` flag to customize:

```bash
# Poll every 30 seconds
uv run adw_triggers/trigger_cron.py --interval 30

# Poll every 60 seconds
uv run adw_triggers/trigger_issue_chain.py --issues 1,2,3 -i 60
```

#### Recommended Intervals
| Use Case | Interval | Rationale |
|----------|----------|-----------|
| Development/Testing | 10-20s | Fast feedback during testing |
| Production (light usage) | 30-60s | Balance responsiveness and API limits |
| Production (heavy usage) | 60-120s | Avoid GitHub API rate limiting |
| CI/CD Integration | Use `--once` | Single execution, no polling |

#### API Rate Limiting
GitHub's API allows 5,000 requests/hour for authenticated users. Each polling cycle makes approximately 1-3 API calls depending on open issues. With default 20s interval:
- ~180 cycles/hour
- ~180-540 API calls/hour
- Safe margin for other operations

For repositories with many open issues, consider increasing the interval.
```

### Pasos a ejecutar
1. Abrir `adws/README.md`
2. Localizar la seccion "## Configuration" (aproximadamente linea 604)
3. Despues de "### ADW Tracking", agregar la nueva subseccion "### Trigger Polling Configuration"
4. Incluir tabla de intervalos recomendados y explicacion de rate limiting
5. Replicar los mismos cambios en el archivo template `README.md.j2`

### Criterios de aceptacion
- [ ] El README incluye seccion "### Trigger Polling Configuration"
- [ ] Documenta el valor por defecto de 20 segundos
- [ ] Muestra ejemplos de como usar `--interval` y `-i`
- [ ] Incluye tabla de intervalos recomendados por caso de uso
- [ ] Menciona consideraciones de rate limiting de GitHub API
- [ ] El template `.j2` tiene los mismos cambios
- [ ] Verificar con:
  ```bash
  # Verificar que la seccion existe
  grep -A3 "Trigger Polling Configuration" adws/README.md

  # Verificar que menciona el default
  grep "20 seconds" adws/README.md

  # Verificar tabla de intervalos
  grep -c "Interval" adws/README.md  # Debe ser >= 2
  ```

---

## 7) [Chore] Actualizar CHANGELOG con nueva version

### Archivos a modificar
- **Archivo raiz**: `CHANGELOG.md`
- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2` (crear si no existe)

### Contexto
Despues de completar las tareas anteriores, es necesario documentar los cambios en el CHANGELOG siguiendo el formato Keep a Changelog y Semantic Versioning.

### Determinar version
- Si solo hay fixes de bugs: incrementar PATCH (0.x.Y)
- Si hay nuevas features sin breaking changes: incrementar MINOR (0.X.0)
- El conjunto de cambios incluye:
  - 1 bug fix (config.yml)
  - 2 features (--once en triggers)
  - 3 mejoras de documentacion
  - **Recomendacion**: incrementar MINOR por las nuevas features

### Formato del CHANGELOG
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.X.0] - YYYY-MM-DD

### Added
- `--once` flag in `trigger_cron.py` for single execution cycle
- `--once` flag in `trigger_issue_chain.py` for single execution cycle
- Documentation for `trigger_issue_chain.py` in ADWs README
- Trigger polling configuration section in ADWs README
- Complete docstring in `adw_triggers/__init__.py` with all available triggers

### Fixed
- `config.yml` structure aligned with `TACConfig` schema
- Moved `allowed_paths` and `forbidden_paths` into `agentic.safety` section
- Restructured `workflows` configuration under `agentic.workflows`
- Added missing `claude` configuration section

### Changed
- N/A

## [0.X-1.0] - Previous date
...
```

### Pasos a ejecutar
1. Determinar la version actual leyendo `CHANGELOG.md` o `pyproject.toml`
2. Calcular la nueva version (MINOR bump por features)
3. Abrir `CHANGELOG.md` (o crearlo si no existe)
4. Agregar nueva entrada con:
   - Numero de version siguiendo SemVer
   - Fecha en formato YYYY-MM-DD
   - Secciones Added, Fixed, Changed segun corresponda
   - Descripcion concisa de cada cambio
5. Si el template `CHANGELOG.md.j2` no existe, crearlo con estructura base
6. Verificar que el formato sigue Keep a Changelog

### Criterios de aceptacion
- [ ] `CHANGELOG.md` tiene entrada para la nueva version
- [ ] La version sigue Semantic Versioning (MAJOR.MINOR.PATCH)
- [ ] La fecha esta en formato ISO (YYYY-MM-DD)
- [ ] Todos los cambios de las tareas 1-6 estan documentados
- [ ] El formato sigue Keep a Changelog (Added, Fixed, Changed, etc.)
- [ ] El template `.j2` existe y tiene estructura base
- [ ] Verificar con:
  ```bash
  # Verificar que existe entrada reciente
  head -30 CHANGELOG.md

  # Verificar formato de fecha
  grep -E "^\#\# \[.+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}" CHANGELOG.md

  # Verificar que menciona --once
  grep "\-\-once" CHANGELOG.md
  ```
