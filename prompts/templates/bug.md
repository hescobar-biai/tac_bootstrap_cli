# Bug Planning Template

Template para planificar correccion de bugs.

## Variables
- $BUG_TITLE: Titulo del bug
- $DESCRIPTION: Descripcion del problema
- $REPRODUCTION_STEPS: Pasos para reproducir

## Instructions

1. **Entender el Bug**
   - Leer descripcion del problema
   - Identificar comportamiento esperado vs actual
   - Documentar pasos de reproduccion

2. **Investigar Root Cause**
   - Encontrar codigo relevante
   - Identificar la causa raiz
   - Verificar si hay issues relacionados

3. **Planificar el Fix**
   - Determinar el fix minimo
   - Identificar side effects
   - Planificar tests de regresion

4. **Crear el Plan**
   - Escribir plan en `specs/bug-{name}.md`

## Output Format

```markdown
# Bug: $BUG_TITLE

## Description
[Que esta roto]

## Reproduction Steps
1. Paso 1
2. Paso 2
3. Observar error

## Expected Behavior
[Que deberia pasar]

## Actual Behavior
[Que pasa actualmente]

## Root Cause
[Por que esta roto]

## Fix
[Como arreglarlo]

## Files to Modify
- `path/to/file` - [cambios]

## Test Cases
- [ ] Test que reproduce el bug
- [ ] Test de regresion

## Definition of Done
- [ ] Bug corregido
- [ ] Tests pasan
- [ ] No regresiones
```
