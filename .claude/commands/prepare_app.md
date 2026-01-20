# Prepare Application

Preparar el entorno de desarrollo de TAC Bootstrap CLI para tests o reviews.

## Instructions

### Si tac_bootstrap_cli/ existe:

1. **Sincronizar dependencias**
   ```bash
   cd tac_bootstrap_cli && uv sync
   ```

2. **Verificar CLI funcional**
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap --help
   ```

3. **Ejecutar tests rápidos**
   ```bash
   cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short -x
   ```

### Si tac_bootstrap_cli/ NO existe:

1. **Informar estado**
   - El CLI aún no ha sido creado
   - No es posible preparar el entorno de desarrollo

2. **Sugerir siguiente paso**
   - Ejecutar TAREA 1.1 del PLAN_TAC_BOOTSTRAP.md para crear estructura base

## Notes

- Este comando prepara el entorno para desarrollo del CLI
- Para tests de la app de ejemplo (si existe), usar los scripts en `scripts/`
- Leer `PLAN_TAC_BOOTSTRAP.md` para entender el estado actual del proyecto
