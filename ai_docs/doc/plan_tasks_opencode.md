# Plan de Implementación: Soporte para OpenCode y Detección Automática de Agente

## OBJECTIVE

Implementar capacidad de detectar y soportar múltiples proveedores de agentes (Claude Code y OpenCode) en TAC Bootstrap, con detección automática basada en configuración o labels de GitHub issues.

---

## ASSUMPTIONS

1. **OpenCode es compatible con el patrón de comandos y agentes similar a Claude Code**
2. **OpenCode usa directorio `.opencode/` en lugar de `.claude/`**
3. **Los comandos de OpenCode pueden diferir en sintaxis o flags**
4. **Los issues de GitHub pueden tener labels para especificar el proveedor: `/claude` o `/opencode`**
5. **El config.yml es la fuente de verdad para el proveedor por defecto del proyecto**
6. **Los comandos de OpenCode usan el CLI `opencode` en lugar de `claude`**

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

## Parallel Execution Groups

| Grupo | Tareas | Cantidad | Dependencia | Descripción |
|-------|---------|-----------|-------------|
| P1 | 1-3 | Ninguna | Actualización de modelos de dominio para soportar proveedores |
| P2 | 4-7 | P1 | Creación de servicios y detección de proveedor |
| P3 | 8-12 | P2 | Actualización de scaffolding y CLI |
| P4 | 13-14 | P3 | Creación de templates para OpenCode |
| P5 | 15 | P4 | Actualización de CLI para soportar parámetro --agentic-provider |
| P6 | 16 | P5 | Creación de plantillas de comandos OpenCode |
| P7 | 17 | P6 | Creación de plantillas de agentes OpenCode |
| P8 | 18 | P7 | Creación de plantillas de hooks OpenCode |
| SEQ | 19 | P8 | CHANGELOG y versión final |

---

## WORKFLOW METADATA

/feature
/adw_sdlc_zte_iso
/adw_id: feature_multi_provider_support_task_2
