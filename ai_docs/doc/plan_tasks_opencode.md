# Plan de Implementación: Soporte Multi-Provider (OpenCode, Cursor, Aider)

## OBJECTIVE

Implementar capacidad de detectar y soportar múltiples proveedores de agentes (Claude Code, OpenCode, y futuros proveedores) en TAC Bootstrap, con detección automática basada en configuración o labels de GitHub issues, incluyendo testing exhaustivo, ADWs multi-provider, y herramientas de migración.

**Version Target:** 0.8.0
**Total Tasks:** 24 (14 originales + 10 complementarias críticas)

---

## ASSUMPTIONS

1. **OpenCode es compatible con el patrón de comandos y agentes similar a Claude Code**
2. **OpenCode usa directorio `.opencode/` en lugar de `.claude/`**
3. **Los comandos de OpenCode pueden diferir en sintaxis o flags**
4. **Los issues de GitHub pueden tener labels para especificar el proveedor: `/claude` o `/opencode`**
5. **El config.yml es la fuente de verdad para el proveedor por defecto del proyecto**
6. **Los comandos de OpenCode usan el CLI `opencode` en lugar de `claude`**
7. **TAC-12 features (scout, parallel build, ai_docs) deben funcionar en todos los proveedores**
8. **Los ADWs deben ser provider-agnostic y detectar automáticamente el proveedor del proyecto**
9. **Debe existir herramienta de migración entre proveedores con rollback**
10. **Arquitectura debe permitir agregar nuevos proveedores (Cursor, Aider) sin refactoring mayor**

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                     TAC Bootstrap CLI                        │
├─────────────────────────────────────────────────────────────┤
│  Provider Detection Layer                                    │
│  ├─ GitHub Label Detection (/claude, /opencode)             │
│  ├─ config.yml Parser                                        │
│  └─ Default Fallback                                         │
├─────────────────────────────────────────────────────────────┤
│  Provider Abstraction Interface                              │
│  ├─ AgentProviderInterface (abstract)                       │
│  ├─ ClaudeProvider (implementation)                         │
│  ├─ OpenCodeProvider (implementation)                       │
│  └─ Future: CursorProvider, AiderProvider                   │
├─────────────────────────────────────────────────────────────┤
│  Scaffold Service (Multi-Provider)                          │
│  ├─ Template Selection by Provider                          │
│  ├─ Directory Structure Generation                          │
│  └─ Config File Generation                                  │
├─────────────────────────────────────────────────────────────┤
│  ADWs (Provider-Aware)                                       │
│  ├─ Auto-detect project provider                            │
│  ├─ Execute commands with correct CLI                       │
│  └─ TAC-12 features work across providers                   │
└─────────────────────────────────────────────────────────────┘
```

---

## TAREAS

### [FEATURE] Task 1: Actualizar modelo AgenticProvider para incluir OPENCODE

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py`

**Description:**
Agregar nueva opción `OPENCODE` al enum `AgenticProvider` para soportar el agente OpenCode además de Claude Code.

**Acceptance Criteria:**
- Enum `AgenticProvider` tiene valor `OPENCODE = "opencode"`
- El enum mantiene compatibilidad con `CLAUDE_CODE = "claude_code"`
- Se actualiza la docstring del enum para documentar ambos proveedores

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_1
```

---

### [FEATURE] Task 2: Crear modelo OpenCodeConfig para configuración del proveedor OpenCode

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py`

**Description:**
Crear modelo `OpenCodeConfig` similar a `ClaudeConfig` para configuración específica del proveedor OpenCode.

**Acceptance Criteria:**
- Modelo `OpenCodeConfig` creado con campos:
  - `settings: OpenCodeSettings` (similar a ClaudeSettings)
  - `commands: OpenCodeCommandsConfig` (similar a ClaudeCommandsConfig)
  - Campos incluyen:
  - `project_name: str` (nombre del proyecto para OpenCode)
  - `preferred_style: str` (estilo de comunicación preferido)
  - `allow_shell: bool` (permite ejecución de comandos shell)

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_2
```

---

### [FEATURE] Task 4: Crear servicio de detección de proveedor desde issue

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/provider_detector.py` (nuevo archivo)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/__init__.py`

**Description:**
Crear módulo `provider_detector.py` que detecta el proveedor de agente apropiado basado en:
1. Labels del issue de GitHub (`/claude` o `/opencode`)
2. Configuración en `config.yml` (si no hay label)
3. Valor por defecto en `TACConfig.agentic.provider`

**Acceptance Criteria:**
- Función `detect_provider_from_issue(issue_number: str, repo_path: str) -> AgenticProvider` creada
- Función busca labels `/claude` y `/opencode` en el issue
- Si no hay labels, usa `config.yml` como fallback
- Si no hay config, usa valor por defecto de `TACConfig`
- Módulo exportado en `adw_modules/__init__.py`
- Maneja errores cuando no se puede detectar el proveedor

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_3
```

---

### [FEATURE] Task 5: Actualizar scaffold_service para soportar generación multi-proveedor

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`

**Description:**
Modificar `scaffold_service.py` para generar la estructura correcta según el proveedor configurado:
- Si `provider == "claude_code"`: genera directorio `.claude/` (comportamiento actual)
- Si `provider == "opencode"`: genera directorio `.opencode/` con equivalentes de OpenCode

**Acceptance Criteria:**
- Método `_add_claude_files` renombrado a `_add_agent_files`
- Método detecta el proveedor desde `config.agentic.provider`
- Si proveedor es `claude_code`: llama `_add_claude_files` (lógica existente)
- Si proveedor es `opencode`: llama nuevo método `_add_opencode_files`
- Método `_add_opencode_files` crea estructura similar a `.claude/` pero en directorio `.opencode/`:
  - `.opencode/settings.json` (configuración de OpenCode)
  - `.opencode/commands/*.md` (comandos slash de OpenCode)
  - `.opencode/agents/*.md` (definiciones de agentes de OpenCode)
  - `.opencode/hooks/*.py` (hooks de OpenCode)

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_4
```

---

### [FEATURE] Task 6: Crear directorio de templates para OpenCode

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/opencode/` (nuevo directorio)

**Description:**
Crear directorio de templates Jinja2 para archivos de configuración de OpenCode.

**Acceptance Criteria:**
- Directorio `/templates/opencode/` creado con los siguientes archivos:
  - `settings.json.j2` (template de configuración de OpenCode)
  - `settings.local.json.j2` (template de configuración local)
  - `commands/README.md.j2` (template de README de comandos)

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_5
```

---

### [CHORE] Task 7: Actualizar CLI para aceptar parámetro --agentic-provider

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`

**Description:**
Agregar parámetro `--agentic-provider` al comando `init` para permitir especificar el proveedor de agentes explícitamente.

**Acceptance Criteria:**
- Parámetro `--agentic-provider` agregado con opciones: `claude_code` (default), `opencode`
- Help del comando actualizado para documentar el nuevo parámetro
- Parámetro validado contra el enum `AgenticProvider`

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_6
```

---

### [FEATURE] Task 8: Actualizar detect_service para usar provider_detector

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`

**Description:**
Modificar `detect_service` para integrar el nuevo módulo `provider_detector` y retornar el proveedor detectado.

**Acceptance Criteria:**
- Servicio actualizado para importar `provider_detector`
- Función principal detecta proveedor usando `provider_detector.detect_provider_from_issue()`
- Retorna `AgenticProvider` enum con el proveedor detectado

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_7
```

---

### [FEATURE] Task 9: Actualizar modelo TACConfig para usar campo agentic_provider

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py`

**Description:**
Actualizar el campo `agentic: AgenticSpec` para usar el nuevo modelo que incluye soporte para ambos proveedores.

**Acceptance Criteria:**
- Campo `agentic` en `TACConfig` usa el modelo actualizado
- Tipo de `provider` validado contra `AgenticProvider` enum
- Compatibilidad mantenida con configuraciones existentes

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_8
```

---

### [FEATURE] Task 10: Actualizar templates de comandos para soportar OpenCode CLI

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2`

**Description:**
Actualizar los templates de scripts de documentación para soportar el proveedor OpenCode:
- Añadir opción `--opencode-model` similar a `--claude-model`
- Actualizar lógica de detección de proveedor
- Agregar documentación sobre el CLI de OpenCode

**Acceptance Criteria:**
- Templates incluyen lógica para detectar proveedor del proyecto
- Si proveedor es `opencode`: usa `opencode` CLI en lugar de `claude` CLI
- Scripts aceptan parámetro `--agentic-provider` o detectan desde config
- Documentación actualizada menciona ambos proveedores

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_9
```

---

### [FEATURE] Task 11: Crear plantillas de comandos de OpenCode

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/opencode/commands/` (nuevo directorio)

**Description:**
Crear templates Jinja2 para comandos slash de OpenCode equivalentes a los de Claude Code.

**Acceptance Criteria:**
- Directorio `/templates/opencode/commands/` creado con archivos:
  - `prime.md.j2` (comando de priming para OpenCode)
  - `start.md.j2` (comando de inicio)
  - `build.md.j2` (comando de construcción)
  - `test.md.j2` (comando de pruebas)
  - `review.md.j2` (comando de revisión)
  - `ship.md.j2` (comando de entrega)
- Cada template usa sintaxis de OpenCode CLI (diferente de Claude Code)
- Variables de Jinja2 adaptadas para `{{ config.agentic.provider }}`

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_10
```

---

### [FEATURE] Task 12: Crear plantillas de agentes de OpenCode

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/opencode/agents/` (nuevo directorio)

**Description:**
Crear templates Jinja2 para definiciones de agentes de OpenCode equivalentes a los agentes de Claude Code.

**Acceptance Criteria:**
- Directorio `/templates/opencode/agents/` creado con archivos:
  - `build-agent.md.j2` (agente de construcción paralela)
  - `scout-report-suggest.md.j2` (agente de exploración)
  - `scout-report-suggest-fast.md.j2` (agente de exploración rápida)
  - `docs-scraper.md.j2` (agente de scraping de documentación)
  - `meta-agent.md.j2` (agente de generación de otros agentes)
- Cada template usa sintaxis de definición de agentes de OpenCode
- Incluye herramientas y configuraciones apropiadas para OpenCode

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_11
```

---

### [FEATURE] Task 13: Crear plantillas de hooks de OpenCode

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/opencode/hooks/` (nuevo directorio)

**Description:**
Crear templates Jinja2 para hooks de ejecución de OpenCode equivalentes a los hooks de Claude Code.

**Acceptance Criteria:**
- Directorio `/templates/opencode/hooks/` creado con archivos:
  - `send_event.py.j2` (hook de envío de eventos)
  - `session_start.py.j2` (hook de inicio de sesión)
  - `stop.py.j2` (hook de detención)
  - `utils/__init__.py.j2` (módulo de utilidades)
  - `utils/constants.py.j2` (constantes compartidas)
- Cada template usa sintaxis de hooks de OpenCode
- Implementa funcionalidad equivalente a hooks de Claude Code pero adaptada a OpenCode

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_12
```

---

### [CHORE] Task 3: Actualizar config.yml para soportar campo provider en agentic

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`

**Description:**
Actualizar la documentación del CLI para incluir información sobre el proveedor OpenCode.

**Acceptance Criteria:**
- Sección nueva agregada: "Agentic Providers" con descripción de Claude Code y OpenCode
- Documentación de `--agentic-provider` agregada
- Tabla de equivalencias de comandos entre proveedores
- Ejemplos de uso con ambos proveedores

---

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_multi_provider_support_task_13
```

---

### [CHORE] Task 14: Actualizar README del CLI para documentar proveedor OpenCode

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`

**Description:**
Crear entrada de changelog para versión 0.8.0 documentando todos los cambios introducidos.

**Acceptance Criteria:**
- Nueva entrada `[0.8.0] - 2026-01-30` creada al inicio de CHANGELOG.md
- Cambios documentados:
  - **Added**: Soporte multi-proveedor (Claude Code y OpenCode)
  - **Added**: Detección automática de proveedor desde labels de GitHub issues
  - **Added**: CLI parameter `--agentic-provider` para especificar proveedor
  - **Added**: Templates para estructura `.opencode/`
  - **Changed**: `scaffold_service.py` refactorizado para soportar multi-proveedor
  - **Changed**: Actualizaciones en modelos de configuración
- Se incluye sección "Breaking Changes" si aplica
- Se incluye sección "Migration Guide" si aplica

---

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_multi_provider_support_task_14
```

---

### [FEATURE] Task 15: Suite de tests para multi-provider ⚠️ CRÍTICO

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/test_multi_provider.py` (nuevo)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/fixtures/opencode/` (nuevos fixtures)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/test_provider_detection.py` (nuevo)

**Description:**
Crear suite completa de tests para verificar funcionalidad multi-provider en todos los niveles:
- Detección correcta de proveedor desde múltiples fuentes
- Generación de estructura correcta según proveedor
- Compatibilidad de templates entre proveedores
- Switching entre proveedores sin errores

**Test Coverage:**
```python
# Provider Detection Tests
def test_detect_provider_from_claude_label()
def test_detect_provider_from_opencode_label()
def test_detect_provider_from_config_yml()
def test_detect_provider_fallback_to_default()
def test_cli_flag_overrides_all_detection()

# Scaffolding Tests
def test_scaffold_generates_claude_structure()
def test_scaffold_generates_opencode_structure()
def test_scaffold_creates_correct_directories()
def test_scaffold_uses_correct_templates()

# Migration Tests
def test_migration_claude_to_opencode()
def test_migration_opencode_to_claude()
def test_migration_creates_backup()
def test_migration_rollback_on_failure()

# Integration Tests
def test_end_to_end_claude_workflow()
def test_end_to_end_opencode_workflow()
def test_adw_detects_project_provider()
```

**Acceptance Criteria:**
- Test coverage > 90% para módulos multi-provider
- Tests pasan en CI/CD pipeline
- Fixtures incluyen ejemplos de ambos proveedores
- Mocks para CLIs externos (claude, opencode)
- Performance tests para detección de proveedor

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_15
```

---

### [FEATURE] Task 16: Actualizar ADWs para soporte multi-provider ⚠️ CRÍTICO

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/provider_utils.py` (nuevo)

**Description:**
Los ADWs necesitan detectar qué proveedor usa el proyecto y ejecutar comandos apropiados. Actualmente solo soportan Claude Code hardcodeado.

**Changes Required:**

```python
# Antes (solo Claude)
def execute_template(request: AgentTemplateRequest):
    cmd = ['claude', '--dangerously-skip-permissions', ...]
    subprocess.run(cmd)

# Después (multi-provider)
def execute_template(request: AgentTemplateRequest):
    provider = detect_project_provider(request.working_dir)
    cli_cmd = get_cli_command(provider)  # 'claude' o 'opencode'
    cmd = [cli_cmd, '--dangerously-skip-permissions', ...]
    subprocess.run(cmd)

def detect_project_provider(working_dir: str) -> AgenticProvider:
    """Detecta proveedor del proyecto actual."""
    if Path(working_dir / '.claude').exists():
        return AgenticProvider.CLAUDE_CODE
    elif Path(working_dir / '.opencode').exists():
        return AgenticProvider.OPENCODE
    else:
        # Lee config.yml o usa default
        return read_provider_from_config(working_dir)
```

**Acceptance Criteria:**
- `execute_template()` detecta proveedor del proyecto automáticamente
- `execute_prompt()` usa CLI correcto según proveedor
- ADWs funcionan en proyectos Claude Code y OpenCode sin cambios
- Logging indica qué proveedor se detectó y usó
- Error claro si proveedor no está instalado
- Funciona con worktrees aislados

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_16
```

---

### [FEATURE] Task 17: CLI para migrar proyectos entre proveedores

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/migration_service.py` (nuevo)

**Description:**
Herramienta para convertir proyectos existentes entre proveedores con backup automático y rollback.

**Command Interface:**
```bash
# Migrar proyecto actual
tac-bootstrap migrate --from claude_code --to opencode

# Dry-run (preview sin cambios)
tac-bootstrap migrate --from claude_code --to opencode --dry-run

# Con backup manual
tac-bootstrap migrate --to opencode --backup-dir /path/to/backup

# Rollback si algo falla
tac-bootstrap migrate --rollback
```

**Migration Process:**
1. Detecta estructura actual (.claude/ o .opencode/)
2. Valida que destino es diferente de origen
3. Crea backup automático con timestamp
4. Convierte comandos/agentes/hooks al nuevo proveedor
5. Actualiza config.yml con nuevo proveedor
6. Renombra directorio (.claude/ → .opencode/)
7. Ajusta sintaxis específica del proveedor
8. Genera reporte de cambios
9. Valida nueva estructura

**Acceptance Criteria:**
- Migración completa sin pérdida de datos
- Backup automático antes de cambios
- Rollback funcional si migración falla
- Reporte detallado de incompatibilidades
- Validación post-migración exitosa
- Soporte para dry-run mode

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_17
```

---

### [FEATURE] Task 18: Capa de abstracción de proveedor (Provider Interface)

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/provider_interface.py` (nuevo)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/providers/` (nuevo directorio)
  - `claude_provider.py`
  - `opencode_provider.py`
  - `base_provider.py`

**Description:**
API unificada para interactuar con cualquier proveedor, facilitando agregar nuevos proveedores sin modificar ADWs.

**Interface Design:**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class CommandResult:
    success: bool
    output: str
    error: Optional[str]
    exit_code: int

class AgentProviderInterface(ABC):
    """Abstract interface for agentic providers."""

    @abstractmethod
    def get_cli_name(self) -> str:
        """Returns CLI command name (e.g., 'claude', 'opencode')."""
        pass

    @abstractmethod
    def get_config_dir(self) -> str:
        """Returns config directory name (e.g., '.claude', '.opencode')."""
        pass

    @abstractmethod
    def execute_command(self, command: str, args: List[str],
                       working_dir: str) -> CommandResult:
        """Executes a slash command with the provider's CLI."""
        pass

    @abstractmethod
    def list_agents(self, working_dir: str) -> List[str]:
        """Lists available agents for this provider."""
        pass

    @abstractmethod
    def validate_command(self, command: str) -> bool:
        """Validates if command is supported by provider."""
        pass

class ClaudeProvider(AgentProviderInterface):
    def get_cli_name(self) -> str:
        return "claude"

    def get_config_dir(self) -> str:
        return ".claude"

    # ... implementations

class OpenCodeProvider(AgentProviderInterface):
    def get_cli_name(self) -> str:
        return "opencode"

    def get_config_dir(self) -> str:
        return ".opencode"

    # ... implementations

# Factory pattern for provider creation
def get_provider(provider_type: AgenticProvider) -> AgentProviderInterface:
    providers = {
        AgenticProvider.CLAUDE_CODE: ClaudeProvider(),
        AgenticProvider.OPENCODE: OpenCodeProvider(),
    }
    return providers[provider_type]
```

**Benefits:**
- Fácil agregar nuevos proveedores (Cursor, Aider, Continue)
- ADWs usan interface, no implementaciones concretas
- Testing más fácil con mocks
- Código más mantenible y SOLID

**Acceptance Criteria:**
- Interface definida con todos los métodos abstractos
- ClaudeProvider implementa interface completa
- OpenCodeProvider implementa interface completa
- Factory pattern funcional
- Tests unitarios para cada provider
- Documentación de cómo agregar nuevo proveedor

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_18
```

---

### [FEATURE] Task 19: Soporte para workflows híbridos (multi-provider per phase)

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`

**Description:**
Permitir usar diferentes proveedores para diferentes fases del workflow (e.g., Claude para planning, OpenCode para building).

**Use Cases:**
- Claude Opus para planning (mejor razonamiento) + OpenCode para building (más rápido)
- Claude Sonnet para implementation + Claude Haiku para testing (más económico)
- Proveedor específico por tipo de tarea

**Config Structure:**
```yaml
agentic:
  default_provider: claude_code  # Fallback
  workflows:
    planning:
      provider: claude_code
      model: opus
      reason: "Better architectural decisions"
    building:
      provider: opencode
      model: fast
      reason: "Faster implementation"
    testing:
      provider: claude_code
      model: sonnet
      reason: "Better test coverage"
    reviewing:
      provider: claude_code
      model: sonnet
      reason: "Thorough code review"
```

**ADW Changes:**
```python
# adw_plan_iso.py
provider = get_workflow_provider("planning", config)  # Returns claude_code

# adw_build_iso.py
provider = get_workflow_provider("building", config)  # Returns opencode
```

**Acceptance Criteria:**
- Config soporta provider por workflow phase
- ADWs leen config para determinar provider
- Resultados interoperables entre proveedores
- Validación de compatibilidad entre fases
- Documentación de best practices
- Logging indica qué provider usó cada fase

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_19
```

---

### [FEATURE] Task 20: Validador de compatibilidad de proveedor ✅ QUALITY

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/validator_service.py` (nuevo)

**Description:**
Valida que comandos/agentes/hooks sean compatibles con el proveedor configurado.

**Command Interface:**
```bash
# Validar proyecto actual
tac-bootstrap validate

# Validar contra proveedor específico
tac-bootstrap validate --provider opencode

# Output detallado
tac-bootstrap validate --verbose

# Solo errores
tac-bootstrap validate --errors-only
```

**Validation Checks:**
```
1. Commands Validation:
   ✅ Sintaxis de comandos válida para el proveedor
   ✅ Flags soportados por el CLI
   ✅ Modelos disponibles

2. Agents Validation:
   ✅ Herramientas disponibles en agentes
   ✅ Sintaxis de definición de agente
   ✅ Configuraciones soportadas

3. Hooks Validation:
   ✅ Hooks usan APIs correctas
   ✅ Dependencias instaladas
   ✅ Sintaxis Python válida

4. Config Validation:
   ✅ config.yml tiene campos requeridos
   ✅ Proveedor especificado existe
   ✅ Valores de configuración válidos
```

**Output Format:**
```
Validating project against provider: opencode

✅ Commands: 15/15 compatible
   ✅ /prime - compatible
   ✅ /build - compatible
   ... (13 more)

⚠️  Agents: 4/6 compatible
   ✅ scout-report-suggest - compatible
   ✅ scout-report-suggest-fast - compatible
   ❌ build-agent uses TodoWrite (not available in OpenCode)
   ❌ meta-agent uses MultiEdit (not available in OpenCode)
   ✅ docs-scraper - compatible
   ✅ playwright-validator - compatible

✅ Hooks: 9/9 compatible

⚠️  Overall: 28/30 checks passed (93% compatible)

Recommendations:
- Remove or replace build-agent.md
- Remove or replace meta-agent.md
- Consider using claude_code for parallel building workflows
```

**Acceptance Criteria:**
- Valida commands, agents, hooks, config
- Reporte claro con ✅ ⚠️ ❌
- Exit code apropiado para CI/CD
- Sugerencias de remediación
- Modo verbose con detalles
- Fast mode para validación rápida

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_20
```

---

### [FEATURE] Task 21: Herramienta de benchmarking multi-provider 📊

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/benchmark_service.py` (nuevo)

**Description:**
Ejecuta mismo workflow en múltiples proveedores y compara performance, costo, y calidad.

**Command Interface:**
```bash
# Benchmark issue específico
tac-bootstrap benchmark --issue 123 --providers claude_code,opencode

# Benchmark workflow completo
tac-bootstrap benchmark --workflow sdlc --providers all

# Output a archivo
tac-bootstrap benchmark --issue 123 --output benchmark_results.json
```

**Metrics Collected:**
```json
{
  "workflow": "Planning Issue #123",
  "timestamp": "2026-01-30T10:00:00Z",
  "results": {
    "claude_code": {
      "duration_seconds": 45,
      "tokens_consumed": 12000,
      "cost_usd": 0.24,
      "model_used": "claude-sonnet-4-5",
      "success": true,
      "output_quality_score": 0.95,
      "errors": 0
    },
    "opencode": {
      "duration_seconds": 28,
      "tokens_consumed": 8000,
      "cost_usd": 0.08,
      "model_used": "opencode-fast",
      "success": true,
      "output_quality_score": 0.88,
      "errors": 0
    }
  },
  "recommendation": "OpenCode: 38% faster, 66% cheaper, -7% quality"
}
```

**Output Display:**
```
Workflow: Planning for Issue #123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Provider      Time    Tokens  Cost    Quality  Result
────────────────────────────────────────────────────
Claude Code   45s     12K     $0.24   95%      ✅
OpenCode      28s     8K      $0.08   88%      ✅

📊 Comparison:
• OpenCode is 38% faster
• OpenCode uses 66% fewer tokens
• OpenCode costs 66% less
• Claude Code has 7% better quality score

💡 Recommendation:
Use OpenCode for speed and cost, Claude Code for quality
```

**Acceptance Criteria:**
- Ejecuta workflow en múltiples proveedores
- Mide tiempo, tokens, costo, calidad
- Output legible en terminal
- Exporta a JSON para análisis
- Cálculo de quality score (diff analysis)
- Recomendación basada en métricas

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_21
```

---

### [CHORE] Task 22: Documentar matriz de features por proveedor 📋

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/docs/PROVIDER_COMPARISON.md` (nuevo)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/docs/PROVIDER_MIGRATION.md` (nuevo)

**Description:**
Crear documentación completa comparando features entre proveedores.

**Content Structure:**

**File: docs/PROVIDER_COMPARISON.md**
```markdown
# Agentic Provider Comparison

## Feature Matrix

| Feature | Claude Code | OpenCode | Cursor | Aider | Notes |
|---------|------------|----------|--------|-------|-------|
| **Core Features** |
| Custom Agents | ✅ Full | ✅ Full | ❌ | ❌ | |
| Slash Commands | ✅ Full | ✅ Full | ⚠️ Limited | ❌ | |
| Hooks System | ✅ 7 types | ✅ 5 types | ❌ | ❌ | |
| Multi-file Edit | ✅ | ✅ | ✅ | ✅ | |
| **Advanced Features** |
| Parallel Agents | ✅ Stable | ⚠️ Beta | ❌ | ❌ | TAC-12 |
| Scout/Explore | ✅ | ⚠️ Partial | ❌ | ❌ | TAC-12 |
| Context Bundling | ✅ | ✅ | ❌ | ❌ | |
| **Performance** |
| Context Window | 200K | 128K | 200K | Unlimited | |
| Avg Response Time | Medium | Fast | Medium | Fast | |
| **Cost (per 1M tokens)** |
| Input | $3 | $1 | $3 | $0 (local) | |
| Output | $15 | $5 | $15 | $0 (local) | |
| **Best For** |
| Planning | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | |
| Implementation | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | |
| Refactoring | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | |
| Testing | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | |

## When to Use Each Provider

### Claude Code
✅ Best for: Complex planning, architectural decisions, comprehensive testing
✅ Strengths: Best reasoning, custom agents, full hook system
❌ Tradeoffs: Higher cost, slower execution

### OpenCode
✅ Best for: Fast implementation, prototyping, cost-sensitive projects
✅ Strengths: Fast, economical, good multi-file edit
❌ Tradeoffs: Limited agent customization, smaller context window

### Hybrid Approach (Recommended)
Use Claude Code for planning + OpenCode for building
```

**Acceptance Criteria:**
- Feature matrix completa y actualizada
- Comparación objetiva sin favoritismos
- Casos de uso claros
- Pros/cons de cada proveedor
- Recomendaciones prácticas
- Ejemplos de workflows híbridos

---

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_multi_provider_support_task_22
```

---

### [FEATURE] Task 23: Asegurar TAC-12 funciona en ambos proveedores 🔗 CRITICAL

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/` (TAC-12 commands)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.opencode/commands/` (nuevos equivalentes)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`

**Description:**
Verificar que todas las features TAC-12 recién implementadas funcionen en OpenCode, o crear adaptaciones.

**TAC-12 Features to Validate:**

| Feature | Claude Code | OpenCode | Action Required |
|---------|------------|----------|-----------------|
| model_extractor.py | ✅ Works | ✅ Works | ✅ Provider-agnostic |
| send_event.py | ✅ Works | ✅ Works | ✅ Provider-agnostic |
| summarizer.py | ⚠️ Anthropic API | ❌ Need adapter | 🔧 Create OpenCode adapter |
| /scout command | ✅ Native | ⚠️ Check | 🔍 Verify OpenCode equivalent |
| /plan_w_scouters | ✅ Native | ⚠️ Check | 🔍 Verify OpenCode equivalent |
| /build_in_parallel | ✅ build-agent | ⚠️ Check | 🔍 Verify OpenCode agent support |
| scout_codebase() | ✅ Works | ⚠️ Needs test | 🧪 Integration test |
| plan_with_scouts() | ✅ Works | ⚠️ Needs test | 🧪 Integration test |
| build_in_parallel() | ✅ Works | ⚠️ Needs test | 🧪 Integration test |

**Implementation Tasks:**

1. **Create OpenCode AI Adapter:**
```python
# adws/adw_modules/ai_adapter.py
def get_ai_client(provider: AgenticProvider):
    if provider == AgenticProvider.CLAUDE_CODE:
        return AnthropicClient()
    elif provider == AgenticProvider.OPENCODE:
        return OpenCodeAIClient()  # Uses OpenCode's AI API
```

2. **Update summarizer.py:**
```python
# Before (Claude-only)
import anthropic
client = anthropic.Anthropic(api_key=api_key)

# After (multi-provider)
from ai_adapter import get_ai_client
client = get_ai_client(detect_provider())
```

3. **Create OpenCode TAC-12 Commands:**
- `.opencode/commands/scout.md` (equivalent to Claude's /scout)
- `.opencode/commands/plan_w_scouters.md`
- `.opencode/commands/build_in_parallel.md`

4. **Test Integration:**
```bash
# Test scout in both providers
tac-bootstrap test-tac12 --provider claude_code --feature scout
tac-bootstrap test-tac12 --provider opencode --feature scout
```

**Acceptance Criteria:**
- All TAC-12 features work in Claude Code (already done)
- All TAC-12 features work in OpenCode or have documented alternatives
- AI adapter supports both providers
- Integration tests pass for both providers
- Documentation updated with provider-specific notes
- Fallback behavior if feature not available in provider

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_23
```

---

### [FEATURE] Task 24: Auto-update de templates de proveedores 🔄

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/update_service.py` (nuevo)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/registry.py` (nuevo)

**Description:**
Actualizar templates de proveedor desde fuente oficial cuando hay nuevas versiones.

**Command Interface:**
```bash
# Check for updates
tac-bootstrap check-updates

# Update specific provider
tac-bootstrap update-provider opencode --from-upstream

# Update all providers
tac-bootstrap update-provider all

# Dry-run (show what would change)
tac-bootstrap update-provider opencode --dry-run

# Update specific components
tac-bootstrap update-provider opencode --components commands,agents
```

**Update Process:**
1. Connect to template registry (GitHub, NPM, or custom)
2. Fetch latest version metadata
3. Compare local vs upstream versions
4. Show diff of changes
5. User approves/rejects changes
6. Merge new templates (preserve customizations)
7. Generate update report
8. Test updated templates

**Registry Structure:**
```json
{
  "providers": {
    "claude_code": {
      "version": "1.5.0",
      "registry_url": "https://registry.tac-bootstrap.com/claude",
      "templates": {
        "commands": "https://..../commands.tar.gz",
        "agents": "https://..../agents.tar.gz",
        "hooks": "https://..../hooks.tar.gz"
      }
    },
    "opencode": {
      "version": "1.2.0",
      "registry_url": "https://registry.tac-bootstrap.com/opencode",
      "templates": { ... }
    }
  }
}
```

**Acceptance Criteria:**
- Registry de templates oficiales funcional
- Detección de nuevas versiones
- Diff claro entre versión local y upstream
- Merge inteligente preserva customizaciones
- Rollback si update falla
- Update log con cambios aplicados
- Soporte para registry privado

---

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_24
```

---

## PRIORIDADES DE IMPLEMENTACIÓN

### MUST HAVE - Version 0.8.0 (Core Multi-Provider)
**Blocking for release:**
1. ✅ Task 1-14 (Plan original completo)
2. ⚠️ Task 15 (Testing multi-provider) - **CRÍTICO**
3. ⚠️ Task 16 (ADWs multi-provider) - **CRÍTICO**
4. ⚠️ Task 20 (Validator) - **QUALITY GATE**
5. ⚠️ Task 23 (TAC-12 integration) - **FEATURE PARITY**

**Estimated effort:** 40-50 hours
**Risk:** MEDIUM (nueva arquitectura)

### SHOULD HAVE - Version 0.8.1 (Developer Experience)
**High value, non-blocking:**
6. ✅ Task 17 (Migration tool)
7. ✅ Task 18 (Provider abstraction)
8. ✅ Task 22 (Feature matrix docs)

**Estimated effort:** 20-25 hours
**Risk:** LOW

### NICE TO HAVE - Version 0.9.0 (Advanced Features)
**Future enhancements:**
9. ✅ Task 19 (Hybrid workflows)
10. ✅ Task 21 (Benchmarking)
11. ✅ Task 24 (Auto-update)

**Estimated effort:** 30-35 hours
**Risk:** LOW

---

## RIESGOS Y MITIGACIÓN

### Riesgo 1: Mantenimiento de Templates Duplicados
**Problema:** 2x proveedores = 2x trabajo de actualización
**Impacto:** ALTO
**Mitigación:**
- Template inheritance: Base templates + provider overrides
- Automated sync CI job que valida paridad
- Shared components donde sea posible
- Provider abstraction layer reduce código duplicado

### Riesgo 2: Template Drift Entre Proveedores
**Problema:** Templates pueden divergir con el tiempo
**Impacto:** MEDIO
**Mitigación:**
- Validator automático (Task 20) en CI/CD
- Weekly sync checks
- Feature matrix documentation mantiene visibilidad
- Integration tests catch divergence early

### Riesgo 3: Complejidad de Testing
**Problema:** Testing aumenta exponencialmente con cada proveedor
**Impacto:** ALTO
**Mitigación:**
- Provider abstraction permite mock testing
- Shared test suite con provider parameter
- Focus en integration tests, no unit tests duplicados
- CI matrix testing (Task 15)

### Riesgo 4: Breaking Changes en Provider APIs
**Problema:** Proveedores externos pueden cambiar APIs
**Impacto:** ALTO
**Mitigación:**
- Version pinning en templates
- Provider abstraction aisla cambios
- Validation layer detecta incompatibilidades
- Auto-update tool (Task 24) facilita updates

### Riesgo 5: Performance Degradation
**Problema:** Provider detection overhead en cada operación
**Impacto:** BAJO
**Mitigación:**
- Caching de provider detection
- Single detection al inicio de workflow
- Benchmarking tool (Task 21) monitorea performance
- Lazy loading de provider implementations

---

## PARALLEL EXECUTION GROUPS (ACTUALIZADO)

| Grupo | Tareas | Dependencia | Prioridad | Descripción |
|-------|---------|-------------|-----------|-------------|
| **P1** | 1-3 | None | MUST | Modelos de dominio |
| **P2** | 4, 18 | P1 | MUST | Detección + Abstraction Layer |
| **P3** | 5-7, 16 | P2 | MUST | Scaffolding + ADWs |
| **P4** | 8-13 | P3 | MUST | Templates OpenCode |
| **P5** | 14-15, 20 | P4 | MUST | Docs + Testing + Validation |
| **P6** | 17, 22, 23 | P5 | SHOULD | Migration + Docs + TAC-12 |
| **P7** | 19, 21, 24 | P6 | NICE | Advanced features |

**Total estimado:** 90-110 horas
**Timeline:** 3-4 sprints (2 semanas cada uno)

---

## METRICS DE ÉXITO

### Version 0.8.0 (MVP Multi-Provider):
- ✅ 2 proveedores soportados (Claude Code, OpenCode)
- ✅ Test coverage > 85%
- ✅ Migración Claude→OpenCode funcional
- ✅ ADWs detectan provider automáticamente
- ✅ TAC-12 features funcionan en ambos
- ✅ Validation tool con 0 false positives
- ✅ Documentation completa

### Version 0.8.1 (DX Improvements):
- ✅ Migration tool con <1% data loss
- ✅ Provider abstraction con 100% test coverage
- ✅ Feature matrix documentation
- ✅ Zero breaking changes para proyectos existentes

### Version 0.9.0 (Advanced):
- ✅ Hybrid workflows en producción
- ✅ Benchmarking data para 10+ workflows
- ✅ Auto-update con 95%+ success rate
- ✅ 3+ proveedores soportados

---

## BREAKING CHANGES Y MIGRACIÓN

### Breaking Changes en 0.8.0:
**Ninguno** - Backward compatible por diseño.

Proyectos existentes de Claude Code:
- ✅ Siguen funcionando sin cambios
- ✅ `config.yml` puede omitir campo `provider` (usa default)
- ✅ ADWs detectan `.claude/` automáticamente

### Migration Path para Early Adopters:

**Si quieres usar OpenCode:**
```bash
# 1. Upgrade TAC Bootstrap
pip install --upgrade tac-bootstrap

# 2. Migrate proyecto
tac-bootstrap migrate --to opencode

# 3. Validate
tac-bootstrap validate --provider opencode

# 4. Test
python adws/adw_plan_iso.py <issue> --scout
```

**Si quieres quedarte en Claude Code:**
```bash
# No action needed! Todo funciona igual.
```

---

## WORKFLOW METADATA (PROYECTO COMPLETO)

```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_v0_8_0
/version: 0.8.0
/tasks: 24
/priority: HIGH
/risk: MEDIUM
/estimated_hours: 90-110
```
