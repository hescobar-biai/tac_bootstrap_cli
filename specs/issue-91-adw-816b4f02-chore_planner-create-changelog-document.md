# Chore: Create CHANGELOG.md Document

## Metadata
issue_number: `91`
adw_id: `816b4f02`
issue_json: `{"number":91,"title":"TAREA 9: Actualizar proyectos existentes (v0.1.0 → v0.2.0)","body":"**Archivo**: `CHANGELOG.md` (crear si no existe)\n\n**Descripción**: Documentar cambios entre versiones para usuarios.\n\n**Contenido**:\n\n```markdown\n# Changelog\n\n## [0.2.0] - 2025-XX-XX\n\n### Added\n- `tac-bootstrap upgrade` command for updating existing projects\n- Version tracking in `config.yml`\n- `target_branch` configuration in `config.yml`\n- `--version` flag for CLI\n\n### Changed\n- All ADW templates synchronized with latest modules\n- Improved worktree port management\n- Enhanced agent retry logic with rate limiting\n\n### Fixed\n- Jinja2 template escaping for JSON examples\n- Template synchronization issues\n\n### Upgrade Notes\nProjects created with v0.1.0 can upgrade using:\n```bash\ntac-bootstrap upgrade\n```\n\nThis will update adws/, .claude/, and scripts/ while preserving your code.\n\n## [0.1.0] - Initial Release\n\n- Initial TAC Bootstrap CLI\n- Project scaffolding for Python and TypeScript\n- ADW workflow templates\n- Claude Code integration\n```\n\n**Criterios de Aceptación**:\n- [ ] CHANGELOG.md creado\n- [ ] Cambios documentados\n- [ ] Instrucciones de upgrade claras\n- [ ] \n🔴 [edge_case] Proyecto con archivos ADW/scripts modificados manualmente:\n\nOVERWRITE - se sobrescriben completamente\nEl backup creado antes del upgrade permite al usuario recuperar sus modificaciones\nNO hay merge strategy - es reemplazo total de adws/, .claude/, scripts/\nEl usuario debe re-aplicar sus cambios manualmente después del upgrade si los necesita\n🔴 [technical_decision] \"Preserving your code\" significa:\n\nPreservar TODO lo que está fuera de adws/, .claude/, scripts/\nsrc/, tests/, archivos de configuración del usuario, etc. = INTOCABLES\nconfig.yml se preserva, solo se actualiza el campo version\nNO hay merge para archivos modificados dentro de los directorios de templates\n🟡 [technical_decision] Detección de versión si config.yml no tiene campo version:\n\nSi config.yml existe pero no tiene version → asumir \"0.1.0\"\nSi config.yml no existe → error: \"Not a TAC Bootstrap project\"\nYa está definido en TAREA 3: config_data.get(\"version\", \"0.1.0\")\n🟡 [missing_info] Breaking changes entre v0.1.0 y v0.2.0:\n\nNO hay breaking changes\nProyectos v0.1.0 siguen funcionando sin upgrade\nEl upgrade es opcional y solo agrega nuevas features/templates\nNo se necesita sección \"### Breaking Changes\"\n🟢 [missing_info] Fecha de release:\n\nMantener 2025-XX-XX como placeholder\nSe actualiza al momento del release real\nNo es bloqueante para crear el archivo\n🟢 [requirements] URL pattern para version comparison:\n\nNO requerido para MVP\nSe puede agregar después si se publica a GitHub\nSuficiente con el formato estándar Keep a Changelog\n🟢 [requirements] Detalle del fix de Jinja2 escaping:\n\nLa descripción actual es suficiente: \"Jinja2 template escaping for JSON examples\"\nNo es necesario más detalle técnico en el CHANGELOG"}`

## Chore Description
Crear el archivo CHANGELOG.md en la raíz del repositorio para documentar los cambios entre versiones del TAC Bootstrap CLI. Este archivo seguirá el formato estándar Keep a Changelog y servirá como referencia para usuarios sobre qué cambios, mejoras y fixes se incluyen en cada versión.

El CHANGELOG debe documentar claramente la transición de v0.1.0 a v0.2.0, enfocándose en:
- Nuevas features agregadas (upgrade command, version tracking, target_branch config)
- Cambios en templates y workflows
- Fixes de templates Jinja2
- Instrucciones claras de upgrade para usuarios

Esta es la TAREA 9 del plan de implementación y marca el cierre del ciclo de upgrade features, completando la documentación necesaria para que usuarios puedan actualizar proyectos existentes de manera segura.

## Relevant Files

- **CHANGELOG.md (nuevo)** - Archivo a crear en la raíz del repositorio que documentará cambios entre versiones
- **tac_bootstrap_cli/tac_bootstrap/__init__.py** - Contiene `__version__ = "0.2.0"` que será la versión actual documentada
- **app_docs/feature-e69c669b-upgrade-command-documentation.md** - Documentación del upgrade command que se referencia en Upgrade Notes
- **README.md** - Puede referenciar el CHANGELOG para detalles de versiones
- **config.yml** - Template que ahora incluye campo version tracking
- **PLAN_TAC_BOOTSTRAP.md** - Plan maestro que define las tareas implementadas (contexto para "Added" section)

## Step by Step Tasks

### Task 1: Crear CHANGELOG.md en raíz del repositorio
- Navegar a la raíz del repositorio (worktree actual: /Volumes/MAc1/Celes/tac_bootstrap/trees/816b4f02)
- Crear archivo CHANGELOG.md nuevo con el contenido especificado en el issue
- Usar el formato exacto provisto en el issue body
- Mantener la fecha como placeholder "2025-XX-XX" (se actualiza en release real)

### Task 2: Verificar contenido del CHANGELOG
- Validar que las secciones de v0.2.0 incluyan:
  - **Added**: upgrade command, version tracking, target_branch config, --version flag
  - **Changed**: ADW templates sync, worktree port management, agent retry logic
  - **Fixed**: Jinja2 escaping, template synchronization
  - **Upgrade Notes**: Instrucciones claras con ejemplo de comando
- Validar que v0.1.0 esté documentada con initial release items
- Confirmar que NO hay sección "Breaking Changes" (no aplica para v0.2.0)

### Task 3: Validar formato Keep a Changelog
- Verificar que el formato siga las convenciones de https://keepachangelog.com:
  - Encabezados con [version] - YYYY-MM-DD
  - Secciones categorizadas (Added, Changed, Fixed, Upgrade Notes)
  - Markdown bien formateado
- Confirmar que las Upgrade Notes sean claras y accionables

### Task 4: Ejecutar Validation Commands
- Correr todos los comandos de validación para asegurar cero regresiones
- Validar que el CHANGELOG es válido markdown
- Confirmar que el archivo está en el lugar correcto (raíz del repositorio)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --version` - Smoke test (debe mostrar 0.2.0)
- `cat CHANGELOG.md` - Verificar que el archivo existe y tiene contenido correcto

## Notes

**Clarificaciones del Issue (🔴🟡🟢 analysis)**:

1. **OVERWRITE strategy**: El upgrade sobrescribe completamente adws/, .claude/, scripts/. El backup permite recuperar modificaciones manuales, pero el usuario debe re-aplicarlas.

2. **"Preserving your code"**: Se preserva TODO fuera de adws/, .claude/, scripts/ (src/, tests/, config.yml, etc.). Solo se actualiza campo version en config.yml.

3. **Version detection fallback**: Si config.yml no tiene campo version, asumir "0.1.0". Si config.yml no existe, error: "Not a TAC Bootstrap project".

4. **No breaking changes**: v0.1.0 proyectos siguen funcionando sin upgrade. El upgrade es opcional y solo agrega features/templates nuevos.

5. **Release date placeholder**: Mantener "2025-XX-XX" - se actualiza en release real.

6. **No URL pattern needed**: No requerido para MVP. Suficiente con formato Keep a Changelog estándar.

7. **Jinja2 escaping detail**: Descripción actual es suficiente. No se necesita más detalle técnico en CHANGELOG.

**Importante**: Este archivo es principalmente documentación y no requiere tests unitarios. La validación consiste en verificar que el archivo existe, tiene el formato correcto, y contiene la información precisa sobre los cambios de versión.
