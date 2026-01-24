# Feature: Registrar metadata en scaffold

## Metadata
issue_number: `156`
adw_id: `feature_3_2`
issue_json: `{"number":156,"title":"Tarea 3.2: Registrar metadata en scaffold","body":"/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_3_2\n\n*Tipo**: feature\n**Ganancia**: Cada vez que se genera o actualiza un proyecto, se registra automáticamente cuándo y con qué versión se hizo.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n2. En `apply_plan()`, antes de escribir config.yml:\n   ```python\n   from datetime import datetime, timezone\n   from tac_bootstrap import __version__\n\n   config.bootstrap = BootstrapMetadata(\n       generated_at=datetime.now(timezone.utc).isoformat(),\n       generated_by=f\"tac-bootstrap v{__version__}\",\n       schema_version=2,\n   )\n   ```\n3. Modificar `templates/config/config.yml.j2` para incluir:\n   ```yaml\n   bootstrap:\n     generated_at: \"{{ config.bootstrap.generated_at }}\"\n     generated_by: \"{{ config.bootstrap.generated_by }}\"\n     schema_version: {{ config.bootstrap.schema_version }}\n   {% if config.bootstrap.last_upgrade %}\n     last_upgrade: \"{{ config.bootstrap.last_upgrade }}\"\n   {% endif %}\n   ```\n\n**Criterios de aceptacion**:\n- `tac-bootstrap init` genera config.yml con seccion bootstrap\n- Timestamps son UTC ISO8601\n- `tac-bootstrap upgrade` actualiza last_upgrade\n\n# FASE 3: Audit Trail y Metadata\n\n**Objetivo**: Registrar metadata de generacion en config.yml para trazabilidad.\n\n**Ganancia de la fase**: Saber exactamente cuando se genero el proyecto, con que version del CLI, y cuando fue la ultima actualizacion. Util para upgrades y debugging.\n\n"}`

## Feature Description
Esta feature agrega metadata de generación y audit trail al archivo config.yml de proyectos generados por TAC Bootstrap CLI. Registra automáticamente:
- Timestamp UTC de cuándo se generó el proyecto
- Versión del CLI que lo generó
- Schema version del config (para futuras migraciones)
- Timestamp de última actualización (para comando upgrade)

Esto proporciona trazabilidad completa para debugging, upgrades automáticos y auditoría de proyectos.

## User Story
As a TAC Bootstrap user
I want to know when my project was generated and with which version of the CLI
So that I can debug issues, understand version compatibility, and safely upgrade my project configuration

## Problem Statement
Actualmente no hay forma de saber:
- Cuándo fue generado un proyecto
- Qué versión del CLI lo generó
- Cuándo fue la última actualización del proyecto
- Qué schema version tiene el config (para migrations futuras)

Esta falta de metadata dificulta:
- Debugging de problemas de configuración
- Implementación del comando upgrade (necesita saber versión actual)
- Auditoría de proyectos en equipo
- Detección de proyectos obsoletos

## Solution Statement
Agregar un modelo Pydantic `BootstrapMetadata` en `domain/models.py` con campos para metadata de generación. En `scaffold_service.py`, poblar automáticamente esta metadata antes de renderizar config.yml. Actualizar el template config.yml.j2 para incluir la sección bootstrap con todos los campos de metadata.

Esta solución es:
- Automática: no requiere input del usuario
- Backward compatible: campos opcionales en TACConfig
- Future-proof: schema_version permite migraciones futuras
- Auditable: timestamps UTC ISO8601 estándar

## Relevant Files
Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Agregar modelo BootstrapMetadata y campo bootstrap en TACConfig
- **tac_bootstrap_cli/tac_bootstrap/__init__.py** - Ya existe con __version__ = "0.2.2"
- **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py** - Modificar apply_plan() para poblar metadata
- **tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2** - Agregar sección bootstrap al template

### New Files
No se crean archivos nuevos. Solo modificaciones a archivos existentes.

## Implementation Plan

### Phase 1: Foundation
Crear el modelo de dominio BootstrapMetadata y agregar el campo bootstrap a TACConfig. Esto establece la base de datos para la metadata.

### Phase 2: Core Implementation
Modificar scaffold_service.py para poblar automáticamente la metadata antes de renderizar config.yml. Agregar try/except para fallback graceful si __version__ no está disponible.

### Phase 3: Integration
Actualizar el template config.yml.j2 para renderizar la sección bootstrap. Verificar que la metadata se genera correctamente en tac-bootstrap init.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear modelo BootstrapMetadata en domain/models.py
- Abrir tac_bootstrap_cli/tac_bootstrap/domain/models.py
- Agregar clase BootstrapMetadata como Pydantic BaseModel:
  - Campo generated_at: str (ISO8601 timestamp)
  - Campo generated_by: str (e.g., "tac-bootstrap v0.2.2")
  - Campo schema_version: int = Field(default=2) (hardcoded a 2 por ahora)
  - Campo last_upgrade: Optional[str] = None (para futuro upgrade command)
- Agregar docstring explicando el propósito de cada campo
- Agregar comentario en schema_version indicando que versioning strategy TBD

### Task 2: Agregar campo bootstrap a TACConfig
- En tac_bootstrap_cli/tac_bootstrap/domain/models.py
- En clase TACConfig, agregar campo:
  - bootstrap: Optional[BootstrapMetadata] = None
- Agregar descripción: "Bootstrap metadata for generation audit trail"

### Task 3: Modificar scaffold_service.py para poblar metadata
- Abrir tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
- En método apply_plan(), ANTES de renderizar config.yml (línea ~580-620):
  - Importar: from datetime import datetime, timezone
  - Importar: from tac_bootstrap import __version__
  - Agregar try/except para importar __version__ con fallback a "unknown"
  - Crear BootstrapMetadata con:
    - generated_at = datetime.now(timezone.utc).isoformat()
    - generated_by = f"tac-bootstrap v{__version__}"
    - schema_version = 2
    - last_upgrade = None (no se setea en generación inicial)
  - Asignar a config.bootstrap = metadata_object
- Agregar comentario explicando que metadata se registra antes de rendering

### Task 4: Actualizar template config.yml.j2
- Abrir tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2
- Al final del archivo (después de sección bootstrap de opciones), agregar:
  ```yaml
  # TAC Bootstrap Metadata (auto-generated)
  {% if config.bootstrap %}
  metadata:
    generated_at: "{{ config.bootstrap.generated_at }}"
    generated_by: "{{ config.bootstrap.generated_by }}"
    schema_version: {{ config.bootstrap.schema_version }}
  {% if config.bootstrap.last_upgrade %}
    last_upgrade: "{{ config.bootstrap.last_upgrade }}"
  {% endif %}
  {% endif %}
  ```
- Usar conditional rendering {% if config.bootstrap %} para backward compatibility

### Task 5: Verificar sintaxis y imports
- Ejecutar: cd tac_bootstrap_cli && uv run ruff check .
- Ejecutar: cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
- Corregir cualquier error de linting o type checking

### Task 6: Test manual con tac-bootstrap init
- Ejecutar: cd tac_bootstrap_cli && uv run tac-bootstrap init --help
- Crear proyecto de prueba en /tmp:
  - uv run tac-bootstrap init /tmp/test-metadata --project-name test --language python --package-manager uv --interactive=false
- Verificar que config.yml contiene sección metadata con:
  - generated_at (timestamp UTC ISO8601)
  - generated_by (e.g., "tac-bootstrap v0.2.2")
  - schema_version: 2
  - NO debe tener last_upgrade en init
- Eliminar proyecto de prueba: rm -rf /tmp/test-metadata

### Task 7: Ejecutar Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- Todos los comandos deben completar sin errores

## Testing Strategy

### Unit Tests
Los tests existentes en test_scaffold_service.py deben seguir pasando. Agregar assertion para verificar que config.bootstrap está presente después de apply_plan().

**Opcional**: Si hay tiempo, agregar test específico:
```python
def test_apply_plan_sets_bootstrap_metadata(tmp_path):
    # Arrange
    config = create_test_config()
    plan = ScaffoldPlan()
    plan.add_file("config.yml", template="config/config.yml.j2", ...)
    service = ScaffoldService()

    # Act
    result = service.apply_plan(plan, tmp_path, config)

    # Assert
    assert config.bootstrap is not None
    assert config.bootstrap.generated_at  # timestamp exists
    assert config.bootstrap.generated_by.startswith("tac-bootstrap v")
    assert config.bootstrap.schema_version == 2
    assert config.bootstrap.last_upgrade is None
```

### Edge Cases
- __version__ import failure → fallback a "unknown"
- config.bootstrap = None → template no renderiza sección (backward compatibility)
- Timestamp validation → debe ser UTC ISO8601 format

## Acceptance Criteria
- `tac-bootstrap init` genera config.yml con sección metadata
- metadata.generated_at es timestamp UTC en formato ISO8601
- metadata.generated_by contiene versión del CLI (e.g., "tac-bootstrap v0.2.2")
- metadata.schema_version es 2
- metadata.last_upgrade NO está presente en init (solo en upgrade futuro)
- Si __version__ no se puede importar, usa "unknown" sin fallar
- Template usa conditional rendering {% if config.bootstrap %} para backward compatibility
- Tests unitarios pasan sin regresiones
- Linting y type checking pasan sin errores

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Esta feature es foundational para el comando `tac-bootstrap upgrade` (FASE 4)
- schema_version=2 es hardcoded por ahora. Versioning strategy TBD en future work.
- last_upgrade field es placeholder para upgrade command. No se usa en esta tarea.
- Usar datetime.now(timezone.utc).isoformat() para timestamps consistentes UTC ISO8601
- Fallback a "unknown" si __version__ no disponible previene failures en scaffolding
- La metadata se llama "metadata" en el YAML (no "bootstrap") para evitar confusión con el campo "bootstrap" existente de opciones
