# Feature Planning Template

Template para planificar nuevas funcionalidades.

## Variables
- $FEATURE_NAME: Nombre de la feature
- $DESCRIPTION: Descripcion detallada
- $ACCEPTANCE_CRITERIA: Criterios de aceptacion

## Instructions

1. **Entender el Requerimiento**
   - Leer descripcion completa
   - Identificar criterios de aceptacion
   - Listar ambiguedades a clarificar

2. **Investigar el Codebase**
   - Encontrar codigo relacionado existente
   - Identificar patrones a seguir
   - Mapear dependencias

3. **Disenar la Solucion**
   - Dividir en tareas discretas
   - Identificar dependencias entre tareas
   - Considerar edge cases

4. **Crear el Plan**
   - Escribir plan en `specs/feature-{name}.md`
   - Incluir todos los pasos
   - Definir tests

## Output Format

```markdown
# Feature: $FEATURE_NAME

## Summary
[Descripcion breve]

## User Stories
- Como [rol], quiero [accion], para [beneficio]

## Technical Design
[Descripcion tecnica de la solucion]

## Files to Modify
- `path/to/file` - [cambios]

## Implementation Steps
1. [ ] Paso 1
2. [ ] Paso 2

## Test Cases
- [ ] Test 1
- [ ] Test 2

## Definition of Done
- [ ] Feature completa
- [ ] Tests pasan
- [ ] Documentacion actualizada
```
