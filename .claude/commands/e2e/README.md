# E2E Tests - Ejemplos para Proyectos Generados

## Nota Importante

Los archivos de test en este directorio son **ejemplos** de cómo estructurar tests E2E para proyectos web que generará TAC Bootstrap CLI.

**NO aplican para el desarrollo del CLI tac-bootstrap en sí.**

## Propósito

Estos archivos sirven como:

1. **Templates de referencia** - Muestran la estructura correcta de un test E2E
2. **Ejemplos de sintaxis** - Demuestran User Story, Test Steps, Success Criteria
3. **Baseline para CLI** - El CLI usará estos patrones para generar tests E2E en proyectos nuevos

## Archivos de Ejemplo

- `test_basic_query.md` - Ejemplo de test básico de funcionalidad
- `test_complex_query.md` - Ejemplo de test con múltiples pasos
- `test_export_functionality.md` - Ejemplo de test de exportación
- `test_sql_injection.md` - Ejemplo de test de seguridad
- `test_disable_input_debounce.md` - Ejemplo de test de UX
- `test_random_query_generator.md` - Ejemplo de test generativo

## Para Desarrollo de TAC Bootstrap CLI

Cuando trabajes en el CLI mismo:

- Usar `/test` para ejecutar tests unitarios de Python
- Los tests del CLI están en `tac_bootstrap_cli/tests/`
- No hay UI web en el CLI, por lo tanto no hay E2E tests

## Para Proyectos Generados por el CLI

Cuando el CLI genere un proyecto con UI web:

- Crear tests E2E en `.claude/commands/e2e/`
- Seguir la estructura de estos ejemplos
- Ejecutar con `/test_e2e <path-to-test-file>`
