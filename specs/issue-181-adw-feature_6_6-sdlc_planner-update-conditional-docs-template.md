# Feature: Actualizar conditional_docs template con reglas de Documentación Fractal

## Metadata
issue_number: `181`
adw_id: `feature_6_6`
issue_json: `{"number":181,"title":"Tarea 6.6: Actualizar conditional_docs template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_6_6\n\n**Tipo**: feature\n**Ganancia**: Los agentes AI saben cuando consultar la documentacion fractal, cerrando el loop entre generacion y consumo de docs.\n\n**Instrucciones para el agente**:\n\n1. Modificar template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2`\n2. Actualizar renderizado en raiz: `.claude/commands/conditional_docs.md`\n2. Agregar las siguientes reglas condicionales al final del archivo:\n   ```markdown\n   ## Fractal Documentation\n\n   - When working with documentation or understanding code structure:\n     - Read `docs/` directory for fractal documentation of each module\n     - Each file in `docs/` corresponds to a folder in `{{ config.paths.app_root | default(\"src\") }}/`\n\n   - When creating new modules or capabilities:\n     - After implementation, run `/generate_fractal_docs changed` to update documentation\n     - Ensure new modules have IDK docstrings before generating fractal docs\n\n   - When refactoring or moving files:\n     - Run `/generate_fractal_docs full` to regenerate all documentation\n     - Review `docs/` for outdated references\n\n   - When looking for canonical terminology:\n     - Read `canonical_idk.yml` for approved domain keywords\n     - Use these keywords in docstrings and documentation\n   ```\n\n**Criterios de aceptacion**:\n- Reglas agregadas no rompen el formato existente del template\n- Condiciones son claras y actionables\n- Referencias a paths usan variables Jinja2\n\n**Objetivo**: Incluir los generadores de documentacion fractal como parte de los proyectos generados, con slash command para invocacion facil.\n\n**Ganancia de la fase**: Proyectos generados incluyen herramientas de documentacion automatica que mantienen docs sincronizados con el codigo, usando LLM local o remoto.\n\n---\n"}`

## Feature Description
Esta feature agrega reglas condicionales sobre Documentación Fractal al template `conditional_docs.md.j2` y actualiza el archivo renderizado en la raíz del proyecto TAC Bootstrap. El objetivo es guiar a los agentes AI sobre cuándo y cómo utilizar las herramientas de documentación fractal (`/generate_fractal_docs`, `docs/` directory, `canonical_idk.yml`) que fueron creadas en las tareas anteriores de la Fase 6.

La actualización cierra el loop entre la generación de documentación fractal (tareas 6.1-6.5) y su consumo efectivo por parte de agentes AI durante el desarrollo.

## User Story
As a **developer using a TAC Bootstrap project**
I want to **have clear guidelines on when to use fractal documentation tools**
So that **AI agents automatically maintain synchronized documentation and use canonical terminology**

## Problem Statement
Las tareas 6.1-6.5 implementaron generadores de documentación fractal (`gen_docstring_jsdocs.py`, `gen_docs_fractal.py`, `/generate_fractal_docs` command, `canonical_idk.yml`), pero no hay guía explícita para que los agentes AI sepan cuándo consultar o regenerar esta documentación.

Sin estas reglas condicionales, los agentes pueden:
- Olvidar actualizar la documentación fractal después de agregar nuevos módulos
- No saber que existe el directorio `docs/` con documentación estructurada
- No utilizar el vocabulario canónico de `canonical_idk.yml` en docstrings
- No regenerar documentación después de refactorings

## Solution Statement
Agregar una nueva sección `## Fractal Documentation` al template `conditional_docs.md.j2` con cuatro reglas condicionales claras:

1. **Cuando trabajar con documentación o entender estructura de código**: Leer `docs/` directory
2. **Cuando crear nuevos módulos/capabilities**: Correr `/generate_fractal_docs changed` post-implementación
3. **Cuando refactorear o mover archivos**: Correr `/generate_fractal_docs full` y revisar `docs/`
4. **Cuando buscar terminología canónica**: Leer `canonical_idk.yml` para keywords aprobados

El template usa la variable Jinja2 `{{ config.paths.app_root | default("src") }}` para referencias de paths parametrizadas.

Como TAC Bootstrap sirve doble propósito (generador + referencia), también se actualiza `.claude/commands/conditional_docs.md` en la raíz con el contenido renderizado, permitiendo que el proyecto bootstrap mismo use estas reglas.

## Relevant Files
Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2` - Template Jinja2 a modificar (agregar sección al final)
- `.claude/commands/conditional_docs.md` - Archivo renderizado en raíz del proyecto bootstrap a actualizar (dual-purpose: generator + reference)
- `config.yml` - Configuración del proyecto con `config.paths.app_root` (para contexto de variable Jinja2)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Servicio que renderiza templates (para entender sistema de templates, no modificar)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Repository de templates (para entender sistema de renderizado, no modificar)

### New Files
Ningún archivo nuevo - solo modificaciones a archivos existentes.

## Implementation Plan

### Phase 1: Foundation
Leer y entender la estructura actual del template `conditional_docs.md.j2` para asegurar que la nueva sección no rompa el formato existente. Verificar que el archivo renderizado `.claude/commands/conditional_docs.md` existe y puede ser actualizado.

### Phase 2: Core Implementation
1. Modificar template `conditional_docs.md.j2`: Agregar sección `## Fractal Documentation` al final con las cuatro reglas condicionales especificadas.
2. Actualizar archivo renderizado `.claude/commands/conditional_docs.md` en raíz: Agregar la misma sección al final (sin variables Jinja2, usando paths concretos del proyecto bootstrap).

### Phase 3: Integration
Verificar que las referencias a `/generate_fractal_docs`, `docs/`, y `canonical_idk.yml` son consistentes con las features implementadas en tareas 6.1-6.5. Confirmar que las variables Jinja2 usan el formato correcto con default filter.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Leer templates y archivos existentes
- Leer `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2` completo para entender formato actual
- Leer `.claude/commands/conditional_docs.md` completo para entender contenido renderizado actual
- Verificar que el formato markdown es consistente en ambos archivos

### Task 2: Modificar template Jinja2 con sección Fractal Documentation
- Abrir `conditional_docs.md.j2` con Edit tool
- Agregar nueva sección `## Fractal Documentation` al final del template
- Incluir las cuatro reglas condicionales especificadas en el issue:
  - Rule 1: When working with documentation (read `docs/`)
  - Rule 2: When creating new modules (run `/generate_fractal_docs changed`)
  - Rule 3: When refactoring (run `/generate_fractal_docs full`)
  - Rule 4: When looking for canonical terminology (read `canonical_idk.yml`)
- Usar variable Jinja2: `{{ config.paths.app_root | default("src") }}`
- Preservar todo el contenido existente del template

### Task 3: Actualizar archivo renderizado en raíz del proyecto bootstrap
- Abrir `.claude/commands/conditional_docs.md` con Edit tool
- Agregar nueva sección `## Fractal Documentation` al final del archivo
- Incluir las cuatro reglas condicionales (sin variables Jinja2, usando `tac_bootstrap_cli` en lugar de la variable)
- Preservar todo el contenido existente del archivo

### Task 4: Validar formato y consistencia
- Verificar que la sintaxis markdown es correcta en ambos archivos
- Confirmar que las referencias a comandos (`/generate_fractal_docs`), archivos (`canonical_idk.yml`), y directorios (`docs/`) son consistentes
- Verificar que la nueva sección no rompe el formato existente (niveles de heading correctos, bullets consistentes)

### Task 5: Ejecutar Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
No se requieren tests unitarios específicos para esta tarea ya que solo se están agregando reglas de documentación en formato markdown a templates. La validación se hace mediante:
1. Smoke test del CLI (comando `--help`)
2. Inspección manual del contenido de los archivos modificados
3. Verificación de sintaxis markdown (implícita en la lectura del archivo)

### Edge Cases
- Template con contenido existente: Verificar que agregar al final no rompe formato
- Variables Jinja2 con default filter: Confirmar sintaxis correcta `{{ var | default("value") }}`
- Referencias a comandos inexistentes en proyectos sin Fase 6: Aceptable - reglas condicionales "When looking for..." solo aplican si el archivo/comando existe
- Proyectos con `app_root` no definido: Variable usa default `"src"` de forma segura

## Acceptance Criteria
- [ ] Template `conditional_docs.md.j2` tiene nueva sección `## Fractal Documentation` al final
- [ ] Sección incluye las cuatro reglas condicionales especificadas (documentation, new modules, refactoring, canonical terminology)
- [ ] Referencias a paths usan variable Jinja2 con default: `{{ config.paths.app_root | default("src") }}`
- [ ] Archivo `.claude/commands/conditional_docs.md` en raíz tiene nueva sección agregada al final
- [ ] Formato markdown es consistente en ambos archivos (sin errores de sintaxis)
- [ ] Contenido existente de ambos archivos está preservado sin cambios
- [ ] Validation commands pasan sin errores (pytest, ruff, mypy, --help)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
**Dual-Purpose Pattern**: TAC Bootstrap sirve como generador y referencia. Por eso actualizamos tanto el template Jinja2 (para proyectos generados) como el archivo renderizado en raíz (para el proyecto bootstrap mismo).

**No Validation Needed**: Las reglas condicionales no requieren validación de existencia de comandos o archivos porque son guidelines contextuales. Si `/generate_fractal_docs` no existe en un proyecto, la condición "When creating new modules" simplemente no aplica. Los agentes AI son suficientemente inteligentes para manejar casos de archivos/comandos faltantes.

**Fase 6 Completion**: Esta es la tarea final de la Fase 6 (Documentación Fractal como Skill). Una vez completada, los proyectos generados incluyen:
- Generadores de docstrings IDK (task 6.1)
- Generador de documentación fractal bottom-up (task 6.2)
- Orchestrator de generadores (task 6.3)
- Slash command `/generate_fractal_docs` (task 6.4)
- Vocabulario canónico `canonical_idk.yml` (task 6.5)
- **Reglas condicionales para uso efectivo** (task 6.6 - esta tarea)

**Future Work**: Considerar agregar reglas condicionales similares para comandos relacionados a documentación en `constitution.md` template para reforzar el uso de fractal docs como principio de desarrollo.
