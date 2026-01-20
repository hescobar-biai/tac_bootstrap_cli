# Feature: Implementar DoctorService

## Metadata
issue_number: `36`
adw_id: `7f57eb36`
issue_json: `{"number":36,"title":"TAREA 7.1: Implementar DoctorService","body":"# Prompt para Agente\n\n## Contexto\nEl comando `doctor` necesita validar que un setup de Agentic Layer esta completo\ny funcional. Debe detectar problemas comunes y sugerir correcciones.\n\n## Objetivo\nImplementar DoctorService que diagnostica y puede reparar setups de Agentic Layer.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py`"}`

## Feature Description
Esta feature implementa un servicio de diagnóstico (`DoctorService`) que valida la completitud y funcionalidad de un setup de Agentic Layer generado por TAC Bootstrap. El servicio realiza health checks exhaustivos, detecta problemas comunes (directorios faltantes, archivos de configuración inválidos, hooks no ejecutables), y puede auto-reparar issues automáticamente.

El `DoctorService` será utilizado por el comando `tac-bootstrap doctor` del CLI para proporcionar validación post-setup, debugging de configuraciones problemáticas, y mantenimiento de proyectos existentes con Agentic Layer.

## User Story
As a developer who has set up an Agentic Layer in my project
I want a doctor command that validates my setup and fixes common issues
So that I can quickly identify and resolve configuration problems without manual debugging

## Problem Statement
Después de generar un Agentic Layer con `tac-bootstrap init` o `tac-bootstrap add-agentic`, pueden ocurrir problemas:
- Directorios requeridos faltantes (.claude, .claude/commands, .claude/hooks)
- Directorios opcionales faltantes (adws, specs, scripts) que limitan funcionalidad
- Archivos de configuración inválidos (.claude/settings.json con JSON malformado, config.yml con YAML inválido)
- Hooks no ejecutables que Claude Code no puede invocar
- Comandos slash faltantes que rompen workflows ADW
- Setups incompletos de ADW (adws/adw_modules faltante, sin workflows)

Sin una herramienta de diagnóstico, el usuario debe:
1. Investigar manualmente qué está fallando cuando Claude Code no funciona correctamente
2. Recordar qué archivos y directorios son requeridos vs opcionales
3. Validar manualmente JSON y YAML de configuración
4. Corregir permisos de archivos manualmente
5. Debugging tedioso sin feedback claro sobre qué está mal

Además, no hay forma de verificar que el setup está completo antes de ejecutar workflows ADW, lo cual puede resultar en fallos en medio de ejecución.

## Solution Statement
Implementar el módulo `tac_bootstrap/application/doctor_service.py` con:

1. **Enum `Severity`**: Niveles de severidad (ERROR, WARNING, INFO) para clasificar issues
2. **Dataclass `Issue`**: Representación estructurada de un issue con severity, message, suggestion, fix_fn
3. **Dataclass `DiagnosticReport`**: Resultado de diagnóstico con flag healthy y lista de issues
4. **Dataclass `FixResult`**: Resultado de intentos de corrección con contadores y mensajes
5. **Clase `DoctorService`**: Servicio principal con métodos `diagnose(repo_path: Path) -> DiagnosticReport` y `fix(repo_path: Path, report: DiagnosticReport) -> FixResult`
6. **Checks comprehensivos**:
   - Directory structure (requeridos: .claude, .claude/commands, .claude/hooks; opcionales: adws, specs, scripts)
   - Claude config (.claude/settings.json existe y es JSON válido con campo permissions)
   - Commands (comandos esenciales: prime.md, test.md, commit.md)
   - Hooks (pre_tool_use.py, post_tool_use.py son ejecutables)
   - ADWs (adws/adw_modules existe, al menos un workflow adw_*.py existe)
   - Config YAML (config.yml existe, es YAML válido con campos project y commands)
7. **Auto-fix capability**:
   - Crear directorios faltantes con _fix_create_dir()
   - Hacer hooks ejecutables con _fix_make_executable()
8. **Métodos privados organizados**: Cada tipo de check en método dedicado para mantener claridad

El servicio opera sin APIs externas, solo análisis local de archivos, y retorna reports estructurados con sugerencias humano-legibles.

## Relevant Files
Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/application/detect_service.py** - Patrón de referencia para servicios de application layer (estructura, docstrings, métodos privados organizados)
- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Referencia para imports y estructura de dataclasses si necesario
- **PLAN_TAC_BOOTSTRAP.md** - Contexto sobre TAREA 7.1 y estructura del Agentic Layer

### New Files
- **tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py** - Módulo principal a crear con DoctorService, Issue, DiagnosticReport, FixResult, Severity

## Implementation Plan

### Phase 1: Foundation
Crear el módulo base con enums y dataclasses:
- Definir enum `Severity` con valores ERROR, WARNING, INFO
- Crear dataclass `Issue` con campos severity, message, suggestion, fix_fn
- Crear dataclass `DiagnosticReport` con healthy flag, lista de issues, método add_issue()
- Crear dataclass `FixResult` con contadores fixed_count/failed_count y mensajes
- Crear clase `DoctorService` con estructura de métodos principales y privados

### Phase 2: Core Diagnostic Checks
Implementar checks fundamentales:
- `_check_directory_structure()`: Detectar directorios faltantes (requeridos vs opcionales)
- `_check_claude_config()`: Validar .claude/settings.json existe y es JSON válido
- `_check_config_yml()`: Validar config.yml existe y es YAML válido con campos requeridos

### Phase 3: Advanced Diagnostic Checks
Implementar checks auxiliares:
- `_check_commands()`: Detectar comandos slash faltantes (esenciales + check si hay alguno)
- `_check_hooks()`: Detectar hooks no ejecutables
- `_check_adws()`: Detectar ADW setup incompleto (modules dir, workflows)

### Phase 4: Auto-Fix Implementation
Implementar funcionalidad de reparación:
- `fix()`: Iterar sobre issues con fix_fn y ejecutar correcciones
- `_fix_create_dir()`: Crear directorios faltantes con mkdir
- `_fix_make_executable()`: Hacer hooks ejecutables con chmod

### Phase 5: Integration & Testing
Verificar integración y testing:
- Ejecutar script de prueba inline en directorio temporal vacío
- Validar detección de múltiples issues con severidad correcta
- Confirmar integración con validation commands

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear archivo doctor_service.py con estructura base
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py`
- Agregar module-level docstring explicando propósito: validación de Agentic Layer setups, health checks, auto-fix de issues comunes
- Importar dependencias necesarias: `dataclass`, `field` de dataclasses; `Enum` de enum; `Path` de pathlib; `List`, `Optional`, `Callable` de typing; `subprocess` para potencial uso futuro
- Verificar que el archivo se creó correctamente

### Task 2: Implementar enum Severity
- Definir clase `Severity(str, Enum)` para niveles de severidad
- Agregar valor `ERROR = "error"` con comentario "Must fix for functionality"
- Agregar valor `WARNING = "warning"` con comentario "Should fix for best results"
- Agregar valor `INFO = "info"` con comentario "Optional improvement"
- Agregar docstring explicando propósito del enum

### Task 3: Implementar dataclass Issue
- Definir dataclass `Issue` con decorador `@dataclass`
- Agregar campo `severity: Severity` (requerido)
- Agregar campo `message: str` (requerido) - descripción del issue
- Agregar campo `suggestion: Optional[str] = None` - sugerencia de corrección
- Agregar campo `fix_fn: Optional[Callable[[Path], bool]] = None` - función de auto-fix
- Agregar docstring explicando propósito: representación de un issue detectado

### Task 4: Implementar dataclass DiagnosticReport
- Definir dataclass `DiagnosticReport` con decorador `@dataclass`
- Agregar campo `healthy: bool = True` - flag de salud general
- Agregar campo `issues: List[Issue] = field(default_factory=list)` - lista de issues
- Implementar método `add_issue(self, issue: Issue) -> None`:
  - Agregar issue a lista
  - Si issue.severity == Severity.ERROR, setear self.healthy = False
- Agregar docstring explicando propósito: resultado de diagnostic check

### Task 5: Implementar dataclass FixResult
- Definir dataclass `FixResult` con decorador `@dataclass`
- Agregar campo `fixed_count: int = 0` - contador de fixes exitosos
- Agregar campo `failed_count: int = 0` - contador de fixes fallidos
- Agregar campo `messages: List[str] = field(default_factory=list)` - mensajes de resultado
- Agregar docstring explicando propósito: resultado de intentos de corrección

### Task 6: Implementar estructura base de DoctorService
- Definir clase `DoctorService` con docstring comprehensivo y ejemplo de uso
- Implementar método `diagnose(self, repo_path: Path) -> DiagnosticReport`:
  - Crear DiagnosticReport vacío
  - Llamar a todos los métodos de check (placeholder por ahora)
  - Retornar report
- Implementar método `fix(self, repo_path: Path, report: DiagnosticReport) -> FixResult`:
  - Crear FixResult vacío
  - Iterar sobre issues en report
  - Si issue tiene fix_fn, ejecutar y trackear resultado
  - Retornar FixResult
- Agregar docstrings con Args y Returns para ambos métodos

### Task 7: Implementar _check_directory_structure()
- Definir método privado `_check_directory_structure(self, repo_path: Path, report: DiagnosticReport) -> None`
- Crear lista de directorios requeridos: [".claude", ".claude/commands", ".claude/hooks"]
- Iterar sobre directorios requeridos y verificar existencia
- Si falta, agregar Issue con severity=ERROR, mensaje descriptivo, suggestion con comando mkdir, fix_fn con lambda que llama _fix_create_dir
- Crear lista de directorios opcionales: ["adws", "specs", "scripts"]
- Iterar sobre directorios opcionales y verificar existencia
- Si falta, agregar Issue con severity=WARNING, mensaje descriptivo, suggestion explicando beneficio del directorio
- Agregar docstring explicando propósito

### Task 8: Implementar _check_claude_config()
- Definir método privado `_check_claude_config(self, repo_path: Path, report: DiagnosticReport) -> None`
- Verificar que .claude/settings.json existe, si no reportar ERROR y retornar early
- Intentar parsear JSON con json.loads(), capturar JSONDecodeError
- Si JSON es inválido, reportar ERROR con mensaje descriptivo y retornar
- Verificar que settings tiene campo "permissions", si no reportar WARNING
- Agregar docstring explicando propósito

### Task 9: Implementar _check_commands()
- Definir método privado `_check_commands(self, repo_path: Path, report: DiagnosticReport) -> None`
- Verificar que .claude/commands existe, si no retornar early (ya reportado en directory check)
- Crear lista de comandos esenciales: ["prime.md", "test.md", "commit.md"]
- Iterar sobre comandos esenciales y verificar existencia
- Si falta, reportar WARNING explicando que el comando es comúnmente usado
- Verificar que existe al menos un archivo .md en commands/, si no reportar ERROR
- Agregar docstring explicando propósito

### Task 10: Implementar _check_hooks()
- Definir método privado `_check_hooks(self, repo_path: Path, report: DiagnosticReport) -> None`
- Verificar que .claude/hooks existe, si no retornar early
- Crear lista de hook files: ["pre_tool_use.py", "post_tool_use.py"]
- Iterar sobre hooks y verificar si existen
- Si existe, verificar si es ejecutable con os.access(hook_path, os.X_OK)
- Si no es ejecutable, reportar WARNING con suggestion chmod, fix_fn con lambda que llama _fix_make_executable
- Agregar import de `os` al inicio del archivo
- Agregar docstring explicando propósito

### Task 11: Implementar _check_adws()
- Definir método privado `_check_adws(self, repo_path: Path, report: DiagnosticReport) -> None`
- Verificar que adws/ existe, si no retornar early (es opcional)
- Verificar que adws/adw_modules/ existe, si no reportar WARNING
- Buscar workflows con glob adws/adw_*.py
- Si no hay workflows, reportar INFO sugiriendo agregar adw_sdlc_iso.py
- Agregar docstring explicando propósito

### Task 12: Implementar _check_config_yml()
- Definir método privado `_check_config_yml(self, repo_path: Path, report: DiagnosticReport) -> None`
- Verificar que config.yml existe, si no reportar WARNING explicando beneficio de config.yml para regeneración idempotente y retornar
- Intentar parsear YAML con yaml.safe_load(), capturar YAMLError
- Si YAML es inválido, reportar ERROR con mensaje descriptivo y retornar
- Verificar que config no es None/vacío, si es vacío reportar ERROR
- Crear lista de campos requeridos: ["project", "commands"]
- Iterar sobre campos requeridos y verificar existencia
- Si falta campo, reportar ERROR
- Agregar import de `yaml` al inicio del archivo
- Agregar docstring explicando propósito

### Task 13: Implementar _fix_create_dir()
- Definir método privado `_fix_create_dir(self, repo_path: Path, dir_path: str) -> bool`
- Construir full_path combinando repo_path / dir_path
- Llamar full_path.mkdir(parents=True, exist_ok=True)
- Verificar con full_path.is_dir() y retornar bool
- Agregar docstring explicando propósito

### Task 14: Implementar _fix_make_executable()
- Definir método privado `_fix_make_executable(self, repo_path: Path, hook: str) -> bool`
- Construir hook_path como repo_path / ".claude" / "hooks" / hook
- Verificar que hook_path existe, si no retornar False
- Importar stat module al inicio del archivo
- Obtener permisos actuales con hook_path.stat().st_mode
- Agregar permisos de ejecución con chmod: current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
- Verificar que ahora es ejecutable con os.access() y retornar bool
- Agregar docstring explicando propósito

### Task 15: Conectar checks en método diagnose()
- Actualizar método diagnose() para llamar a todos los checks:
  - self._check_directory_structure(repo_path, report)
  - self._check_claude_config(repo_path, report)
  - self._check_commands(repo_path, report)
  - self._check_hooks(repo_path, report)
  - self._check_adws(repo_path, report)
  - self._check_config_yml(repo_path, report)
- Asegurar que todos los checks se ejecutan y acumulan issues en report

### Task 16: Ejecutar validación inline
- Ejecutar comandos de verificación:
  - cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
  - cd tac_bootstrap_cli && uv run ruff check .
  - cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
  - cd tac_bootstrap_cli && uv run tac-bootstrap --help (smoke test)
- Ejecutar test inline en directorio temporal:
  ```python
  from tac_bootstrap.application.doctor_service import DoctorService
  from pathlib import Path
  import tempfile

  doctor = DoctorService()
  with tempfile.TemporaryDirectory() as tmp:
      report = doctor.diagnose(Path(tmp))
      print(f'Healthy: {report.healthy}')
      print(f'Issues: {len(report.issues)}')
      for issue in report.issues[:5]:
          print(f'  [{issue.severity.value}] {issue.message}')
  ```
- Verificar que se detectan múltiples issues (directorios faltantes, archivos faltantes)
- Verificar que healthy es False debido a ERRORs

## Testing Strategy

### Unit Tests
Tests necesarios (a implementar en fase futura):
- Test de Severity enum tiene valores correctos
- Test de Issue dataclass acepta todos los campos
- Test de DiagnosticReport.add_issue() actualiza healthy flag
- Test de DoctorService.diagnose() en directorio vacío detecta todos los issues esperados
- Test de DoctorService.diagnose() en setup válido retorna healthy=True
- Test de DoctorService.fix() puede crear directorios
- Test de DoctorService.fix() puede hacer hooks ejecutables
- Test de _check_claude_config() detecta JSON malformado
- Test de _check_config_yml() detecta YAML malformado

### Edge Cases
Casos edge a probar:
- Directorio que no existe como repo_path
- settings.json con JSON válido pero sin campo permissions
- config.yml vacío
- Hooks que existen pero no son ejecutables
- adws/ existe pero sin adw_modules/
- .claude/commands existe pero sin archivos .md

## Acceptance Criteria
- [ ] DoctorService detecta directorios faltantes con severidad correcta (ERROR para requeridos, WARNING para opcionales)
- [ ] DoctorService valida JSON de settings.json y detecta errores de sintaxis
- [ ] DoctorService valida YAML de config.yml y detecta errores de sintaxis
- [ ] DoctorService detecta hooks no ejecutables y sugiere chmod
- [ ] DoctorService.fix() puede crear directorios faltantes exitosamente
- [ ] DoctorService.fix() puede hacer hooks ejecutables exitosamente
- [ ] DiagnosticReport.healthy es False cuando hay al menos un ERROR
- [ ] DiagnosticReport contiene sugerencias humano-legibles para cada issue
- [ ] Código pasa pytest, ruff, mypy sin errores
- [ ] Test inline en directorio vacío detecta múltiples issues

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.application.doctor_service import DoctorService; from pathlib import Path; import tempfile; doctor = DoctorService(); tmp = tempfile.mkdtemp(); report = doctor.diagnose(Path(tmp)); print(f'Healthy: {report.healthy}'); print(f'Issues: {len(report.issues)}'); [print(f'  [{issue.severity.value}] {issue.message}') for issue in report.issues[:5]]; import shutil; shutil.rmtree(tmp)"` - Test inline

## Notes
- No intentar fixes que requieran network (descarga de archivos, clonado de repos)
- No modificar archivos de usuario sin fix_fn explícito aprobado
- Mantener métodos privados organizados y con docstrings claros
- Seguir patrón de DetectService para estructura y estilo
- Severidad ERROR debe usarse solo para issues que rompen funcionalidad crítica
- Severidad WARNING para issues que limitan funcionalidad pero no rompen workflow básico
- Severidad INFO para mejoras opcionales que no afectan funcionalidad
- fix_fn debe ser idempotente (ejecutar múltiples veces no debe causar errores)
- Todos los checks deben ser defensivos y no lanzar excepciones no manejadas
- JSON/YAML parsing debe usar try/except y reportar errores descriptivos
