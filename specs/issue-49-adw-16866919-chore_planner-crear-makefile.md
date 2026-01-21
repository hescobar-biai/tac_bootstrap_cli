# Chore: Crear Makefile para desarrollo

## Metadata
issue_number: `49`
adw_id: `16866919`
issue_json: `{"number":49,"title":"TAREA 8: Crear Makefile","body":"**Archivo a crear:** `Makefile`\n\n**Prompt:**\n```\nCrea un Makefile en la raíz de tac_bootstrap_cli/ con comandos útiles para desarrollo.\n\nComandos a incluir:\n\n# Instalación\ninstall:        Instalar dependencias con uv\ninstall-dev:    Instalar con dependencias de desarrollo\n\n# Desarrollo\ndev:            Correr CLI en modo desarrollo\nlint:           Ejecutar ruff check\nlint-fix:       Ejecutar ruff con auto-fix\nformat:         Formatear código con ruff format\ntypecheck:      Ejecutar mypy\n\n# Testing\ntest:           Correr todos los tests\ntest-v:         Correr tests con verbose\ntest-cov:       Correr tests con coverage report\ntest-watch:     Correr tests en modo watch (si pytest-watch está disponible)\n\n# Build\nbuild:          Construir paquete wheel\nclean:          Limpiar archivos generados (__pycache__, .pytest_cache, etc.)\n\n# CLI\ncli-help:       Mostrar ayuda del CLI\ncli-version:    Mostrar versión\ncli-init-dry:   Ejemplo de init con dry-run\ncli-doctor:     Ejemplo de doctor\n\n# Utilidades\nhelp:           Mostrar ayuda de todos los comandos\n\nUsa variables para rutas:\nPYTHON := uv run python\nPYTEST := uv run pytest\nCLI := uv run tac-bootstrap\n\nIncluye .PHONY para todos los targets.\n```\n\n**Criterios de aceptación:**\n- [ ] Makefile funciona con `make <comando>`\n- [ ] Todos los comandos documentados\n- [ ] `make help` muestra todos los comandos"}`

## Chore Description
Crear un Makefile completo en la raíz de `tac_bootstrap_cli/` que proporcione comandos útiles para todas las operaciones de desarrollo, testing, build y uso del CLI. El Makefile debe usar variables para ejecutar comandos con `uv` y seguir mejores prácticas usando `.PHONY` para targets no-archivos.

## Relevant Files

### Archivos para entender el contexto:
- `tac_bootstrap_cli/pyproject.toml` - Configuración del proyecto, dependencias y metadata. Necesario para entender qué comandos están disponibles y cómo está configurado pytest, mypy, ruff.
- `tac_bootstrap_cli/tests/` - Directorio de tests. Necesario para definir el path correcto en comandos de test.
- `tac_bootstrap_cli/tac_bootstrap/` - Código fuente principal. Necesario para comandos de lint, format, typecheck.

### New Files
- `tac_bootstrap_cli/Makefile` - Archivo nuevo a crear con todos los comandos de desarrollo.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear Makefile con estructura base
- Crear archivo `tac_bootstrap_cli/Makefile`
- Definir variables al inicio:
  - `PYTHON := uv run python`
  - `PYTEST := uv run pytest`
  - `CLI := uv run tac-bootstrap`
  - `RUFF := uv run ruff`
  - `MYPY := uv run mypy`
- Agregar comentario header con descripción del archivo

### Task 2: Implementar comandos de instalación
- `install`: `uv sync` - Instalar dependencias básicas
- `install-dev`: `uv sync --all-extras` o `uv sync --group dev` - Instalar con dependencias de desarrollo

### Task 3: Implementar comandos de desarrollo
- `dev`: `$(CLI) --help` - Muestra CLI en modo dev (smoke test)
- `lint`: `$(RUFF) check .` - Ejecutar ruff check
- `lint-fix`: `$(RUFF) check --fix .` - Ejecutar ruff con auto-fix
- `format`: `$(RUFF) format .` - Formatear código
- `typecheck`: `$(MYPY) tac_bootstrap` - Ejecutar mypy en el código fuente

### Task 4: Implementar comandos de testing
- `test`: `$(PYTEST) tests/` - Correr todos los tests
- `test-v`: `$(PYTEST) tests/ -v` - Tests con verbose
- `test-cov`: `$(PYTEST) tests/ --cov=tac_bootstrap --cov-report=term-missing` - Tests con coverage
- `test-watch`: `$(PYTEST) tests/ -f` (si pytest-watch disponible) o mensaje indicando instalar pytest-watch

### Task 5: Implementar comandos de build
- `build`: `uv build` - Construir paquete wheel
- `clean`: Eliminar archivos generados:
  - `find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true`
  - `find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true`
  - `find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true`
  - `find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true`
  - `rm -rf dist/ build/ *.egg-info`

### Task 6: Implementar comandos CLI de ejemplo
- `cli-help`: `$(CLI) --help` - Mostrar ayuda del CLI
- `cli-version`: `$(CLI) --version` - Mostrar versión
- `cli-init-dry`: `$(CLI) init --dry-run` o ejemplo similar - Dry-run de init
- `cli-doctor`: `$(CLI) doctor` - Ejecutar doctor command (si existe)

### Task 7: Implementar comando help
- `help`: Target que imprime todos los comandos disponibles con sus descripciones
- Usar formato limpio y legible, por ejemplo:
```
@echo "Comandos disponibles:"
@echo "  make install       - Instalar dependencias"
@echo "  make test          - Correr tests"
...
```

### Task 8: Agregar .PHONY
- Al final del archivo, agregar línea `.PHONY:` con todos los targets que no son archivos
- Listar todos los comandos: `install install-dev dev lint lint-fix format typecheck test test-v test-cov test-watch build clean cli-help cli-version cli-init-dry cli-doctor help`

### Task 9: Validar Makefile
- Ejecutar `cd tac_bootstrap_cli && make help` - Verificar que help funciona
- Ejecutar `cd tac_bootstrap_cli && make lint` - Verificar que lint funciona
- Ejecutar `cd tac_bootstrap_cli && make test` - Verificar que tests corren
- Ejecutar comandos de validación completos (ver sección siguiente)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && make help` - Verificar que help muestra todos los comandos
- `cd tac_bootstrap_cli && make lint` - Verificar linting funciona
- `cd tac_bootstrap_cli && make test` - Verificar tests pasan
- `cd tac_bootstrap_cli && make cli-help` - Verificar CLI funciona
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting final
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test del CLI

## Notes
- El Makefile debe ser compatible con GNU Make
- Usar `@` antes de comandos echo para no mostrar el comando mismo
- Los comandos de clean deben usar `|| true` o `-` para no fallar si los directorios no existen
- Para test-watch, considerar que pytest-watch puede no estar instalado, manejarlo gracefully
- Los comandos cli-init-dry y cli-doctor deben ajustarse según los comandos reales disponibles en el CLI
- Verificar que todos los paths relativos funcionan cuando se ejecuta `make` desde `tac_bootstrap_cli/`
