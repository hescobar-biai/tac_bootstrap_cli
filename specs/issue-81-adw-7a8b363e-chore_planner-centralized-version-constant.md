# Chore: Crear constante de versión centralizada

## Metadata
issue_number: `81`
adw_id: `7a8b363e`
issue_json: `{"number":81,"title":"TAREA 2: Crear constante de versión centralizada","body":"/chore                                                                                                                                                                                         *Archivo**: `tac_bootstrap_cli/tac_bootstrap/__init__.py`\n\n**Descripción**: Crear constante `__version__` centralizada que se use en todo el proyecto.\n\n**Cambios**:\n\n```python\n\"\"\"TAC Bootstrap - Agentic Layer Generator.\"\"\"\n\n__version__ = \"0.2.0\"\n__all__ = [\"__version__\"]\n```\n\n**Archivo**: `tac_bootstrap_cli/tac_bootstrap/domain/models.py`\n\n**Cambios**:\n\n```python\nfrom tac_bootstrap import __version__\n\nclass TACConfig(BaseModel):\n    version: str = Field(default=__version__, ...)\n```\n\n**Archivo**: `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`\n\n**Cambios**:\n\n```python\nfrom tac_bootstrap import __version__\n\n@app.callback()\ndef main(\n    version: bool = typer.Option(None, \"--version\", \"-v\", callback=version_callback)\n):\n    \"\"\"TAC Bootstrap - Agentic Layer Generator.\"\"\"\n    pass\n\ndef version_callback(value: bool):\n    if value:\n        print(f\"TAC Bootstrap v{__version__}\")\n        raise typer.Exit()\n```\n\n**Criterios de Aceptación**:\n- [ ] `__version__` definida en `__init__.py`\n- [ ] CLI muestra versión con `tac --version`\n- [ ] `TACConfig.version` usa `__version__` como default\n- [ ] Un solo lugar para actualizar versión\nLas assumptions son correctas. Responde en el issue:\n\n\n## Respuestas - TAREA 2\n\n### Respuestas rápidas:\n\n1. **Import circular**: No habrá problema. `__init__.py` solo define `__version__ = \"0.2.0\"`, no importa nada de domain/models.\n   \n2. **Field completo**: \n   ```python\n   version: str = Field(default=__version__, description=\"TAC Bootstrap version\")\nversion_callback: Puede ir donde sea conveniente, antes de main() está bien.\n\nInmutabilidad: Es overridable (para upgrade cuando lee config existente), no se necesita validación especial.\n\nSemver: No se requiere validación estricta, es string simple.\n\n0.2.0: Correcto - representa esta nueva versión con el feature de upgrade.\n\n--help: Solo en --version, no en help.\n\nConfirmación:\n✅ Todas las assumptions son correctas. Proceder.\n\n\n\nO simplemente ejecuta con `--clarify-continue`:\n\n```bash\n# Si es plan individual\nuv run adws/adw_plan_iso.py <issue-number> e7940d6d --clarify-continue\n\n# Si es workflow compuesto\nuv run adws/adw_plan_build_iso.py <issue-number> --clarify-continue\nLas assumptions cubren todo lo necesario para TAREA 2."}`

## Chore Description
Actualizar la versión del proyecto de 0.1.0 a 0.2.0 y centralizar la constante `__version__` en un solo lugar (`tac_bootstrap/__init__.py`) para que sea utilizada consistentemente en todo el proyecto:

1. CLI (`interfaces/cli.py`) - Para mostrar versión con `--version`
2. Configuración (`domain/models.py`) - Como default en `TACConfig.version`

Esto asegura que solo haya un lugar donde actualizar la versión cuando se hagan releases.

## Relevant Files
Archivos existentes a modificar:

- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Ya existe con `__version__ = "0.1.0"`, se actualizará a 0.2.0 y se agregará `__all__`
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Ya tiene `TACConfig.version` con default hardcoded "0.2.0" (línea 424-426), se cambiará para importar `__version__`
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Ya importa `__version__` (línea 11), ya lo usa en welcome text (línea 49) y en version command (línea 74), falta agregar soporte para flag `--version` en el callback principal

### New Files
No se requieren archivos nuevos.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Actualizar `__version__` en `__init__.py`
- Actualizar versión de "0.1.0" a "0.2.0"
- Agregar `__all__ = ["__version__"]` para exportación explícita
- Archivo: `tac_bootstrap_cli/tac_bootstrap/__init__.py`

### Task 2: Importar `__version__` en `models.py`
- Agregar import: `from tac_bootstrap import __version__`
- Cambiar el Field de `TACConfig.version` para usar `default=__version__` en lugar de `default="0.2.0"`
- Archivo: `tac_bootstrap_cli/tac_bootstrap/domain/models.py` (línea 424)

### Task 3: Agregar soporte para `--version` flag en CLI
- Agregar `version_callback` function antes de `main()`
- Modificar `@app.callback()` para agregar parámetro `version` con Option que usa el callback
- El callback debe mostrar: `TAC Bootstrap v{__version__}` y hacer `raise typer.Exit()`
- Archivo: `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`

### Task 4: Validar funcionalidad
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --version` - Debe mostrar "TAC Bootstrap v0.2.0"
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Debe mostrar panel con version 0.2.0
- Verificar que no se muestre en `--help` (solo --version trigger)
- Ejecutar Validation Commands completos

### Task 5: Ejecutar Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run tac-bootstrap --version` - Test flag --version
- `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Test comando version

## Notes
- No hay riesgo de import circular: `__init__.py` solo define constante, no importa nada de domain/models
- La versión debe ser overridable en TACConfig (cuando se lee un config.yml existente con versión diferente para upgrade)
- No se requiere validación estricta de semver, es string simple
- El flag `--version` es estándar en CLIs, diferente del comando `version` que muestra panel con Rich
- El callback debe ir antes de `main()` en el archivo cli.py
