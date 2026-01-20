# Review Template

Template para revisar implementaciones.

## Variables
- $PLAN_FILE: Ruta al archivo de plan
- $IMPLEMENTATION: Descripcion de lo implementado

## Instructions

1. **Cargar el Plan**
   - Leer el archivo de plan especificado
   - Entender todos los requerimientos
   - Listar criterios de aceptacion

2. **Verificar Completitud**
   - Para cada item del plan:
     - Verificar si esta implementado
     - Verificar si tiene tests
     - Notar desviaciones

3. **Ejecutar Validacion**
   - Correr tests
   - Correr linter
   - Correr build

4. **Revisar Calidad**
   - Codigo sigue patrones del proyecto
   - No hay valores hardcodeados
   - Manejo de errores presente
   - No hay issues de seguridad

5. **Generar Reporte**

## Output Format

```markdown
# Review: [Nombre del Plan]

## Plan File
`$PLAN_FILE`

## Checklist
- [ ] Todas las tareas del plan completadas
- [ ] Tests pasan
- [ ] Lint pasa
- [ ] Build exitoso
- [ ] Calidad de codigo aceptable

## Tasks Verification
| Task | Status | Notes |
|------|--------|-------|
| Task 1 | DONE | |
| Task 2 | DONE | |

## Test Results
- Total: X
- Passed: X
- Failed: X

## Issues Found
- (listar issues encontrados)

## Verdict
- [ ] APPROVED - Listo para merge
- [ ] NEEDS_CHANGES - Requiere cambios

## Recommendations
- (sugerencias de mejora)
```
