# Plan: Fix `add-agentic` Command - Templates Not Generated

**Fecha**: 2026-01-21
**Prioridad**: Alta
**Issue**: El comando `tac-bootstrap add-agentic` solo crea `config.yml` pero no genera templates

---

## Problema

Cuando se ejecuta `tac-bootstrap add-agentic` en un repositorio existente:
- ✅ Detecta correctamente lenguaje, framework, package manager
- ✅ Crea `config.yml`
- ❌ NO crea `.claude/commands/` (25+ archivos)
- ❌ NO crea `.claude/hooks/` (6+ archivos)
- ❌ NO crea `adws/` (14+ workflows)
- ❌ NO crea `scripts/` (utilidades)

**Causa**: En `scaffold_service.py`, cuando `existing_repo=True`, todos los templates se marcan como `FileAction.SKIP`.

---

## Tarea 1: Corregir lógica de FileAction en scaffold_service.py

### Descripción
Cambiar la lógica que determina la acción de archivos para repositorios existentes. Actualmente usa `SKIP` (nunca crea), debe usar `CREATE` (crea solo si no existe).

### Prompt

```
Necesito corregir un bug en el archivo scaffold_service.py de TAC Bootstrap CLI.

**Archivo**: tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

**Problema**: Cuando `existing_repo=True`, todos los archivos de templates se marcan con `FileAction.SKIP`, lo que significa que nunca se crean.

**Solución**: Cambiar `FileAction.SKIP` por `FileAction.CREATE` en los siguientes métodos:

1. `_add_claude_files()` - línea ~113
2. `_add_adw_files()` - línea ~204
3. `_add_script_files()` - línea ~284
4. `_add_config_files()` - línea ~305
5. `_add_structure_files()` - línea ~343

**Patrón a buscar y reemplazar**:
```python
# ANTES
action = FileAction.CREATE if not existing_repo else FileAction.SKIP

# DESPUÉS
action = FileAction.CREATE  # CREATE = solo crea si no existe (seguro para repos existentes)
```

**Nota**: `FileAction.CREATE` ya tiene la lógica correcta - solo crea archivos que NO existen, no sobrescribe archivos existentes del usuario.

**Criterios de aceptación**:
- [ ] Los 5 métodos usan `FileAction.CREATE` independiente de `existing_repo`
- [ ] El parámetro `existing_repo` puede eliminarse o mantenerse para lógica futura
- [ ] Los tests existentes siguen pasando
```

---

## Tarea 2: Verificar el fix manualmente

### Descripción
Probar que el comando `add-agentic` ahora genera todos los templates correctamente.

### Prompt

```
Verifica que el fix del comando add-agentic funciona correctamente.

**Pasos de verificación**:

1. Ir a un proyecto de prueba existente:
   ```bash
   cd ~/Documents/Celes/dbt-models
   ```

2. Limpiar archivos generados anteriormente (si existen):
   ```bash
   rm -rf .claude adws scripts config.yml constitution.md CLAUDE.md
   ```

3. Ejecutar el comando:
   ```bash
   uv run tac-bootstrap add-agentic
   ```

4. Verificar que se crearon los archivos:
   ```bash
   ls -la .claude/commands/    # Debe tener 25+ archivos .md
   ls -la .claude/hooks/       # Debe tener 6+ archivos .py
   ls -la adws/                # Debe tener 14+ workflows
   ls -la adws/adw_modules/    # Debe tener módulos
   ls scripts/                 # Debe tener scripts
   cat config.yml              # Debe existir con configuración
   ```

5. Re-ejecutar para verificar idempotencia:
   ```bash
   tac-bootstrap add-agentic
   ```
   - Debería mostrar "Files Skipped: X" para archivos existentes
   - NO debe sobrescribir archivos del usuario

**Resultado esperado**:
- Antes del fix: "Files Created: 1"
- Después del fix: "Files Created: 45+"
```

---

## Tarea 3: Actualizar tests unitarios

### Descripción
Verificar y actualizar tests para cubrir el escenario de `add-agentic` en repositorios existentes.

### Prompt

```
Revisa y actualiza los tests del scaffold_service para cubrir el caso de add-agentic en repos existentes.

**Archivo de tests**: tac_bootstrap_cli/tests/test_scaffold_service.py

**Verificar que existe un test para**:
1. `build_plan()` con `existing_repo=True` genera archivos con `FileAction.CREATE`
2. `apply_plan()` crea archivos cuando no existen
3. `apply_plan()` NO sobrescribe archivos existentes (respeta `FileAction.CREATE`)

**Si no existen, crear tests como**:

```python
def test_build_plan_existing_repo_creates_templates():
    """Verify add-agentic creates templates for existing repos."""
    service = ScaffoldService()
    config = create_test_config()

    plan = service.build_plan(config, existing_repo=True)

    # Should have claude files with CREATE action (not SKIP)
    claude_files = [op for op in plan.operations if '.claude/' in str(op.path)]
    assert len(claude_files) > 0
    for op in claude_files:
        assert op.action == FileAction.CREATE, f"{op.path} should be CREATE, not {op.action}"

def test_apply_plan_does_not_overwrite_existing():
    """Verify CREATE action doesn't overwrite existing files."""
    # Setup: create a file that already exists
    # Run apply_plan with CREATE action
    # Verify file was not modified
```

**Ejecutar tests**:
```bash
cd tac_bootstrap_cli
make test
```

**Criterios de aceptación**:
- [ ] Tests cubren el caso de existing_repo=True
- [ ] Tests verifican que CREATE no sobrescribe
- [ ] Todos los tests pasan
```

---

## Tarea 4: Actualizar documentación del CLI

### Descripción
Actualizar el README del CLI para documentar correctamente el comportamiento de `add-agentic`.

### Prompt

```
Actualiza la documentación del comando add-agentic en el README del CLI.

**Archivo**: tac_bootstrap_cli/README.md

**Buscar la sección de add-agentic y actualizar para que diga**:

```markdown
### For Existing Projects

```bash
# Add Agentic Layer to existing repository
cd your-existing-project
tac-bootstrap add-agentic

# This will:
# - Auto-detect language, framework, package manager
# - Create .claude/commands/ with 25+ slash commands
# - Create .claude/hooks/ with automation hooks
# - Create adws/ with AI Developer Workflows
# - Create scripts/ with utility scripts
# - Create config.yml with detected settings
# - Create constitution.md with project principles

# Safe for existing repos:
# - Only creates files that don't exist
# - Never overwrites your existing files
# - Run multiple times safely (idempotent)
```
```

**Criterios de aceptación**:
- [ ] Documentación explica qué archivos se crean
- [ ] Documenta que es seguro para repos existentes
- [ ] Menciona idempotencia
```

---

## Resumen de Archivos a Modificar

| Tarea | Archivo | Tipo de Cambio |
|-------|---------|----------------|
| 1 | `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` | Fix bug |
| 2 | N/A | Verificación manual |
| 3 | `tac_bootstrap_cli/tests/test_scaffold_service.py` | Añadir/actualizar tests |
| 4 | `tac_bootstrap_cli/README.md` | Actualizar documentación |

---

## Verificación Final

```bash
# 1. Correr todos los tests
cd tac_bootstrap_cli && make test

# 2. Probar en proyecto real
cd ~/Documents/Celes/dbt-models
rm -rf .claude adws scripts config.yml
tac-bootstrap add-agentic
ls -la .claude/commands/ | wc -l  # Debe ser > 25

# 3. Verificar idempotencia
tac-bootstrap add-agentic  # No debe sobrescribir
```
