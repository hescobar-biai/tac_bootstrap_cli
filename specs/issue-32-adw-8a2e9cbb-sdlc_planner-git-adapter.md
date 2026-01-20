# Feature: Implementar GitAdapter

## Metadata
issue_number: `32`
adw_id: `8a2e9cbb`
issue_json: `{"number":32,"title":"TAREA 5.3: Implementar GitAdapter","body":"# Prompt para Agente\n\n## Contexto\nNecesitamos un adaptador para operaciones Git que se usan durante scaffolding,\ncomo inicializar repositorio, crear commits iniciales, etc.\n\n## Objetivo\nImplementar git_adapter.py con operaciones Git basicas.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py`"}`

## Feature Description
Esta feature implementa un adaptador Git (`GitAdapter` class) que proporciona una interfaz limpia y segura para operaciones Git durante el scaffolding de proyectos. El adaptador encapsula comandos Git comunes como inicialización de repositorios, staging, commits, y operaciones de worktree, proporcionando un resultado estructurado para cada operación.

El módulo será utilizado por el `ScaffoldService` para operaciones Git durante la generación de proyectos, así como por los ADWs (AI Developer Workflows) que requieren manipulación de repositorios y worktrees.

## User Story
As a TAC Bootstrap CLI developer or ADW workflow
I want to have a clean Git operations adapter
So that I can perform repository operations (init, commit, worktree management) safely during scaffolding and workflows without handling raw subprocess calls directly

## Problem Statement
El `ScaffoldService` y los ADWs necesitan realizar operaciones Git durante:
- Inicialización de nuevos proyectos (git init, commit inicial)
- Gestión de worktrees para desarrollo paralelo aislado
- Verificación de estado del repositorio antes de operaciones

Actualmente no existe un módulo dedicado para operaciones Git. Sin este adaptador, cada componente que necesite Git tendría que:
- Manejar subprocess calls directamente con manejo de errores duplicado
- Parsear outputs de git manualmente
- Reinventar validaciones (¿es un repo? ¿existe la rama?)
- Carecer de abstracción consistente para capturar success/failure

## Solution Statement
Implementar el módulo `tac_bootstrap/infrastructure/git_adapter.py` con:

1. **Dataclass `GitResult`**: Resultado estructurado con `success`, `output`, `error`
2. **Clase `GitAdapter`**: Adaptador principal con método base `_run()` para ejecutar comandos Git
3. **Operaciones básicas**: `init()`, `is_repo()`, `add()`, `add_all()`, `commit()`, `status()`
4. **Operaciones de branch**: `get_current_branch()`, `branch_exists()`, `checkout()`
5. **Operaciones de worktree**: `create_worktree()`, `remove_worktree()`, `list_worktrees()`
6. **Utilidades**: `has_changes()`, `get_remote_url()`
7. **Manejo de errores robusto**: Captura `CalledProcessError`, `FileNotFoundError` (git no instalado), y retorna `GitResult` consistentemente

El adaptador NO implementará operaciones que requieran autenticación (push, clone) según está definido en el scope del issue.

## Relevant Files
Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py** - Módulo de referencia para patrones de infrastructure (estructura de clase, docstrings, manejo de Path)
- **tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py** - Otro módulo de infraestructura como patrón de referencia
- **adws/adw_modules/git_ops.py** (si existe) - Para entender cómo se usan operaciones Git en workflows existentes

### New Files
- **tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py** - Módulo principal a crear con GitAdapter y GitResult

## Implementation Plan

### Phase 1: Foundation
Crear el módulo base con dataclass `GitResult` y estructura de `GitAdapter`:
- Definir dataclass `GitResult` con campos `success`, `output`, `error`
- Crear clase `GitAdapter` con `__init__` que toma `repo_path: Path`
- Implementar método base `_run()` que ejecuta comandos git con manejo de errores completo

### Phase 2: Core Implementation
Implementar operaciones Git fundamentales:
- Operaciones básicas: `is_repo()`, `init()`, `add()`, `add_all()`, `commit()`
- Operaciones de status: `status()`, `has_changes()`
- Operaciones de branch: `get_current_branch()`, `branch_exists()`, `checkout()`

### Phase 3: Advanced Operations
Implementar operaciones de worktree y utilidades:
- Operaciones de worktree: `create_worktree()`, `remove_worktree()`, `list_worktrees()`
- Utilidades: `get_remote_url()`

### Phase 4: Integration
Verificar integración y testing:
- Ejecutar script de prueba inline para verificar todas las operaciones
- Validar que el módulo funciona en repositorios reales
- Confirmar integración con validation commands

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear archivo git_adapter.py con estructura base
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py`
- Agregar module-level docstring explicando el propósito del módulo
- Importar dependencias: `subprocess`, `dataclass` de dataclasses, `Path` de pathlib, `Optional`, `List` de typing
- Verificar que el archivo se creó correctamente

### Task 2: Implementar dataclass GitResult
- Definir dataclass `GitResult` con decorador `@dataclass`
- Agregar campo `success: bool`
- Agregar campo `output: str = ""`
- Agregar campo `error: str = ""`
- Agregar docstring explicando el propósito de la dataclass

### Task 3: Crear clase GitAdapter e implementar __init__
- Definir clase `GitAdapter` con class-level docstring
- Implementar `__init__(self, repo_path: Path)`
- Almacenar `repo_path` como atributo de instancia
- Agregar docstring con ejemplo de uso (init, add_all, commit)

### Task 4: Implementar método base _run()
- Implementar `_run(self, *args: str, check: bool = True) -> GitResult`
- Ejecutar subprocess con `["git", *args]` en `cwd=self.repo_path`
- Configurar `capture_output=True`, `text=True`, `check=check`
- Capturar `subprocess.CalledProcessError` y retornar `GitResult(success=False)` con error message
- Capturar `FileNotFoundError` para caso de git no instalado
- Retornar `GitResult(success=True)` con stdout/stderr en caso exitoso
- Agregar docstring completo con parámetros y retorno

### Task 5: Implementar operaciones básicas de repositorio
- Implementar `is_repo(self) -> bool` que verifica si `.git` directory existe
- Implementar `init(self, initial_branch: str = "main") -> GitResult` usando `git init -b {branch}`
- Agregar docstrings completos

### Task 6: Implementar operaciones de staging
- Implementar `add(self, *paths: str) -> GitResult` que ejecuta `git add` con paths variables
- Implementar `add_all(self) -> GitResult` que ejecuta `git add -A`
- Agregar docstrings completos

### Task 7: Implementar operación commit
- Implementar `commit(self, message: str, allow_empty: bool = False) -> GitResult`
- Construir args con `["commit", "-m", message]`
- Si `allow_empty=True`, agregar `"--allow-empty"` a args
- Agregar docstring completo

### Task 8: Implementar operaciones de status
- Implementar `status(self, porcelain: bool = True) -> GitResult`
- Si `porcelain=True`, agregar `"--porcelain"` flag
- Implementar `has_changes(self) -> bool` que usa `status()` y verifica si output no está vacío
- Agregar docstrings completos

### Task 9: Implementar operaciones de branch
- Implementar `get_current_branch(self) -> Optional[str]` usando `git branch --show-current`
- Retornar `result.output` si success, sino `None`
- Implementar `branch_exists(self, branch: str) -> bool` usando `git rev-parse --verify {branch}`
- Implementar `checkout(self, branch: str, create: bool = False) -> GitResult`
- Si `create=True`, agregar `-b` flag
- Agregar docstrings completos

### Task 10: Implementar operaciones de worktree
- Implementar `create_worktree(self, path: Path, branch: str, create_branch: bool = True) -> GitResult`
- Construir args con `["worktree", "add", str(path)]`
- Si `create_branch=True`, agregar `["-b", branch]`, sino solo `[branch]`
- Implementar `remove_worktree(self, path: Path, force: bool = False) -> GitResult`
- Si `force=True`, agregar `"--force"` flag
- Implementar `list_worktrees(self) -> List[str]`
- Ejecutar `git worktree list --porcelain` y parsear output
- Buscar líneas que empiecen con "worktree " y extraer path
- Retornar lista de paths
- Agregar docstrings completos

### Task 11: Implementar utilidades
- Implementar `get_remote_url(self, remote: str = "origin") -> Optional[str]`
- Ejecutar `git remote get-url {remote}` con `check=False`
- Retornar output si success, sino `None`
- Agregar docstring completo

### Task 12: Ejecutar script de prueba inline
- Crear script Python inline usando `tempfile.TemporaryDirectory()` como repo temporal
- Instanciar `GitAdapter(Path(tmp))`
- Probar `init()` y verificar `result.success`
- Probar `is_repo()` y verificar retorna `True`
- Probar `get_current_branch()` y verificar retorna "main"
- Probar `add_all()` y `commit()` con mensaje de prueba
- Probar `status()` y verificar output
- Probar `has_changes()` después de commit (debería ser False)
- Ejecutar con `uv run python -c "..."` desde `tac_bootstrap_cli/`
- Verificar que todas las operaciones funcionan correctamente

### Task 13: Ejecutar comandos de validación
- Ejecutar todos los comandos listados en la sección "Validation Commands"
- Verificar que pytest pasa sin regresiones
- Verificar que ruff check no reporta errores de linting
- Verificar que mypy no reporta errores de tipos
- Verificar que el CLI funciona con `--help` (smoke test)

## Testing Strategy

### Unit Tests
El módulo será probado mediante:
1. **Test inline durante desarrollo** (Task 12): Verificar todas las operaciones básicas en un repositorio temporal aislado
2. **Tests existentes**: El módulo no rompe funcionalidad existente (validation commands)
3. **Tests futuros**: Los tests formales serán agregados cuando ScaffoldService use GitAdapter en producción

### Edge Cases
Casos edge que el módulo debe manejar:

1. **Git no instalado**: `_run()` debe capturar `FileNotFoundError` y retornar `GitResult(success=False, error="Git is not installed or not in PATH")`
2. **Comando git falla**: `_run()` debe capturar `CalledProcessError` y retornar `GitResult(success=False)` con stderr en error field
3. **Directorio no es repo**: `is_repo()` retorna `False` sin error
4. **Branch no existe**: `branch_exists()` retorna `False` sin error; `get_current_branch()` retorna `None`
5. **Worktree parsing**: `list_worktrees()` debe parsear correctamente output porcelain y retornar lista vacía si comando falla
6. **Remote no existe**: `get_remote_url()` retorna `None` sin error
7. **Commit vacío sin allow_empty**: git falla, pero `GitResult` captura el error gracefully

## Acceptance Criteria

1. ✅ El archivo `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py` existe
2. ✅ Dataclass `GitResult` tiene campos `success`, `output`, `error`
3. ✅ Clase `GitAdapter` se inicializa con `repo_path: Path`
4. ✅ Método `_run()` ejecuta comandos git y maneja errores (`CalledProcessError`, `FileNotFoundError`)
5. ✅ Método `is_repo()` detecta repositorios existentes verificando `.git` directory
6. ✅ Método `init()` crea nuevo repositorio con rama inicial configurable
7. ✅ Métodos `add()`, `add_all()`, `commit()` funcionan correctamente para staging y commits
8. ✅ Métodos de worktree (`create_worktree`, `remove_worktree`, `list_worktrees`) funcionan correctamente
9. ✅ Métodos de branch (`get_current_branch`, `branch_exists`, `checkout`) funcionan correctamente
10. ✅ Método `has_changes()` detecta cambios uncommitted
11. ✅ Todas las operaciones retornan `GitResult` con información estructurada
12. ✅ Script de prueba inline (Task 12) ejecuta sin errores y muestra resultados esperados
13. ✅ Todos los validation commands pasan sin regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- NO implementar `push` (requiere autenticación remota)
- NO implementar `clone` (fuera de scope, no necesario para scaffolding)
- NO implementar `pull` o `fetch` (operaciones remotas fuera de scope)
- El módulo usa `subprocess.run()` con `text=True` para capturar output como strings
- Todas las operaciones que pueden fallar usan `check=False` en `_run()` y verifican `returncode == 0`
- El parsing de `list_worktrees()` usa formato porcelain para mayor confiabilidad
- `create_worktree()` por defecto crea una nueva rama (`create_branch=True`) porque es el caso de uso común en ADWs
- El adaptador es stateless - cada operación es independiente y puede fallar sin afectar el estado interno
- `repo_path` se pasa como `cwd` a subprocess, permitiendo que git detecte automáticamente el `.git` directory
- Todos los métodos que retornan `Optional[str]` usan `check=False` en `_run()` para evitar exceptions en casos de error esperado
