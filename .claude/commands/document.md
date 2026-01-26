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

### 3. Extraer Keywords IDK
- Analizar los cambios de código y extraer 3-8 palabras clave (Information Dense Keywords - IDK)
- Si existe `canonical_idk.yml`, priorizar keywords de ese archivo
- Complementar términos canónicos con keywords específicas del feature según sea necesario
- Las keywords deben representar conceptos core, patrones, tecnologías o términos de dominio

### 4. Generar Documentación
- Crear archivo en `app_docs/` con nombre: `feature-{adw_id}-{descriptive-name}.md`
- CRITICAL: Crear la documentación usando ruta RELATIVA `app_docs/feature-{adw_id}-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `app_docs/filename.md`, NO `/Users/.../app_docs/filename.md`
- Seguir el formato de documentación abajo incluyendo frontmatter YAML
- Enfocar en:
  - Qué se construyó (basado en git diff)
  - Cómo funciona (implementación técnica)
  - Cómo usarlo (perspectiva de usuario)
  - Configuración o setup requerido
  - Instrucciones de testing con comandos bash ejecutables

### 5. Actualizar Documentación Condicional
- Después de crear el archivo, leer `.claude/commands/conditional_docs.md`
- Agregar entrada para el nuevo archivo con condiciones apropiadas

## Documentation Format

```md
---
doc_type: feature
adw_id: N/A
date: <fecha actual YYYY-MM-DD>
idk:
  - keyword1
  - keyword2
  - keyword3
tags:
  - feature
  - general
related_code:
  - path/to/file1.py
  - path/to/test_file1.py
---

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
<comando ejecutable 1>
```

<Descripción de test adicional si es necesario>

```bash
<comando ejecutable 2>
```

## Notes

<Contexto adicional, limitaciones, o consideraciones futuras>
```

## Report

CRITICAL OUTPUT FORMAT - Debes seguir esto exactamente:

TU OUTPUT FINAL DEBE SER EXACTAMENTE UNA LÍNEA conteniendo solo la ruta RELATIVA como:
```
app_docs/feature-e4dc9574-feature-name.md
```

NO incluyas:
- Ninguna explicación o comentario
- Frases como "Perfecto!", "Creé...", "El archivo de documentación está en..."
- Formato markdown alrededor de la ruta
- Múltiples líneas
- Rutas absolutas (que empiezan con /)

SOLO output la ruta RELATIVA. Esto es parseado por máquina.
