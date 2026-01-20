# Feature: Implementar DetectService

## Metadata
issue_number: `34`
adw_id: `3b39c634`
issue_json: `{"number":34,"title":"TAREA 6.1: Implementar DetectService","body":"# Prompt para Agente\n\n## Contexto\nEl comando `add-agentic` necesita auto-detectar el lenguaje, framework y package manager\nde un repositorio existente para sugerir configuracion apropiada.\n\n## Objetivo\nImplementar DetectService que analiza un repositorio y detecta su stack tecnologico.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`"}`

## Feature Description
Esta feature implementa un servicio de detección inteligente (`DetectService`) que analiza la estructura y archivos de un repositorio existente para identificar automáticamente su stack tecnológico. El servicio detecta el lenguaje de programación principal, framework web (si aplica), gestor de paquetes, directorio raíz de la aplicación, y comandos comunes del proyecto.

El `DetectService` será utilizado por el comando `add-agentic` del CLI para pre-poblar el wizard interactivo con sugerencias inteligentes basadas en la estructura existente del proyecto, minimizando la entrada manual del usuario y reduciendo errores de configuración.

## User Story
As a developer adding the agentic layer to an existing project
I want the CLI to auto-detect my project's language, framework, and package manager
So that I can quickly configure TAC Bootstrap without manually specifying settings that can be inferred from my repository

## Problem Statement
Cuando un usuario ejecuta `tac-bootstrap add-agentic` en un repositorio existente, necesita especificar:
- Lenguaje de programación (Python, TypeScript, Go, etc.)
- Framework web (FastAPI, Next.js, Spring, etc.)
- Gestor de paquetes (uv, npm, cargo, etc.)
- Directorio raíz de la aplicación (src, app, lib, etc.)
- Comandos comunes (start, test, lint, build)

Sin auto-detección, el usuario debe:
1. Recordar y tipear manualmente cada configuración
2. Conocer las opciones exactas disponibles en los enums
3. Arriesgarse a errores de configuración manual
4. Desperdiciar tiempo en un proceso tedioso

Además, el wizard debe ser inteligente y sugerir valores apropiados basados en el contexto del proyecto, no solo defaults genéricos.

## Solution Statement
Implementar el módulo `tac_bootstrap/application/detect_service.py` con:

1. **Dataclass `DetectedProject`**: Resultado estructurado con `language`, `framework`, `package_manager`, `app_root`, `commands`, `confidence`
2. **Clase `DetectService`**: Servicio principal con método `detect(repo_path: Path) -> DetectedProject`
3. **Detección de lenguaje**: Análisis de archivos indicadores (pyproject.toml, tsconfig.json, go.mod, Cargo.toml, pom.xml, etc.)
4. **Detección de package manager**: Inferencia basada en lock files y archivos de configuración específicos
5. **Detección de framework**: Análisis de dependencias en archivos de configuración (pyproject.toml, package.json, go.mod, Cargo.toml)
6. **Detección de app root**: Búsqueda de directorios comunes (src, app, lib) y patrones específicos del lenguaje
7. **Detección de comandos**: Extracción de scripts de package.json, pyproject.toml scripts, etc.
8. **Métodos privados organizados**: Cada tipo de detección en método dedicado para mantener claridad

El servicio opera sin APIs externas, solo análisis local de archivos, y retorna un score de confidence para indicar la certeza de la detección.

## Relevant Files
Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Enums (Language, Framework, PackageManager) y helpers (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
- **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py** - Patrón de referencia para servicios de application layer (estructura, docstrings)
- **tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py** - Si necesitamos operaciones de filesystem (aunque usaremos Path directamente)

### New Files
- **tac_bootstrap_cli/tac_bootstrap/application/detect_service.py** - Módulo principal a crear con DetectService y DetectedProject

## Implementation Plan

### Phase 1: Foundation
Crear el módulo base con dataclass `DetectedProject` y estructura de `DetectService`:
- Definir dataclass `DetectedProject` con todos los campos necesarios
- Crear clase `DetectService` con método principal `detect()`
- Establecer estructura de métodos privados para cada tipo de detección

### Phase 2: Core Implementation
Implementar detecciones fundamentales:
- `_detect_language()`: Detectar lenguaje por archivos indicadores
- `_detect_package_manager()`: Detectar gestor de paquetes basado en lenguaje
- `_detect_framework()`: Detectar framework analizando dependencias

### Phase 3: Advanced Detection
Implementar detecciones auxiliares:
- `_detect_app_root()`: Identificar directorio raíz de la aplicación
- `_detect_commands()`: Extraer comandos de archivos de configuración
- Helpers: `_read_package_json()`, `_get_python_deps()`

### Phase 4: Integration & Testing
Verificar integración y testing:
- Ejecutar script de prueba inline en el propio repositorio tac_bootstrap_cli
- Validar detección correcta de Python, uv, etc.
- Confirmar integración con validation commands

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear archivo detect_service.py con estructura base
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`
- Agregar module-level docstring explicando el propósito del módulo (detección de lenguaje, framework, package manager, etc.)
- Importar dependencias necesarias: `dataclass`, `field` de dataclasses; `Path` de pathlib; `Dict`, `List`, `Optional` de typing; `json` para parsear package.json
- Importar enums del domain: `from tac_bootstrap.domain.models import Language, Framework, PackageManager`
- Verificar que el archivo se creó correctamente

### Task 2: Implementar dataclass DetectedProject
- Definir dataclass `DetectedProject` con decorador `@dataclass`
- Agregar campo `language: Language` (requerido)
- Agregar campo `framework: Optional[Framework] = None`
- Agregar campo `package_manager: PackageManager = PackageManager.PIP` (default PIP)
- Agregar campo `app_root: Optional[str] = None`
- Agregar campo `commands: Dict[str, str] = field(default_factory=dict)`
- Agregar campo `confidence: float = 0.0` (score 0-1)
- Agregar docstring explicando el propósito de la dataclass (resultado de detección de proyecto)

### Task 3: Crear clase DetectService e implementar __init__
- Definir clase `DetectService` con class-level docstring
- No requiere `__init__` personalizado (sin estado)
- Agregar docstring con ejemplo de uso (detector = DetectService(); detected = detector.detect(Path("/path/to/repo")); print(f"Language: {detected.language}"))

### Task 4: Implementar método principal detect()
- Implementar `detect(self, repo_path: Path) -> DetectedProject`
- Llamar `_detect_language(repo_path)` y almacenar resultado en `language`
- Llamar `_detect_package_manager(repo_path, language)` y almacenar en `package_manager`
- Llamar `_detect_framework(repo_path, language)` y almacenar en `framework`
- Llamar `_detect_app_root(repo_path, language)` y almacenar en `app_root`
- Llamar `_detect_commands(repo_path, language, package_manager)` y almacenar en `commands`
- Retornar `DetectedProject` con todos los valores detectados y `confidence=0.8` (TODO: calcular real confidence)
- Agregar docstring completo con Args y Returns

### Task 5: Implementar _detect_language()
- Implementar `_detect_language(self, repo_path: Path) -> Language`
- Definir lista `python_files = ["pyproject.toml", "setup.py", "requirements.txt", "Pipfile", "poetry.lock", "uv.lock"]`
- Si alguno existe, retornar `Language.PYTHON`
- Definir lista `ts_files = ["tsconfig.json"]`
- Si `tsconfig.json` existe, retornar `Language.TYPESCRIPT`
- Si `package.json` existe, leer con `_read_package_json()` y verificar si tiene "typescript" en dependencies o devDependencies, retornar `Language.TYPESCRIPT`, sino `Language.JAVASCRIPT`
- Si `go.mod` existe, retornar `Language.GO`
- Si `Cargo.toml` existe, retornar `Language.RUST`
- Definir lista `java_files = ["pom.xml", "build.gradle", "build.gradle.kts"]`
- Si alguno existe, retornar `Language.JAVA`
- Default: retornar `Language.PYTHON`
- Agregar docstring explicando la lógica (checks for language-specific files in order of priority)

### Task 6: Implementar _detect_package_manager()
- Implementar `_detect_package_manager(self, repo_path: Path, language: Language) -> PackageManager`
- Si `language == Language.PYTHON`:
  - Si `uv.lock` o `.python-version` existe, retornar `PackageManager.UV`
  - Si `poetry.lock` existe, retornar `PackageManager.POETRY`
  - Si `Pipfile.lock` existe, retornar `PackageManager.PIPENV`
  - Default: retornar `PackageManager.PIP`
- Si `language in (Language.TYPESCRIPT, Language.JAVASCRIPT)`:
  - Si `pnpm-lock.yaml` existe, retornar `PackageManager.PNPM`
  - Si `yarn.lock` existe, retornar `PackageManager.YARN`
  - Si `bun.lockb` existe, retornar `PackageManager.BUN`
  - Default: retornar `PackageManager.NPM`
- Si `language == Language.GO`, retornar `PackageManager.GO_MOD`
- Si `language == Language.RUST`, retornar `PackageManager.CARGO`
- Si `language == Language.JAVA`:
  - Si `pom.xml` existe, retornar `PackageManager.MAVEN`
  - Default: retornar `PackageManager.GRADLE`
- Default final: retornar `PackageManager.PIP`
- Agregar docstring (Detect package manager for language)

### Task 7: Implementar _detect_framework() para Python
- Implementar `_detect_framework(self, repo_path: Path, language: Language) -> Optional[Framework]`
- Si `language == Language.PYTHON`:
  - Llamar `_get_python_deps(repo_path)` para obtener lista de dependencias
  - Si "fastapi" está en deps, retornar `Framework.FASTAPI`
  - Si "django" está en deps, retornar `Framework.DJANGO`
  - Si "flask" está en deps, retornar `Framework.FLASK`
- Agregar docstring (Detect web framework)
- (Próximas tareas agregarán detección para otros lenguajes)

### Task 8: Implementar _detect_framework() para TypeScript/JavaScript
- Continuar implementación de `_detect_framework()`:
- Si `language in (Language.TYPESCRIPT, Language.JAVASCRIPT)`:
  - Leer package.json con `_read_package_json(repo_path)`
  - Si `pkg_json` existe, combinar dependencies y devDependencies en `deps`
  - Si "next" está en deps, retornar `Framework.NEXTJS`
  - Si "@nestjs/core" está en deps, retornar `Framework.NESTJS`
  - Si "express" está en deps, retornar `Framework.EXPRESS`
  - Si "react" está en deps, retornar `Framework.REACT`
  - Si "vue" está en deps, retornar `Framework.VUE`

### Task 9: Implementar _detect_framework() para Go, Rust, Java
- Continuar implementación de `_detect_framework()`:
- Si `language == Language.GO`:
  - Leer `go.mod` file como texto
  - Si "gin-gonic/gin" está en contenido, retornar `Framework.GIN`
  - Si "labstack/echo" está en contenido, retornar `Framework.ECHO`
- Si `language == Language.RUST`:
  - Leer `Cargo.toml` file como texto
  - Si "axum" está en contenido, retornar `Framework.AXUM`
  - Si "actix" está en contenido, retornar `Framework.ACTIX`
- Si `language == Language.JAVA`:
  - Si `pom.xml` existe y contiene "spring" (lowercase), retornar `Framework.SPRING`
- Default final: retornar `Framework.NONE`

### Task 10: Implementar _detect_app_root()
- Implementar `_detect_app_root(self, repo_path: Path, language: Language) -> Optional[str]`
- Definir lista `common_roots = ["src", "app", "lib"]`
- Para cada root en common_roots, si `(repo_path / root).is_dir()`, retornar root
- Si `language == Language.PYTHON`:
  - Iterar sobre `repo_path.iterdir()`
  - Si item es directorio y contiene `__init__.py`, retornar `item.name`
- Default: retornar `"."`
- Agregar docstring (Detect application root directory)

### Task 11: Implementar _detect_commands() para TypeScript/JavaScript
- Implementar `_detect_commands(self, repo_path: Path, language: Language, package_manager: PackageManager) -> Dict[str, str]`
- Inicializar `commands = {}`
- Si `language in (Language.TYPESCRIPT, Language.JAVASCRIPT)`:
  - Leer package.json con `_read_package_json(repo_path)`
  - Si `pkg_json` existe y tiene "scripts" key:
    - Extraer `scripts = pkg_json["scripts"]`
    - Si "start" o "dev" en scripts: `commands["start"] = f"{package_manager.value} run {script_name}"`
    - Si "test" en scripts: `commands["test"] = f"{package_manager.value} test"`
    - Si "lint" en scripts: `commands["lint"] = f"{package_manager.value} run lint"`
    - Si "build" en scripts: `commands["build"] = f"{package_manager.value} run build"`
- Agregar docstring (Detect existing project commands)

### Task 12: Implementar _detect_commands() para Python
- Continuar implementación de `_detect_commands()`:
- Si `language == Language.PYTHON`:
  - Leer `pyproject.toml` si existe
  - Intentar parsear con `tomllib` (import en Python 3.11+)
  - Extraer `scripts = data.get("project", {}).get("scripts", {})`
  - Mapear scripts comunes si están definidos (opcional, dado que pyproject.toml scripts no es estándar)
  - Usar try/except para manejar errores de parsing silenciosamente
- Retornar `commands`

### Task 13: Implementar helper _read_package_json()
- Implementar `_read_package_json(self, repo_path: Path) -> Optional[dict]`
- Definir `pkg_path = repo_path / "package.json"`
- Si `pkg_path` no existe, retornar `None`
- Intentar leer y parsear JSON con `json.loads(pkg_path.read_text())`
- Capturar `json.JSONDecodeError` y retornar `None` en caso de error
- Retornar dict parseado si exitoso
- Agregar docstring (Read and parse package.json)

### Task 14: Implementar helper _get_python_deps()
- Implementar `_get_python_deps(self, repo_path: Path) -> List[str]`
- Inicializar `deps = []`
- Intentar leer `pyproject.toml`:
  - Usar `tomllib` para parsear (with open en modo binario)
  - Extraer `project_deps = data.get("project", {}).get("dependencies", [])`
  - Para cada dep, extraer nombre del paquete (split por "[", ">=", "==", tomar primer elemento, lowercase)
  - Agregar a `deps`
  - Usar try/except para manejar errores silenciosamente
- Leer `requirements.txt` si existe:
  - Para cada línea, skip comentarios y líneas vacías
  - Extraer nombre del paquete (split por "[", ">=", "==", lowercase)
  - Agregar a `deps`
- Retornar lista `deps`
- Agregar docstring (Get list of Python dependencies)

### Task 15: Ejecutar script de prueba inline en tac_bootstrap_cli
- Crear script Python inline que:
  - Importa `DetectService` y `Path`
  - Instancia `detector = DetectService()`
  - Ejecuta `detected = detector.detect(Path("."))`
  - Imprime `Language: {detected.language}` (debería ser PYTHON)
  - Imprime `Package Manager: {detected.package_manager}` (debería ser UV)
  - Imprime `Framework: {detected.framework}` (debería ser NONE)
  - Imprime `App Root: {detected.app_root}` (debería ser "tac_bootstrap" o similar)
- Ejecutar con `uv run python -c "..."` desde `tac_bootstrap_cli/`
- Verificar que las detecciones son correctas para el proyecto tac_bootstrap_cli

### Task 16: Ejecutar comandos de validación
- Ejecutar todos los comandos listados en la sección "Validation Commands"
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` y verificar que pasa sin regresiones
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check .` y verificar que no hay errores de linting
- Ejecutar `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` y verificar que no hay errores de tipos
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --help` y verificar que funciona (smoke test)
- Marcar todos los acceptance criteria como completados si todos los comandos pasan

## Testing Strategy

### Unit Tests
El módulo será probado mediante:
1. **Test inline durante desarrollo** (Task 15): Verificar detección correcta en el repositorio tac_bootstrap_cli (Python + uv)
2. **Tests existentes**: El módulo no rompe funcionalidad existente (validation commands)
3. **Tests futuros**: Cuando se integre con el wizard en `add-agentic`, se probarán otros tipos de proyectos

### Edge Cases
Casos edge que el módulo debe manejar:

1. **Repositorio vacío**: `_detect_language()` retorna `Language.PYTHON` (default)
2. **package.json malformado**: `_read_package_json()` retorna `None` sin error
3. **pyproject.toml sin dependencies**: `_get_python_deps()` retorna lista vacía
4. **Múltiples frameworks**: Retorna el primero detectado según orden de prioridad (FastAPI antes que Django)
5. **No app_root encontrado**: Retorna `"."` como default
6. **No scripts en package.json**: `commands` dict queda vacío
7. **TypeScript como dependency de JS project**: Correctamente detecta como TypeScript
8. **Lock files múltiples**: Prioridad definida (uv.lock > poetry.lock > Pipfile.lock)

## Acceptance Criteria

1. ✅ El archivo `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py` existe
2. ✅ Dataclass `DetectedProject` tiene campos `language`, `framework`, `package_manager`, `app_root`, `commands`, `confidence`
3. ✅ Clase `DetectService` tiene método `detect(repo_path: Path) -> DetectedProject`
4. ✅ `_detect_language()` detecta Python por `pyproject.toml`, `requirements.txt`, etc.
5. ✅ `_detect_language()` detecta TypeScript por `tsconfig.json`
6. ✅ `_detect_language()` detecta JavaScript, Go, Rust, Java por sus archivos característicos
7. ✅ `_detect_package_manager()` detecta correctamente gestores por lock files (uv, poetry, npm, pnpm, yarn, bun, cargo, maven, gradle)
8. ✅ `_detect_framework()` detecta frameworks Python (FastAPI, Django, Flask)
9. ✅ `_detect_framework()` detecta frameworks TypeScript/JavaScript (Next.js, NestJS, Express, React, Vue)
10. ✅ `_detect_framework()` detecta frameworks Go (Gin, Echo), Rust (Axum, Actix), Java (Spring)
11. ✅ `_detect_app_root()` identifica directorios comunes (src, app, lib) o directorio con `__init__.py` para Python
12. ✅ `_detect_commands()` extrae comandos de `package.json` scripts correctamente
13. ✅ `_read_package_json()` parsea JSON y maneja errores gracefully
14. ✅ `_get_python_deps()` extrae dependencias de `pyproject.toml` y `requirements.txt`
15. ✅ Script inline de prueba detecta correctamente el proyecto tac_bootstrap_cli (Python + uv)
16. ✅ Todos los validation commands pasan sin regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Dependencias adicionales
- Python 3.11+ tiene `tomllib` builtin para parsear TOML
- Python 3.10 requiere `tomli` (agregar con `uv add tomli` si es necesario)
- Verificar versión de Python en pyproject.toml antes de decidir

### Integración futura
- Este servicio será consumido por `WizardService` en el comando `add-agentic`
- Los valores detectados se usarán como defaults sugeridos en el wizard interactivo
- El usuario podrá override cualquier valor detectado

### Limitaciones conocidas
- No usa APIs externas (solo análisis local)
- No analiza contenido completo de archivos grandes (solo dependencias y configs)
- Confidence score es hardcoded a 0.8 (TODO: implementar cálculo real basado en cantidad de indicadores encontrados)
- No detecta monorepos o proyectos multi-lenguaje (retorna el lenguaje más prominente)

### Consideraciones de diseño
- Métodos privados organizados por tipo de detección para mantener código limpio
- Uso de Optional para valores que pueden no detectarse
- Defaults razonables para todos los campos
- No lanza excepciones, retorna valores default en caso de error
- Parsing defensivo con try/except para archivos malformados
