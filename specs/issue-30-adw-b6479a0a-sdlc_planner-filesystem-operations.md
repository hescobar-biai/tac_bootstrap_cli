# Feature: Implementar FileSystem Operations Module

## Metadata
issue_number: `30`
adw_id: `b6479a0a`
issue_json: `{"number":30,"title":"TAREA 5.2: Implementar FileSystem operations","body":"# Prompt para Agente\n\n## Contexto\nEl ScaffoldService necesita operaciones de filesystem para crear directorios y archivos.\nEstas operaciones deben ser idempotentes y seguras.\n\n## Objetivo\nImplementar el modulo fs.py con operaciones de filesystem idempotentes.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py`"}`

## Feature Description
Esta feature implementa un módulo completo de operaciones de filesystem (`FileSystem` class) que proporciona métodos seguros, idempotentes y cross-platform para crear, leer, escribir, modificar y eliminar archivos y directorios. El módulo es crítico para el funcionamiento del `ScaffoldService`, que lo utiliza para generar la estructura del proyecto TAC Bootstrap en nuevos proyectos.

El módulo maneja casos edge como directorios faltantes, archivos inexistentes, permisos de ejecución, y operaciones de append idempotentes para evitar duplicación de contenido.

## User Story
As a TAC Bootstrap CLI developer
I want to have a reliable and safe filesystem operations module
So that the ScaffoldService can create project structures without errors, handle existing files gracefully, and ensure all operations are idempotent and cross-platform compatible

## Problem Statement
El `ScaffoldService` necesita realizar operaciones de filesystem para generar la estructura de archivos y directorios de un proyecto TAC Bootstrap. Actualmente, el servicio importa `FileSystem` desde `tac_bootstrap.infrastructure.fs` (línea 330 en scaffold_service.py), pero este módulo aún no existe.

Sin un módulo de filesystem dedicado, tendríamos que:
- Usar directamente `Path.mkdir()`, `Path.write_text()`, etc., duplicando lógica
- Manejar casos edge (directorios faltantes, archivos existentes) en cada lugar
- Reinventar la rueda para operaciones comunes como "append sin duplicar"
- Arriesgarnos a errores de permisos o problemas de cross-platform compatibility

## Solution Statement
Implementar el módulo `tac_bootstrap/infrastructure/fs.py` con la clase `FileSystem` que encapsula todas las operaciones de filesystem necesarias para la generación de scaffolds. La clase proporcionará:

1. **Operaciones idempotentes**: `ensure_directory()` no falla si el directorio existe, `append_file()` no duplica contenido
2. **Auto-creación de directorios padre**: Todas las operaciones de escritura crean automáticamente directorios padre faltantes
3. **Manejo de permisos**: `make_executable()` para scripts generados
4. **Operaciones seguras**: Todas las operaciones manejan casos edge (archivos inexistentes, permisos, etc.)
5. **Cross-platform**: Uso de `pathlib.Path` y `stat` para portabilidad

El módulo seguirá los patrones establecidos por `TemplateRepository` y será utilizado directamente por `ScaffoldService.apply_plan()`.

## Relevant Files
Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py** (línea 330) - Ya importa y usa `FileSystem`, necesita que el módulo exista para funcionar
- **tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py** - Patrón de referencia para módulos de infraestructura (estructura de clase, docstrings, manejo de errores)
- **tac_bootstrap_cli/tac_bootstrap/domain/plan.py** - Define `FileAction` enum que determina cómo se escriben los archivos (CREATE, OVERWRITE, PATCH, SKIP)

### New Files
- **tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py** - Módulo principal a crear con la clase FileSystem

## Implementation Plan

### Phase 1: Foundation
Crear el módulo base con operaciones fundamentales de filesystem:
- Operaciones de directorio: `ensure_directory()`, `dir_exists()`
- Operaciones de lectura: `read_file()`, `file_exists()`
- Operaciones de escritura básica: `write_file()`

### Phase 2: Core Implementation
Implementar operaciones avanzadas y especializadas:
- Append idempotente: `append_file()` con detección de contenido duplicado
- Permisos: `make_executable()` para scripts
- Copia de archivos: `copy_file()`
- Eliminación: `remove_file()`, `remove_directory()`

### Phase 3: Integration
Verificar integración con ScaffoldService:
- Ejecutar tests de integración con ScaffoldService
- Validar que todas las operaciones funcionan end-to-end
- Smoke test del CLI completo

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear archivo fs.py con estructura base y docstrings
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py`
- Agregar module-level docstring explicando el propósito del módulo
- Importar dependencias: `os`, `stat`, `Path`, `Optional` de typing
- Definir clase `FileSystem` con class-level docstring
- Verificar que el archivo se creó correctamente con `ls -la`

### Task 2: Implementar operaciones de directorio
- Implementar método `ensure_directory(path: Path) -> bool` con lógica idempotente
  - Retornar `True` si se creó, `False` si ya existía
  - Usar `mkdir(parents=True, exist_ok=True)` para crear directorios padre
- Implementar método `dir_exists(path: Path) -> bool`
  - Usar `path.is_dir()` para verificar
- Agregar docstrings completos con Args, Returns, y descripción

### Task 3: Implementar operaciones de escritura básica
- Implementar método `write_file(path: Path, content: str, encoding: str = "utf-8") -> None`
  - Crear directorios padre automáticamente con `path.parent.mkdir(parents=True, exist_ok=True)`
  - Escribir contenido con `path.write_text(content, encoding=encoding)`
- Implementar método `file_exists(path: Path) -> bool`
  - Usar `path.is_file()` para verificar
- Agregar docstrings detallados

### Task 4: Implementar operación append idempotente
- Implementar método `append_file(path: Path, content: str, encoding: str = "utf-8", separator: str = "\n\n") -> None`
  - Crear directorios padre si no existen
  - Si archivo existe, leer contenido existente
  - Verificar si `content.strip()` ya está presente en el archivo existente
  - Si ya existe, retornar sin modificar (idempotencia)
  - Si no existe, agregar con separator entre contenido existente y nuevo
  - Si archivo no existe, crear con el contenido
- Agregar docstring con ejemplo de uso

### Task 5: Implementar make_executable
- Implementar método `make_executable(path: Path) -> None`
  - Si archivo no existe, retornar sin error
  - Obtener permisos actuales con `path.stat().st_mode`
  - Agregar permiso de ejecución para user (`stat.S_IXUSR`)
  - Si group tiene lectura, agregar ejecución para group (`stat.S_IXGRP`)
  - Si other tiene lectura, agregar ejecución para other (`stat.S_IXOTH`)
  - Aplicar nuevos permisos con `os.chmod(path, new_mode)`
- Agregar docstring explicando la lógica de permisos

### Task 6: Implementar operaciones de lectura
- Implementar método `read_file(path: Path, encoding: str = "utf-8", default: Optional[str] = None) -> Optional[str]`
  - Si archivo no existe, retornar `default`
  - Si existe, retornar contenido con `path.read_text(encoding=encoding)`
- Agregar docstring con parámetro `default` explicado

### Task 7: Implementar operaciones de copia y eliminación
- Implementar método `copy_file(src: Path, dst: Path) -> None`
  - Crear directorios padre del destino
  - Usar `shutil.copy2(src, dst)` para preservar metadata
  - Importar `shutil` al inicio del archivo
- Implementar método `remove_file(path: Path) -> bool`
  - Retornar `True` si se eliminó, `False` si no existía
  - Usar `path.unlink()` si existe
- Implementar método `remove_directory(path: Path, recursive: bool = False) -> bool`
  - Si `recursive=True`, usar `shutil.rmtree(path)`
  - Si `recursive=False`, usar `path.rmdir()`
  - Retornar `False` si no existía
- Agregar docstrings completos para todos los métodos

### Task 8: Test manual con script inline
- Crear y ejecutar script de prueba Python que:
  - Importa `FileSystem` desde `tac_bootstrap.infrastructure.fs`
  - Usa `tempfile.TemporaryDirectory()` como directorio temporal
  - Prueba `ensure_directory()` con path anidado (a/b/c)
  - Prueba `write_file()` y verifica contenido
  - Prueba `append_file()` dos veces y verifica idempotencia
  - Prueba `make_executable()` y verifica permisos con `os.access(path, os.X_OK)`
  - Imprime resultados de cada operación
- Ejecutar con `uv run python -c "..."` desde tac_bootstrap_cli/
- Verificar que todas las operaciones funcionan correctamente

### Task 9: Verificar integración con ScaffoldService
- Ejecutar script inline que:
  - Importa `ScaffoldService` y `TACConfig`
  - Crea configuración de prueba mínima
  - Llama `build_plan()` para generar plan
  - Llama `apply_plan()` en directorio temporal
  - Verifica que `ApplyResult.success == True`
  - Imprime estadísticas de archivos y directorios creados
- Confirmar que ScaffoldService usa FileSystem sin errores

### Task 10: Ejecutar comandos de validación
- Ejecutar todos los comandos listados en la sección "Validation Commands"
- Verificar que pytest pasa sin regresiones
- Verificar que ruff check no reporta errores de linting
- Verificar que mypy no reporta errores de tipos
- Verificar que el CLI funciona con `--help` (smoke test)

## Testing Strategy

### Unit Tests
El módulo será probado mediante:
1. **Test inline durante desarrollo** (Task 8): Verificar todas las operaciones básicas en un ambiente temporal aislado
2. **Test de integración** (Task 9): Verificar que ScaffoldService usa FileSystem correctamente
3. **Tests existentes de ScaffoldService**: Deberían pasar sin modificación una vez que FileSystem existe

### Edge Cases
Casos edge que el módulo debe manejar:

1. **Directorios faltantes**: Todas las operaciones de escritura deben crear directorios padre automáticamente
2. **Archivos inexistentes**: `read_file()` debe retornar `default` en vez de fallar; `make_executable()` debe retornar silenciosamente
3. **Contenido duplicado**: `append_file()` debe detectar si el contenido ya existe y no duplicarlo
4. **Permisos de ejecución**: `make_executable()` debe preservar permisos existentes y solo agregar ejecución donde corresponda
5. **Operaciones idempotentes**: `ensure_directory()` debe retornar `False` si el directorio ya existe sin error; `append_file()` no debe modificar archivo si contenido ya presente
6. **Cross-platform paths**: Uso de `pathlib.Path` garantiza portabilidad entre Windows/Unix

## Acceptance Criteria

1. ✅ El archivo `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` existe y contiene la clase `FileSystem`
2. ✅ Método `ensure_directory()` es idempotente (no falla si directorio existe, crea directorios padre)
3. ✅ Método `write_file()` crea automáticamente directorios padre antes de escribir
4. ✅ Método `append_file()` no duplica contenido si ya está presente en el archivo
5. ✅ Método `make_executable()` agrega permisos de ejecución correctamente y maneja archivos inexistentes
6. ✅ Todas las operaciones de lectura manejan archivos inexistentes sin error (retornando valores default)
7. ✅ El módulo usa `pathlib.Path` para operaciones cross-platform
8. ✅ `ScaffoldService.apply_plan()` funciona correctamente usando el nuevo módulo `FileSystem`
9. ✅ Script de prueba inline (Task 8) ejecuta sin errores y muestra resultados esperados
10. ✅ Todos los validation commands pasan sin regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- El módulo NO debe incluir operaciones de git - esas van en un módulo separado `git_adapter`
- NO agregar logging complejo - mantener el módulo simple y enfocado
- Todas las operaciones deben usar encoding UTF-8 por defecto para consistencia
- Los métodos que modifican filesystem (write, remove, etc.) no deben retornar valores excepto cuando sea útil (ej: `ensure_directory` retorna bool para indicar si se creó)
- El parámetro `separator` en `append_file()` por defecto es `"\n\n"` (doble salto de línea) para separar secciones de contenido
- La lógica de detección de duplicados en `append_file()` usa `content.strip() in existing` - esto puede generar falsos positivos si el contenido a agregar es substring del existente, pero es suficiente para casos de uso actuales
- `make_executable()` preserva permisos existentes y solo agrega ejecución donde el usuario/grupo/other tiene lectura
- El import de `shutil` debe ir al inicio del archivo junto con otros imports
