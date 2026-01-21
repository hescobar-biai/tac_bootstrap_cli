# Chore: Actualizar documentación del CLI

## Metadata
issue_number: `76`
adw_id: `60574393`
issue_json: `{"number":76,"title":"Tarea 4: Actualizar documentación del CLI","body":"### Descripción\nActualizar el README del CLI para documentar correctamente el comportamiento de `add-agentic`.\n\n### Prompt\n\n```\nActualiza la documentación del comando add-agentic en el README del CLI.\n\n**Archivo**: tac_bootstrap_cli/README.md\n\n**Buscar la sección de add-agentic y actualizar para que diga**:\n\n```markdown\n### For Existing Projects\n\n```bash\n# Add Agentic Layer to existing repository\ncd your-existing-project\ntac-bootstrap add-agentic\n\n# This will:\n# - Auto-detect language, framework, package manager\n# - Create .claude/commands/ with 25+ slash commands\n# - Create .claude/hooks/ with automation hooks\n# - Create adws/ with AI Developer Workflows\n# - Create scripts/ with utility scripts\n# - Create config.yml with detected settings\n# - Create constitution.md with project principles\n\n# Safe for existing repos:\n# - Only creates files that don't exist\n# - Never overwrites your existing files\n# - Run multiple times safely (idempotent)\n```\n```\n\n**Criterios de aceptación**:\n- [ ] Documentación explica qué archivos se crean\n- [ ] Documenta que es seguro para repos existentes\n- [ ] Menciona idempotencia"}`

## Chore Description
Actualizar la sección "For Existing Projects" del README del CLI para documentar claramente el comportamiento del comando `add-agentic`, específicamente:
- Qué archivos y directorios se crean
- Que es seguro para repositorios existentes (no sobrescribe archivos)
- Que el comando es idempotente (puede ejecutarse múltiples veces)

## Relevant Files
Archivos para completar la chore:

- `tac_bootstrap_cli/README.md` (líneas 197-220) - Contiene la sección "For Existing Projects" que debe ser actualizada con información más detallada sobre el comportamiento de `add-agentic`

### New Files
No se requieren archivos nuevos para esta chore.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Actualizar sección "For Existing Projects"
- Reemplazar el contenido actual de la sección (líneas 197-220) con la nueva documentación
- Agregar comentarios explicativos después del comando `tac-bootstrap add-agentic` que documenten:
  - Los directorios/archivos que se crean (.claude/commands/, .claude/hooks/, adws/, scripts/, config.yml, constitution.md)
  - Que detecta automáticamente lenguaje, framework y package manager
  - Que es seguro para repos existentes (solo crea archivos que no existen)
  - Que nunca sobrescribe archivos existentes
  - Que se puede ejecutar múltiples veces de forma segura (idempotente)

### Task 2: Verificar formato y consistencia
- Asegurar que el formato markdown sea consistente con el resto del README
- Verificar que los comentarios en bash usen el prefijo `#`
- Mantener las opciones de `add-agentic` existentes en la sección siguiente

### Task 3: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo
- Verificar que no hay regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- El README ya tiene una estructura clara, solo necesitamos enriquecer la sección de `add-agentic`
- Mantener coherencia con el estilo de documentación existente (uso de comentarios bash, formato de código)
- La nueva documentación debe hacer énfasis en la seguridad y no-destructividad del comando
