# Chore: Crear templates .gitkeep para directorios agents

## Metadata
issue_number: `313`
adw_id: `chore_Tac_10_task_7`
issue_json: `{"number":313,"title":"Crear templates .gitkeep para directorios agents","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_10_task_7\n\n- **Descripción**: Crear templates .gitkeep para los nuevos directorios de agents que se crearán durante el scaffold.\n- **Archivos**:\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2`\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/hook_logs/.gitkeep`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/context_bundles/.gitkeep`\n- **Nota**: Crear archivos en ambas ubicaciones\n\n\n"}`

## Chore Description
Crear archivos .gitkeep tanto en templates Jinja2 (para generación durante scaffold) como en los directorios agents del repositorio tac_bootstrap. Los archivos .gitkeep permiten que Git rastree directorios vacíos, lo cual es esencial para mantener la estructura de directorios de `agents/hook_logs/` y `agents/context_bundles/` tanto en proyectos generados como en el propio tac_bootstrap.

## Relevant Files
Archivos y directorios relevantes para completar la chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/structure/` - Directorio de templates Jinja2 para scaffold
  - Actualmente contiene: `ai_docs/`, `app_docs/`, `specs/`, `constitution.md.j2`
  - Necesita agregar: `agents/hook_logs/.gitkeep.j2` y `agents/context_bundles/.gitkeep.j2`

- `agents/` - Directorio en la raíz del proyecto tac_bootstrap
  - Actualmente existe: `agents/context_bundles/.gitkeep`
  - Necesita crear: `agents/hook_logs/` y su `.gitkeep`

### New Files
Los siguientes archivos nuevos deben crearse:

1. **Templates Jinja2 (vacíos):**
   - `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2`
   - `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2`

2. **Archivos directos en tac_bootstrap (vacíos):**
   - `agents/hook_logs/.gitkeep`

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear estructura de directorios en templates
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/`
- Crear subdirectorio `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/`
- Crear subdirectorio `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/`

### Task 2: Crear archivos .gitkeep.j2 en templates
- Crear archivo vacío `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2`
- Crear archivo vacío `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2`
- Estos archivos deben estar completamente vacíos (sin contenido Jinja2)

### Task 3: Crear estructura de directorios en tac_bootstrap root
- Crear directorio `agents/hook_logs/` (si no existe)
- El directorio `agents/context_bundles/` ya existe

### Task 4: Crear archivos .gitkeep en tac_bootstrap root
- Crear archivo vacío `agents/hook_logs/.gitkeep`
- El archivo `agents/context_bundles/.gitkeep` ya existe

### Task 5: Validación
- Ejecutar Validation Commands para asegurar cero regresiones
- Verificar que todos los archivos fueron creados correctamente

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `find tac_bootstrap_cli/tac_bootstrap/templates/structure/agents -name '.gitkeep.j2'` - Verificar templates creados
- `find agents -name '.gitkeep'` - Verificar archivos directos creados

## Notes
- Los archivos .gitkeep son convencionalmente vacíos - su única función es permitir que Git rastree directorios vacíos
- No se requiere registro manual en configuración - los archivos .j2 en `templates/structure/` son descubiertos automáticamente durante el proceso de scaffold
- Esta chore sigue el patrón establecido donde tac_bootstrap usa la misma estructura que genera para otros proyectos
- Auto-Resolved Clarifications confirmaron que no se necesitan variables Jinja2, tests dedicados, ni cambios de configuración
