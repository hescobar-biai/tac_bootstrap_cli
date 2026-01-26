# Specifications

Este directorio contiene las especificaciones de issues y features.

## Estructura

```
specs/
├── feature-*.md          # Especificaciones de nuevas features
├── bug-*.md              # Especificaciones de bugs a resolver
├── chore-*.md            # Especificaciones de tareas técnicas
└── issue-*.md            # Especificaciones generales de issues
```

## Tipos de Archivos

- **feature-*.md**: Especificaciones detalladas de nuevas funcionalidades
- **bug-*.md**: Descripción de bugs, pasos para reproducir y criterios de validación
- **chore-*.md**: Tareas técnicas como refactoring, actualización de dependencias, etc.
- **issue-*.md**: Especificaciones generales que pueden combinar varios tipos de trabajo

## Formato

Cada especificación debe incluir:

```markdown
# [Tipo]: [Título]

## Metadata
issue_number: `XX`
adw_id: `xxxxxxxx`

## Description
[Descripción detallada del trabajo a realizar]

## Step by Step Tasks
[Lista numerada de pasos específicos]

## Validation Commands
[Comandos para verificar que el trabajo se completó correctamente]

## Notes
[Notas adicionales, contexto o referencias]
```
