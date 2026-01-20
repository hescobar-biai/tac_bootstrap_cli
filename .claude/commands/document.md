# Document Feature

Generar documentación markdown para features implementadas en TAC Bootstrap CLI analizando cambios de código y especificaciones.

## Variables

adw_id: $1
spec_path: $2 si se proporciona, de lo contrario dejar en blanco
documentation_screenshots_dir: $3 si se proporciona, de lo contrario dejar en blanco

## Instructions

### 1. Analizar Cambios
- Ejecutar `git diff origin/main --stat` para ver archivos cambiados
- Ejecutar `git diff origin/main --name-only` para lista de archivos
- Para cambios significativos (>50 líneas), ejecutar `git diff origin/main <file>`

### 2. Leer Especificación (si se proporciona)
- Si `spec_path` se proporciona, leer para entender:
  - Requerimientos y objetivos originales
  - Funcionalidad esperada
  - Criterios de éxito

### 3. Generar Documentación
- Crear archivo en `app_docs/` con nombre: `feature-{adw_id}-{descriptive-name}.md`
- Seguir el formato de documentación abajo
- Enfocar en:
  - Qué se construyó (basado en git diff)
  - Cómo funciona (implementación técnica)
  - Cómo usarlo (perspectiva de usuario)
  - Configuración o setup requerido

### 4. Actualizar Documentación Condicional
- Después de crear el archivo, leer `.claude/commands/conditional_docs.md`
- Agregar entrada para el nuevo archivo con condiciones apropiadas

## Documentation Format

```md
# <Feature Title>

**ADW ID:** <adw_id>
**Date:** <fecha actual>
**Specification:** <spec_path o "N/A">

## Overview

<2-3 oraciones resumiendo qué se construyó y por qué>

## What Was Built

<Listar componentes/features implementados basado en análisis de git diff>

- <Componente/feature 1>
- <Componente/feature 2>

## Technical Implementation

### Files Modified

<Listar archivos clave cambiados con descripción>

- `tac_bootstrap_cli/tac_bootstrap/<path>`: <qué se cambió/agregó>

### Key Changes

<Describir cambios técnicos más importantes en 3-5 bullet points>

## How to Use

<Instrucciones paso a paso para usar la nueva feature>

1. <Paso 1>
2. <Paso 2>

## Configuration

<Opciones de configuración, variables de entorno, o settings>

## Testing

<Descripción de cómo probar la feature>

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "<test_name>"
```

## Notes

<Contexto adicional, limitaciones, o consideraciones futuras>
```

## Report

- IMPORTANTE: Retornar exclusivamente el path al archivo de documentación creado.
