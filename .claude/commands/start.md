# Start

Iniciar TAC Bootstrap CLI en modo desarrollo.

## Variables
- PORT: No aplica (CLI, no servidor web)

## Check
Verificar que tac_bootstrap_cli existe:
```bash
ls tac_bootstrap_cli/pyproject.toml
```

## Workflow

### Si tac_bootstrap_cli existe:

1. Verificar dependencias:
   ```bash
   cd tac_bootstrap_cli && uv sync
   ```

2. Mostrar ayuda del CLI:
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap --help
   ```

3. Mostrar versión:
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap version
   ```

### Si tac_bootstrap_cli NO existe:

1. Informar que el CLI aún no ha sido creado
2. Mostrar instrucciones:
   ```
   El CLI de TAC Bootstrap aún no existe.

   Para crearlo, ejecuta TAREA 1.1 del plan:
   1. Lee PLAN_TAC_BOOTSTRAP.md
   2. Busca "TAREA 1.1: Crear estructura base"
   3. Ejecuta el prompt de esa tarea
   ```

## Report
- Estado del CLI (instalado/pendiente)
- Comandos disponibles (si está instalado)
- Próximos pasos
