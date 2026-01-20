# Plan Template

Template para generar planes de implementacion.

## Variables
- $TITLE: Titulo del plan
- $DESCRIPTION: Descripcion del trabajo
- $TYPE: feature | bug | chore

## Plan Format

```markdown
# $TYPE: $TITLE

## Summary
[1-2 sentence description]

## Context
[Background and motivation]

## Files to Modify
- `path/to/file.py` - [what changes]
- `path/to/new_file.py` - [create new]

## Implementation Steps
1. [ ] Step one
2. [ ] Step two
3. [ ] Step three

## Test Cases
- [ ] Test case 1
- [ ] Test case 2

## Definition of Done
- [ ] All tasks completed
- [ ] Tests pass
- [ ] Lint passes
- [ ] Code reviewed
```

## Instructions

1. Analizar el contexto proporcionado
2. Identificar archivos a modificar
3. Dividir en pasos atomicos
4. Definir tests necesarios
5. Establecer criterios de completitud
