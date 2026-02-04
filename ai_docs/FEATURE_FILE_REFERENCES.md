# Feature: Auto-Load Files from Issue Body + Comments (Hybrid)

## Overview

El sistema ahora detecta y carga automáticamente archivos referenciados en **AMBOS lugares**:
1. **Issue body** - Descripción inicial del issue
2. **Issue comments** - Comentarios posteriores (más recientes primero)

Los archivos se agregan al contexto del agente durante la planificación.

## Uso

### Detección Automática (Sin Keywords Necesarios)

**NO necesitas keywords especiales** - el sistema detecta automáticamente cualquier mención de archivos .md:

**Ejemplo 1 - En el Issue Body:**
```markdown
### Issue Description

Implementar autenticación OAuth según plan_tasks_Tac_14.md

Seguir la arquitectura definida en ai_docs/auth_architecture.md y usar specs/auth-spec.md como referencia.
```

**Ejemplo 2 - En un Comment:**
```markdown
Actualización:

Ahora usar plan_tasks_Tac_14_v2.md en lugar del anterior.
Ver también specs/new-requirements.md para cambios.
```

**Resultado:** Los archivos se detectan y cargan automáticamente, sin necesidad de poner keywords como "load:", "file:", etc.

### Patrones Detectados Automáticamente

El sistema usa **regex patterns** para detectar referencias a archivos .md:

✅ `plan_tasks_*.md` - Planes de tareas (ej: plan_tasks_Tac_14.md)
✅ `specs/*.md` - Especificaciones (ej: specs/auth-feature.md)
✅ `ai_docs/*.md` - Documentación AI (ej: ai_docs/architecture.md)
✅ `app_docs/*.md` - Documentación de aplicación (ej: app_docs/setup.md)
✅ Cualquier ruta `.md` - Cualquier mención (ej: path/to/file.md)

**Cómo funciona:**
- Escanea issue body + comments buscando estos patrones
- NO requiere keywords como "load:", "file:", "ref:" etc.
- Si mencionas `plan_tasks_Tac_14.md` en cualquier parte, lo detecta
- Automáticamente busca el archivo y lo carga
- Si no existe, advierte pero continúa el workflow

### Ubicaciones de Búsqueda

El sistema busca archivos en múltiples ubicaciones:

1. **Ruta directa**: `plan_tasks_Tac_14.md` → `./plan_tasks_Tac_14.md`
2. **En specs/**: `auth.md` → `./specs/auth.md`
3. **En ai_docs/**: `architecture.md` → `./ai_docs/architecture.md`
4. **En ai_docs/doc/**: `plan_tasks_Tac_14.md` → `./ai_docs/doc/plan_tasks_Tac_14.md` ← **NUEVO**
5. **En app_docs/**: `setup.md` → `./app_docs/setup.md`

## Ejemplos Reales

### Ejemplo 1: Mención Natural (Sin Keywords)

**Issue Body:**
```markdown
Necesito implementar autenticación.

Revisar el plan en plan_tasks_Tac_14.md para detalles.
```

**Comment del usuario (días después):**
```markdown
Actualización: ahora usar specs/oauth-requirements.md
```

**Resultado:**
```
[INFO] Found 1 file reference(s) in body
[INFO] Found 1 file reference(s) in comment #1
[INFO] Total: 2 unique file reference(s) from issue body + comments
[INFO] ✓ Loaded referenced file: plan_tasks_Tac_14.md (12450 chars)
[INFO] ✓ Loaded referenced file: specs/oauth-requirements.md (3200 chars)

📎 Loaded 2 referenced file(s): plan_tasks_Tac_14.md, specs/oauth-requirements.md
```

**Nota:** No se usaron keywords como "load:", "file:", etc. - detección 100% automática.

### Ejemplo 2: Múltiples Formas de Mencionar

Todas estas formas funcionan:

```markdown
# Todas detectadas automáticamente:

Ver plan_tasks_Tac_14.md                          ✓ Detectado
Según descrito en specs/feature.md               ✓ Detectado
Arquitectura: ai_docs/oauth_flow.md              ✓ Detectado
Documentación en app_docs/setup.md               ✓ Detectado
plan_tasks_Tac_14.md tiene los detalles          ✓ Detectado
```

**Resultado:** Todos los archivos se detectan y cargan automáticamente.

### Ejemplo 2: Múltiples Referencias

**Issue Body:**
```markdown
### Task
Implementar autenticación.

**Referencias:**
- Spec: specs/auth-feature.md
- Architecture: ai_docs/oauth_flow.md
- Plan: plan_tasks_Auth_v2.md
```

**Resultado:**
```
📎 Loaded 3 referenced file(s): specs/auth-feature.md, ai_docs/oauth_flow.md, plan_tasks_Auth_v2.md
```

### Ejemplo 3: Archivo No Encontrado

**Issue Body:**
```markdown
Ver plan_tasks_Missing.md para detalles
```

**Log:**
```
✗ Referenced file not found: plan_tasks_Missing.md
```

El workflow continúa normalmente, solo advierte que el archivo no se encontró.

## Formato del Contexto

Los archivos se agregan al final del contexto del agente:

````markdown
## Referenced Files from Issue

### plan_tasks_Tac_14.md
```markdown
# Task Plan: TAC-14

## Objective
Implement OAuth authentication...
```

### specs/auth-spec.md
```markdown
# Authentication Specification
...
```
````

## Workflows Soportados

✅ **adw_plan_iso.py** - Planning phase (implementado)
✅ **adw_sdlc_zte_iso.py** - Zero Touch Execution con detección híbrida (implementado)
🚧 **adw_build_iso.py** - Build phase (próximamente)
🚧 **adw_review_iso.py** - Review phase (próximamente)
🚧 **adw_document_iso.py** - Documentation phase (próximamente)

## Detección Híbrida (adw_sdlc_zte_iso.py)

El workflow ZTE usa un enfoque **híbrido** que combina dos sistemas con prioridades:

### PRIORIDAD 1: Referencias Explícitas
- Usa `extract_file_references_from_issue()` para detectar archivos mencionados en body/comments
- Cualquier archivo .md mencionado explícitamente se carga primero
- Ejemplo: "file: plan_tasks_Tac_14.md" o simplemente "plan_tasks_Tac_14.md"

### PRIORIDAD 2: Detección Automática (Fallback)
- Usa `detect_relevant_docs()` para keywords automáticos
- Solo agrega archivos que NO fueron detectados explícitamente
- Evita duplicados comparando nombres base

### Ejemplo de Flujo Híbrido

**Issue Body:**
```markdown
Implementar feature según plan_tasks_Tac_14.md
```

**Resultado:**
```
📎 Found 1 explicit file reference(s): plan_tasks_Tac_14.md
📚 Auto-detected 8 documentation topic(s): PLAN_TAC_BOOTSTRAP, Tac-13, ...
📚 Total documentation to load: 9 topic(s)
```

**Orden de carga:**
1. `plan_tasks_Tac_14.md` (explícito, alta prioridad)
2. `PLAN_TAC_BOOTSTRAP` (automático, no duplicado)
3. `Tac-13` (automático, no duplicado)
4. ... otros topics automáticos sin duplicar

## Beneficios

1. **No más copy-paste**: No necesitas copiar contenido de archivos al issue
2. **Context automático**: El agente tiene todo el contexto necesario
3. **Menos tokens**: Solo se cargan archivos mencionados explícitamente
4. **Flexible**: Funciona con cualquier estructura de archivos .md

## Implementación Técnica

### Funciones Nuevas

**`extract_file_references_from_issue()`**
- Usa regex para detectar referencias a archivos .md
- Busca archivos en múltiples ubicaciones
- Retorna dict de {path: content}

**`format_file_references_for_context()`**
- Formatea archivos cargados como markdown
- Agrega sección "Referenced Files from Issue"
- Retorna string listo para agregar al contexto

### Ubicación

- **Código**: `adws/adw_modules/workflow_ops.py` (líneas 1561-1655)
- **Uso**: `adws/adw_plan_iso.py` (líneas 500-528)

## Limitaciones

- Solo archivos `.md` (markdown)
- Máximo tamaño de archivo: Sin límite (considera tokens)
- Encoding: UTF-8
- Rutas relativas al working directory (worktree)

## Roadmap

- [ ] Extender a otros workflows (build, review, document)
- [ ] Soporte para otros formatos (.yaml, .json, .txt)
- [ ] Límite de tamaño configurable
- [ ] Cache de archivos cargados
- [ ] Wildcards (`plan_tasks_*.md` carga todos)
