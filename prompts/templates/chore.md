# Chore Planning Template

Template para planificar tareas de mantenimiento.

## Variables
- $CHORE_TITLE: Titulo de la tarea
- $DESCRIPTION: Descripcion del trabajo

## Instructions

1. **Entender la Tarea**
   - Leer descripcion de la tarea
   - Identificar alcance y limites
   - Determinar criterios de exito

2. **Planificar el Trabajo**
   - Listar todos los cambios necesarios
   - Identificar riesgos o breaking changes
   - Planificar pasos de verificacion

3. **Crear el Plan**
   - Escribir plan en `specs/chore-{name}.md`

## Output Format

```markdown
# Chore: $CHORE_TITLE

## Description
[Que necesita hacerse]

## Motivation
[Por que es necesario]

## Changes
- [ ] Cambio 1
- [ ] Cambio 2

## Files to Modify
- `path/to/file` - [cambios]

## Verification
- [ ] Tests pasan
- [ ] Build exitoso
- [ ] No breaking changes

## Definition of Done
- [ ] Todos los cambios completos
- [ ] Verificado funcionando
```
