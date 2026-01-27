# Chore: Configurar dependencias del proyecto

## Metadata
issue_number: `3`
adw_id: `092f0ee8`
issue_json: `{"number":3,"title":"TAREA 1.2: Configurar dependencias del proyecto","body":"# Prompt para Agente\n\n## Contexto\nYa tenemos la estructura base del paquete `tac_bootstrap_cli`. Ahora necesitamos configurar\nlas dependencias del proyecto para poder usar las librerias necesarias.\n\n## Objetivo\nActualizar `pyproject.toml` con todas las dependencias necesarias e instalarlas con `uv`.\n\n## Archivo a Modificar\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`\n\n## Dependencias Requeridas\n\n### Dependencias de Produccion\n```toml\ndependencies = [\n    \"typer>=0.9.0\",        # CLI framework - maneja comandos, argumentos, opciones\n    \"rich>=13.0.0\",        # UI terminal - tablas, paneles, colores, progress bars\n    \"jinja2>=3.0.0\",       # Templates - renderizado de archivos parametrizables\n    \"pydantic>=2.0.0\",     # Validacion - schemas para config.yml y modelos\n    \"pyyaml>=6.0.0\",       # YAML - lectura/escritura de config.yml\n    \"gitpython>=3.1.0\",    # Git - operaciones git init, commit, etc.\n]\n```\n\n### Dependencias de Desarrollo\n```toml\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",       # Testing framework\n    \"pytest-cov>=4.0.0\",   # Coverage reports\n    \"mypy>=1.0.0\",         # Type checking\n    \"ruff>=0.1.0\",         # Linting y formatting\n]\n```\n\n### Entry Points\n```toml\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n```\n\n### Build System\n```toml\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n```\n\n## Acciones a Ejecutar\n\n1. Actualizar `pyproject.toml` con el contenido completo\n2. Ejecutar `uv sync` para instalar dependencias\n3. Verificar que `tac-bootstrap --help` funciona\n\n## pyproject.toml Completo\n\n```toml\n[project]\nname = \"tac-bootstrap\"\nversion = \"0.1.0\"\ndescription = \"CLI to bootstrap Agentic Layer for Claude Code with TAC patterns\"\nreadme = \"README.md\"\nrequires-python = \">=3.10\"\nlicense = {text = \"MIT\"}\nauthors = [\n    {name = \"TAC Team\"}\n]\nkeywords = [\"cli\", \"claude\", \"agentic\", \"tac\", \"bootstrap\"]\n\ndependencies = [\n    \"typer>=0.9.0\",\n    \"rich>=13.0.0\",\n    \"jinja2>=3.0.0\",\n    \"pydantic>=2.0.0\",\n    \"pyyaml>=6.0.0\",\n    \"gitpython>=3.1.0\",\n]\n\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",\n    \"pytest-cov>=4.0.0\",\n    \"mypy>=1.0.0\",\n    \"ruff>=0.1.0\",\n]\n\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py310\"\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"N\", \"W\"]\n\n[tool.mypy]\npython_version = \"3.10\"\nwarn_return_any = true\nwarn_unused_configs = true\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\npython_files = [\"test_*.py\"]\n```\n\n## Criterios de Aceptacion\n1. [ ] `pyproject.toml` actualizado con todas las dependencias\n2. [ ] `uv sync` ejecuta sin errores\n3. [ ] `uv run tac-bootstrap --help` muestra ayuda\n4. [ ] `uv run tac-bootstrap version` muestra \"tac-bootstrap v0.1.0\"\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv sync\nuv run tac-bootstrap --help\nuv run tac-bootstrap version\n```\n\n## NO hacer\n- No implementar comandos adicionales aun\n- No crear tests aun"}`

## Chore Description
Esta tarea actualiza el archivo `pyproject.toml` del CLI tac-bootstrap con todas las dependencias necesarias. El pyproject.toml ya existe y contiene la estructura base del paquete, pero necesita ser actualizado según las especificaciones de la tarea 1.2 del plan de implementación.

La tarea requiere:
1. Revisar el `pyproject.toml` actual y compararlo con las especificaciones requeridas
2. Actualizar dependencias de producción y desarrollo según la versión especificada en la issue
3. Validar configuraciones de herramientas (ruff, mypy, pytest)
4. Ejecutar `uv sync` para instalar todas las dependencias
5. Verificar que los comandos CLI funcionan correctamente

IMPORTANTE: El pyproject.toml ya existe en versión 0.6.0 con dependencias más modernas. Necesitamos verificar si todas las dependencias requeridas están presentes y actualizar si es necesario.

## Relevant Files
Archivos para completar la chore:

- `tac_bootstrap_cli/pyproject.toml` - Archivo principal a actualizar con dependencias. Actualmente existe en versión 0.6.0, necesita validación contra especificaciones de la tarea 1.2.
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Define __version__, podría necesitar actualización si cambia la versión del paquete.
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Entry point del CLI, necesita existir para validar comandos.
- `tac_bootstrap_cli/README.md` - Documentación del paquete, podría necesitar actualización.

### New Files
No se requieren archivos nuevos. Todos los archivos necesarios ya existen en `tac_bootstrap_cli/`.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analizar pyproject.toml actual
- Leer el archivo `tac_bootstrap_cli/pyproject.toml` completo
- Comparar dependencias actuales con las requeridas por la tarea 1.2
- Identificar diferencias en versiones, herramientas y configuraciones
- Determinar si es necesario actualizar o si ya cumple con los requisitos

### Task 2: Validar estructura del paquete
- Verificar que `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` existe y tiene el app Typer
- Confirmar que el entry point está correctamente configurado
- Revisar que `__init__.py` define `__version__`
- Asegurar que la estructura sigue la convención esperada

### Task 3: Actualizar pyproject.toml si es necesario
- Si hay diferencias relevantes entre el actual y las especificaciones:
  - Actualizar secciones que no cumplan con requisitos mínimos
  - Mantener versiones más modernas si son compatibles
  - Preservar configuraciones adicionales útiles
- Si el archivo actual ya cumple o supera los requisitos:
  - Documentar que no se requieren cambios
  - Continuar con validación

### Task 4: Ejecutar uv sync
- Cambiar al directorio `tac_bootstrap_cli`
- Ejecutar `uv sync` para instalar/actualizar dependencias
- Verificar que no hay errores en la instalación
- Confirmar que se genera/actualiza el archivo `uv.lock`

### Task 5: Validar comandos CLI
- Ejecutar `uv run tac-bootstrap --help` y verificar que muestra ayuda
- Ejecutar `uv run tac-bootstrap version` y verificar salida
- Confirmar que los comandos funcionan sin errores
- Documentar cualquier comportamiento inesperado

### Task 6: Ejecutar Validation Commands
- Cambiar a directorio `tac_bootstrap_cli`
- Ejecutar suite de tests con pytest
- Ejecutar linter con ruff
- Ejecutar smoke test del CLI
- Confirmar cero regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- El pyproject.toml actual está en versión 0.6.0, no 0.1.0 como especifica la tarea original
- Ya existen dependencias modernas instaladas (rich>=13.7.0, pydantic>=2.5.0, etc.)
- La tarea requiere versión 0.1.0, pero esto parece ser parte del plan de bootstrap desde cero
- Se debe evaluar si realmente necesitamos retroceder versiones o si la tarea ya está completada
- El working directory es un worktree (trees/092f0ee8), posiblemente para un ADW workflow aislado
- Las rutas absolutas en la issue original (/Volumes/MAc1/) no aplican al entorno actual
