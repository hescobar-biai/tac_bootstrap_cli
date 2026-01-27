# Feature: Crear template t_metaprompt_workflow.md.j2 para generar prompts

## Metadata
issue_number: `307`
adw_id: `feature_Tac_10_task_2`
issue_json: `{"number":307,"title":"Crear template t_metaprompt_workflow.md.j2 para generar prompts","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_10_task_2\n\n\n- **Descripción**: Crear un meta-prompt (Level 6) que genera nuevos prompts siguiendo el formato consistente de TAC. Incluye documentación de referencia y un Specified Format template.\n- **Archivos**:\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/t_metaprompt_workflow.md`\n- **Contenido**:\n  - Frontmatter con allowed-tools (Write, Edit, WebFetch, Task)\n  - Variables: HIGH_LEVEL_PROMPT ($ARGUMENTS)\n  - Documentation links para slash commands\n  - Specified Format template con estructura estándar (metadata, variables, workflow, report)\n- **Nota**: El template .j2 usa variables Jinja2, el archivo .md es la versión renderizada para uso directo\n"}`

## Feature Description
Crear un meta-prompt (Level 6 en la jerarquía de abstracción de TAC) que genera nuevos prompts siguiendo el formato consistente del framework TAC. Este comando toma una descripción de alto nivel de la necesidad del usuario y produce un prompt estructurado completo con frontmatter, variables, workflow y formato de reporte. El meta-prompt incluye documentación de referencia a comandos slash existentes y un template de formato especificado para guiar la generación.

El template debe existir en dos formas:
1. **Template Jinja2 (.j2)**: Fuente autorizada para el generador TAC Bootstrap CLI, con variables Jinja2 interpolables
2. **Archivo renderizado (.md)**: Versión completamente renderizada para uso directo en este repositorio (dogfooding)

## User Story
As a TAC Bootstrap user or maintainer
I want to generate new prompt templates that follow TAC standards
So that I can quickly create consistent, well-structured prompts without starting from scratch

## Problem Statement
Crear nuevos prompts para comandos slash requiere:
- Conocer la estructura exacta del formato TAC (frontmatter, variables, workflow, report)
- Mantener consistencia con prompts existentes
- Incluir la documentación de referencia apropiada
- Seguir convenciones de nomenclatura y sintaxis
- Recordar todos los campos obligatorios y opcionales

Actualmente no existe una herramienta que automatice la generación de prompts siguiendo el formato estándar de TAC.

## Solution Statement
Crear un meta-prompt `/t_metaprompt_workflow` que:
- Acepta una descripción de alto nivel del prompt deseado (HIGH_LEVEL_PROMPT)
- Genera un prompt completo con estructura TAC estándar
- Incluye frontmatter con allowed-tools configurables
- Provee links de documentación a comandos slash comunes
- Usa un "Specified Format template" con 4 secciones: metadata, variables, workflow, report
- Incluye un ejemplo simple para ilustrar el formato
- Es genérico y reutilizable para cualquier tipo de prompt

## Relevant Files
Archivos necesarios para implementar la feature:

- `.claude/commands/feature.md` - Referencia de estructura de prompt existente con frontmatter y workflow
- `.claude/commands/parallel_subagents.md` - Referencia de estructura de prompt con variables y report format
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Template Jinja2 para ver patrón de variables
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` - Template Jinja2 con frontmatter y variables
- `ai_docs/doc/Tac-10_1.md` - Documentación de niveles de abstracción (Level 6)
- `ai_docs/doc/plan_tasks_Tac_10.md` - Especificación detallada de la Tarea 2
- `.claude/commands/` - Directorio con 25+ comandos slash para referencias de documentación

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2` - Template Jinja2 con variables interpolables
- `.claude/commands/t_metaprompt_workflow.md` - Versión renderizada para uso directo en este repo

## Implementation Plan

### Phase 1: Foundation
Investigar patrones existentes y estructura de meta-prompts:
- Revisar estructura de frontmatter en prompts existentes
- Identificar comandos slash comunes para links de documentación
- Analizar formato de variables con sintaxis $SYNTAX
- Entender estructura estándar de workflow (pasos numerados)
- Revisar formatos de report en prompts existentes

### Phase 2: Core Implementation
Crear ambos archivos del template:
1. Crear template Jinja2 (.j2) con variables interpolables
2. Crear versión .md renderizada para dogfooding

### Phase 3: Integration
Verificar que el meta-prompt funciona correctamente:
- Tests de renderizado del template
- Validación de formato y estructura
- Smoke test generando un prompt simple

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Investigar patrones de prompts existentes
- Leer `.claude/commands/feature.md` para ver estructura completa de prompt
- Leer `.claude/commands/parallel_subagents.md` para ver frontmatter y formato de variables
- Leer `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` para ver uso de variables Jinja2
- Leer `ai_docs/doc/plan_tasks_Tac_10.md` para ver especificación de Tarea 2
- Identificar comandos slash comunes en `.claude/commands/` para documentación (feature, implement, test, review, commit)

### Task 2: Crear template Jinja2 t_metaprompt_workflow.md.j2
- Crear archivo en `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2`
- Incluir frontmatter minimal con:
  - `allowed-tools`: ["Write", "Edit", "WebFetch", "Task"]
- Crear introducción explicando que es un meta-prompt Level 6
- Definir sección Variables:
  - `HIGH_LEVEL_PROMPT`: $ARGUMENTS (descripción del prompt a generar)
- Crear sección Instructions con:
  - Explicación de qué es un meta-prompt y su propósito
  - Instrucción de esperar $ARGUMENTS como input
  - Guía para interpretar HIGH_LEVEL_PROMPT y generar estructura completa
- Crear sección Documentation con links locales:
  - `.claude/commands/feature.md` - Feature planning
  - `.claude/commands/implement.md` - Implementation
  - `.claude/commands/test.md` - Testing
  - `.claude/commands/review.md` - Review
  - `.claude/commands/commit.md` - Git commits
- Crear sección Specified Format Template con estructura:
  - **Metadata section**: Purpose, context, level
  - **Variables section**: Input variables with $SYNTAX, descriptions, defaults
  - **Workflow section**: Numbered steps with clear actions
  - **Report section**: Expected output format and deliverables
- Incluir un ejemplo simple (e.g., "crear función de validación") mostrando formato completo
- Mantener el template genérico y reutilizable

### Task 3: Crear versión renderizada t_metaprompt_workflow.md
- Crear archivo en `.claude/commands/t_metaprompt_workflow.md`
- Copiar contenido del template .j2 pero sin sintaxis Jinja2
- Mantener estructura idéntica al template
- Este archivo es la versión "dogfooded" para uso directo
- Verificar consistencia con el template .j2

### Task 4: Verificar templates contra especificación
- Comparar con estructura de `feature.md` y `parallel_subagents.md` para consistencia
- Verificar que frontmatter es válido YAML
- Confirmar que Variable HIGH_LEVEL_PROMPT está bien definida
- Validar que Specified Format template tiene las 4 secciones
- Confirmar que ejemplo es claro y simple
- Verificar que links de documentación son rutas relativas válidas

### Task 5: Ejecutar validation commands
- Ejecutar todos los comandos de validación para verificar cero regresiones
- Opcionalmente hacer smoke test generando un prompt simple

## Testing Strategy

### Unit Tests
- Test de renderizado del template Jinja2 con config por defecto
- Test de que frontmatter se parsea correctamente (YAML válido)
- Test de que variables se interpolan correctamente
- Test de estructura de secciones (Variables, Instructions, Documentation, Specified Format, Example)
- Test de que links de documentación apuntan a archivos existentes

### Edge Cases
- HIGH_LEVEL_PROMPT vacío (debe instruir al agente a pedir input)
- Descripción muy vaga vs muy específica (template debe ser flexible)
- Generación de diferentes tipos de prompts (workflow, delegation, research)

## Acceptance Criteria
- El template Jinja2 `t_metaprompt_workflow.md.j2` existe y es válido sintácticamente
- El archivo renderizado `t_metaprompt_workflow.md` existe y es funcional
- Ambos archivos tienen frontmatter minimal con `allowed-tools` únicamente
- La variable HIGH_LEVEL_PROMPT está definida como $ARGUMENTS
- Incluye sección Documentation con links locales a 5+ comandos comunes
- El Specified Format Template tiene exactamente 4 secciones: metadata, variables, workflow, report
- Incluye un ejemplo simple y completo mostrando el formato
- El template es genérico y no incluye variables específicas de proyecto (como config.project.name)
- Incluye nota explicando que es un meta-prompt Level 6
- Los links de documentación usan rutas relativas a `.claude/commands/`
- El formato es consistente con otros templates existentes
- Los comandos de validación pasan sin regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Este comando implementa Level 6 de TAC-10 (meta-prompt que genera prompts)
- El término "meta-prompt" indica que es un prompt cuyo output es otro prompt
- La simplicidad del frontmatter (solo allowed-tools) evita complejidad innecesaria
- Links locales a `.claude/commands/` son más confiables que URLs externas
- El Specified Format Template con 4 secciones proporciona estructura clara sin ser demasiado prescriptivo
- HIGH_LEVEL_PROMPT como única variable mantiene el meta-prompt genérico y flexible
- El ejemplo debe ser simple (e.g., función de validación) para ilustrar sin saturar
- La naturaleza genérica permite usar este meta-prompt para cualquier tipo de prompt (workflow, delegation, research, etc.)
- Al igual que parallel_subagents, mantener doble naturaleza: .j2 para generador + .md para dogfooding
- El meta-prompt no valida input - delega al agente manejar casos edge naturalmente
- Mantener consistencia con naming: t_metaprompt_workflow (prefijo 't_' indica template generator)
