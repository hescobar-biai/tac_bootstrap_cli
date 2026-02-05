# Feature: Implementar Database Schema SQLite (BASE + TEMPLATES)

## Metadata
issue_number: `627`
adw_id: `feature_Tac_14_Task_6`
issue_json: `{"number": 627, "title": "Implementar Database Schema SQLite (BASE + TEMPLATES)", "body": "file: plan_tasks_Tac_14.md\nfile: plan_tasks_Tac_14_v2_SQLITE.md..."}`

## Feature Description
Implementar un schema de base de datos SQLite completo para el sistema orchestrator de TAC Bootstrap. Esta feature crea la infraestructura de persistencia necesaria para tracking de agentes, prompts, logs y estado del sistema, siguiendo el patrón dual-location (BASE funcional + TEMPLATES Jinja2).

El schema debe seguir el enfoque "zero-config" con auto-inicialización, WAL mode para concurrencia, validación dual (DB CHECK constraints + Pydantic), y gestión defensiva de integridad mediante triggers y CASCADE deletes.

## User Story
As a TAC Bootstrap user
I want a zero-config SQLite database that automatically initializes and tracks agent orchestration state
So that I can monitor agent workflows, debug issues, and analyze execution history without manual database setup

## Problem Statement
TAC-14 requiere transformar tac_bootstrap en un sistema Class 3 Orchestrator con estado persistente. Actualmente no existe infraestructura de base de datos, lo que limita:
- No hay tracking de agentes runtime
- No hay persistencia de prompts/ADW executions
- No hay logs estructurados para debugging
- No hay análisis histórico de workflows
- No hay base para integración con FastAPI/WebSockets (fases posteriores)

El cambio de PostgreSQL (TAC-14 v1) a SQLite (TAC-14 v2) reduce barreras de adopción pero mantiene toda la funcionalidad esencial.

## Solution Statement
Crear schema SQLite con 5 tablas core (orchestrator_agents, agents, prompts, agent_logs, system_logs) usando:
- **Auto-inicialización**: Lazy creation al primer acceso con función helper
- **Concurrencia**: WAL mode + aiosqlite para async operations
- **Validación dual**: CHECK constraints en DB + Pydantic models en Python
- **Integridad defensiva**: Triggers para timestamps + CASCADE deletes
- **Migración versioned**: Directorio migrations/ con SQL numerados
- **Template pattern**: Base funcional en `adws/schema/` + template Jinja2 en CLI

Database file location: `adws/schema/orchestrator.db` (gitignored), override via `TAC_ORCHESTRATOR_DB` env var.

## Relevant Files
Archivos necesarios para implementar la feature:

### Existing Files (Context)
- `adws/adw_modules/adw_agent_sdk.py` - Modelos Pydantic existentes que informarán el schema
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Registro de templates
- `.gitignore` - Ya incluye `*.db`, `*.sqlite`, `*.sqlite3` (líneas 37-39, 173-175)

### New Files
**BASE (Functional)**:
- `adws/schema/` - Directorio principal del schema
- `adws/schema/orchestrator.db` - Database file (gitignored, auto-creado)
- `adws/schema/schema_orchestrator.sql` - Schema definition completo
- `adws/schema/migrations/` - Directorio para versioned migrations
- `adws/schema/migrations/001_initial.sql` - Initial schema migration
- `adws/schema/README.md` - Setup instructions y documentación
- `adws/schema/.gitkeep` - Para mantener directorio migrations/ en git

**TEMPLATES (Jinja2)**:
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/migrations/.gitkeep`

## Implementation Plan

### Phase 1: Foundation - Create Directory Structure
Crear directorios y estructura base para el schema SQLite.

**Acciones**:
1. Crear directorio `adws/schema/` en BASE
2. Crear subdirectorio `adws/schema/migrations/`
3. Crear `.gitkeep` en migrations/ para preservar en git
4. Verificar que `.gitignore` ya incluye `*.db` y `*.sqlite` (no modificar)

**Rationale**: Estructura de directorios debe existir antes de crear archivos SQL.

### Phase 2: Core Implementation - SQLite Schema Definition
Crear el schema SQL completo con 5 tablas, constraints, triggers e indexes.

**Acciones**:
1. Crear `adws/schema/schema_orchestrator.sql` con:
   - 5 tablas: orchestrator_agents, agents, prompts, agent_logs, system_logs
   - Tipos SQLite nativos (TEXT para UUIDs, INTEGER, REAL, TEXT)
   - CHECK constraints para enums (status, log_level, log_type)
   - FOREIGN KEY constraints con ON DELETE CASCADE
   - DEFAULT values (datetime('now') para timestamps)
   - Trigger para auto-update de updated_at en orchestrator_agents
2. Agregar 6 strategic indexes:
   - `idx_agents_session` en agents(session_id)
   - `idx_agents_orch` en agents(orchestrator_agent_id)
   - `idx_prompts_agent` en prompts(agent_id)
   - `idx_prompts_status` en prompts(status)
   - `idx_agent_logs_agent` en agent_logs(agent_id)
   - `idx_system_logs_level` en system_logs(log_level)
3. Agregar comentarios SQL documentando cada tabla y campo
4. Crear `adws/schema/migrations/001_initial.sql` (copia del schema completo)

**Rationale**: Schema debe ser completo y auto-documentado. Indexes mejoran performance de queries comunes.

### Phase 3: Integration - Documentation and Templates
Crear documentación, templates Jinja2 y registro en scaffold_service.

**Acciones**:
1. Crear `adws/schema/README.md` con:
   - Overview del schema (5 tablas, propósito)
   - Zero-config auto-initialization explicada
   - Tabla de tipos SQLite vs Python
   - Ubicación default del DB file
   - Override con `TAC_ORCHESTRATOR_DB` env var
   - WAL mode y concurrency notes
   - Migration strategy (versioned SQL files)
   - Future PostgreSQL upgrade path
   - Instrucciones para inspect/debug (sqlite3 CLI)
2. Crear template `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2`
   - Copiar schema_orchestrator.sql completo
   - NO agregar variables Jinja2 (schema es estático)
3. Crear template `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2`
   - Usar variable `{{ config.project.name }}` si aplicable
   - Mantener resto del contenido estático
4. Crear `.gitkeep` en templates: `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/migrations/.gitkeep`
5. Registrar templates en `scaffold_service.py`:
   - Agregar método `_add_schema_files()` en ScaffoldService
   - Agregar llamada en `build_plan()` después de `_add_adw_files()`
   - Renderizar 3 archivos: schema SQL, README, .gitkeep

**Rationale**: Templates permiten que proyectos generados incluyan el schema. README es documentación crítica para usuarios.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create Schema Directory Structure
**Acciones**:
- Crear directorio `adws/schema/` usando Bash mkdir -p
- Crear subdirectorio `adws/schema/migrations/`
- Crear archivo vacío `adws/schema/migrations/.gitkeep` con touch
- Verificar que .gitignore ya incluye patrones *.db (NO modificar)

**Validation**:
```bash
ls -la adws/schema/
ls -la adws/schema/migrations/
```

### Task 2: Create SQLite Schema Definition File
**Acciones**:
- Crear `adws/schema/schema_orchestrator.sql` usando Write tool
- Incluir todas las 5 tablas con comentarios detallados
- Definir CHECK constraints para status, log_level, log_type
- Agregar FOREIGN KEY constraints con ON DELETE CASCADE
- Crear trigger para auto-update de updated_at
- Agregar 6 strategic indexes al final del archivo

**Schema Structure**:
```sql
-- Table 1: orchestrator_agents (agent definitions)
-- Table 2: agents (runtime instances)
-- Table 3: prompts (ADW executions)
-- Table 4: agent_logs (agent lifecycle events)
-- Table 5: system_logs (system-level logging)
-- Trigger: update_orchestrator_agents_updated_at
-- Indexes: 6 indexes for performance
```

**Validation**:
```bash
sqlite3 :memory: < adws/schema/schema_orchestrator.sql
echo $?  # Should be 0 (success)
```

### Task 3: Create Initial Migration File
**Acciones**:
- Copiar `adws/schema/schema_orchestrator.sql` a `adws/schema/migrations/001_initial.sql`
- Agregar header comment con migration metadata:
  ```sql
  -- Migration: 001_initial
  -- Description: Initial schema for orchestrator database
  -- Created: 2026-02-04
  -- TAC Version: 0.8.0
  ```

**Validation**:
```bash
diff adws/schema/schema_orchestrator.sql adws/schema/migrations/001_initial.sql
# Should only differ in header comment
```

### Task 4: Create Schema README Documentation
**Acciones**:
- Crear `adws/schema/README.md` usando Write tool
- Incluir secciones:
  1. Overview (propósito, 5 tablas)
  2. Database Location (default path, env var override)
  3. Auto-Initialization (zero-config explicado)
  4. Schema Tables (tabla markdown con 5 filas)
  5. Data Types (SQLite → Python mapping)
  6. Concurrency (WAL mode, aiosqlite)
  7. Migrations (versioned SQL files)
  8. Inspection (sqlite3 CLI commands)
  9. Future Upgrade (PostgreSQL path)

**Validation**: Read README and verify completeness

### Task 5: Create Jinja2 Templates for CLI
**Acciones**:
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/`
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/migrations/`
- Copiar `schema_orchestrator.sql` → `schema_orchestrator.sql.j2` (sin cambios)
- Copiar `README.md` → `README.md.j2` (sin variables Jinja2 por ahora)
- Crear `.gitkeep` vacío en templates/adws/schema/migrations/

**Validation**:
```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/
# Should show: schema_orchestrator.sql.j2, README.md.j2, migrations/
```

### Task 6: Register Schema Templates in ScaffoldService
**Acciones**:
- Leer `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` completamente
- Agregar método privado `_add_schema_files()` siguiendo patrón de `_add_adw_files()`
- En método `build_plan()`, agregar llamada `self._add_schema_files(plan, config, existing_repo)` después de línea 91
- Implementar `_add_schema_files()` para renderizar 3 templates:
  1. `adws/schema/schema_orchestrator.sql`
  2. `adws/schema/README.md`
  3. `adws/schema/migrations/.gitkeep`
- Seguir patrón existente: crear FileAction con template_path y target_path

**Implementation Pattern**:
```python
def _add_schema_files(
    self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool
) -> None:
    """Add schema files to scaffold plan."""
    # Only if orchestrator enabled (future check, default to True for now)

    # Schema SQL file
    plan.add_action(FileAction(
        action_type="create",
        path=Path("adws/schema/schema_orchestrator.sql"),
        template_path="adws/schema/schema_orchestrator.sql.j2",
        context={"config": config},
    ))

    # README
    plan.add_action(FileAction(
        action_type="create",
        path=Path("adws/schema/README.md"),
        template_path="adws/schema/README.md.j2",
        context={"config": config},
    ))

    # .gitkeep for migrations/
    plan.add_action(FileAction(
        action_type="create",
        path=Path("adws/schema/migrations/.gitkeep"),
        template_path="adws/schema/migrations/.gitkeep",
        context={},
    ))
```

**Validation**: Read modified scaffold_service.py and verify integration

### Task 7: Validation - Run All Tests and Smoke Tests
**Acciones**:
- Ejecutar validation commands en orden (ver sección Validation Commands)
- Verificar que schema SQL es válido con sqlite3
- Verificar que templates existen en ambas ubicaciones
- Verificar que scaffold_service.py compila sin errores
- Generar un proyecto de prueba para verificar que schema se copia correctamente

**Commands**:
```bash
# Validate SQL syntax
sqlite3 :memory: < adws/schema/schema_orchestrator.sql

# Validate BASE files exist
ls -la adws/schema/schema_orchestrator.sql
ls -la adws/schema/README.md
ls -la adws/schema/migrations/001_initial.sql

# Validate TEMPLATE files exist
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/migrations/.gitkeep

# Run validation commands (see below)
```

## Testing Strategy

### Unit Tests
**No unit tests required for this task** - Se agregan en Fase 8 (Task 15) como parte de test suites completos.

Esta tarea crea solo el schema SQL estático. La lógica de database operations (conexión, CRUD) se implementa en Task 8 (adw_database.py) y se testea ahí.

### Edge Cases
1. **Empty database**: Schema debe crear todas las tablas desde cero
2. **Re-run schema**: SQLite debe ignorar `CREATE TABLE IF NOT EXISTS` (no implementado en esta tarea, pero documentado para futura implementación)
3. **Invalid data types**: CHECK constraints deben rechazar valores inválidos
4. **Orphaned records**: CASCADE deletes deben limpiar automáticamente
5. **Concurrent access**: WAL mode debe manejar múltiples lectores (documentado en README)
6. **Migration conflicts**: Versioned migrations previenen conflictos (estructura creada, migraciones futuras)

### Integration Tests
1. **SQL syntax validation**: Ejecutar schema en sqlite3 :memory:
2. **Template rendering**: Verificar que .j2 templates se copian correctamente
3. **ScaffoldService registration**: Verificar que templates se registran en build_plan()
4. **File creation**: Generar proyecto de prueba y verificar archivos

## Acceptance Criteria
- [ ] Directorio `adws/schema/` creado en BASE con migrations/ subdirectorio
- [ ] Archivo `schema_orchestrator.sql` contiene 5 tablas completas con tipos SQLite nativos
- [ ] CHECK constraints definidos para status, log_level, log_type enums
- [ ] FOREIGN KEY constraints con ON DELETE CASCADE en todas las relaciones
- [ ] Trigger `update_orchestrator_agents_updated_at` implementado
- [ ] 6 strategic indexes creados para performance
- [ ] Migration file `001_initial.sql` creado con header comment
- [ ] README.md completo con 9 secciones documentadas
- [ ] Templates .j2 creados en `tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/`
- [ ] Método `_add_schema_files()` agregado a ScaffoldService
- [ ] Templates registrados en `build_plan()` después de ADW files
- [ ] Schema SQL valida sin errores en sqlite3 :memory:
- [ ] .gitignore ya incluye `*.db` patterns (verificado, no modificado)
- [ ] Todos los validation commands pasan exitosamente

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

```bash
# 1. Validate SQL schema syntax
sqlite3 :memory: < adws/schema/schema_orchestrator.sql
echo "SQL schema validation: $?"

# 2. Validate BASE files exist
ls -la adws/schema/schema_orchestrator.sql adws/schema/README.md adws/schema/migrations/001_initial.sql

# 3. Validate TEMPLATE files exist
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/schema_orchestrator.sql.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/schema/README.md.j2

# 4. Validate .gitignore patterns (should already exist)
grep -E "\*\.db|\*\.sqlite" .gitignore

# 5. Run CLI tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# 6. Run linting
cd tac_bootstrap_cli && uv run ruff check .

# 7. Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# 8. Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### SQLite vs PostgreSQL Type Mapping
| PostgreSQL (v1) | SQLite (v2) | Python Type | Notes |
|----------------|-------------|-------------|-------|
| UUID | TEXT | str | Store as string representation |
| TIMESTAMPTZ | TEXT | datetime | ISO 8601 format, use datetime('now') |
| VARCHAR | TEXT | str | SQLite has single TEXT type |
| INTEGER | INTEGER | int | Same in both |
| DECIMAL | REAL | float/Decimal | Use REAL for cost_usd |
| JSONB | TEXT | dict | Store JSON as TEXT |

### Design Decisions
1. **Zero-config auto-init**: Database file se crea automáticamente al primer acceso (implementado en Task 8: adw_database.py, no en esta tarea)
2. **WAL mode**: Se habilita en connection string (implementado en Task 8)
3. **Defensive integrity**: Triggers + CASCADE previenen bugs comunes
4. **Dual validation**: DB constraints + Pydantic (Pydantic models en Task 7)
5. **Future-proof migrations**: Estructura permite easy PostgreSQL upgrade

### Dependencies
- SQLite 3.35+ (built-in en Python 3.10+)
- aiosqlite >=0.19.0 (se agrega en Task 8: adw_database.py)

### Future Enhancements (Not in this task)
- Automatic retention policies (Phase 10, Task 19: utility scripts)
- Query performance monitoring
- Database backup automation
- PostgreSQL migration tooling (pgloader)
- Audit trail for schema changes

### Related Tasks
- **Task 7** (next): Crear orch_database_models.py con Pydantic models mapeando a este schema
- **Task 8** (depends on 7): Crear adw_database.py con CRUD operations y connection pooling
- **Task 15** (testing): Crear test suites incluyendo test_database.py
- **Task 19** (utilities): Crear setup_database.sh script

### Migration from TAC-14 v1 (PostgreSQL)
This schema is simplified from original PostgreSQL version:
- Removed explicit UUID type → TEXT
- Removed TIMESTAMPTZ → TEXT with ISO format
- Removed JSONB → TEXT
- Simplified indexes (6 instead of 8)
- Preserved all 5 core tables
- Preserved referential integrity
- Preserved functional requirements

### Environment Variable
`TAC_ORCHESTRATOR_DB` - Override default database location
- Default: `adws/schema/orchestrator.db`
- Example: `export TAC_ORCHESTRATOR_DB=/tmp/test_orchestrator.db`
- Used by connection helper in Task 8 (adw_database.py)
