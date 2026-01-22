# Chore: Agregar dependencia `packaging` para comparación semántica de versiones

## Metadata
issue_number: `86`
adw_id: `e326b973`
issue_json: `{"number":86,"title":"TAREA 5: Agregar dependencia `packaging`","body":"**Archivo**: `tac_bootstrap_cli/pyproject.toml`\n\n**Descripción**: Agregar dependencia `packaging` para comparación semántica de versiones.\n\n**Cambios**:\n\n```toml\n[project]\ndependencies = [\n    \"typer>=0.9.0\",\n    \"rich>=13.0.0\",\n    \"jinja2>=3.1.0\",\n    \"pydantic>=2.0.0\",\n    \"pyyaml>=6.0\",\n    \"packaging>=23.0\",  # Para comparación de versiones\n]\n```\n\n**Criterios de Aceptación**:\n- [ ] `packaging` agregado a dependencias\n- [ ] `uv sync` instala correctamente\n- [ ] Import funciona en upgrade_service.py\n"}`

## Chore Description
Agregar la dependencia `packaging>=23.0` al archivo `pyproject.toml` del CLI. Esta dependencia es necesaria para realizar comparaciones semánticas de versiones en el `upgrade_service.py`, donde ya se está importando y usando (`from packaging import version as pkg_version` en línea 11).

Actualmente, el import de `packaging` en `upgrade_service.py` está presente pero la dependencia no está declarada en `pyproject.toml`, lo que podría causar errores de import si el paquete no está instalado en el entorno.

## Relevant Files
Archivos para completar la chore:

- `tac_bootstrap_cli/pyproject.toml` - Archivo de configuración del proyecto donde se deben agregar las dependencias. Actualmente tiene: typer, rich, jinja2, pydantic, pyyaml, gitpython.
- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - Servicio que ya está usando `packaging` para comparar versiones semánticas (línea 11 y 76).

### New Files
No se requieren archivos nuevos.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Agregar dependencia packaging a pyproject.toml
- Abrir `tac_bootstrap_cli/pyproject.toml`
- Agregar `"packaging>=23.0",` a la lista de dependencias en la sección `[project]`
- Agregar comentario `# Para comparación de versiones` al final de la línea
- Ubicar la nueva dependencia después de `pyyaml>=6.0.1` y antes del cierre del array

### Task 2: Sincronizar dependencias con uv
- Ejecutar `cd tac_bootstrap_cli && uv sync` para instalar la nueva dependencia
- Verificar que no haya errores en la instalación

### Task 3: Validar que el import funciona
- Ejecutar validación commands para asegurar que no hay regresiones
- Verificar que upgrade_service.py puede importar packaging correctamente

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv sync` - Sincronizar dependencias
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run python -c "from packaging import version; print(version.parse('1.0.0'))"` - Verificar import directo

## Notes
- La dependencia `packaging` ya está siendo usada en `upgrade_service.py` (línea 11), por lo que esta chore solo formaliza la dependencia en `pyproject.toml`
- La versión `>=23.0` es la versión estable actual de packaging que incluye todas las funcionalidades necesarias para comparación semántica de versiones
- Esta es una dependencia de producción, no de desarrollo, por lo que debe ir en `[project].dependencies` y no en `[project.optional-dependencies].dev`
