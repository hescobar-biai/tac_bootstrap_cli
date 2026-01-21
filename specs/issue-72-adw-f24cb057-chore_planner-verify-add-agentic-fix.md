# Chore: Verificar el fix del comando add-agentic manualmente

## Metadata
issue_number: `72`
adw_id: `f24cb057`
issue_json: `{"number":72,"title":"Tarea 2: Verificar el fix manualmente","body":"### Descripción\nProbar que el comando `add-agentic` ahora genera todos los templates correctamente.\n\n### Prompt\n\n```\nVerifica que el fix del comando add-agentic funciona correctamente.\n\n**Pasos de verificación**:\n\n1. Ir a un proyecto de prueba existente:\n   ```bash\n   cd ~/Documents/Celes/dbt-models\n   ```\n\n2. Limpiar archivos generados anteriormente (si existen):\n   ```bash\n   rm -rf .claude adws scripts config.yml constitution.md CLAUDE.md\n   ```\n\n3. Ejecutar el comando:\n   ```bash\n   uv run tac-bootstrap add-agentic\n   ```\n\n4. Verificar que se crearon los archivos:\n   ```bash\n   ls -la .claude/commands/    # Debe tener 25+ archivos .md\n   ls -la .claude/hooks/       # Debe tener 6+ archivos .py\n   ls -la adws/                # Debe tener 14+ workflows\n   ls -la adws/adw_modules/    # Debe tener módulos\n   ls scripts/                 # Debe tener scripts\n   cat config.yml              # Debe existir con configuración\n   ```\n\n5. Re-ejecutar para verificar idempotencia:\n   ```bash\n   tac-bootstrap add-agentic\n   ```\n   - Debería mostrar \"Files Skipped: X\" para archivos existentes\n   - NO debe sobrescribir archivos del usuario\n\n**Resultado esperado**:\n- Antes del fix: \"Files Created: 1\"\n- Después del fix: \"Files Created: 45+\""}`

## Chore Description
Este chore verifica que el fix del issue #70 funciona correctamente. El problema original era que el comando `add-agentic` solo creaba 1 archivo en lugar de los 45+ archivos esperados (comandos, hooks, workflows, scripts, etc.).

El objetivo es validar manualmente que:
1. Todos los templates se generan correctamente
2. La idempotencia funciona (no sobrescribe archivos existentes)
3. El contador de archivos creados es preciso

## Relevant Files
Archivos relevantes para esta verificación:

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Comando `add-agentic`
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Lógica de generación de archivos
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - Modelos de plan de scaffolding
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Repositorio de templates
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` - Operaciones de filesystem

### New Files
No se requieren archivos nuevos, solo verificación manual.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Preparar directorio de prueba
- Navegar al directorio de prueba: `cd ~/Documents/Celes/dbt-models`
- Verificar que el directorio existe y es accesible
- Crear un respaldo si hay archivos previos importantes

### Task 2: Limpiar archivos generados previamente
- Eliminar archivos TAC existentes: `rm -rf .claude adws scripts config.yml constitution.md CLAUDE.md`
- Verificar que se eliminaron correctamente con `ls -la`

### Task 3: Ejecutar el comando add-agentic
- Ejecutar desde la raíz del proyecto TAC Bootstrap: `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/f24cb057/tac_bootstrap_cli`
- Ejecutar el comando en el directorio de prueba: `uv run tac-bootstrap add-agentic --target-dir ~/Documents/Celes/dbt-models`
- Capturar el output del comando, especialmente el contador de archivos creados

### Task 4: Verificar archivos generados - Claude Commands
- Listar archivos en `.claude/commands/`: `ls -la ~/Documents/Celes/dbt-models/.claude/commands/`
- Contar archivos: `ls ~/Documents/Celes/dbt-models/.claude/commands/ | wc -l`
- Verificar que hay 25+ archivos .md

### Task 5: Verificar archivos generados - Claude Hooks
- Listar archivos en `.claude/hooks/`: `ls -la ~/Documents/Celes/dbt-models/.claude/hooks/`
- Contar archivos: `find ~/Documents/Celes/dbt-models/.claude/hooks/ -type f -name "*.py" | wc -l`
- Verificar que hay 6+ archivos .py

### Task 6: Verificar archivos generados - ADW Workflows
- Listar archivos en `adws/`: `ls -la ~/Documents/Celes/dbt-models/adws/`
- Contar workflows: `ls ~/Documents/Celes/dbt-models/adws/adw_*.py | wc -l`
- Verificar que hay 14+ workflows
- Verificar que existe `adws/adw_modules/`: `ls ~/Documents/Celes/dbt-models/adws/adw_modules/`

### Task 7: Verificar archivos generados - Scripts y Config
- Listar scripts: `ls ~/Documents/Celes/dbt-models/scripts/`
- Verificar config: `cat ~/Documents/Celes/dbt-models/config.yml`
- Verificar constitution: `cat ~/Documents/Celes/dbt-models/constitution.md`
- Verificar CLAUDE.md: `cat ~/Documents/Celes/dbt-models/CLAUDE.md`

### Task 8: Verificar total de archivos creados
- Contar total de archivos generados: `find ~/Documents/Celes/dbt-models/.claude ~/Documents/Celes/dbt-models/adws ~/Documents/Celes/dbt-models/scripts -type f | wc -l`
- Verificar que el contador del comando coincide con el total real
- Confirmar que se crearon 45+ archivos

### Task 9: Verificar idempotencia
- Re-ejecutar el mismo comando: `uv run tac-bootstrap add-agentic --target-dir ~/Documents/Celes/dbt-models`
- Capturar output, especialmente "Files Skipped"
- Verificar que NO se sobrescribieron archivos existentes
- Verificar que "Files Created: 0" y "Files Skipped: 45+"

### Task 10: Validar con comandos de validación
- Ejecutar tests unitarios
- Ejecutar linting
- Ejecutar smoke test del CLI

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/f24cb057/tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/f24cb057/tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd /Volumes/MAc1/Celes/tac_bootstrap/trees/f24cb057/tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Resultado Esperado
- **Antes del fix (issue #70)**: "Files Created: 1"
- **Después del fix**: "Files Created: 45+"

### Archivos Críticos a Verificar
1. **Claude Commands** (25+ archivos): start.md, feature.md, implement.md, test.md, etc.
2. **Claude Hooks** (6+ archivos): user_prompt_submit.py, claude_message.py, etc.
3. **ADW Workflows** (14+ archivos): adw_sdlc_iso.py, adw_patch_iso.py, etc.
4. **ADW Modules**: Shared utilities y helpers
5. **Scripts**: Scripts de desarrollo y utilidad
6. **Config Files**: config.yml, constitution.md, CLAUDE.md

### Verificación de Idempotencia
La segunda ejecución debe:
- NO sobrescribir archivos existentes
- Mostrar "Files Skipped: X" con el contador correcto
- Mostrar "Files Created: 0" si no hay archivos nuevos
- NO modificar timestamps de archivos existentes

### Troubleshooting
Si falla la verificación:
- Revisar logs de error del comando
- Verificar permisos de escritura en el directorio
- Revisar la lógica de skip en `scaffold_service.py:_should_skip_file()`
- Verificar que los templates existen en `tac_bootstrap_cli/tac_bootstrap/infrastructure/templates/`
