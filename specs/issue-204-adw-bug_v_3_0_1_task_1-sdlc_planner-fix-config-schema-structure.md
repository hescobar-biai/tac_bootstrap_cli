# Bug: Corregir estructura y consistencia de `config.yml` con el schema actual

## Metadata
issue_number: `204`
adw_id: `bug_v_3_0_1_task_1`
issue_json: `{"number":204,"title":"Corregir estructura y consistencia de `config.yml` con el schema actual","body":"bug\n/adw_sdlc_zte_iso\n/adw_id: bug_v_3_0_1_task_1\n\n## Archivos a modificar\n- **Archivo raiz**: `config.yml`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`\n\n### Contexto\nEl archivo `config.yml` actual tiene claves que estan fuera de sus secciones correspondientes segun el modelo `TACConfig` definido en `tac_bootstrap_cli/tac_bootstrap/domain/models.py`. Esto causa errores de validacion al cargar la configuracion.\n\n### Problema especifico\nLas siguientes claves estan mal ubicadas en `config.yml`:\n1. `allowed_paths` y `forbidden_paths` estan a nivel raiz, pero deben estar dentro de `agentic.safety`\n2. `workflows` a nivel raiz tiene estructura incorrecta - debe estar dentro de `agentic.workflows`\n3. Falta la seccion `claude` con `settings` y `commands`\n4. Las claves `workflows.settings` y `workflows.commands` no corresponden al schema\n\n### Estructura correcta segun TACConfig\n```yaml\nversion: \"0.x.x\"\nschema_version: 1\n\nproject:\n  name: \"...\"\n  mode: \"existing\"\n  repo_root: \".\"\n  language: \"python\"\n  framework: \"none\"\n  architecture: \"ddd\"\n  package_manager: \"uv\"\n\npaths:\n  app_root: \"...\"\n  agentic_root: \".\"\n  prompts_dir: \"prompts\"\n  adws_dir: \"adws\"\n  specs_dir: \"specs\"\n  logs_dir: \"logs\"\n  scripts_dir: \"scripts\"\n  worktrees_dir: \"trees\"\n\ncommands:\n  start: \"...\"\n  test: \"...\"\n  lint: \"...\"\n  typecheck: \"...\"\n  format: \"...\"\n  build: \"...\"\n\nagentic:\n  provider: \"claude_code\"\n  target_branch: \"main\"\n  model_policy:\n    default: \"sonnet\"\n    heavy: \"opus\"\n  worktrees:\n    enabled: true\n    max_parallel: 5\n    naming: \"feat-{slug}-{timestamp}\"\n  logging:\n    level: \"INFO\"\n    capture_agent_transcript: true\n    run_id_strategy: \"uuid\"\n  safety:\n    require_tests_pass: true\n    require_review_artifacts: true\n    allowed_paths:\n      - \"tac_bootstrap_cli/\"\n      - \"adws/\"\n      - \"scripts/\"\n      - \"specs/\"\n      - \"tests/\"\n    forbidden_paths:\n      - \".env\"\n      - \"secrets/\"\n  workflows:\n    default: \"sdlc_iso\"\n    available:\n      - \"sdlc_iso\"\n      - \"patch_iso\"\n      - \"plan_implement\"\n\nclaude:\n  settings:\n    project_name: \"tac-bootstrap\"\n    preferred_style: \"concise\"\n    allow_shell: true\n  commands:\n    prime: \".claude/commands/prime.md\"\n    start: \".claude/commands/start.md\"\n    build: \".claude/commands/build.md\"\n    test: \".claude/commands/test.md\"\n    review: \".claude/commands/review.md\"\n    ship: \".claude/commands/ship.md\"\n\ntemplates:\n  plan_template: \"prompts/templates/plan.md\"\n  chore_template: \"prompts/templates/chore.md\"\n  feature_template: \"prompts/templates/feature.md\"\n  bug_template: \"prompts/templates/bug.md\"\n  review_template: \"prompts/templates/review.md\"\n\nbootstrap:\n  create_git_repo: false\n  initial_commit: false\n  license: \"MIT\"\n  readme: true\n```\n\n### Pasos a ejecutar\n1. Leer el archivo `config.yml` actual\n2. Leer el modelo `TACConfig` en `tac_bootstrap_cli/tac_bootstrap/domain/models.py` para confirmar estructura\n3. Reorganizar las claves del `config.yml` para que coincidan con el schema:\n   - Mover `allowed_paths` y `forbidden_paths` dentro de `agentic.safety`\n   - Reestructurar `workflows` dentro de `agentic.workflows` con solo `default` y `available`\n   - Agregar seccion `claude` con `settings` y `commands`\n   - Eliminar claves que no pertenecen al schema (`workflows.settings`, `workflows.commands` a nivel raiz)\n4. Actualizar el template Jinja2 `config.yml.j2` para que genere la estructura correcta\n5. Verificar que la configuracion carga sin errores\n\n### Criterios de aceptacion\n- [ ] El archivo `config.yml` tiene todas las claves dentro de sus secciones correctas segun `TACConfig`\n- [ ] No hay claves a nivel raiz que no esten en el schema (`allowed_paths`, `forbidden_paths`, `workflows` mal estructurado)\n- [ ] El template `config.yml.j2` genera YAML con la estructura correcta\n- [ ] El comando de validacion ejecuta sin errores:\n  ```bash\n  cd tac_bootstrap_cli && uv run python -c \"\n  import yaml\n  from tac_bootstrap.domain.models import TACConfig\n  with open('../config.yml') as f:\n      data = yaml.safe_load(f)\n  config = TACConfig(**data)\n  print('Validacion exitosa:', config.project.name)"}`

## Bug Description
El archivo `config.yml` en la raiz del proyecto tiene una estructura que no coincide con el modelo Pydantic `TACConfig` definido en `tac_bootstrap_cli/tac_bootstrap/domain/models.py`. Esto causa errores de validacion cuando el sistema intenta cargar y validar la configuracion.

El problema se manifiesta en claves que estan ubicadas a nivel raiz cuando deberian estar dentro de secciones especificas, y en la ausencia de secciones requeridas por el schema.

## Problem Statement
1. Las claves `allowed_paths` y `forbidden_paths` estan a nivel raiz (lineas 50-58), pero segun el modelo `SafetyConfig` (lineas 258-276 de models.py), deben estar dentro de `agentic.safety`
2. La seccion `workflows` a nivel raiz (lineas 59-75) tiene una estructura incorrecta con subclaves `settings` y `commands` que no pertenecen a `WorkflowsConfig` (lineas 279-296 de models.py), sino que deberian estar en una seccion `claude` separada
3. Falta completamente la seccion `claude` que es requerida por el modelo `TACConfig` (linea 536 de models.py) y debe contener `settings` y `commands`
4. El modelo `TACConfig` espera que `agentic.workflows` contenga solo `default` y `available`, no `settings` ni `commands`

## Solution Statement
Reorganizar el archivo `config.yml` para que su estructura coincida exactamente con el modelo `TACConfig`:

1. Mover `allowed_paths` y `forbidden_paths` dentro de `agentic.safety`
2. Simplificar `workflows` y moverlo dentro de `agentic.workflows` con solo las claves `default` y `available`
3. Crear una nueva seccion top-level `claude` que contenga:
   - `settings` con `project_name`, `preferred_style`, `allow_shell`
   - `commands` con los paths a los comandos slash
4. Actualizar el template Jinja2 `config.yml.j2` para que genere la estructura correcta en proyectos futuros

## Steps to Reproduce
1. Leer el archivo `config.yml` actual
2. Intentar validar con:
   ```bash
   cd tac_bootstrap_cli && uv run python -c "
   import yaml
   from tac_bootstrap.domain.models import TACConfig
   with open('../config.yml') as f:
       data = yaml.safe_load(f)
   config = TACConfig(**data)
   print('Validacion exitosa:', config.project.name)"
   ```
3. Observar el error de validacion debido a claves incorrectas

## Root Cause Analysis
El archivo `config.yml` fue creado siguiendo una estructura antigua o inconsistente que no refleja el modelo final `TACConfig` implementado en `models.py`. Las principales discrepancias son:

1. **Historico**: Las claves `allowed_paths` y `forbidden_paths` posiblemente fueron movidas dentro de `safety` en el modelo, pero el archivo de configuracion no fue actualizado
2. **Confusion de responsabilidades**: Las claves `settings` y `commands` dentro de `workflows` en realidad pertenecen a la configuracion de Claude Code, no a los workflows ADW
3. **Seccion faltante**: La seccion `claude` es requerida por el schema pero no existe en el archivo actual
4. **Template desactualizado**: El template Jinja2 que genera `config.yml` tambien necesita actualizacion para reflejar estos cambios

## Relevant Files
Archivos para arreglar el bug:

- `config.yml` (linea 1-89) - Archivo de configuracion principal que necesita reestructuracion
  - Lineas 50-58: `allowed_paths` y `forbidden_paths` a nivel raiz (deben moverse)
  - Lineas 59-75: `workflows` con estructura incorrecta (debe simplificarse y moverse)
  - Falta seccion `claude` completa

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` (lineas 485-546) - Modelo `TACConfig` que define la estructura correcta
  - Linea 536: Requiere `claude: ClaudeConfig`
  - Lineas 308-336: Define `AgenticSpec` con `safety` y `workflows` anidados
  - Lineas 258-276: Define `SafetyConfig` con `allowed_paths` y `forbidden_paths`
  - Lineas 279-296: Define `WorkflowsConfig` con solo `default` y `available`
  - Lineas 364-374: Define `ClaudeConfig` con `settings` y `commands`

- `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2` - Template Jinja2 que debe actualizarse para generar estructura correcta

### New Files
No se requieren archivos nuevos.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Reorganizar config.yml para coincidir con el schema
- Leer el archivo `config.yml` actual
- Mover `allowed_paths` y `forbidden_paths` dentro de `agentic.safety`
- Mover `workflows` dentro de `agentic.workflows` y mantener solo `default` y `available`
- Crear nueva seccion top-level `claude` con:
  - `settings`: `project_name: "tac-bootstrap"`, `preferred_style: "concise"`, `allow_shell: true`
  - `commands`: mover los paths de comandos desde `workflows.commands`
- Eliminar las claves `workflows.settings` y `workflows.commands` del nivel raiz
- Actualizar el campo `version` a usar formato string si es necesario

### Task 2: Actualizar template config.yml.j2
- Leer el template actual `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`
- Actualizar el template para que genere la estructura correcta con:
  - `agentic.safety.allowed_paths` y `agentic.safety.forbidden_paths`
  - `agentic.workflows` con solo `default` y `available`
  - Seccion `claude` con `settings` y `commands`
- Asegurar que el template usa las variables correctas del objeto `config`

### Task 3: Validar la configuracion reorganizada
- Ejecutar el comando de validacion:
  ```bash
  cd tac_bootstrap_cli && uv run python -c "
  import yaml
  from tac_bootstrap.domain.models import TACConfig
  with open('../config.yml') as f:
      data = yaml.safe_load(f)
  config = TACConfig(**data)
  print('Validacion exitosa:', config.project.name)"
  ```
- Verificar que no hay errores de validacion
- Verificar que todas las claves se cargan correctamente
- Confirmar que `config.claude.settings.project_name` es accesible
- Confirmar que `config.agentic.safety.allowed_paths` contiene los valores esperados

### Task 4: Ejecutar Validation Commands
- Correr todos los comandos de validacion listados abajo

## Validation Commands
Ejecutar todos los comandos para validar el fix con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run python -c "import yaml; from tac_bootstrap.domain.models import TACConfig; data = yaml.safe_load(open('../config.yml')); config = TACConfig(**data); print('Validacion exitosa:', config.project.name)"` - Validacion del schema

## Notes
- Este es un fix quirurgico que solo reorganiza la estructura del YAML sin cambiar funcionalidad
- No se requieren nuevas dependencias
- El campo `version` en config.yml usa `version: 1` (int) pero el modelo espera string - verificar si requiere conversion
- Mantener todos los valores actuales, solo mover claves a sus secciones correctas
- El template debe usar las variables de Jinja2 correctas para acceder a `config.claude`, `config.agentic.safety`, etc.
