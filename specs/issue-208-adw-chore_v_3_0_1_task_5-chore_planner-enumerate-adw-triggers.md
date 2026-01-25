# Chore: Enumerar triggers disponibles en paquete `adw_triggers`

## Metadata
issue_number: `208`
adw_id: `chore_v_3_0_1_task_5`
issue_json: `{"number":208,"title":"Enumerar triggers disponibles en paquete `adw_triggers`","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_3_0_1_task_5\n\n### Archivos a modificar\n- **Archivo raiz**: `adws/adw_triggers/__init__.py`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`\n\n### Contexto\nEl archivo `__init__.py` del paquete `adw_triggers` actualmente solo contiene un comentario basico. Necesita un docstring completo que liste todos los triggers disponibles y su proposito, sirviendo como documentacion de referencia rapida.\n\n### Contenido actual\n```python\n# ADW Triggers Package\n```\n\n### Contenido esperado\n```python\n\"\"\"\nADW Triggers Package - Automation entry points for AI Developer Workflows.\n\nThis package contains trigger scripts that monitor GitHub and automatically\ninvoke ADW workflows based on events or schedules.\n\nAvailable Triggers:\n    trigger_cron.py\n        Polling-based monitor that checks GitHub issues at regular intervals.\n        Detects workflow commands (adw_plan_iso, adw_sdlc_iso, etc.) in issue\n        bodies or comments and triggers the corresponding workflow.\n        Usage: uv run adw_triggers/trigger_cron.py [--interval N] [--once]\n\n    trigger_issue_chain.py\n        Sequential issue processor that handles issues in a specific order.\n        Only processes issue N+1 after issue N is closed, enabling dependent\n        workflows and ordered batch processing.\n        Usage: uv run adw_triggers/trigger_issue_chain.py --issues 1,2,3 [--once]\n\n    trigger_webhook.py\n        Real-time webhook server that receives GitHub events instantly.\n        Faster response than polling but requires public endpoint and\n        webhook configuration in GitHub repository settings.\n        Usage: uv run adw_triggers/trigger_webhook.py [--port N]\n\nCommon Features:\n    - All triggers support workflow detection via keywords (adw_plan_iso, etc.)\n    - All triggers post status comments to GitHub issues\n    - All triggers create isolated worktrees for parallel execution\n    - Graceful shutdown on SIGINT/SIGTERM signals\n\nEnvironment Variables:\n    GITHUB_TOKEN or gh auth: GitHub authentication\n    ANTHROPIC_API_KEY: Claude API access\n    GITHUB_WEBHOOK_SECRET: (webhook only) Signature validation\n\nSee Also:\n    - adws/README.md for complete documentation\n    - config.yml for interval and workflow configuration\n\"\"\"\n```\n\n### Pasos a ejecutar\n1. Abrir `adws/adw_triggers/__init__.py`\n2. Reemplazar el contenido actual con el docstring completo mostrado arriba\n3. Verificar que el docstring es accesible via `help()` o `__doc__`\n4. Replicar los mismos cambios en el archivo template `__init__.py.j2`\n\n### Criterios de aceptacion\n- [ ] El archivo `__init__.py` contiene docstring completo con todos los triggers\n- [ ] Cada trigger tiene: nombre, descripcion breve, y ejemplo de uso\n- [ ] El docstring incluye seccion de variables de entorno requeridas\n- [ ] El docstring es accesible programaticamente\n- [ ] El template `.j2` tiene los mismos cambios\n- [ ] Verificar con:\n  ```bash\n  # Verificar que el docstring es accesible\n  uv run python -c \"import sys; sys.path.insert(0, 'adws'); from adw_triggers import __doc__; print(__doc__[:200])\"\n\n  # Verificar que menciona los tres triggers\n  grep -c \"trigger_\" adws/adw_triggers/__init__.py  # Debe ser >= 3\n  ```"}`

## Chore Description
Actualizar el archivo `__init__.py` del paquete `adw_triggers` para incluir un docstring completo que enumere todos los triggers disponibles. Actualmente solo contiene un comentario básico (`# ADW Triggers Package`), necesita documentación detallada sobre los tres triggers: `trigger_cron.py`, `trigger_issue_chain.py`, y `trigger_webhook.py`.

El docstring debe servir como documentación de referencia rápida, listando cada trigger con su descripción, propósito, y ejemplo de uso. También debe replicarse en el template Jinja2 correspondiente.

## Relevant Files
Archivos para completar la chore:

- **`adws/adw_triggers/__init__.py`** - Archivo principal del paquete que necesita el docstring completo
- **`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`** - Template Jinja2 que debe reflejar los mismos cambios
- **`adws/adw_triggers/trigger_cron.py`** - Trigger de polling (revisar para entender funcionalidad)
- **`adws/adw_triggers/trigger_issue_chain.py`** - Trigger de procesamiento secuencial (revisar para entender funcionalidad)
- **`adws/adw_triggers/trigger_webhook.py`** - Trigger de webhook en tiempo real (revisar para entender funcionalidad)

### New Files
No se requieren archivos nuevos.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Actualizar `adws/adw_triggers/__init__.py`
- Abrir el archivo `adws/adw_triggers/__init__.py`
- Reemplazar el contenido actual (`# ADW Triggers Package`) con el docstring completo especificado en el issue
- El docstring debe incluir:
  - Descripción general del paquete
  - Sección "Available Triggers" con los tres triggers (cron, issue_chain, webhook)
  - Para cada trigger: descripción, propósito, y ejemplo de uso
  - Sección "Common Features" con características compartidas
  - Sección "Environment Variables" con variables requeridas
  - Sección "See Also" con referencias a documentación adicional
- Guardar el archivo

### Task 2: Actualizar template `__init__.py.j2`
- Abrir el archivo `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2`
- Reemplazar el contenido actual con el mismo docstring del Task 1
- Mantener cualquier variable Jinja2 existente (como `{{ config.project.name }}`) si aplica
- Guardar el archivo

### Task 3: Validar cambios
- Ejecutar comando para verificar que el docstring es accesible:
  ```bash
  uv run python -c "import sys; sys.path.insert(0, 'adws'); from adw_triggers import __doc__; print(__doc__[:200])"
  ```
- Verificar que menciona los tres triggers:
  ```bash
  grep -c "trigger_" adws/adw_triggers/__init__.py
  ```
  - El resultado debe ser >= 3
- Ejecutar Validation Commands completos

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `uv run python -c "import sys; sys.path.insert(0, 'adws'); from adw_triggers import __doc__; print(__doc__[:200])"` - Verificar docstring accesible
- `grep -c "trigger_" adws/adw_triggers/__init__.py` - Verificar que menciona >= 3 triggers

## Notes
- Esta es una tarea de documentación, no requiere cambios en lógica de código
- El docstring debe ser Python válido y seguir PEP 257
- El template `.j2` debe mantener la misma estructura pero puede incluir variables Jinja2 si es necesario
- Los tres triggers mencionados ya existen en el directorio `adws/adw_triggers/`
