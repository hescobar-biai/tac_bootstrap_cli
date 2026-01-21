# Plan: Rama Target Configurable para ADW Workflows

**Fecha**: 2026-01-21
**Prioridad**: Alta
**Issue**: Referencias hardcodeadas a "main" en múltiples archivos ADW

---

## Problema

Múltiples archivos en `adws/` tienen referencias hardcodeadas a "main" como rama target. No todos los proyectos usan `main` (algunos usan `master`, `develop`, `trunk`, etc.).

---

## Archivos Afectados

### En `/adws/` (código real)

| Archivo | Referencias a "main" | Tipo |
|---------|---------------------|------|
| `adw_ship_iso.py` | 15+ | Merge, push, checkout |
| `adw_sdlc_zte_iso.py` | 1 | Warning message |
| `adw_document_iso.py` | 4 | git diff origin/main |
| `adw_modules/worktree_ops.py` | 2 | git worktree add ... origin/main |
| `adw_modules/workflow_ops.py` | 1 | git diff origin/main |
| `adw_modules/git_ops.py` | 2 | Branch validation |
| `README.md` | 8+ | Documentación |

### En `/templates/adws/` (templates Jinja2)

Los mismos archivos pero con extensión `.j2`

---

## Tarea 1: Agregar `target_branch` a config.yml

### Descripción
Agregar campo de configuración para la rama target con default "main".

### Prompt

```
Necesito agregar el campo `target_branch` a la configuración de TAC Bootstrap.

**Archivos a modificar:**

1. `/Volumes/MAc1/Celes/tac_bootstrap/config.yml`
   - Agregar bajo la sección `agentic:`
   ```yaml
   agentic:
     target_branch: main  # Rama destino para merge/push (main, master, develop)
   ```

2. `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`
   - Agregar el campo usando Jinja2:
   ```yaml
   agentic:
     target_branch: {{ config.agentic.target_branch | default('main') }}
   ```

3. `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py`
   - Agregar el campo al modelo de configuración si existe

**Criterios de aceptación:**
- [ ] config.yml tiene el nuevo campo
- [ ] Template genera el campo correctamente
- [ ] Default es "main" si no se especifica
```

---

## Tarea 2: Agregar pregunta al Wizard

### Descripción
El wizard interactivo debe preguntar por la rama target.

### Prompt

```
Necesito agregar una pregunta al wizard de TAC Bootstrap para configurar la rama target.

**Archivo**: `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`

**Buscar**: La sección del wizard donde se hacen las preguntas interactivas

**Agregar pregunta**:
```python
# Después de preguntar por worktrees
target_branch = typer.prompt(
    "Target branch for merge/push",
    default="main",
    show_default=True
)
```

**La pregunta debe:**
- Aparecer después de "Enable git worktrees?"
- Tener "main" como default
- Mostrar el default al usuario
- Guardar el valor en la configuración

**Criterios de aceptación:**
- [ ] Wizard pregunta por target branch
- [ ] Default es "main"
- [ ] Valor se guarda en config generado
```

---

## Tarea 3: Crear función helper para leer target_branch

### Descripción
Crear una función reutilizable que lea la rama target de config.yml.

### Prompt

```
Necesito crear una función helper para leer `target_branch` de config.yml.

**Archivo**: `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_modules/utils.py`

**Agregar función**:
```python
def get_target_branch(config_path: str = "config.yml") -> str:
    """Get target branch from config.yml, default to 'main'.

    Args:
        config_path: Path to config.yml file

    Returns:
        Target branch name (e.g., 'main', 'master', 'develop')
    """
    try:
        import yaml
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config.get("agentic", {}).get("target_branch", "main")
    except Exception:
        return "main"
```

**También agregar al template**:
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/utils.py.j2`

**Criterios de aceptación:**
- [ ] Función existe en utils.py
- [ ] Retorna "main" si no hay config
- [ ] Retorna el valor configurado si existe
```

---

## Tarea 4: Actualizar adw_ship_iso.py

### Descripción
Reemplazar todas las referencias hardcodeadas a "main" con la función helper.

### Prompt

```
Necesito actualizar adw_ship_iso.py para usar target_branch configurable.

**Archivos**:
- `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_ship_iso.py`
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_ship_iso.py.j2`

**Cambios requeridos**:

1. Importar la función helper:
   ```python
   from adw_modules.utils import get_target_branch
   ```

2. Al inicio de main(), obtener la rama:
   ```python
   target_branch = get_target_branch()
   ```

3. Reemplazar TODAS las referencias (15+):
   - Línea 94: `["git", "checkout", "main"]` → `["git", "checkout", target_branch]`
   - Línea 103: `["git", "pull", "origin", "main"]` → `["git", "pull", "origin", target_branch]`
   - Línea 125: `["git", "push", "origin", "main"]` → `["git", "push", "origin", target_branch]`
   - Todos los mensajes de log y comentarios

4. Renombrar función:
   - `manual_merge_to_main()` → `manual_merge_to_target()`

**Criterios de aceptación:**
- [ ] No hay referencias hardcodeadas a "main"
- [ ] Usa get_target_branch() para obtener la rama
- [ ] Todos los logs muestran la rama correcta
- [ ] Template usa {{ config.agentic.target_branch | default('main') }}
```

---

## Tarea 5: Actualizar adw_modules/worktree_ops.py

### Descripción
Los worktrees se crean desde origin/main, debe ser configurable.

### Prompt

```
Necesito actualizar worktree_ops.py para usar target_branch configurable.

**Archivos**:
- `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_modules/worktree_ops.py`
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/worktree_ops.py.j2`

**Cambios en create_worktree()**:

```python
from .utils import get_target_branch

def create_worktree(...):
    target_branch = get_target_branch()

    # Línea 57: Cambiar
    # ANTES: cmd = ["git", "worktree", "add", "-b", branch_name, worktree_path, "origin/main"]
    # DESPUÉS:
    cmd = ["git", "worktree", "add", "-b", branch_name, worktree_path, f"origin/{target_branch}"]
```

**Criterios de aceptación:**
- [ ] Worktrees se crean desde origin/{target_branch}
- [ ] Funciona con main, master, develop, etc.
```

---

## Tarea 6: Actualizar adw_document_iso.py

### Descripción
Los diffs se hacen contra origin/main, debe ser configurable.

### Prompt

```
Necesito actualizar adw_document_iso.py para usar target_branch configurable.

**Archivos**:
- `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_document_iso.py`
- Template correspondiente

**Cambios en has_changes_from_main()**:

```python
from adw_modules.utils import get_target_branch

def has_changes_from_main(...):  # Considerar renombrar a has_changes_from_target()
    target_branch = get_target_branch()

    # Línea 76: Cambiar
    # ANTES: ["git", "diff", "origin/main", "--stat"]
    # DESPUÉS:
    ["git", "diff", f"origin/{target_branch}", "--stat"]
```

**También actualizar mensajes de log** que mencionan "main".

**Criterios de aceptación:**
- [ ] Diffs se hacen contra origin/{target_branch}
- [ ] Logs muestran la rama correcta
```

---

## Tarea 7: Actualizar adw_modules/workflow_ops.py

### Descripción
Hay un diff contra origin/main que debe ser configurable.

### Prompt

```
Actualizar workflow_ops.py para usar target_branch configurable.

**Archivo**: `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`

**Buscar línea 714**:
```python
# ANTES
["git", "diff", "origin/main", "--name-only"]

# DESPUÉS
from .utils import get_target_branch
target_branch = get_target_branch()
["git", "diff", f"origin/{target_branch}", "--name-only"]
```

**Criterios de aceptación:**
- [ ] Diff usa target_branch configurable
```

---

## Tarea 8: Actualizar adw_modules/git_ops.py

### Descripción
Hay validación de branch contra "main" que debe ser configurable.

### Prompt

```
Actualizar git_ops.py para usar target_branch configurable.

**Archivo**: `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_modules/git_ops.py`

**Buscar líneas 258-267**:
```python
# ANTES
if current_branch and current_branch != "main":

# DESPUÉS
from .utils import get_target_branch
target_branch = get_target_branch()
if current_branch and current_branch != target_branch:
```

**Criterios de aceptación:**
- [ ] Validación usa target_branch configurable
```

---

## Tarea 9: Actualizar adw_sdlc_zte_iso.py

### Descripción
Actualizar el mensaje de warning.

### Prompt

```
Actualizar adw_sdlc_zte_iso.py para mostrar la rama target correcta en el warning.

**Archivo**: `/Volumes/MAc1/Celes/tac_bootstrap/adws/adw_sdlc_zte_iso.py`

**Línea 60**:
```python
# ANTES
print("\n⚠️  WARNING: This will automatically merge to main if all phases pass!")

# DESPUÉS
from adw_modules.utils import get_target_branch
target_branch = get_target_branch()
print(f"\n⚠️  WARNING: This will automatically merge to {target_branch} if all phases pass!")
```

**Criterios de aceptación:**
- [ ] Warning muestra la rama target correcta
```

---

## Tarea 10: Actualizar README.md

### Descripción
Actualizar documentación para mencionar que la rama es configurable.

### Prompt

```
Actualizar la documentación en adws/README.md.

**Archivo**: `/Volumes/MAc1/Celes/tac_bootstrap/adws/README.md`

**Agregar sección sobre configuración**:
```markdown
## Configuration

### Target Branch

By default, ADW workflows merge to `main`. To change this:

1. Edit `config.yml`:
   ```yaml
   agentic:
     target_branch: develop  # or master, trunk, etc.
   ```

2. All workflows will now use the configured branch for:
   - Creating worktrees (branching from origin/{target_branch})
   - Comparing changes (git diff origin/{target_branch})
   - Merging (merge to {target_branch})
   - Pushing (push to origin/{target_branch})
```

**También actualizar** referencias específicas a "main" para mencionar que es configurable.

**Criterios de aceptación:**
- [ ] README documenta cómo configurar target_branch
- [ ] Referencias a "main" indican que es configurable
```

---

## Verificación Final

```bash
# 1. Cambiar config.yml
# agentic:
#   target_branch: develop

# 2. Verificar que no hay "main" hardcodeado
grep -r '"main"' adws/*.py adws/adw_modules/*.py | grep -v "def main" | grep -v "__main__"

# 3. Crear worktree (debe usar origin/develop)
uv run adws/adw_plan_iso.py 123

# 4. Ship (debe hacer merge a develop)
uv run adws/adw_ship_iso.py 123 <adw_id>

# 5. Restaurar
# agentic:
#   target_branch: main
```

---

## Resumen de Cambios

| Tipo | Cantidad |
|------|----------|
| Archivos en adws/ | 7 |
| Archivos en templates/adws/ | 7 |
| config.yml | 1 |
| Templates config/ | 1 |
| Wizard (cli.py) | 1 |
| **Total** | **17 archivos** |
