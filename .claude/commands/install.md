# Install & Prime

Instalar dependencias y preparar el entorno de desarrollo para TAC Bootstrap CLI.

## Read
- README.md
- CLAUDE.md
- PLAN_TAC_BOOTSTRAP.md (secciones relevantes)
- config.yml

## Check Structure
Verificar que existe la estructura del CLI:
```
tac_bootstrap_cli/
├── pyproject.toml
├── tac_bootstrap/
│   ├── __init__.py
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interfaces/
└── tests/
```

Si no existe, informar al usuario que debe ejecutar TAREA 1.1 del plan.

## Run (si tac_bootstrap_cli existe)
1. Instalar dependencias del CLI:
   ```bash
   cd tac_bootstrap_cli && uv sync
   ```

2. Verificar instalación:
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap --help
   ```

## Run (si tac_bootstrap_cli NO existe)
1. Informar que el CLI aún no ha sido creado
2. Sugerir ejecutar TAREA 1.1 del PLAN_TAC_BOOTSTRAP.md

## Read and Execute
.claude/commands/prime.md

## Report
- Estado de la instalación (exitosa/pendiente)
- Versión del CLI instalada (si aplica)
- Próximos pasos según el plan
- Comandos disponibles:
  - `/prime` - Preparar contexto
  - `/feature` - Planificar feature
  - `/implement <plan>` - Ejecutar plan
  - `/test` - Correr tests
